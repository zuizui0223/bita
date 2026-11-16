"""Transition decomposition of a publisher-verified binary evolution figure.

All inferences are exploratory, source-post-open, single experiment only.
The data are repeated observations on 16 evolving populations, NOT 96
independent trials and NOT 1,000 independent evolution lineages per assay.

A 0->1 transition is a *change in detectable status* between sampled
generations, never proof of a de novo mutation or lineage birth.
"""
from __future__ import annotations

import argparse
import copy
import itertools
import json
import math
from pathlib import Path

from scripts.analyze_bita_ecoli_trajectory_sensitivity import (
    SOURCE,
    GENERATIONS,
    extract_trajectories,
    exact_population_permutation,
    build_readout as parent_build_readout,
    score as parent_score,
)

ROOT = Path(__file__).resolve().parents[1]
PARENT_FROZEN = ROOT / (
    "empirical/trait_architecture_history/"
    "dsouza2016_aa_auxotrophy_trajectory_sensitivity.json"
)

OLD_OUTCOMES = (
    "sampled_detected_count",
    "late_detected_count",
    "ever_detected",
    "final_detected",
)
NEW_OUTCOMES = (
    "zero_to_one",
    "one_to_one",
    "one_to_zero",
    "repeat_detected_population",
)
ALL_OUTCOMES = OLD_OUTCOMES + NEW_OUTCOMES
TREATMENTS = ("AA_present", "AA_absent")
TRANSITIONS = ("0_to_0", "0_to_1", "1_to_0", "1_to_1")


def trajectory_profile(states: list[int]) -> dict:
    if len(states) != len(GENERATIONS) or any(type(s) is not int or s not in (0, 1) for s in states):
        raise ValueError("expected six binary observations from one evolved population")
    trans = {name: 0 for name in TRANSITIONS}
    for from_state, to_state in zip(states[:-1], states[1:]):
        trans[f"{from_state}_to_{to_state}"] += 1
    assert sum(trans.values()) == 5

    positives = [i for i, s in enumerate(states) if s]
    first_idx = positives[0] if positives else None
    first_events = 1 if first_idx is not None else 0
    reappearances = 0
    if first_idx is not None:
        for i in range(first_idx + 1, len(states)):
            if states[i] == 1 and states[i - 1] == 0:
                reappearances += 1

    positive_observations = len(positives)
    if trans["0_to_1"] != first_events + reappearances:
        raise ValueError("transitions are inconsistent with first detections plus re-detections")
    if trans["0_to_1"] + trans["1_to_1"] != positive_observations:
        # At generation 0 the source figure has no positive populations.
        raise ValueError("positive inspections were not fully explained by adjacent transitions")
    return {
        "transition_counts": trans,
        "first_detected_generation": (
            GENERATIONS[first_idx] if first_idx is not None else None
        ),
        "positive_inspections": positive_observations,
        "ever_detected": int(first_idx is not None),
        "repeated_positive_inspections": int(positive_observations >= 2),
        "adjacent_positive_transition_count": trans["1_to_1"],
        "redetections_after_observed_gap": reappearances,
        "present_at_final": states[-1],
    }


def arm_summary(tracks: dict) -> dict:
    if set(tracks) != set(TREATMENTS) or any(len(tracks[arm]) != 8 for arm in TREATMENTS):
        raise ValueError("expected exactly two eight-population arms")
    summaries = {}
    for arm in TREATMENTS:
        profiles = [trajectory_profile(x) for x in tracks[arm]]
        sums = {
            k: sum(p["transition_counts"][k] for p in profiles)
            for k in TRANSITIONS
        }
        if sum(sums.values()) != 40:
            raise ValueError("one arm must have exactly 8x5 observed transitions")
        namekeys = ("positive_inspections", "ever_detected", "repeated_positive_inspections",
                    "adjacent_positive_transition_count", "redetections_after_observed_gap",
                    "present_at_final")
        sums.update({k: sum(p[k] for p in profiles) for k in namekeys})
        sums["first_detection_population_count"] = sum(p["first_detected_generation"] is not None for p in profiles)
        sums["zero_to_one_decomposition"] = {
            "first_detected_across_observed_histories": sums["first_detection_population_count"],
            "later_redetections_after_observed_gap": sums["redetections_after_observed_gap"],
        }
        if sums["0_to_1"] != sum(sums["zero_to_one_decomposition"].values()):
            raise ValueError("arm zero-to-one decomposition must close exactly")
        summaries[arm] = {
            "biological_populations": 8,
            "observed_time_intervals": 40,
            "counts": sums,
            "per_population": [
                {"population_id": f"R{i+1}", **p} for i, p in enumerate(profiles)
            ],
        }
    return summaries


