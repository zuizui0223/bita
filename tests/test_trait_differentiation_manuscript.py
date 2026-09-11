"""Regression guards for the active BITA mechanism-identification manuscript."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md"


def _text() -> str:
    return MANUSCRIPT.read_text(encoding="utf-8")


def test_active_manuscript_exists_and_leads_with_mechanism_identification() -> None:
    assert MANUSCRIPT.exists()
    text = _text()
    assert text.splitlines()[0] == "# Trait interaction is not ecological mechanism: an identification framework for multifunctional traits"
    assert "multifunctional traits" in text.lower()
    assert "interaction" in text.lower()
    assert "mechanism" in text.lower()


def test_nested_outcome_hierarchy_is_explicit() -> None:
    text = _text()
    for token in (
        "Level 1 — positive interaction relief",
        "Level 2 — functional constraint release",
        "Level 3 — strict reversal",
        "A_0",
        "A_1",
        "Delta_{AD}",
    ):
        assert token in text, token
    assert "Level 1 does not imply Levels 2 or 3" in text


def test_total_interaction_is_not_collapsed_to_unique_mechanism() -> None:
    text = _text()
    assert "identified set" in text
    assert "rho" in text
    assert "iota" in text
    assert "kappa" in text
    assert "does not identify" in text
    assert "partial identification" in text


def test_crossed_intervention_and_separability_design_are_explicit() -> None:
    text = _text()
    assert "A\\times D\\times E_G\\times E_P" in text
    assert "four-way" in text.lower()
    assert "separability" in text.lower()
    assert "pollinator-absent" in text.lower() or "pollinator-independent" in text.lower()
    assert "remaining joint channel" in text.lower()


def test_empirical_pattern_precedes_next_identifiable_experiment() -> None:
    text = _text()
    assert text.index("## 5. The empirical pattern") < text.index("## 6. Designing the next identifiable experiment")
    assert "56 directional route records from 25 independent biological clusters" in text
    assert "17 high-information systems" in text
    assert "fragmented identification frontier" in text.lower()
    assert "None closes the entire sequence" in text


def test_route_recurrence_is_not_promoted_to_prevalence_or_mechanism() -> None:
    text = _text().lower()
    assert "not prevalence" in text or "not an estimate of natural prevalence" in text
    assert "route" in text
    assert "mechanism" in text
    assert "marginal" in text or "constituent" in text


def test_manuscript_preserves_boundary_with_slk() -> None:
    text = _text()
    assert "## 7. Relation to SCH and SLK" in text
    assert "SLK" in text
    assert "architecture" in text.lower()
    assert "not the novelty center of this paper" in text
    assert "R" in text and "K" in text and "Phi" in text


def test_manuscript_does_not_promote_interaction_to_historical_differentiation() -> None:
    text = _text().lower()
    assert "historical" in text
    assert "does not" in text
    assert "trait differentiation" in text or "differentiated" in text
    assert "positive" in text and "interaction" in text


def test_claim_ceiling_closes_on_identification_not_architecture_value() -> None:
    text = _text()
    block = text.split("## 9. Claim ceiling", 1)[1]
    assert "interaction" in block.lower()
    assert "mechanism" in block.lower()
    assert "historical" in block.lower()
    assert "prevalence" in block.lower()
    assert "SLK" in text
