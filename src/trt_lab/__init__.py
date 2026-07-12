"""CPU-verifiable benchmark parsing, statistics, and reporting utilities."""

from .report import build_report, render_json, render_markdown
from .samples import Sample, SampleValidationError, load_samples, parse_stream
from .statistics import percentile, summarize_values

__all__ = [
    "Sample",
    "SampleValidationError",
    "build_report",
    "load_samples",
    "parse_stream",
    "percentile",
    "render_json",
    "render_markdown",
    "summarize_values",
]

__version__ = "0.1.0"
