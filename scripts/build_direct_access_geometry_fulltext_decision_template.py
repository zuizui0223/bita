"""Build a full-text decision template from the post-freeze bibliographic screen.

Known direct-corpus matches are prefilled and immutable downstream. New records
remain pending until full-text eligibility is adjudicated.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

FIELDS = (
    "frame_id",
    "doi",
    "title",
    "year",
    "source_dbs",
    "query_ids",
    "decision_status",
    "biological_program_id",
    "direction",
    "duplicate_of_program_id",
    "decision_basis",
    "source_identifier",
    "notes",
)

SCREEN_REQUIRED = (
    "frame_id",
    "doi",
    "title",
    "year",
    "source_dbs",
    "query_ids",
    "screen_status",
    "known_study_id",
    "known_direction",
    "eligibility_status",
    "direction",
    "screening_notes",
)


def build(screen_path: Path) -> list[dict[str, str]]:
    with screen_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        observed = tuple(reader.fieldnames or ())
        if observed != SCREEN_REQUIRED:
            raise ValueError(
                f"FULLTEXT_TEMPLATE_SCREEN_SCHEMA_MISMATCH:"
                f"expected={SCREEN_REQUIRED}:observed={observed}"
            )
        rows = list(reader)

    if not rows:
        raise ValueError("FULLTEXT_TEMPLATE_EMPTY_SCREEN")

    output: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in rows:
        fid = row["frame_id"].strip()
        if not fid:
            raise ValueError("FULLTEXT_TEMPLATE_EMPTY_FRAME_ID")
        if fid in seen:
            raise ValueError(f"FULLTEXT_TEMPLATE_DUPLICATE_FRAME_ID:{fid}")
        seen.add(fid)

        status = row["screen_status"].strip()
        if status == "KNOWN_DIRECT_CORPUS_MATCH":
            sid = row["known_study_id"].strip()
            direction = row["known_direction"].strip()
            if not sid or direction not in {"POSITIVE", "NULL", "OPPOSITE", "MIXED"}:
                raise ValueError(f"FULLTEXT_TEMPLATE_INVALID_KNOWN_ROW:{fid}")
            decision_status = "ELIGIBLE_DIRECT"
            biological_program_id = sid
            decision_basis = "PREEXISTING_24_PROGRAM_DIRECT_CORPUS"
            source_identifier = row["doi"].strip() or f"title-year:{row['title']}|{row['year']}"
        elif status == "PENDING_FULLTEXT_ELIGIBILITY":
            decision_status = "PENDING_FULLTEXT"
            biological_program_id = ""
            direction = ""
            decision_basis = ""
            source_identifier = ""
        else:
            raise ValueError(f"FULLTEXT_TEMPLATE_UNKNOWN_SCREEN_STATUS:{fid}:{status}")

        output.append({
            "frame_id": fid,
            "doi": row["doi"].strip(),
            "title": row["title"].strip(),
            "year": row["year"].strip(),
            "source_dbs": row["source_dbs"].strip(),
            "query_ids": row["query_ids"].strip(),
            "decision_status": decision_status,
            "biological_program_id": biological_program_id,
            "direction": direction,
            "duplicate_of_program_id": "",
            "decision_basis": decision_basis,
            "source_identifier": source_identifier,
            "notes": "",
        })
    return output


def write(rows: list[dict[str, str]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--screen", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = build(args.screen)
    write(rows, args.output)
    print(f"FULLTEXT_DECISION_TEMPLATE_ROWS={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
