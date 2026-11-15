"""Source independence and claim ceiling contracts for BITA cross-system map."""
import csv
import json
from pathlib import Path
import pytest
from scripts.audit_bita_cross_system_registry import summarize

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "empirical/trait_architecture_history/cross_system_evidence_v1.csv"

def read():
    with CSV.open(newline="",encoding="utf-8") as stream:
        return list(csv.DictReader(stream))

def test_prespecified_independence_units_and_exclusions():
    s = summarize(read())
    assert s["source_publications_n"] == 8
    assert s["all_unique_programme_families_n"] == 7
    assert s["primary_source_publications_n"] == 6
    assert s["primary_independent_programme_families_n"] == 5
    assert s["context_only_source_publications_n"] == 2
    assert s["matched_history_programme_families_n"] == 0
    assert s["identified_architecture_origin_programme_families_n"] == 0
    assert s["new_study_level_effect_sizes_n"] == 0
    assert s["pooled_meta_analysis_performed"] is False

def test_salmonella_papers_share_a_research_family():
    a = [r for r in read() if r["source_id"].startswith("Nasvall")]
    assert len(a) == 2 and len({r["programme_family"] for r in a}) == 1

def test_experiments_not_pooled_from_variant_counts():
    r = read()
    d = next(x for x in r if x["source_id"] == "Despres_2024")
    assert "207" in d["source_observation"] and "613" in d["source_observation"]
    assert all(x["poolable_same_endpoint"] == "False" for x in r)

def test_negative_control_and_unavailable_original_source():
    m = next(x for x in read() if x["source_id"] == "Mihajlovic_2025")
    assert "no blue-green duplicate specialization" in m["source_observation"]
    assert "pending" in m["data_state"]
    assert m["architecture_origin_identified"] == "False"

def test_duplicate_and_pseudopooling_fail_closed():
    x=read()
    with pytest.raises(ValueError,match="duplicate"):
        summarize(x+[dict(x[0])])
    x[0]["poolable_same_endpoint"]="True"
    with pytest.raises(ValueError,match="prespecified"):
        summarize(x)

def test_frozen_summary_matches_programme_registry():
    p = CSV.with_name("cross_system_evidence_readout_v1.json")
    assert p.is_file()
    assert json.loads(p.read_text(encoding="utf-8")) == summarize(read())
