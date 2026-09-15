"""Robustness analyses for shared-axis versus differentiated-axis architectures.

The closed-form baseline in :mod:`trait_architecture.differentiation` uses
quadratic functional losses and quadratic residual coupling.  This module removes
that special shape while preserving the same architecture comparison.

For powers p > 1 and q > 1, compare

    L_S(z) = w1 |z-theta1|^p + w2 |z-theta2|^p

with

    L_D(x,y) = w1 |x-theta1|^p + w2 |y-theta2|^p
               + coupling |x-y|^q + K.

The optimizer works on the dimensionless interval coordinate joining the two
function-specific optima.  Trait-span powers are absorbed into effective
fitness coefficients before optimization, so a pure change of trait units does
not change the numerical problem being solved.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, fsum, isfinite, log, sqrt
from sys import float_info
from typing import Callable


_ROUNDOFF_REL_TOL = 128.0 * float_info.epsilon


def _finite(value: float, name: str) -> None:
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")


def _positive(value: float, name: str) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _power(value: float, name: str) -> None:
    if not isfinite(value) or value <= 1.0:
        raise ValueError(f"{name} must be finite and > 1 for the convex robustness family")


def _non_negative(value: float, name: str) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and non-negative")


def _roundoff_band(*values: float) -> float:
    if any(not isfinite(float(value)) for value in values):
        raise ValueError("roundoff comparison values must be finite")
    return _ROUNDOFF_REL_TOL * max((abs(float(value)) for value in values), default=0.0)


def _log_trait_span(optimum_1: float, optimum_2: float) -> float | None:
    """Return log(|theta2-theta1|) without requiring the span itself to be finite."""

    first = float(optimum_1)
    second = float(optimum_2)
    if first == second:
        return None
    direct = abs(second - first)
    if isfinite(direct) and direct > 0.0:
        return log(direct)

    scale = max(abs(first), abs(second))
    if scale == 0.0 or not isfinite(scale):
        raise ValueError("trait span is not numerically resolvable")
    normalized = abs(second / scale - first / scale)
    if normalized <= 0.0 or not isfinite(normalized):
        raise ValueError("trait span is not numerically resolvable")
    return log(scale) + log(normalized)


def _effective_coefficient(
    coefficient: float,
    power: float,
    log_span: float,
    name: str,
) -> float:
    """Return coefficient*span**power without materializing the span power."""

    value = float(coefficient)
    if value == 0.0:
        return 0.0
    log_value = log(value) + float(power) * log_span
    if not isfinite(log_value):
        raise ValueError(f"{name} effective coefficient is not representable")
    try:
        out = exp(log_value)
    except OverflowError as exc:
        raise ValueError(f"{name} effective coefficient overflows float") from exc
    if out == 0.0:
        raise ValueError(f"{name} effective coefficient underflows float")
    if not isfinite(out):
        raise ValueError(f"{name} effective coefficient is not finite")
    return out


def _trait_from_unit_interval(optimum_1: float, optimum_2: float, coordinate: float) -> float:
    """Map t in [0,1] back by a convex combination of finite endpoints."""

    t = float(coordinate)
    value = (1.0 - t) * float(optimum_1) + t * float(optimum_2)
    if not isfinite(value):
        raise ValueError("optimized trait coordinate is not representable as a finite float")
    return value


def _finite_sum(*values: float, name: str) -> float:
    try:
        total = fsum(values)
    except OverflowError as exc:
        raise ValueError(f"{name} is not representable as a finite float") from exc
    if not isfinite(total):
        raise ValueError(f"{name} is not representable as a finite float")
    return total


def _golden_minimize(
    function: Callable[[float], float],
    lower: float,
    upper: float,
    *,
    tolerance: float = 1e-10,
    max_iter: int = 300,
) -> tuple[float, float]:
    """Deterministically minimise a unimodal function on a dimensionless interval."""

    if upper < lower:
        lower, upper = upper, lower
    if lower == upper:
        return lower, function(lower)

    _positive(tolerance, "tolerance")
    if max_iter <= 0:
        raise ValueError("max_iter must be positive")

    inv_phi = 2.0 / (1.0 + sqrt(5.0))
    c = upper - (upper - lower) * inv_phi
    d = lower + (upper - lower) * inv_phi
    fc = function(c)
    fd = function(d)

    for _ in range(max_iter):
        if upper - lower <= tolerance:
            break
        if fc <= fd:
            upper, d, fd = d, c, fc
            c = upper - (upper - lower) * inv_phi
            fc = function(c)
        else:
            lower, c, fc = c, d, fd
            d = lower + (upper - lower) * inv_phi
            fd = function(d)

    optimum = 0.5 * (lower + upper)
    return optimum, function(optimum)


@dataclass(frozen=True)
class PowerSharedOptimum:
    trait: float
    loss: float
    fitness: float


@dataclass(frozen=True)
class PowerDifferentiatedOptimum:
    trait_1: float
    trait_2: float
    loss_before_fixed_cost: float
    architecture_cost: float
    fitness: float

    @property
    def separation(self) -> float:
        return abs(self.trait_1 - self.trait_2)


@dataclass(frozen=True)
class PowerArchitectureComparison:
    shared: PowerSharedOptimum
    differentiated: PowerDifferentiatedOptimum
    recoverable_conflict_loss: float
    architecture_gain: float
    preferred_architecture: str
    functional_power: float
    coupling_power: float


def shared_power_optimum(
    optimum_1: float,
    optimum_2: float,
    *,
    weight_1: float = 1.0,
    weight_2: float = 1.0,
    functional_power: float = 2.0,
    tolerance: float = 1e-10,
) -> PowerSharedOptimum:
    """Numerically optimize the shared architecture on t in [0,1].

    ``tolerance`` is dimensionless on that normalized interval.
    """

    _finite(optimum_1, "optimum_1")
    _finite(optimum_2, "optimum_2")
    _positive(weight_1, "weight_1")
    _positive(weight_2, "weight_2")
    _power(functional_power, "functional_power")
    _positive(tolerance, "tolerance")

    log_span = _log_trait_span(optimum_1, optimum_2)
    if log_span is None:
        return PowerSharedOptimum(trait=float(optimum_1), loss=0.0, fitness=-0.0)

    first = _effective_coefficient(weight_1, functional_power, log_span, "weight_1")
    second = _effective_coefficient(weight_2, functional_power, log_span, "weight_2")

    def loss(t: float) -> float:
        return _finite_sum(
            first * t**functional_power,
            second * (1.0 - t) ** functional_power,
            name="shared power loss",
        )

    coordinate, minimum_loss = _golden_minimize(
        loss,
        0.0,
        1.0,
        tolerance=tolerance,
    )
    trait = _trait_from_unit_interval(optimum_1, optimum_2, coordinate)
    return PowerSharedOptimum(trait=trait, loss=minimum_loss, fitness=-minimum_loss)


def differentiated_power_optimum(
    optimum_1: float,
    optimum_2: float,
    *,
    weight_1: float = 1.0,
    weight_2: float = 1.0,
    coupling: float = 0.0,
    architecture_cost: float = 0.0,
    functional_power: float = 2.0,
    coupling_power: float | None = None,
    tolerance: float = 1e-10,
) -> PowerDifferentiatedOptimum:
    """Numerically optimize the differentiated architecture on [0,1]^2.

    ``tolerance`` is dimensionless on the normalized trait interval.
    """

    _finite(optimum_1, "optimum_1")
    _finite(optimum_2, "optimum_2")
    _positive(weight_1, "weight_1")
    _positive(weight_2, "weight_2")
    _non_negative(coupling, "coupling")
    _non_negative(architecture_cost, "architecture_cost")
    _power(functional_power, "functional_power")
    _positive(tolerance, "tolerance")
    if coupling_power is None:
        coupling_power = functional_power
    _power(coupling_power, "coupling_power")

    log_span = _log_trait_span(optimum_1, optimum_2)
    if log_span is None:
        cost = float(architecture_cost)
        return PowerDifferentiatedOptimum(
            trait_1=float(optimum_1),
            trait_2=float(optimum_2),
            loss_before_fixed_cost=0.0,
            architecture_cost=cost,
            fitness=-cost,
        )

    first = _effective_coefficient(weight_1, functional_power, log_span, "weight_1")
    second = _effective_coefficient(weight_2, functional_power, log_span, "weight_2")
    cross = _effective_coefficient(coupling, coupling_power, log_span, "coupling")

    def optimise_y(tx: float) -> tuple[float, float]:
        first_loss = first * tx**functional_power

        def loss_y(ty: float) -> float:
            return _finite_sum(
                first_loss,
                second * (1.0 - ty) ** functional_power,
                cross * abs(tx - ty) ** coupling_power,
                name="differentiated power loss",
            )

        return _golden_minimize(loss_y, 0.0, 1.0, tolerance=tolerance)

    def profiled_loss(tx: float) -> float:
        _, loss = optimise_y(tx)
        return loss

    tx, _ = _golden_minimize(profiled_loss, 0.0, 1.0, tolerance=tolerance)
    ty, loss_before_cost = optimise_y(tx)
    trait_1 = _trait_from_unit_interval(optimum_1, optimum_2, tx)
    trait_2 = _trait_from_unit_interval(optimum_1, optimum_2, ty)
    cost = float(architecture_cost)
    fitness = -_finite_sum(loss_before_cost, cost, name="differentiated total loss")

    return PowerDifferentiatedOptimum(
        trait_1=trait_1,
        trait_2=trait_2,
        loss_before_fixed_cost=loss_before_cost,
        architecture_cost=cost,
        fitness=fitness,
    )


def compare_power_architectures(
    optimum_1: float,
    optimum_2: float,
    *,
    weight_1: float = 1.0,
    weight_2: float = 1.0,
    coupling: float = 0.0,
    architecture_cost: float = 0.0,
    functional_power: float = 2.0,
    coupling_power: float | None = None,
    neutral_tolerance: float | None = None,
    optimisation_tolerance: float = 1e-10,
) -> PowerArchitectureComparison:
    """Compare shared and differentiated optima under non-quadratic losses.

    ``optimisation_tolerance`` is dimensionless on the normalized trait
    interval. If ``neutral_tolerance`` is supplied it remains an absolute
    fitness-unit band; otherwise only a roundoff-relative band is used.
    """

    if neutral_tolerance is not None:
        _non_negative(neutral_tolerance, "neutral_tolerance")
    _positive(optimisation_tolerance, "optimisation_tolerance")
    _non_negative(architecture_cost, "architecture_cost")

    shared = shared_power_optimum(
        optimum_1,
        optimum_2,
        weight_1=weight_1,
        weight_2=weight_2,
        functional_power=functional_power,
        tolerance=optimisation_tolerance,
    )
    differentiated = differentiated_power_optimum(
        optimum_1,
        optimum_2,
        weight_1=weight_1,
        weight_2=weight_2,
        coupling=coupling,
        architecture_cost=architecture_cost,
        functional_power=functional_power,
        coupling_power=coupling_power,
        tolerance=optimisation_tolerance,
    )

    recoverable = shared.loss - differentiated.loss_before_fixed_cost
    gap_band = _roundoff_band(shared.loss, differentiated.loss_before_fixed_cost)
    if recoverable < 0.0:
        if abs(recoverable) <= gap_band:
            recoverable = 0.0
        else:
            raise RuntimeError("differentiated optimization exceeded the shared optimum loss")

    cost = float(architecture_cost)
    gain = _finite_sum(recoverable, -cost, name="architecture gain")
    band = (
        float(neutral_tolerance)
        if neutral_tolerance is not None
        else _roundoff_band(shared.loss, differentiated.loss_before_fixed_cost, recoverable, cost)
    )

    if gain > band:
        preferred = "differentiated"
    elif gain < -band:
        preferred = "shared"
    else:
        preferred = "indifferent"

    return PowerArchitectureComparison(
        shared=shared,
        differentiated=differentiated,
        recoverable_conflict_loss=recoverable,
        architecture_gain=gain,
        preferred_architecture=preferred,
        functional_power=functional_power,
        coupling_power=functional_power if coupling_power is None else coupling_power,
    )
