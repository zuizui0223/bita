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


@dataclass(frozen=True)
class RobustUncertainBudgetBracket:
    """Fail-closed critical-budget bracket under bounded parameter uncertainty."""

    robust_no_cross_below_or_at: float
    robust_sufficient_above: float
    deficit_lower: float
    deficit_upper: float
    penalty_norm_lower: float
    penalty_norm_upper: float
    curvature_lower: float
    curvature_upper: float


def scalar_finite_gain_bounds(
    *,
    linear_gain: float,
    squared_norm: float,
    curvature_upper: float,
    curvature_lower: float = 0.0,
) -> tuple[float, float]:
    """Return lower/upper finite gain bounds from scalar Hessian bounds."""

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
    """Bracket the minimum Euclidean budget needed for a static crossing."""

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


def robust_uncertain_budget_bracket(
    *,
    deficit_lower: float,
    deficit_upper: float,
    penalty_norm_lower: float,
    penalty_norm_upper: float,
    curvature_lower: float,
    curvature_upper: float,
) -> RobustUncertainBudgetBracket:
    """Return a simultaneous fail-closed budget band under bounded inputs.

    Robust no-cross uses the easiest possible crossing realization:
    smallest deficit, largest active penalty, largest curvature.

    Robust sufficiency uses the hardest realization:
    largest deficit, smallest active penalty, smallest guaranteed curvature.
    """

    if deficit_lower <= 0 or deficit_upper <= 0:
        raise ValueError("deficit bounds must be positive")
    if deficit_lower > deficit_upper:
        raise ValueError("deficit_lower cannot exceed deficit_upper")
    if penalty_norm_lower < 0 or penalty_norm_upper < 0:
        raise ValueError("penalty norm bounds must be nonnegative")
    if penalty_norm_lower > penalty_norm_upper:
        raise ValueError("penalty_norm_lower cannot exceed penalty_norm_upper")
    if curvature_lower < 0 or curvature_upper < 0:
        raise ValueError("curvature bounds must be nonnegative")
    if curvature_lower > curvature_upper:
        raise ValueError("curvature_lower cannot exceed curvature_upper")

    robust_no = _positive_root(
        deficit_lower,
        penalty_norm_upper,
        curvature_upper,
    )
    robust_yes = _positive_root(
        deficit_upper,
        penalty_norm_lower,
        curvature_lower,
    )

    return RobustUncertainBudgetBracket(
        robust_no_cross_below_or_at=robust_no,
        robust_sufficient_above=robust_yes,
        deficit_lower=deficit_lower,
        deficit_upper=deficit_upper,
        penalty_norm_lower=penalty_norm_lower,
        penalty_norm_upper=penalty_norm_upper,
        curvature_lower=curvature_lower,
        curvature_upper=curvature_upper,
    )
