"""Theory-only exact exponential startup-cost thresholds; no biological data."""
from __future__ import annotations

from collections import Counter
from itertools import product
from math import expm1, isclose, nextafter

import pytest

from trait_architecture.startup_thresholds import (
    startup_cost_window,
    conflict_distance_thresholds,
)


def test_sharp_upper_cap_and_finite_jump_match_high_precision_reference():
    # Constants computed independently with mpmath at 60 decimal digits.
    w = startup_cost_window(distance=1, activation_scale=.3)
    assert w.lower_cost == pytest.approx(.3, abs=1e-15)
    assert w.upper_cost == pytest.approx(.332285925447970815855168, abs=2e-15)
    assert w.tangent_fraction == pytest.approx(.287829804463115959648252, abs=2e-14)
    assert w.exists_in_model is True
    assert w.numerically_resolved is True
    assert w.transition_type == 'FINITE_SEPARATION'


def test_two_conflict_thresholds_and_no_false_empirical_claim():
    t = conflict_distance_thresholds(cost_cap=.315, activation_scale=.3)
    assert t.global_gain_distance == pytest.approx(.9736420087943984519, abs=2e-14)
    assert t.local_gradient_distance == pytest.approx(1.0246950765959598383, abs=2e-14)
    assert t.global_gain_distance < 1 < t.local_gradient_distance
    assert t.data_level == 'THEORY_ONLY'


@pytest.mark.parametrize('r', [1., 1.001, 1.5, 10., 100.])
def test_no_strict_trap_window_at_or_above_tau_equals_s(r):
    w = startup_cost_window(distance=1, activation_scale=.5*r)
    assert w.exists_in_model is False
    assert w.lower_cost == w.upper_cost
    assert w.tangent_fraction == 0
    assert w.transition_type == 'CONTINUOUS'
    t = conflict_distance_thresholds(cost_cap=.315, activation_scale=.5*r)
    assert t.global_gain_distance == t.local_gradient_distance


@pytest.mark.parametrize('r, q, v', [
    (.1, 1.00004545364422134738, .99977247293606915814),
    (.6, 1.32914370179188326342, .57565960892623191930),
    (.9, 1.80760276821658565930, .14896153371182668229),
    (.99, 1.98007509458319319306, .01499053271773734948),
    (.9999, 1.99980000750009375826, .00014999906240858507),
])
def test_dimensionless_oracle_values(r, q, v):
    w = startup_cost_window(distance=1, activation_scale=.5*r)
    assert w.normalized_upper_cost == pytest.approx(q, rel=2e-14)
    assert w.tangent_fraction/.5 == pytest.approx(v, rel=3e-11, abs=1e-15)


def test_sub_float_window_is_not_mislabelled_absent():
    tau = nextafter(.5, 0.)
    w = startup_cost_window(distance=1, activation_scale=tau)
    assert w.exists_in_model is True
    assert w.numerically_resolved is False
    assert w.resolution == 'EXISTS_BELOW_FLOAT_RESOLUTION'
    assert w.tangent_fraction > 0


def test_very_small_tau_does_not_overflow_exponential():
    w = startup_cost_window(distance=1, activation_scale=1e-9)
    assert w.upper_cost == pytest.approx(.25)
    assert w.tangent_fraction == pytest.approx(.5)
    assert w.numerically_resolved


def test_units_and_function_weight_symmetry():
    w = startup_cost_window(distance=1, weight_1=.5, weight_2=2, coupling=.2, activation_scale=.3)
    swap = startup_cost_window(distance=1, weight_1=2, weight_2=.5, coupling=.2, activation_scale=.3)
    assert w == swap
    for factor in (1e-8, 1e8):
        scaled = startup_cost_window(distance=1, weight_1=.5*factor, weight_2=2*factor,
                                     coupling=.2*factor, activation_scale=.3)
        assert scaled.upper_cost == pytest.approx(w.upper_cost*factor, rel=3e-14)
        assert scaled.lower_cost == pytest.approx(w.lower_cost*factor, rel=3e-14)
        assert scaled.tangent_fraction == pytest.approx(w.tangent_fraction, abs=1e-14)
    twice = startup_cost_window(distance=2, weight_1=.5, weight_2=2, coupling=.2, activation_scale=.3)
    assert twice.upper_cost == pytest.approx(4*w.upper_cost)


