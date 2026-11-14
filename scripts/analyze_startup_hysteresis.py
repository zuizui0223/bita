"""Reproduce conditional BITA persistence/entry boundaries and slow ramps."""
from __future__ import annotations
import argparse
from dataclasses import asdict
from itertools import product
import json
from math import expm1
from pathlib import Path

from trait_architecture.startup_hysteresis import continuation_thresholds,equilibria,local_attractor

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'docs/BITA_STARTUP_HYSTERESIS_READOUT_2026_11_14.json'


def build_readout() -> dict:
    kw=dict(cost_cap=.315,activation_scale=.3)
    t=continuation_thresholds(**kw)
    up,down={},{}
    u=0.
    for i in range(900,1101):
        d=i/1000
        u=local_attractor(u,distance=d,**kw)
        up[i]=u
    for i in range(1100,899,-1):
        d=i/1000
        u=local_attractor(u,distance=d,**kw)
        down[i]=u
    checked=passed=0
    for (w1,w2),lam,r,c in product(((1,1),(.5,2),(2,.5)),(0,.2,.5,1.5),(.2,.5,.8,.95,.99),(.1,.315)):
        h=w1*w2/(w1+w2); s=h/(h+lam)
        z=continuation_thresholds(cost_cap=c,weight_1=w1,weight_2=w2,coupling=lam,activation_scale=s*r)
        checked+=1
        passed+=z.persistence_distance<z.global_gain_distance<z.entry_distance
    if passed!=checked:
        raise AssertionError('declared ordering failed')
    low=equilibria(distance=.96,**kw)
    return {
        'model':'BITA_EXPONENTIAL_STARTUP_HISTORY_DEPENDENCE_V1',
        'source_model_commit':'924a2338dc253db4818648d9e550fdbec74de775',
        'data_level':'THEORY_ONLY','new_independent_biological_studies':0,
        'dynamics_assumption':'quasi-static projected-gradient ascent on u in [0,1]; fixed weights, coupling, cost and tau; no drift, finite jumps, recombination or physical-time inference',
        'cost_interpretation':'state-dependent cost, not a one-off historical expenditure; K(u) stays fixed as d varies',
        'stationary_equation':'log(d^2/d_entry^2)=t+expm1(-t)/r; t=-log(1-u/s), r=tau/s',
        'fold':'u_fold=s-tau; log(d_fold/d_entry)=(1-1/r-log(r))/2 for r<1',
        'synthetic_grid':{'n':checked,'strict_order_passed':passed,
            'weights':[[1,1],[.5,2],[2,.5]],'couplings':[0,.2,.5,1.5],
            'tau_over_s':[.2,.5,.8,.95,.99],'cost_caps':[.1,.315],
            'interpretation':'finite numerical audit, not natural frequencies or independent studies'},
        'example':{
            'parameters':dict(kw,weight_1=1.,weight_2=1.,coupling=.5),
            'thresholds':asdict(t),
            'locally_stable_but_globally_inferior':{
                'distance':.96,'equilibria':asdict(low),
                'score_of_differentiated_state':.96**2*(low.differentiated_fraction-low.differentiated_fraction**2)+.315*expm1(-low.differentiated_fraction/.3)},
            'same_environment_d1':{'from_shared':up[1000],'from_differentiated':down[1000]},
            'loop':{
                'ramp_min':.9,'ramp_max':1.1,'step':.001,
                'up_first_split_d':next(i/1000 for i in range(900,1101) if up[i]>0),
                'down_first_shared_d':next(i/1000 for i in range(1100,899,-1) if down[i]==0),
                'selected_path_points':[{'distance':i/1000,'ascending_u':up[i],'descending_u':down[i]}
                    for i in (940,947,948,960,980,1000,1020,1024,1025,1040,1060)],
                'boundary_interpretation':'grid event is bracketed by exact boundary, not an exact numeric replacement for it'}},
        'empirical_identification':{
            'current_lanes':['plant allocation','phylogenetic jaw covariance','floral interaction routing'],
            'identified_history_dependent_thresholds':0,
            'required_contrast':'same measured current environment and comparable lineages with independently recorded divergent histories; ideally controlled up/down perturbation with relaxation-time checks',
            'not_sufficient':['a cross-sectional trait-environment correlation','bimodality alone','related species differing in traits','a delayed transient without quasi-static stability','a null current association']},
        'claim_boundary':'conditional phenotype-landscape hysteresis under a specified local dynamic law; not evidence for historical origin, genetic inheritance, speciation, permanent irreversibility, empirical K(u), or a calibrated meta-analytic effect. The physical split is u*d; u is a normalized coordinate, not an observed organ size.',
    }


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=OUTPUT)
    args=parser.parse_args()
    out=build_readout()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2,sort_keys=True,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps({'output':str(args.output),'thresholds':out['example']['thresholds'],
                      'synthetic_grid':out['synthetic_grid']},sort_keys=True))

if __name__=='__main__':
    main()
