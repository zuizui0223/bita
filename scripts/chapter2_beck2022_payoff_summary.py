"""Recompute the one-programme summary-statistic effect; never meta-pool contexts."""
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DIR=ROOT/"empirical"/"trait_architecture_history"
def compute(data):
    out=[]
    for r in data["rows"]:
        assert min(r["split_mean"],r["wt_mean"])>0 and min(r["split_n"],r["wt_n"])>=2
        y=math.log(r["split_mean"]/r["wt_mean"])
        v=(r["split_sd"]/r["split_mean"])**2/r["split_n"]+(r["wt_sd"]/r["wt_mean"])**2/r["wt_n"]
        out.append(dict(id=r["id"],lnRR=y,sampling_variance_delta=v,percent_change=100*math.expm1(y),approx_normal_95_ci_lnRR=[y-1.96*math.sqrt(v),y+1.96*math.sqrt(v)],conservative_t_df2_sensitivity_lnRR=[y-4.3026527297*math.sqrt(v),y+4.3026527297*math.sqrt(v)],growth_rate_percent_change_descriptive=100*(r["split_growth_rate"]/r["wt_growth_rate"]-1)))
    assert len(out)==2 and out[0]["id"]=="weak_buffer" and out[1]["id"]=="strong_buffer"
    y=out[1]["lnRR"]-out[0]["lnRR"]
    v=sum(r["sampling_variance_delta"] for r in out)
    return dict(independent_programmes=1,effect_rows=2,cross_study_pool_performed=False,rows=out,strong_minus_weak=dict(ln_ratio_of_ratios=y,ratio_of_ratios=math.exp(y),sampling_variance_delta_assuming_independent_contexts=v,approx_normal_95_ci_ln_ratio_of_ratios=[y-1.96*math.sqrt(v),y+1.96*math.sqrt(v)]),meta_gate="NOT_POOLABLE_SINGLE_PROGRAMME")
def check(a,b):
    if isinstance(a,dict):
        assert a.keys()==b.keys()
        for k in a: check(a[k],b[k])
    elif isinstance(a,list):
        assert len(a)==len(b)
        for x,y in zip(a,b): check(x,y)
    elif isinstance(a,float):
        assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-12)
    else: assert a==b
if __name__=="__main__":
    s=json.loads((DIR/"beck2022_payoff_summary_input.json").read_text())
    z=compute(s)
    check(z,json.loads((DIR/"beck2022_payoff_summary_readout.json").read_text()))
    print(json.dumps(z,indent=2))
