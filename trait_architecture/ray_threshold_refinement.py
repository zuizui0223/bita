from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RayThresholdRefinement:
    raw_lower: float
    raw_upper: float
    chord_lower: float
    secant_upper: float
    refined_lower: float
    refined_upper: float
    previous_slope: float
    crossing_slope: float
    convexity_ok: bool


def refine_convex_ray_threshold(
    *,
    t0: float,
    t1: float,
    t2: float,
    m0: float,
    m1: float,
    m2: float,
    tolerance: float = 1e-12,
) -> RayThresholdRefinement:
    """Refine a BITA fixed-ray crossing bracket from three sampled margins.

    Requires ``t0<t1<t2`` and the sign/order pattern ``m0<=m1<0<m2``.
    Under a non-decreasing convex ray, the chord zero across the straddling
    pair is a lower bound on the true critical dose. The preceding secant gives
    an upper bound when it has positive slope; otherwise the positive sample
    itself remains the upper bound.
    """

    if tolerance < 0:
        raise ValueError("tolerance must be nonnegative")
    if not (t0 < t1 < t2):
        raise ValueError("require t0 < t1 < t2")
    if m0 > m1 + tolerance:
        raise ValueError("require m0 <= m1 under the monotone ray model")
    if not (m1 < -tolerance and m2 > tolerance):
        raise ValueError("require a negative m1 and positive m2 crossing pair")

    s01 = (m1 - m0) / (t1 - t0)
    s12 = (m2 - m1) / (t2 - t1)
    convexity_ok = s01 <= s12 + tolerance
    if not convexity_ok:
        raise ValueError("sampled secant slopes violate convexity: s01 > s12")
    if s12 <= 0:
        raise ValueError("crossing secant slope must be positive")

    chord_lower = t1 - m1 / s12
    if s01 > tolerance:
        secant_upper = min(t2, t1 - m1 / s01)
    else:
        secant_upper = t2

    refined_lower = max(t1, chord_lower)
    refined_upper = min(t2, secant_upper)
    if refined_lower > refined_upper + tolerance:
        raise ValueError("refined interval is internally inconsistent")

    return RayThresholdRefinement(
        raw_lower=t1,
        raw_upper=t2,
        chord_lower=chord_lower,
        secant_upper=secant_upper,
        refined_lower=refined_lower,
        refined_upper=refined_upper,
        previous_slope=s01,
        crossing_slope=s12,
        convexity_ok=True,
    )
