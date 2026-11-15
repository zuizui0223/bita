"""Tests distinguish source-verified summaries from nonexistent Dryad raw replicates."""
import hashlib
import json
import math
import pytest
from scripts import analyze_bita_pseudomonas_published_stats as m


def synthetic_jats():
    return b"""<article>
    <sec><title>Productivity of specialist and wildtype cultures</title>
    <p>four experimental blocks; eight (monocultures) and twelve (mixes) independent replicates.</p></sec>
    <sec><title>Specialization increases productivity in iron rich but not iron-limited media</title>
    <p>slope: 0.0002; slope = -0.0008; slope = -0.0011; slope = -0.0054</p>
    <p>t 73 = 12.17, p &lt; 0.0001; t 73 = 1.819, p = 0.0730;
       t 73 = -12.89, p &lt; 0.0001; t 71 = -6.745, p &lt; 0.0001</p>
    </sec>
    <sec><title>Negative frequency-dependent fitness patterns foster specialist co-existence</title>
    <p>slope=-0.0129, slope=-0.0048, slope=-0.0070, slope=-0.0075;
       fitted: 69.80%; 38.99%; 22.29%; 30.09%</p></sec>
    <fig><caption>Boxplots across 12 (mixes) independent replicates</caption></fig>
    </article>"""


def test_four_reported_t_tests_and_source_denominators(monkeypatch):
    x=synthetic_jats()
    monkeypatch.setattr(m,"JATS_SHA256",hashlib.sha256(x).hexdigest())
    d=m.parse_original_jats(x)
    assert d["environmental_strata_n"]==4
    assert d["independent_studies_n"]==1
    assert d["new_individual_growth_observations"]==0
    assert d["pooled_meta_analysis_performed"] is False
    v=d["conditions"]
    assert [r["condition"] for r in v] == ["iron_replete","plain_CAA","chelator_100uM","chelator_300uM"]
    assert [r["t_test_n_implied"] for r in v] == [74,74,74,72]
    assert [r["one_sample_t"] for r in v] == [12.17,1.819,-12.89,-6.745]
    assert v[0]["standardized_departure_from_wildtype_reference"]==pytest.approx(12.17/math.sqrt(74))
    assert v[2]["standardized_departure_from_wildtype_reference"]==pytest.approx(-12.89/math.sqrt(74))
    assert [r["productivity_direction_vs_wildtype"] for r in v]==[
       "higher","not_resolved","lower","lower"]
    assert [r["productivity_slope_vs_initial_pyochelin"] for r in v]==[
       0.0002,-0.0008,-0.0011,-0.0054]
    assert [r["fitted_pyochelin_equilibrium_percent"] for r in v]==[
       69.80,38.99,22.29,30.09]
    assert d["design"]["independent_experimental_blocks"]==4
    assert "not a raw mean" in d["claim_limit"]
    assert "not equivalence" in d["claim_limit"]
    json.dumps(d,allow_nan=False)


def test_source_fingerprint_is_fail_closed(monkeypatch):
    x=synthetic_jats()
    with pytest.raises(ValueError,match="sha256"):
        m.parse_original_jats(x)
    changed_t=x.replace(b"12.17",b"12.18",1)
    monkeypatch.setattr(m,"JATS_SHA256",hashlib.sha256(changed_t).hexdigest())
    with pytest.raises(ValueError,match="source WT"):
        m.parse_original_jats(changed_t)
    changed_slope=x.replace(b"0.0002",b"0.0003",1)
    monkeypatch.setattr(m,"JATS_SHA256",hashlib.sha256(changed_slope).hexdigest())
    with pytest.raises(ValueError,match="source"):
        m.parse_original_jats(changed_slope)


def test_missing_section_does_not_invent_values(monkeypatch):
    x=synthetic_jats().replace(b"Negative frequency-dependent",b"No matching headline")
    monkeypatch.setattr(m,"JATS_SHA256",hashlib.sha256(x).hexdigest())
    with pytest.raises(ValueError,match="section"):
        m.parse_original_jats(x)


def test_no_false_precision_or_independent_origin_estimates():
    assert m.JATS_SHA256=="ff26c2e12bcd44bc7137656a7290ac9944ebc6823e8aae405e7a7f4ce999d55e"
    assert "study" not in m.MEDIA[0][0].lower()


def test_frozen_original_jats_readout_not_an_invented_dryad_study():
    from pathlib import Path
    root=Path(__file__).resolve().parents[1]
    path=root/"empirical/trait_architecture_history/mridha2022_published_stats_readout.json"
    x=json.loads(path.read_text(encoding="utf8"))
    assert x["study_doi"]=="10.1111/jeb.14001"
    assert x["independent_studies_n"]==1
    assert x["environmental_strata_n"]==4
    assert x["new_individual_growth_observations"]==0
    assert x["pooled_meta_analysis_performed"] is False
    assert x["source_jats_sha256"]==m.JATS_SHA256
    assert x["dryad_download_gate"]=={"api_files_http":401,"browser_file_stream_http":403}
    v=x["conditions"]
    assert [r["one_sample_t"] for r in v]==[12.17,1.819,-12.89,-6.745]
    assert [r["productivity_direction_vs_wildtype"] for r in v]==[
        "higher","not_resolved","lower","lower"]
    assert [r["productivity_slope_vs_initial_pyochelin"] for r in v]==[
        .0002,-.0008,-.0011,-.0054]
    assert all(r["standardized_departure_from_wildtype_reference"]==
               pytest.approx(r["one_sample_t"]/math.sqrt(r["t_df"]+1),abs=2e-14)
               for r in v)
    assert x["design"]["independent_experimental_blocks"]==4
    assert "not the number of independent evolutionary origins" in x["claim_limit"]
