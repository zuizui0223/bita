from __future__ import annotations

from math import sqrt
from typing import Sequence


def certified_linear_gain_floor(
    active_penalties: Sequence[float],
    decoupling: Sequence[float],
) -> float:
    if len(active_penalties) != len(decoupling) or not active_penalties:
        raise ValueError("active_penalties and decoupling must have the same nonzero length")
    if any(c < 0 for c in active_penalties):
        raise ValueError("active penalties must be nonnegative")
    if any(x < 0 for x in decoupling):
        raise ValueError("decoupling amounts must be nonnegative")
    return sum(float(c) * float(x) for c, x in zip(active_penalties, decoupling))


def sufficient_static_crossing(
    architecture_deficit: float,
    active_penalties: Sequence[float],
    decoupling: Sequence[float],
) -> bool:
    if architecture_deficit <= 0:
        raise ValueError("architecture_deficit must be positive on the shared-favored side")
    return certified_linear_gain_floor(active_penalties, decoupling) > architecture_deficit


def certified_l2_budget_threshold(
    architecture_deficit: float,
    active_penalties: Sequence[float],
) -> float:
    if architecture_deficit <= 0:
        raise ValueError("architecture_deficit must be positive")
    if not active_penalties or any(c < 0 for c in active_penalties):
        raise ValueError("active penalties must be nonempty and nonnegative")
    norm = sqrt(sum(float(c) ** 2 for c in active_penalties))
    if norm == 0:
        return float("inf")
    return architecture_deficit / norm
