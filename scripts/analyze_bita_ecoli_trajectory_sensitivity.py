"""Population-grain exact sensitivity for D'Souza & Kost (2016) Figure 2.

Reuses the SHA-verified categorical figure readout from PR #376. The 96
population-time observations are repeated assays of just 16 populations.
Every exact permutation reallocates *whole population trajectories*, never
individual heatmap cells or plated colonies. All outcomes are exploratory.
"""
from __future__ import annotations

import argparse
import copy
import itertools
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "empirical/trait_architecture_history/dsouza2016_aa_auxotrophy_fig2_readout.json"
ARMS = ("AA_present", "AA_absent")
GENERATIONS = (0, 250, 500, 1000, 1500, 2000)
POPULATIONS = tuple(f"R{i}" for i in range(1, 9))
SOURCE_FIG_SHA = "71da8f3c1707d1ade887d4030446d1869f9fd33b05fa8cfed6fb3cd49823bd8b"


def extract_trajectories(source: dict) -> dict[str, list[list[int]]]:
    """Fail closed on figure provenance, unit, duplicate, and coverage errors."""
    if source.get("doi") != "10.1371/journal.pgen.1006364":
        raise ValueError("unexpected article DOI")
    if source.get("source_fig2_sha256") != SOURCE_FIG_SHA:
        raise ValueError("source figure provenance changed")
    if source.get("source_grade") != (
        "ORIGINAL_PUBLISHER_FIG2_BINARY_HEATMAP_NOT_RAW_COLONY_FREQUENCIES"
    ):
        raise ValueError("binary figure source grade required")
    design = source["source_validation"]["source_design"]
    if design["total_evolved_populations"] != 16 or design["independent_populations_per_regime"] != 8:
        raise ValueError("independent evolution populations changed")
    if tuple(design["generation_samples"]) != GENERATIONS:
        raise ValueError("sampled generation schedule changed")
    if len(source["figure_cells"]) != 96:
        raise ValueError("expected 96 original-source figure cells")

    indexed = {}
    for row in source["figure_cells"]:
        key = (row.get("condition"), row.get("population_id"), row.get("generation"))
        if key[0] not in ARMS or key[1] not in POPULATIONS or key[2] not in GENERATIONS:
            raise ValueError("unknown treatment, population, or generation")
        if key in indexed:
            raise ValueError("duplicate population-generation observation")
        state = row.get("detectable_auxotrophic_colony")
        if type(state) is not bool:
            raise ValueError("original source must provide boolean detection, not frequency")
        if row.get("derived_from") != "original_published_heatmap_color_not_raw_colony_count":
            raise ValueError("source cell provenance missing")
        indexed[key] = int(state)

    expected = {(arm, p, g) for arm in ARMS for p in POPULATIONS for g in GENERATIONS}
    if set(indexed) != expected:
        raise ValueError("missing source population-generation observations")
    return {
        arm: [[indexed[(arm, p, g)] for g in GENERATIONS] for p in POPULATIONS]
        for arm in ARMS
    }


def exact_population_permutation(aa: list[int], noaa: list[int]) -> dict:
    """Enumerate all fixed-size label partitions; preserve population dependence."""
    if min(len(aa), len(noaa)) < 2:
        raise ValueError("need independent biological populations in each arm")
    if any(type(v) is not int or v < 0 for v in aa + noaa):
        raise ValueError("count outcomes must be nonnegative integers")
    all_values = aa + noaa
    n_aa, n_no = len(aa), len(noaa)
    total = sum(all_values)
    observed = sum(aa) / n_aa - sum(noaa) / n_no
    extreme = 0
    assignments = 0
    for subset in itertools.combinations(range(len(all_values)), n_aa):
        aa_sum = sum(all_values[i] for i in subset)
        alternative = aa_sum / n_aa - (total - aa_sum) / n_no
        assignments += 1
        if abs(alternative) >= abs(observed) - 1e-12:
            extreme += 1
    if assignments != math.comb(n_aa + n_no, n_aa):
        raise ValueError("incomplete exact enumeration")
    return {
        "difference_in_mean_population_scores": observed,
        "two_sided_exact_label_permutation_p": extreme / assignments,
        "extreme_label_partitions": extreme,
        "all_label_partitions": assignments,
    }


