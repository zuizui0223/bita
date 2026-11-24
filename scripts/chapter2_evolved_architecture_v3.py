"""Verify source-summary counts and exact within-programme contrasts; no meta-pooling."""
import json, math
from pathlib import Path
D=Path(__file__).resolve().parents[1]/"empirical"/"trait_architecture_history"
def fisher(a,n,b,m):
    s=a+b
    denom=math.comb(n+m,s)
    def numerator(x):
        return math.comb(n,x)*math.comb(m,s-x)
    k=numerator(a)
    return sum(numerator(x) for x in range(max(0,s-m),min(n,s)+1) if numerator(x)<=k)/denom
def wilson(x,n):
    z=1.959963984540054
    p=x/n
    d=1+z*z/n
    c=(p+z*z/(2*n))/d
    h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return c-h,c+h
def rd(q):
    a,n,b,m=(q[k] for k in ("exposed_events","exposed_n","reference_events","reference_n"))
    p,r=a/n,b/m
    l1,u1=wilson(a,n)
    l2,u2=wilson(b,m)
    return dict(risk_difference=p-r,wilson_newcombe_95ci=[max(-1,p-r-math.hypot(p-l1,u2-r)),min(1,p-r+math.hypot(u1-p,r-l2))],fisher_two_sided_unpaired=fisher(a,n,b,m))
def verify():
    s=json.loads((D/"chapter2_evolved_architecture_intake_v3.json").read_text())
    o=json.loads((D/"chapter2_evolved_architecture_readout_v3.json").read_text())
    p,y,x,w=s["programmes"]
    assert len({a["programme"] for a in s["programmes"]})==4
    assert p["contrast"]==dict(exposed_events=6,exposed_n=6,reference_events=0,reference_n=6)
    assert p["sensitivity"]["reference_events"]==1
    for key,q in [("poltak_three_morphs",p["contrast"]),("poltak_any_novel_type_sensitivity",p["sensitivity"]),("altameemi_existing_retained_bimodality_unpaired_reference",dict(exposed_events=4,exposed_n=4,reference_events=0,reference_n=4))]:
        a,b=rd(q),o[key]
        for k in a:
            aa,bb=a[k],b[k]
            if isinstance(aa,list):
                assert all(math.isclose(i,j,abs_tol=1e-12) for i,j in zip(aa,bb))
            else: assert math.isclose(aa,bb,abs_tol=1e-12)
    assert math.isclose(x["maintenance"]["paired_nfds_slope_t"]/math.sqrt(x["maintenance"]["paired_nfds_slope_df"]+1),o["saxer_paired_slope_dz"])
    assert o["altameemi_paired_reference_two_sided"]==0.125
    assert x["origin"]["founding_populations"]==12 and x["maintenance"]["matched_original_populations"]==9
    assert not s["pande_s2"]["verified_original_bytes"]
    assert not o["cross_study_pool_performed"] and not o["endpoint_binary_pool_performed"]
    assert not o["yang_biomass_mean_effect_recovered"]
    print(json.dumps(o,indent=2))
if __name__=="__main__":
    verify()
