"""Exact mathematical startup-window regressions for the existing BITA toy model.

All inputs here are explicitly SYNTHETIC, not biological effect estimates.
These tests do not replace the analytic proof in the accompanying note.
"""
from __future__ import annotations

from itertools import product
from math import expm1

import pytest

from trait_architecture.evolutionary_accessibility import (
    gain_at_fraction,
    initial_gradient,
    landscape,
)


def _h_s(weight_1: float, weight_2: float, coupling: float) -> tuple[float, float]:
    h = weight_1 * weight_2 / (weight_1 + weight_2)
    return h, h / (h + coupling)


def test_positive_gain_locally_trapped_outside_prior_sufficient_window():
    # s=0.5: tau=0.3 exceeds the old sufficient threshold s/2=0.25.
    # c=0.315 exceeds the old sufficient upper cap s*h*d^2=0.25.
    params = dict(
        distance=1.0, weight_1=1.0, weight_2=1.0,
        coupling=0.5, activation_scale=0.3, activation_cost_cap=0.315,
    )
    assert 0.25 < params["activation_scale"] < 0.5
    assert params["activation_cost_cap"] > 0.25
    assert initial_gradient(**params) == pytest.approx(-0.05, abs=1e-12)
    assert gain_at_fraction(0.3, **params) == pytest.approx(
        0.01088202396900434, abs=1e-12,
    )
    r = landscape(**params)
    assert r.classification == "GLOBAL_GAIN_BUT_LOCAL_TRAP"
    assert r.maximum_relative_fitness > 0.01088


@pytest.mark.parametrize("tau_multiplier", (1.0, 1.2, 2.0))
def test_no_positive_global_gain_when_tau_at_or_above_s(tau_multiplier: float):
    # Proof covers every u, not just the finite grid checked here.
    # 3 weights x 4 couplings x 3 distances x 3 caps x 3 tau ratios = 324.
    checked = 0
    for (w1, w2), lam, d, cap_factor in product(
        ((1.0, 1.0), (0.5, 2.0), (2.0, 0.5)),
        (0.0, 0.2, 0.5, 1.5),
        (0.3, 1.0, 2.0),
        (1.01, 1.2, 2.0),
    ):
        h, s = _h_s(w1, w2, lam)
        tau = s * tau_multiplier
        cap = 2 * h * d * d * tau * cap_factor
        params = dict(
            distance=d, weight_1=w1, weight_2=w2, coupling=lam,
            activation_scale=tau, activation_cost_cap=cap,
        )
        assert initial_gradient(**params) < 0
        r = landscape(**params)
        assert r.classification == "SHARED_GLOBAL_OPTIMUM"
        assert r.maximum_relative_fitness == pytest.approx(0.0, abs=1e-10)
        checked += 1
    assert checked == 108


def test_constructive_nonempty_cost_window_for_tau_below_s():
    # Construct c between the exact initial-gradient bound and Q(u).
    # This checks 3 weights x 4 couplings x 3 distances = 36 designs.
    checked = 0
    for (w1, w2), lam, d in product(
        ((1.0, 1.0), (0.5, 2.0), (2.0, 0.5)),
        (0.0, 0.2, 0.5, 1.5),
        (0.3, 1.0, 2.0),
    ):
        h, s = _h_s(w1, w2, lam)
        tau = 0.75 * s
        u = 0.05 * s
        gross_gain = d*d*(2*h*u - (h+lam)*u*u)
        q_u = gross_gain / (-expm1(-u/tau))
        lower_cap = 2*h*d*d*tau
        assert q_u > lower_cap
        cap = (lower_cap + q_u) / 2
        params = dict(
            distance=d, weight_1=w1, weight_2=w2, coupling=lam,
            activation_scale=tau, activation_cost_cap=cap,
        )
        assert initial_gradient(**params) < 0
        assert gain_at_fraction(u, **params) > 0
        assert landscape(**params).classification == "GLOBAL_GAIN_BUT_LOCAL_TRAP"
        checked += 1
    assert checked == 36


def test_bounded_cost_curvature_is_necessary_in_constructed_trap():
    # Phi''= -2(h+lambda)*d^2 + c/tau^2*exp(-u/tau).
    # Positive Phi'' somewhere is necessary for initially negative slope
    # to reach positive gain. The exponential's maximum Phi'' is at u=0.
    h, s = _h_s(1.0, 1.0, 0.5)
    assert s == pytest.approx(0.5)
    cap, tau, d, lam = 0.315, 0.3, 1.0, 0.5
    assert cap/(tau*tau) > 2*(h+lam)*d*d
    assert landscape(
        distance=d, coupling=lam, activation_scale=tau,
        activation_cost_cap=cap,
    ).classification == "GLOBAL_GAIN_BUT_LOCAL_TRAP"
