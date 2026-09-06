import pytest

from trait_architecture.decoupling_cost_rescue import cost_rescue_bracket


def test_decoupling_alone_guaranteed_when_lower_gain_exceeds_deficit():
    out = cost_rescue_bracket(
        deficit=1.0,
        lower_full_gain=1.2,
        upper_full_gain=1.5,
    )
    assert out.necessary_cost_relief == 0.0
    assert out.sufficient_cost_relief == 0.0
    assert out.decoupling_alone_guaranteed
    assert not out.positive_cost_relief_necessary


def test_positive_cost_relief_is_necessary_when_upper_gain_is_too_small():
    out = cost_rescue_bracket(
        deficit=2.0,
        lower_full_gain=0.8,
        upper_full_gain=1.2,
    )
    assert out.necessary_cost_relief == pytest.approx(0.8)
    assert out.sufficient_cost_relief == pytest.approx(1.2)
    assert out.positive_cost_relief_necessary


def test_unresolved_interval_between_necessary_and_sufficient_relief():
    out = cost_rescue_bracket(
        deficit=1.0,
        lower_full_gain=0.7,
        upper_full_gain=1.1,
    )
    assert out.necessary_cost_relief == 0.0
    assert out.sufficient_cost_relief == pytest.approx(0.3)
    assert not out.decoupling_alone_guaranteed
    assert not out.positive_cost_relief_necessary


def test_exact_gain_collapses_cost_relief_interval():
    out = cost_rescue_bracket(
        deficit=1.5,
        lower_full_gain=0.9,
        upper_full_gain=0.9,
    )
    assert out.necessary_cost_relief == pytest.approx(0.6)
    assert out.sufficient_cost_relief == pytest.approx(0.6)


def test_invalid_gain_interval_fails_closed():
    with pytest.raises(ValueError):
        cost_rescue_bracket(
            deficit=1.0,
            lower_full_gain=1.2,
            upper_full_gain=1.0,
        )
