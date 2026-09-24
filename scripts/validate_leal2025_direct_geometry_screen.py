"""Validate the Leal historical-label screen for direct geometry -> robbery evidence."""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "empirical" / "floral_defence_selectivity"
SCREEN = BASE / "LEAL2025_DIRECT_GEOMETRY_SCREEN_V1.csv"

ALLOWED = {
    "INELIGIBLE_NO_GEOMETRY_TEST",
    "ELIGIBLE_DIRECTION_EXPOSED",
    "PROVENANCE_CONFLICT_SPLIT_REQUIRED",
}


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate(path: Path = SCREEN) -> dict[str, object]:
    rows = _read(path)
    if len(rows) != 56:
        raise ValueError(f"LEAL_GEOMETRY_SCREEN_LABEL_COUNT_MISMATCH:{len(rows)}")

    labels = [row["study_id"].strip() for row in rows]
    if len(set(labels)) != len(labels):
        raise ValueError("LEAL_GEOMETRY_SCREEN_DUPLICATE_LABEL")

    statuses = Counter(row["screen_status"].strip() for row in rows)
    unknown = sorted(set(statuses) - ALLOWED)
    if unknown:
        raise ValueError("LEAL_GEOMETRY_SCREEN_UNKNOWN_STATUS:" + ",".join(unknown))

    if statuses["INELIGIBLE_NO_GEOMETRY_TEST"] != 50:
        raise ValueError("LEAL_GEOMETRY_SCREEN_EXPECTED_50_INELIGIBLE")
    if statuses["ELIGIBLE_DIRECTION_EXPOSED"] != 4:
        raise ValueError("LEAL_GEOMETRY_SCREEN_EXPECTED_4_ELIGIBLE")
    if statuses["PROVENANCE_CONFLICT_SPLIT_REQUIRED"] != 2:
        raise ValueError("LEAL_GEOMETRY_SCREEN_EXPECTED_2_PROVENANCE_CONFLICTS")

    conflicts = sorted(
        row["study_id"].strip()
        for row in rows
        if row["screen_status"].strip() == "PROVENANCE_CONFLICT_SPLIT_REQUIRED"
    )
    if conflicts != ["Varma&Sinu2019", "Zhangetal2009a"]:
        raise ValueError("LEAL_GEOMETRY_SCREEN_UNEXPECTED_CONFLICT_SET")

    eligible = [
        row for row in rows
        if row["screen_status"].strip() == "ELIGIBLE_DIRECTION_EXPOSED"
    ]
    directions = Counter(row["direction"].strip() for row in eligible)
    expected_directions = {"POSITIVE": 2, "NULL": 1, "MIXED": 1}
    if dict(directions) != expected_directions:
        raise ValueError(
            "LEAL_GEOMETRY_SCREEN_DIRECTION_MISMATCH:"
            + json.dumps(dict(directions), sort_keys=True)
        )

    for row in rows:
        status = row["screen_status"].strip()
        if status == "INELIGIBLE_NO_GEOMETRY_TEST":
            if row["eligible"].strip() != "NO":
                raise ValueError(f"INELIGIBLE_ROW_NOT_NO:{row['study_id']}")
            if not row["notes"].strip():
                raise ValueError(f"INELIGIBLE_ROW_MISSING_REASON:{row['study_id']}")
        elif status == "ELIGIBLE_DIRECTION_EXPOSED":
            if row["eligible"].strip() != "YES":
                raise ValueError(f"ELIGIBLE_ROW_NOT_YES:{row['study_id']}")
            if not row["access_predictor"].strip() or not row["robbery_outcome"].strip():
                raise ValueError(f"ELIGIBLE_ROW_MISSING_CONSTRUCT:{row['study_id']}")
            if row["direction"].strip() not in {"POSITIVE", "NULL", "OPPOSITE", "MIXED"}:
                raise ValueError(f"ELIGIBLE_ROW_INVALID_DIRECTION:{row['study_id']}")
        else:
            if any(row[key].strip() for key in ("eligible", "direction")):
                raise ValueError(f"CONFLICT_ROW_PREMATURELY_ADJUDICATED:{row['study_id']}")

    return {
        "schema": "BITA_LEAL2025_DIRECT_GEOMETRY_SCREEN_V1",
        "historical_study_field_labels": 56,
        "screened_unambiguous_labels": 54,
        "ineligible_no_geometry_test": 50,
        "eligible_direct_geometry_test": 4,
        "eligible_directions": {
            "POSITIVE": 2,
            "NULL": 1,
            "OPPOSITE": 0,
            "MIXED": 1,
        },
        "provenance_conflict_labels": conflicts,
        "source_resolved_program_denominator_ready": False,
        "formal_recurrence_result_open": False,
        "status": "LABEL_SCREEN_COMPLETE_SOURCE_REPAIR_REQUIRED",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--screen", type=Path, default=SCREEN)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = validate(args.screen)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
