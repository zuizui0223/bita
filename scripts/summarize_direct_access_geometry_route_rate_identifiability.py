"""Summarize the frozen 33-program route-rate identifiability audit."""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

EXPECTED_CLASSES = (
    "ZERO_INCLUSIVE_BOTH_ROUTE_RATES",
    "BOTH_ROUTE_COUNTS_NO_ZERO_INCLUSIVE_DENOMINATOR",
    "CONDITIONAL_ROUTE_CHOICE_ONLY",
    "ROBBERY_PREVALENCE_ONLY",
    "OTHER_ROUTE_RESOLVED_NOT_RATE_IDENTIFIABLE",
    "UNRESOLVED_SOURCE",
)
EXPECTED_N = 33


def summarize(path: str | Path) -> dict[str, object]:
    rows = list(csv.DictReader(Path(path).open(encoding="utf-8", newline="")))
    if len(rows) != EXPECTED_N:
        raise ValueError(f"expected {EXPECTED_N} programs, found {len(rows)}")

    ids = [row["program_id"].strip() for row in rows]
    if any(not value for value in ids):
        raise ValueError("blank program_id")
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate program_id")

    invalid = sorted(
        {
            row["identifiability_class"].strip()
            for row in rows
            if row["identifiability_class"].strip() not in EXPECTED_CLASSES
        }
    )
    if invalid:
        raise ValueError(f"invalid identifiability classes: {invalid}")

    pending_cells: list[str] = []
    for row in rows:
        for key in (
            "identifiability_class",
            "geometry_manipulation",
            "legitimate_route_separate",
            "robbery_route_separate",
            "zero_interaction_state",
            "common_effort_denominator",
            "source_basis",
            "source_locator",
            "rationale",
        ):
            if row[key].strip() in {"", "PENDING"}:
                pending_cells.append(f"{row['program_id']}:{key}")
    if pending_cells:
        raise ValueError(f"audit contains unresolved cells: {pending_cells[:10]}")

    counts = Counter(row["identifiability_class"].strip() for row in rows)
    for key in EXPECTED_CLASSES:
        counts.setdefault(key, 0)

    strict = counts["ZERO_INCLUSIVE_BOTH_ROUTE_RATES"]
    non_strict = EXPECTED_N - strict
    route_both_any = (
        strict
        + counts["BOTH_ROUTE_COUNTS_NO_ZERO_INCLUSIVE_DENOMINATOR"]
    )

    strict_programs = sorted(
        row["program_id"]
        for row in rows
        if row["identifiability_class"].strip()
        == "ZERO_INCLUSIVE_BOTH_ROUTE_RATES"
    )

    return {
        "schema": "BITA_DIRECT_ACCESS_GEOMETRY_ROUTE_RATE_IDENTIFIABILITY_V1",
        "status": "POST_HOC_DESIGN_AUDIT_COMPLETE",
        "source_frame_programs": EXPECTED_N,
        "class_counts": dict(sorted(counts.items())),
        "strict_zero_inclusive_both_route_programs": strict,
        "strict_zero_inclusive_both_route_fraction": strict / EXPECTED_N,
        "not_strict_zero_inclusive_both_route_programs": non_strict,
        "not_strict_zero_inclusive_both_route_fraction": non_strict / EXPECTED_N,
        "both_route_metrics_any_denominator_programs": route_both_any,
        "strict_program_ids": strict_programs,
        "claim": (
            f"Within the frozen 33-program direct access-geometry frame, "
            f"{strict}/{EXPECTED_N} programs ({100*strict/EXPECTED_N:.1f}%) "
            "meet the strict zero-inclusive both-route-rate criterion. "
            f"The remaining {non_strict}/{EXPECTED_N} do not. This is a "
            "post-hoc finite-frame design audit, not an estimate of the "
            "prevalence of study designs in all ecological literature."
        ),
        "claim_boundaries": [
            "post_hoc_design_audit",
            "finite_formal_frame_not_all_literature",
            "does_not_change_effect_direction_counts",
            "does_not_increment_standardized_network_k",
            "strict_class_requires_common_zero_inclusive_denominator",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("audit_csv", type=Path)
    parser.add_argument("output_json", type=Path)
    args = parser.parse_args()
    result = summarize(args.audit_csv)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
