from __future__ import annotations

import pytest

from trait_architecture.identification import (
    IdentificationAssumptions,
    compare_joint_cost,
    delta_ad,
    estimate_joint_cost_assay,
    identify_crossed_design,
)


def assumptions(**overrides: bool) -> IdentificationAssumptions:
    values = {
        "antagonist_intervention_selective": True,
        "pollinator_intervention_selective": True,
        "trait_levels_comparable_across_cells": True,
    }
    values.update(overrides)
    return IdentificationAssumptions(**values)


def additive_cells(*, rho: float = 0.9, iota_increment: float = 0.5, m0_delta: float = 0.2, kappa: float = 0.2):
    """Synthetic W = M0 + P*J - G*Loss - C with known A x D terms."""
    # Delta_AD M0 = m0_delta
    # -Delta_AD J = iota_increment
    # -Delta_AD Loss = rho
    # Delta_AD C = kappa
    cells = {}
    for a in (0, 1):
        for d in (0, 1):
            m0 = 1.0 + 0.1 * a + 0.1 * d + m0_delta * a * d
            pollinator_increment = 0.4 + 0.3 * a + 0.1 * d - iota_increment * a * d
            antagonist_loss = 0.5 + 0.2 * a - 0.1 * d - rho * a * d
            cost = 0.1 * a + 0.1 * d + kappa * a * d
            for g in (0, 1):
                for p in (0, 1):
                    cells[(a, d, g, p)] = m0 + p * pollinator_increment - g * antagonist_loss - cost
    return cells


def test_delta_ad_is_two_level_secant_interaction() -> None:
    surface = {(0, 0): 1.0, (1, 0): 2.0, (0, 1): 3.0, (1, 1): 7.0}
    assert delta_ad(surface) == pytest.approx(3.0)


def test_crossed_design_recovers_rho_iota_and_joint_residual_after_baseline_correction() -> None:
    cells = additive_cells(rho=0.9, iota_increment=0.5, m0_delta=0.2, kappa=0.2)
    result = identify_crossed_design(cells, assumptions(), baseline_mutualist_delta=0.2)

    assert result.assumptions_pass
    assert result.separability_pass
    assert result.consumer_contrasts_identified
    assert result.rho_pollinator_absent == pytest.approx(0.9)
    assert result.rho_pollinator_present == pytest.approx(0.9)
    assert result.iota_increment_antagonist_absent == pytest.approx(0.5)
    assert result.iota_increment_antagonist_present == pytest.approx(0.5)
    assert result.rho_delta == pytest.approx(0.9)
    assert result.iota_increment_delta == pytest.approx(0.5)
    assert result.iota_total_delta == pytest.approx(0.3)
    assert result.delta_w_full == pytest.approx(0.4)
    assert result.unallocated_residual == pytest.approx(0.2)
    assert result.negative_joint_channel_forced is False


def test_missing_M0_interaction_does_not_silently_become_iota_or_kappa() -> None:
    result = identify_crossed_design(additive_cells(), assumptions())

    assert result.consumer_contrasts_identified
    assert result.rho_delta == pytest.approx(0.9)
    assert result.iota_increment_delta == pytest.approx(0.5)
    assert result.iota_total_delta is None
    assert result.unallocated_residual is None
    assert result.negative_joint_channel_forced is None


def test_nonselective_intervention_fails_identification_even_when_arithmetic_is_separable() -> None:
    result = identify_crossed_design(
        additive_cells(),
        assumptions(pollinator_intervention_selective=False),
        baseline_mutualist_delta=0.2,
    )

    assert result.separability_pass
    assert not result.assumptions_pass
    assert not result.consumer_contrasts_identified
    assert result.rho_delta is None
    assert result.iota_total_delta is None
    assert result.failed_assumptions == ("pollinator_intervention_selective",)


def test_cross_consumer_interaction_is_detected_as_separability_failure() -> None:
    cells = additive_cells()
    contaminated = dict(cells)
    for (a, d, g, p), value in cells.items():
        contaminated[(a, d, g, p)] = value + 0.25 * a * d * g * p

    result = identify_crossed_design(contaminated, assumptions(), baseline_mutualist_delta=0.2)

    assert result.assumptions_pass
    assert not result.separability_pass
    assert result.rho_invariance_gap != pytest.approx(0.0)
    assert result.iota_increment_invariance_gap != pytest.approx(0.0)
    assert not result.consumer_contrasts_identified
    assert result.unallocated_residual is None


def test_independent_joint_cost_assay_stays_distinct_from_residual() -> None:
    result = identify_crossed_design(additive_cells(), assumptions(), baseline_mutualist_delta=0.2)
    assay = estimate_joint_cost_assay(
        {(0, 0): 0.0, (1, 0): 0.1, (0, 1): 0.1, (1, 1): 0.4},
        common_outcome_scale=True,
    )
    comparison = compare_joint_cost(result, assay)

    assert assay.kappa_delta == pytest.approx(0.2)
    assert assay.sign == "positive"
    assert comparison.sign_agrees
    assert comparison.magnitude_difference == pytest.approx(0.0)


def test_complementarity_with_rho_not_exceeding_iota_forces_negative_joint_channel() -> None:
    cells = additive_cells(rho=0.4, iota_increment=0.5, m0_delta=0.0, kappa=-0.4)
    result = identify_crossed_design(cells, assumptions(), baseline_mutualist_delta=0.0)

    assert result.delta_w_full == pytest.approx(0.3)
    assert result.rho_delta == pytest.approx(0.4)
    assert result.iota_total_delta == pytest.approx(0.5)
    assert result.unallocated_residual == pytest.approx(-0.4)
    assert result.negative_joint_channel_forced is True


def test_cost_comparison_requires_identified_residual() -> None:
    result = identify_crossed_design(additive_cells(), assumptions())
    assay = estimate_joint_cost_assay({(0, 0): 0.0, (1, 0): 0.0, (0, 1): 0.0, (1, 1): 0.2})
    with pytest.raises(ValueError, match="residual is unavailable"):
        compare_joint_cost(result, assay)
