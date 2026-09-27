"""Apply a direction-coding batch only to records whose eligibility was frozen first."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from scripts.build_direct_access_geometry_fulltext_decision_template import FIELDS

ELIGIBILITY_FIELDS = (
    "frame_id",
    "doi",
    "title",
    "eligibility_state",
    "biological_program_id",
    "independence_relation",
    "decision_basis",
    "source_identifier",
    "direction_coded",
    "notes",
)

BATCH_FIELDS = (
    "frame_id",
    "doi",
    "title",
    "biological_program_id",
    "direction",
    "orientation_basis",
    "source_identifier",
    "evidence_basis",
    "notes",
)
DIRECTIONS = {"POSITIVE", "NULL", "OPPOSITE", "MIXED"}


def _read(path: Path) -> tuple[tuple[str, ...], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return tuple(reader.fieldnames or ()), list(reader)


def apply(
    decisions_path: Path,
    batch_path: Path,
    eligibility_paths: list[Path],
    output_path: Path,
    receipt_path: Path,
) -> dict[str, object]:
    decision_fields, decisions = _read(decisions_path)
    batch_fields, batch = _read(batch_path)
    if decision_fields != FIELDS:
        raise ValueError("DIR_APPLY_DECISION_SCHEMA_MISMATCH")
    if batch_fields != BATCH_FIELDS:
        raise ValueError("DIR_APPLY_BATCH_SCHEMA_MISMATCH")

    eligibility: dict[str, dict[str, str]] = {}
    for path in eligibility_paths:
        fields, rows = _read(path)
        if fields != ELIGIBILITY_FIELDS:
            raise ValueError(f"DIR_APPLY_ELIGIBILITY_SCHEMA_MISMATCH:{path}")
        for row in rows:
            fid = row["frame_id"].strip()
            if not fid or fid in eligibility:
                raise ValueError(f"DIR_APPLY_DUPLICATE_ELIGIBILITY_RECORD:{fid}")
            eligibility[fid] = row

    by_id = {row["frame_id"].strip(): row for row in decisions}
    seen_programs = {
        row["biological_program_id"].strip()
        for row in decisions
        if row["decision_status"].strip() == "ELIGIBLE_DIRECT"
        and row["biological_program_id"].strip()
    }

    applied = []
    direction_counts = {key: 0 for key in ("POSITIVE", "NULL", "OPPOSITE", "MIXED")}

    for row in batch:
        fid = row["frame_id"].strip()
        decision = by_id.get(fid)
        if decision is None:
            raise ValueError(f"DIR_APPLY_UNKNOWN_FRAME_ID:{fid}")
        if decision["decision_status"].strip() != "PENDING_FULLTEXT":
            raise ValueError(f"DIR_APPLY_NOT_PENDING:{fid}:{decision['decision_status']}")
        if decision["doi"].strip() != row["doi"].strip():
            raise ValueError(f"DIR_APPLY_DOI_MISMATCH:{fid}")
        if decision["title"].strip() != row["title"].strip():
            raise ValueError(f"DIR_APPLY_TITLE_MISMATCH:{fid}")

        program = row["biological_program_id"].strip()
        direction = row["direction"].strip()
        if not program or program in seen_programs:
            raise ValueError(f"DIR_APPLY_DUPLICATE_OR_EMPTY_PROGRAM:{fid}:{program}")
        if direction not in DIRECTIONS:
            raise ValueError(f"DIR_APPLY_INVALID_DIRECTION:{fid}:{direction}")
        if not row["source_identifier"].strip() or not row["evidence_basis"].strip():
            raise ValueError(f"DIR_APPLY_MISSING_SOURCE:{fid}")

        frozen = eligibility.get(fid)
        if frozen is None:
            raise ValueError(f"DIR_APPLY_ELIGIBILITY_NOT_PRE_FROZEN:{fid}:{program}")
        if frozen["eligibility_state"].strip() != "ELIGIBLE_DIRECT_NEW":
            raise ValueError(
                f"DIR_APPLY_ELIGIBILITY_NOT_NEW_DIRECT:{fid}:"
                f"{frozen['eligibility_state'].strip()}"
            )
        if frozen["biological_program_id"].strip() != program:
            raise ValueError(
                f"DIR_APPLY_ELIGIBILITY_PROGRAM_MISMATCH:{fid}:"
                f"batch={program}:frozen={frozen['biological_program_id'].strip()}"
            )
        if frozen["direction_coded"].strip() != "NO":
            raise ValueError(f"DIR_APPLY_ELIGIBILITY_DIRECTION_ALREADY_CODED:{fid}")

        decision["decision_status"] = "ELIGIBLE_DIRECT"
        decision["biological_program_id"] = program
        decision["direction"] = direction
        decision["duplicate_of_program_id"] = ""
        decision["decision_basis"] = "PRIMARY_SOURCE_DIRECTION_CODE_AFTER_ELIGIBILITY_FREEZE"
        decision["source_identifier"] = row["source_identifier"].strip()
        decision["notes"] = (
            f"DIRECTION_CODED_AFTER_ELIGIBILITY_FREEZE;"
            f"orientation={row['orientation_basis'].strip()};"
            f"evidence={row['evidence_basis'].strip()};"
            f"{row['notes'].strip()}"
        )
        seen_programs.add(program)
        direction_counts[direction] += 1
        applied.append({"frame_id": fid, "program": program, "direction": direction})

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(decisions)

    receipt = {
        "schema": "BITA_DIRECT_ACCESS_GEOMETRY_DIRECTION_APPLY_V1",
        "status": "DIRECTION_BATCH_APPLIED_AFTER_ELIGIBILITY_FREEZE",
        "applied_records": applied,
        "direction_counts": direction_counts,
        "eligible_direct_total_after_apply": sum(
            row["decision_status"].strip() == "ELIGIBLE_DIRECT" for row in decisions
        ),
        "pending_records_after_apply": sum(
            row["decision_status"].strip() == "PENDING_FULLTEXT" for row in decisions
        ),
    }
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--decisions", type=Path, required=True)
    parser.add_argument("--batch", type=Path, required=True)
    parser.add_argument(
        "--eligibility-adjudication",
        type=Path,
        action="append",
        required=True,
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    result = apply(
        args.decisions,
        args.batch,
        args.eligibility_adjudication,
        args.output,
        args.receipt,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
