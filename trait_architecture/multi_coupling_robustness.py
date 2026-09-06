from dataclasses import dataclass
from math import sqrt
from typing import Iterable


@dataclass(frozen=True)
class DirectionalCouplingBound:
    weighted_penalty_rate: float
    minimum_distance_to_crossing: float | None
    crossing_possible_under_model: bool


def _as_tuple(values: Iterable[float]) -> tuple[float, ...]:
    result = tuple(float(v) for v in values)
    if not result:
        raise ValueError("coupling vectors must be nonempty")
    return result


def directional_coupling_bound(
    *,
    net_margin: float,
    active_penalties: Iterable[float],
    direction: Iterable[float],
) -> DirectionalCouplingBound:
    if net_margin <= 0:
        raise ValueError("net_margin must be positive")
    c = _as_tuple(active_penalties)
    v = _as_tuple(direction)
    if len(c) != len(v):
        raise ValueError("active_penalties and direction must have equal length")
    if any(x < 0 for x in c):
        raise ValueError("active penalties must be nonnegative")
    if any(x < 0 for x in v):
        raise ValueError("direction must be componentwise nonnegative")

    rate = sum(ci * vi for ci, vi in zip(c, v))
    if rate == 0:
        return DirectionalCouplingBound(
            weighted_penalty_rate=0.0,
            minimum_distance_to_crossing=None,
            crossing_possible_under_model=False,
        )
    return DirectionalCouplingBound(
        weighted_penalty_rate=rate,
        minimum_distance_to_crossing=net_margin / rate,
        crossing_possible_under_model=True,
    )


def euclidean_coupling_distance_bound(*, net_margin: float, active_penalties: Iterable[float]) -> float | None:
    if net_margin <= 0:
        raise ValueError("net_margin must be positive")
    c = _as_tuple(active_penalties)
    if any(x < 0 for x in c):
        raise ValueError("active penalties must be nonnegative")
    norm = sqrt(sum(x * x for x in c))
    if norm == 0:
        return None
    return net_margin / norm


def penalty_weighted_change(*, active_penalties: Iterable[float], delta_coupling: Iterable[float]) -> float:
    c = _as_tuple(active_penalties)
    d = _as_tuple(delta_coupling)
    if len(c) != len(d):
        raise ValueError("vectors must have equal length")
    if any(x < 0 for x in c) or any(x < 0 for x in d):
        raise ValueError("vectors must be componentwise nonnegative")
    return sum(ci * di for ci, di in zip(c, d))
