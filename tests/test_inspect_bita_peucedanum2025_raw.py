"""Test HUSCAP exact CSV parser, source guard, and plot/year grains (synthetic)."""
from __future__ import annotations

import hashlib
import io
import zipfile

import pytest

from scripts import inspect_bita_peucedanum2025_raw as raw


def fixture_blob():
    buff = io.BytesIO()
    with zipfile.ZipFile(buff,"w") as z:
        z.writestr("All_Plots_Data.csv",
            "Year,Plot,ID,HflowerN,MflowerN,InitialFruitN,Height,OvipN,FinalFruitN,PredationR\n"
            "Y2020,HA,PA01,20,70,16,16,4,8,0.47\n"
            "Y2020,HA,PA02,12,53,2,10,1,0,1\n"
            "Y2021,HL,PB01,8,4,10,12,0,9,NA\n")
        z.writestr("HA_Plot_Data.csv",
            "ID,HFlowerNo,MFlowerNo,Height,TotalMFlowerNo,TotalFlowerNo,"
            "InitialFruitNo,EstFinalFruitNo,DamagedFruitNo,SiredSeedNo\n"
            "A574,18,67,5,144,162,0,0,NA,1\n"
            "A575,17,44,11,136,153,0,0,NA,17\n")
    return buff.getvalue()


def test_exact_zip_header_join_and_aggregates(monkeypatch):
    blob=fixture_blob()
    monkeypatch.setattr(raw,"EXPECTED_ZIP_SHA256",hashlib.sha256(blob).hexdigest())
    diag=raw.inspect(blob)
    assert diag["n_population_rows"]==3
    assert diag["n_paternity_rows"]==2
    assert diag["population_year_counts"]=={"Y2020":2,"Y2021":1}
    assert diag["year_plot_aggregates"][0]["n_plants"]==2
    assert diag["year_plot_aggregates"][0]["male_fraction_mean"]==pytest.approx(
        ((70/(20+70)) + (53/(12+53)))/2)
    assert diag["numeric_fields"]["population"]["PredationR"]["missing"]==1
    assert diag["statistical_hypothesis_test_run"] is False
    assert diag["raw_rows_redistributed"] is False


def test_source_sha_mismatch_rejected_even_if_zip_valid():
    with pytest.raises(ValueError,match="SOURCE.*SHA256_DRIFT"):
        raw.inspect(fixture_blob())


def test_invalid_header_fails_closed(monkeypatch):
    blob=fixture_blob().replace(b"HflowerN",b"anotherx")
    monkeypatch.setattr(raw,"EXPECTED_ZIP_SHA256",hashlib.sha256(blob).hexdigest())
    with pytest.raises((ValueError,zipfile.BadZipFile)):
        raw.inspect(blob)


def test_na_and_zero_denominator_are_not_fabricated():
    assert raw.number("NA") is None
    assert raw.number("-") is None
    assert raw.number("0")==0
    assert raw.number("oops") is None
    assert raw.describe([None,None])=={"observed":0,"missing":2}
