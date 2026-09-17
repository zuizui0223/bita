from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC_SUFFIX = "." + "md"
AUDIT = ROOT / "docs" / f"QUANTITATIVE_RESULTS_DISCUSSION_AUDIT_V1{DOC_SUFFIX}"
LEDGER = ROOT / "docs" / f"QUANTITATIVE_CLAIM_LEDGER_V1{DOC_SUFFIX}"


def test_quantitative_results_discussion_audit_has_three_column_contract() -> None:
    text = AUDIT.read_text(encoding="utf-8")
    assert "| Qualitative claim | Quantitative claim licensed | Ceiling / not licensed |" in text


def test_audit_preserves_bita_empirical_and_identification_numbers() -> None:
    ledger = LEDGER.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")
    for token in (
        "56 directional route records",
        "25 independent biological clusters",
        "17 systems",
        "0 systems",
        "A1 approximately +0.200 to +0.240",
        "A0 approximately -0.030 to +0.030",
    ):
        assert token in ledger
        assert token in audit


def test_audit_blocks_mechanism_and_prevalence_overpromotion() -> None:
    text = AUDIT.read_text(encoding="utf-8")
    assert "NATURAL_PREVALENCE = NOT_ESTIMATED" in text
    assert "CHANNEL_ALLOCATION = NOT_POINT_IDENTIFIED_FROM_TOTAL_INTERACTION" in text
    assert "Level-1" in text
    assert "Level-2/3" in text
