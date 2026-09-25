from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from scripts.build_direct_access_geometry_fulltext_decision_template import (
    SCREEN_REQUIRED,
    build,
    write,
)
from scripts.summarize_direct_access_geometry_formal_recurrence import summarize


HIST_FIELDS = (
    "study_id",
    "screen_status",
    "access_predictor",
    "robbery_outcome",
    "eligible",
    "direction",
    "source_identifier",
    "notes",
)


def _write(path: Path, fields, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _fixture(tmp_path: Path):
    directions = (
        [("P%02d" % i, "POSITIVE") for i in range(1, 17)]
        + [("N%02d" % i, "NULL") for i in range(1, 6)]
        + [("O01", "OPPOSITE")]
        + [("M01", "MIXED"), ("M02", "MIXED")]
    )
    assert len(directions) == 24

    screen_rows = []
    for idx, (program, direction) in enumerate(directions, start=1):
        screen_rows.append(
            {
                "frame_id": f"known_{idx:02d}",
                "doi": f"10.1000/known{idx}",
                "title": f"Known {idx}",
                "year": str(2000 + (idx % 20)),
                "source_dbs": "Scopus",
                "query_ids": "Q1",
                "screen_status": "KNOWN_DIRECT_CORPUS_MATCH",
                "known_study_id": program,
                "known_direction": direction,
                "eligibility_status": "KNOWN_ELIGIBLE_DIRECT",
                "direction": direction,
                "screening_notes": "matched_by=DOI",
            }
        )
    screen_rows.extend(
        [
            {
                "frame_id": "new_eligible",
                "doi": "10.1000/new",
                "title": "New eligible",
                "year": "2025",
                "source_dbs": "Scopus",
                "query_ids": "Q5",
                "screen_status": "PENDING_FULLTEXT_ELIGIBILITY",
                "known_study_id": "",
                "known_direction": "",
                "eligibility_status": "PENDING",
                "direction": "",
                "screening_notes": "",
            },
            {
                "frame_id": "new_ineligible",
                "doi": "10.1000/no",
                "title": "New ineligible",
                "year": "2024",
                "source_dbs": "Scopus",
                "query_ids": "Q7",
                "screen_status": "PENDING_FULLTEXT_ELIGIBILITY",
                "known_study_id": "",
                "known_direction": "",
                "eligibility_status": "PENDING",
                "direction": "",
                "screening_notes": "",
            },
        ]
    )
    screen = tmp_path / "screen.csv"
    _write(screen, SCREEN_REQUIRED, screen_rows)

    decisions = build(screen)
    for row in decisions:
        if row["frame_id"] == "new_eligible":
            row.update(
                {
                    "decision_status": "ELIGIBLE_DIRECT",
                    "biological_program_id": "NEW_NULL",
                    "direction": "NULL",
                    "decision_basis": "PRIMARY_FULLTEXT_GEOMETRY_ROUTE_TEST",
                    "source_identifier": "10.1000/new",
                }
            )
        elif row["frame_id"] == "new_ineligible":
            row.update(
                {
                    "decision_status": "INELIGIBLE_NO_ROUTE_OUTCOME",
                    "decision_basis": "PRIMARY_FULLTEXT_NO_ROUTE_OUTCOME",
                    "source_identifier": "10.1000/no",
                }
            )
    decision_path = tmp_path / "decisions.csv"
    write(decisions, decision_path)

    bootstrap = tmp_path / "bootstrap.json"
    bootstrap.write_text(
        json.dumps(
            {
                "schema": "BITA_DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_SCREEN_BOOTSTRAP_V1",
                "status": "FRAME_SCREEN_BOOTSTRAPPED_KNOWN_CORPUS_RECALL_COMPLETE",
                "known_direct_corpus_programs": 24,
                "known_programs_matched": 24,
                "known_programs_unmatched": [],
                "unknown_record_direction_coded": False,
                "formal_recurrence_result_open": False,
            }
        ),
        encoding="utf-8",
    )

    historical_rows = []
    for i in range(50):
        historical_rows.append(
            {
                "study_id": f"I{i:02d}",
                "screen_status": "INELIGIBLE_NO_GEOMETRY_TEST",
                "access_predictor": "",
                "robbery_outcome": "",
                "eligible": "NO",
                "direction": "",
                "source_identifier": f"source-{i}",
                "notes": "no geometry test",
            }
        )
    for sid, direction in (
        ("H_POS_1", "POSITIVE"),
        ("H_POS_2", "POSITIVE"),
        ("H_NULL", "NULL"),
        ("H_MIXED", "MIXED"),
    ):
        historical_rows.append(
            {
                "study_id": sid,
                "screen_status": "ELIGIBLE_DIRECTION_EXPOSED",
                "access_predictor": "geometry",
                "robbery_outcome": "robbery",
                "eligible": "YES",
                "direction": direction,
                "source_identifier": sid,
                "notes": "eligible",
            }
        )
    for sid in ("Varma&Sinu2019", "Zhangetal2009a"):
        historical_rows.append(
            {
                "study_id": sid,
                "screen_status": "PROVENANCE_CONFLICT_ELIGIBILITY_STABLE_INELIGIBLE",
                "access_predictor": "",
                "robbery_outcome": "",
                "eligible": "NO",
                "direction": "",
                "source_identifier": "",
                "notes": "eligibility stably no",
            }
        )
    historical = tmp_path / "historical.csv"
    _write(historical, HIST_FIELDS, historical_rows)

    crosswalk = tmp_path / "crosswalk.csv"
    _write(
        crosswalk,
        ("direct_study_id", "leal2025_frame_status", "leal2025_study_id", "reason"),
        [
            {
                "direct_study_id": "P01",
                "leal2025_frame_status": "IN_FRAME",
                "leal2025_study_id": "H_POS_1",
                "reason": "historical",
            },
            {
                "direct_study_id": "P02",
                "leal2025_frame_status": "IN_FRAME",
                "leal2025_study_id": "H_POS_2",
                "reason": "historical",
            },
            {
                "direct_study_id": "N01",
                "leal2025_frame_status": "IN_FRAME",
                "leal2025_study_id": "H_NULL",
                "reason": "historical",
            },
            {
                "direct_study_id": "M01",
                "leal2025_frame_status": "IN_FRAME",
                "leal2025_study_id": "H_MIXED",
                "reason": "historical",
            },
        ],
    )
    return screen, decision_path, bootstrap, historical, crosswalk


def test_formal_summary_reports_finite_frame_counts_without_p_value(tmp_path: Path) -> None:
    screen, decisions, bootstrap, historical, crosswalk = _fixture(tmp_path)
    result = summarize(
        screen,
        decisions,
        bootstrap,
        historical_screen_path=historical,
        crosswalk_path=crosswalk,
    )

    assert result["status"] == "FORMAL_FINITE_FRAME_DIRECTION_SUMMARY_OPEN"
    assert result["frame_records"] == 26
    assert result["source_db"] == "Scopus"
    assert result["eligible_direct_programs"] == 25
    assert result["direction_counts"] == {
        "POSITIVE": 16,
        "NULL": 6,
        "OPPOSITE": 1,
        "MIXED": 2,
    }
    assert result["preexisting_direct_programs_recovered"] == 24
    assert result["new_eligible_programs_from_formal_frame"] == 1
    assert result["new_eligible_direction_counts"] == {
        "POSITIVE": 0,
        "NULL": 1,
        "OPPOSITE": 0,
        "MIXED": 0,
    }
    assert result["ineligible_bibliographic_records"] == 1
    assert result["historical_direct_eligible_programs"] == 4
    assert result["historical_anchor_double_counted"] is False
    assert result["formal_recurrence_descriptive_summary_open"] is True
    assert result["formal_direction_p_value_computed"] is False
    assert result["pooled_effect_computed"] is False
    assert result["natural_prevalence_estimated"] is False
    assert result["primary_standardized_network_k"] == 2


def test_formal_summary_fails_if_known_24_recall_is_incomplete(tmp_path: Path) -> None:
    screen, decisions, bootstrap, historical, crosswalk = _fixture(tmp_path)
    payload = json.loads(bootstrap.read_text(encoding="utf-8"))
    payload["status"] = "FRAME_SCREEN_BOOTSTRAPPED_KNOWN_CORPUS_RECALL_INCOMPLETE"
    payload["known_programs_matched"] = 23
    payload["known_programs_unmatched"] = ["P16"]
    bootstrap.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="FORMAL_SUMMARY_KNOWN_CORPUS_RECALL_INCOMPLETE"):
        summarize(
            screen,
            decisions,
            bootstrap,
            historical_screen_path=historical,
            crosswalk_path=crosswalk,
        )


