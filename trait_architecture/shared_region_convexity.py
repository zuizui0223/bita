from __future__ import annotations

from dataclasses import dataclass
from math import isinf


@dataclass(frozen=True)
class SharedChordCertificate:
    shared_endpoints: bool
    hidden_bita_excluded: bool
    segment_margin_upper: float


@dataclass(frozen=True)
class ChordConvexityAudit:
    chord_upper_bound: float
    residual: float
    convexity_violated: bool


@dataclass(frozen=True)
class StrongConvexChordAudit:
    chord_value: float
    sag_lower: float
    sag_upper: float
    observed_sag: float
    violates_lower: bool
    violates_upper: bool


@dataclass(frozen=True)
class IntervalSagClassification:
    possible_sag_lower: float
    possible_sag_upper: float
    required_sag_lower: float
    required_sag_upper: float
    classification: str


def convex_chord_margin_upper(*, margin0: float, margin1: float, t: float) -> float:
    if not 0.0 <= t <= 1.0:
        raise ValueError("t must lie in [0, 1]")
    return (1.0 - t) * float(margin0) + t * float(margin1)


def certify_shared_chord(*, margin0: float, margin1: float) -> SharedChordCertificate:
    shared = margin0 <= 0.0 and margin1 <= 0.0
    return SharedChordCertificate(
        shared_endpoints=shared,
        hidden_bita_excluded=shared,
        segment_margin_upper=max(float(margin0), float(margin1)),
    )


def audit_joint_convexity_chord(
    *,
    margin0: float,
    margin1: float,
    observed_margin: float,
    t: float,
    tolerance: float = 0.0,
) -> ChordConvexityAudit:
    if tolerance < 0.0:
        raise ValueError("tolerance must be nonnegative")
    upper = convex_chord_margin_upper(margin0=margin0, margin1=margin1, t=t)
    residual = float(observed_margin) - upper
    return ChordConvexityAudit(
        chord_upper_bound=upper,
        residual=residual,
        convexity_violated=residual > tolerance,
    )


def strong_convex_sag_bounds(
    *,
    curvature_lower: float,
    curvature_upper: float,
    t: float,
    metric_distance_sq: float = 1.0,
) -> tuple[float, float]:
    if not 0.0 <= t <= 1.0:
        raise ValueError("t must lie in [0, 1]")
    if curvature_lower < 0.0 or curvature_upper < curvature_lower:
        raise ValueError("curvature bounds must satisfy 0 <= lower <= upper")
    if metric_distance_sq < 0.0:
        raise ValueError("metric_distance_sq must be nonnegative")
    factor = 0.5 * t * (1.0 - t) * metric_distance_sq
    upper = float("inf") if isinf(curvature_upper) and factor > 0.0 else curvature_upper * factor
    if factor == 0.0:
        upper = 0.0
    return curvature_lower * factor, upper


def audit_strong_convex_chord(
    *,
    margin0: float,
    margin1: float,
    observed_margin: float,
    t: float,
    curvature_lower: float,
    curvature_upper: float,
    metric_distance_sq: float = 1.0,
    tolerance: float = 0.0,
) -> StrongConvexChordAudit:
    if tolerance < 0.0:
        raise ValueError("tolerance must be nonnegative")
    chord = convex_chord_margin_upper(margin0=margin0, margin1=margin1, t=t)
    lower, upper = strong_convex_sag_bounds(
        curvature_lower=curvature_lower,
        curvature_upper=curvature_upper,
        t=t,
        metric_distance_sq=metric_distance_sq,
    )
    sag = chord - float(observed_margin)
    return StrongConvexChordAudit(
        chord_value=chord,
        sag_lower=lower,
        sag_upper=upper,
        observed_sag=sag,
        violates_lower=sag < lower - tolerance,
        violates_upper=sag > upper + tolerance,
    )


def interval_convex_sag_bounds(
    *,
    margin0_lower: float,
    margin0_upper: float,
    margin1_lower: float,
    margin1_upper: float,
    interior_lower: float,
    interior_upper: float,
    t: float,
) -> tuple[float, float]:
    if not 0.0 <= t <= 1.0:
        raise ValueError("t must lie in [0, 1]")
    if margin0_lower > margin0_upper or margin1_lower > margin1_upper or interior_lower > interior_upper:
        raise ValueError("each interval must satisfy lower <= upper")

    possible_lower = (
        (1.0 - t) * float(margin0_lower)
        + t * float(margin1_lower)
        - float(interior_upper)
    )
    possible_upper = (
        (1.0 - t) * float(margin0_upper)
        + t * float(margin1_upper)
        - float(interior_lower)
    )
    return possible_lower, possible_upper


def classify_interval_convex_chord(
    *,
    margin0_lower: float,
    margin0_upper: float,
    margin1_lower: float,
    margin1_upper: float,
    interior_lower: float,
    interior_upper: float,
    t: float,
    curvature_lower: float = 0.0,
    curvature_upper: float = float("inf"),
    metric_distance_sq: float = 1.0,
) -> IntervalSagClassification:
    possible_lower, possible_upper = interval_convex_sag_bounds(
        margin0_lower=margin0_lower,
        margin0_upper=margin0_upper,
        margin1_lower=margin1_lower,
        margin1_upper=margin1_upper,
        interior_lower=interior_lower,
        interior_upper=interior_upper,
        t=t,
    )
    required_lower, required_upper = strong_convex_sag_bounds(
        curvature_lower=curvature_lower,
        curvature_upper=curvature_upper,
        t=t,
        metric_distance_sq=metric_distance_sq,
    )

    if possible_upper < required_lower:
        classification = "LOWER_BOUND_VIOLATED"
    elif possible_lower > required_upper:
        classification = "UPPER_BOUND_VIOLATED"
    elif possible_lower >= required_lower and possible_upper <= required_upper:
        classification = "IDENTIFIED_WITHIN_INTERVALS"
    else:
        classification = "UNRESOLVED"

    return IntervalSagClassification(
        possible_sag_lower=possible_lower,
        possible_sag_upper=possible_upper,
        required_sag_lower=required_lower,
        required_sag_upper=required_upper,
        classification=classification,
    )


def certify_interval_shared_chord(
    *,
    margin0_upper: float,
    margin1_upper: float,
) -> SharedChordCertificate:
    shared = margin0_upper <= 0.0 and margin1_upper <= 0.0
    return SharedChordCertificate(
        shared_endpoints=shared,
        hidden_bita_excluded=shared,
        segment_margin_upper=max(float(margin0_upper), float(margin1_upper)),
    )
