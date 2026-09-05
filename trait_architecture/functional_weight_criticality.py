"""Critical functional-weight threshold for the SCH -> BITA architecture switch.

Let ``a`` be the fixed weight of function 1, ``b`` the context-dependent weight
of function 2, ``d`` the separation between their preferred states, ``lambda``
the residual coupling of the differentiated architecture, and ``K`` its added
architecture cost.

For the quadratic SCH/BITA bridge, recoverable shared-axis conflict loss is

    R(b) = a^2 b^2 d^2 / ((a+b) * (a b + lambda (a+b))).

For positive conflict (d>0), R(b) increases monotonically with b but approaches
an upper bound. Therefore increasing ecological pressure does not necessarily
force differentiation: if K is at or above the asymptotic recoverable loss,
there is no finite function-2 weight at which differentiation becomes favored.
"""

from __future__ import annotations

from dataclasses import dataclass
import math


def _finite(value: float, name: str) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _positive(value: float, name: str) -> float:
    value = _finite(value, name)
    if value <= 0:
        raise ValueError(f"{name} must be > 0")
    return value


def _nonnegative(value: float, name: str) -> float:
    value = _finite(value, name)
    if value < 0:
        raise ValueError(f"{name} must be >= 0")
    return value


@dataclass(frozen=True)
class FunctionalWeightCriticality:
    fixed_function1_weight: float
    coupling: float
    optimum_distance: float
    architecture_cost: float
    asymptotic_recoverable_loss: float
    critical_function2_weight: float | None
    status: str


def recoverable_loss_at_function2_weight(
    function2_weight: float,
    function1_weight: float,
    coupling: float,
    optimum_distance: float,
) -> float:
    """Return R(b), the pre-cost conflict loss recoverable by differentiation."""

    b = _nonnegative(function2_weight, "function2_weight")
    a = _positive(function1_weight, "function1_weight")
    lam = _nonnegative(coupling, "coupling")
    d = _nonnegative(optimum_distance, "optimum_distance")
    if b == 0 or d == 0:
        return 0.0
    numerator = a * a * b * b * d * d
    denominator = (a + b) * (a * b + lam * (a + b))
    return numerator / denominator


def asymptotic_recoverable_loss(
    function1_weight: float,
    coupling: float,
    optimum_distance: float,
) -> float:
    """Return lim_{b->infinity} R(b) = a^2 d^2 / (a + lambda)."""

    a = _positive(function1_weight, "function1_weight")
    lam = _nonnegative(coupling, "coupling")
    d = _nonnegative(optimum_distance, "optimum_distance")
    return a * a * d * d / (a + lam)


def critical_function2_weight(
    function1_weight: float,
    coupling: float,
    optimum_distance: float,
    architecture_cost: float,
    tolerance: float = 1e-12,
) -> FunctionalWeightCriticality:
    """Solve R(b)=K for the context-dependent function-2 weight b.

    Returns a finite threshold when one exists. ``math.inf`` denotes a boundary
    reached only asymptotically. ``None`` denotes that no weight of function 2
    can make differentiation pay under the declared parameters.
    """

    a = _positive(function1_weight, "function1_weight")
    lam = _nonnegative(coupling, "coupling")
    d = _nonnegative(optimum_distance, "optimum_distance")
    K = _nonnegative(architecture_cost, "architecture_cost")
    tol = _nonnegative(tolerance, "tolerance")
    ceiling = asymptotic_recoverable_loss(a, lam, d)

    if d == 0:
        if K <= tol:
            return FunctionalWeightCriticality(
                a, lam, d, K, ceiling, 0.0,
                "ALL_FUNCTION2_WEIGHTS_ON_ZERO_CONFLICT_BOUNDARY",
            )
        return FunctionalWeightCriticality(
            a, lam, d, K, ceiling, None,
            "NO_CONFLICT_SHARED_ARCHITECTURE_ALWAYS_FAVOURED",
        )

    if K <= tol:
        return FunctionalWeightCriticality(
            a, lam, d, K, ceiling, 0.0,
            "ZERO_COST_COLLAPSES_ARCHITECTURE_THRESHOLD_TO_CONFLICT_ONSET",
        )

    scale = max(1.0, abs(K), abs(ceiling))
    if abs(K - ceiling) <= tol * scale:
        return FunctionalWeightCriticality(
            a, lam, d, K, ceiling, math.inf,
            "ASYMPTOTIC_CRITICAL_WEIGHT_NO_FINITE_CROSSING",
        )
    if K > ceiling:
        return FunctionalWeightCriticality(
            a, lam, d, K, ceiling, None,
            "COST_EXCEEDS_MAX_RECOVERABLE_LOSS_SHARED_ALWAYS_FAVOURED",
        )

    # Solving R(b)=K gives A b^2 - K a(a+2 lambda)b - K lambda a^2 = 0,
    # where A = a^2 d^2 - K(a+lambda) > 0 in the finite-crossing regime.
    A = a * a * d * d - K * (a + lam)
    discriminant = K * K * (a + 2.0 * lam) ** 2 + 4.0 * K * lam * A
    bcrit = a * (K * (a + 2.0 * lam) + math.sqrt(discriminant)) / (2.0 * A)

    return FunctionalWeightCriticality(
        a, lam, d, K, ceiling, bcrit,
        "FINITE_FUNCTION2_WEIGHT_CRITICAL_POINT",
    )


def monotonicity_log_derivative(
    function2_weight: float,
    function1_weight: float,
    coupling: float,
) -> float:
    """Return d log R / db for b>0 and d>0; it is strictly positive.

    The expression is

        a (a b + 2 a lambda + 2 b lambda)
        / [b (a+b) (a b + a lambda + b lambda)].

    It does not depend on optimum distance because distance only scales R.
    """

    b = _positive(function2_weight, "function2_weight")
    a = _positive(function1_weight, "function1_weight")
    lam = _nonnegative(coupling, "coupling")
    numerator = a * (a * b + 2.0 * a * lam + 2.0 * b * lam)
    denominator = b * (a + b) * (a * b + a * lam + b * lam)
    return numerator / denominator
