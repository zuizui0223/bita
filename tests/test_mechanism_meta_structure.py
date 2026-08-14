from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"
SCOPE = ROOT / "docs" / "SUBMISSION_SCOPE.md"


def test_manuscript_is_explicitly_mechanism_then_pattern() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")

    required_in_order = (
        "## 2. Part I — Mechanistic theory: mechanism and principle",
        "## 3. Part I results — mechanistic sign regimes",
        "## 4. Part II — Meta-analysis and cross-study pattern synthesis",
        "## 5. Part II results — meta-analytic patterns across systems",
        "## 6. Integration — from mechanism to pattern",
        "## 7. Conclusions",
    )
    positions = [text.index(token) for token in required_in_order]
    assert positions == sorted(positions)

    title = text.splitlines()[0]
    assert "When are floral attraction and defence complementary?" in title
    assert "one-sided mechanistic bound" in title
    assert "cross-system patterns" in title
    assert "what mechanism determines" in text
    assert "what cross-system patterns recur" in text
    assert (
        "Quantitative meta-analysis is used only where compatible effect scales exist" in text
        or "We use **meta-analysis** only where study outcomes can be expressed on a defensible common quantitative scale" in text
    )
    assert "random-effects synthesis" in text
    assert "### 5.4 Meta-analysis 1:" in text
    assert "### 5.5 Meta-analytic synthesis 2:" in text
    assert "### 5.6 Cross-system pattern: recurrent mechanisms, conditional balance" in text
    assert "recurrent mechanisms plus context-dependent balance" in text
    assert "56 effect or directional records across 25 independent biological study clusters" in text
    assert "Fourteen study clusters" in text
    assert "Seventeen independent study clusters" in text


def test_pattern_half_does_not_overclaim_grand_meta_analysis() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    scope = SCOPE.read_text(encoding="utf-8")

    assert "We use **meta-analysis** only where study outcomes can be expressed on a defensible common quantitative scale" in text
    assert "we did not fit a cross-outcome grand moderator coefficient" in text
    assert "not prevalence in nature" in text
    assert "The source-adjudicated route ledger is **not itself a grand meta-analysis**" in scope
    assert "recurrent constituent mechanisms + context-dependent balance" in scope


def test_new_framing_is_latex_safe() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")

    assert r"\(W_{AD}=\rho-\iota-\kappa\)" in text
    assert r"\(A\times D\)" in text
    assert r"Mechanism \(\rightarrow\) Pattern" in text
    assert "W_{AD}=\nho" not in text
    assert "A\times D".replace("\\t", "\t") not in text


def test_old_interleaved_structure_is_retired() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    for old in (
        "## 2. Model and analytical framework",
        "### 2.7 Mechanism-pattern empirical synthesis",
        "### 2.8 Quantitative synthesis modules",
        "### 3.7 Quantitative module 1:",
        "## 4. Discussion",
        "## 5. Conclusions",
    ):
        assert old not in text
