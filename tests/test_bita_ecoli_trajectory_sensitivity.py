"""Source-frozen independent population and exact label enumeration contracts."""
import copy
import json
import math
from pathlib import Path
import pytest

from scripts.analyze_bita_ecoli_trajectory_sensitivity import (
    SOURCE, GENERATIONS, build_readout, exact_population_permutation,
    extract_trajectories,
)

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "empirical/trait_architecture_history/dsouza2016_aa_auxotrophy_trajectory_sensitivity.json"


def source():
    return json.loads(SOURCE.read_text(encoding="utf8"))


def test_full_96_source_cells_are_16_population_trajectories():
    tracks = extract_trajectories(source())
    assert list(tracks) == ["AA_present", "AA_absent"]
    assert len(tracks["AA_present"]) == len(tracks["AA_absent"]) == 8
    assert all(len(t) == len(GENERATIONS) for arm in tracks.values() for t in arm)
    assert ["".join(map(str, t)) for t in tracks["AA_present"]] == [
        "000010", "000101", "000111", "000101",
        "000001", "000001", "000000", "000101",
    ]
    assert ["".join(map(str, t)) for t in tracks["AA_absent"]] == [
        "000000", "001000", "000000", "000000",
        "000000", "000000", "000010", "000010",
    ]


def test_exact_permutations_are_whole_evolutionary_populations():
    src = source()
    d = build_readout(src)
    assert d["independent_population_count"] == 16
    assert d["repeated_population_time_cells"] == 96
    assert d["positive_population_counts_by_generation"] == {
        "0": {"AA_present": 0, "AA_absent": 0},
        "250": {"AA_present": 0, "AA_absent": 0},
        "500": {"AA_present": 0, "AA_absent": 1},
        "1000": {"AA_present": 4, "AA_absent": 0},
        "1500": {"AA_present": 2, "AA_absent": 2},
        "2000": {"AA_present": 6, "AA_absent": 0},
    }
    expected = {
        "sampled_detected_count": (12, 3, 1.125, 306),
        "late_detected_count": (12, 2, 1.25, 156),
        "ever_detected": (7, 3, .5, 1530),
        "final_detected": (6, 0, .75, 90),
    }
    for name, (aa, na, delta, numerator) in expected.items():
        observed = d["outcomes"][name]
        assert observed["AA_present_sum"] == aa
        assert observed["AA_absent_sum"] == na
        assert observed["difference_in_mean_population_scores"] == pytest.approx(delta)
        assert observed["extreme_label_partitions"] == numerator
        assert observed["all_label_partitions"] == math.comb(16, 8) == 12870
        assert observed["two_sided_exact_label_permutation_p"] == pytest.approx(numerator / 12870)


def test_source_label_disagreement_is_not_hidden_or_falsely_resolved():
    d = build_readout(source())
    x = d["source_500_generation_label_discrepancy"]
    assert x["unresolved"] is True
    assert x["figure"] == "nonAA R2"
    assert x["original_results_prose"] == "nonAA R3"
    assert all(x["alternate_assignment_leaves_all_exact_tests_unchanged"].values())



def test_four_view_joint_max_t_is_from_the_same_12870_population_label_partitions():
    d = build_readout(source())["four_view_multiplicity_sensitivity"]
    assert d["method"] == "max_abs_population_permutation_z_four_displayed_outcomes"
    assert d["prospective_confirmatory_family"] is False
    assert d["whole_populations_relabelled"] is True
    assert d["all_label_partitions"] == 12870
    names = ("sampled_detected_count", "late_detected_count", "ever_detected", "final_detected")
    assert d["outcome_names"] == list(names)
    for name, count in zip(names, (360, 252, 2610, 168)):
        assert d["familywise_extreme_partitions"][name] == count
        assert d["four_view_max_t_adjusted_p"][name] == pytest.approx(count / 12870)
    assert d["observed_abs_standardized_difference"]["final_detected"] == pytest.approx(3.0)


def test_one_evolution_population_dropout_not_cell_dropout():
    x = build_readout(source())["leave_one_population_out_sampled_count"]
    assert x["refits"] == 16
    assert x["all_effects_positive"] is True
    assert x["min_mean_score_difference"] == pytest.approx(.9107142857142858)
    assert x["max_mean_score_difference"] == pytest.approx(1.3392857142857142)
    assert x["min_two_sided_p"] == pytest.approx(.005439005439005439)
    assert x["max_two_sided_p"] == pytest.approx(.04242424242424243)


def test_frozen_readout_matches_independent_stdlib_recomputation():
    actual = build_readout(source())
    frozen = json.loads(FROZEN.read_text(encoding="utf8"))
    assert actual == frozen
    flags = actual["inference_scope"]
    assert flags["meta_analysis_performed"] is False
    assert flags["four_reported_outcomes_max_t_adjusted"] is True
    assert flags["reported_outcome_family_selected_post_source"] is True
    assert all(v is True for k, v in flags.items() if k != "meta_analysis_performed")


def test_invalid_source_units_and_mutated_sha_fail_closed():
    d = source()
    d["source_fig2_sha256"] = "invalid"
    with pytest.raises(ValueError, match="provenance"):
        extract_trajectories(d)
    d = source()
    d["figure_cells"][1]["detectable_auxotrophic_colony"] = 1
    with pytest.raises(ValueError, match="boolean"):
        extract_trajectories(d)
    d = source()
    d["figure_cells"][1] = copy.deepcopy(d["figure_cells"][0])
    with pytest.raises(ValueError, match="duplicate"):
        extract_trajectories(d)


def test_exact_partition_enumerator_small_sanity():
    p = exact_population_permutation([1, 1], [0, 0])
    assert p["all_label_partitions"] == 6
    assert p["extreme_label_partitions"] == 2
    assert p["two_sided_exact_label_permutation_p"] == pytest.approx(1 / 3)
    with pytest.raises(ValueError):
        exact_population_permutation([1, 2], [-1, 0])