def eight_view_score(states: list[int], outcome: str) -> int:
    if outcome in OLD_OUTCOMES:
        return parent_score(states, outcome)
    p = trajectory_profile(states)
    if outcome == "zero_to_one":
        return p["transition_counts"]["0_to_1"]
    if outcome == "one_to_one":
        return p["transition_counts"]["1_to_1"]
    if outcome == "one_to_zero":
        return p["transition_counts"]["1_to_0"]
    if outcome == "repeat_detected_population":
        return p["repeated_positive_inspections"]
    raise ValueError(f"unknown predeclared outcome {outcome}")


def exact_eight_view_max_t(tracks: dict) -> dict:
    """12,870 full-history label allocations, no timepoint pseudoreplication.

    Finite-population standardized absolute contrast; the same permutations
    are used for all 8 statistics. Valid as a conditional sensitivity over
    the eight *displayed*, post-source-selected summaries only.
    """
    original = tracks["AA_present"] + tracks["AA_absent"]
    if len(original) != 16:
        raise ValueError("all 16 original evolving populations required")
    mat = [[eight_view_score(x, name) for name in ALL_OUTCOMES] for x in original]
    k = len(ALL_OUTCOMES)
    totals = [sum(row[j] for row in mat) for j in range(k)]
    mu = [x / 16 for x in totals]
    sd = [
        math.sqrt((1/8 + 1/8) * sum((row[j] - mu[j]) ** 2 for row in mat) / 15)
        for j in range(k)
    ]
    if any(s <= 0 for s in sd):
        raise ValueError("zero-variance contrast not valid for 8-view maxT")
    observed = [
        (sum(row[j] for row in mat[:8]) / 8) -
        (sum(row[j] for row in mat[8:]) / 8)
        for j in range(k)
    ]
    obs_abs_z = [abs(d) / s for d, s in zip(observed, sd)]
    extreme = [0] * k
    n = 0
    for combination in itertools.combinations(range(16), 8):
        sums = [sum(mat[i][j] for i in combination) for j in range(k)]
        differences = [sums[j]/8 - (totals[j] - sums[j])/8 for j in range(k)]
        zmax = max(abs(d)/s for d, s in zip(differences, sd))
        n += 1
        for j in range(k):
            if zmax >= obs_abs_z[j] - 1e-12:
                extreme[j] += 1
    if n != math.comb(16, 8) or n != 12870:
        raise ValueError("incomplete whole-population permutation enumeration")
    return {
        "labels": list(ALL_OUTCOMES),
        "method": "eight_post_source_view_max_absolute_permutation_z",
        "all_label_partitions": n,
        "observed_between_arm_mean_differences": dict(zip(ALL_OUTCOMES, observed)),
        "finite_population_permutation_sd": dict(zip(ALL_OUTCOMES, sd)),
        "observed_abs_standardized_differences": dict(zip(ALL_OUTCOMES, obs_abs_z)),
        "adjusted_extreme_partitions": dict(zip(ALL_OUTCOMES, extreme)),
        "adjusted_p_for_only_the_eight_displayed_views": dict(zip(ALL_OUTCOMES, [v/n for v in extreme])),
        "not_prospective_confirmatory": True,
        "family_selected_after_inspecting_source": True,
        "whole_population_trajectories_not_individual_cells_are_reallocated": True,
    }


def interval_summary(tracks: dict) -> list[dict]:
    out = []
    for j in range(1, len(GENERATIONS)):
        armintervals = {}
        for arm in TREATMENTS:
            q = {name: 0 for name in TRANSITIONS}
            for states in tracks[arm]:
                q[f"{states[j-1]}_to_{states[j]}"] += 1
            if sum(q.values()) != 8:
                raise ValueError("each arm/time interval must contain 8 population transitions")
            armintervals[arm] = q
        out.append({
            "from_generation": GENERATIONS[j-1],
            "to_generation": GENERATIONS[j],
            "elapsed_generations": GENERATIONS[j] - GENERATIONS[j-1],
            "per_arm_transitions": armintervals,
        })
    return out


