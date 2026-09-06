import math

from trait_architecture.coupling_robustness import (
    coupling_robustness_bound,
    critical_coupling_cost_derivatives,
)


def symmetric_quadratic_recovery(lam: float, L: float = 0.5) -> float:
    return L / (1.0 + 2.0 * lam)


def symmetric_quadratic_derivative(lam: float, L: float = 0.5) -> float:
    return -2.0 * L / (1.0 + 2.0 * lam) ** 2


def symmetric_quadratic_second(lam: float, L: float = 0.5) -> float:
    return 8.0 * L / (1.0 + 2.0 * lam) ** 3


def test_tangent_bound_is_conservative_in_quadratic_case():
    L = 0.5
    K = 0.1
    lam0 = 1.0
    R0 = symmetric_quadratic_recovery(lam0, L)
    margin = R0 - K
    c0 = -symmetric_quadratic_derivative(lam0, L)

    result = coupling_robustness_bound(net_margin=margin, active_coupling_penalty=c0)
    exact_critical = (L / K - 1.0) / 2.0
    exact_distance = exact_critical - lam0

    assert result.minimum_extra_coupling_to_crossing is not None
    assert result.minimum_extra_coupling_to_crossing <= exact_distance + 1e-12
    assert result.later_crossing_possible_under_model


def test_zero_local_penalty_blocks_later_crossing_under_model():
    result = coupling_robustness_bound(net_margin=0.2, active_coupling_penalty=0.0)
    assert result.minimum_extra_coupling_to_crossing is None
    assert not result.later_crossing_possible_under_model


def test_critical_coupling_decreases_convexly_with_cost():
    lam = 0.8
    first_R = symmetric_quadratic_derivative(lam)
    second_R = symmetric_quadratic_second(lam)
    d1, d2 = critical_coupling_cost_derivatives(
        recovery_first=first_R,
        recovery_second=second_R,
    )
    assert d1 < 0
    assert d2 >= 0


def test_invalid_inputs_fail_closed():
    for kwargs in (
        {"net_margin": 0.0, "active_coupling_penalty": 1.0},
        {"net_margin": 0.2, "active_coupling_penalty": -0.1},
    ):
        try:
            coupling_robustness_bound(**kwargs)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid robustness inputs should fail")

    try:
        critical_coupling_cost_derivatives(recovery_first=0.0, recovery_second=1.0)
    except ValueError:
        pass
    else:
        raise AssertionError("nondecreasing recovery should fail")
