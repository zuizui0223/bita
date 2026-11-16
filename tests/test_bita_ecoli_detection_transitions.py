"""Whole-population transition decomposition tests; no trajectory-cell pseudoreplication."""
import copy
import json
import math
from pathlib import Path

import pytest

from scripts.analyze_bita_ecoli_detection_transitions import (
    ALL_OUTCOMES, SOURCE, PARENT_FROZEN,
    build_readout, trajectory_profile, arm_summary,
    exact_eight_view_max_t,
)

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / (
    "empirical/trait_architecture_history/"
    "dsouza2016_aa_auxotrophy_transition_audit.json"
)


def original():
    return json.loads(SOURCE.read_text(encoding="utf8"))


def parent():
    return json.loads(PARENT_FROZEN.read_text(encoding="utf8"))


def test_all_positive_figure_cells_partition_by_parent_sampling_state():
    d = build_readout(original(), parent())
    assert d["independent_evolved_populations"] == 16
    assert d["original_figure_binary_cells_not_independent_trials"] == 96
    a = d["arm_aggregates"]["AA_present"]
    b = d["arm_aggregates"]["AA_absent"]
    assert a["biological_populations"] == b["biological_populations"] == 8
    assert a["observed_time_intervals"] == b["observed_time_intervals"] == 40
    assert {x: a["counts"][x] for x in ("0_to_0", "0_to_1", "1_to_0", "1_to_1")} == {
        "0_to_0": 24, "0_to_1": 10, "1_to_0": 4, "1_to_1": 2}
    assert {x: b["counts"][x] for x in ("0_to_0", "0_to_1", "1_to_0", "1_to_1")} == {
        "0_to_0": 34, "0_to_1": 3, "1_to_0": 3, "1_to_1": 0}
    for arm in (a, b):
        q = arm["counts"]
        assert q["0_to_1"] + q["1_to_1"] == q["positive_inspections"]
        assert q["0_to_1"] == sum(q["zero_to_one_decomposition"].values())
        assert len(arm["per_population"]) == 8


def test_first_vs_redetection_vs_successive_positive_lineage():
    d = build_readout(original(), parent())["arm_aggregates"]
    a = d["AA_present"]["counts"]
    b = d["AA_absent"]["counts"]
    assert (a["first_detection_population_count"], a["redetections_after_observed_gap"]) == (7, 3)
    assert (b["first_detection_population_count"], b["redetections_after_observed_gap"]) == (3, 0)
    assert a["repeated_positive_inspections"] == 4 and b["repeated_positive_inspections"] == 0
    assert a["populations_with_adjacent_positive_inspections"] == 1
    assert b["populations_with_adjacent_positive_inspections"] == 0
    aa = d["AA_present"]["per_population"]
    successive = [p["population_id"] for p in aa if p["adjacent_positive_transition_count"]]
    assert successive == ["R3"]
    assert aa[2]["adjacent_positive_transition_count"] == 2
    assert {p["population_id"] for p in aa if p["redetections_after_observed_gap"]} == {
        "R2", "R4", "R8"
    }
    assert (a["present_at_final"], b["present_at_final"]) == (6, 0)


def test_exact_whole_history_permutation_new_views():
    d = build_readout(original(), parent())
    tests = d["four_new_exploratory_population_exact_tests"]
    expected = {
        "zero_to_one": (0.875, 504),
        "one_to_one": (0.25, 12870),
        "one_to_zero": (0.125, 12870),
        "repeat_detected_population": (0.5, 990),
    }
    for name, (delta, count) in expected.items():
        q = tests[name]
        assert len(q["AA_population_scores"]) == 8
        assert len(q["nonAA_population_scores"]) == 8
        assert q["difference_in_mean_population_scores"] == pytest.approx(delta)
        assert q["extreme_label_partitions"] == count
        assert q["all_label_partitions"] == math.comb(16, 8) == 12870
        assert q["two_sided_exact_label_permutation_p"] == pytest.approx(count / 12870)


def test_expand_four_to_eight_view_adjustment_is_inference_limiting():
    d = build_readout(original(), parent())
    q = d["eight_view_multiplicity_sensitivity"]
    assert q["labels"] == list(ALL_OUTCOMES)
    assert q["all_label_partitions"] == 12870
    assert q["not_prospective_confirmatory"] is True
    assert q["family_selected_after_inspecting_source"] is True
    expected_extremes = (786, 264, 3100, 180, 858, 12870, 12870, 1548)
    for name, count in zip(ALL_OUTCOMES, expected_extremes):
        assert q["adjusted_extreme_partitions"][name] == count
        assert q["adjusted_p_for_only_the_eight_displayed_views"][name] == pytest.approx(count / 12870)
    assert q["adjusted_p_for_only_the_eight_displayed_views"]["sampled_detected_count"] > 0.05
    assert q["adjusted_p_for_only_the_eight_displayed_views"]["zero_to_one"] > 0.05
    assert q["adjusted_p_for_only_the_eight_displayed_views"]["late_detected_count"] < 0.05
    assert q["adjusted_p_for_only_the_eight_displayed_views"]["final_detected"] < 0.05


def test_uneven_timepoints_and_source_identity_discrepancy_are_visible():
    d = build_readout(original(), parent())
    assert [x["elapsed_generations"] for x in d["interval_aggregates"]] == [250, 250, 500, 500, 500]
    q = d["R2_R3_source_discrepancy"]
    assert q["figure"] == "non-AA R2 at generation 500"
    assert q["article_prose"] == "non-AA R3 at generation 500"
    assert q["unresolved"] is True
    assert q["aggregate_transition_counts_unchanged_by_label_swap"] is True
    assert q["eight_view_extreme_partition_counts_unchanged"] is True
    assert all(d["interpretation_limits"].values())


def test_full_source_roundtrip_and_frozen_output():
    assert build_readout(original(), parent()) == json.loads(FROZEN.read_text(encoding="utf8"))


def test_fails_closed_if_parent_source_or_data_changed():
    source = original()
    source["figure_cells"][0]["detectable_auxotrophic_colony"] = 3
    with pytest.raises(ValueError):
        build_readout(source, parent())
    source = original()
    source["figure_cells"].pop()
    with pytest.raises(ValueError):
        build_readout(source, parent())
    bad_parent = parent()
    bad_parent["four_view_multiplicity_sensitivity"]["all_label_partitions"] = 96
    with pytest.raises(ValueError, match="parent trajectory"):
        build_readout(original(), bad_parent)
    with pytest.raises(ValueError, match="six binary"):
        trajectory_profile([0, 1])
