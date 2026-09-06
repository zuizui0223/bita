import math

from trait_architecture.multi_coupling_robustness import (
    directional_coupling_bound,
    euclidean_coupling_distance_bound,
    penalty_weighted_change,
)


def test_directional_bound_uses_penalty_weighted_rate():
    result = directional_coupling_bound(
        net_margin=0.6,
        active_penalties=[0.2, 0.5],
        direction=[1.0, 2.0],
    )
    assert math.isclose(result.weighted_penalty_rate, 1.2)
    assert math.isclose(result.minimum_distance_to_crossing, 0.5)
    assert result.crossing_possible_under_model


def test_zero_penalty_direction_has_no_later_crossing_under_model():
    result = directional_coupling_bound(
        net_margin=0.3,
        active_penalties=[0.0, 0.4],
        direction=[1.0, 0.0],
    )
    assert result.minimum_distance_to_crossing is None
    assert not result.crossing_possible_under_model


def test_euclidean_bound_matches_dual_norm_formula():
    bound = euclidean_coupling_distance_bound(
        net_margin=0.5,
        active_penalties=[3.0, 4.0],
    )
    assert math.isclose(bound, 0.1)


def test_penalty_weighted_change_identifies_forbidden_near_region():
    margin = 0.5
    weighted = penalty_weighted_change(
        active_penalties=[0.2, 0.4, 0.1],
        delta_coupling=[0.5, 0.5, 0.5],
    )
    assert weighted < margin


def test_invalid_multi_coupling_inputs_fail_closed():
    bad_calls = [
        lambda: directional_coupling_bound(net_margin=0.0, active_penalties=[1.0], direction=[1.0]),
        lambda: directional_coupling_bound(net_margin=0.2, active_penalties=[1.0, 2.0], direction=[1.0]),
        lambda: directional_coupling_bound(net_margin=0.2, active_penalties=[-1.0], direction=[1.0]),
        lambda: euclidean_coupling_distance_bound(net_margin=0.2, active_penalties=[]),
    ]
    for call in bad_calls:
        try:
            call()
        except ValueError:
            pass
        else:
            raise AssertionError("invalid multi-coupling inputs should fail")
