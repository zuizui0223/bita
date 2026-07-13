import math

import pytest

from trait_architecture.model import ModelParameters
from trait_architecture.robustness import (
    BASELINE_FORM,
    FunctionalForm,
    MixedPartialResult,
    RobustnessCase,
    evaluate_forms,
    mixed_partial,
    summarise_case,
)


def test_baseline_mixed_partial_matches_declared_analytic_expression() -> None:
    parameters = ModelParameters(
        attraction_gain=1.2,
        attraction_tracking=1.1,
        floral_defence_efficacy=0.75,
        defence_pollinator_cost=0.45,
        attraction_defence_shared_cost=0.10,
        assurance_outcross_dilution=0.10,
    )
    case = RobustnessCase(
        case_id="baseline",
        attraction=0.4,
        defence=0.3,
        assurance=0.2,
        pollinator_service=0.7,
        floral_damage_pressure=0.6,
    )

    result = mixed_partial(case, parameters)

    expected_antagonism = 0.6 * 1.1 * 0.75
    expected_pollination = 0.7 * 1.2 * 0.45 * math.exp(-0.45 * 0.3) * (1 - 0.10 * 0.2)
    expected_cost = 0.10
    assert result.antagonism_term == pytest.approx(expected_antagonism)
    assert result.pollination_obstruction_term == pytest.approx(expected_pollination)
    assert result.shared_cost_term == pytest.approx(expected_cost)
    assert result.mixed_partial == pytest.approx(expected_antagonism - expected_pollination - expected_cost)


def test_endpoint_normalized_saturating_attraction_changes_local_slope_not_endpoint_scale() -> None:
    parameters = ModelParameters()
    q = 1.0
    # b_A (1+q) A / (1+q A) equals b_A at A=1 and 0 at A=0.
    assert parameters.attraction_gain * (1 + q) / (1 + q) == pytest.approx(parameters.attraction_gain)

    case = RobustnessCase("saturating", 0.8, 0.5, 0.0, 0.8, 0.2)
    baseline = mixed_partial(case, parameters, BASELINE_FORM)
    saturated = mixed_partial(case, parameters, FunctionalForm("saturated", attraction_saturation=q))
    assert saturated.pollination_obstruction_term < baseline.pollination_obstruction_term


def test_endpoint_normalized_saturating_defence_changes_local_slope_not_endpoint_scale() -> None:
    parameters = ModelParameters()
    q = 1.0 / 0.35
    # e_F (1+q) D / (1+q D) equals e_F at D=1.
    assert parameters.floral_defence_efficacy * (1 + q) / (1 + q) == pytest.approx(
        parameters.floral_defence_efficacy
    )

    case = RobustnessCase("defence", 0.5, 0.9, 0.0, 0.2, 0.8)
    baseline = mixed_partial(case, parameters, BASELINE_FORM)
    saturated = mixed_partial(case, parameters, FunctionalForm("saturated", defence_saturation=q))
    assert saturated.antagonism_term < baseline.antagonism_term


def test_curved_joint_cost_preserves_corner_cost_scale() -> None:
    parameters = ModelParameters(attraction_defence_shared_cost=0.2)
    k = 1.0
    corner_cost = parameters.attraction_defence_shared_cost * (1 + 2 * k) / (1 + 2 * k)
    assert corner_cost == pytest.approx(parameters.attraction_defence_shared_cost)

    case = RobustnessCase("cost", 0.5, 0.5, 0.0, 0.5, 0.5)
    curved = mixed_partial(case, parameters, FunctionalForm("curved", shared_cost_curvature=k))
    assert curved.shared_cost_term == pytest.approx(parameters.attraction_defence_shared_cost)


def test_summary_calls_unanimity_only_over_the_supplied_tested_set() -> None:
    results = [
        MixedPartialResult("case", "one", 1.0, 0.0, 0.0, 1.0, "complementary"),
        MixedPartialResult("case", "two", 2.0, 0.0, 0.0, 2.0, "complementary"),
    ]
    summary = summarise_case(results)
    assert summary.modal_sign == "complementary"
    assert summary.robustness_class == "tested_set_unanimous"
    assert summary.modal_sign_agreement == 1.0


def test_summary_preserves_an_exact_sign_tie_as_mixed() -> None:
    results = [
        MixedPartialResult("case", "one", 1.0, 0.0, 0.0, 1.0, "complementary"),
        MixedPartialResult("case", "two", 0.0, 1.0, 0.0, -1.0, "substitutable"),
    ]
    summary = summarise_case(results)
    assert summary.modal_sign == "mixed"
    assert summary.robustness_class == "mixed_or_sensitive"
    assert summary.modal_sign_agreement == 0.5


def test_nonfinite_functional_form_values_are_rejected() -> None:
    with pytest.raises(ValueError, match="finite and non-negative"):
        FunctionalForm("bad", attraction_saturation=math.nan)
    with pytest.raises(ValueError, match="finite and non-negative"):
        FunctionalForm("bad", defence_saturation=math.inf)


def test_nonfinite_model_parameters_are_rejected_before_the_sweep() -> None:
    with pytest.raises(ValueError, match="finite and non-negative"):
        ModelParameters(attraction_tracking=math.inf)
    with pytest.raises(ValueError, match="finite and non-negative"):
        ModelParameters(attraction_gain=math.nan)


def test_default_forms_cover_baseline_and_three_nonlinear_variants() -> None:
    case = RobustnessCase("forms", 0.5, 0.5, 0.5, 0.5, 0.5)
    results = evaluate_forms(case, ModelParameters())
    assert {result.form_id for result in results} == {
        "baseline",
        "saturating_attraction",
        "saturating_defence",
        "saturating_both_curved_cost",
    }