def score(trajectory: list[int], outcome: str) -> int:
    if outcome == "sampled_detected_count":
        # Generation 0 and 250 are both structurally zero in the source.
        # This is an *equal-sampled-timepoint* count, NOT a calendar-time AUC.
        return sum(trajectory)
    if outcome == "late_detected_count":
        return sum(trajectory[3:])  # 1000, 1500, 2000 generations only
    if outcome == "ever_detected":
        return int(any(trajectory))
    if outcome == "final_detected":
        return trajectory[-1]
    raise ValueError("unknown population-level outcome")


def analyze_outcome(tracks: dict, outcome: str) -> dict:
    aa = [score(x, outcome) for x in tracks["AA_present"]]
    noaa = [score(x, outcome) for x in tracks["AA_absent"]]
    test = exact_population_permutation(aa, noaa)
    return {
        "AA_present_population_scores": aa,
        "AA_absent_population_scores": noaa,
        "AA_present_sum": sum(aa),
        "AA_absent_sum": sum(noaa),
        "AA_present_mean": sum(aa) / len(aa),
        "AA_absent_mean": sum(noaa) / len(noaa),
        **test,
    }



def exact_four_outcome_max_t(tracks: dict, outcome_names: tuple[str, ...]) -> dict:
    """Joint whole-population max-|T| calibration for the four *reported* views.

    Exact exhaustive permutations and finite-population standardization make
    the four outcomes comparable without assuming independent timepoints.
    This corrects only the displayed outcome family; selection of the family
    occurred after reading the paper and is NOT prospective confirmatory FWER.
    """
    histories = tracks["AA_present"] + tracks["AA_absent"]
    if len(histories) != 16:
        raise ValueError("joint permutation requires the original 16 populations")
    values = [[score(t, name) for name in outcome_names] for t in histories]
    k = len(outcome_names)
    if k != 4:
        raise ValueError("freeze exactly the four reported outcome choices")
    total = [sum(row[j] for row in values) for j in range(k)]
    mean = [s / 16 for s in total]
    # Finite-population random partition variance of a difference in means
    # with 8 of 16 whole-population observations in each treatment arm.
    sd = [
        math.sqrt(
            sum((row[j] - mean[j]) ** 2 for row in values) / 15 * (1 / 8 + 1 / 8)
        )
        for j in range(k)
    ]
    if any(v <= 0 for v in sd):
        raise ValueError("maxT needs positive permutation variance for each view")
    observed_delta = [
        sum(values[i][j] for i in range(8)) / 8
        - sum(values[i][j] for i in range(8, 16)) / 8
        for j in range(k)
    ]
    observed_z = [abs(x) / s for x, s in zip(observed_delta, sd)]
    exceed = [0] * k
    n_assignments = 0
    for subset in itertools.combinations(range(16), 8):
        assigned = [sum(values[i][j] for i in subset) for j in range(k)]
        diffs = [assigned[j] / 8 - (total[j] - assigned[j]) / 8 for j in range(k)]
        permuted_max = max(abs(d) / s for d, s in zip(diffs, sd))
        for j in range(k):
            if permuted_max >= observed_z[j] - 1e-12:
                exceed[j] += 1
        n_assignments += 1
    if n_assignments != 12870:
        raise ValueError("incomplete joint exact label enumeration")
    return {
        "method": "max_abs_population_permutation_z_four_displayed_outcomes",
        "prospective_confirmatory_family": False,
        "whole_populations_relabelled": True,
        "outcome_names": list(outcome_names),
        "null_permutation_sd_of_difference": dict(zip(outcome_names, sd)),
        "observed_abs_standardized_difference": dict(zip(outcome_names, observed_z)),
        "familywise_extreme_partitions": dict(zip(outcome_names, exceed)),
        "all_label_partitions": n_assignments,
        "four_view_max_t_adjusted_p": dict(zip(
            outcome_names, [v / n_assignments for v in exceed]
        )),
    }


