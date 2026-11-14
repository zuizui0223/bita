"""Reproduce the existing BITA model's exact critical-cost/distance readout."""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict
from itertools import product
import json
from math import expm1, isclose
from pathlib import Path

from trait_architecture.startup_thresholds import (
    conflict_distance_thresholds,
    startup_cost_window,
)

ROOT=Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT=ROOT/'docs'/'BITA_STARTUP_THRESHOLDS_READOUT_2026_11_14.json'


def build_readout() -> dict:
    counts=Counter()
    for (w1,w2), lam, cap, tau, d in product(
        ((1,1),(.5,2),(2,.5)), (0,.2,.5,1.5), (.03,.15,.4), (.01,.05,.2), (.3,.7,1,1.5,2),
    ):
        w=startup_cost_window(distance=d,weight_1=w1,weight_2=w2,coupling=lam,activation_scale=tau)
        if cap>=w.upper_cost or isclose(cap,w.upper_cost,rel_tol=1e-12):
            label='SHARED_GLOBAL_OPTIMUM'
        elif cap<w.lower_cost and not isclose(cap,w.lower_cost,rel_tol=1e-12):
            label='SMALL_STEPS_CAN_INVADE'
        elif cap>w.lower_cost and not isclose(cap,w.lower_cost,rel_tol=1e-12):
            label='GLOBAL_GAIN_BUT_LOCAL_TRAP'
        else:
            label='LOCAL_MARGINAL'
        counts[label]+=1
    expected={'SHARED_GLOBAL_OPTIMUM':205,'GLOBAL_GAIN_BUT_LOCAL_TRAP':175,'SMALL_STEPS_CAN_INVADE':160}
    if dict(counts)!=expected:
        raise AssertionError(f'frozen 540-cell count mismatch: {counts}')
    cap,tau=.315,.3
    curve=[{'u':i/20,'gain':i/20-(i/20)**2+cap*expm1(-(i/20)/tau)} for i in range(11)]
    return {
        'model':'BITA_EXPONENTIAL_STARTUP_EXACT_THRESHOLDS_V1',
        'data_level':'THEORY_ONLY',
        'source_model_commit':'c30aa3331eceaa657f779626ff2d2efdf22a0b18',
        'new_independent_biological_studies':0,
        'normalization':'r=tau/s, v=u/s, R=h*s*d^2; Ccrit=R*max Q_r(v)',
        'normalized_Q':'v*(2-v)/(1-exp(-v/r)); Q_r(0)=2*r',
        'positive_maximum_bracket':'1-r < v_star < 1 for 0<r<1; limiting maximum at v=0 for r>=1',
        'strict_cost_window':'2*h*d^2*tau < c < Ccrit; nonempty iff tau<s',
        'frozen_grid_concordance':{'n':540,'counts':dict(sorted(counts.items())),
            'comparison':'same 540 hypothetical cells and published counts, not independent ecological replication',
            'boundary_relative_tolerance':1e-12},
        'example':{
            'parameters':{'weight_1':1,'weight_2':1,'coupling':.5,'distance':1,'activation_scale':tau,'cost_cap':cap},
            'cost_window':asdict(startup_cost_window(distance=1,activation_scale=tau)),
            'thresholds':asdict(conflict_distance_thresholds(cost_cap=cap,activation_scale=tau)),
            'gain_curve':curve,
        },
        'tau_sensitivity_same_d1_weights_and_coupling':[
            {'tau':t,'lower_cost':w.lower_cost,'upper_cost':w.upper_cost,
             'tangent_fraction':w.tangent_fraction,'resolution':w.resolution}
            for t in (.05,.1,.2,.25,.3,.4,.45,.49,.5,.6)
            for w in [startup_cost_window(distance=1,activation_scale=t)]
        ],
        'claim_boundary':(
            'All thresholds are conditional on the assumed quadratic gain and exponential startup cost; '
            'not a genetic invasion or fixation proof, empirical K(u) estimate, historical-origin test, '
            'or estimate of natural strategy frequencies. Global equality has no strict global gain; local equality has zero slope but can have second-order benefit. '
            'Small-step labels refer only to deterministic phenotype-gradient conditions. '
            'Numerically unresolved windows must not be treated as absent.'
        ),
    }


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=DEFAULT_OUTPUT)
    args=parser.parse_args()
    data=build_readout()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(data,indent=2,sort_keys=True,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps({'output':str(args.output),'example':data['example']['thresholds'],
                      'frozen_grid':data['frozen_grid_concordance']},sort_keys=True))


if __name__=='__main__':
    main()
