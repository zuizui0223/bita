"""Discrete identification estimands for attraction-defence experiments.

The experimental target is a two-level attraction (A) x defence (D) contrast,
crossed with selective antagonist (G) and pollinator (P) interventions. The
module deliberately separates three questions:

1. Can the biotic channel contrasts be recovered from the 16-cell design?
2. Do those contrasts remain invariant across the other consumer state, as
   required by the additive channel decomposition?
3. Does an independent joint-cost assay agree with the residual joint channel?

The 16-cell design is therefore not treated as sufficient by construction.
Channel estimates are labelled identified only after explicit intervention and
comparability assumptions pass and the cross-state invariance diagnostics are
within the declared numerical tolerance. In empirical work, invariance should
be assessed with uncertainty/equivalence methods rather than a hard tolerance.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isclose
from typing import Mapping

CellKey = tuple[int, int, int, int]  # A, D, antagonist present, pollinator present
ADKey = tuple[int, int]


@dataclass(frozen=True)
class IdentificationAssumptions:
    """Design-level conditions required before channel contrasts are causal.

    ``pollinator_independent_baseline_characterized`` does not require zero
    autonomous reproduction. It requires the P intervention to represent the
    pollinator-dependent increment without introducing an unmeasured A x D
    change in the pollinator-independent baseline (for example through bagging
    microclimate or simultaneous antagonist exclusion). Self-incompatible
    systems are one route; explicit baseline measurement is another.
    """

    antagonist_intervention_selective: bool
    pollinator_intervention_selective: bool
    pollinator_independent_baseline_characterized: bool
    trait_levels_comparable_across_cells: bool

    @property
    def all_pass(self) -> bool:
        return all(
            (
                self.antagonist_intervention_selective,
                self.pollinator_intervention_selective,
                self.pollinator_independent_baseline_characterized,
                self.trait_levels_comparable_across_cells,
            )
        )

    @property
    def failed(self) -> tuple[str, ...]:
        checks = {
            "antagonist_intervention_selective": self.antagonist_intervention_selective,
            "pollinator_intervention_selective": self.pollinator_intervention_selective,
            "pollinator_independent_baseline_characterized": self.pollinator_independent_baseline_characterized,
            "trait_levels_comparable_across_cells": self.trait_levels_comparable_across_cells,
        }
        return tuple(name for name, ok in checks.items() if not ok)


@dataclass(frozen=True)
class CrossedIdentificationResult:
    """Deterministic estimands and identification diagnostics for 16 cells."""

    delta_w_full: float
    rho_pollinator_absent: float
    rho_pollinator_present: float
    iota_antagonist_absent: float
    iota_antagonist_present: float
    rho_invariance_gap: float
    iota_invariance_gap: float
    assumptions_pass: bool
    separability_pass: bool
    identified: bool
    rho_delta: float | None
    iota_delta: float | None
    kappa_residual: float | None
    negative_kappa_forced_by_biotic_channels: bool | None
    failed_assumptions: tuple[str, ...]


@dataclass(frozen=True)
class JointCostAssayResult:
    """Independent A x D cost-curvature assay.

    ``kappa_delta`` is the discrete second difference of the measured cost
    endpoint. Its sign can be used without assuming scale equivalence to W. A
    magnitude comparison with the residual kappa requires the cost endpoint to
    be on the same declared outcome scale.
    """

    kappa_delta: float
    sign: str
    common_outcome_scale: bool


@dataclass(frozen=True)
class JointCostComparison:
    residual_kappa: float
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
    """Two-level A x D second difference: 11 - 10 - 01 + 00."""
    expected = {(0, 0), (0, 1), (1, 0), (1, 1)}
    if set(surface) != expected:
        raise ValueError("A x D surface must contain exactly {(0,0),(0,1),(1,0),(1,1)}")
    return surface[(1, 1)] - surface[(1, 0)] - surface[(0, 1)] + surface[(0, 0)]


def context_delta_ad(cells: Mapping[CellKey, float], antagonist_present: int, pollinator_present: int) -> float:
    """A x D interaction at one fixed consumer-state combination."""
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


def _pollinator_interference(cells: Mapping[CellKey, float], antagonist_present: int) -> float:
    """-Delta_AD of the pollinator-presence contrast at fixed G state."""
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
    invariance_tolerance: float = 1e-9,
) -> CrossedIdentificationResult:
    """Recover discrete channel contrasts and test their identification gates.

    Under an additive channel representation, antagonist relief should be the
    same whether pollinators are absent or present, and pollinator interference
    should be the same whether antagonists are absent or present. Violations are
    not silently absorbed into kappa: they fail the separability gate.

    ``invariance_tolerance`` is appropriate for deterministic simulations and
    software checks. Empirical analyses should replace it with uncertainty-aware
    equivalence/invariance tests.
    """
    if invariance_tolerance < 0:
        raise ValueError("invariance_tolerance must be non-negative")
    validate_crossed_cells(cells)

    rho_p0 = _antagonist_relief(cells, 0)
    rho_p1 = _antagonist_relief(cells, 1)
    iota_g0 = _pollinator_interference(cells, 0)
    iota_g1 = _pollinator_interference(cells, 1)
    rho_gap = rho_p1 - rho_p0
    iota_gap = iota_g1 - iota_g0

    separability_pass = isclose(rho_gap, 0.0, abs_tol=invariance_tolerance, rel_tol=0.0) and isclose(
        iota_gap, 0.0, abs_tol=invariance_tolerance, rel_tol=0.0
    )
    assumptions_pass = assumptions.all_pass
    identified = assumptions_pass and separability_pass

    rho = 0.5 * (rho_p0 + rho_p1) if identified else None
    iota = 0.5 * (iota_g0 + iota_g1) if identified else None
    delta_w_full = context_delta_ad(cells, 1, 1)
    kappa_residual = rho - iota - delta_w_full if identified and rho is not None and iota is not None else None
    forced_negative = (
        delta_w_full > 0 and rho <= iota
        if identified and rho is not None and iota is not None
        else None
    )

    return CrossedIdentificationResult(
        delta_w_full=delta_w_full,
        rho_pollinator_absent=rho_p0,
        rho_pollinator_present=rho_p1,
        iota_antagonist_absent=iota_g0,
        iota_antagonist_present=iota_g1,
        rho_invariance_gap=rho_gap,
        iota_invariance_gap=iota_gap,
        assumptions_pass=assumptions_pass,
        separability_pass=separability_pass,
        identified=identified,
        rho_delta=rho,
        iota_delta=iota,
        kappa_residual=kappa_residual,
        negative_kappa_forced_by_biotic_channels=forced_negative,
        failed_assumptions=assumptions.failed,
    )


def estimate_joint_cost_assay(cost_cells: Mapping[ADKey, float], *, common_outcome_scale: bool = False) -> JointCostAssayResult:
    """Estimate the independent discrete joint-cost curvature from four A x D cells."""
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
    """Compare residual and independently assayed joint-cost channels.

    A magnitude difference is returned only when the independent assay is on the
    same declared outcome scale. Otherwise only sign agreement is meaningful.
    """
    if identification.kappa_residual is None:
        raise ValueError("residual kappa is unavailable because the crossed-design identification gates did not pass")
    residual = identification.kappa_residual
    assay_value = assay.kappa_delta
    residual_sign = 0 if residual == 0 else (1 if residual > 0 else -1)
    assay_sign = 0 if assay_value == 0 else (1 if assay_value > 0 else -1)
    return JointCostComparison(
        residual_kappa=residual,
        assay_kappa=assay_value,
        sign_agrees=residual_sign == assay_sign,
        magnitude_difference=(residual - assay_value) if assay.common_outcome_scale else None,
    )
