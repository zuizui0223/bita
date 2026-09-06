import pytest

from trait_architecture.full_decoupling_reachability import (
    FULL_CROSSING,
    UNREACHABLE,
    UNRESOLVED,
    classify_full_decoupling_reachability,
)


def test_unreachable_when_even_global_upper_bound_cannot_pay_deficit():
    out = classify_full_decoupling_reachability(
        current_coupling=[0.2, 0.1],
        active_penalties=[1.0, 1.0],
        deficit=1.0,
        curvature_lower=0.0,
        curvature_upper=2.0,
    )
    assert out.upper_full_gain < 1.0
    assert out.status == UNREACHABLE


def test_full_decoupling_guarantees_crossing_when_lower_bound_exceeds_deficit():
    out = classify_full_decoupling_reachability(
        current_coupling=[0.5, 0.5],
        active_penalties=[2.0, 1.0],
        deficit=1.0,
        curvature_lower=1.0,
        curvature_upper=3.0,
    )
    assert out.lower_full_gain > 1.0
    assert out.status == FULL_CROSSING


def test_reachability_can_remain_unresolved_between_bounds():
    out = classify_full_decoupling_reachability(
        current_coupling=[0.5],
        active_penalties=[1.0],
        deficit=0.7,
        curvature_lower=0.0,
        curvature_upper=2.0,
    )
    assert out.lower_full_gain <= out.deficit < out.upper_full_gain
    assert out.status == UNRESOLVED


def test_exact_curvature_collapses_full_gain_interval():
    out = classify_full_decoupling_reachability(
        current_coupling=[0.4, 0.3],
        active_penalties=[1.2, 0.8],
        deficit=0.5,
        curvature_lower=1.5,
        curvature_upper=1.5,
    )
    assert out.lower_full_gain == pytest.approx(out.upper_full_gain)


def test_invalid_inputs_fail_closed():
    with pytest.raises(ValueError):
        classify_full_decoupling_reachability(
            current_coupling=[0.1],
            active_penalties=[1.0, 2.0],
            deficit=1.0,
            curvature_upper=1.0,
        )
    with pytest.raises(ValueError):
        classify_full_decoupling_reachability(
            current_coupling=[0.1],
            active_penalties=[1.0],
            deficit=0.0,
            curvature_upper=1.0,
        )
