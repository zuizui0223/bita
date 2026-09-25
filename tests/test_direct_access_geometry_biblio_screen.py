from __future__ import annotations

import csv
from pathlib import Path

from scripts.init_direct_access_geometry_biblio_screen import FIELDS, initialize


FRAME_FIELDS = [
    "candidate_id",
    "identity_key",
    "doi",
    "title",
    "publication_year",
    "publication_date",
    "journal",
    "authors",
    "abstract",
    "source_providers",
    "provider_ids",
    "matched_query_ids",
    "source_urls",
    "best_provider_rank",
    "larceny_text_match",
    "geometry_text_match",
    "screen_status",
    "screen_reason",
]

DIRECT_FIELDS = [
    "study_id",
    "year",
    "doi",
    "fauna",
    "plant_scope",
    "study_scale",
    "access_predictor",
    "robbery_outcome",
    "direction",
    "effect_detail",
    "network_k_eligible",
    "reason_not_k",
    "source_role",
    "notes",
]


def _write(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _frame(candidate_id: str, doi: str, geometry: str) -> dict[str, str]:
    row = {field: "" for field in FRAME_FIELDS}
    row.update(
        {
            "candidate_id": candidate_id,
            "identity_key": f"doi:{doi}" if doi else f"provider:{candidate_id}",
            "doi": doi,
            "title": f"Study {candidate_id}",
            "publication_year": "2020",
            "source_providers": "crossref",
            "matched_query_ids": "Q01",
            "larceny_text_match": "true",
            "geometry_text_match": geometry,
            "screen_status": "UNSCREENED",
        }
    )
    return row


def _direct(study_id: str, doi: str, direction: str) -> dict[str, str]:
    row = {field: "" for field in DIRECT_FIELDS}
    row.update(
        {
            "study_id": study_id,
            "year": "2020",
            "doi": doi,
            "direction": direction,
            "network_k_eligible": "NO",
            "reason_not_k": "not standardized network",
        }
    )
    return row


def test_initializer_retains_every_frame_record_and_only_preseeds_known_dois(
    tmp_path: Path,
) -> None:
    frame = tmp_path / "frame.csv"
    direct = tmp_path / "direct.csv"
    _write(
        frame,
        FRAME_FIELDS,
        [
            _frame("bib_a", "10.1000/a", "true"),
            _frame("bib_b", "10.1000/b", "false"),
            _frame("bib_c", "", "true"),
        ],
    )
    _write(
        direct,
        DIRECT_FIELDS,
        [
            _direct("KnownA", "https://doi.org/10.1000/A", "NULL"),
            _direct("NotInFrame", "10.1000/z", "POSITIVE"),
        ],
    )

    rows = initialize(frame, direct)
    assert len(rows) == 3
    assert set(rows[0]) == set(FIELDS)

    known = next(row for row in rows if row["candidate_id"] == "bib_a")
    assert known["known_direct_study_id"] == "KnownA"
    assert known["screen_status"] == "ELIGIBLE_PREVIOUSLY_ADJUDICATED"
    assert known["eligibility_decision"] == "YES"
    assert known["direction"] == "NULL"

    unknown = next(row for row in rows if row["candidate_id"] == "bib_b")
    assert unknown["screen_status"] == "UNSCREENED"
    assert unknown["eligibility_decision"] == ""
    assert unknown["direction"] == ""

    no_doi = next(row for row in rows if row["candidate_id"] == "bib_c")
    assert no_doi["screen_status"] == "UNSCREENED"
