"""Descriptive parent-relative multi-function profile from Kinsler 2024 S1.

Biological unit = *selected isolated barcode/clone*, nested within unknown
independent evolving population replicate. This is NOT a test based on 4,633
independent populations, nor an estimate of mutational origin frequencies.

Published-author source is checksum locked by audit_bita_kinsler2024_source.
Uses the authors' deposited relative-to-parent columns, not new parent
subtraction, with source-publication, ancestor, and evolution-stage strata.
"""
from __future__ import annotations

import argparse
import collections
import json
import math
from pathlib import Path

from scripts.audit_bita_kinsler2024_source import audit_files, read_csv

BACKGROUNDS = ("CYR1", "GPB2", "TOR1", "IRA1_MIS", "IRA1_NON")
CONDITIONS = ("Evo2D", "Evo3D")
ADAPTIVE_CLASSES = ("adaptive_haploid", "high_fitness_diploids")
FUNCTIONS = ("FerPerHour_relative", "ResPerHour_relative", "StaPerHour_relative")
EXPECTED_SOURCE_FIELDS = (
    "barcode", "class_new", "ancestor", "evolution_condition",
    "source_publication", *FUNCTIONS,
    "FerPerHour_error", "ResPerHour_error", "StaPerHour_error",
)


def finite_field(row: dict, key: str) -> float | None:
    field = str(row.get(key, "")).strip()
    if field.lower() in {"", "nan", "na", "none", "null"}:
        return None
    try:
        num = float(field)
    except ValueError as exc:
        raise ValueError(f"non-numeric performance field {key}") from exc
    if not math.isfinite(num):
        return None
    return num


def phenotype_quadrant(f: float, r: float) -> str:
    if r > 0 and f > 0:
        return "both_fermentation_and_respiration_improve"
    if r > 0 and f < 0:
        return "respiration_gain_fermentation_cost"
    if r > 0:
        return "respiration_gain_fermentation_zero"
    if f > 0 and r <= 0:
        return "fermentation_gain_respiration_not_positive"
    return "neither_performance_positive"


def summarize_group(rows: list[dict]) -> dict:
    """All numerators are selected-clone description, not evolutionary hits."""
    complete = []
    missing = 0
    for row in rows:
        f = finite_field(row, FUNCTIONS[0])
        r = finite_field(row, FUNCTIONS[1])
        s = finite_field(row, FUNCTIONS[2])
        if f is None or r is None:
            missing += 1
            continue
        ferr = finite_field(row, "FerPerHour_error")
        rerr = finite_field(row, "ResPerHour_error")
        if ferr is not None and ferr < 0 or rerr is not None and rerr < 0:
            raise ValueError("negative original reported error")
        complete.append((f, r, s, ferr, rerr))
    quad = collections.Counter(phenotype_quadrant(f, r) for f, r, _, _, _ in complete)
    n = len(complete)
    if sum(quad.values()) != n:
        raise ValueError("quadrant classification is not exhaustive")
    both = quad["both_fermentation_and_respiration_improve"]
    cost = quad["respiration_gain_fermentation_cost"]
    robust = {
        "available_with_both_reported_phenotype_errors": 0,
        "both_positive_margin_gt_2errors": 0,
        "resp_positive_and_fer_negative_margin_gt_2errors": 0,
        "other_or_uncertain_sign": 0,
    }
    for f, r, s, ferr, rerr in complete:
        if ferr is None or rerr is None:
            continue
        robust["available_with_both_reported_phenotype_errors"] += 1
        if f > 2*ferr and r > 2*rerr:
            robust["both_positive_margin_gt_2errors"] += 1
        elif r > 2*rerr and f < -2*ferr:
            robust["resp_positive_and_fer_negative_margin_gt_2errors"] += 1
        else:
            robust["other_or_uncertain_sign"] += 1
    if sum(robust[k] for k in (
        "both_positive_margin_gt_2errors",
        "resp_positive_and_fer_negative_margin_gt_2errors",
        "other_or_uncertain_sign",
    )) != robust["available_with_both_reported_phenotype_errors"]:
        raise ValueError("error margin categories not exhaustive")
    stationary = {
        "available_stationary_measurements": sum(s is not None for _, _, s, _, _ in complete),
        "stationary_gain_among_both": sum(
            s is not None and s > 0 and f > 0 and r > 0 for f, r, s, _, _ in complete
        ),
        "stationary_gain_among_resp_gain_fer_cost": sum(
            s is not None and s > 0 and f < 0 and r > 0 for f, r, s, _, _ in complete
        ),
        "stationary_nonmissing_among_both": sum(
            s is not None and f > 0 and r > 0 for f, r, s, _, _ in complete
        ),
        "stationary_nonmissing_among_resp_gain_fer_cost": sum(
            s is not None and f < 0 and r > 0 for f, r, s, _, _ in complete
        ),
    }
    return {
        "selected_clone_rows": len(rows),
        "complete_parent_relative_fermentation_respiration": n,
        "missing_parent_relative_either": missing,
        "quadrants": dict(sorted(quad.items())),
        "descriptive_both_gain_share": both / n if n else None,
        "descriptive_resp_gain_fer_cost_share": cost / n if n else None,
        "strict_two_reported_error_margin": robust,
        "stationary_phase": stationary,
        "inferential_unit": "selected_isolated_barcode_nested_under_unrecovered_evolution_replication",
    }


