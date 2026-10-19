"""Synthetic fixture validation of actual 2025 source reanalysis (not evidence)."""
from __future__ import annotations

import hashlib
import io
import zipfile
import json

import pytest

from scripts import analyze_bita_peucedanum2025_population_patterns as a
from scripts import inspect_bita_peucedanum2025_raw as raw


def synthetic():
    p=["Year,Plot,ID,HflowerN,MflowerN,InitialFruitN,Height,OvipN,FinalFruitN,PredationR"]
    for year in ("Y2022","Y2023"):
        for i,plot in enumerate(("HA","HL","HC","HD","KD")):
            for j in range(5):
                m=10+i*8+j
                h=30-i*3+j
                pred=0.1+0.12*i
                p.append(f"{year},{plot},P{i}{j}{year},{h},{m},10,14,{i+j%2},7,{pred}")
    x=["ID,HFlowerNo,MFlowerNo,Height,TotalMFlowerNo,TotalFlowerNo,InitialFruitNo,EstFinalFruitNo,DamagedFruitNo,SiredSeedNo"]
    for i in range(40):
        h=5+i%13
        m=15+i%17
        x.append(f"HA{i},{h},{m},12,{m+5},{h+m+5},{h},{i%11},2,{i%7}")
    buff=io.BytesIO()
    with zipfile.ZipFile(buff,"w") as z:
        z.writestr("All_Plots_Data.csv","\n".join(p)+"\n")
        z.writestr("HA_Plot_Data.csv","\n".join(x)+"\n")
    return buff.getvalue()


def test_direct_raw_2025_observational_pattern_and_exact_five_plot_grain(monkeypatch):
    blob=synthetic()
    monkeypatch.setattr(raw,"EXPECTED_ZIP_SHA256",hashlib.sha256(blob).hexdigest())
    result=a.analyze_data(blob)
    assert result["n_plants_total"]==50
    assert result["n_paternity_plants"]==40
    assert result["n_distinct_plots"]==5
    assert result["n_plot_years"]==10
    assert result["n_plot_years_with_predation"]==10
    assert result["five_plot_exact"]["n_exact_permutations"]==120
    assert result["five_plot_exact"]["p_exact_two_sided"]>=1/120
    assert result["ha_paternity_exploratory_spearman"]["total_display_vs_siring"]["n_individuals"]==40
    assert result["raw_rows_redistributed"] is False
    assert '"P0' not in json.dumps(result)


def test_exact_plot_rho_p_handles_n5_and_ties():
    plots=[{"male_fraction":x,"mean_predation":y}
           for x,y in zip((.1,.2,.3,.4,.5),(.1,.2,.3,.4,.5))]
    ans=a.exact_plot_permutation(plots,"male_fraction","mean_predation")
    assert ans["rho"]==pytest.approx(1)
    assert ans["p_exact_two_sided"]==pytest.approx(2/120)
    with pytest.raises(ValueError,match="FIVE"):
        a.exact_plot_permutation(plots[:4],"male_fraction","mean_predation")


def test_rank_ties_mean_rank_and_rank_test_null():
    assert a.average_ranks([4,4,2,1])==[3.5,3.5,2,1]
    assert a.spearman([1,2,3],[3,2,1])==pytest.approx(-1)
    assert a.spearman([1,1,1],[2,3,4]) is None


def test_partial_source_drift_fails_before_biological_analysis():
    with pytest.raises(ValueError,match="2025_HUSCAP_ARCHIVE_SHA256_DRIFT"):
        a.analyze_data(synthetic())
