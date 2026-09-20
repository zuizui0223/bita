"""Dependency-free distribution helpers for small-sample inference."""
from __future__ import annotations

import math


def _log_beta(a: float, b: float) -> float:
    return math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)


def _betacf(a: float, b: float, x: float) -> float:
    tiny = 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < tiny:
        d = tiny
    d = 1.0 / d
    h = d
    for m in range(1, 300):
        m2 = 2 * m
        numerator = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + numerator * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + numerator / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        h *= d * c
        numerator = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + numerator * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + numerator / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-14:
            break
    return h


def regularized_incomplete_beta(a: float, b: float, x: float) -> float:
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    front = math.exp(a * math.log(x) + b * math.log1p(-x) - _log_beta(a, b))
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _betacf(a, b, x) / a
    return (
        1.0
        - math.exp(b * math.log1p(-x) + a * math.log(x) - _log_beta(b, a))
        * _betacf(b, a, 1.0 - x)
        / b
    )


def student_t_two_sided_p(t_value: float, df: float) -> float:
    if df <= 0:
        raise ValueError("degrees of freedom must be positive")
    if not math.isfinite(t_value):
        raise ValueError("t value must be finite")
    x = df / (df + t_value * t_value)
    return regularized_incomplete_beta(df / 2.0, 0.5, x)


def student_t_quantile_975(df: float) -> float:
    if df <= 0:
        raise ValueError("degrees of freedom must be positive")
    low, high = 0.0, 2000.0
    for _ in range(200):
        middle = 0.5 * (low + high)
        if student_t_two_sided_p(middle, df) > 0.05:
            low = middle
        else:
            high = middle
    return 0.5 * (low + high)
