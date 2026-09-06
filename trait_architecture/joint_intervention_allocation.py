from __future__ import annotations

from dataclasses import dataclass
from math import inf
from typing import Sequence


@dataclass(frozen=True)
class JointAllocation:
    decoupling: tuple[float, ...]
    cost_relief: float
    certified_margin_gain: float
    budget_used: float
    marginal_efficiency: float


@dataclass(frozen=True)
class CertifiedCrossingBudget:
    budget: float
    last_lane: str


def _validate(
    active_penalties: Sequence[float],
    decoupling_costs: Sequence[float],
    coupling_caps: Sequence[float],
    cost_relief_price: float,
) -> None:
    n = len(active_penalties)
    if n == 0 or len(decoupling_costs) != n or len(coupling_caps) != n:
        raise ValueError("coupling vectors must have the same nonzero length")
    if any(c < 0 for c in active_penalties):
        raise ValueError("active penalties must be nonnegative")
    if any(a <= 0 for a in decoupling_costs) or cost_relief_price <= 0:
        raise ValueError("intervention prices must be positive")
    if any(cap < 0 for cap in coupling_caps):
        raise ValueError("coupling caps must be nonnegative")


def allocate_joint_linear_budget(
    *,
    active_penalties: Sequence[float],
    decoupling_costs: Sequence[float],
    coupling_caps: Sequence[float],
    cost_relief_price: float,
    budget: float,
) -> JointAllocation:
    _validate(active_penalties, decoupling_costs, coupling_caps, cost_relief_price)
    if budget < 0:
        raise ValueError("budget must be nonnegative")

    lanes = []
    for i, (c, a, cap) in enumerate(zip(active_penalties, decoupling_costs, coupling_caps)):
        lanes.append((c / a, f"coupling:{i}", a, cap))
    lanes.append((1.0 / cost_relief_price, "cost", cost_relief_price, inf))
    lanes.sort(key=lambda row: row[0], reverse=True)

    remaining = budget
    x = [0.0] * len(active_penalties)
    kappa = 0.0
    gain = 0.0
    used = 0.0
    marginal = 0.0

    for efficiency, name, price, cap in lanes:
        if remaining <= 0:
            break
        max_spend = inf if cap == inf else price * cap
        spend = remaining if max_spend == inf else min(remaining, max_spend)
        amount = spend / price
        if name == "cost":
            kappa += amount
            lane_gain = amount
        else:
            i = int(name.split(":", 1)[1])
            x[i] += amount
            lane_gain = active_penalties[i] * amount
        gain += lane_gain
        used += spend
        remaining -= spend
        if spend > 0:
            marginal = efficiency

    return JointAllocation(
        decoupling=tuple(x),
        cost_relief=kappa,
        certified_margin_gain=gain,
        budget_used=used,
        marginal_efficiency=marginal,
    )


def minimum_certified_joint_budget(
    *,
    deficit: float,
    active_penalties: Sequence[float],
    decoupling_costs: Sequence[float],
    coupling_caps: Sequence[float],
    cost_relief_price: float,
) -> CertifiedCrossingBudget:
    _validate(active_penalties, decoupling_costs, coupling_caps, cost_relief_price)
    if deficit <= 0:
        raise ValueError("deficit must be positive")

    lanes = []
    for i, (c, a, cap) in enumerate(zip(active_penalties, decoupling_costs, coupling_caps)):
        lanes.append((c / a, f"coupling:{i}", c * cap, a))
    lanes.append((1.0 / cost_relief_price, "cost", inf, cost_relief_price))
    lanes.sort(key=lambda row: row[0], reverse=True)

    remaining_gain = deficit
    budget = 0.0
    last_lane = ""
    for efficiency, name, max_gain, price in lanes:
        if remaining_gain <= 0:
            break
        if max_gain == inf or max_gain >= remaining_gain:
            # Price per unit certified gain is 1/efficiency.
            if efficiency <= 0:
                raise RuntimeError("positive deficit cannot be closed by a zero-efficiency lane")
            budget += remaining_gain / efficiency
            remaining_gain = 0.0
            last_lane = name
            break
        if max_gain > 0:
            budget += max_gain / efficiency
            remaining_gain -= max_gain
            last_lane = name

    return CertifiedCrossingBudget(budget=budget, last_lane=last_lane)
