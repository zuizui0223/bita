from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Sequence


@dataclass(frozen=True)
class BoxDecouplingPlan:
    allocation: tuple[float, ...]
    certified_linear_gain: float
    budget_used: float
    saturated_channels: tuple[int, ...]


def _validate_vectors(
    active_penalties: Sequence[float],
    coupling_available: Sequence[float],
    costs: Sequence[float],
) -> None:
    if not active_penalties:
        raise ValueError("vectors must be nonempty")
    if not (
        len(active_penalties) == len(coupling_available) == len(costs)
    ):
        raise ValueError("all vectors must have the same length")
    if any(c < 0 for c in active_penalties):
        raise ValueError("active penalties must be nonnegative")
    if any(lam < 0 for lam in coupling_available):
        raise ValueError("available coupling must be nonnegative")
    if any(a <= 0 for a in costs):
        raise ValueError("cost weights must be positive")


def weighted_l1_box_plan(
    active_penalties: Sequence[float],
    coupling_available: Sequence[float],
    unit_costs: Sequence[float],
    budget: float,
) -> BoxDecouplingPlan:
    """Fractional-knapsack optimum for a weighted-L1 decoupling budget."""

    _validate_vectors(active_penalties, coupling_available, unit_costs)
    if budget < 0:
        raise ValueError("budget must be nonnegative")

    n = len(active_penalties)
    allocation = [0.0] * n
    remaining = float(budget)

    order = sorted(
        range(n),
        key=lambda i: active_penalties[i] / unit_costs[i],
        reverse=True,
    )

    for i in order:
        if remaining <= 0:
            break
        if active_penalties[i] <= 0 or coupling_available[i] <= 0:
            continue
        take = min(coupling_available[i], remaining / unit_costs[i])
        allocation[i] = take
        remaining -= unit_costs[i] * take

    gain = sum(c * x for c, x in zip(active_penalties, allocation))
    used = sum(a * x for a, x in zip(unit_costs, allocation))
    saturated = tuple(
        i
        for i, (x, lam) in enumerate(zip(allocation, coupling_available))
        if lam > 0 and abs(x - lam) <= 1e-12
    )
    return BoxDecouplingPlan(tuple(allocation), gain, used, saturated)


def diagonal_l2_box_plan(
    active_penalties: Sequence[float],
    coupling_available: Sequence[float],
    quadratic_costs: Sequence[float],
    budget: float,
) -> BoxDecouplingPlan:
    """Exact capped-proportional solution for a diagonal quadratic budget.

    Maximizes ``c^T x`` subject to ``sum_i q_i x_i^2 <= budget^2`` and
    ``0 <= x_i <= lambda_i``.
    """

    _validate_vectors(active_penalties, coupling_available, quadratic_costs)
    if budget < 0:
        raise ValueError("budget must be nonnegative")

    n = len(active_penalties)
    allocation = [0.0] * n
    eps2 = float(budget) ** 2

    positive = [
        i
        for i in range(n)
        if active_penalties[i] > 0 and coupling_available[i] > 0
    ]
    if not positive or eps2 == 0:
        return BoxDecouplingPlan(tuple(allocation), 0.0, 0.0, tuple())

    full_cost2 = sum(
        quadratic_costs[i] * coupling_available[i] ** 2 for i in positive
    )
    if eps2 >= full_cost2:
        for i in positive:
            allocation[i] = coupling_available[i]
        gain = sum(c * x for c, x in zip(active_penalties, allocation))
        return BoxDecouplingPlan(
            tuple(allocation),
            gain,
            sqrt(full_cost2),
            tuple(sorted(positive)),
        )

    # Saturation threshold in the proportional parameter tau:
    # tau * c_i / q_i = lambda_i.
    thresholds = sorted(
        (
            coupling_available[i] * quadratic_costs[i] / active_penalties[i],
            i,
        )
        for i in positive
    )

    saturated: set[int] = set()
    sat_cost2 = 0.0

    while True:
        unsaturated = [i for i in positive if i not in saturated]
        coeff = sum(
            active_penalties[i] ** 2 / quadratic_costs[i]
            for i in unsaturated
        )
        if coeff <= 0:
            break
        tau = sqrt(max(0.0, eps2 - sat_cost2) / coeff)

        newly_saturated = [
            i
            for threshold, i in thresholds
            if i not in saturated and tau >= threshold - 1e-14
        ]
        if not newly_saturated:
            for i in unsaturated:
                allocation[i] = tau * active_penalties[i] / quadratic_costs[i]
            break

        # Saturate every channel whose unconstrained request has crossed its cap.
        for i in newly_saturated:
            saturated.add(i)
            allocation[i] = coupling_available[i]
            sat_cost2 += quadratic_costs[i] * coupling_available[i] ** 2

        if sat_cost2 >= eps2 - 1e-14:
            break

    gain = sum(c * x for c, x in zip(active_penalties, allocation))
    used2 = sum(q * x * x for q, x in zip(quadratic_costs, allocation))
    return BoxDecouplingPlan(
        tuple(allocation),
        gain,
        sqrt(max(0.0, used2)),
        tuple(sorted(saturated)),
    )
