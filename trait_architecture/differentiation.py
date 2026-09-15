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
from sys import float_info


_ROUNDOFF_REL_TOL = 64.0 * float_info.epsilon


def _finite(value: float, name: str) -> None:
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")


def _positive(value: float, name: str) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _non_negative(value: float, name: str) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and non-negative")


def _weight_geometry(weight_1: float, weight_2: float) -> tuple[float, float, float]:
    """Return normalized weights and the harmonic conflict coefficient.

    The coefficient is ``w1*w2/(w1+w2)`` but is evaluated without materializing
    ``w1*w2``.  The normalized weights are also used for stable convex trait
    coordinates.
    """

    _positive(weight_1, "weight_1")
    _positive(weight_2, "weight_2")
    scale = max(float(weight_1), float(weight_2))
    u = float(weight_1) / scale
    v = float(weight_2) / scale
    total = u + v
    p1 = u / total
    p2 = v / total
    coefficient = scale * (u * v / total)
    if coefficient <= 0.0 or not isfinite(coefficient):
        raise ValueError("harmonic weight coefficient is not representable as a positive finite float")
    return p1, p2, coefficient


def _conflict_load(
    optimum_1: float,
    optimum_2: float,
    coefficient: float,
) -> float:
    """Evaluate ``coefficient*(theta1-theta2)^2`` without a squared distance."""

    conflict = float(optimum_1) - float(optimum_2)
    if not isfinite(conflict):
        raise ValueError("optimum separation is not representable as a finite float")
    value = conflict * (coefficient * conflict)
    if not isfinite(value):
        raise ValueError("conflict loss is not representable as a finite float")
    return value


def _decoupling_parts(coefficient: float, coupling: float) -> tuple[float, float]:
    """Return ``(s, 1-s)`` from commensurate coefficient and coupling scales."""

    _non_negative(coupling, "coupling")
    c = float(coupling)
    if c == 0.0:
        return 1.0, 0.0
    scale = max(coefficient, c)
    h = coefficient / scale
    c_n = c / scale
    total = h + c_n
    return h / total, c_n / total


def _roundoff_band(*values: float) -> float:
    if any(not isfinite(float(value)) for value in values):
        raise ValueError("roundoff comparison values must be finite")
    return _ROUNDOFF_REL_TOL * max((abs(float(value)) for value in values), default=0.0)


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
    p1, p2, coefficient = _weight_geometry(weight_1, weight_2)

    trait = p1 * float(optimum_1) + p2 * float(optimum_2)
    conflict_loss = _conflict_load(optimum_1, optimum_2, coefficient)

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
    """

    _, _, coefficient = _weight_geometry(weight_1, weight_2)
    fraction, _ = _decoupling_parts(coefficient, coupling)
    return fraction


def differentiated_axis_optimum(
    optimum_1: float,
    optimum_2: float,
    weight_1: float = 1.0,
    weight_2: float = 1.0,
    coupling: float = 0.0,
    architecture_cost: float = 0.0,
) -> DifferentiatedAxisOptimum:
    """Return the best two-axis solution under residual coupling.

    The optimized pair has the same weighted center as the shared solution and
    retains fraction ``s`` of the function-specific optimum separation.  This
    representation is algebraically identical to the direct 2x2 solution but
    avoids dimensional coefficient products.
    """

    _finite(optimum_1, "optimum_1")
    _finite(optimum_2, "optimum_2")
    _non_negative(architecture_cost, "architecture_cost")
    p1, p2, coefficient = _weight_geometry(weight_1, weight_2)
    fraction, residual_fraction = _decoupling_parts(coefficient, coupling)

    shared_center = p1 * float(optimum_1) + p2 * float(optimum_2)
    conflict = float(optimum_1) - float(optimum_2)
    if not isfinite(conflict):
        raise ValueError("optimum separation is not representable as a finite float")
    retained_separation = fraction * conflict
    trait_1 = shared_center + p2 * retained_separation
    trait_2 = shared_center - p1 * retained_separation
    if not isfinite(trait_1) or not isfinite(trait_2):
        raise ValueError("differentiated optimum is not representable as a finite float")

    shared_loss = _conflict_load(optimum_1, optimum_2, coefficient)
    residual_conflict_loss = residual_fraction * shared_loss
    fitness = -residual_conflict_loss - float(architecture_cost)
    if not isfinite(fitness):
        raise ValueError("differentiated fitness is not representable as a finite float")

    return DifferentiatedAxisOptimum(
        trait_1=trait_1,
        trait_2=trait_2,
        residual_conflict_loss=residual_conflict_loss,
        architecture_cost=float(architecture_cost),
        fitness=fitness,
    )


def differentiation_threshold(
    optimum_1: float,
    optimum_2: float,
    weight_1: float = 1.0,
    weight_2: float = 1.0,
    coupling: float = 0.0,
) -> float:
    """Maximum fixed architecture cost compatible with differentiation."""

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
    neutral_tolerance: float | None = None,
) -> ArchitectureComparison:
    """Compare optimized shared and differentiated trait architectures.

    If ``neutral_tolerance`` is supplied, it retains its historical meaning as
    an absolute fitness-unit neutral band.  With the default ``None``, only a
    machine-roundoff band relative to the commensurate threshold/cost scale is
    used, so changing fitness units cannot relabel a genuinely signed gain.
    """

    if neutral_tolerance is not None:
        _non_negative(neutral_tolerance, "neutral_tolerance")

    _non_negative(architecture_cost, "architecture_cost")
    shared = shared_axis_optimum(
        optimum_1=optimum_1,
        optimum_2=optimum_2,
        weight_1=weight_1,
        weight_2=weight_2,
    )
    p1, p2, coefficient = _weight_geometry(weight_1, weight_2)
    del p1, p2
    fraction, residual_fraction = _decoupling_parts(coefficient, coupling)

    conflict = float(optimum_1) - float(optimum_2)
    if not isfinite(conflict):
        raise ValueError("optimum separation is not representable as a finite float")
    shared_center = shared.trait
    retained_separation = fraction * conflict
    p1, p2, _ = _weight_geometry(weight_1, weight_2)
    trait_1 = shared_center + p2 * retained_separation
    trait_2 = shared_center - p1 * retained_separation
    residual = residual_fraction * shared.conflict_loss
    differentiated_fitness = -residual - float(architecture_cost)
    differentiated = DifferentiatedAxisOptimum(
        trait_1=trait_1,
        trait_2=trait_2,
        residual_conflict_loss=residual,
        architecture_cost=float(architecture_cost),
        fitness=differentiated_fitness,
    )

    threshold = fraction * shared.conflict_loss
    recoverable = threshold
    gain = threshold - float(architecture_cost)
    if not isfinite(gain):
        raise ValueError("architecture gain is not representable as a finite float")

    band = (
        float(neutral_tolerance)
        if neutral_tolerance is not None
        else _roundoff_band(threshold, float(architecture_cost))
    )
    if gain > band:
        preferred = "differentiated"
    elif gain < -band:
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
