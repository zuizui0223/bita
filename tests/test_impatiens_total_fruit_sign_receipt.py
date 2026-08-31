from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "empirical" / "identification_design" / "IMPATIENS_TOTAL_FRUIT_SIGN_RECEIPT_V1.json"
READOUT = ROOT / "empirical" / "identification_design" / "IMPATIENS_2018_IDENTIFICATION_RETROFIT_V2.md"


def test_total_fruit_sign_receipt_remains_unresolved() -> None:
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert receipt["endpoint"] == "Total_Fruits_Per_Day"
    assert receipt["n_complete"] == 170
    assert receipt["ci95_lower"] < 0 < receipt["ci95_upper"]
    assert receipt["sign_status"] == "CROSSES_ZERO"
    assert receipt["causal_status"] == "OBSERVATIONAL_A_D_NOT_CAUSAL_ESCAPE"
    assert receipt["estimate"] < 0


def test_total_fruit_readout_does_not_promote_escape() -> None:
    text = READOUT.read_text(encoding="utf-8")
    assert "outcome coverage" in text
    assert "not causal identification" in text
    assert "UNRESOLVED_TOTAL_SIGN_CURRENT_EVIDENCE" in text
    assert "does **not** supply the missing positive escape-sign anchor" in text
    assert "not evidence that attraction–defence escape is absent in nature" in text
