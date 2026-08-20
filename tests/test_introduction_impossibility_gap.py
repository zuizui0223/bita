from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"
BACKGROUND = ROOT / "docs" / "BACKGROUND_NOVELTY_GAP_REVIEW.md"
BLUEPRINT = ROOT / "docs" / "INTRODUCTION_BLUEPRINT.md"


def test_introduction_acknowledges_close_prior_art_before_claiming_gap() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    intro = text.split("## 1. Introduction", 1)[1].split("## 2. Part I", 1)[0]
    assert "Johnson et al. 2021" in intro
    assert "attraction-defence balance, non-additivity, trade-offs, and context-dependent evolutionary outcomes are not new ideas" in intro
    assert "can we identify where it cannot occur?" in intro
    assert "one-sided exclusion rule" in intro
    assert "not a new interaction type or a new mixed partial" in intro


def test_mechanism_precedes_pattern_as_evidence_architecture() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    intro = text.split("### 1.5 Two-part contribution: mechanism and pattern", 1)[1].split("### 1.6", 1)[0]
    assert "Mechanism \\(\\rightarrow\\) Pattern" in intro
    assert "Part I first defines the mechanism classes and derives the structural constraint" in intro
    assert "does not search for a pattern and infer a mechanism afterward" in intro
    assert "direct estimation of the full mixed partial separate" in intro


def test_background_support_docs_match_impossibility_boundary_positioning() -> None:
    background = BACKGROUND.read_text(encoding="utf-8")
    blueprint = BLUEPRINT.read_text(encoding="utf-8")
    assert "### Gap 0: existing balance models do not by themselves provide the focal one-sided impossibility boundary" in background
    assert "Johnson et al. (2021)" in background
    assert "before predicting where complementarity occurs, can we identify where it cannot occur?" in blueprint
    assert "mechanism-first evidence architecture" in blueprint


def test_close_prior_theory_reference_is_cited_and_alphabetized() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    body, refs = text.split("\n## References\n", 1)
    assert "Johnson et al. 2021" in body
    assert "10.1038/s41467-021-23177-x" in refs
    assert refs.index("Johnson CA") < refs.index("Junker RR") < refs.index("Knauer AC")
