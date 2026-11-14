"""Declared theory-only persistence and entry thresholds, never empirical data."""
from __future__ import annotations

from importlib import import_module
from itertools import product
from math import exp, expm1, isfinite, nextafter
from pathlib import Path
import json

import pytest


def api():
    # A missing implementation is an explicit test failure (not an import error).
    try:
        return import_module('trait_architecture.startup_hysteresis')
    except ModuleNotFoundError:
        pytest.fail('startup_hysteresis implementation is not yet present')


def phi(u, d, c=.315, tau=.3, h=.5, lam=.5):
    return d*d*(2*h*u-(h+lam)*u*u)+c*expm1(-u/tau)


def test_three_thresholds_match_independent_high_precision_reference():
    t=api().continuation_thresholds(cost_cap=.315,activation_scale=.3)
    assert t.persistence_distance == pytest.approx(.947881827184716126,abs=2e-14)
    assert t.global_gain_distance == pytest.approx(.973642008794398452,abs=2e-14)
    assert t.entry_distance == pytest.approx(1.02469507659595984,abs=2e-14)
    assert t.fold_fraction == pytest.approx(.2,abs=1e-15)
    assert t.has_hysteresis and t.numerically_resolved
    assert t.data_level == 'THEORY_ONLY'


def test_fold_is_stationary_and_zero_curvature_not_a_strict_maximum():
    t=api().continuation_thresholds(cost_cap=.315,activation_scale=.3)
    u,d=t.fold_fraction,t.persistence_distance
    assert abs(d*d*(1-2*u)-.315/.3*exp(-u/.3)) < 1e-14
    assert abs(-2*d*d+.315/.3**2*exp(-u/.3)) < 1e-14
    e=api().equilibria(distance=d,cost_cap=.315,activation_scale=.3)
    assert e.phase == 'FOLD_MARGINAL'
    with pytest.raises(ValueError,match='marginal'):
        api().local_attractor(.4,distance=d,cost_cap=.315,activation_scale=.3)


@pytest.mark.parametrize('d,phase',[(.90,'SHARED_ONLY'),(.96,'BISTABLE'),(1.,'BISTABLE'),(1.05,'DIFFERENTIATED_ONLY')])
def test_four_regimes_from_same_model(d,phase):
    e=api().equilibria(distance=d,cost_cap=.315,activation_scale=.3)
    assert e.phase == phase
    if phase=='BISTABLE':
        assert 0 < e.unstable_fraction < .2 < e.differentiated_fraction < .5
        assert e.shared_locally_stable


@pytest.mark.parametrize('d,lo,hi',[
    (.96,.127200259353487858,.262642717989735482),
    (1.,.0390001886335195764,.318280973258352611),
])
def test_two_roots_match_independent_oracle_and_have_opposite_curvature(d,lo,hi):
    e=api().equilibria(distance=d,cost_cap=.315,activation_scale=.3)
    assert e.unstable_fraction==pytest.approx(lo,abs=2e-14)
    assert e.differentiated_fraction==pytest.approx(hi,abs=2e-14)
    for u,sign in ((lo,1),(hi,-1)):
        assert abs(d*d*(1-2*u)-.315/.3*exp(-u/.3)) < 1e-13
        curvature=-2*d*d+.315/.3**2*exp(-u/.3)
        assert sign*curvature > 0


def test_retention_can_be_locally_stable_but_globally_inferior():
    e=api().equilibria(distance=.96,cost_cap=.315,activation_scale=.3)
    assert phi(e.differentiated_fraction,.96)==pytest.approx(-.0052724598839576334,abs=2e-14)
    assert api().local_attractor(0,distance=.96,cost_cap=.315,activation_scale=.3)==0
    assert api().local_attractor(.4,distance=.96,cost_cap=.315,activation_scale=.3)==pytest.approx(e.differentiated_fraction)


def test_shared_state_can_persist_despite_better_differentiated_state():
    e=api().equilibria(distance=1,cost_cap=.315,activation_scale=.3)
    assert phi(e.differentiated_fraction,1)>0
    assert api().local_attractor(0,distance=1,cost_cap=.315,activation_scale=.3)==0
    assert api().local_attractor(.4,distance=1,cost_cap=.315,activation_scale=.3)==pytest.approx(e.differentiated_fraction)
    with pytest.raises(ValueError,match='separatrix'):
        api().local_attractor(e.unstable_fraction,distance=1,cost_cap=.315,activation_scale=.3)


