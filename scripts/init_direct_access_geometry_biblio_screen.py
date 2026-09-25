"""Initialize the outcome-independent screening ledger for the frozen bibliographic frame.

The frame itself must be frozen before this step. Known direct studies are joined by DOI
only after frame construction; their existing adjudications are carried forward as
provenance, while every other bibliographic candidate remains UNSCREENED.
"""
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "empirical" / "floral_defence_selectivity"
DEFAULT_FRAME = BASE / "DIRECT_ACCESS_GEOMETRY_BIBLIO_FRAME_V1.csv"
DEFAULT_DIRECT = BASE / "DIRECT_ACCESS_GEOMETRY_ROBBERY_CORPUS_V1.csv"
DEFAULT_OUTPUT = BASE / "DIRECT_ACCESS_GEOMETRY_BIBLIO_SCREEN_V1.csv"

FIELDS = (
    "candidate_id",
    "identity_key",
    "doi",
    "title",
    "publication_year",
    "geometry_text_match",
    "source_providers",
    "matched_query_ids",
    "known_direct_study_id",
    "screen_status",
    "access_predictor_present",
    "route_resolved_robbery_outcome_present",
    "independent_biological_program",
    "eligibility_decision",
    "direction",
    "full_text_source",
    "screen_notes",
)


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _doi(value: str) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", text)
    text = re.sub(r"^doi:\s*", "", text)
    return text


def initialize(frame_path: Path, direct_path: Path) -> list[dict[str, str]]:
    frame = _read(frame_path)
    direct = _read(direct_path)

    direct_by_doi: dict[str, dict[str, str]] = {}
    for row in direct:
        doi = _doi(row.get("doi", ""))
        if not doi:
            continue
        if doi in direct_by_doi:
            raise ValueError(f"DIRECT_CORPUS_DUPLICATE_DOI:{doi}")
        direct_by_doi[doi] = row

    output: list[dict[str, str]] = []
    seen_candidates: set[str] = set()
    for row in frame:
        candidate_id = row.get("candidate_id", "").strip()
        if not candidate_id:
            raise ValueError("BIBLIO_SCREEN_FRAME_MISSING_CANDIDATE_ID")
        if candidate_id in seen_candidates:
            raise ValueError(f"BIBLIO_SCREEN_DUPLICATE_CANDIDATE_ID:{candidate_id}")
        seen_candidates.add(candidate_id)

        doi = _doi(row.get("doi", ""))
        known = direct_by_doi.get(doi) if doi else None
        if known is None:
            known_id = ""
            status = "UNSCREENED"
            access = ""
            outcome = ""
            independent = ""
            eligible = ""
            direction = ""
            source = ""
            notes = ""
        else:
            known_id = known["study_id"].strip()
            status = "ELIGIBLE_PREVIOUSLY_ADJUDICATED"
            access = "YES"
            outcome = "YES"
            independent = "YES"
            eligible = "YES"
            direction = known["direction"].strip()
            source = f"DIRECT_ACCESS_GEOMETRY_ROBBERY_CORPUS_V1:{known_id}"
            notes = (
                "Existing direct-study adjudication joined after bibliographic-frame "
                "freeze by normalized DOI; not used to select or drop frame records."
            )

        output.append(
            {
                "candidate_id": candidate_id,
                "identity_key": row.get("identity_key", ""),
                "doi": doi,
                "title": row.get("title", ""),
                "publication_year": row.get("publication_year", ""),
                "geometry_text_match": row.get("geometry_text_match", ""),
                "source_providers": row.get("source_providers", ""),
                "matched_query_ids": row.get("matched_query_ids", ""),
                "known_direct_study_id": known_id,
                "screen_status": status,
                "access_predictor_present": access,
                "route_resolved_robbery_outcome_present": outcome,
                "independent_biological_program": independent,
                "eligibility_decision": eligible,
                "direction": direction,
                "full_text_source": source,
                "screen_notes": notes,
            }
        )
    return output


def write(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frame", type=Path, default=DEFAULT_FRAME)
    parser.add_argument("--direct", type=Path, default=DEFAULT_DIRECT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    rows = initialize(args.frame, args.direct)
    write(args.output, rows)
    print(
        f"screen_rows={len(rows)} "
        f"known_adjudicated={sum(r['screen_status'] == 'ELIGIBLE_PREVIOUSLY_ADJUDICATED' for r in rows)} "
        f"unscreened={sum(r['screen_status'] == 'UNSCREENED' for r in rows)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
