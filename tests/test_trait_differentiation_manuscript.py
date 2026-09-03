"""Regression guards for the integrated SCH/BITA Chapter 2 manuscript draft."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md"


def _text() -> str:
    return MANUSCRIPT.read_text(encoding="utf-8")


def test_integrated_chapter2_draft_exists_and_leads_with_general_tradeoff() -> None:
    assert MANUSCRIPT.exists()
    text = _text()
    title = text.splitlines()[0]
    assert "trait trade-off" in title
    assert "differentiation rather than compromise" in title
    assert "functional trait" in text.lower() or "multifunctional trait" in text.lower()


def test_main_architecture_identity_is_explicit() -> None:
    text = _text()
    for token in (
        "L_S^*",
        "decoupling fraction",
        "R=sL_S^*",
        "\\Delta_{arch}=W_D^*-W_S^*=sL_S^*-K",
        "K<sL_S^*",
    ):
        assert token in text, token


def test_incomplete_differentiation_is_not_collapsed_to_independence() -> None:
    text = _text().lower()
    assert "structural differentiation does not imply independence" in text
    assert "residual coupling" in text
    assert "0<s<1" in text.replace(" ", "")


def test_registered_nonquadratic_result_is_reported_with_ceiling() -> None:
    text = _text()
    for token in ("300", "60/60", "convex", "finite robustness design"):
        assert token in text, token
    lower = text.lower()
    assert "not an exhaustive theorem" in lower or "not a universal theorem" in lower


def test_prior_specialization_theory_is_acknowledged_before_novelty_claim() -> None:
    text = _text()
    for token in (
        "Rüffler",
        "Guillaume and Otto",
        "Sack and Buckley",
        "not the existence of specialization",
    ):
        assert token in text, token


def test_cross_system_architecture_anchors_are_kept_bounded() -> None:
    text = _text()
    for token in ("cichlid", "Dalechampia", "Burress", "Conith", "Armbruster"):
        assert token.lower() in text.lower(), token
    assert "do not estimate" in text.lower() or "does not estimate" in text.lower()


def test_floral_identification_work_is_retained_as_worked_case() -> None:
    text = _text()
    for token in (
        "Floral attraction and defence as a worked case",
        "\\Delta_{AD}W",
        "identified set",
        "A\\times D\\times E_G\\times E_P",
        "56 route records from 25 independent biological study clusters",
        "17 systems",
    ):
        assert token in text, token


def test_manuscript_does_not_promote_trait_interaction_to_historical_differentiation() -> None:
    text = _text().lower()
    assert "does not reconstruct the historical origin" in text or "does not establish" in text
    assert "does not specify whether a lineage can reach that architecture" in text
    assert "historical causation remains" not in text or "historical" in text


def test_final_programme_closes_balance_to_differentiation_to_identification() -> None:
    text = _text()
    conclusion = text.split("## 7. Conclusions", 1)[1]
    assert "SCH asks how conflicting functions balance on one trait" in conclusion
    assert "BITA asks when evolution can stop compromising" in conclusion
    assert "mechanism" in conclusion.lower()
