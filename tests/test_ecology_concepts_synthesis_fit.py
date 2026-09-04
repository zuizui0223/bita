from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "manuscript" / "MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md"
PORTAL = ROOT / "submission" / "AUTHOR_AND_PORTAL_METADATA_TEMPLATE.md"
COVER = ROOT / "submission" / "COVER_LETTER_ECOLOGY_CONCEPTS_SYNTHESIS.md"
STRATEGY = ROOT / "submission" / "TARGET_JOURNAL_STRATEGY.md"
FIT = ROOT / "submission" / "ECOLOGY_CONCEPTS_SYNTHESIS_FIT_AUDIT.md"


def _abstract(text: str) -> str:
    return text.split("## Abstract\n\n", 1)[1].split("\n\n**Keywords:**", 1)[0].strip()


def _words(text: str) -> list[str]:
    text = re.sub(r"\\\(|\\\)|[{}*_`]", " ", text)
    return re.findall(r"\b[\w+×-]+\b", text, flags=re.UNICODE)


def _keywords(text: str) -> list[str]:
    line = next(line for line in text.splitlines() if line.startswith("**Keywords:**"))
    payload = line.removeprefix("**Keywords:**").strip()
    return [item.strip() for item in payload.split(";") if item.strip()]


def test_ecology_is_current_first_choice_for_integrated_chapter2() -> None:
    portal = PORTAL.read_text(encoding="utf-8")
    strategy = STRATEGY.read_text(encoding="utf-8")
    assert "- Article type: **Concepts & Synthesis**" in portal
    assert "- Target journal: **Ecology**" in portal
    assert "## Current first choice" in strategy
    assert "**Ecology — Concepts & Synthesis**" in strategy
    assert "The American Naturalist" in strategy
    assert "Theoretical Ecology" in strategy
    assert "not the current first-choice submission graph" in strategy


def test_canonical_abstract_preserves_balance_differentiation_identification_hierarchy() -> None:
    text = MAN.read_text(encoding="utf-8")
    abstract = _abstract(text)
    assert len(_words(abstract)) >= 150
    for token in (
        "compromise",
        "differentiation",
        "300-condition robustness grid",
        "cichlids",
        "Dalechampia",
        "floral attraction and defence",
        "mechanistic worked case",
    ):
        assert token.lower() in abstract.lower(), token
    keywords = _keywords(text)
    assert 6 <= len(keywords) <= 12
    for token in ("functional trade-off", "trait differentiation", "causal identification"):
        assert token in keywords


def test_broad_concepts_and_synthesis_framing_is_architecture_led() -> None:
    text = MAN.read_text(encoding="utf-8")
    for token in (
        "when does the best differentiated phenotype outperform the best one-trait compromise?",
        "balance → differentiation → identification",
        "Our contribution is therefore a bridge rather than a claim of theoretical priority.",
        "structural differentiation can remain incomplete",
        "their total fitness interaction still does not identify mechanism",
        "fragmented identification",
    ):
        assert token.lower() in text.lower(), token
    assert "novelty of a new trait-differentiation framework cannot be the statement that trade-offs sometimes favour specialization" in text


def test_open_research_and_ai_disclosure_surfaces_remain_available_in_integrated_graph() -> None:
    text = MAN.read_text(encoding="utf-8")
    component = (ROOT / "manuscript" / "MANUSCRIPT_IDENTIFICATION_DESIGN.md").read_text(encoding="utf-8")
    # The canonical package builder adds the review-stage Open Research statement
    # and retains the identification component in Appendix/provenance.
    assert "## 5. Once several trait axes exist" in text
    disclosure = "### 5.4 Computational and AI-assisted workflow transparency"
    assert disclosure in component
    block = component.split(disclosure, 1)[1].split("## 6. Discussion", 1)[0]
    assert "OpenAI ChatGPT" in block
    assert "Anthropic Claude" in block
    assert "not treated as empirical evidence" in block
    assert "authors retain responsibility" in block.lower()


def test_ecology_cover_letter_matches_chapter2_story_and_standard_length() -> None:
    text = COVER.read_text(encoding="utf-8")
    assert "Concepts & Synthesis" in text
    assert "When does a trait trade-off resolve by differentiation rather than compromise?" in text
    assert "shared-axis balance → partial trait differentiation → mechanism identification" in text
    assert "mechanism identification" in text
    assert "56 source-adjudicated route records from 25 independent biological clusters" in text
    assert "30 Main Document pages" in text
    assert "within the standard 30-page Concepts & Synthesis target" in text
    assert "38-page Appendix S1" in text
    assert "Potential reviewers, if requested by the submission portal" in text
    assert "Complete the number and fields requested by ScholarOne" in text
    assert not re.search(r"^[1-5]\. \[Name — institution — e-mail — expertise — conflict check\]$", text, flags=re.MULTILINE)


def test_fit_audit_records_current_package_and_acceptance_stage_archive() -> None:
    text = FIT.read_text(encoding="utf-8")
    assert "Rendered review-package audit" in text
    assert "Main Document" in text and "Appendix S1" in text
    assert "**30 pages**" in text
    assert "**38 pages**" in text
    assert "68 pages" in text
    assert "standard 30-page target" in text
    assert "acceptance-stage" in text
    assert "## Architecture synthesis fit" in text
    assert "## Mechanism-identification fit" in text
    assert "fragmented identification frontier" in text
