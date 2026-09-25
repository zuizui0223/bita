from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import pytest

from scripts.validate_direct_access_geometry_biblio_frame import validate


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
    "sentinel_query_match",
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


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _frame_row(doi: str) -> dict[str, str]:
    row = {field: "" for field in FRAME_FIELDS}
    row.update(
        {
            "candidate_id": "bib_x",
            "identity_key": f"doi:{doi}",
            "doi": doi,
            "title": "Nectar robbing and corolla morphology",
            "publication_year": "2020",
            "source_providers": "crossref",
            "provider_ids": "crossref:x",
            "matched_query_ids": "Q01",
            "best_provider_rank": "1",
            "larceny_text_match": "true",
            "geometry_text_match": "true",
            "sentinel_query_match": "false",
            "screen_status": "UNSCREENED",
        }
    )
    return row


def _direct_row(study_id: str, doi: str, direction: str) -> dict[str, str]:
    row = {field: "" for field in DIRECT_FIELDS}
    row.update(
        {
            "study_id": study_id,
            "year": "2020",
            "doi": doi,
            "direction": direction,
            "network_k_eligible": "NO",
            "reason_not_k": "not a standardized network",
        }
    )
    return row


def test_known_doi_coverage_passes_when_all_known_direct_dois_are_present(
    tmp_path: Path,
) -> None:
    frame = tmp_path / "frame.csv"
    direct = tmp_path / "direct.csv"
    receipt = tmp_path / "receipt.json"

    _write_csv(frame, FRAME_FIELDS, [_frame_row("10.1000/a"), _frame_row("10.1000/b")])
    _write_csv(
        direct,
        DIRECT_FIELDS,
        [
            _direct_row("A", "10.1000/a", "POSITIVE"),
            _direct_row("B", "10.1000/b", "NULL"),
            _direct_row("C", "", "MIXED"),
        ],
    )
    receipt.write_text(
        json.dumps(
            {
                "frame_sha256": hashlib.sha256(frame.read_bytes()).hexdigest(),
                "deduplicated_candidates": 2,
            }
        ),
        encoding="utf-8",
    )

    result = validate(frame, receipt, direct)
    assert result["known_direct_programs"] == 3
    assert result["known_direct_programs_with_doi"] == 2
    assert result["known_doi_covered"] == 2
    assert result["known_doi_missing"] == 0


def test_known_doi_coverage_fails_closed_on_missing_program(tmp_path: Path) -> None:
    frame = tmp_path / "frame.csv"
    direct = tmp_path / "direct.csv"
    receipt = tmp_path / "receipt.json"

    _write_csv(frame, FRAME_FIELDS, [_frame_row("10.1000/a")])
    _write_csv(
        direct,
        DIRECT_FIELDS,
        [
            _direct_row("A", "10.1000/a", "POSITIVE"),
            _direct_row("B", "10.1000/b", "OPPOSITE"),
        ],
    )
    receipt.write_text(
        json.dumps(
            {
                "frame_sha256": hashlib.sha256(frame.read_bytes()).hexdigest(),
                "deduplicated_candidates": 1,
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="BIBLIO_FRAME_MISSES_KNOWN_DIRECT_PROGRAMS"):
        validate(frame, receipt, direct)
