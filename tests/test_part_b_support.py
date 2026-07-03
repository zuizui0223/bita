import math

import pytest

from trait_architecture.model import ModelParameters
from trait_architecture.robustness import (
    BASELINE_FORM,
    FunctionalForm,
    RobustnessCase,
    mixed_partial,
)
from trait_architecture.part_b_support import (
    CHANNEL_PARAMETER_FIELDS,
    break_even_shared_cost,
    envelope_break_even_map,
    parameters_from_channel_levels,
)


def _case() -> RobustnessCase:
    return RobustnessCase(
        case_id="c1",
        attraction=0.4,
        defence=0.3,
        assurance=0.2,
        pollinator_service=0.7,
        floral_damage_pressure=0.6,
    )


def test_break_even_equals_channel_balance_at_baseline() -> None:
    parameters = ModelParameters(
        attraction_gain=1.2,
        attraction_tracking=1.1,
        floral_defence_efficacy=0.75,
        defence_pollinator_cost=0.45,
        attraction_defence_shared_cost=0.10,
        assurance_outcross_dilution=0.10,
    )
    case = _case()

    result = break_even_shared_cost(case, parameters)
    decomposition = mixed_partial(case, parameters)

    # At the baseline form the shared-cost multiplier is exactly 1, so the
    # break-even shared cost equals the channel balance.
    assert result.shared_cost_multiplier == 1.0
    expected_balance = decomposition.antagonism_term - decomposition.pollination_obstruction_term
    assert result.channel_balance == pytest.approx(expected_balance)
    assert result.break_even_shared_cost == pytest.approx(expected_balance)


def test_break_even_sign_is_consistent_with_mixed_partial() -> None:
    # The mixed partial must be positive iff declared c_AD is below the break-even.
    case = _case()
    for c_ad in (0.0, 0.05, 0.10, 0.3, 0.8):
        parameters = ModelParameters(attraction_defence_shared_cost=c_ad)
        result = break_even_shared_cost(case, parameters)
        decomposition = mixed_partial(case, parameters)
        below = c_ad < result.break_even_shared_cost
        assert (decomposition.mixed_partial > 0) == below
        assert result.predicted_sign == decomposition.sign
        assert result.margin_to_break_even == pytest.approx(result.break_even_shared_cost - c_ad)


def test_curved_shared_cost_scales_break_even_down() -> None:
    # With curvature the c_AD term is amplified, so the break-even c_AD is lower.
    case = _case()
    parameters = ModelParameters()
    curved = FunctionalForm(form_id="curved", shared_cost_curvature=1.0)

    flat = break_even_shared_cost(case, parameters, BASELINE_FORM)
    bent = break_even_shared_cost(case, parameters, curved)

    expected_multiplier = 1.0 + 2.0 * 1.0 * (case.attraction + case.defence)
    assert bent.shared_cost_multiplier == pytest.approx(expected_multiplier)
    assert bent.break_even_shared_cost == pytest.approx(flat.channel_balance / expected_multiplier)
    assert bent.break_even_shared_cost < flat.break_even_shared_cost


def test_parameters_from_channel_levels_only_touches_the_four_arrows() -> None:
    base = ModelParameters(attraction_defence_shared_cost=0.17, assurance_outcross_dilution=0.13)
    overridden = parameters_from_channel_levels(
        base,
        {"attraction_gain": 0.9, "defence_pollinator_cost": 0.6},
    )
    assert overridden.attraction_gain == 0.9
    assert overridden.defence_pollinator_cost == 0.6
    # c_AD and c_R are never touched by Part B channel overrides.
    assert overridden.attraction_defence_shared_cost == 0.17
    assert overridden.assurance_outcross_dilution == 0.13


def test_parameters_from_channel_levels_rejects_non_channel_fields() -> None:
    with pytest.raises(ValueError):
        parameters_from_channel_levels(ModelParameters(), {"attraction_defence_shared_cost": 0.2})


def test_channel_fields_are_real_model_parameters() -> None:
    fields = set(ModelParameters().__dict__)
    assert set(CHANNEL_PARAMETER_FIELDS) <= fields


def test_envelope_map_labels_regimes_per_shared_cost_scenario() -> None:
    case = _case()
    # A complementarity-favouring level (strong tracking + efficacy, weak obstruction)
    # and a substitution-favouring level (weak tracking, strong obstruction).
    overrides = {
        "complementary_lean": {
            "attraction_gain": 0.4,
            "attraction_tracking": 1.4,
            "floral_defence_efficacy": 0.9,
            "defence_pollinator_cost": 0.2,
        },
        "substitutable_lean": {
            "attraction_gain": 1.6,
            "attraction_tracking": 0.2,
            "floral_defence_efficacy": 0.3,
            "defence_pollinator_cost": 0.9,
        },
    }
    rows = envelope_break_even_map(
        [case],
        overrides,
        shared_cost_scenarios=(0.05, 0.4),
    )
    assert len(rows) == 2
    by_level = {row["envelope_level"]: row for row in rows}

    # The complementary-lean level has a positive channel balance, so a small
    # declared shared cost still leaves it complementary.
    comp = by_level["complementary_lean"]
    assert comp["channel_balance"] > 0
    assert comp["regime_at_c_AD_0.05"] == "complementary"

    # The substitutable-lean level has a negative channel balance; even zero-ish
    # shared cost cannot make it complementary.
    subs = by_level["substitutable_lean"]
    assert subs["channel_balance"] < 0
    assert subs["regime_at_c_AD_0.05"] == "substitutable"
    assert subs["regime_at_c_AD_0.4"] == "substitutable"