def build_readout(source: dict, frozen_parent: dict) -> dict:
    tracks = extract_trajectories(source)
    recomputed_parent = parent_build_readout(source)
    if recomputed_parent != frozen_parent:
        raise ValueError("parent trajectory source / frozen result changed")
    arms = arm_summary(tracks)
    already_frozen = frozen_parent["outcomes"]
    for outcome in OLD_OUTCOMES:
        s = [eight_view_score(x, outcome) for x in tracks["AA_present"]]
        t = [eight_view_score(x, outcome) for x in tracks["AA_absent"]]
        if exact_population_permutation(s, t)["two_sided_exact_label_permutation_p"] != already_frozen[outcome]["two_sided_exact_label_permutation_p"]:
            raise ValueError("incompatible parent exact p")
    max_t = exact_eight_view_max_t(tracks)

    # The Figure 2 non-AA R2 versus article prose R3 at generation 500
    # is an unresolved ID discrepancy, not a hidden error correction.
    other = copy.deepcopy(tracks)
    if other["AA_absent"][1][2] != 1 or other["AA_absent"][2][2] != 0:
        raise ValueError("published source figure R2/R3 anomaly unexpectedly changed")
    other["AA_absent"][1][2] = 0
    other["AA_absent"][2][2] = 1
    alternate_counts = arm_summary(other)
    for arm in TREATMENTS:
        if alternate_counts[arm]["counts"] != arms[arm]["counts"]:
            raise ValueError("aggregate transition counts unexpectedly depend on R2/R3 disagreement")
    alt_max_t = exact_eight_view_max_t(other)
    if max_t["adjusted_extreme_partitions"] != alt_max_t["adjusted_extreme_partitions"]:
        raise ValueError("8-view exact statistics changed under source label reassignment")

    by_arm = {arm: arms[arm]["counts"] for arm in TREATMENTS}
    if by_arm["AA_present"]["0_to_1"] != 10 or by_arm["AA_absent"]["0_to_1"] != 3:
        raise ValueError("published source 0->1 totals changed")
    if by_arm["AA_present"]["1_to_1"] != 2 or by_arm["AA_absent"]["1_to_1"] != 0:
        raise ValueError("published source consecutive positive counts changed")
    if by_arm["AA_present"]["positive_inspections"] != 12 or by_arm["AA_absent"]["positive_inspections"] != 3:
        raise ValueError("published total positive cell count changed")

    new_exact = {}
    for name in NEW_OUTCOMES:
        a = [eight_view_score(x, name) for x in tracks["AA_present"]]
        b = [eight_view_score(x, name) for x in tracks["AA_absent"]]
        new_exact[name] = {
            "AA_population_scores": a,
            "nonAA_population_scores": b,
            **exact_population_permutation(a, b),
        }
    return {
        "source_doi": source["doi"],
        "frozen_original_publisher_figure_sha256": source["source_fig2_sha256"],
        "parent_source": "PR #376 original Figure 2, PR #377 source-validated exact 4-view analysis",
        "independent_evolved_populations": 16,
        "original_figure_binary_cells_not_independent_trials": 96,
        "arm_aggregates": arms,
        "interval_aggregates": interval_summary(tracks),
        "four_new_exploratory_population_exact_tests": new_exact,
        "eight_view_multiplicity_sensitivity": max_t,
        "R2_R3_source_discrepancy": {
            "figure": "non-AA R2 at generation 500",
            "article_prose": "non-AA R3 at generation 500",
            "unresolved": True,
            "aggregate_transition_counts_unchanged_by_label_swap": True,
            "eight_view_extreme_partition_counts_unchanged": True,
        },
        "interpretation_limits": {
            "first_detection_is_not_de_novo_mutation_origin": True,
            "re_detection_after_zero_is_not_new_mutation_or_true_regain": True,
            "adjacent_positive_assays_are_not_genotype_identity_or_fixation": True,
            "zero_assay_is_not_mutation_absence_or_true_extinction": True,
            "unequal_interval_lengths_preclude_per_generation_hazard_interpretation": True,
            "nested_observations_and_8_lineages_per_arm": True,
            "evolved_population_not_screened_colony_is_inferential_unit": True,
            "eight_view_max_t_is_post_source_not_prospective": True,
            "not_a_new_independent_study_or_meta_analysis": True,
            "no_identified_genetic_origins_or_2_function_division_of_labour": True,
        },
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source", type=Path, default=SOURCE)
    p.add_argument("--parent", type=Path, default=PARENT_FROZEN)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    readout = build_readout(
        json.loads(args.source.read_text(encoding="utf8")),
        json.loads(args.parent.read_text(encoding="utf8")),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(readout, ensure_ascii=False, indent=2, allow_nan=False)+"\n", encoding="utf8")
    print("BITA_ECOLI_TRANSITION_AUDIT:" + json.dumps({
        "counts": {k: v["counts"] for k, v in readout["arm_aggregates"].items()},
        "maxT8_p": readout["eight_view_multiplicity_sensitivity"]["adjusted_p_for_only_the_eight_displayed_views"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
