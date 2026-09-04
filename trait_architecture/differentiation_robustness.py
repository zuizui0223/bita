"""Robustness analyses for shared-axis versus differentiated-axis architectures.

The closed-form baseline in :mod:`trait_architecture.differentiation` uses
quadratic functional losses and quadratic residual coupling.  This module removes
that special shape while preserving the same architecture comparison.

For powers p > 1 and q > 1, compare

    L_S(z) = w1 |z-theta1|^p + w2 |z-theta2|^p

with

    L_D(x,y) = w1 |x-theta1|^p + w2 |y-theta2|^p
               + coupling |x-y|^q + K.

The optimum of each convex loss lies inside the interval bounded by the two
function-specific optima, so deterministic golden-section minimisation is enough
and introduces no external numerical dependency.

These calculations test whether the qualitative Chapter-2 result depends on the
quadratic assumption.  They are not an evolutionary-dynamics model and do not by
themselves establish a historical transition to differentiated traits.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt
from typing import Callable


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


def _golden_minimize(
    function: Callable[[float], float],
    lower: float,
    upper: float,
    *,
    tolerance: float = 1e-10,
    max_iter: int = 300,
) -> tuple[float, float]:
    """Deterministically minimise a unimodal function on a closed interval."""

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
    """Numerically optimise the shared architecture for a convex power loss."""

    _finite(optimum_1, "optimum_1")
    _finite(optimum_2, "optimum_2")
    _positive(weight_1, "weight_1")
    _positive(weight_2, "weight_2")
    _power(functional_power, "functional_power")

    lower, upper = sorted((optimum_1, optimum_2))

    def loss(z: float) -> float:
        return (
            weight_1 * abs(z - optimum_1) ** functional_power
            + weight_2 * abs(z - optimum_2) ** functional_power
        )

    trait, minimum_loss = _golden_minimize(
        loss,
        lower,
        upper,
        tolerance=tolerance,
    )
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
    """Numerically optimise a two-axis convex power-loss architecture."""

    _finite(optimum_1, "optimum_1")
    _finite(optimum_2, "optimum_2")
    _positive(weight_1, "weight_1")
    _positive(weight_2, "weight_2")
    _non_negative(coupling, "coupling")
    _non_negative(architecture_cost, "architecture_cost")
    _power(functional_power, "functional_power")
    if coupling_power is None:
        coupling_power = functional_power
    _power(coupling_power, "coupling_power")

    lower, upper = sorted((optimum_1, optimum_2))

    def optimise_y(x: float) -> tuple[float, float]:
        def loss_y(y: float) -> float:
            return (
                weight_1 * abs(x - optimum_1) ** functional_power
                + weight_2 * abs(y - optimum_2) ** functional_power
                + coupling * abs(x - y) ** coupling_power
            )

        return _golden_minimize(
            loss_y,
            lower,
            upper,
            tolerance=tolerance,
        )

    def profiled_loss(x: float) -> float:
        _, loss = optimise_y(x)
        return loss

    trait_1, _ = _golden_minimize(
        profiled_loss,
        lower,
        upper,
        tolerance=tolerance,
    )
    trait_2, loss_before_cost = optimise_y(trait_1)

    return PowerDifferentiatedOptimum(
        trait_1=trait_1,
        trait_2=trait_2,
        loss_before_fixed_cost=loss_before_cost,
        architecture_cost=architecture_cost,
        fitness=-loss_before_cost - architecture_cost,
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
    neutral_tolerance: float = 1e-9,
    optimisation_tolerance: float = 1e-10,
) -> PowerArchitectureComparison:
    """Compare shared and differentiated optima under non-quadratic losses."""

    _non_negative(neutral_tolerance, "neutral_tolerance")

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
    gain = differentiated.fitness - shared.fitness

    if gain > neutral_tolerance:
        preferred = "differentiated"
    elif gain < -neutral_tolerance:
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
