"""Empirical dimensional-release estimands linking SCH Chapter 1 to BITA Chapter 2.

This module is intentionally distinct from the general architecture model in
``differentiation.py`` and from the local two-level A×D interaction estimands.

SCH's default multi-level crossed experiment directly identifies state-specific
references such as ``z_P*``. BITA can then ask whether adding or strengthening a
second functional coordinate moves the optimum of a retained coordinate ``x``
closer to that predeclared SCH reference.

The module evaluates already-estimated optima and common-scale fitness values. It
does not fit the underlying multi-level response surfaces or supply sampling
uncertainty; those must come from the registered experimental analysis.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Literal


ReferenceKind = Literal["state_specific", "pure_function"]


def _finite(value: float, name: str) -> None:
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")


def _non_negative(value: float, name: str) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and non-negative")


@dataclass(frozen=True)
class DimensionalReleaseResult:
    """Point-estimand summary for release of one retained trait coordinate.

    ``reference`` should normally be the SCH state-specific function-1-facing
    optimum (for the floral implementation, ``z_P*``). A pure-function reference
    is admissible only after SCH has independently passed its stricter
    context-stable component-optimum gate.
    """

    reference: float
    reference_kind: ReferenceKind
    x_opt_before: float
    x_opt_after: float
    distance_before: float
    distance_after: float
    release_amount: float
    fitness_before: float | None
    fitness_after: float | None
    fitness_gain: float | None
    moves_toward_reference: bool
    fitness_improves: bool | None
    status: str


@dataclass(frozen=True)
class PairedReferenceRelease:
    """Report state-specific and optional pure-function release separately."""

    state_specific: DimensionalReleaseResult
    pure_function: DimensionalReleaseResult | None


def evaluate_dimensional_release(
    *,
    reference: float,
    x_opt_before: float,
    x_opt_after: float,
    reference_kind: ReferenceKind = "state_specific",
    fitness_before: float | None = None,
    fitness_after: float | None = None,
    min_release: float = 0.0,
    min_fitness_gain: float = 0.0,
    tolerance: float = 1e-12,
) -> DimensionalReleaseResult:
    """Evaluate whether a second axis moves ``x*`` toward an SCH reference.

    The primary point estimand is

    ``release_amount = |x_before - reference| - |x_after - reference|``.

    Positive values mean that the optimized retained coordinate is closer to the
    reference after the second axis is added or strengthened. ``min_release`` is
    a prospectively declared biologically meaningful displacement.

    If common-scale optimized fitness values are supplied, ``fitness_gain`` is
    also evaluated. Fitness is deliberately optional because movement toward a
    reference and improvement of the total outcome are different claims.

    This function does not infer uncertainty. A confirmatory analysis should pass
    bootstrap/design-based intervals for the optima and release contrast through a
    separate registered inference layer.
    """

    if reference_kind not in {"state_specific", "pure_function"}:
        raise ValueError("reference_kind must be 'state_specific' or 'pure_function'")

    _finite(reference, "reference")
    _finite(x_opt_before, "x_opt_before")
    _finite(x_opt_after, "x_opt_after")
    _non_negative(min_release, "min_release")
    _non_negative(min_fitness_gain, "min_fitness_gain")
    _non_negative(tolerance, "tolerance")

    if (fitness_before is None) != (fitness_after is None):
        raise ValueError("fitness_before and fitness_after must be supplied together")
    if fitness_before is not None:
        _finite(fitness_before, "fitness_before")
        _finite(fitness_after, "fitness_after")

    distance_before = abs(x_opt_before - reference)
    distance_after = abs(x_opt_after - reference)
    release_amount = distance_before - distance_after
    moves = release_amount > min_release + tolerance

    if fitness_before is None:
        gain = None
        improves = None
        status = "STATE_SPECIFIC_RELEASE" if moves else "NO_DIMENSIONAL_RELEASE"
        if reference_kind == "pure_function" and moves:
            status = "PURE_FUNCTION_RELEASE"
    else:
        gain = fitness_after - fitness_before
        improves = gain > min_fitness_gain + tolerance
        if moves and improves:
            status = (
                "STATE_SPECIFIC_RELEASE_WITH_FITNESS_GAIN"
                if reference_kind == "state_specific"
                else "PURE_FUNCTION_RELEASE_WITH_FITNESS_GAIN"
            )
        elif moves:
            status = "REFERENCE_RELEASE_WITHOUT_FITNESS_GAIN"
        elif improves:
            status = "FITNESS_GAIN_WITHOUT_REFERENCE_RELEASE"
        else:
            status = "NO_DIMENSIONAL_RELEASE"

    return DimensionalReleaseResult(
        reference=reference,
        reference_kind=reference_kind,
        x_opt_before=x_opt_before,
        x_opt_after=x_opt_after,
        distance_before=distance_before,
        distance_after=distance_after,
        release_amount=release_amount,
        fitness_before=fitness_before,
        fitness_after=fitness_after,
        fitness_gain=gain,
        moves_toward_reference=moves,
        fitness_improves=improves,
        status=status,
    )


def evaluate_sch_handoff_release(
    *,
    z_p: float,
    x_opt_before: float,
    x_opt_after: float,
    z_f1: float | None = None,
    fitness_before: float | None = None,
    fitness_after: float | None = None,
    min_release: float = 0.0,
    min_fitness_gain: float = 0.0,
    tolerance: float = 1e-12,
) -> PairedReferenceRelease:
    """Evaluate the default SCH state reference and optional pure reference.

    ``z_p`` is the directly identified SCH function-1-facing *state-specific*
    optimum. ``z_f1`` must be supplied only when SCH has independently identified
    a context-stable component/pure-function optimum. The two results are returned
    separately so that the stronger lane cannot silently replace the default one.
    """

    state_specific = evaluate_dimensional_release(
        reference=z_p,
        reference_kind="state_specific",
        x_opt_before=x_opt_before,
        x_opt_after=x_opt_after,
        fitness_before=fitness_before,
        fitness_after=fitness_after,
        min_release=min_release,
        min_fitness_gain=min_fitness_gain,
        tolerance=tolerance,
    )

    pure = None
    if z_f1 is not None:
        pure = evaluate_dimensional_release(
            reference=z_f1,
            reference_kind="pure_function",
            x_opt_before=x_opt_before,
            x_opt_after=x_opt_after,
            fitness_before=fitness_before,
            fitness_after=fitness_after,
            min_release=min_release,
            min_fitness_gain=min_fitness_gain,
            tolerance=tolerance,
        )

    return PairedReferenceRelease(
        state_specific=state_specific,
        pure_function=pure,
    )
