import pytest

from trait_architecture.model import ModelParameters
from trait_architecture.robustness import RobustnessCase, mixed_partial
from trait_architecture.sign_criterion import RegimeScaledCriterion, SignCriterion


def test_antagonist_relief_can_make_traits_locally_complementary() -> None:
    criterion = SignCriterion(
        antagonist_relief=1.2,
        mutualist_interference=0.5,
        joint_cost=0.2,
    )
    assert criterion.mixed_partial == pytest.approx(0.5)
    assert criterion.classify() == "locally_complementary"


def test_mutualist_interference_and_joint_cost_can_make_traits_substitutable() -> None:
    criterion = SignCriterion(
        antagonist_relief=0.4,
        mutualist_interference=0.5,
        joint_cost=0.2,
    )
    assert criterion.mixed_partial == pytest.approx(-0.3)
    assert criterion.classify() == "locally_substitutable"


def test_break_even_boundary_is_explicit() -> None:
    criterion = SignCriterion(
        antagonist_relief=0.7,
        mutualist_interference=0.5,
        joint_cost=0.2,
    )
    assert criterion.break_even_antagonist_relief == pytest.approx(0.7)
    assert criterion.classify() == "locally_neutral"


def test_baseline_robustness_result_is_a_corollary_of_general_criterion() -> None:
    case = RobustnessCase(
        case_id="baseline_corollary",
        attraction=0.4,
        defence=0.3,
        assurance=0.2,
        pollinator_service=0.6,
        floral_damage_pressure=0.7,
    )
    result = mixed_partial(case, ModelParameters())
    criterion = SignCriterion(
        antagonist_relief=result.antagonism_term,
        mutualist_interference=result.pollination_obstruction_term,
        joint_cost=result.shared_cost_term,
    )
    assert criterion.mixed_partial == pytest.approx(result.mixed_partial)


def test_signed_channel_magnitudes_must_be_oriented_before_use() -> None:
    with pytest.raises(ValueError, match="must be non-negative after orientation"):
        SignCriterion(
            antagonist_relief=-0.1,
            mutualist_interference=0.2,
            joint_cost=0.1,
        )


def test_more_antagonist_pressure_pushes_toward_complementarity() -> None:
    low_h = RegimeScaledCriterion(
        pollinator_service=0.6,
        antagonist_pressure=0.2,
        relief_rate=1.0,
        interference_rate=0.5,
        joint_cost=0.1,
    )
    high_h = RegimeScaledCriterion(
        pollinator_service=0.6,
        antagonist_pressure=0.8,
        relief_rate=1.0,
        interference_rate=0.5,
        joint_cost=0.1,
    )
    assert high_h.mixed_partial > low_h.mixed_partial
    assert high_h.d_mixed_partial_d_antagonist_pressure == pytest.approx(1.0)


def test_more_pollinator_service_pushes_toward_substitutability() -> None:
    low_p = RegimeScaledCriterion(
        pollinator_service=0.2,
        antagonist_pressure=0.6,
        relief_rate=0.8,
        interference_rate=0.7,
        joint_cost=0.1,
    )
    high_p = RegimeScaledCriterion(
        pollinator_service=0.8,
        antagonist_pressure=0.6,
        relief_rate=0.8,
        interference_rate=0.7,
        joint_cost=0.1,
    )
    assert high_p.mixed_partial < low_p.mixed_partial
    assert high_p.d_mixed_partial_d_pollinator_service == pytest.approx(-0.7)


def test_break_even_antagonist_pressure_is_predictive_boundary() -> None:
    criterion = RegimeScaledCriterion(
        pollinator_service=0.5,
        antagonist_pressure=0.0,
        relief_rate=0.8,
        interference_rate=0.6,
        joint_cost=0.1,
    )
    assert criterion.break_even_antagonist_pressure == pytest.approx(0.5)