@pytest.mark.parametrize('r',[1.,1.01,2.,10.])
def test_continuous_negative_control_has_no_bistability_or_hysteresis(r):
    t=api().continuation_thresholds(cost_cap=.315,activation_scale=.5*r)
    assert not t.has_hysteresis
    assert t.persistence_distance==t.entry_distance==t.global_gain_distance
    assert t.fold_fraction==0
    for factor in (.8,.999,1.001,1.2):
        e=api().equilibria(distance=t.entry_distance*factor,cost_cap=.315,activation_scale=.5*r)
        assert e.phase==('SHARED_ONLY' if factor<1 else 'DIFFERENTIATED_ONLY')


def test_zero_startup_cost_and_zero_conflict_negative_controls():
    t=api().continuation_thresholds(cost_cap=0,activation_scale=.3)
    assert not t.has_hysteresis
    assert t.entry_distance==t.persistence_distance==t.global_gain_distance==0
    e=api().equilibria(distance=1,cost_cap=0,activation_scale=.3)
    assert e.differentiated_fraction==pytest.approx(.5)
    assert api().local_attractor(.25,distance=0,cost_cap=0,activation_scale=.3)==.25
    e=api().equilibria(distance=0,cost_cap=.315,activation_scale=.3)
    assert e.phase=='SHARED_ONLY'


def test_weight_exchange_and_score_unit_changes_preserve_thresholds():
    kw=dict(cost_cap=.315,weight_1=.5,weight_2=2,coupling=.2,activation_scale=.3)
    t=api().continuation_thresholds(**kw)
    assert api().continuation_thresholds(**dict(kw,weight_1=2,weight_2=.5))==t
    for scale in (1e-8,1e8):
        z=api().continuation_thresholds(**dict(kw,cost_cap=.315*scale,weight_1=.5*scale,weight_2=2*scale,coupling=.2*scale))
        for field in ('entry_distance','persistence_distance','global_gain_distance','fold_fraction'):
            assert getattr(z,field)==pytest.approx(getattr(t,field),rel=2e-13)


def test_fold_global_entry_order_across_fixed_120_synthetic_designs():
    n=0
    for (w1,w2),lam,r,c in product(((1,1),(.5,2),(2,.5)),(0,.2,.5,1.5),(.2,.5,.8,.95,.99),(.1,.315)):
        h=w1*w2/(w1+w2); s=h/(h+lam)
        t=api().continuation_thresholds(cost_cap=c,weight_1=w1,weight_2=w2,coupling=lam,activation_scale=s*r)
        assert t.persistence_distance < t.global_gain_distance < t.entry_distance
        n+=1
    assert n==120


def test_underflow_and_narrow_windows_are_flagged_not_declared_absent():
    a=api().continuation_thresholds(cost_cap=.315,activation_scale=1e-9)
    assert a.has_hysteresis
    assert a.persistence_distance is None
    assert isfinite(a.log_persistence_distance)
    assert not a.numerically_resolved
    b=api().continuation_thresholds(cost_cap=.315,activation_scale=nextafter(.5,0.))
    assert b.has_hysteresis and not b.numerically_resolved


@pytest.mark.parametrize('kw',[{'cost_cap':-1},{'cost_cap':float('nan')},{'activation_scale':0},{'coupling':-1},{'weight_1':0}])
def test_invalid_inputs_fail_closed(kw):
    with pytest.raises(ValueError):
        api().continuation_thresholds(**dict({'cost_cap':.315,'activation_scale':.3},**kw))


def test_script_and_frozen_readout_match_and_never_claim_biological_replication():
    try:
        build=import_module('scripts.analyze_startup_hysteresis').build_readout
    except ModuleNotFoundError:
        pytest.fail('hysteresis readout implementation is not yet present')
    out=build()
    assert out['data_level']=='THEORY_ONLY'
    assert out['new_independent_biological_studies']==0
    assert 'quasi-static projected-gradient' in out['dynamics_assumption']
    assert out['synthetic_grid']['n']==120
    assert out['synthetic_grid']['strict_order_passed']==120
    at_one=out['example']['same_environment_d1']
    assert at_one['from_shared']==0
    assert at_one['from_differentiated'] > .3
    assert out['example']['loop']['up_first_split_d']==pytest.approx(1.025)
    assert out['example']['loop']['down_first_shared_d']==pytest.approx(.947)
    stored=Path(__file__).resolve().parents[1]/'docs/BITA_STARTUP_HYSTERESIS_READOUT_2026_11_14.json'
    assert json.loads(stored.read_text())==out
