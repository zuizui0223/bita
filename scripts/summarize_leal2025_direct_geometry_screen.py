"""Summarize the completed historical Leal-label screen for direct geometry -> robbery."""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = (
    ROOT / "empirical" / "floral_defence_selectivity"
    / "LEAL2025_DIRECT_GEOMETRY_SCREEN_V1.csv"
)

ALLOWED = {
    "INELIGIBLE_NO_GEOMETRY_TEST",
    "ELIGIBLE_DIRECTION_EXPOSED",
    "PROVENANCE_CONFLICT_SPLIT_REQUIRED",
}
DIRECTIONS = {"POSITIVE", "NULL", "OPPOSITE", "MIXED"}


def summarize(path: Path = SCREEN) -> dict[str, object]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    if len(rows) != 56:
        raise ValueError(f"HISTORICAL_SCREEN_EXPECTED_56_LABELS:{len(rows)}")

    ids = [row["study_id"].strip() for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("HISTORICAL_SCREEN_DUPLICATE_LABEL")

    statuses = Counter(row["screen_status"].strip() for row in rows)
    bad = set(statuses) - ALLOWED
    if bad:
        raise ValueError("HISTORICAL_SCREEN_INVALID_STATUS:" + ",".join(sorted(bad)))

    eligible = [
        row for row in rows
        if row["screen_status"].strip() == "ELIGIBLE_DIRECTION_EXPOSED"
    ]
    conflicts = [
        row for row in rows
        if row["screen_status"].strip() == "PROVENANCE_CONFLICT_SPLIT_REQUIRED"
    ]
    unscreened = [row for row in rows if row["screen_status"].strip() == "UNSCREENED"]

    if unscreened:
        raise ValueError(
            "HISTORICAL_SCREEN_NOT_COMPLETE:"
            + ",".join(row["study_id"] for row in unscreened)
        )
    for row in eligible:
        direction = row["direction"].strip()
        if direction not in DIRECTIONS:
            raise ValueError(
                f"HISTORICAL_ELIGIBLE_INVALID_DIRECTION:{row['study_id']}:{direction}"
            )
        if row["eligible"].strip() != "YES":
            raise ValueError(f"HISTORICAL_ELIGIBLE_FLAG_MISMATCH:{row['study_id']}")

    direction_counts = Counter(row["direction"].strip() for row in eligible)
    return {
        "schema": "BITA_LEAL2025_DIRECT_GEOMETRY_SCREEN_SUMMARY_V1",
        "historical_source_labels": len(rows),
        "screened_labels": len(rows),
        "ineligible_no_geometry_test": statuses["INELIGIBLE_NO_GEOMETRY_TEST"],
        "eligible_direct_geometry_labels": len(eligible),
        "provenance_conflict_labels": len(conflicts),
        "eligible_direction_counts": {
            key: direction_counts.get(key, 0)
            for key in ("POSITIVE", "NULL", "OPPOSITE", "MIXED")
        },
        "eligible_labels": [row["study_id"] for row in eligible],
        "conflict_labels": [row["study_id"] for row in conflicts],
        "source_resolved_independent_program_denominator": None,
        "formal_recurrence_result_open": False,
        "primary_standardized_network_k": 2,
        "status": "HISTORICAL_LABEL_SCREEN_COMPLETE_PROVENANCE_REPAIR_REQUIRED",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--screen", type=Path, default=SCREEN)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = summarize(args.screen)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
