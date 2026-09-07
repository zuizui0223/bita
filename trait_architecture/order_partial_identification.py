from __future__ import annotations

from dataclasses import dataclass
from math import inf
from typing import Iterable, Sequence

from .order_geometry import componentwise_leq


@dataclass(frozen=True)
class OrderMarginBounds:
    lower: float
    upper: float
    classification: str
    lower_sources: tuple[int, ...]
    upper_sources: tuple[int, ...]


def order_margin_bounds(
    query: Sequence[float],
    points: Iterable[Sequence[float]],
    intervals: Iterable[tuple[float, float]],
    *,
    tol: float = 1e-12,
) -> OrderMarginBounds:
    q = tuple(float(x) for x in query)
    xs = tuple(tuple(float(x) for x in p) for p in points)
    ivals = tuple((float(lo), float(hi)) for lo, hi in intervals)
    if not q or not xs or len(xs) != len(ivals):
        raise ValueError("query, points and intervals must be nonempty and aligned")
    if any(len(p) != len(q) for p in xs):
        raise ValueError("all points must match query dimension")
    if any(lo > hi for lo, hi in ivals):
        raise ValueError("interval lower bound cannot exceed upper bound")

    lower_sources = tuple(i for i, p in enumerate(xs) if componentwise_leq(p, q, tol=tol))
    upper_sources = tuple(i for i, p in enumerate(xs) if componentwise_leq(q, p, tol=tol))

    lower = max((ivals[i][0] for i in lower_sources), default=-inf)
    upper = min((ivals[i][1] for i in upper_sources), default=inf)

    if lower > upper + tol:
        classification = "MONOTONICITY_INCONSISTENT"
    elif lower > tol:
        classification = "BITA_SIDE_CERTIFIED"
    elif upper <= tol:
        classification = "SHARED_OR_BOUNDARY_CERTIFIED"
    else:
        classification = "ORDER_UNRESOLVED"

    return OrderMarginBounds(
        lower=lower,
        upper=upper,
        classification=classification,
        lower_sources=lower_sources,
        upper_sources=upper_sources,
    )


def exact_order_margin_bounds(
    query: Sequence[float],
    points: Iterable[Sequence[float]],
    margins: Iterable[float],
) -> OrderMarginBounds:
    values = tuple(float(x) for x in margins)
    return order_margin_bounds(query, points, ((x, x) for x in values))
