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
from sys import float_info


_ROUNDOFF_REL_TOL = 64.0 * float_info.epsilon


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


def _finite_result(value: float, name: str) -> float:
    if not math.isfinite(value):
        raise ValueError(f"{name} is not representable as a finite float; rescale units")
    return value


def _conflict_coefficient(weight1: float, weight2: float) -> float:
    """Return w1*w2/(w1+w2) without forming the weight product."""

    w1 = _positive(weight1, "weight1")
    w2 = _positive(weight2, "weight2")
    if w1 <= w2:
        coefficient = w1 / (1.0 + w1 / w2)
    else:
        coefficient = w2 / (1.0 + w2 / w1)
    if coefficient == 0.0:
        raise ValueError("conflict coefficient underflows float precision; rescale weight units")
    return _finite_result(coefficient, "conflict coefficient")


def _roundoff_architecture_status(recoverable: float, cost: float) -> str:
    """Classify R-K using only a scale-relative machine-roundoff band."""

    margin = recoverable - cost
    band = _ROUNDOFF_REL_TOL * max(abs(recoverable), abs(cost))
    if margin > band:
        return "DIFFERENTIATED_ARCHITECTURE_FAVOURED"
    if margin < -band:
        return "SHARED_ARCHITECTURE_FAVOURED"
    return "COMMON_ARCHITECTURE_CRITICAL_SURFACE"


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
    coefficient = _conflict_coefficient(weight1, weight2)
    if coupling == 0.0:
        return 1.0
    if coefficient >= coupling:
        value = 1.0 / (1.0 + coupling / coefficient)
    else:
        ratio = coefficient / coupling
        if ratio == 0.0:
            raise ValueError("decoupling fraction underflows float precision; rescale weight units")
        value = ratio / (1.0 + ratio)
    return _finite_result(value, "decoupling fraction")


def shared_conflict_load(optimum_distance: float, weight1: float, weight2: float) -> float:
    optimum_distance = _nonnegative(optimum_distance, "optimum_distance")
    coefficient = _conflict_coefficient(weight1, weight2)
    if optimum_distance == 0.0:
        return 0.0
    first = coefficient * optimum_distance
    value = first * optimum_distance
    if coefficient != 0.0 and optimum_distance != 0.0 and value == 0.0:
        raise ValueError("shared conflict load underflows float precision; rescale units")
    return _finite_result(value, "shared conflict load")


def architecture_margin(conflict_load: float, decoupling: float, architecture_cost: float) -> float:
    conflict_load = _nonnegative(conflict_load, "conflict_load")
    decoupling = _nonnegative(decoupling, "decoupling")
    architecture_cost = _nonnegative(architecture_cost, "architecture_cost")
    if decoupling > 1:
        raise ValueError("decoupling must be <= 1")
    return decoupling * conflict_load - architecture_cost


def classify_architecture_margin(margin: float, tolerance: float = 1e-12) -> str:
    """Classify a supplied margin using an explicit absolute margin-unit band.

    This public helper preserves its original contract. Automatic numerical
    classification inside :func:`criticality_map` uses a separate roundoff-only
    relative rule based on the commensurate R and K terms.
    """

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
    value = decoupling * conflict_load
    if decoupling != 0.0 and conflict_load != 0.0 and value == 0.0:
        raise ValueError("critical cost underflows float precision; rescale fitness units")
    return _finite_result(value, "critical cost")


def critical_shared_load(architecture_cost: float, decoupling: float) -> float:
    architecture_cost = _nonnegative(architecture_cost, "architecture_cost")
    decoupling = _nonnegative(decoupling, "decoupling")
    if decoupling > 1:
        raise ValueError("decoupling must be <= 1")
    if decoupling == 0:
        return 0.0 if architecture_cost == 0 else math.inf
    value = architecture_cost / decoupling
    if architecture_cost != 0.0 and value == 0.0:
        raise ValueError("critical shared load underflows float precision; rescale fitness units")
    return _finite_result(value, "critical shared load")


def critical_decoupling(conflict_load: float, architecture_cost: float) -> float | None:
    """Return s_crit=K/L when a finite s in [0,1] can reach the boundary.

    Returns None when even complete decoupling (s=1) cannot pay the cost.
    """

    conflict_load = _nonnegative(conflict_load, "conflict_load")
    architecture_cost = _nonnegative(architecture_cost, "architecture_cost")
    if conflict_load == 0:
        return 0.0 if architecture_cost == 0 else None
    value = architecture_cost / conflict_load
    if architecture_cost != 0.0 and value == 0.0:
        raise ValueError("critical decoupling underflows float precision; rescale fitness units")
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
    coefficient = _conflict_coefficient(weight1, weight2)

    if conflict_load == 0:
        return math.inf if architecture_cost == 0 else None
    if architecture_cost == 0:
        return math.inf
    if architecture_cost > conflict_load:
        return None
    delta = conflict_load - architecture_cost
    if delta == 0.0:
        return 0.0
    ratio = delta / architecture_cost
    value = coefficient * ratio
    if value == 0.0:
        raise ValueError("critical coupling underflows float precision; rescale weight units")
    return max(0.0, _finite_result(value, "critical coupling"))


def critical_optimum_distance(
    architecture_cost: float,
    weight1: float,
    weight2: float,
    coupling: float,
) -> float:
    architecture_cost = _nonnegative(architecture_cost, "architecture_cost")
    coefficient = _conflict_coefficient(weight1, weight2)
    s = decoupling_fraction(weight1, weight2, coupling)
    if architecture_cost == 0:
        return 0.0
    if s == 0.0:
        raise ValueError("positive cost has no finite critical distance at zero decoupling")

    # dcrit^2 = K/(s*coefficient). Work in square roots so the intermediate
    # K/(s*coefficient) need not be representable when dcrit itself still is.
    denominator_root = math.sqrt(s) * math.sqrt(coefficient)
    if denominator_root == 0.0:
        raise ValueError("critical-distance denominator underflows; rescale units")
    value = math.sqrt(architecture_cost) / denominator_root
    return _finite_result(value, "critical optimum distance")


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
    cost = _nonnegative(architecture_cost, "architecture_cost")
    load = shared_conflict_load(optimum_distance, weight1, weight2)
    s = decoupling_fraction(weight1, weight2, coupling)
    recoverable = critical_cost(load, s)
    margin = recoverable - cost
    return CriticalityMap(
        shared_conflict_load=load,
        decoupling_fraction=s,
        architecture_cost=cost,
        recoverable_loss=recoverable,
        architecture_margin=margin,
        architecture_status=_roundoff_architecture_status(recoverable, cost),
        critical_cost=critical_cost(load, s),
        critical_shared_load=critical_shared_load(cost, s),
        critical_decoupling=critical_decoupling(load, cost),
        critical_coupling=critical_coupling(load, cost, weight1, weight2),
        critical_optimum_distance=critical_optimum_distance(
            cost, weight1, weight2, coupling
        ),
    )


def cross_world_equivalence_statement() -> dict[str, str]:
    return {
        "theory_architecture_surface": "SAME: s*L_S*=K <=> L_S*=K/s <=> K=s*L_S*",
        "sch_intrinsic_conflict_boundary": "DIFFERENT: L_S*=0 is conflict onset inside the fixed one-axis world",
        "bita_empirical_release_boundary": "DIFFERENT_UNITS: R_state=0 is geometric release onset",
        "current_empirical_equivalence": "NOT_YET_IDENTIFIED: requires commensurable fitness recovery, architecture cost, and paired SCH/BITA context",
    }
