"""Minimal shared-axis versus differentiated-axis trait-architecture model.

This module is deliberately general. It does not define the competing functions
as pollination, defence, attraction, or antagonism. Two functions may favour
different states of one shared trait coordinate. The model compares the best
fitness attainable under that integrated compromise with the best fitness under
a two-axis architecture that can partially decouple the functions.

The quadratic form is a baseline theorem-generating model, not a claim that all
biological fitness surfaces are quadratic. Alternative response shapes are tested
in :mod:`trait_architecture.differentiation_robustness`.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


def _finite(value: float, name: str) -> None:
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")


def _positive(value: float, name: str) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _non_negative(value: float, name: str) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and non-negative")


@dataclass(frozen=True)
class SharedAxisOptimum:
    """Best compromise when both functions act on one trait coordinate."""

    trait: float
    conflict_loss: float
    fitness: float


@dataclass(frozen=True)
class DifferentiatedAxisOptimum:
    """Best two-axis solution after paying residual coupling and architecture cost."""

    trait_1: float
    trait_2: float
    residual_conflict_loss: float
    architecture_cost: float
    fitness: float

    @property
    def separation(self) -> float:
        """Absolute distance between the two optimized trait states."""

        return abs(self.trait_1 - self.trait_2)


@dataclass(frozen=True)
class ArchitectureComparison:
    """Comparison between the best shared and differentiated architectures."""

    shared: SharedAxisOptimum
    differentiated: DifferentiatedAxisOptimum
    decoupling_fraction: float
    recoverable_conflict_loss: float
    differentiation_threshold: float
    architecture_gain: float
    preferred_architecture: str


def shared_axis_optimum(
    optimum_1: float,
    optimum_2: float,
    weight_1: float = 1.0,
    weight_2: float = 1.0,
) -> SharedAxisOptimum:
    """Return the best one-axis compromise for two quadratic functional demands.

    Fitness is normalized so that each function contributes zero loss at its own
    preferred state. The shared architecture maximizes

    ``-w1 * (z - theta1)^2 - w2 * (z - theta2)^2``.
    """

    _finite(optimum_1, "optimum_1")
    _finite(optimum_2, "optimum_2")
    _positive(weight_1, "weight_1")
    _positive(weight_2, "weight_2")

    denominator = weight_1 + weight_2
    trait = (weight_1 * optimum_1 + weight_2 * optimum_2) / denominator
    conflict = optimum_1 - optimum_2
    conflict_loss = weight_1 * weight_2 * conflict * conflict / denominator

    return SharedAxisOptimum(
        trait=trait,
        conflict_loss=conflict_loss,
        fitness=-conflict_loss,
    )


def decoupling_fraction(
    weight_1: float = 1.0,
    weight_2: float = 1.0,
    coupling: float = 0.0,
) -> float:
    """Fraction of the function-specific optimum separation retained after coupling.

    In the quadratic baseline,

    ``|x* - y*| / |theta1 - theta2|``

    equals

    ``w1*w2 / (w1*w2 + coupling*(w1+w2))``

    whenever ``theta1 != theta2``. The same quantity also equals the fraction of
    the shared-axis conflict loss that the differentiated architecture can recover
    before paying its fixed architecture cost.

    It ranges from 1 under full decoupling (``coupling = 0``) toward 0 as residual
    coupling becomes arbitrarily strong.
    """

    _positive(weight_1, "weight_1")
    _positive(weight_2, "weight_2")
    _non_negative(coupling, "coupling")

    numerator = weight_1 * weight_2
    denominator = numerator + coupling * (weight_1 + weight_2)
    return numerator / denominator


def differentiated_axis_optimum(
    optimum_1: float,
    optimum_2: float,
    weight_1: float = 1.0,
    weight_2: float = 1.0,
    coupling: float = 0.0,
    architecture_cost: float = 0.0,
) -> DifferentiatedAxisOptimum:
    """Return the best two-axis solution under residual coupling.

    The differentiated architecture maximizes

    ``-w1*(x-theta1)^2 - w2*(y-theta2)^2 - coupling*(x-y)^2 - K``.

    ``coupling`` is a residual cross-talk/coordination penalty that resists
    functional separation. ``architecture_cost`` is the fixed cost of maintaining
    the differentiated architecture.
    """

    _finite(optimum_1, "optimum_1")
    _finite(optimum_2, "optimum_2")
    _positive(weight_1, "weight_1")
    _positive(weight_2, "weight_2")
    _non_negative(coupling, "coupling")
    _non_negative(architecture_cost, "architecture_cost")

    denominator = weight_1 * weight_2 + coupling * weight_1 + coupling * weight_2

    trait_1 = (
        weight_1 * weight_2 * optimum_1
        + weight_1 * coupling * optimum_1
        + weight_2 * coupling * optimum_2
    ) / denominator
    trait_2 = (
        weight_1 * weight_2 * optimum_2
        + weight_1 * coupling * optimum_1
        + weight_2 * coupling * optimum_2
    ) / denominator

    conflict = optimum_1 - optimum_2
    residual_conflict_loss = (
        weight_1
        * weight_2
        * coupling
        * conflict
        * conflict
        / denominator
    )

    return DifferentiatedAxisOptimum(
        trait_1=trait_1,
        trait_2=trait_2,
        residual_conflict_loss=residual_conflict_loss,
        architecture_cost=architecture_cost,
        fitness=-residual_conflict_loss - architecture_cost,
    )


def differentiation_threshold(
    optimum_1: float,
    optimum_2: float,
    weight_1: float = 1.0,
    weight_2: float = 1.0,
    coupling: float = 0.0,
) -> float:
    """Maximum fixed architecture cost compatible with differentiation.

    For the quadratic baseline, differentiation is favoured exactly when

    ``architecture_cost < differentiation_threshold(...)``.

    The threshold is the shared-axis conflict loss multiplied by the decoupling
    fraction. In closed form it is

    ``w1^2 w2^2 (theta1-theta2)^2 /
      ((w1+w2) * (w1*w2 + coupling*(w1+w2)))``.
    """

    shared = shared_axis_optimum(
        optimum_1=optimum_1,
        optimum_2=optimum_2,
        weight_1=weight_1,
        weight_2=weight_2,
    )
    fraction = decoupling_fraction(
        weight_1=weight_1,
        weight_2=weight_2,
        coupling=coupling,
    )
    return shared.conflict_loss * fraction


def compare_architectures(
    optimum_1: float,
    optimum_2: float,
    weight_1: float = 1.0,
    weight_2: float = 1.0,
    coupling: float = 0.0,
    architecture_cost: float = 0.0,
    neutral_tolerance: float = 1e-12,
) -> ArchitectureComparison:
    """Compare optimized shared and differentiated trait architectures."""

    _non_negative(neutral_tolerance, "neutral_tolerance")

    shared = shared_axis_optimum(
        optimum_1=optimum_1,
        optimum_2=optimum_2,
        weight_1=weight_1,
        weight_2=weight_2,
    )
    differentiated = differentiated_axis_optimum(
        optimum_1=optimum_1,
        optimum_2=optimum_2,
        weight_1=weight_1,
        weight_2=weight_2,
        coupling=coupling,
        architecture_cost=architecture_cost,
    )
    fraction = decoupling_fraction(
        weight_1=weight_1,
        weight_2=weight_2,
        coupling=coupling,
    )
    recoverable = shared.conflict_loss - differentiated.residual_conflict_loss
    threshold = differentiation_threshold(
        optimum_1=optimum_1,
        optimum_2=optimum_2,
        weight_1=weight_1,
        weight_2=weight_2,
        coupling=coupling,
    )
    gain = differentiated.fitness - shared.fitness

    if gain > neutral_tolerance:
        preferred = "differentiated"
    elif gain < -neutral_tolerance:
        preferred = "shared"
    else:
        preferred = "indifferent"

    return ArchitectureComparison(
        shared=shared,
        differentiated=differentiated,
        decoupling_fraction=fraction,
        recoverable_conflict_loss=recoverable,
        differentiation_threshold=threshold,
        architecture_gain=gain,
        preferred_architecture=preferred,
    )