def test_formal_summary_fails_if_historical_anchor_missing_from_frame(tmp_path: Path) -> None:
    screen, decisions, bootstrap, historical, crosswalk = _fixture(tmp_path)
    rows = list(csv.DictReader(crosswalk.open(encoding="utf-8")))
    rows[0]["direct_study_id"] = "NOT_PRESENT"
    _write(
        crosswalk,
        ("direct_study_id", "leal2025_frame_status", "leal2025_study_id", "reason"),
        rows,
    )

    with pytest.raises(ValueError, match="FORMAL_SUMMARY_HISTORICAL_PROGRAM_NOT_IN_ELIGIBLE_FRAME"):
        summarize(
            screen,
            decisions,
            bootstrap,
            historical_screen_path=historical,
            crosswalk_path=crosswalk,
        )


def test_formal_summary_fails_if_source_databases_are_mixed(tmp_path: Path) -> None:
    screen, decisions, bootstrap, historical, crosswalk = _fixture(tmp_path)
    rows = list(csv.DictReader(decisions.open(encoding="utf-8")))
    rows[-1]["source_dbs"] = "WebOfScience"
    write(rows, decisions)

    with pytest.raises(ValueError, match="FULLTEXT_VALIDATE_IMMUTABLE_METADATA_CHANGED"):
        summarize(
            screen,
            decisions,
            bootstrap,
            historical_screen_path=historical,
            crosswalk_path=crosswalk,
        )
