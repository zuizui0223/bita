from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Iterable

from trait_architecture.floral_defence_selectivity import (
    derive_defence_state,
    derive_pollinator_state,
    load_csv_rows,
    registry_key,
    validate_architecture_codes,
    validate_no_outcome_leakage,
    validate_outcome_codes,
    validate_registry,
)


def _index_unique(
    rows: Iterable[dict[str, str]], label: str
) -> dict[tuple[str, str, str], dict[str, str]]:
    indexed: dict[tuple[str, str, str], dict[str, str]] = {}
    for row in rows:
        key = registry_key(row)
        if key in indexed:
            raise ValueError(f"duplicate {label} key: {key}")
        indexed[key] = row
    return indexed


def _raise_validation(label: str, errors: list[str]) -> None:
    if errors:
        raise ValueError(f"{label} validation failed: " + "; ".join(errors))


def build_analysis_ready(
    registry_rows: list[dict[str, str]],
    architecture_rows: list[dict[str, str]],
    outcome_rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], dict[str, int]]:
    _raise_validation("registry", validate_registry(registry_rows))
    _raise_validation("architecture", validate_architecture_codes(architecture_rows))
    _raise_validation("architecture leakage", validate_no_outcome_leakage(architecture_rows))
    _raise_validation("outcome", validate_outcome_codes(outcome_rows))

    registry = _index_unique(registry_rows, "registry")
    architecture = _index_unique(architecture_rows, "architecture")
    outcomes = _index_unique(outcome_rows, "outcome")

    joined: list[dict[str, str]] = []
    for key, reg in registry.items():
        if key not in architecture:
            raise ValueError(f"missing architecture for registry key: {key}")
        if key not in outcomes:
            raise ValueError(f"missing outcome for registry key: {key}")
        row = dict(reg)
        row.update(architecture[key])
        row.update(outcomes[key])
        row["defence_efficacy_state"] = derive_defence_state(outcomes[key])
        row["pollinator_cost_state_derived"] = derive_pollinator_state(outcomes[key])
        joined.append(row)

    extra_architecture = sorted(set(architecture) - set(registry))
    extra_outcomes = sorted(set(outcomes) - set(registry))
    if extra_architecture:
        raise ValueError(f"architecture keys not present in registry: {extra_architecture}")
    if extra_outcomes:
        raise ValueError(f"outcome keys not present in registry: {extra_outcomes}")

    clusters = {row["study_cluster_id"] for row in joined}
    stage1 = {
        row["study_cluster_id"]
        for row in joined
        if row["defence_efficacy_state"] in {"EFFECTIVE", "NULL_OR_WEAK"}
    }
    stage2_strict = {
        row["study_cluster_id"]
        for row in joined
        if row["defence_efficacy_state"] == "EFFECTIVE"
        and row["pollinator_cost_state_derived"] in {"PRESERVED_OR_IMPROVED", "IMPAIRED"}
    }
    stage2_null = {
        row["study_cluster_id"]
        for row in joined
        if row["defence_efficacy_state"] == "EFFECTIVE"
        and row["pollinator_cost_state_derived"] == "NO_DETECTED_CHANGE"
    }
    stage2_transition = {
        row["study_cluster_id"]
        for row in joined
        if row["defence_efficacy_state"] == "EFFECTIVE"
        and row["pollinator_cost_state_derived"] == "MIXED"
    }
    derivation = {
        row["study_cluster_id"]
        for row in joined
        if row["derivation_or_holdout"] == "derivation"
    }
    holdout = {
        row["study_cluster_id"]
        for row in joined
        if row["derivation_or_holdout"] == "holdout"
    }

    audit = {
        "registry_rows": len(registry_rows),
        "independent_study_clusters": len(clusters),
        "stage1_eligible_clusters": len(stage1),
        "stage2_strict_eligible_clusters": len(stage2_strict),
        "stage2_null_compatible_clusters": len(stage2_null),
        "stage2_transition_clusters": len(stage2_transition),
        "derivation_clusters": len(derivation),
        "holdout_clusters": len(holdout),
    }
    return joined, audit


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for field in row:
            if field not in fieldnames:
                fieldnames.append(field)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    registry = load_csv_rows(args.input_dir / "matched_system_registry.csv")
    architecture = load_csv_rows(args.input_dir / "architecture_codes.csv")
    outcomes = load_csv_rows(args.input_dir / "outcome_codes.csv")
    joined, audit = build_analysis_ready(registry, architecture, outcomes)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(args.output_dir / "analysis_ready_matched_systems.csv", joined)
    (args.output_dir / "corpus_audit.json").write_text(
        json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    provenance = [
        {
            "study_cluster_id": row["study_cluster_id"],
            "D_axis_id": row["D_axis_id"],
            "context_id": row["context_id"],
            "source_provenance_path": row["source_provenance_path"],
            "architecture_basis_path": row["architecture_basis_path"],
            "outcome_basis_path": row["outcome_basis_path"],
        }
        for row in joined
    ]
    _write_csv(args.output_dir / "provenance_audit.csv", provenance)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
