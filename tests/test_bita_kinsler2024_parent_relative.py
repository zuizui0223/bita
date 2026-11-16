"""Inference-grain and author parent-relative sign tests, without source duplication."""
import math
import pytest

from scripts.analyze_bita_kinsler2024_parent_relative import (
    finite_field, phenotype_quadrant, summarize_group, analyzed_cohorts,
)


def row(f, r, s, a="IRA1_NON", env="Evo2D", cl="adaptive_haploid",
        pub="This_study", ferr="0.01", rerr="0.01"):
    return {
        "FerPerHour_relative": str(f),
        "ResPerHour_relative": str(r),
        "StaPerHour_relative": str(s),
        "FerPerHour_error": str(ferr),
        "ResPerHour_error": str(rerr),
        "ancestor": a, "evolution_condition": env, "class_new": cl,
        "source_publication": pub,
    }


def test_disjoint_quadrants_including_nonpositive():
    assert phenotype_quadrant(1, 1) == "both_fermentation_and_respiration_improve"
    assert phenotype_quadrant(-1, 1) == "respiration_gain_fermentation_cost"
    assert phenotype_quadrant(0, 1) == "respiration_gain_fermentation_zero"
    assert phenotype_quadrant(1, -1) == "fermentation_gain_respiration_not_positive"
    assert phenotype_quadrant(-1, -1) == "neither_performance_positive"


def test_exact_selected_clone_numerators_not_evolution_population_n():
    rows = [
        row(.05, .04, -.01),
        row(-.05, .04, .01),
        row(.01, .05, -.01),
        row(-.05, -.02, .03),
    ]
    d = summarize_group(rows)
    assert d["selected_clone_rows"] == 4
    assert d["complete_parent_relative_fermentation_respiration"] == 4
    assert d["descriptive_both_gain_share"] == .5
    assert d["descriptive_resp_gain_fer_cost_share"] == .25
    assert d["strict_two_reported_error_margin"]["both_positive_margin_gt_2errors"] == 1
    assert d["strict_two_reported_error_margin"]["resp_positive_and_fer_negative_margin_gt_2errors"] == 1
    assert d["stationary_phase"]["stationary_gain_among_both"] == 0
    assert d["stationary_phase"]["stationary_gain_among_resp_gain_fer_cost"] == 1
    assert d["inferential_unit"].startswith("selected_isolated_barcode")


def test_missingness_not_silently_filled():
    d = summarize_group([row("", ".04", ""), row(".03", ".04", ".01")])
    assert d["selected_clone_rows"] == 2
    assert d["complete_parent_relative_fermentation_respiration"] == 1
    assert d["missing_parent_relative_either"] == 1
    assert finite_field(row("nan",".01","0"), "FerPerHour_relative") is None
    assert finite_field(row("Infinity",".01","0"), "FerPerHour_relative") is None
    with pytest.raises(ValueError, match="negative"):
        summarize_group([row(".1",".1","0",rerr="-.2")])


def test_only_selected_2D_or_3D_advanced_mutants_enter_analysis():
    rows = [
        row(.1,.1,.1, a="IRA1_NON",env="Evo2D"),
        row(.1,.1,.1, a="CYR1",env="Evo3D"),
        row(.1,.1,.1, a="WT",env="Evo2D"),
        row(.1,.1,.1, a="IRA1_NON",env="Evo1D"),
        row(.1,.1,.1, a="IRA1_NON",env="Evo2D",cl="neutral_haploids"),
    ]
    selected, summary = analyzed_cohorts(rows)
    assert len(selected) == 2
    assert summary["selected_by_source_publication"]["This_study"] == 2
    assert summary["selected_by_condition_class"]["Evo2D|adaptive_haploid"] == 1
    assert summary["selected_by_condition_class"]["Evo3D|adaptive_haploid"] == 1
