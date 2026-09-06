from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Sequence


@dataclass(frozen=True)
class DecouplingPlan:
    direction: tuple[float, ...]
    first_order_gain: float
    dual_penalty_norm: float


@dataclass(frozen=True)
class JointRobustness:
    distance: float
    coupling_shift: tuple[float, ...]
    cost_shift: float


def _validate_penalties(active_penalties: Sequence[float]) -> tuple[float, ...]:
    if not active_penalties:
        raise ValueError("active_penalties must be nonempty")
    penalties = tuple(float(c) for c in active_penalties)
    if any(c < 0 for c in penalties):
        raise ValueError("active penalties must be nonnegative")
    return penalties


def optimal_diagonal_decoupling(
    active_penalties: Sequence[float],
    metric_diag: Sequence[float],
    budget: float,
) -> DecouplingPlan:
    penalties = _validate_penalties(active_penalties)
    if budget < 0:
        raise ValueError("budget must be nonnegative")
    if len(penalties) != len(metric_diag):
        raise ValueError("active_penalties and metric_diag must have the same nonzero length")
    if any(q <= 0 for q in metric_diag):
        raise ValueError("metric diagonal must be positive")

    dual_sq = sum((c * c) / q for c, q in zip(penalties, metric_diag))
    if dual_sq == 0:
        return DecouplingPlan(
            direction=tuple(0.0 for _ in penalties),
            first_order_gain=0.0,
            dual_penalty_norm=0.0,
        )

    dual_norm = sqrt(dual_sq)
    direction = tuple(
        -budget * (c / q) / dual_norm
        for c, q in zip(penalties, metric_diag)
    )
    return DecouplingPlan(
        direction=direction,
        first_order_gain=budget * dual_norm,
        dual_penalty_norm=dual_norm,
    )


def optimal_l1_decoupling(active_penalties: Sequence[float], budget: float) -> DecouplingPlan:
    penalties = _validate_penalties(active_penalties)
    if budget < 0:
        raise ValueError("budget must be nonnegative")
    maximum = max(penalties)
    if maximum == 0:
        return DecouplingPlan(tuple(0.0 for _ in penalties), 0.0, 0.0)
    index = penalties.index(maximum)
    direction = tuple(-budget if i == index else 0.0 for i in range(len(penalties)))
    return DecouplingPlan(direction, budget * maximum, maximum)


def optimal_l2_decoupling(active_penalties: Sequence[float], budget: float) -> DecouplingPlan:
    penalties = _validate_penalties(active_penalties)
    if budget < 0:
        raise ValueError("budget must be nonnegative")
    norm = sqrt(sum(c * c for c in penalties))
    if norm == 0:
        return DecouplingPlan(tuple(0.0 for _ in penalties), 0.0, 0.0)
    direction = tuple(-budget * c / norm for c in penalties)
    return DecouplingPlan(direction, budget * norm, norm)


def optimal_linf_decoupling(active_penalties: Sequence[float], budget: float) -> DecouplingPlan:
    penalties = _validate_penalties(active_penalties)
    if budget < 0:
        raise ValueError("budget must be nonnegative")
    dual_norm = sum(penalties)
    direction = tuple(-budget if c > 0 else 0.0 for c in penalties)
    return DecouplingPlan(direction, budget * dual_norm, dual_norm)


def best_single_channel(active_penalties: Sequence[float], metric_diag: Sequence[float]) -> int:
    penalties = _validate_penalties(active_penalties)
    if len(penalties) != len(metric_diag):
        raise ValueError("active_penalties and metric_diag must have the same nonzero length")
    if any(q <= 0 for q in metric_diag):
        raise ValueError("metric diagonal must be positive")
    scores = [c / sqrt(q) for c, q in zip(penalties, metric_diag)]
    return max(range(len(scores)), key=scores.__getitem__)


def joint_diagonal_robustness(
    margin: float,
    active_penalties: Sequence[float],
    coupling_metric_diag: Sequence[float],
    cost_metric_weight: float = 1.0,
) -> JointRobustness:
    penalties = _validate_penalties(active_penalties)
    if margin <= 0:
        raise ValueError("margin must be positive")
    if len(penalties) != len(coupling_metric_diag):
        raise ValueError("active_penalties and coupling_metric_diag must have the same nonzero length")
    if any(q <= 0 for q in coupling_metric_diag) or cost_metric_weight <= 0:
        raise ValueError("metric weights must be positive")

    denom_sq = sum(
        (c * c) / q for c, q in zip(penalties, coupling_metric_diag)
    ) + 1.0 / cost_metric_weight
    distance = margin / sqrt(denom_sq)
    coupling_shift = tuple(
        margin * (c / q) / denom_sq
        for c, q in zip(penalties, coupling_metric_diag)
    )
    cost_shift = margin * (1.0 / cost_metric_weight) / denom_sq
    return JointRobustness(
        distance=distance,
        coupling_shift=coupling_shift,
        cost_shift=cost_shift,
    )
