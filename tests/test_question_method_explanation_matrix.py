from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "empirical" / "identification_design" / "QUESTION_METHOD_EXPLANATION_MATRIX_V1.csv"
READOUT = ROOT / "docs" / "QUESTION_METHOD_EXPLANATION_MATRIX.md"
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_IDENTIFICATION_DESIGN.md"


def _rows() -> list[dict[str, str]]:
    with MATRIX.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_matrix_covers_the_full_explanation_ladder() -> None:
    rows = _rows()
    assert [row["level_id"] for row in rows] == [f"L{i}" for i in range(1, 9)]
    assert all(row["scientific_question"] for row in rows)
    assert all(row["method"] for row in rows)
    assert all(row["minimum_information"] for row in rows)
    assert all(row["does_not_explain"] for row in rows)
    assert all(row["next_valid_gate"] for row in rows)


def test_current_evidence_does_not_claim_full_mechanism_recovery() -> None:
    rows = {row["level_id"]: row for row in _rows()}
    assert rows["L1"]["current_status"] == "ACHIEVED_RECURRENCE_ONLY"
    assert rows["L2"]["current_status"] == "DIRECT_FACTORIAL_SIGN_POSITIVE_FORMAL_UNCERTAINTY_UNRESOLVED"
    assert rows["L5"]["current_status"] == "ACHIEVED_SCREENED_FRONTIER"
    assert rows["L6"]["current_status"] == "NOT_ACHIEVED_ZERO_OF_SIXTEEN"
    assert rows["L8"]["current_status"] == "NOT_ACHIEVED_ZERO_STRICT"
    assert "source-design interval" in rows["L2"]["does_not_explain"]
    assert "unidentified, not zero" in rows["L8"]["does_not_explain"]


def test_human_readout_and_main_separate_escape_sign_from_mechanism() -> None:
    readout = READOUT.read_text(encoding="utf-8")
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    assert "What BITA can explain, by method" in readout
    assert "Full channel point identification is therefore **not** a prerequisite" in readout
    assert "positive functional escape" in readout
    assert "not cue privatization" in readout
    assert "which method explains which part of the question" in manuscript
    assert "It does not reach full channel allocation in any screened system" in manuscript
    assert "a valid positive total interval would decide the escape sign" in manuscript
    assert "informational escape" in manuscript
    assert "functional escape" in manuscript


def test_stale_all_channels_first_escape_claim_is_absent() -> None:
    readout = READOUT.read_text(encoding="utf-8").lower()
    manuscript = MANUSCRIPT.read_text(encoding="utf-8").lower()
    stale = (
        "the full inequality remains unevaluable because no complete system identifies all three terms",
        "the complete escape inequality remains a generated test",
    )
    for phrase in stale:
        assert phrase not in readout
        assert phrase not in manuscript
