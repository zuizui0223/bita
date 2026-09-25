"""Validate full-text decisions for the formal geometry bibliographic frame."""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from scripts.build_direct_access_geometry_fulltext_decision_template import (
    FIELDS,
    SCREEN_REQUIRED,
)

DIRECTIONS = {"POSITIVE", "NULL", "OPPOSITE", "MIXED"}


def _read(path: Path) -> tuple[tuple[str, ...], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return tuple(reader.fieldnames or ()), list(reader)


def validate(
    screen_path: Path,
    decisions_path: Path,
    *,
    require_complete: bool = False,
) -> dict[str, object]:
    screen_fields, screen_rows = _read(screen_path)
    decision_fields, decision_rows = _read(decisions_path)

    if screen_fields != SCREEN_REQUIRED:
        raise ValueError("FULLTEXT_VALIDATE_SCREEN_SCHEMA_MISMATCH")
    if decision_fields != FIELDS:
        raise ValueError("FULLTEXT_VALIDATE_DECISION_SCHEMA_MISMATCH")

    screen_by_id: dict[str, dict[str, str]] = {}
    for row in screen_rows:
        fid = row["frame_id"].strip()
        if not fid or fid in screen_by_id:
            raise ValueError(f"FULLTEXT_VALIDATE_BAD_SCREEN_FRAME_ID:{fid}")
        screen_by_id[fid] = row

    decisions_by_id: dict[str, dict[str, str]] = {}
    for row in decision_rows:
        fid = row["frame_id"].strip()
        if not fid or fid in decisions_by_id:
            raise ValueError(f"FULLTEXT_VALIDATE_BAD_DECISION_FRAME_ID:{fid}")
        decisions_by_id[fid] = row

    if set(screen_by_id) != set(decisions_by_id):
        missing = sorted(set(screen_by_id) - set(decisions_by_id))
        extra = sorted(set(decisions_by_id) - set(screen_by_id))
        raise ValueError(
            f"FULLTEXT_VALIDATE_FRAME_COVERAGE_MISMATCH:missing={missing}:extra={extra}"
        )

    pending: list[str] = []
    eligible_programs: list[str] = []
    direction_counts: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()
    duplicate_targets: list[str] = []

    for fid, decision in decisions_by_id.items():
        screen = screen_by_id[fid]

        for key in ("doi", "title", "year", "source_dbs", "query_ids"):
            if decision[key].strip() != screen[key].strip():
                raise ValueError(f"FULLTEXT_VALIDATE_IMMUTABLE_METADATA_CHANGED:{fid}:{key}")

        status = decision["decision_status"].strip()
        direction = decision["direction"].strip()
        program_id = decision["biological_program_id"].strip()
        duplicate_of = decision["duplicate_of_program_id"].strip()
        basis = decision["decision_basis"].strip()
        source_identifier = decision["source_identifier"].strip()

        if screen["screen_status"].strip() == "KNOWN_DIRECT_CORPUS_MATCH":
            expected_program = screen["known_study_id"].strip()
            expected_direction = screen["known_direction"].strip()
            if status != "ELIGIBLE_DIRECT":
                raise ValueError(f"FULLTEXT_VALIDATE_KNOWN_STATUS_CHANGED:{fid}")
            if program_id != expected_program:
                raise ValueError(f"FULLTEXT_VALIDATE_KNOWN_PROGRAM_CHANGED:{fid}")
            if direction != expected_direction:
                raise ValueError(f"FULLTEXT_VALIDATE_KNOWN_DIRECTION_CHANGED:{fid}")
            if duplicate_of:
                raise ValueError(f"FULLTEXT_VALIDATE_KNOWN_MARKED_DUPLICATE:{fid}")
            if not basis.startswith("PREEXISTING_"):
                raise ValueError(f"FULLTEXT_VALIDATE_KNOWN_BASIS_CHANGED:{fid}")

        if status == "PENDING_FULLTEXT":
            pending.append(fid)
            if any((program_id, direction, duplicate_of, basis, source_identifier)):
                raise ValueError(f"FULLTEXT_VALIDATE_PENDING_HAS_DECISION_DATA:{fid}")
        elif status == "ELIGIBLE_DIRECT":
            if not program_id:
                raise ValueError(f"FULLTEXT_VALIDATE_ELIGIBLE_MISSING_PROGRAM:{fid}")
            if direction not in DIRECTIONS:
                raise ValueError(f"FULLTEXT_VALIDATE_ELIGIBLE_INVALID_DIRECTION:{fid}")
            if duplicate_of:
                raise ValueError(f"FULLTEXT_VALIDATE_ELIGIBLE_HAS_DUPLICATE_TARGET:{fid}")
            if not basis or not source_identifier:
                raise ValueError(f"FULLTEXT_VALIDATE_ELIGIBLE_MISSING_PROVENANCE:{fid}")
            eligible_programs.append(program_id)
            direction_counts[direction] += 1
        elif status == "DUPLICATE_BIOLOGICAL_PROGRAM":
            if program_id or direction:
                raise ValueError(f"FULLTEXT_VALIDATE_DUPLICATE_HAS_EFFECT_DATA:{fid}")
            if not duplicate_of or not basis or not source_identifier:
                raise ValueError(f"FULLTEXT_VALIDATE_DUPLICATE_MISSING_PROVENANCE:{fid}")
            duplicate_targets.append(duplicate_of)
        elif status.startswith("INELIGIBLE_"):
            if program_id or direction or duplicate_of:
                raise ValueError(f"FULLTEXT_VALIDATE_INELIGIBLE_HAS_EFFECT_DATA:{fid}")
            if not basis or not source_identifier:
                raise ValueError(f"FULLTEXT_VALIDATE_INELIGIBLE_MISSING_PROVENANCE:{fid}")
        else:
            raise ValueError(f"FULLTEXT_VALIDATE_UNKNOWN_STATUS:{fid}:{status}")

        status_counts[status] += 1

    duplicates = sorted(
        program
        for program, count in Counter(eligible_programs).items()
        if count > 1
    )
    if duplicates:
        raise ValueError(
            "FULLTEXT_VALIDATE_DUPLICATE_ELIGIBLE_PROGRAM_IDS:" + ",".join(duplicates)
        )

    if require_complete and pending:
        raise ValueError(
            "FULLTEXT_VALIDATE_PENDING_RECORDS:" + ",".join(sorted(pending))
        )

    complete = not pending
    return {
        "schema": "BITA_DIRECT_ACCESS_GEOMETRY_FULLTEXT_DECISIONS_V1",
        "status": (
            "FULLTEXT_ELIGIBILITY_SCREEN_COMPLETE"
            if complete
            else "FULLTEXT_ELIGIBILITY_SCREEN_INCOMPLETE"
        ),
        "frame_records": len(screen_rows),
        "pending_records": len(pending),
        "eligible_direct_programs_in_frame": len(eligible_programs),
        "eligible_direction_counts": {
            key: direction_counts.get(key, 0)
            for key in ("POSITIVE", "NULL", "OPPOSITE", "MIXED")
        },
        "duplicate_records": status_counts.get("DUPLICATE_BIOLOGICAL_PROGRAM", 0),
        "ineligible_records": sum(
            count for key, count in status_counts.items() if key.startswith("INELIGIBLE_")
        ),
        "biological_program_ids_unique": True,
        "fulltext_screen_complete": complete,
        "formal_recurrence_result_open": False,
        "primary_standardized_network_k": 2,
        "next_gate": (
            "FORMAL_RECURRENCE_SUMMARY"
            if complete
            else "COMPLETE_PENDING_FULLTEXT_DECISIONS"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--screen", type=Path, required=True)
    parser.add_argument("--decisions", type=Path, required=True)
    parser.add_argument("--require-complete", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = validate(
        args.screen,
        args.decisions,
        require_complete=args.require_complete,
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
