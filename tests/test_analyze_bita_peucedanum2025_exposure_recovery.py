"""Exposure-adjusted and fruit-retention regression contracts on synthetic rows only."""
from __future__ import annotations

import math

import pytest

from scripts import analyze_bita_peucedanum2025_exposure_recovery as e
from scripts import analyze_bita_peucedanum2025_within_context as w


def fixture_population() -> list[dict]:
    result=[]
    for plot_index, plot in enumerate(("HA","HL","HC","HD","KD")):
        for yr in (2022,2023):
            for j in range(8):
                perfect = 12 + (j*5+plot_index*3+yr)%17
                male = 18 + (j*7+plot_index*2+yr)%29
                height = 8 + (j*3+plot_index*7)%17
                eggs = (j*3 + plot_index*2 + yr)%9
                initial = min(perfect, 2+(j*2+plot_index)%15)
                final = max(0, initial - (j + plot_index)%4)
                result.append({
                    "Year":f"Y{yr}","Plot":plot,"ID":f"{plot}{yr}_{j}",
                    "HflowerN":str(perfect),"MflowerN":str(male),
                    "Height":str(height),"OvipN":str(eggs),
                    "PredationR":str((j+plot_index)%5/8),
                    "InitialFruitN":str(initial),"FinalFruitN":str(final),
                })
    return result


def test_perfect_target_control_is_distinct_from_total_display_control():
    a=w.make_population_rows(fixture_population(),"ovip")[0]
    assert len(a)==80
    perfect=w.fwl(a,permutations=49,controls=("log_perfect","height"))
    total=w.fwl(a,permutations=49,controls=("log_total","height"))
    assert perfect["controls"]==["log_perfect","height"]
    assert total["controls"]==["log_total","height"]
    assert perfect["residualized_allocation_sd"]>0
    assert total["residualized_allocation_sd"]>0
    assert perfect["within_context_allocation_beta"] != pytest.approx(
        total["within_context_allocation_beta"],abs=1e-6,
    )


def test_retention_rows_are_held_on_single_common_observed_support():
    pop=fixture_population()
    valid,stats=e.make_retention_rows(pop)
    assert stats["matched_retention_rows"]==80
    assert stats["excluded"]==0
    assert all(0<=r["y"]<=1 for r in valid)
    assert all(r["initial"]>=r["final"] for r in valid)
    good=valid[0]
    assert good["y"]==pytest.approx(good["final"]/good["initial"])
    # Removing plausible data is auditable and never converted to zero.
    pop[0]["FinalFruitN"]="999"
    pop[1]["InitialFruitN"]="0"
    pop[2]["FinalFruitN"]="NA"
    out,counts=e.make_retention_rows(pop)
    assert len(out)==77
    assert counts["excluded"]==3
    assert counts["exclusion_reasons"]=={
        "final_exceeds_initial":1,
        "missing_required":1,
        "zero_initial_unidentified_denominator":1,
    }


def test_source_locked_analysis_never_invents_causal_fitness_gain(monkeypatch):
    pop=fixture_population()
    monkeypatch.setattr(e,"checked_csvs",lambda blob:{"population":pop})
    out=e.analyze(b"fictitious_source_fixture")
    assert out["doi"]=="10.14943/hu95572"
    assert out["causal_fitness_or_heritability_identified"] is False
    assert out["raw_rows_redistributed"] is False
    assert out["matched_fruit_construction"]["matched_retention_rows"]==80
    assert set(out["matched_fruit_comparison"])=={
        "final_to_initial_fraction",
        "common_initial_fruits_log",
        "common_final_fruits_log",
    }
    assert {x["n_individuals"] for x in out["matched_fruit_comparison"].values()}=={80}
    assert all(x["five_geographic_plot_jackknife"]["n_geographic_plot_clusters"]==5
               for x in out["matched_fruit_comparison"].values())
    assert out["target_exposure_adjusted"]["ovip"]["n_source_complete"]==80
    assert out["target_exposure_adjusted"]["ovip"][
        "alternative_perfect_target_adjusted"]["controls"]==[
            "log_perfect","height",
        ]


def test_retention_does_not_treat_zero_initial_as_observed_zero_survival():
    rows=fixture_population()[:3]
    rows[0]["InitialFruitN"]="0"
    rows[0]["FinalFruitN"]="0"
    valid, audit=e.make_retention_rows(rows)
    assert len(valid)==2
    assert audit["exclusion_reasons"]=={"zero_initial_unidentified_denominator":1}
