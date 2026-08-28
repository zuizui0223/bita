from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "empirical" / "identification_design" / "DEFENCE_ESCAPE_ROUTE_HYPOTHESIS_RECOVERY_V1.csv"
READOUT = ROOT / "docs" / "DEFENCE_ESCAPE_ROUTE_HYPOTHESIS_RECOVERY.md"
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_IDENTIFICATION_DESIGN.md"
PRIMARY_AUDIT = ROOT / "docs" / "BITA_DEFENCE_ESCAPE_ROUTE_PRIMARY_SOURCE_AUDIT_V1.md"
PUBLICATION_LEDGER = ROOT / "docs" / "PUBLICATION_MATERIAL_RECOVERY_LEDGER.md"


def _rows() -> dict[str, dict[str, str]]:
    with LEDGER.open(encoding="utf-8", newline="") as handle:
        return {row["hypothesis_id"]: row for row in csv.DictReader(handle)}


def test_escape_route_ledger_is_complete_and_fail_closed() -> None:
    rows = _rows()
    assert list(rows) == [f"ER{i}" for i in range(1, 11)]
    assert all(row["positive_answer"] for row in rows.values())
    assert all(row["claim_ceiling"] for row in rows.values())
    assert all(row["next_valid_gate"] for row in rows.values())
    assert rows["ER7"]["current_status"] == "NOT_ACHIEVED_ZERO_OF_SIXTEEN"
    assert rows["ER8"]["current_status"] == "NOT_ACHIEVED_ZERO_STRICT"
    assert rows["ER9"]["current_status"] == "NOT_EVALUABLE_CURRENT_EVIDENCE"
    assert rows["ER10"]["current_status"] == "ACHIEVED_METHOD_RESULT"


def test_readout_states_positive_recovery_without_promoting_full_escape() -> None:
    text = READOUT.read_text(encoding="utf-8")
    assert "What the ecological evidence has positively answered" in text
    assert "constituent mechanisms and the switching rule" in text
    assert "rho_delta > iota_delta + kappa_delta" in text
    assert "not currently evaluable for a complete observed system" in text
    assert "zero recovered assays does not imply zero cost" in text


def test_main_manuscript_frames_D_as_the_second_trait_escape_hypothesis() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    assert "a distinct defence trait is a candidate escape route" in text
    assert "a two-trait allocation hypothesis" in text
    assert "answers part of the escape-route question positively" in text
    assert "the complete escape inequality remains a generated test" in text


def test_primary_audit_and_publication_ledger_preserve_directness_boundaries() -> None:
    audit = PRIMARY_AUDIT.read_text(encoding="utf-8")
    ledger = PUBLICATION_LEDGER.read_text(encoding="utf-8")
    assert "direct rho_delta:                    0 studies" in audit
    assert "full point identification:          0 studies" in audit
    assert "plausibility" in audit and "identification" in audit
    assert "six high-information systems source-checked" in ledger
    assert "Targeted audit is not prevalence" in ledger
