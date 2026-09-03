"""Analytic helpers for the SCH -> BITA shared-to-differentiated benchmark.

The model is deliberately local and quadratic.  It is a design/interpretation
benchmark, not a claim that natural fitness surfaces are globally quadratic.
"""

from __future__ import annotations


def _check_curvatures(a: float, b: float) -> None:
    if a <= 0 or b <= 0:
        raise ValueError("a and b must both be > 0")


def shared_optimum(z1: float, z2: float, a: float, b: float) -> float:
    """Return the optimum of one shared trait serving two quadratic functions.

    The shared mismatch loss is

        a * (z - z1)^2 + b * (z - z2)^2.
    """

    _check_curvatures(a, b)
    return (a * z1 + b * z2) / (a + b)


def compromise_penalty(z1: float, z2: float, a: float, b: float) -> float:
    """Return the minimum mismatch loss imposed by the one-trait architecture."""

    _check_curvatures(a, b)
    return (a * b / (a + b)) * (z1 - z2) ** 2


def differentiation_gain(
    z1: float,
    z2: float,
    a: float,
    b: float,
    extra_cost: float = 0.0,
) -> float:
    """Return the ideal gain from two independent functional coordinates.

    ``extra_cost`` is the added construction/development/regulation/ecological
    cost of the differentiated architecture relative to the shared one.
    Positive values penalize differentiation.
    """

    return compromise_penalty(z1, z2, a, b) - extra_cost


def differentiation_favored(
    z1: float,
    z2: float,
    a: float,
    b: float,
    extra_cost: float = 0.0,
) -> bool:
    """Return True when the ideal differentiation gain is positive."""

    return differentiation_gain(z1, z2, a, b, extra_cost) > 0
