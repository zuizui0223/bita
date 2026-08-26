"""Discrete identification estimands for attraction-defence experiments.

The experimental target is a two-level attraction (A) x defence (D) contrast,
crossed with selective antagonist (G) and pollinator (P) interventions. The
module deliberately separates four questions:

1. Can the consumer contrasts be recovered from the 16-cell design?
2. Do those contrasts remain invariant across the other consumer state, as
   required by an additive/separable channel representation?
3. Can the pollinator-dependent contrast be converted to the manuscript's
   total mutualist-interference estimand after accounting for the pollinator-
   absent baseline interaction M0_AD?
4. Does an independent joint-cost assay agree in sign (and, when commensurate,
   magnitude) with the residual joint channel?

The 16-cell design is therefore not treated as sufficient by construction.
Empirical analyses should estimate uncertainty for all contrasts and use an
explicit equivalence/invariance criterion; the hard numerical tolerance here is
only for deterministic calculations, simulations, and regression tests.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isclose
from typing import Mapping

CellKey = tuple[int, int, int, int]  # A, D, antagonist present, pollinator present
ADKey = tuple[int, int]


@dataclass(frozen=True)
class IdentificationAssumptions:
    """Design-level conditions required before consumer contrasts are causal.

    Selective means that toggling one consumer channel does not itself alter the
    other channel or the A/D manipulation. For example, a bag that simultaneously
    excludes pollinators and antagonists fails the pollinator-selectivity gate.
    ``trait_levels_comparable_across_cells`` requires the same biological A and D
    contrasts across all consumer-state cells.
    """

    antagonist_intervention_selective: bool
    pollinator_intervention_selective: bool
    trait_levels_comparable_across_cells: bool

    @property
    def all_pass(self) -> bool:
        return all(
            (
                self.antagonist_intervention_selective,
                self.pollinator_intervention_selective,
                self.trait_levels_comparable_across_cells,
            )
        )

    @property
    def failed(self) -> tuple[str, ...]:
        checks = {
            "antagonist_intervention_selective": self.antagonist_intervention_selective,
            "pollinator_intervention_selective": self.pollinator_intervention_selective,
            "trait_levels_comparable_across_cells": self.trait_levels_comparable_across_cells,
        }
        return tuple(name for name, ok in checks.items() if not ok)


@dataclass(frozen=True)
class CrossedIdentificationResult:
    """Deterministic estimands and identification diagnostics for 16 cells.

    ``iota_increment_delta`` is identified from the pollinator contrast as
    ``-Delta_AD(M1 - M0)``. It equals the manuscript's ``iota_delta = -Delta_AD M1``
    only when ``baseline_mutualist_delta = Delta_AD M0`` is supplied (including
    an explicitly justified zero, e.g. in a suitable self-incompatible design).

    ``four_way_coupling`` is the A x D x G x P interaction written in the
    antagonist-relief direction. The iota-invariance gap is its exact negative,
    so the two apparent invariance checks are not independent tests.
    """

    delta_w_full: float
    rho_pollinator_absent: float
    rho_pollinator_present: float
    iota_increment_antagonist_absent: float
    iota_increment_antagonist_present: float
    rho_invariance_gap: float
    iota_increment_invariance_gap: float
    four_way_coupling: float
    assumptions_pass: bool
    separability_pass: bool
    consumer_contrasts_identified: bool
    rho_delta: float | None
    iota_increment_delta: float | None
    baseline_mutualist_delta: float | None
    iota_total_delta: float | None
    unallocated_residual: float | None
    negative_joint_channel_forced: bool | None
    failed_assumptions: tuple[str, ...]


@dataclass(frozen=True)
class JointCostAssayResult:
    """Independent A x D cost-curvature assay.

    ``kappa_delta`` is the discrete second difference of the measured cost
    endpoint. Its sign can be used without assuming scale equivalence to W. A
    magnitude comparison with the crossed-design residual requires the cost
    endpoint to be on the same declared outcome scale and requires the residual
    to contain no other unmeasured A x D channel.
    """

    kappa_delta: float
    sign: str
    common_outcome_scale: bool


@dataclass(frozen=True)
class JointCostComparison:
    residual_joint_channel: float
    assay_kappa: float
    sign_agrees: bool
    magnitude_difference: float | None


def _require_binary(value: int, name: str) -> None:
    if value not in (0, 1):
        raise ValueError(f"{name} must be 0 or 1, got {value!r}")


def validate_crossed_cells(cells: Mapping[CellKey, float]) -> None:
    expected = {(a, d, g, p) for a in (0, 1) for d in (0, 1) for g in (0, 1) for p in (0, 1)}
    got = set(cells)
    missing = sorted(expected - got)
    extra = sorted(got - expected)
    if missing or extra:
        raise ValueError(f"crossed design must contain exactly 16 binary cells; missing={missing}, extra={extra}")


def delta_ad(surface: Mapping[ADKey, float]) -> float:
    """Two-level A x D second difference: 11 - 10 - 01 + 00.

    This is a secant interaction across the chosen A and D levels, not a local
    mixed partial. It approaches the derivative estimand only in a suitable
    small-contrast limit.
    """
    expected = {(0, 0), (0, 1), (1, 0), (1, 1)}
    if set(surface) != expected:
        raise ValueError("A x D surface must contain exactly {(0,0),(0,1),(1,0),(1,1)}")
    return surface[(1, 1)] - surface[(1, 0)] - surface[(0, 1)] + surface[(0, 0)]


def context_delta_ad(cells: Mapping[CellKey, float], antagonist_present: int, pollinator_present: int) -> float:
    """A x D second difference at one fixed consumer-state combination."""
    validate_crossed_cells(cells)
    _require_binary(antagonist_present, "antagonist_present")
    _require_binary(pollinator_present, "pollinator_present")
    surface = {
        (a, d): cells[(a, d, antagonist_present, pollinator_present)]
        for a in (0, 1)
        for d in (0, 1)
    }
    return delta_ad(surface)


def _antagonist_relief(cells: Mapping[CellKey, float], pollinator_present: int) -> float:
    """-Delta_AD of the antagonist-exclusion contrast at fixed P state."""
    surface = {
        (a, d): cells[(a, d, 0, pollinator_present)] - cells[(a, d, 1, pollinator_present)]
        for a in (0, 1)
        for d in (0, 1)
    }
    return -delta_ad(surface)


def _pollinator_increment_interference(cells: Mapping[CellKey, float], antagonist_present: int) -> float:
    """-Delta_AD of the pollinator-presence increment at fixed G state."""
    surface = {
        (a, d): cells[(a, d, antagonist_present, 1)] - cells[(a, d, antagonist_present, 0)]
        for a in (0, 1)
        for d in (0, 1)
    }
    return -delta_ad(surface)


def identify_crossed_design(
    cells: Mapping[CellKey, float],
    assumptions: IdentificationAssumptions,
    *,
    baseline_mutualist_delta: float | None = None,
    invariance_tolerance: float = 1e-9,
) -> CrossedIdentificationResult:
    """Recover consumer contrasts and test the identification gates.

    Parameters
    ----------
    cells:
        Sixteen mean/estimand values keyed by ``(A, D, G, P)``. ``G=1`` and
        ``P=1`` denote antagonist and pollinator presence respectively.
    assumptions:
        Explicit selectivity/comparability gates. Failed gates prevent causal
        channel identification even if the arithmetic contrasts can be formed.
    baseline_mutualist_delta:
        Independent estimate of ``Delta_AD M0`` under pollinator absence. Supply
        ``0.0`` only when zero interaction is biologically justified. If omitted,
        the design identifies pollinator-dependent interference in ``M1-M0`` but
        not the manuscript's total ``iota = -Delta_AD M1``; consequently the
        residual joint channel is not labelled identified.
    invariance_tolerance:
        Deterministic tolerance for the cross-state separability check. Replace
        with uncertainty-aware equivalence testing in empirical applications.
    """
    if invariance_tolerance < 0:
        raise ValueError("invariance_tolerance must be non-negative")
    validate_crossed_cells(cells)

    rho_p0 = _antagonist_relief(cells, 0)
    rho_p1 = _antagonist_relief(cells, 1)
    iota_g0 = _pollinator_increment_interference(cells, 0)
    iota_g1 = _pollinator_increment_interference(cells, 1)
    rho_gap = rho_p1 - rho_p0
    iota_gap = iota_g1 - iota_g0

    # Both expressions are the same A x D x G x P contrast up to sign.
    if not isclose(rho_gap, -iota_gap, abs_tol=1e-12, rel_tol=0.0):
        raise RuntimeError("internal contrast identity failed: rho and iota invariance gaps must be exact opposites")
    four_way = rho_gap
    separability_pass = isclose(four_way, 0.0, abs_tol=invariance_tolerance, rel_tol=0.0)
    assumptions_pass = assumptions.all_pass
    consumer_identified = assumptions_pass and separability_pass

    rho = 0.5 * (rho_p0 + rho_p1) if consumer_identified else None
    iota_increment = 0.5 * (iota_g0 + iota_g1) if consumer_identified else None
    iota_total = (
        iota_increment - baseline_mutualist_delta
        if consumer_identified and iota_increment is not None and baseline_mutualist_delta is not None
        else None
    )
    delta_w_full = context_delta_ad(cells, 1, 1)

    # The residual equals kappa only if the declared decomposition is complete,
    # M0_AD has been accounted for, and no additional A x D channel remains.
    residual = rho - iota_total - delta_w_full if rho is not None and iota_total is not None else None
    forced_negative = (
        delta_w_full > 0 and rho <= iota_total
        if rho is not None and iota_total is not None
        else None
    )

    return CrossedIdentificationResult(
        delta_w_full=delta_w_full,
        rho_pollinator_absent=rho_p0,
        rho_pollinator_present=rho_p1,
        iota_increment_antagonist_absent=iota_g0,
        iota_increment_antagonist_present=iota_g1,
        rho_invariance_gap=rho_gap,
        iota_increment_invariance_gap=iota_gap,
        four_way_coupling=four_way,
        assumptions_pass=assumptions_pass,
        separability_pass=separability_pass,
        consumer_contrasts_identified=consumer_identified,
        rho_delta=rho,
        iota_increment_delta=iota_increment,
        baseline_mutualist_delta=baseline_mutualist_delta,
        iota_total_delta=iota_total,
        unallocated_residual=residual,
        negative_joint_channel_forced=forced_negative,
        failed_assumptions=assumptions.failed,
    )


def estimate_joint_cost_assay(cost_cells: Mapping[ADKey, float], *, common_outcome_scale: bool = False) -> JointCostAssayResult:
    """Estimate independent discrete joint-cost curvature from four A x D cells."""
    kappa = delta_ad(cost_cells)
    if kappa > 0:
        sign = "positive"
    elif kappa < 0:
        sign = "negative"
    else:
        sign = "zero"
    return JointCostAssayResult(kappa_delta=kappa, sign=sign, common_outcome_scale=common_outcome_scale)


def compare_joint_cost(
    identification: CrossedIdentificationResult,
    assay: JointCostAssayResult,
) -> JointCostComparison:
    """Compare the crossed-design residual with an independent cost assay.

    Disagreement is diagnostically useful: it can indicate an incomplete channel
    decomposition, nonselective interventions, baseline misspecification, or a
    cost assay that is not measuring the same joint channel. The function never
    re-labels the residual as kappa merely because an assay exists.
    """
    if identification.unallocated_residual is None:
        raise ValueError(
            "joint-channel residual is unavailable because consumer identification or baseline correction is incomplete"
        )
    residual = identification.unallocated_residual
    assay_value = assay.kappa_delta
    residual_sign = 0 if residual == 0 else (1 if residual > 0 else -1)
    assay_sign = 0 if assay_value == 0 else (1 if assay_value > 0 else -1)
    return JointCostComparison(
        residual_joint_channel=residual,
        assay_kappa=assay_value,
        sign_agrees=residual_sign == assay_sign,
        magnitude_difference=(residual - assay_value) if assay.common_outcome_scale else None,
    )
