from __future__ import annotations

from dataclasses import dataclass


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
    return curvature_lower * factor, curvature_upper * factor


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
