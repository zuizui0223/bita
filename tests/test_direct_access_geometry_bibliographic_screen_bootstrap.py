from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from scripts.bootstrap_direct_access_geometry_bibliographic_screen import (
    FRAME_FIELDS,
    bootstrap,
)


def _write_csv(path: Path, fields: tuple[str, ...] | list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _fixture(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    frame = tmp_path / "frame.csv"
    frame_rows = [
        {
            "frame_id": "bib_doi",
            "dedupe_key": "doi:10.1000/known",
            "doi": "10.1000/known",
            "title": "Known DOI paper",
            "year": "2010",
            "authors": "A",
            "publication": "Journal",
            "source_dbs": "OpenAlex",
            "query_ids": "Q1|Q3",
            "source_record_ids": "OpenAlex:W1",
            "source_urls": "",
            "raw_rows_collapsed": "2",
        },
        {
            "frame_id": "bib_alias",
            "dedupe_key": "title-year:known title alias|2006",
            "doi": "",
            "title": "Known title alias",
            "year": "2006",
            "authors": "B",
            "publication": "Journal",
            "source_dbs": "OpenAlex",
            "query_ids": "Q7",
            "source_record_ids": "OpenAlex:W2",
            "source_urls": "",
            "raw_rows_collapsed": "1",
        },
        {
            "frame_id": "bib_unknown",
            "dedupe_key": "doi:10.1000/unknown",
            "doi": "10.1000/unknown",
            "title": "Unknown paper",
            "year": "2020",
            "authors": "C",
            "publication": "Journal",
            "source_dbs": "OpenAlex",
            "query_ids": "Q5",
            "source_record_ids": "OpenAlex:W3",
            "source_urls": "",
            "raw_rows_collapsed": "1",
        },
    ]
    _write_csv(frame, FRAME_FIELDS, frame_rows)

    receipt = tmp_path / "frame_receipt.json"
    receipt.write_text(
        json.dumps(
            {
                "schema": "BITA_DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_FRAME_V1",
                "status": "OUTCOME_BLIND_FRAME_FROZEN",
                "unique_bibliographic_records": 3,
                "formal_recurrence_result_open": False,
            }
        ),
        encoding="utf-8",
    )

    corpus = tmp_path / "corpus.csv"
    corpus_fields = [
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
    _write_csv(
        corpus,
        corpus_fields,
        [
            {
                "study_id": "Known_DOI",
                "year": "2010",
                "doi": "https://doi.org/10.1000/KNOWN",
                "fauna": "Insecta",
                "plant_scope": "x",
                "study_scale": "x",
                "access_predictor": "x",
                "robbery_outcome": "x",
                "direction": "POSITIVE",
                "effect_detail": "x",
                "network_k_eligible": "NO",
                "reason_not_k": "x",
                "source_role": "DIRECT_SUPPORT",
                "notes": "x",
            },
            {
                "study_id": "Known_Alias",
                "year": "2006",
                "doi": "",
                "fauna": "Insecta",
                "plant_scope": "x",
                "study_scale": "x",
                "access_predictor": "x",
                "robbery_outcome": "x",
                "direction": "NULL",
                "effect_detail": "x",
                "network_k_eligible": "NO",
                "reason_not_k": "x",
                "source_role": "DIRECT_NULL",
                "notes": "x",
            },
        ],
    )

    aliases = tmp_path / "aliases.csv"
    _write_csv(
        aliases,
        ["study_id", "year", "title_alias", "source_note"],
        [
            {
                "study_id": "Known_Alias",
                "year": "2006",
                "title_alias": "Known title alias",
                "source_note": "fixture",
            }
        ],
    )
    return frame, receipt, corpus, aliases


def test_bootstrap_matches_known_records_and_leaves_unknown_direction_blank(tmp_path: Path) -> None:
    frame, receipt, corpus, aliases = _fixture(tmp_path)
    rows, result = bootstrap(
        frame,
        receipt,
        corpus_path=corpus,
        alias_path=aliases,
    )

    by_id = {row["frame_id"]: row for row in rows}
    assert by_id["bib_doi"]["screen_status"] == "KNOWN_DIRECT_CORPUS_MATCH"
    assert by_id["bib_doi"]["known_study_id"] == "Known_DOI"
    assert by_id["bib_doi"]["direction"] == "POSITIVE"
    assert by_id["bib_doi"]["screening_notes"] == "matched_by=DOI"

    assert by_id["bib_alias"]["screen_status"] == "KNOWN_DIRECT_CORPUS_MATCH"
    assert by_id["bib_alias"]["known_study_id"] == "Known_Alias"
    assert by_id["bib_alias"]["direction"] == "NULL"
    assert by_id["bib_alias"]["screening_notes"] == "matched_by=TITLE_YEAR_ALIAS"

    assert by_id["bib_unknown"]["screen_status"] == "PENDING_FULLTEXT_ELIGIBILITY"
    assert by_id["bib_unknown"]["known_study_id"] == ""
    assert by_id["bib_unknown"]["direction"] == ""
    assert by_id["bib_unknown"]["eligibility_status"] == "PENDING"

    assert result["known_programs_matched"] == 2
    assert result["known_programs_unmatched"] == []
    assert result["pending_fulltext_records"] == 1
    assert result["unknown_record_direction_coded"] is False
    assert result["formal_recurrence_result_open"] is False
    assert result["primary_standardized_network_k"] == 2
    assert result["status"] == "FRAME_SCREEN_BOOTSTRAPPED_KNOWN_CORPUS_RECALL_COMPLETE"


def test_bootstrap_reports_known_programs_missing_from_frozen_frame(tmp_path: Path) -> None:
    frame, receipt, corpus, aliases = _fixture(tmp_path)
    rows = list(csv.DictReader(frame.open(encoding="utf-8")))
    rows = [row for row in rows if row["frame_id"] != "bib_alias"]
    _write_csv(frame, FRAME_FIELDS, rows)
    receipt.write_text(
        json.dumps(
            {
                "schema": "BITA_DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_FRAME_V1",
                "status": "OUTCOME_BLIND_FRAME_FROZEN",
                "unique_bibliographic_records": 2,
                "formal_recurrence_result_open": False,
            }
        ),
        encoding="utf-8",
    )

    _, result = bootstrap(
        frame,
        receipt,
        corpus_path=corpus,
        alias_path=aliases,
    )
    assert result["known_programs_unmatched"] == ["Known_Alias"]
    assert result["status"] == "FRAME_SCREEN_BOOTSTRAPPED_KNOWN_CORPUS_RECALL_INCOMPLETE"


def test_doiless_direct_programs_must_have_title_aliases(tmp_path: Path) -> None:
    frame, receipt, corpus, aliases = _fixture(tmp_path)
    aliases.write_text("study_id,year,title_alias,source_note\n", encoding="utf-8")

    with pytest.raises(ValueError, match="BIB_SCREEN_DOILESS_ALIAS_COVERAGE_MISMATCH"):
        bootstrap(
            frame,
            receipt,
            corpus_path=corpus,
            alias_path=aliases,
        )


def test_bootstrap_rejects_nonfrozen_frame_receipt(tmp_path: Path) -> None:
    frame, receipt, corpus, aliases = _fixture(tmp_path)
    receipt.write_text(
        json.dumps(
            {
                "schema": "BITA_DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_FRAME_V1",
                "status": "DRAFT",
                "unique_bibliographic_records": 3,
                "formal_recurrence_result_open": False,
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="BIB_SCREEN_FRAME_NOT_FROZEN"):
        bootstrap(
            frame,
            receipt,
            corpus_path=corpus,
            alias_path=aliases,
        )


def test_bootstrap_accounts_for_verified_provider_absence(tmp_path: Path) -> None:
    frame, receipt, corpus, aliases = _fixture(tmp_path)
    rows = list(csv.DictReader(frame.open(encoding="utf-8")))
    rows = [row for row in rows if row["frame_id"] != "bib_alias"]
    _write_csv(frame, FRAME_FIELDS, rows)
    receipt.write_text(
        json.dumps(
            {
                "schema": "BITA_DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_FRAME_V1",
                "status": "OUTCOME_BLIND_FRAME_FROZEN",
                "unique_bibliographic_records": 2,
                "formal_recurrence_result_open": False,
            }
        ),
        encoding="utf-8",
    )

    exceptions = tmp_path / "provider_exceptions.csv"
    _write_csv(
        exceptions,
        [
            "study_id",
            "source_db",
            "provider_check",
            "provider_result_count",
            "external_verification",
            "adjudication",
            "notes",
        ],
        [
            {
                "study_id": "Known_Alias",
                "source_db": "OpenAlex",
                "provider_check": "exact_title_search",
                "provider_result_count": "0",
                "external_verification": "publisher",
                "adjudication": "VERIFIED_PROVIDER_ABSENCE",
                "notes": "fixture",
            }
        ],
    )

    _, result = bootstrap(
        frame,
        receipt,
        corpus_path=corpus,
        alias_path=aliases,
        provider_coverage_exceptions_path=exceptions,
    )

    assert result["known_programs_matched"] == 1
    assert result["known_programs_unmatched"] == ["Known_Alias"]
    assert result["known_programs_provider_absent"] == ["Known_Alias"]
    assert result["known_programs_unresolved"] == []
    assert result["provider_coverage_exceptions_applied"] is True
    assert result["provider_coverage_exception_sha256"]
    assert (
        result["status"]
        == "FRAME_SCREEN_BOOTSTRAPPED_KNOWN_CORPUS_RECALL_ACCOUNTED_PROVIDER_ABSENCE"
    )


def test_bootstrap_rejects_stale_provider_absence_if_study_is_recovered(tmp_path: Path) -> None:
    frame, receipt, corpus, aliases = _fixture(tmp_path)
    exceptions = tmp_path / "provider_exceptions.csv"
    _write_csv(
        exceptions,
        [
            "study_id",
            "source_db",
            "provider_check",
            "provider_result_count",
            "external_verification",
            "adjudication",
            "notes",
        ],
        [
            {
                "study_id": "Known_Alias",
                "source_db": "OpenAlex",
                "provider_check": "exact_title_search",
                "provider_result_count": "0",
                "external_verification": "publisher",
                "adjudication": "VERIFIED_PROVIDER_ABSENCE",
                "notes": "fixture",
            }
        ],
    )

    with pytest.raises(
        ValueError,
        match="BIB_SCREEN_PROVIDER_EXCEPTION_STUDY_WAS_RECOVERED",
    ):
        bootstrap(
            frame,
            receipt,
            corpus_path=corpus,
            alias_path=aliases,
            provider_coverage_exceptions_path=exceptions,
        )
