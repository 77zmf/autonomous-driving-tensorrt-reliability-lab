"""Load and strictly validate per-iteration benchmark samples."""

from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import IO, Iterable, List, Mapping, Optional, Union


PathLike = Union[str, Path]
SUPPORTED_SUFFIXES = {
    ".csv": "csv",
    ".jsonl": "jsonl",
    ".ndjson": "jsonl",
}
REQUIRED_FIELDS = ("iteration", "component", "latency_ms")


class SampleValidationError(ValueError):
    """Raised when benchmark input does not match the sample schema."""


@dataclass(frozen=True)
class Sample:
    """One latency measurement for a component at a given iteration."""

    iteration: int
    component: str
    latency_ms: float


def _fail(location: str, message: str) -> SampleValidationError:
    return SampleValidationError(f"{location}: {message}")


def _parse_iteration(value: object, location: str) -> int:
    if isinstance(value, bool):
        raise _fail(location, "iteration must be a non-negative integer")

    if isinstance(value, int):
        parsed = value
    elif isinstance(value, str):
        try:
            parsed = int(value.strip())
        except (TypeError, ValueError):
            raise _fail(location, "iteration must be a non-negative integer") from None
    else:
        raise _fail(location, "iteration must be a non-negative integer")

    if parsed < 0:
        raise _fail(location, "iteration must be a non-negative integer")
    return parsed


def _parse_component(value: object, location: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise _fail(location, "component must be a non-empty string")
    return value.strip()


def _parse_latency(value: object, location: str) -> float:
    if isinstance(value, bool) or value is None:
        raise _fail(location, "latency_ms must be a non-negative finite number")

    if isinstance(value, (int, float)):
        parsed = float(value)
    elif isinstance(value, str):
        try:
            parsed = float(value.strip())
        except (TypeError, ValueError):
            raise _fail(
                location, "latency_ms must be a non-negative finite number"
            ) from None
    else:
        raise _fail(location, "latency_ms must be a non-negative finite number")

    if not math.isfinite(parsed) or parsed < 0:
        raise _fail(location, "latency_ms must be a non-negative finite number")
    return parsed


def _validate_record(record: Mapping[str, object], location: str) -> Sample:
    missing = [field for field in REQUIRED_FIELDS if field not in record]
    if missing:
        raise _fail(location, f"missing required field(s): {', '.join(missing)}")

    return Sample(
        iteration=_parse_iteration(record["iteration"], location),
        component=_parse_component(record["component"], location),
        latency_ms=_parse_latency(record["latency_ms"], location),
    )


def _require_samples(samples: Iterable[Sample]) -> List[Sample]:
    materialized = list(samples)
    if not materialized:
        raise SampleValidationError("input contains no samples")
    return materialized


def parse_jsonl(stream: IO[str]) -> List[Sample]:
    """Parse newline-delimited JSON objects from *stream*."""

    samples = []
    for line_number, raw_line in enumerate(stream, start=1):
        line = raw_line.strip()
        if not line:
            continue
        location = f"JSONL line {line_number}"
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            raise _fail(location, f"invalid JSON: {error.msg}") from None
        if not isinstance(record, dict):
            raise _fail(location, "sample must be a JSON object")
        samples.append(_validate_record(record, location))
    return _require_samples(samples)


def parse_csv(stream: IO[str]) -> List[Sample]:
    """Parse benchmark samples from a CSV stream with a header row."""

    reader = csv.DictReader(stream)
    if reader.fieldnames is None:
        raise SampleValidationError("CSV input is missing a header row")
    if len(reader.fieldnames) != len(set(reader.fieldnames)):
        raise SampleValidationError("CSV header contains duplicate field names")

    missing = [field for field in REQUIRED_FIELDS if field not in reader.fieldnames]
    if missing:
        raise SampleValidationError(
            f"CSV header is missing required field(s): {', '.join(missing)}"
        )

    samples = []
    for row in reader:
        location = f"CSV line {reader.line_num}"
        if None in row:
            raise _fail(location, "row has more values than the header")
        samples.append(_validate_record(row, location))
    return _require_samples(samples)


def parse_stream(stream: IO[str], input_format: str) -> List[Sample]:
    """Parse a text stream in ``jsonl`` or ``csv`` format."""

    normalized = input_format.lower()
    if normalized == "jsonl":
        return parse_jsonl(stream)
    if normalized == "csv":
        return parse_csv(stream)
    raise ValueError(f"unsupported input format: {input_format}")


def infer_input_format(path: PathLike) -> str:
    """Infer input format from a supported filename extension."""

    suffix = Path(path).suffix.lower()
    try:
        return SUPPORTED_SUFFIXES[suffix]
    except KeyError:
        supported = ", ".join(sorted(SUPPORTED_SUFFIXES))
        raise ValueError(
            f"cannot infer input format from {path!s}; supported extensions: {supported}"
        ) from None


def load_samples(
    path: PathLike, input_format: Optional[str] = None
) -> List[Sample]:
    """Load samples from *path*, inferring format when not supplied."""

    resolved_format = input_format or infer_input_format(path)
    with Path(path).open("r", encoding="utf-8-sig", newline="") as stream:
        return parse_stream(stream, resolved_format)