def analyzed_cohorts(rows: list[dict]) -> tuple[list[dict], dict]:
    """Never silently select a sample that contains WT or pure diploids."""
    combos = {}
    all_selected = []
    for row in rows:
        a, env, cl = (row["ancestor"], row["evolution_condition"], row["class_new"])
        if a in BACKGROUNDS and env in CONDITIONS and cl in ADAPTIVE_CLASSES:
            combos.setdefault((a, env, cl), []).append(row)
            all_selected.append(row)
    totals_by_source = collections.Counter(r["source_publication"] for r in all_selected)
    return all_selected, {
        "selected_by_source_publication": dict(sorted(totals_by_source.items())),
        "selected_by_condition_class": {
            f"{env}|{cl}": sum(r["evolution_condition"] == env and r["class_new"] == cl
                            for r in all_selected)
            for env in CONDITIONS for cl in ADAPTIVE_CLASSES
        },
        "selected_by_ancestor_and_condition": {
            f"{a}|{env}": len([r for r in all_selected
                              if r["ancestor"] == a and r["evolution_condition"] == env])
            for a in BACKGROUNDS for env in CONDITIONS
        },
    }


def analyze_original(s1: bytes, s3: bytes) -> dict:
    source_inventory = audit_files(s1, s3)
    headers, rows = read_csv(s1)
    if any(key not in headers for key in EXPECTED_SOURCE_FIELDS):
        raise ValueError("source lacks original deposited parental-relative/uncertainty fields")
    if len(rows) != 4633 or len({r["barcode"] for r in rows}) != 4633:
        raise ValueError("S1 original-row population changed")
    selected, totals = analyzed_cohorts(rows)
    groups = {}
    for env in CONDITIONS:
        for cl in ADAPTIVE_CLASSES:
            subset = [r for r in selected if r["evolution_condition"] == env
                      and r["class_new"] == cl]
            groups[f"{env}|{cl}"] = summarize_group(subset)
    # The publisher's ~35% Evo2D and ~13% Evo3D rounded results
    # correspond to *both* selected adaptive classes (306 and 202 rows),
    # not just the `adaptive_haploid` class in the CSV.
    for env in CONDITIONS:
        subset = [r for r in selected if r["evolution_condition"] == env]
        groups[f"{env}|all_adaptive_classes"] = summarize_group(subset)
    by_parent = {}
    for a in BACKGROUNDS:
        for env in CONDITIONS:
            for cl in ADAPTIVE_CLASSES:
                subset = [r for r in selected if r["ancestor"] == a
                          and r["evolution_condition"] == env
                          and r["class_new"] == cl]
                by_parent[f"{a}|{env}|{cl}"] = summarize_group(subset)
            subset_all = [r for r in selected if r["ancestor"] == a and r["evolution_condition"] == env]
            by_parent[f"{a}|{env}|all_adaptive_classes"] = summarize_group(subset_all)
    by_publication = {}
    for name in sorted({r["source_publication"] for r in selected}):
        for env in CONDITIONS:
            subset = [r for r in selected if r["source_publication"] == name
                      and r["evolution_condition"] == env and
                      r["class_new"] == "adaptive_haploid"]
            by_publication[f"{name}|{env}|adaptive_haploid"] = summarize_group(subset)
    # Independent publication provenance: prior Aggeli second-step clones
    # are mixed into the same author S1 aggregate as This_study. Preserve
    # all selected adaptive classes, and never count prior work as new 2024.
    for name in sorted({r["source_publication"] for r in selected}):
        for env in CONDITIONS:
            subset = [r for r in selected if r["source_publication"] == name
                      and r["evolution_condition"] == env]
            by_publication[f"{name}|{env}|all_adaptive_classes"] = summarize_group(subset)
    # Same-source, same two parental backgrounds as strictest available
    # compositional check. Still not a true n=evolution-populations effect.
    ira1_matched = {}
    for env in CONDITIONS:
        by_ancestor = {}
        for a in ("IRA1_MIS", "IRA1_NON"):
            subset = [r for r in selected if r["source_publication"] == "This_study"
                      and r["ancestor"] == a and r["evolution_condition"] == env]
            by_ancestor[a] = summarize_group(subset)
        full = [r for r in selected if r["source_publication"] == "This_study"
                and r["ancestor"] in ("IRA1_MIS", "IRA1_NON")
                and r["evolution_condition"] == env]
        q = [by_ancestor[a]["descriptive_both_gain_share"] for a in ("IRA1_MIS", "IRA1_NON")]
        if any(x is None for x in q):
            raise ValueError("both IRA1 parental backgrounds must be observed in each evolution condition")
        ira1_matched[env] = {
            "per_background": by_ancestor,
            "clone_weighted": summarize_group(full),
            "equal_two_parent_mean_both_gain_share": sum(q)/2,
            "same_source_and_two_parents_not_independently_randomized_mutation_origins": True,
        }
    equal_parent = {}
    for env in CONDITIONS:
        rates = []
        for a in BACKGROUNDS:
            q = by_parent[f"{a}|{env}|adaptive_haploid"]
            if q["complete_parent_relative_fermentation_respiration"]:
                rates.append((a, q["descriptive_both_gain_share"],
                              q["descriptive_resp_gain_fer_cost_share"]))
        equal_parent[env] = {
            "represented_backgrounds": [x[0] for x in rates],
            "backgrounds_n": len(rates),
            "mean_of_ancestral_background_specific_both_gain_shares": (
                sum(x[1] for x in rates)/len(rates) if rates else None),
            "mean_of_ancestral_background_specific_resp_gain_fer_cost_shares": (
                sum(x[2] for x in rates)/len(rates) if rates else None),
            "not_an_evolutionary_population_weighted_estimate": True,
        }
    # No independent population ID in S1; cloneID / barcode cannot be treated
    # as a replacement without published mapping.
    return {
        "source_doi": source_inventory["primary_doi"],
        "author_commit": source_inventory["author_repo_commit"],
        "source_SHA256": {
            k: v["bytes_sha256"] for k, v in
            source_inventory["source_git_blobs"].items()
        },
        "S1_all_rows": len(rows),
        "S1_sources": source_inventory["S1_original_source_schema_and_counts"]["category_counts"].get("source_publication"),
        "source_selection": totals,
        "clone_weighted_by_environment_and_class": groups,
        "parent_and_evolution_condition_strata": by_parent,
        "publication_and_evolution_condition_strata": by_publication,
        "same_new_source_matched_IRA1_parent_sensitivity": ira1_matched,
        "equal_weight_across_present_parents_descriptive": equal_parent,
        "interpretation_ceiling": {
            "parent_relative_columns_are_author_deposited": True,
            "source_file_is_four_publication_historical_composite": True,
            "2024_source_rows_not_assumed_independent_of_Aggeli2020": True,
            "single_evolved_clone_not_an_independent_evolution_population": True,
            "no_source_population_id_found_in_deposited_S1_schema": True,
            "S3_185_selected_R2_barcodes_not_full_Evo2D_2024_denominator": True,
            "not_a_random_sample_of_mutation_occurrences": True,
            "two_error_margin_not_equivalent_to_original_repeated_resampling": True,
            "no_predeclared_hypothesis_test_or_meta_analysis": True,
            "no_historical_division_of_two_functions_or_Bita_Ku_estimated": True,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--s1", type=Path, required=True)
    parser.add_argument("--s3", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arg = parser.parse_args()
    d = analyze_original(arg.s1.read_bytes(), arg.s3.read_bytes())
    arg.output.parent.mkdir(parents=True, exist_ok=True)
    arg.output.write_text(json.dumps(d, indent=2, allow_nan=False) + "\n", encoding="utf8")
    print("BITA_KINSLER_PARENT_RELATIVE_PROFILE:" + json.dumps({
        "total_and_source": {"S1_rows":d["S1_all_rows"],"sources":d["S1_sources"]},
        "selection": d["source_selection"],
        "by_condition": d["clone_weighted_by_environment_and_class"],
        "equal_parent": d["equal_weight_across_present_parents_descriptive"],
        "by_publication": d["publication_and_evolution_condition_strata"],
        "matched_IRA1": d["same_new_source_matched_IRA1_parent_sensitivity"],
        "by_parent":d["parent_and_evolution_condition_strata"],
    },separators=(",",":")))


if __name__ == "__main__":
    main()
