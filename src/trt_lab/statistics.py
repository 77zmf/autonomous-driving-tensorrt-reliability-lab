"""Dependency-free deterministic statistics for latency samples."""

from __future__ import annotations

import math
from typing import Dict, Iterable, List, Sequence


def _validated_values(values: Iterable[float]) -> List[float]:
    materialized = []
    for value in values:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("statistics require numeric values")
        parsed = float(value)
        if not math.isfinite(parsed) or parsed < 0:
            raise ValueError("statistics require non-negative finite values")
        materialized.append(parsed)
    if not materialized:
        raise ValueError("statistics require at least one value")
    return materialized


def _percentile_from_sorted(sorted_values: Sequence[float], probability: float) -> float:
    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability must be between 0 and 1")
    if len(sorted_values) == 1:
        return float(sorted_values[0])

    position = (len(sorted_values) - 1) * probability
    lower_index = math.floor(position)
    upper_index = math.ceil(position)
    lower = float(sorted_values[lower_index])
    upper = float(sorted_values[upper_index])
    if lower_index == upper_index:
        return lower
    return lower + (upper - lower) * (position - lower_index)


def percentile(values: Iterable[float], probability: float) -> float:
    """Return a linearly interpolated percentile (R-7/NumPy default method)."""

    sorted_values = sorted(_validated_values(values))
    return _percentile_from_sorted(sorted_values, probability)


def summarize_values(values: Iterable[float]) -> Dict[str, float]:
    """Compute the report's fixed set of descriptive statistics."""

    sorted_values = sorted(_validated_values(values))
    count = len(sorted_values)
    p50 = _percentile_from_sorted(sorted_values, 0.50)
    return {
        "count": count,
        "min": sorted_values[0],
        "max": sorted_values[-1],
        "mean": math.fsum(sorted_values) / count,
        "median": p50,
        "p50": p50,
        "p90": _percentile_from_sorted(sorted_values, 0.90),
        "p95": _percentile_from_sorted(sorted_values, 0.95),
        "p99": _percentile_from_sorted(sorted_values, 0.99),
    }
