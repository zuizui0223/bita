from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HISTORICAL_MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"
CURRENT_MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_IDENTIFICATION_DESIGN.md"
SCOPE = ROOT / "docs" / "SUBMISSION_SCOPE.md"


def test_historical_manuscript_remains_reproducible_mechanism_then_pattern() -> None:
    text = HISTORICAL_MANUSCRIPT.read_text(encoding="utf-8")

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
    assert "56 effect or directional records across 25 independent biological study clusters" in text


def test_current_pattern_layer_does_not_overclaim_grand_meta_analysis() -> None:
    historical = HISTORICAL_MANUSCRIPT.read_text(encoding="utf-8")
    current = CURRENT_MANUSCRIPT.read_text(encoding="utf-8")
    scope = SCOPE.read_text(encoding="utf-8")

    # The historical synthesis remains available as provenance for the route ledger.
    assert "We use **meta-analysis** only where study outcomes can be expressed on a defensible common quantitative scale" in historical
    assert "we did not fit a cross-outcome grand moderator coefficient" in historical

    # The canonical paper reuses the route architecture only for recurrence.
    assert "The source-adjudicated route ledger is **not itself a grand meta-analysis**" in scope
    assert "Constituent channels recur, but their joint allocation remains unidentified." in scope
    assert "marginal route recurrence does not estimate" in current
    assert "none of these counts is an estimate of natural prevalence" in current


def test_historical_framing_is_latex_safe() -> None:
    text = HISTORICAL_MANUSCRIPT.read_text(encoding="utf-8")
    assert r"\(W_{AD}=\rho-\iota-\kappa\)" in text
    assert r"\(A\times D\)" in text
    assert r"Mechanism \(\rightarrow\) Pattern" in text
    assert "W_{AD}=\nho" not in text


def test_current_manuscript_is_identification_led() -> None:
    text = CURRENT_MANUSCRIPT.read_text(encoding="utf-8")
    assert "## 4. From mechanism to pattern: recurrence before identification" in text
    assert "The Mechanism → Pattern bridge is therefore two-stage" in text
    assert "A total attraction-by-defence interaction therefore does not identify its mechanism." in text
    assert "The missing object is their intersection." in text