def test_original_frozen_540_cells_agree_with_exact_threshold_classification():
    counts = Counter()
    for (w1,w2), lam, cap, tau, d in product(
        ((1,1),(.5,2),(2,.5)), (0,.2,.5,1.5), (.03,.15,.4), (.01,.05,.2), (.3,.7,1,1.5,2),
    ):
        w = startup_cost_window(distance=d, weight_1=w1, weight_2=w2,
                                coupling=lam, activation_scale=tau)
        if cap >= w.upper_cost or isclose(cap, w.upper_cost, rel_tol=1e-12):
            label = 'SHARED_GLOBAL_OPTIMUM'
        elif cap < w.lower_cost and not isclose(cap, w.lower_cost, rel_tol=1e-12):
            label = 'SMALL_STEPS_CAN_INVADE'
        elif cap > w.lower_cost and not isclose(cap, w.lower_cost, rel_tol=1e-12):
            label = 'GLOBAL_GAIN_BUT_LOCAL_TRAP'
        else:
            label = 'LOCAL_MARGINAL'
        counts[label] += 1
    assert counts == {'SHARED_GLOBAL_OPTIMUM':205, 'GLOBAL_GAIN_BUT_LOCAL_TRAP':175,
                      'SMALL_STEPS_CAN_INVADE':160}


def test_tangency_is_zero_gain_and_stationary_at_upper_cost():
    from math import exp
    for tau in (.025, .05, .1, .2, .3, .4, .45, .49):
        w = startup_cost_window(distance=1, activation_scale=tau)
        u, cap = w.tangent_fraction, w.upper_cost
        gain = u-u*u+cap*expm1(-u/tau)
        grad = 1-2*u-cap/tau*exp(-u/tau)
        assert abs(gain) < 2e-14
        assert abs(grad) < 2e-13
        midcap=(w.lower_cost+w.upper_cost)/2
        assert 1-midcap/tau < 0
        assert u-u*u+midcap*expm1(-u/tau) > 0


@pytest.mark.parametrize('kw', [
    {'distance':0}, {'distance':-1}, {'distance':float('nan')},
    {'weight_1':0}, {'weight_2':-1}, {'coupling':-1},
    {'activation_scale':0}, {'activation_scale':float('inf')},
    {'distance':1e200}, {'weight_1':1e-300, 'weight_2':1e300, 'coupling':1e300},
])
def test_invalid_or_unrepresentable_inputs_fail_closed(kw):
    with pytest.raises(ValueError):
        startup_cost_window(**dict({'distance':1}, **kw))


def test_zero_cost_threshold_and_invalid_cost():
    t=conflict_distance_thresholds(cost_cap=0, activation_scale=.3)
    assert t.global_gain_distance == t.local_gradient_distance == 0
    for c in (-1, float('nan'), float('inf')):
        with pytest.raises(ValueError):
            conflict_distance_thresholds(cost_cap=c)


def test_reproducible_readout_retains_grid_counts_and_theory_boundary():
    from scripts.analyze_startup_thresholds import build_readout
    out=build_readout()
    assert out['data_level']=='THEORY_ONLY'
    assert out['frozen_grid_concordance']['n']==540
    assert out['frozen_grid_concordance']['counts']=={
        'SHARED_GLOBAL_OPTIMUM':205, 'GLOBAL_GAIN_BUT_LOCAL_TRAP':175,
        'SMALL_STEPS_CAN_INVADE':160,
    }
    assert out['new_independent_biological_studies']==0
    assert out['example']['thresholds']['global_gain_distance']==pytest.approx(.9736420087943985)
    assert out['example']['thresholds']['local_gradient_distance']==pytest.approx(1.0246950765959598)
    assert out['example']['gain_curve'][6]['u']==pytest.approx(.30)
    assert out['example']['gain_curve'][6]['gain']==pytest.approx(.01088202396900434)
    assert 'not a genetic invasion or fixation proof' in out['claim_boundary']
    import json
    from pathlib import Path
    stored=Path(__file__).resolve().parents[1]/'docs/BITA_STARTUP_THRESHOLDS_READOUT_2026_11_14.json'
    assert json.loads(stored.read_text())==out


def test_zero_local_slope_can_still_allow_second_order_gain_when_tau_below_s():
    # Local equality is NOT a general no-invasion statement: at r<1,
    # Phi'(0)=0 but Phi''(0)>0. The API promises strictly positive gradient only.
    t=conflict_distance_thresholds(cost_cap=.315,activation_scale=.3)
    d=t.local_gradient_distance
    assert d*d-.315/.3 == pytest.approx(0,abs=1e-14)
    u=1e-4
    assert d*d*(u-u*u)+.315*expm1(-u/.3)>0


def test_underflowing_harmonic_weight_fails_with_valueerror_not_zero_division():
    with pytest.raises(ValueError):
        startup_cost_window(weight_1=5e-324,weight_2=5e-324,coupling=0)
