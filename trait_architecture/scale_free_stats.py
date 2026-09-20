"""Scale-free numerical helpers for standardized empirical statistics.

These helpers deliberately avoid fixed thresholds expressed in the physical
units of the input variable. Degeneracy is defined by exact lack of variation;
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


def relative_range(values: Sequence[float]) -> float:
    """Return `(max-min)/abs(mean)` without a measurement-unit floor.

    A common positive rescaling of the values leaves the result unchanged. If
    the center is exactly zero, an exactly constant range is zero and any
    nonzero range is unbounded.
    """

    if not values:
        raise ValueError("relative range requires at least one value")
    numeric = [float(value) for value in values]
    if not all(math.isfinite(value) for value in numeric):
        raise ValueError("relative range requires finite values")
    span = max(numeric) - min(numeric)
    center = mean(numeric)
    if center == 0.0:
        return 0.0 if span == 0.0 else math.inf
    return span / abs(center)


def pooled_sample_sd(first: Sequence[float], second: Sequence[float]) -> float:
    """Sample-size-weighted pooled SD for two independent groups."""

    if len(first) < 2 or len(second) < 2:
        raise ValueError("pooled SD requires at least two observations per group")
    s_first = sample_sd(first)
    s_second = sample_sd(second)
    df = len(first) + len(second) - 2
    variance = (
        (len(first) - 1) * s_first * s_first
        + (len(second) - 1) * s_second * s_second
    ) / df
    return math.sqrt(max(0.0, variance))


def hedges_small_sample_correction(df: float) -> float:
    """Approximate Hedges J correction used elsewhere in BITA."""

    if df <= 1:
        raise ValueError("Hedges correction requires df > 1")
    return 1.0 - 3.0 / (4.0 * df - 1.0)


def standardized_mean_difference(
    first: Sequence[float],
    second: Sequence[float],
    *,
    absolute: bool = False,
) -> float:
    """Return Cohen's d using the sample-size-weighted pooled sample SD.

    This function is used for randomization/manipulation balance diagnostics,
    where the uncorrected standardized mean difference is the intended object.
    Use hedges_g for a small-sample bias-corrected effect size.

    If both groups are exactly constant, equal means give zero and unequal
    means give an infinite standardized difference. No fixed threshold in
    measurement units is used.
    """

    if not first or not second:
        raise ValueError("standardized mean difference requires two non-empty groups")
    if len(first) < 2 or len(second) < 2:
        raise ValueError("standardized mean difference requires at least two observations per group")
    pooled = pooled_sample_sd(first, second)
    difference = mean(second) - mean(first)
    if pooled == 0.0:
        if difference == 0.0:
            return 0.0
        result = math.copysign(math.inf, difference)
    else:
        result = difference / pooled
    return abs(result) if absolute else result


def hedges_g(
    first: Sequence[float],
    second: Sequence[float],
    *,
    absolute: bool = False,
) -> float:
    """Return small-sample bias-corrected standardized mean difference."""

    d = standardized_mean_difference(first, second, absolute=False)
    if not math.isfinite(d):
        result = d
    else:
        df = len(first) + len(second) - 2
        result = hedges_small_sample_correction(float(df)) * d
    return abs(result) if absolute else result

