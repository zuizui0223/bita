from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"
AUDIT = ROOT / "docs" / "LITERATURE_POSITIONING_AUDIT_2026-08-21.md"


def test_elementary_math_is_explicit_at_reader_checkpoints() -> None:
    text = MAN.read_text(encoding="utf-8")
    abstract = text.split("## Abstract", 1)[1].split("**Keywords:**", 1)[0]
    theorem = text.split("**Theorem 1 (one-sided selectivity bound).**", 1)[1].split("## 3.", 1)[0]
    discussion = text.split("### 6.1 A simple bound on a complex ecological balance", 1)[1].split("### 6.2", 1)[0]
    assert "algebra is deliberately elementary" in abstract.lower()
    assert "The algebra is therefore one line" in theorem
    assert "one-line exclusion" in discussion
    assert "positive joint-cost term can still reverse the sign" in theorem


def test_ecological_interpretation_keeps_evidence_boundary() -> None:
    text = MAN.read_text(encoding="utf-8")
    assert "functional-discrimination condition" in text
    assert "do not directly estimate \\(\\rho-\\iota\\)" in text
    assert "not to classify individual systems as mathematically inside the window" in text
    assert "motivate hypotheses about \\(\\kappa\\); they do not identify it" in text


def test_context_dependence_is_mechanistic_not_blanket_heterogeneity() -> None:
    text = MAN.read_text(encoding="utf-8")
    assert "mechanistic context dependence" in text
    assert "apparent context dependence" in text
    assert "source-adjudication and evidence hierarchy" in text
    assert "Catford et al. 2022" in text


def test_close_prior_art_is_acknowledged_without_priority_claim() -> None:
    text = MAN.read_text(encoding="utf-8")
    intro = text.split("### 1.2 Existing theories", 1)[1].split("### 1.3", 1)[0]
    for token in (
        "Strauss and Whittall 2006",
        "Adler 2008",
        "Kessler and Halitschke 2009",
        "Johnson et al. 2015",
        "Lucas-Barbosa 2016",
        "Rusman et al. 2018",
        "Sletvold 2019",
    ):
        assert token in intro
    assert "not a priority claim" in intro


def test_targeted_literature_audit_documents_scope() -> None:
    audit = AUDIT.read_text(encoding="utf-8")
    assert "reopening of broad Pattern evidence discovery" in audit
    assert "The algebraic answer is elementary" in audit
    assert "Hypothesis-generating only" in audit
