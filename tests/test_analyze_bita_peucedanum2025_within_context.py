"""Controlled fictitious samples: inferential code tests are not ecological evidence."""
from __future__ import annotations

import math

import pytest

from scripts import analyze_bita_peucedanum2025_within_context as w


def synthetic(n_groups=3,per_group=20):
    rows=[]
    for group in range(n_groups):
        for j in range(per_group):
            x=0.15 + .012*j + .016*group
            logtotal=math.log1p(50+(j*j+7*group)%45)
            height=8+(j*7+3*group)%19
            y=-2*x+.4*logtotal+.025*height+group*0.9
            rows.append({
                "group":f"Y202{group}/P{group}","plot":f"P{group}",
                "x":x,"log_total":logtotal,"height":height,"y":y,
            })
    return rows


def test_fwl_recovers_known_conditional_beta_and_group_fixed_effect():
    r=w.fwl(synthetic(),permutations=49)
    assert r["n_individuals"]==60
    assert r["n_context_groups"]==3
    assert r["within_context_allocation_beta"]==pytest.approx(-2,abs=1e-9)
    assert r["effect_per_10pp_male_share"]==pytest.approx(-0.2,abs=1e-10)
    assert r["two_sided_within_context_residual_permutation_p"]>=1/50


def test_fwl_permutation_reproducible_without_network():
    rows=synthetic()
    a=w.fwl(rows,permutations=99)
    b=w.fwl(rows,permutations=99)
    assert a==b


def test_invalid_group_and_constant_predictor_fail_closed():
    with pytest.raises(ValueError,match="INSUFFICIENT"):
        w.fwl(synthetic(n_groups=1,per_group=4))
    rows=synthetic()
    for row in rows:
        row["x"]=0.4
    with pytest.raises(ValueError,match="NO_WITHIN_CONTEXT"):
        w.fwl(rows)


def test_population_rows_disallow_missing_and_bound_rates():
    src=[
      {"Year":"Y2020","Plot":"HA","HflowerN":"10","MflowerN":"20",
       "Height":"12","OvipN":"2","PredationR":"0.4"},
      {"Year":"Y2020","Plot":"HA","HflowerN":"0","MflowerN":"0",
       "Height":"12","OvipN":"0","PredationR":"NA"},
      {"Year":"Y2020","Plot":"HA","HflowerN":"10","MflowerN":"20",
       "Height":"12","OvipN":"4","PredationR":"1.5"},
    ]
    x,missing=w.make_population_rows(src,"ovip")
    assert len(x)==2 and missing==1
    y,missing=w.make_population_rows(src,"predation")
    assert len(y)==1 and missing==2


def test_paternity_field_and_unit_consistency():
    raw=[{"HFlowerNo":"20","MFlowerNo":"30","Height":"12",
          "TotalFlowerNo":"80","SiredSeedNo":"5"}]
    data,exc=w.make_paternity_rows(raw)
    assert exc==0 and len(data)==1
    assert data[0]["x"]==pytest.approx(.6)
    assert data[0]["y"]==pytest.approx(math.log1p(5))



def test_five_plot_jackknife_quantifies_independent_site_uncertainty():
    estimates={
        "HA": -0.9988218466795866,
        "HC": -1.157998073403385,
        "HD": -1.4882103818652526,
        "HL": -1.0103294096575572,
        "KD": -1.4000164825504635,
    }
    receipt=w.five_plot_jackknife(-1.2127362061824114,estimates)
    assert receipt["status"]=="SMALL_FIVE_PLOT_JACKKNIFE_DIAGNOSTIC"
    assert receipt["n_geographic_plot_clusters"]==5
    assert receipt["degrees_of_freedom"]==4
    assert receipt["delete_one_plot_se"]==pytest.approx(.40066969636648936)
    assert receipt["approximate_t4_ci95"]==pytest.approx(
        [-2.3251736234602367,-0.10029878890458588]
    )
    assert receipt["interval_status"]=="EXCLUDES_ZERO"
    assert receipt["all_deleted_plot_estimates_same_sign"]


def test_five_plot_jackknife_does_not_overclaim_missing_sites():
    estimates={"HA":.1,"HC":.2,"HD":.3,"HL":.4,"KD":None}
    receipt=w.five_plot_jackknife(.25,estimates)
    assert receipt["status"]=="NOT_IDENTIFIED_INCOMPLETE_GEOGRAPHIC_JACKKNIFE"
    assert "approximate_t4_ci95" not in receipt
