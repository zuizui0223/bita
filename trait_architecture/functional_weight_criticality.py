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
from sys import float_info


_DEFAULT_RELATIVE_TOL = 64.0 * float_info.epsilon


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


def _relative_band(values: tuple[float, ...], tolerance: float) -> float:
    tol = _nonnegative(tolerance, "tolerance")
    if not values:
        return 0.0
    if not all(math.isfinite(value) for value in values):
        raise ValueError("numerical comparison values must be finite")
    return tol * max(abs(value) for value in values)


def _finite_result(value: float, name: str) -> float:
    if not math.isfinite(value):
        raise ValueError(f"{name} is not representable as a finite float; rescale units")
    return value


def _distance_scaled_payoff(a: float, d: float, factor: float) -> float:
    """Return ``a*d^2*factor`` without materializing a dimensional square."""

    return _finite_result((a * d) * (factor * d), "recoverable loss")


def _weight_ratios(b: float, a: float, lam: float) -> tuple[float, float]:
    x = b / a
    ell = lam / a
    if not math.isfinite(x) or not math.isfinite(ell) or (b > 0.0 and x == 0.0):
        raise ValueError("functional-weight ratios are not representable; rescale weight units")
    return x, ell


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
    """Return R(b), the pre-cost conflict loss recoverable by differentiation.

    The calculation uses ``x=b/a`` and ``ell=lambda/a`` and factors R into the
    shared conflict fraction and the separation fraction.  Large ``x`` is
    evaluated through ``1/x`` so the asymptotic regime never materializes
    ``x**2``.
    """

    b = _nonnegative(function2_weight, "function2_weight")
    a = _positive(function1_weight, "function1_weight")
    lam = _nonnegative(coupling, "coupling")
    d = _nonnegative(optimum_distance, "optimum_distance")
    if b == 0 or d == 0:
        return 0.0

    x, ell = _weight_ratios(b, a, lam)
    if x >= 1.0:
        inv = 1.0 / x
        conflict_fraction = 1.0 / (1.0 + inv)
        separation_fraction = 1.0 / (1.0 + ell * (1.0 + inv))
    else:
        conflict_fraction = x / (1.0 + x)
        separation_denominator = x + ell * (1.0 + x)
        separation_fraction = x / separation_denominator

    left = _finite_result((a * d) * conflict_fraction, "shared conflict scale")
    right = _finite_result(separation_fraction * d, "separation-scaled distance")
    return _finite_result(left * right, "recoverable loss")


def asymptotic_recoverable_loss(
    function1_weight: float,
    coupling: float,
    optimum_distance: float,
) -> float:
    """Return lim_{b->infinity} R(b) = a^2 d^2 / (a + lambda)."""

    a = _positive(function1_weight, "function1_weight")
    lam = _nonnegative(coupling, "coupling")
    d = _nonnegative(optimum_distance, "optimum_distance")
    if d == 0:
        return 0.0
    ell = lam / a
    if not math.isfinite(ell):
        raise ValueError("coupling/function1-weight ratio is not representable; rescale weight units")
    return _distance_scaled_payoff(a, d, 1.0 / (1.0 + ell))


def critical_function2_weight(
    function1_weight: float,
    coupling: float,
    optimum_distance: float,
    architecture_cost: float,
    tolerance: float = _DEFAULT_RELATIVE_TOL,
) -> FunctionalWeightCriticality:
    """Solve R(b)=K for the context-dependent function-2 weight b.

    Returns a finite threshold when one exists. ``math.inf`` denotes a boundary
    reached only asymptotically. ``None`` denotes that no weight of function 2
    can make differentiation pay under the declared parameters.

    ``tolerance`` is dimensionless and is used only as a roundoff band for the
    finite cost-versus-ceiling comparison. Structural zero cost is exact.
    """

    a = _positive(function1_weight, "function1_weight")
    lam = _nonnegative(coupling, "coupling")
    d = _nonnegative(optimum_distance, "optimum_distance")
    K = _nonnegative(architecture_cost, "architecture_cost")
    tol = _nonnegative(tolerance, "tolerance")
    ceiling = asymptotic_recoverable_loss(a, lam, d)

    if d == 0:
        if K == 0.0:
            return FunctionalWeightCriticality(
                a, lam, d, K, ceiling, 0.0,
                "ALL_FUNCTION2_WEIGHTS_ON_ZERO_CONFLICT_BOUNDARY",
            )
        return FunctionalWeightCriticality(
            a, lam, d, K, ceiling, None,
            "NO_CONFLICT_SHARED_ARCHITECTURE_ALWAYS_FAVOURED",
        )

    if K == 0.0:
        return FunctionalWeightCriticality(
            a, lam, d, K, ceiling, 0.0,
            "ZERO_COST_COLLAPSES_ARCHITECTURE_THRESHOLD_TO_CONFLICT_ONSET",
        )

    ceiling_band = _relative_band((K, ceiling), tol)
    if abs(K - ceiling) <= ceiling_band:
        return FunctionalWeightCriticality(
            a, lam, d, K, ceiling, math.inf,
            "ASYMPTOTIC_CRITICAL_WEIGHT_NO_FINITE_CROSSING",
        )
    if K > ceiling:
        return FunctionalWeightCriticality(
            a, lam, d, K, ceiling, None,
            "COST_EXCEEDS_MAX_RECOVERABLE_LOSS_SHARED_ALWAYS_FAVOURED",
        )

    # Use x=b/a, ell=lambda/a, D=a*d^2 and k=K/D. Then the finite root solves
    #   [1-k(1+ell)] x^2 - k(1+2ell)x - k*ell = 0.
    D = _distance_scaled_payoff(a, d, 1.0)
    k_ratio = K / D
    ell = lam / a
    if not math.isfinite(k_ratio) or not math.isfinite(ell):
        raise ValueError("dimensionless critical-weight ratios are not representable; rescale units")

    A = 1.0 - k_ratio * (1.0 + ell)
    if A <= 0.0:
        raise ValueError("finite critical-weight denominator collapsed numerically; rescale units")
    linear = k_ratio * (1.0 + 2.0 * ell)
    discriminant = linear * linear + 4.0 * (k_ratio * ell) * A
    if discriminant < 0.0 or not math.isfinite(discriminant):
        raise ValueError("critical-weight discriminant is not representable; rescale units")
    xcrit = (linear + math.sqrt(discriminant)) / (2.0 * A)
    bcrit = _finite_result(a * xcrit, "critical function-2 weight")

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

    Small ``x=b/a`` uses a reciprocal-free log-derivative identity; large x
    uses ``u=1/x`` so cancellation among three O(1/x) terms is avoided.
    """

    b = _positive(function2_weight, "function2_weight")
    a = _positive(function1_weight, "function1_weight")
    lam = _nonnegative(coupling, "coupling")
    x, ell = _weight_ratios(b, a, lam)

    if x >= 1.0:
        u = 1.0 / x
        dimensionless = (
            u * u * (1.0 + 2.0 * ell * (1.0 + u))
            / ((1.0 + u) * (1.0 + ell * (1.0 + u)))
        )
    else:
        dimensionless = (
            2.0 / x
            - 1.0 / (1.0 + x)
            - (1.0 + ell) / (x + ell * (1.0 + x))
        )
    return _finite_result(dimensionless / a, "monotonicity log derivative")