def build_readout(source: dict) -> dict:
    tracks = extract_trajectories(source)
    outcome_names = ("sampled_detected_count", "late_detected_count", "ever_detected", "final_detected")
    outcomes = {name: analyze_outcome(tracks, name) for name in outcome_names}
    max_t = exact_four_outcome_max_t(tracks, outcome_names)
    # Parent's exact two-arm endpoint computation must agree with an
    # independent whole-population permutation of the source line histories.
    parent = source["primary_endpoint"]
    if (parent["aa_positive_populations"], parent["nonAA_positive_populations"]) != (6, 0):
        raise ValueError("parent source endpoint changed")
    if abs(outcomes["final_detected"]["two_sided_exact_label_permutation_p"] - parent["two_sided_fisher_exact_p"]) > 1e-12:
        raise ValueError("source parent endpoint/Fisher mismatch")

    # Robustness to disputed 500-generation non-AA R2 (figure) vs R3 (prose)
    # identity: transfer that single detection to R3 as an *alternative*,
    # without endorsing either conflicting source identity.
    nonaa_r2_500 = tracks["AA_absent"][1][2]
    nonaa_r3_500 = tracks["AA_absent"][2][2]
    if (nonaa_r2_500, nonaa_r3_500) != (1, 0):
        raise ValueError("expected R2/R3 source figure ambiguity not present")
    alternate = copy.deepcopy(tracks)
    alternate["AA_absent"][1][2] = 0
    alternate["AA_absent"][2][2] = 1
    alt_identical = {
        name: exact_population_permutation(
            [score(t, name) for t in alternate["AA_present"]],
            [score(t, name) for t in alternate["AA_absent"]],
        ) == {
            key: original[key]
            for key in (
                "difference_in_mean_population_scores", "two_sided_exact_label_permutation_p",
                "extreme_label_partitions", "all_label_partitions"
            )
        }
        for name, original in outcomes.items()
    }
    if not all(alt_identical.values()):
        raise ValueError("source-label swap unexpectedly changes grouped inference")

    whole = "sampled_detected_count"
    looo = [
        exact_population_permutation(
            [score(t, whole) for j, t in enumerate(tracks["AA_present"]) if j != i] if arm == "AA_present"
                else [score(t, whole) for t in tracks["AA_present"]],
            [score(t, whole) for j, t in enumerate(tracks["AA_absent"]) if j != i] if arm == "AA_absent"
                else [score(t, whole) for t in tracks["AA_absent"]],
        )
        for arm in ARMS for i in range(8)
    ]
    by_gen = {
        str(g): {
            arm: sum(t[i] for t in tracks[arm])
            for arm in ARMS
        }
        for i, g in enumerate(GENERATIONS)
    }
    return {
        "source_doi": source["doi"],
        "frozen_publisher_figure_sha256": SOURCE_FIG_SHA,
        "source": "parent PR #376 frozen 96-cell categorical heatmap, not individual CFU counts",
        "independent_population_count": 16,
        "population_count_per_arm": 8,
        "repeated_population_time_cells": 96,
        "sampled_generations": list(GENERATIONS),
        "positive_population_counts_by_generation": by_gen,
        "outcomes": outcomes,
        "four_view_multiplicity_sensitivity": max_t,
        "source_500_generation_label_discrepancy": {
            "figure": "nonAA R2", "original_results_prose": "nonAA R3",
            "unresolved": True, "alternate_assignment_leaves_all_exact_tests_unchanged": alt_identical
        },
        "leave_one_population_out_sampled_count": {
            "refits": len(looo),
            "min_mean_score_difference": min(x["difference_in_mean_population_scores"] for x in looo),
            "max_mean_score_difference": max(x["difference_in_mean_population_scores"] for x in looo),
            "min_two_sided_p": min(x["two_sided_exact_label_permutation_p"] for x in looo),
            "max_two_sided_p": max(x["two_sided_exact_label_permutation_p"] for x in looo),
            "all_effects_positive": all(x["difference_in_mean_population_scores"] > 0 for x in looo),
        },
        "inference_scope": {
            "all_outcomes_exploratory_post_source": True,
            "four_reported_outcomes_max_t_adjusted": True,
            "reported_outcome_family_selected_post_source": True,
            "whole_trajectory_labels_permuted_not_96_cells": True,
            "permutation_exchangeability_assumption_required": True,
            "sampled_detection_count_not_duration_or_true_auxotroph_frequency": True,
            "raw_workbook_unavailable_no_colony_frequency_estimated": True,
            "non_detection_not_absence_of_mutation": True,
            "function_loss_not_reciprocal_division_of_labour": True,
            "mutation_supply_and_selection_not_separately_identified": True,
            "meta_analysis_performed": False,
        },
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, default=SOURCE)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    result = build_readout(json.loads(args.input.read_text(encoding="utf8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf8")
    print("BITA_ECOLI_TRAJECTORY_EXACT:" + json.dumps({
        name: {
            "difference": obj["difference_in_mean_population_scores"],
            "p": obj["two_sided_exact_label_permutation_p"],
        }
        for name, obj in result["outcomes"].items()
    }, sort_keys=True))


if __name__ == "__main__":
    main()
