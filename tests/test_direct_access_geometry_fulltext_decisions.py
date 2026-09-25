from __future__ import annotations

import csv
from pathlib import Path

import pytest

from scripts.build_direct_access_geometry_fulltext_decision_template import (
    FIELDS,
    build,
    write,
)
from scripts.validate_direct_access_geometry_fulltext_decisions import validate


SCREEN_FIELDS = (
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


def _write(path: Path, fields: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _screen(tmp_path: Path) -> Path:
    path = tmp_path / "screen.csv"
    rows = [
        {
            "frame_id": "known",
            "doi": "10.1/known",
            "title": "Known",
            "year": "2010",
            "source_dbs": "OpenAlex",
            "query_ids": "Q1",
            "screen_status": "KNOWN_DIRECT_CORPUS_MATCH",
            "known_study_id": "Known_Program",
            "known_direction": "POSITIVE",
            "eligibility_status": "KNOWN_ELIGIBLE_DIRECT",
            "direction": "POSITIVE",
            "screening_notes": "matched_by=DOI",
        },
        {
            "frame_id": "new1",
            "doi": "10.1/new1",
            "title": "New one",
            "year": "2020",
            "source_dbs": "OpenAlex",
            "query_ids": "Q5",
            "screen_status": "PENDING_FULLTEXT_ELIGIBILITY",
            "known_study_id": "",
            "known_direction": "",
            "eligibility_status": "PENDING",
            "direction": "",
            "screening_notes": "",
        },
        {
            "frame_id": "new2",
            "doi": "",
            "title": "New two",
            "year": "2021",
            "source_dbs": "OpenAlex",
            "query_ids": "Q7",
            "screen_status": "PENDING_FULLTEXT_ELIGIBILITY",
            "known_study_id": "",
            "known_direction": "",
            "eligibility_status": "PENDING",
            "direction": "",
            "screening_notes": "",
        },
    ]
    _write(path, SCREEN_FIELDS, rows)
    return path


def test_template_prefills_known_and_leaves_new_records_pending(tmp_path: Path) -> None:
    screen = _screen(tmp_path)
    rows = build(screen)
    by_id = {row["frame_id"]: row for row in rows}

    assert by_id["known"]["decision_status"] == "ELIGIBLE_DIRECT"
    assert by_id["known"]["biological_program_id"] == "Known_Program"
    assert by_id["known"]["direction"] == "POSITIVE"
    assert by_id["known"]["decision_basis"] == "PREEXISTING_24_PROGRAM_DIRECT_CORPUS"

    assert by_id["new1"]["decision_status"] == "PENDING_FULLTEXT"
    assert by_id["new1"]["direction"] == ""
    assert by_id["new1"]["decision_basis"] == ""


def test_validator_accepts_complete_screen_and_keeps_recurrence_closed(tmp_path: Path) -> None:
    screen = _screen(tmp_path)
    decision_path = tmp_path / "decisions.csv"
    rows = build(screen)

    for row in rows:
        if row["frame_id"] == "new1":
            row.update(
                {
                    "decision_status": "ELIGIBLE_DIRECT",
                    "biological_program_id": "New_Program",
                    "direction": "NULL",
                    "decision_basis": "PRIMARY_FULLTEXT_GEOMETRY_AND_ROUTE_TEST",
                    "source_identifier": "10.1/new1",
                    "notes": "adjudicated",
                }
            )
        elif row["frame_id"] == "new2":
            row.update(
                {
                    "decision_status": "INELIGIBLE_NO_ROUTE_OUTCOME",
                    "decision_basis": "PRIMARY_FULLTEXT_NO_ROUTE_RESOLVED_ROBBERY",
                    "source_identifier": "title-year:New two|2021",
                    "notes": "adjudicated",
                }
            )
    write(rows, decision_path)

    result = validate(screen, decision_path, require_complete=True)
    assert result["status"] == "FULLTEXT_ELIGIBILITY_SCREEN_COMPLETE"
    assert result["frame_records"] == 3
    assert result["pending_records"] == 0
    assert result["eligible_direct_programs_in_frame"] == 2
    assert result["eligible_direction_counts"] == {
        "POSITIVE": 1,
        "NULL": 1,
        "OPPOSITE": 0,
        "MIXED": 0,
    }
    assert result["ineligible_records"] == 1
    assert result["formal_recurrence_result_open"] is False
    assert result["primary_standardized_network_k"] == 2
    assert result["next_gate"] == "FORMAL_RECURRENCE_SUMMARY"


def test_require_complete_rejects_pending_records(tmp_path: Path) -> None:
    screen = _screen(tmp_path)
    decision_path = tmp_path / "decisions.csv"
    write(build(screen), decision_path)

    with pytest.raises(ValueError, match="FULLTEXT_VALIDATE_PENDING_RECORDS"):
        validate(screen, decision_path, require_complete=True)


def test_known_direct_decision_is_immutable(tmp_path: Path) -> None:
    screen = _screen(tmp_path)
    decision_path = tmp_path / "decisions.csv"
    rows = build(screen)
    rows[0]["direction"] = "NULL"
    write(rows, decision_path)

    with pytest.raises(ValueError, match="FULLTEXT_VALIDATE_KNOWN_DIRECTION_CHANGED"):
        validate(screen, decision_path)


def test_ineligible_record_cannot_carry_direction(tmp_path: Path) -> None:
    screen = _screen(tmp_path)
    decision_path = tmp_path / "decisions.csv"
    rows = build(screen)
    target = next(row for row in rows if row["frame_id"] == "new1")
    target.update(
        {
            "decision_status": "INELIGIBLE_NO_ROUTE_OUTCOME",
            "direction": "POSITIVE",
            "decision_basis": "PRIMARY_FULLTEXT_NO_ROUTE_OUTCOME",
            "source_identifier": "10.1/new1",
        }
    )
    write(rows, decision_path)

    with pytest.raises(ValueError, match="FULLTEXT_VALIDATE_INELIGIBLE_HAS_EFFECT_DATA"):
        validate(screen, decision_path)


def test_duplicate_target_must_be_an_eligible_program(tmp_path: Path) -> None:
    screen = _screen(tmp_path)
    decision_path = tmp_path / "decisions.csv"
    rows = build(screen)
    target = next(row for row in rows if row["frame_id"] == "new1")
    target.update(
        {
            "decision_status": "DUPLICATE_BIOLOGICAL_PROGRAM",
            "duplicate_of_program_id": "Missing_Program",
            "decision_basis": "PRIMARY_FULLTEXT_DUPLICATE_REPORT",
            "source_identifier": "10.1/new1",
        }
    )
    other = next(row for row in rows if row["frame_id"] == "new2")
    other.update(
        {
            "decision_status": "INELIGIBLE_NO_ROUTE_OUTCOME",
            "decision_basis": "PRIMARY_FULLTEXT_NO_ROUTE_OUTCOME",
            "source_identifier": "title-year:New two|2021",
        }
    )
    write(rows, decision_path)

    with pytest.raises(ValueError, match="FULLTEXT_VALIDATE_DUPLICATE_TARGET_NOT_ELIGIBLE"):
        validate(screen, decision_path, require_complete=True)
