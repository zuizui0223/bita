"""Incubator utilities for a standalone balance-domain programme.

This module is intentionally not exported from :mod:`trait_architecture`.  It
belongs to the cross-project incubator tracked in issue #176 and is not part of
the canonical BITA manuscript API.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence


@dataclass(frozen=True)
class BalanceDomainPoint:
    environment: float
    conflict_load: float
    decoupling: float
    architecture_cost: float
    recoverable_loss: float
    phi: float
    criticality_index: float | None
    reserve: float
    state: str


@dataclass(frozen=True)
class BalanceDomainPath:
    points: tuple[BalanceDomainPoint, ...]
    zero_crossings: tuple[float, ...]
    topology: str
    balance_width: float
    integrated_reserve: float
    monotone_no_reentry_guarantee: bool


def _finite(value: float, name: str) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def classify_balance_point(
    *,
    conflict_load: float,
    decoupling: float,
    architecture_cost: float,
    tolerance: float = 1e-12,
) -> tuple[float, float, float | None, float, str]:
    """Classify one point in the static BALANCE/DIFFERENTIATION map.

    Returns ``(R, phi, q, reserve, state)`` where ``R=sL``, ``phi=R-K``,
    ``q=R/K`` for positive ``K``, and ``reserve=K-R``.
    """

    conflict_load = _finite(conflict_load, "conflict_load")
    decoupling = _finite(decoupling, "decoupling")
    architecture_cost = _finite(architecture_cost, "architecture_cost")
    if conflict_load < 0:
        raise ValueError("conflict_load must be non-negative")
    if not 0 <= decoupling <= 1:
        raise ValueError("decoupling must lie in [0, 1]")
    if architecture_cost < 0:
        raise ValueError("architecture_cost must be non-negative")

    recoverable = decoupling * conflict_load
    phi = recoverable - architecture_cost
    reserve = architecture_cost - recoverable
    q = recoverable / architecture_cost if architecture_cost > tolerance else None

    if conflict_load <= tolerance:
        state = "no_conflict"
    elif abs(phi) <= tolerance:
        state = "critical"
    elif phi < 0:
        state = "balance"
    else:
        state = "differentiation"
    return recoverable, phi, q, reserve, state


def _is_nondecreasing(values: Sequence[float], tolerance: float) -> bool:
    return all(b + tolerance >= a for a, b in zip(values, values[1:]))


def _is_nonincreasing(values: Sequence[float], tolerance: float) -> bool:
    return all(b <= a + tolerance for a, b in zip(values, values[1:]))


def monotone_no_reentry_guarantee(
    conflict_load: Sequence[float],
    decoupling: Sequence[float],
    architecture_cost: Sequence[float],
    *,
    tolerance: float = 1e-12,
) -> bool:
    """Return the sufficient condition that rules out re-entrant BALANCE.

    If ``L(e)`` and ``s(e)`` are nondecreasing and non-negative while ``K(e)``
    is nonincreasing, then ``phi(e)=s(e)L(e)-K(e)`` is nondecreasing.  Hence it
    can cross zero at most once and BALANCE cannot re-enter after
    DIFFERENTIATION along that ordered environmental path.
    """

    return (
        _is_nondecreasing(conflict_load, tolerance)
        and _is_nondecreasing(decoupling, tolerance)
        and _is_nonincreasing(architecture_cost, tolerance)
    )


def _compressed_regime_sequence(points: Sequence[BalanceDomainPoint]) -> list[str]:
    seq: list[str] = []
    for point in points:
        if point.state not in {"balance", "differentiation"}:
            continue
        if not seq or seq[-1] != point.state:
            seq.append(point.state)
    return seq


def _classify_topology(points: Sequence[BalanceDomainPoint]) -> str:
    conflict_points = [p for p in points if p.state != "no_conflict"]
    if not conflict_points:
        return "no_conflict"
    seq = _compressed_regime_sequence(conflict_points)
    if not seq:
        return "boundary_only"
    if seq == ["balance"]:
        return "all_balance"
    if seq == ["differentiation"]:
        return "all_differentiation"
    if seq == ["balance", "differentiation"]:
        return "balance_to_differentiation"
    if seq == ["differentiation", "balance"]:
        return "differentiation_to_balance"
    return "reentrant"


def _zero_crossings(points: Sequence[BalanceDomainPoint], tolerance: float) -> tuple[float, ...]:
    crossings: list[float] = []
    for point in points:
        if point.state == "critical" and point.conflict_load > tolerance:
            crossings.append(point.environment)
    for left, right in zip(points, points[1:]):
        if max(left.conflict_load, right.conflict_load) <= tolerance:
            continue
        if left.phi * right.phi < 0:
            frac = -left.phi / (right.phi - left.phi)
            crossings.append(left.environment + frac * (right.environment - left.environment))
    crossings.sort()
    unique: list[float] = []
    for crossing in crossings:
        if not unique or abs(crossing - unique[-1]) > tolerance:
            unique.append(crossing)
    return tuple(unique)


def _balance_width(points: Sequence[BalanceDomainPoint], crossings: Sequence[float]) -> float:
    """Piecewise-linear approximation of total BALANCE width in ``e``.

    Width is integrated by clipping each segment using the linearly
    interpolated architecture margin.  This is an environmental-path summary,
    not a claim that the true biological response is linear between sampled
    contexts.
    """

    total = 0.0
    for left, right in zip(points, points[1:]):
        e0, e1 = left.environment, right.environment
        if e1 <= e0:
            raise ValueError("environment must be strictly increasing")
        if max(left.conflict_load, right.conflict_load) <= 0:
            continue
        p0, p1 = left.phi, right.phi
        if p0 < 0 and p1 < 0:
            total += e1 - e0
        elif p0 < 0 <= p1 and p1 != p0:
            frac = -p0 / (p1 - p0)
            total += frac * (e1 - e0)
        elif p0 >= 0 > p1 and p1 != p0:
            frac = -p0 / (p1 - p0)
            total += (1 - frac) * (e1 - e0)
    return total


def analyze_balance_domain_path(
    *,
    environment: Sequence[float],
    conflict_load: Sequence[float],
    decoupling: Sequence[float],
    architecture_cost: Sequence[float],
    tolerance: float = 1e-12,
) -> BalanceDomainPath:
    """Analyze the internal geometry of BALANCE along an ordered environment.

    Inputs are deliberately architecture-level quantities rather than raw
    ecological proxies.  A biological variable such as predator pressure must
    first be calibrated onto these quantities; the analyzer will not silently
    perform that identification step.
    """

    lengths = {len(environment), len(conflict_load), len(decoupling), len(architecture_cost)}
    if len(lengths) != 1 or not lengths:
        raise ValueError("all input sequences must have the same non-zero length")
    if len(environment) < 2:
        raise ValueError("at least two environmental contexts are required")

    e = tuple(_finite(x, "environment") for x in environment)
    if any(b <= a for a, b in zip(e, e[1:])):
        raise ValueError("environment must be strictly increasing")

    points: list[BalanceDomainPoint] = []
    for ee, ll, ss, kk in zip(e, conflict_load, decoupling, architecture_cost):
        r, phi, q, reserve, state = classify_balance_point(
            conflict_load=ll,
            decoupling=ss,
            architecture_cost=kk,
            tolerance=tolerance,
        )
        points.append(
            BalanceDomainPoint(
                environment=ee,
                conflict_load=float(ll),
                decoupling=float(ss),
                architecture_cost=float(kk),
                recoverable_loss=r,
                phi=phi,
                criticality_index=q,
                reserve=reserve,
                state=state,
            )
        )

    crossings = _zero_crossings(points, tolerance)
    topology = _classify_topology(points)
    width = _balance_width(points, crossings)

    # A simple trapezoidal reserve integral over sampled contexts.  It is zero
    # outside positive-conflict BALANCE states and is used only as a path-level
    # resilience summary.
    reserve_values = [
        max(point.reserve, 0.0) if point.conflict_load > tolerance else 0.0
        for point in points
    ]
    integrated_reserve = sum(
        0.5 * (r0 + r1) * (e1 - e0)
        for e0, e1, r0, r1 in zip(e, e[1:], reserve_values, reserve_values[1:])
    )

    guarantee = monotone_no_reentry_guarantee(
        conflict_load, decoupling, architecture_cost, tolerance=tolerance
    )
    if guarantee and topology == "reentrant":
        raise AssertionError("re-entry contradicts the registered monotonicity guarantee")

    return BalanceDomainPath(
        points=tuple(points),
        zero_crossings=crossings,
        topology=topology,
        balance_width=width,
        integrated_reserve=integrated_reserve,
        monotone_no_reentry_guarantee=guarantee,
    )
