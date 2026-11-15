"""Selected screening positives versus independently assayed growth, without pseudoreplication."""
import math
import pytest

from scripts.analyze_bita_fcy1_validation import (
    SOURCE_COMMIT, SOURCE_POSITIVE_BLOB, VALIDATION_ALLELES,
    classify_panel, summarize_classification,
)

def test_prespecified_source_gate_and_panel():
    assert SOURCE_COMMIT == "f124cef96a3b5806a096b679b2bd57b68aec6514"
    assert SOURCE_POSITIVE_BLOB == "36839a3fd2eb05a521a070d11e60cde1748a682e"
    assert len(VALIDATION_ALLELES) == 18
    assert len(set(VALIDATION_ALLELES)) == 18
    assert "E64V" in VALIDATION_ALLELES and "M100W" in VALIDATION_ALLELES

def test_skipna_reciprocal_and_screen_confusion_contract():
    demo = [
        {"pair":("A","B"),"rates":(0.025,0.035)},  # screen+, growth+
        {"pair":("A","C"),"rates":(0.010,None)},   # screen+, growth-
        {"pair":("B","C"),"rates":(None,0.030)},   # screen-, growth+
        {"pair":("C","C"),"rates":(0.005,0.009)},  # screen-, growth-
        {"pair":("A","A"),"rates":(None,None)},    # unresolved
    ]
    annotated=classify_panel(demo,{("A","B"),("A","C")},threshold=.02)
    counts=summarize_classification(annotated)
    assert counts["n_total"]==5
    assert counts["n_measured"]==4
    assert counts["n_missing"]==1
    assert counts["true_positive"]==counts["false_positive"]==1
    assert counts["false_negative"]==counts["true_negative"]==1
    by_pair = {(r["allele_1"],r["allele_2"]):r for r in annotated}
    assert by_pair[("A","C")]["mean_growth_od_per_hour"]==pytest.approx(.01)
    assert by_pair[("B","C")]["mean_growth_od_per_hour"]==pytest.approx(.03)
    assert counts["screen_precision"]==pytest.approx(.5)
    assert counts["screen_specificity"]==pytest.approx(.5)

def test_threshold_equal_is_positive():
    x=classify_panel([{"pair":("A","B"),"rates":(.02,None)}],{("A","B")})
    assert summarize_classification(x)["true_positive"]==1

def test_duplicate_unordered_pairs_and_bad_inputs_fail_closed():
    with pytest.raises(ValueError,match="duplicate"):
        classify_panel([{"pair":("A","B"),"rates":(.1,None)},{"pair":("B","A"),"rates":(0,.1)}],set())
    with pytest.raises(ValueError,match="finite"):
        classify_panel([{"pair":("A","A"),"rates":(float("nan"),0)}],set())
    with pytest.raises(ValueError,match="unmeasured"):
        classify_panel([{"pair":("A","B"),"rates":(None,None)}],{("A","B")},allow_unmeasured=False)
    with pytest.raises(ValueError,match="positive screening pair"):
        classify_panel([{"pair":("A","B"),"rates":(.03,.04)}],{("A","C")})

def test_negative_assays_are_not_universal_failure_probability():
    xs=classify_panel([{"pair":("A","A"),"rates":(.0,.0)}],set())
    x=summarize_classification(xs)
    assert x["n_measured"]==1
    assert x["false_negative"]==0
    assert x["screen_precision"] is None
    assert x["screen_sensitivity"] is None


def test_frozen_source_reanalysis_keeps_discordant_self_pair_outside_heteromers():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    p = root / "empirical/trait_architecture_history/despres2024_growth_validation_summary.json"
    record = json.loads(p.read_text(encoding="utf-8"))
    assert record["source_growth_workbooks_available"] == 22
    assert record["source_growth_workbooks_missing"] == [
        "plate_6_C.xlsx", "plate_6_D.xlsx"]
    all_pairs = record["unrestricted_including_same_allele_controls"]
    assert (all_pairs["total_pairs"], all_pairs["measured"], all_pairs["missing"]) == (171,167,4)
    assert (all_pairs["screen_positive_and_growth_positive"],
            all_pairs["screen_positive_and_growth_negative"],
            all_pairs["screen_negative_and_growth_positive"],
            all_pairs["screen_negative_and_growth_negative"]) == (24,3,3,137)
    primary = record["primary_distinct_variant_pairs"]
    assert (primary["total_pairs"],primary["measured"],primary["missing"]) == (153,152,1)
    assert (primary["TP"],primary["FP"],primary["FN"],primary["TN"]) == (24,3,3,122)
    assert record["source_excluded_contaminated_control"]["pair"] == ["M93G","M93G"]
    assert record["source_excluded_contaminated_control"]["reason"] == "cross_contamination_reported_by_authors"
    assert record["source_excluded_contaminated_control"]["raw_measurement_retained_not_scored"] == pytest.approx(.13188)
    assert record["source_excluded_contaminated_control"]["in_primary_heteromer_analysis"] is False
    assert record["no_meta_analysis"] and record["fitness_comparison_shared_vs_divided_architecture_not_identified"]
