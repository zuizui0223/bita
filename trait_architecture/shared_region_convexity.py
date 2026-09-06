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
