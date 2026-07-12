"""Command-line entry point for benchmark report generation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from .report import build_report, render_json, render_markdown
from .samples import SampleValidationError, load_samples, parse_stream


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trt-reliability-report",
        description="Summarize per-iteration latency samples from JSONL or CSV.",
    )
    parser.add_argument("input", help="input .jsonl/.ndjson/.csv file, or - for stdin")
    parser.add_argument(
        "--input-format",
        choices=("auto", "jsonl", "csv"),
        default="auto",
        help="input format (default: infer from filename)",
    )
    parser.add_argument(
        "-f",
        "--format",
        dest="output_format",
        choices=("json", "markdown"),
        default="json",
        help="report format (default: json)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="-",
        help="output file, or - for stdout (default: -)",
    )
    return parser


def _load(args: argparse.Namespace):
    if args.input == "-":
        if args.input_format == "auto":
            raise ValueError("--input-format is required when reading from stdin")
        return parse_stream(sys.stdin, args.input_format)

    input_format = None if args.input_format == "auto" else args.input_format
    return load_samples(args.input, input_format)


def _write_output(output: str, content: str) -> None:
    if output == "-":
        sys.stdout.write(content)
        return
    Path(output).write_text(content, encoding="utf-8")


def main(argv: Optional[List[str]] = None) -> int:
    """Run the CLI and return a process exit code."""

    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        report = build_report(_load(args))
        content = (
            render_json(report)
            if args.output_format == "json"
            else render_markdown(report)
        )
        _write_output(args.output, content)
    except (OSError, SampleValidationError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    return 0
