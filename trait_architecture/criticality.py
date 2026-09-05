"""Critical surfaces linking SCH balance to BITA differentiation.

The core architecture boundary is Phi = R - K = 0. In the quadratic model,
R = s * L_S*, so the same boundary can be parameterized from the shared-world
side (critical conflict load or optimum separation) or the differentiated-world
side (critical cost, decoupling, or residual coupling).

This module deliberately separates that architecture boundary from:
- SCH intrinsic conflict onset (L_S*=0), and
- empirical geometric dimensional-release onset (R_state=0).
Those are different criticalities unless additional calibration makes them
commensurable on one fitness scale.
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
class CriticalityMap:
    shared_conflict_load: float
    decoupling_fraction: float
    architecture_cost: float
    recoverable_loss: float
    architecture_margin: float
    architecture_status: str
    critical_cost: float
    critical_shared_load: float
    critical_decoupling: float | None
    critical_coupling: float | None
    critical_optimum_distance: float


def decoupling_fraction(weight1: float, weight2: float, coupling: float) -> float:
    weight1 = _positive(weight1, "weight1")
    weight2 = _positive(weight2, "weight2")
    coupling = _nonnegative(coupling, "coupling")
    numerator = weight1 * weight2
    return numerator / (numerator + coupling * (weight1 + weight2))


def shared_conflict_load(optimum_distance: float, weight1: float, weight2: float) -> float:
    optimum_distance = _nonnegative(optimum_distance, "optimum_distance")
    weight1 = _positive(weight1, "weight1")
    weight2 = _positive(weight2, "weight2")
    return weight1 * weight2 * optimum_distance * optimum_distance / (weight1 + weight2)


def architecture_margin(conflict_load: float, decoupling: float, architecture_cost: float) -> float:
    conflict_load = _nonnegative(conflict_load, "conflict_load")
    decoupling = _nonnegative(decoupling, "decoupling")
    architecture_cost = _nonnegative(architecture_cost, "architecture_cost")
    if decoupling > 1:
        raise ValueError("decoupling must be <= 1")
    return decoupling * conflict_load - architecture_cost


def classify_architecture_margin(margin: float, tolerance: float = 1e-12) -> str:
    margin = _finite(margin, "margin")
    tolerance = _nonnegative(tolerance, "tolerance")
    if margin > tolerance:
        return "DIFFERENTIATED_ARCHITECTURE_FAVOURED"
    if margin < -tolerance:
        return "SHARED_ARCHITECTURE_FAVOURED"
    return "COMMON_ARCHITECTURE_CRITICAL_SURFACE"


def critical_cost(conflict_load: float, decoupling: float) -> float:
    conflict_load = _nonnegative(conflict_load, "conflict_load")
    decoupling = _nonnegative(decoupling, "decoupling")
    if decoupling > 1:
        raise ValueError("decoupling must be <= 1")
    return decoupling * conflict_load


def critical_shared_load(architecture_cost: float, decoupling: float) -> float:
    architecture_cost = _nonnegative(architecture_cost, "architecture_cost")
    decoupling = _nonnegative(decoupling, "decoupling")
    if decoupling > 1:
        raise ValueError("decoupling must be <= 1")
    if decoupling == 0:
        return 0.0 if architecture_cost == 0 else math.inf
    return architecture_cost / decoupling


def critical_decoupling(conflict_load: float, architecture_cost: float) -> float | None:
    """Return s_crit=K/L when a finite s in [0,1] can reach the boundary.

    Returns None when even complete decoupling (s=1) cannot pay the cost.
    """

    conflict_load = _nonnegative(conflict_load, "conflict_load")
    architecture_cost = _nonnegative(architecture_cost, "architecture_cost")
    if conflict_load == 0:
        return 0.0 if architecture_cost == 0 else None
    value = architecture_cost / conflict_load
    if value > 1:
        return None
    return value


def critical_coupling(
    conflict_load: float,
    architecture_cost: float,
    weight1: float,
    weight2: float,
) -> float | None:
    """Residual coupling lambda at which s L_S* = K.

    Returns infinity for K=0 with positive conflict (any finite coupling remains
    weakly on the differentiated side before other costs), and None when no
    nonnegative coupling can make the differentiated architecture pay because
    K exceeds the fully decoupled recoverable loss.
    """

    conflict_load = _nonnegative(conflict_load, "conflict_load")
    architecture_cost = _nonnegative(architecture_cost, "architecture_cost")
    weight1 = _positive(weight1, "weight1")
    weight2 = _positive(weight2, "weight2")

    if conflict_load == 0:
        return math.inf if architecture_cost == 0 else None
    if architecture_cost == 0:
        return math.inf
    if architecture_cost > conflict_load:
        return None
    coefficient = weight1 * weight2 / (weight1 + weight2)
    value = coefficient * (conflict_load / architecture_cost - 1.0)
    return max(0.0, value)


def critical_optimum_distance(
    architecture_cost: float,
    weight1: float,
    weight2: float,
    coupling: float,
) -> float:
    architecture_cost = _nonnegative(architecture_cost, "architecture_cost")
    weight1 = _positive(weight1, "weight1")
    weight2 = _positive(weight2, "weight2")
    coupling = _nonnegative(coupling, "coupling")
    if architecture_cost == 0:
        return 0.0
    numerator = architecture_cost * (weight1 + weight2) * (
        weight1 * weight2 + coupling * (weight1 + weight2)
    )
    denominator = weight1 * weight1 * weight2 * weight2
    return math.sqrt(numerator / denominator)


def empirical_release_margin(distance_y0_to_sch_reference: float, distance_y1_to_sch_reference: float) -> float:
    """Geometric R_state; positive means the y1 state moves x* toward SCH reference."""

    d0 = _nonnegative(distance_y0_to_sch_reference, "distance_y0_to_sch_reference")
    d1 = _nonnegative(distance_y1_to_sch_reference, "distance_y1_to_sch_reference")
    return d0 - d1


def classify_empirical_release(release_margin: float, tolerance: float = 1e-12) -> str:
    release_margin = _finite(release_margin, "release_margin")
    tolerance = _nonnegative(tolerance, "tolerance")
    if release_margin > tolerance:
        return "GEOMETRIC_DIMENSIONAL_RELEASE"
    if release_margin < -tolerance:
        return "GEOMETRIC_MOVEMENT_AWAY_FROM_SCH_REFERENCE"
    return "EMPIRICAL_RELEASE_CRITICAL_BOUNDARY"


def criticality_map(
    optimum_distance: float,
    weight1: float,
    weight2: float,
    coupling: float,
    architecture_cost: float,
) -> CriticalityMap:
    load = shared_conflict_load(optimum_distance, weight1, weight2)
    s = decoupling_fraction(weight1, weight2, coupling)
    recoverable = s * load
    margin = recoverable - _nonnegative(architecture_cost, "architecture_cost")
    return CriticalityMap(
        shared_conflict_load=load,
        decoupling_fraction=s,
        architecture_cost=architecture_cost,
        recoverable_loss=recoverable,
        architecture_margin=margin,
        architecture_status=classify_architecture_margin(margin),
        critical_cost=critical_cost(load, s),
        critical_shared_load=critical_shared_load(architecture_cost, s),
        critical_decoupling=critical_decoupling(load, architecture_cost),
        critical_coupling=critical_coupling(load, architecture_cost, weight1, weight2),
        critical_optimum_distance=critical_optimum_distance(
            architecture_cost, weight1, weight2, coupling
        ),
    )


def cross_world_equivalence_statement() -> dict[str, str]:
    return {
        "theory_architecture_surface": "SAME: s*L_S*=K <=> L_S*=K/s <=> K=s*L_S*",
        "sch_intrinsic_conflict_boundary": "DIFFERENT: L_S*=0 is conflict onset inside the fixed one-axis world",
        "bita_empirical_release_boundary": "DIFFERENT_UNITS: R_state=0 is geometric release onset",
        "current_empirical_equivalence": "NOT_YET_IDENTIFIED: requires commensurable fitness recovery, architecture cost, and paired SCH/BITA context",
    }
