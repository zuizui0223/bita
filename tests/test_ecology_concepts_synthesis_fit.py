from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "manuscript" / "MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md"
PORTAL = ROOT / "submission" / "AUTHOR_AND_PORTAL_METADATA_TEMPLATE.md"
COVER = ROOT / "submission" / "COVER_LETTER_ECOLOGY_CONCEPTS_SYNTHESIS.md"
STRATEGY = ROOT / "submission" / "TARGET_JOURNAL_STRATEGY.md"
FIT = ROOT / "submission" / "ECOLOGY_CONCEPTS_SYNTHESIS_FIT_AUDIT.md"
IDENTIFICATION = ROOT / "manuscript" / "MANUSCRIPT_IDENTIFICATION_DESIGN.md"


def _abstract(text: str) -> str:
    return text.split("## Abstract\n\n", 1)[1].split("\n\n**Keywords:**", 1)[0].strip()


def _words(text: str) -> list[str]:
    text = re.sub(r"\\\(|\\\)|[{}*_`]", " ", text)
    return re.findall(r"\b[\w+×-]+\b", text, flags=re.UNICODE)


def _keywords(text: str) -> list[str]:
    line = next(line for line in text.splitlines() if line.startswith("**Keywords:**"))
    return [item.strip() for item in line.removeprefix("**Keywords:**").strip().split(";") if item.strip()]


def test_ecology_remains_current_target_class_for_active_mechanism_paper() -> None:
    portal = PORTAL.read_text(encoding="utf-8")
    strategy = STRATEGY.read_text(encoding="utf-8")
    status = (ROOT / "docs" / "PUBLICATION_STATUS.md").read_text(encoding="utf-8")
    assert "Concepts & Synthesis" in portal
    assert "Ecology" in portal
    assert "Ecology" in strategy
    assert "ECOLOGY_CONCEPTS_AND_SYNTHESIS" in status


def test_canonical_abstract_is_mechanism_identification_led() -> None:
    text = MAN.read_text(encoding="utf-8")
    abstract = _abstract(text)
    assert len(_words(abstract)) >= 150
    for token in (
        "trait interaction",
        "identified set",
        "partial identification",
        "four-way interaction",
        "56 directional route records",
        "25 independent biological",
        "17 high-information",
        "fragmented",
    ):
        assert token.lower() in abstract.lower(), token
    keywords = _keywords(text)
    assert 6 <= len(keywords) <= 12
    for token in ("causal identification", "ecological mechanism", "trait interaction"):
        assert token in keywords


def test_concepts_and_synthesis_framing_keeps_architecture_value_in_slk() -> None:
    text = MAN.read_text(encoding="utf-8")
    fit = FIT.read_text(encoding="utf-8")
    assert "broader architecture-value question" in text
    assert "owned by the companion SLK framework" in text
    assert "Trait interaction is not ecological mechanism" in fit
    assert "belongs to SLK" in fit
    assert "historical and not submission-current" in fit


def test_open_research_and_ai_disclosure_surfaces_remain_available() -> None:
    component = IDENTIFICATION.read_text(encoding="utf-8")
    assert "Computational and AI-assisted workflow transparency" in component
    block = component.split("Computational and AI-assisted workflow transparency", 1)[1]
    assert "OpenAI" in block
    assert "Anthropic" in block
    assert "not treated as empirical evidence" in block


def test_ecology_cover_letter_matches_current_mechanism_story() -> None:
    text = COVER.read_text(encoding="utf-8")
    assert "Concepts & Synthesis" in text
    assert "Trait interaction is not ecological mechanism" in text
    assert "Delta_AD W = rho_delta - iota_delta - kappa_delta" in text
    assert "56 directional route records from 25 independent biological clusters" in text
    assert "17-system high-information audit" in text
    assert "recurrent constituent biology with fragmented identification" in text
    assert "companion SLK framework owns" in text
    assert "previously generated 30-page Main / 38-page Appendix package" in text
    assert "no longer submission-current" in text


def test_fit_audit_routes_to_current_builder_and_requires_fresh_qa() -> None:
    text = FIT.read_text(encoding="utf-8")
    assert "scripts/build_bita_mechanism_candidate_sources.py" in text
    assert ".github/workflows/build-bita-mechanism-review-package.yml" in text
    assert "56 directional route records" in text
    assert "25 independent biological clusters" in text
    assert "17 high-information systems" in text
    assert "RECURRENT_CONSTITUENT_BIOLOGY" in text
    assert "FRAGMENTED_IDENTIFICATION" in text
    assert "rebuild the active mechanism-identification DOCX/PDF" in text
