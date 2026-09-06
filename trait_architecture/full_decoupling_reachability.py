from __future__ import annotations

from dataclasses import dataclass
from math import fsum
from typing import Sequence


UNREACHABLE = "UNREACHABLE_WITHIN_REGISTERED_DECOUPLING"
FULL_CROSSING = "FULL_DECOUPLING_GUARANTEES_CROSSING"
UNRESOLVED = "REACHABILITY_UNRESOLVED_BY_CURVATURE_BOUNDS"


@dataclass(frozen=True)
class FullDecouplingReachability:
    status: str
    lower_full_gain: float
    upper_full_gain: float
    deficit: float
    linear_full_gain: float
    squared_full_norm: float
    curvature_lower: float
    curvature_upper: float


def classify_full_decoupling_reachability(
    *,
    current_coupling: Sequence[float],
    active_penalties: Sequence[float],
    deficit: float,
    curvature_lower: float = 0.0,
    curvature_upper: float,
) -> FullDecouplingReachability:
    if len(current_coupling) != len(active_penalties) or not current_coupling:
        raise ValueError("current_coupling and active_penalties must have the same nonzero length")
    if any(x < 0 for x in current_coupling):
        raise ValueError("current coupling must be nonnegative")
    if any(c < 0 for c in active_penalties):
        raise ValueError("active penalties must be nonnegative")
    if deficit <= 0:
        raise ValueError("deficit must be positive for a shared-favored reachability test")
    if curvature_lower < 0 or curvature_upper < 0:
        raise ValueError("curvature bounds must be nonnegative")
    if curvature_lower > curvature_upper:
        raise ValueError("curvature_lower cannot exceed curvature_upper")

    linear = fsum(c * lam for c, lam in zip(active_penalties, current_coupling))
    norm_sq = fsum(lam * lam for lam in current_coupling)
    lower = linear + 0.5 * curvature_lower * norm_sq
    upper = linear + 0.5 * curvature_upper * norm_sq

    if upper <= deficit:
        status = UNREACHABLE
    elif lower > deficit:
        status = FULL_CROSSING
    else:
        status = UNRESOLVED

    return FullDecouplingReachability(
        status=status,
        lower_full_gain=lower,
        upper_full_gain=upper,
        deficit=deficit,
        linear_full_gain=linear,
        squared_full_norm=norm_sq,
        curvature_lower=curvature_lower,
        curvature_upper=curvature_upper,
    )
