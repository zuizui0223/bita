"""Validate Stage-U systematic update/gap-fill screening for direct geometry -> robbery."""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = (
    ROOT / "empirical" / "floral_defence_selectivity"
    / "DIRECT_ACCESS_GEOMETRY_STAGE_U_REGISTRY_V1.csv"
)

ELIGIBLE = "ELIGIBLE"
DUPLICATE = "DUPLICATE_COMPONENT_OF_LATER_SYNTHESIS"
INELIGIBLE_PREFIX = "INELIGIBLE_"
DIRECTIONS = {"POSITIVE", "NULL", "OPPOSITE", "MIXED"}


def validate(path: Path = REGISTRY) -> dict[str, object]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        raise ValueError("STAGE_U_REGISTRY_EMPTY")
    ids = [row["candidate_id"].strip() for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("STAGE_U_DUPLICATE_CANDIDATE_ID")

    eligible = []
    duplicates = []
    ineligible = []
    invalid = []

    for row in rows:
        status = row["eligibility_status"].strip()
        direction = row["direction_if_eligible"].strip()
        if status == ELIGIBLE:
            eligible.append(row)
            if direction not in DIRECTIONS:
                invalid.append(f"eligible_direction:{row['candidate_id']}:{direction}")
        elif status == DUPLICATE:
            duplicates.append(row)
            if direction:
                invalid.append(f"duplicate_has_direction:{row['candidate_id']}")
        elif status.startswith(INELIGIBLE_PREFIX):
            ineligible.append(row)
            if direction:
                invalid.append(f"ineligible_has_direction:{row['candidate_id']}")
        else:
            invalid.append(f"status:{row['candidate_id']}:{status}")

        if not row["reason"].strip():
            invalid.append(f"missing_reason:{row['candidate_id']}")

    if invalid:
        raise ValueError("STAGE_U_INVALID:" + ",".join(invalid))

    directions = Counter(row["direction_if_eligible"].strip() for row in eligible)
    return {
        "schema": "BITA_DIRECT_ACCESS_GEOMETRY_STAGE_U_V1",
        "candidate_records": len(rows),
        "eligible_new_programs": len(eligible),
        "duplicate_records": len(duplicates),
        "ineligible_records": len(ineligible),
        "eligible_direction_counts": {
            key: directions.get(key, 0)
            for key in ("POSITIVE", "NULL", "OPPOSITE", "MIXED")
        },
        "stage_u_search_complete": False,
        "formal_recurrence_result_open": False,
        "primary_standardized_network_k": 2,
        "status": "STAGE_U_BATCH_2_SCREENED_SEARCH_CONTINUES",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=REGISTRY)
    args = parser.parse_args()
    print(json.dumps(validate(args.registry), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
