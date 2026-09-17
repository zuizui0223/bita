from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "QUANTITATIVE_CLAIM_LEDGER_V1.md"
CLAIMS = ROOT / "manuscript" / "CLAIM_FREEZE.md"

CLASSES = (
    "EMPIRICAL",
    "LITERATURE-AUDIT",
    "THEORETICAL-WITNESS",
    "MODEL-PREDICTION",
    "NOT-ESTIMATED",
)


def test_quantitative_claim_ledger_declares_all_claim_classes() -> None:
    text = LEDGER.read_text(encoding="utf-8")
    for claim_class in CLASSES:
        assert f"`{claim_class}`" in text


def test_ledger_preserves_frozen_bita_quantities() -> None:
    claims = CLAIMS.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    tokens = (
        "56 directional route records",
        "25 independent biological clusters",
        "17 systems",
        "A1 approximately +0.200 to +0.240",
        "A0 approximately -0.030 to +0.030",
    )
    for token in tokens:
        assert token in claims
        assert token in ledger


def test_ledger_preserves_identification_ceiling() -> None:
    text = LEDGER.read_text(encoding="utf-8")
    assert "0 systems" in text
    assert "full allocation design plus an independent remaining-channel assay" in text
    assert "NATURAL_PREVALENCE = NOT_ESTIMATED" in text
    assert "CHANNEL_ALLOCATION = NOT_POINT_IDENTIFIED_FROM_TOTAL_INTERACTION" in text
