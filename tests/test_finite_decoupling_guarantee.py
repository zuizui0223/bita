import math

from trait_architecture.finite_decoupling import (
    certified_l2_budget_threshold,
    certified_linear_gain_floor,
    sufficient_static_crossing,
)


def test_convex_decreasing_exponential_recovery_exceeds_tangent_floor():
    # R(lambda)=exp(-lambda) is decreasing and convex.
    lambda0 = 1.0
    decoupling = 0.2
    c0 = math.exp(-lambda0)  # -R'(lambda0)
    exact_gain = math.exp(-(lambda0 - decoupling)) - math.exp(-lambda0)
    floor = certified_linear_gain_floor((c0,), (decoupling,))
    assert exact_gain >= floor


def test_sufficient_crossing_uses_certified_floor():
    assert sufficient_static_crossing(
        architecture_deficit=0.5,
        active_penalties=(2.0, 1.0),
        decoupling=(0.3, 0.0),
    )
    assert not sufficient_static_crossing(
        architecture_deficit=0.5,
        active_penalties=(2.0, 1.0),
        decoupling=(0.2, 0.0),
    )


def test_l2_threshold_is_deficit_over_penalty_norm():
    threshold = certified_l2_budget_threshold(5.0, (3.0, 4.0))
    assert math.isclose(threshold, 1.0, rel_tol=1e-12)
