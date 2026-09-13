"""Scale-free numerical helpers for standardized empirical statistics.

These helpers deliberately avoid fixed thresholds expressed in the physical
units of the input variable.  Degeneracy is defined by exact lack of variation;
nonzero variation is normalized before sums of squares are formed so harmless
positive unit conversions do not change availability of a standardized
statistic.
"""

from __future__ import annotations

import math
from statistics import mean
from typing import Sequence


def _centered(values: Sequence[float]) -> tuple[float, list[float], float]:
    if not values:
        raise ValueError("at least one value is required")
    numeric = [float(value) for value in values]
    if not all(math.isfinite(value) for value in numeric):
        raise ValueError("standardized statistics require finite values")
    center = mean(numeric)
    deviations = [value - center for value in numeric]
    max_deviation = max(abs(value) for value in deviations)
    return center, deviations, max_deviation


def population_sd(values: Sequence[float]) -> float:
    """Return population SD using scaled deviations; fail on a constant input."""

    if len(values) < 2:
        raise ValueError("standardized contrast requires at least two observations")
    _, deviations, max_deviation = _centered(values)
    if max_deviation == 0.0:
        raise ValueError("standardized contrast is undefined for a constant outcome")
    normalized_ss = sum((value / max_deviation) ** 2 for value in deviations)
    return max_deviation * math.sqrt(normalized_ss / len(deviations))


def sample_sd(values: Sequence[float]) -> float:
    """Return sample SD using scaled deviations; constants have SD zero."""

    if len(values) < 2:
        return 0.0
    _, deviations, max_deviation = _centered(values)
    if max_deviation == 0.0:
        return 0.0
    normalized_ss = sum((value / max_deviation) ** 2 for value in deviations)
    return max_deviation * math.sqrt(normalized_ss / (len(deviations) - 1))


def zscore(values: Sequence[float]) -> list[float]:
    """Return population z scores without an input-unit absolute variance gate."""

    if len(values) < 2:
        raise ValueError("standardization requires at least two values")
    _, deviations, max_deviation = _centered(values)
    if max_deviation == 0.0:
        raise ValueError("standardization is undefined for a constant variable")
    normalized = [value / max_deviation for value in deviations]
    normalized_rms = math.sqrt(sum(value * value for value in normalized) / len(normalized))
    return [value / normalized_rms for value in normalized]


def standardized_mean_difference(
    first: Sequence[float],
    second: Sequence[float],
    *,
    absolute: bool = False,
) -> float:
    """Return (mean(second)-mean(first))/pooled sample SD.

    With ``absolute=True`` the magnitude is returned.  If both groups are
    exactly constant, equal means give zero and unequal means give an infinite
    standardized difference.  No fixed threshold in measurement units is used.
    """

    if not first or not second:
        raise ValueError("standardized mean difference requires two non-empty groups")
    s_first = sample_sd(first)
    s_second = sample_sd(second)
    pooled = math.hypot(s_first, s_second) / math.sqrt(2.0)
    difference = mean(second) - mean(first)
    if pooled == 0.0:
        if difference == 0.0:
            return 0.0
        result = math.copysign(math.inf, difference)
    else:
        result = difference / pooled
    return abs(result) if absolute else result
