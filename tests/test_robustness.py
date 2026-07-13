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
    assert result.antagonism_term == expected_antagonism
    assert result.pollination_obstruction_term == expected_pollination
    assert result.shared_cost_term == expected_cost
    assert result.mixed_partial == expected_antagonism - expected_pollination - expected_cost


def test_saturating_attraction_reduces_pollination_obstruction_at_positive_attraction() -> None:
    parameters = ModelParameters()
    case = RobustnessCase(
        case_id="saturating",
        attraction=0.8,
        defence=0.5,
        assurance=0.0,
        pollinator_service=0.8,
        floral_damage_pressure=0.2,
    )

    baseline = mixed_partial(case, parameters, BASELINE_FORM)
    saturated = mixed_partial(case, parameters, FunctionalForm("saturated", attraction_saturation=1.0))

    assert saturated.pollination_obstruction_term < baseline.pollination_obstruction_term


def test_saturating_defence_reduces_marginal_protection_at_high_defence() -> None:
    parameters = ModelParameters()
    case = RobustnessCase(
        case_id="defence",
        attraction=0.5,
        defence=0.9,
        assurance=0.0,
        pollinator_service=0.2,
        floral_damage_pressure=0.8,
    )

    baseline = mixed_partial(case, parameters, BASELINE_FORM)
    saturated = mixed_partial(
        case,
        parameters,
        FunctionalForm("saturated", defence_half_saturation=0.35),
    )

    assert saturated.antagonism_term < baseline.antagonism_term


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
    with pytest.raises(ValueError, match="finite and positive"):
        FunctionalForm("bad", defence_half_saturation=math.inf)


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
