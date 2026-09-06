from __future__ import annotations

from dataclasses import dataclass
from math import inf, sqrt


@dataclass(frozen=True)
class EuclideanCrossingBudgetBracket:
    """Conservative bracket for the minimum Euclidean decoupling budget."""

    no_cross_below_or_at: float
    sufficient_above: float
    penalty_norm: float
    curvature_upper: float
    deficit: float


def scalar_finite_gain_bounds(
    *,
    linear_gain: float,
    squared_norm: float,
    curvature_upper: float,
    curvature_lower: float = 0.0,
) -> tuple[float, float]:
    """Return lower/upper finite gain bounds from scalar Hessian bounds.

    Assumes ``curvature_lower I <= Hessian <= curvature_upper I`` along the
    intervention segment. ``linear_gain`` is c0^T x and ``squared_norm`` is
    ||x||_2^2.
    """

    if linear_gain < 0:
        raise ValueError("linear_gain must be nonnegative for a decoupling move")
    if squared_norm < 0:
        raise ValueError("squared_norm must be nonnegative")
    if curvature_lower < 0 or curvature_upper < 0:
        raise ValueError("curvature bounds must be nonnegative")
    if curvature_lower > curvature_upper:
        raise ValueError("curvature_lower cannot exceed curvature_upper")

    lower = linear_gain + 0.5 * curvature_lower * squared_norm
    upper = linear_gain + 0.5 * curvature_upper * squared_norm
    return lower, upper


def euclidean_crossing_budget_bracket(
    *,
    deficit: float,
    penalty_norm: float,
    curvature_upper: float,
) -> EuclideanCrossingBudgetBracket:
    """Bracket the minimum Euclidean budget needed for a static crossing.

    ``deficit = K - R(lambda_0)`` must be positive. Under the global bound
    ``0 <= Hessian <= curvature_upper I``:

    * budgets ``epsilon`` satisfying
      ``penalty_norm*epsilon + 0.5*curvature_upper*epsilon**2 <= deficit``
      cannot contain a crossing move;
    * when the gradient-aligned move is componentwise feasible, any
      ``epsilon > deficit/penalty_norm`` guarantees a crossing by convexity.

    The returned endpoints use equality. Strict inequality is required for a
    strictly positive post-crossing architecture margin.
    """

    if deficit <= 0:
        raise ValueError("deficit must be positive")
    if penalty_norm < 0:
        raise ValueError("penalty_norm must be nonnegative")
    if curvature_upper < 0:
        raise ValueError("curvature_upper must be nonnegative")

    c = penalty_norm
    beta = curvature_upper

    if beta == 0.0:
        if c == 0.0:
            no_cross = inf
            sufficient = inf
        else:
            no_cross = deficit / c
            sufficient = deficit / c
    else:
        no_cross = (sqrt(c * c + 2.0 * beta * deficit) - c) / beta
        sufficient = inf if c == 0.0 else deficit / c

    return EuclideanCrossingBudgetBracket(
        no_cross_below_or_at=no_cross,
        sufficient_above=sufficient,
        penalty_norm=c,
        curvature_upper=beta,
        deficit=deficit,
    )
