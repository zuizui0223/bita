from __future__ import annotations

from dataclasses import dataclass
from math import inf, sqrt


@dataclass(frozen=True)
class EuclideanCrossingBudgetBracket:
    """Curvature-bracketed minimum Euclidean decoupling budget."""

    no_cross_below_or_at: float
    sufficient_above: float
    penalty_norm: float
    curvature_lower: float
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


def _positive_root(deficit: float, linear: float, curvature: float) -> float:
    """Solve linear*e + 0.5*curvature*e^2 = deficit for e >= 0."""

    if curvature == 0.0:
        return inf if linear == 0.0 else deficit / linear
    return (sqrt(linear * linear + 2.0 * curvature * deficit) - linear) / curvature


def euclidean_crossing_budget_bracket(
    *,
    deficit: float,
    penalty_norm: float,
    curvature_upper: float,
    curvature_lower: float = 0.0,
) -> EuclideanCrossingBudgetBracket:
    """Bracket the minimum Euclidean budget needed for a static crossing.

    ``deficit = K - R(lambda_0)`` must be positive. Under the segment-wise
    curvature bounds

    ``curvature_lower I <= Hessian <= curvature_upper I``:

    * every move inside budgets up to ``no_cross_below_or_at`` is incapable of
      crossing, because even the curvature-upper gain envelope stays below the
      deficit;
    * when the gradient-aligned move is componentwise feasible, budgets above
      ``sufficient_above`` guarantee crossing because the curvature-lower gain
      floor exceeds the deficit.

    The endpoints solve the corresponding equality. Strict inequality is
    required for a strictly positive post-crossing architecture margin.
    """

    if deficit <= 0:
        raise ValueError("deficit must be positive")
    if penalty_norm < 0:
        raise ValueError("penalty_norm must be nonnegative")
    if curvature_lower < 0 or curvature_upper < 0:
        raise ValueError("curvature bounds must be nonnegative")
    if curvature_lower > curvature_upper:
        raise ValueError("curvature_lower cannot exceed curvature_upper")

    c = penalty_norm
    alpha = curvature_lower
    beta = curvature_upper

    no_cross = _positive_root(deficit, c, beta)
    sufficient = _positive_root(deficit, c, alpha)

    return EuclideanCrossingBudgetBracket(
        no_cross_below_or_at=no_cross,
        sufficient_above=sufficient,
        penalty_norm=c,
        curvature_lower=alpha,
        curvature_upper=beta,
        deficit=deficit,
    )
