import pytest

from trait_architecture.balance_domain_dynamics import (
    architecture_action,
    local_environmental_hysteresis_width,
    persistence_band,
)


def test_positive_switching_costs_create_history_dependent_band():
    band = persistence_band(
        switching_cost_shared_to_differentiated=2.0,
        switching_cost_differentiated_to_shared=1.0,
        horizon=10.0,
    )
    assert band.reverse_threshold_phi == pytest.approx(-0.1)
    assert band.forward_threshold_phi == pytest.approx(0.2)
    assert band.width_phi == pytest.approx(0.3)

    # Same environment, different history: neither architecture switches.
    assert architecture_action(
        phi=0.05,
        current_architecture="shared",
        switching_cost_shared_to_differentiated=2.0,
        switching_cost_differentiated_to_shared=1.0,
        horizon=10.0,
    ) == "stay"
    assert architecture_action(
        phi=0.05,
        current_architecture="differentiated",
        switching_cost_shared_to_differentiated=2.0,
        switching_cost_differentiated_to_shared=1.0,
        horizon=10.0,
    ) == "stay"


def test_switching_occurs_outside_the_persistence_band():
    common = dict(
        switching_cost_shared_to_differentiated=2.0,
        switching_cost_differentiated_to_shared=1.0,
        horizon=10.0,
    )
    assert architecture_action(phi=0.21, current_architecture="shared", **common) == "switch"
    assert architecture_action(phi=-0.11, current_architecture="differentiated", **common) == "switch"


def test_static_phi_zero_boundary_is_recovered_when_switching_costs_vanish():
    band = persistence_band(
        switching_cost_shared_to_differentiated=0.0,
        switching_cost_differentiated_to_shared=0.0,
        horizon=10.0,
    )
    assert band.reverse_threshold_phi == 0.0
    assert band.forward_threshold_phi == 0.0
    assert band.width_phi == 0.0


def test_longer_environmental_persistence_collapses_dynamic_band_toward_static_boundary():
    short = persistence_band(
        switching_cost_shared_to_differentiated=2.0,
        switching_cost_differentiated_to_shared=1.0,
        horizon=5.0,
    )
    long = persistence_band(
        switching_cost_shared_to_differentiated=2.0,
        switching_cost_differentiated_to_shared=1.0,
        horizon=50.0,
    )
    assert long.width_phi < short.width_phi
    assert long.width_phi == pytest.approx(short.width_phi / 10.0)


def test_first_order_environmental_hysteresis_width():
    width = local_environmental_hysteresis_width(
        phi_slope_at_static_boundary=0.5,
        switching_cost_shared_to_differentiated=2.0,
        switching_cost_differentiated_to_shared=1.0,
        horizon=10.0,
    )
    assert width == pytest.approx(0.6)


def test_dynamic_model_fails_closed_on_invalid_horizon_or_architecture():
    with pytest.raises(ValueError):
        persistence_band(
            switching_cost_shared_to_differentiated=1.0,
            switching_cost_differentiated_to_shared=1.0,
            horizon=0.0,
        )
    with pytest.raises(ValueError):
        architecture_action(
            phi=0.0,
            current_architecture="unknown",
            switching_cost_shared_to_differentiated=1.0,
            switching_cost_differentiated_to_shared=1.0,
            horizon=1.0,
        )
