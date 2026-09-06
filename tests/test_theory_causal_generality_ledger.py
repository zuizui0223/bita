import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "THEORY_CAUSAL_GENERALITY_LEDGER_V1.csv"


def _rows():
    with LEDGER.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_stage_order_and_layer_separation():
    rows = _rows()
    assert [row["stage"] for row in rows] == [
        "T1", "T2", "T3", "T4", "T5", "C0", "C1", "C2", "C3", "C4", "C5", "G0", "G1", "G2", "G3"
    ]
    assert {row["layer"] for row in rows[:5]} == {"theory"}
    assert {row["layer"] for row in rows[5:11]} == {"causal"}
    assert {row["layer"] for row in rows[11:]} == {"generality"}


def test_fragmented_literature_is_not_promoted_to_complete_replication():
    by_stage = {row["stage"]: row for row in _rows()}
    assert "INCOMPLETE" in by_stage["G1"]["status"]
    assert "NOT_YET_EXECUTED" in by_stage["G0"]["status"]
    assert "RARELY_IDENTIFIED" in by_stage["C5"]["status"]
    assert by_stage["T5"]["status"] == "NET_GAP_IDENTIFIES_DIFFERENCE_NOT_COMPONENTS"


def test_payoff_invasion_is_not_a_bita_promotion_gate():
    text = (ROOT / "docs" / "THEORY_CAUSAL_GENERALITY_RECOVERY_V1.md").read_text(encoding="utf-8")
    assert "PAYOFF invasion" in text
    assert "not BITA promotion criteria" in text
