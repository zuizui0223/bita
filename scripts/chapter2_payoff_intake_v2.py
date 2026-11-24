"""Recalculate bounded Chapter 2 source-summary quantities; no cross-study pooling."""
import json, math
from pathlib import Path
D=Path(__file__).resolve().parents[1]/"empirical"/"trait_architecture_history"
s=json.loads((D/"chapter2_payoff_intake_v2_input.json").read_text())
o=json.loads((D/"chapter2_payoff_intake_v2_readout.json").read_text())
b,p,d,m,e=s["sources"]
y=math.log(b["mix_mean"]/b["wt_mean"])
v=(b["mix_sd"]/b["mix_mean"])**2/b["mix_n"]+(b["wt_sd"]/b["wt_mean"])**2/b["wt_n"]
def same(a,b):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-12),(a,b)
same(y,o["bernstein"]["lnRR"]);same(v,o["bernstein"]["variance_delta"])
same(100*math.expm1(y),o["bernstein"]["percent_change"])
for key,k in [("approx_normal_95_ci_lnRR",1.96),("t_df2_sensitivity_lnRR",4.3026527297)]:
    for a,b in zip([y-k*math.sqrt(v),y+k*math.sqrt(v)],o["bernstein"][key]):same(a,b)
same(p["significantly_higher_pairs"]/p["tested_pairs"],o["pande"]["significant_positive_fraction_of_tested_construct_pairs"])
assert p["remaining_pairs"]==p["tested_pairs"]-p["significantly_higher_pairs"]
# df=10; t(0.98,10) computed using scipy.stats.t.ppf, fixed numerical quantile.
df=d["mix_n"]+d["wt_n"]-2
assert df==10 and d["p_upper_two_sided"]==0.04
tcrit=2.359314623736535
J=math.exp(math.lgamma(df/2)-0.5*math.log(df/2)-math.lgamma((df-1)/2))
bound=tcrit*math.sqrt(1/d["mix_n"]+1/d["wt_n"])
same(bound,o["dragos"]["cohens_d_strict_lower_bound"])
same(J*bound,o["dragos"]["hedges_g_strict_lower_bound"])
up=(e["aae_max_rounded_mean_across_four_weak_buffer_initial_ph"]+0.005)/(e["wt_weak_buffer_ph7_rounded_mean"]-0.005)
same(up,o["beck"]["aae_pH7_ratio_rounding_conservative_upper_bound"])
same(math.log(up),o["beck"]["aae_pH7_lnRR_rounding_conservative_upper_bound"])
assert not o["coverage"]["pooled_meta_analysis"]
assert not o["bernstein"]["strict_pool_eligible"]
assert o["dragos"]["not_point_estimate"]
assert not o["beck"]["strict_equal_total_density_verified"]
print(json.dumps(o,indent=2))
