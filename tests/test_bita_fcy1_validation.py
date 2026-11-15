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
