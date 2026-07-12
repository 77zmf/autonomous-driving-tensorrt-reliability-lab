"""Build machine-readable JSON and human-readable Markdown reports."""

from __future__ import annotations

import json
from collections import defaultdict
from typing import Dict, Iterable, List, Mapping, Union

from .samples import Sample
from .statistics import summarize_values


ReportValue = Union[int, float]
Summary = Dict[str, ReportValue]
METRIC_COLUMNS = ("count", "min", "max", "mean", "median", "p50", "p90", "p95", "p99")


def build_report(samples: Iterable[Sample]) -> Dict[str, object]:
    """Aggregate samples independently by component.

    Latencies from different pipeline scopes are deliberately never combined:
    an aggregate of, for example, ``inference`` and ``end_to_end`` has no
    meaningful engineering interpretation.
    """

    materialized = list(samples)
    if not materialized:
        raise ValueError("cannot build a report without samples")

    grouped = defaultdict(list)
    for sample in materialized:
        grouped[sample.component].append(sample.latency_ms)

    return {
        "schema_version": 1,
        "metric": "latency_ms",
        "unit": "milliseconds",
        "components": {
            component: summarize_values(grouped[component])
            for component in sorted(grouped)
        },
    }


def render_json(report: Mapping[str, object]) -> str:
    """Serialize a report as stable, pretty-printed JSON."""

    return json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n"


def _format_value(value: ReportValue) -> str:
    if isinstance(value, int):
        return str(value)
    return format(value, ".9g")


def _markdown_row(label: str, summary: Mapping[str, ReportValue]) -> str:
    values = [_format_value(summary[column]) for column in METRIC_COLUMNS]
    return "| " + " | ".join([label, *values]) + " |"


def render_markdown(report: Mapping[str, object]) -> str:
    """Render a compact Markdown table with one independent component per row."""

    components = report["components"]
    if not isinstance(components, Mapping):
        raise ValueError("report does not contain a valid components section")

    title_columns = ["Component", *(column.upper() for column in METRIC_COLUMNS)]
    lines: List[str] = [
        "# TensorRT Reliability Benchmark Report",
        "",
        "Metric: `latency_ms` (milliseconds)",
        "",
        "| " + " | ".join(title_columns) + " |",
        "| " + " | ".join(["---", *("---:" for _ in METRIC_COLUMNS)]) + " |",
    ]
    for component in sorted(components):
        summary = components[component]
        if not isinstance(summary, Mapping):
            raise ValueError(f"component {component!r} does not contain a summary")
        lines.append(_markdown_row(str(component), summary))
    return "\n".join(lines) + "\n"
