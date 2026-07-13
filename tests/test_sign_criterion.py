import pytest

from trait_architecture.sign_criterion import SignCriterion


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


def test_signed_channel_magnitudes_must_be_oriented_before_use() -> None:
    with pytest.raises(ValueError, match="must be non-negative after orientation"):
        SignCriterion(
            antagonist_relief=-0.1,
            mutualist_interference=0.2,
            joint_cost=0.1,
        )
