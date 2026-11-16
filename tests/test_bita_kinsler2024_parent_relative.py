"""Inference-grain and author parent-relative sign tests, without source duplication."""
import math
import json
from pathlib import Path
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


def test_stationary_source_error_threshold_is_distinct_from_positive_sign():
    rows = [
        row(.05, .04, .019),  # s>0 but below the source error of .02
        row(-.05, .04, .021), # s>error; respiration gain and fermentation cost
        row(.05, .04, .030),  # both gain and stationary gain>error
    ]
    for x in rows:
        x["StaPerHour_error"] = ".02"
    q = summarize_group(rows)
    st = q["stationary_phase"]
    assert st["stationary_gain_among_both"] == 2  # raw s>0 and f,r>0
    assert st["stationary_positive_exceeds_deposited_error"] == 2
    assert st["stationary_positive_exceeds_error_among_both"] == 1
    assert st["stationary_positive_exceeds_error_among_other"] == 1
    assert st["stationary_with_error_available"] == 3
    rows[1]["StaPerHour_error"] = "-.01"
    with pytest.raises(ValueError, match="negative"):
        summarize_group(rows)


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


def test_frozen_original_publisher_table_count_reproduction():
    root = Path(__file__).resolve().parents[1]
    frozen = json.loads((root / (
        "empirical/trait_architecture_history/"
        "kinsler2024_parent_relative_readout.json"
    )).read_text(encoding="utf8"))
    source_counts = frozen["publisher_count_reconstruction"]
    assert source_counts["Evo2D"] == {
        "selected_adaptive_clones": 306,
        "both_fermentation_respiration_positive": 109,
        "stationary_positive_exceeds_deposited_error": 77,
        "stationary_positive_among_both": 7,
        "stationary_positive_among_other": 70,
    }
    assert source_counts["Evo3D"] == {
        "selected_adaptive_clones": 202,
        "both_fermentation_respiration_positive": 25,
        "stationary_positive_exceeds_deposited_error": 160,
        "stationary_positive_among_both": 5,
        "stationary_positive_among_other": 155,
    }
    assert frozen["S1_all_rows"] == 4633
    assert frozen["S1_sources"] == {
        "Aggeli2020": 2459, "Li2019": 442,
        "This_study": 1250, "Venkataram2015": 482,
    }
    source = frozen["source_selection"]["selected_by_source_publication"]
    assert source == {"Aggeli2020": 121, "This_study": 387}
    assert frozen["interpretation_ceiling"]["single_evolved_clone_not_an_independent_evolution_population"]
    assert frozen["interpretation_ceiling"]["no_source_population_id_found_in_deposited_S1_schema"]


def test_matched_genotype_stratification_sign_reversal_not_mutation_origin_rate():
    root = Path(__file__).resolve().parents[1]
    d = json.loads((root / (
        "empirical/trait_architecture_history/"
        "kinsler2024_parent_relative_readout.json"
    )).read_text(encoding="utf8"))
    matched = d["same_new_source_matched_IRA1_parent_sensitivity"]
    m2, m3 = matched["Evo2D"], matched["Evo3D"]
    assert m2["per_background"]["IRA1_MIS"]["selected_clone_rows"] == 90
    assert m2["per_background"]["IRA1_NON"]["selected_clone_rows"] == 95
    assert m3["per_background"]["IRA1_MIS"]["selected_clone_rows"] == 30
    assert m3["per_background"]["IRA1_NON"]["selected_clone_rows"] == 134
    assert m2["equal_two_parent_mean_both_gain_share"] == pytest.approx(0.21725146198830408)
    assert m3["equal_two_parent_mean_both_gain_share"] == pytest.approx(0.22039800995024877)
    assert m2["clone_weighted"]["selected_clone_rows"] == 185
    assert m3["clone_weighted"]["selected_clone_rows"] == 164
