from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ACTIVE_TEXT_FILES = [
    "README.md",
    "SUPPLEMENT_MANIFEST.md",
    "docs/PART_I_ROBUSTNESS_PROTOCOL.md",
    "empirical/part_i_robustness/PART_I_SENSITIVITY_READOUT_V2.md",
    "scripts/run_part_i_robustness.py",
    "scripts/build_part_i_manuscript_readout.py",
    "trait_architecture/robustness.py",
]

BANNED_ACTIVE_TOKENS = [
    "conditional_majority",
    "initial_qualitative_grid_v1",
    "part_i_robustness_envelope.csv",
    "part_i_robustness_cases.csv",
    "part_i_robustness_report.json",
    "parameter_envelope_class_counts",
]


def test_active_submission_uses_only_v2_contract_language() -> None:
    for relative in ACTIVE_TEXT_FILES:
        text = (ROOT / relative).read_text(encoding="utf-8")
        for token in BANNED_ACTIVE_TOKENS:
            assert token not in text, f"{token!r} remains in {relative}"


def test_background_review_states_safe_novelty_boundary() -> None:
    text = (ROOT / "docs" / "BACKGROUND_NOVELTY_GAP_REVIEW.md").read_text(
        encoding="utf-8"
    )
    assert "Multivariate and correlational selection are established" in text
    assert "mechanism decomposition is not identified by total fitness alone" in text
    assert "provisional positioning statement" in text
    assert "first model showing" in text
    assert "Sentence to avoid" in text
