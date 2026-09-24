"""Validate the formal sampling-frame scaffolding for direct access geometry -> robbery."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "empirical" / "floral_defence_selectivity"
LEAL = BASE / "LEAL2025_ROBBER_STUDY_FRAME_V1.csv"
DIRECT = BASE / "DIRECT_ACCESS_GEOMETRY_ROBBERY_CORPUS_V1.csv"
CROSSWALK = BASE / "DIRECT_ACCESS_GEOMETRY_LEAL2025_CROSSWALK_V1.csv"


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate() -> dict[str, object]:
    leal = _read(LEAL)
    direct = _read(DIRECT)
    cross = _read(CROSSWALK)

    leal_ids = [row["study_id"].strip() for row in leal]
    direct_ids = [row["study_id"].strip() for row in direct]
    cross_ids = [row["direct_study_id"].strip() for row in cross]

    if len(leal_ids) != 56:
        raise ValueError(f"LEAL_FRAME_COUNT_MISMATCH:{len(leal_ids)}")
    if len(set(leal_ids)) != len(leal_ids):
        raise ValueError("LEAL_FRAME_DUPLICATE_STUDY_ID")
    if len(set(direct_ids)) != len(direct_ids):
        raise ValueError("DIRECT_FRAME_DUPLICATE_STUDY_ID")
    if set(cross_ids) != set(direct_ids):
        missing = sorted(set(direct_ids) - set(cross_ids))
        extra = sorted(set(cross_ids) - set(direct_ids))
        raise ValueError(f"CROSSWALK_COVERAGE_MISMATCH:missing={missing}:extra={extra}")

    allowed = {"IN_FRAME", "NOT_IN_FRAME"}
    bad = sorted({row["leal2025_frame_status"] for row in cross} - allowed)
    if bad:
        raise ValueError("CROSSWALK_INVALID_STATUS:" + ",".join(bad))

    in_frame = [row for row in cross if row["leal2025_frame_status"] == "IN_FRAME"]
    if len(in_frame) != 3:
        raise ValueError(f"CROSSWALK_EXPECTED_THREE_OVERLAPS:{len(in_frame)}")

    for row in in_frame:
        mapped = row["leal2025_study_id"].strip()
        if not mapped:
            raise ValueError(f"CROSSWALK_MISSING_LEAL_ID:{row['direct_study_id']}")
        if mapped not in leal_ids:
            raise ValueError(
                f"CROSSWALK_UNKNOWN_LEAL_ID:{row['direct_study_id']}:{mapped}"
            )

    for row in cross:
        if row["leal2025_frame_status"] == "NOT_IN_FRAME" and row["leal2025_study_id"].strip():
            raise ValueError(f"CROSSWALK_NONFRAME_HAS_LEAL_ID:{row['direct_study_id']}")

    return {
        "schema": "BITA_DIRECT_ACCESS_GEOMETRY_FORMAL_FRAME_V1",
        "historical_frame_studies": len(leal_ids),
        "direct_discovery_programs": len(direct_ids),
        "discovery_overlap_with_historical_frame": len(in_frame),
        "discovery_not_in_historical_frame": len(direct_ids) - len(in_frame),
        "formal_recurrence_result_open": False,
        "primary_standardized_network_k": 2,
        "status": "FRAME_FROZEN_SCREENING_REQUIRED",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = validate()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
