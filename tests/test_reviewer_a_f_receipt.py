from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "docs" / "REVIEWER_A_F_CORRECTION_RECEIPT.md"


def test_reviewer_a_f_correction_receipt_exists_and_records_all_six_points() -> None:
    text = RECEIPT.read_text(encoding="utf-8")
    for marker in (
        "## A — Leal data availability and reproducibility",
        "## B — theorem premise",
        "## C — proof versus finite-grid verification",
        "## D — 56/25 count provenance and non-additivity",
        "## E — AI disclosure",
        "## F — Sasidharan synthesis wording",
    ):
        assert marker in text
    assert "ed33b25593c0d90ad6657753f6f5501d9efc7b82" in text
    assert "kappa >= 0" in text
    assert "OpenAI and Anthropic" in text
