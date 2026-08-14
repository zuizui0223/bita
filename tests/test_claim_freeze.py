"""Regression guards for the frozen paper-level scientific claims."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"
CLAIM_FREEZE = ROOT / "manuscript" / "CLAIM_FREEZE.md"
STORY_BOUNDARY = ROOT / "docs" / "MECHANISM_PATTERN_STORY_BOUNDARY.md"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_claim_freeze_assets_exist() -> None:
    assert CLAIM_FREEZE.exists()
    assert STORY_BOUNDARY.exists()


def test_manuscript_keeps_the_one_sided_theorem_visible() -> None:
    text = _text(MANUSCRIPT)
    assert "one-sided" in text
    assert "W_{AD}>0" in text or "W_{AD} > 0" in text
    assert "selectivity window" in text
    assert "necessary" in text
    assert "not sufficient" in text or "converse is not" in text


def test_manuscript_keeps_the_verified_looseness_and_h_gate() -> None:
    text = _text(MANUSCRIPT)
    for token in ("2,592", "77.2%", "35 of 48", "-1.13,+0.71", "0-8%"):
        assert token in text, token


def test_manuscript_does_not_turn_constituent_paths_into_total_calibration() -> None:
    text = _text(MANUSCRIPT)
    assert "does not calibrate \\(W_{AD}\\)" in text or "does not estimate \\(W_{AD}\\)" in text
    assert "constituent-path evidence" in text
    assert "unidentified, not zero" in text


def test_prohibited_overclaim_phrases_stay_absent() -> None:
    text = _text(MANUSCRIPT).lower()
    prohibited = (
        "we provide the first general theory",
        "we derive a novel universal criterion",
        "the selectivity window is sufficient for complementarity",
        "we empirically validate w_ad",
        "kappa is zero because",
    )
    for phrase in prohibited:
        assert phrase not in text, phrase


def test_next_experiment_remains_a_falsification_gate_not_a_missing_result() -> None:
    text = _text(MANUSCRIPT)
    assert "2 \\times 2 allocation" in text
    assert "full attraction \\times defence factorial" in text
    assert "sufficiently negative" in text


def test_claim_freeze_names_the_non_novel_prior_art_boundary() -> None:
    text = _text(CLAIM_FREEZE).lower()
    for phrase in (
        "correlational selection",
        "defence carrying a pollination cost",
        "context dependence itself",
        "route counts are not prevalence estimates",
    ):
        assert phrase in text, phrase
