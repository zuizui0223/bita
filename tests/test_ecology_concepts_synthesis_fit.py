from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "manuscript" / "MANUSCRIPT_IDENTIFICATION_DESIGN.md"
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


def test_ecology_package_is_preserved_as_legacy_while_theoretical_ecology_is_active() -> None:
    portal = PORTAL.read_text(encoding="utf-8")
    strategy = STRATEGY.read_text(encoding="utf-8")
    assert "- Article type: **Concepts & Synthesis**" in portal
    assert "- Target journal: **Ecology**" in portal
    assert "## Current first choice" in strategy
    assert "**Theoretical Ecology — Regular Article**" in strategy
    assert "not an Ecology Concepts & Synthesis submission" in strategy
    assert "legacy/fallback" in strategy
    assert "Oikos — Forum" not in strategy


def test_active_canonical_abstract_preserves_current_scientific_hierarchy() -> None:
    text = MAN.read_text(encoding="utf-8")
    abstract = _abstract(text)
    assert len(_words(abstract)) >= 150
    for token in (
        "Level 1",
        "Level 2",
        "Level 3",
        "56 route records from 25 independent biological clusters",
        "recurrence, not channel identification",
        "A_0",
        "A_1",
    ):
        assert token in abstract
    keywords = _keywords(text)
    assert 6 <= len(keywords) <= 12
    assert keywords == sorted(keywords, key=str.casefold)


def test_legacy_ecology_portal_remains_a_separate_fallback_surface() -> None:
    portal = PORTAL.read_text(encoding="utf-8")
    strategy = STRATEGY.read_text(encoding="utf-8")
    pabs = portal.split("### Abstract\n\n", 1)[1].split("\n\n### Keywords", 1)[0].strip()
    assert pabs
    assert "- Target journal: **Ecology**" in portal
    assert "**Theoretical Ecology — Regular Article**" in strategy
    # The active Theoretical Ecology package owns its own abstract contract;
    # this legacy Ecology portal is retained as provenance/fallback and need not
    # be byte-identical to the current canonical manuscript.


def test_broad_concepts_and_synthesis_framing_is_identification_led() -> None:
    text = MAN.read_text(encoding="utf-8")
    assert "A total attraction-by-defence interaction therefore does not identify its mechanism" in text
    assert "The contribution is not a new ecological interaction type and not a mathematically elaborate theorem." in text
    assert "The missing object is their intersection." in text
    assert "The transferable principle is not the floral notation." in text
    assert "Mechanism → Pattern bridge is therefore two-stage" in text
    assert "mechanism allocation" in text
    assert "marginal route recurrence does not estimate" in text
    assert "positive interaction relief" in text
    assert "constraint release" in text


def test_open_research_and_ai_disclosure_surfaces_are_present() -> None:
    text = MAN.read_text(encoding="utf-8")
    assert "## Open Research statement" in text
    disclosure = "### 5.4 Computational and AI-assisted workflow transparency"
    assert disclosure in text
    block = text.split(disclosure, 1)[1].split("## 6. Discussion", 1)[0]
    assert "OpenAI ChatGPT" in block
    assert "Anthropic Claude" in block
    assert "not treated as empirical evidence" in block
    assert "authors retain responsibility" in block.lower()


def test_ecology_cover_letter_matches_identification_story_and_standard_length() -> None:
    text = COVER.read_text(encoding="utf-8")
    assert "Concepts & Synthesis" in text
    assert "From floral trait interactions to mechanism identification" in text
    assert "interaction detection" in text
    assert "mechanism allocation" in text
    assert "56 source-adjudicated route records from 25 independent biological clusters" in text
    assert "29 Main Document pages" in text
    assert "within the standard 30-page Concepts & Synthesis target" in text
    assert "## 1. Broad ecological contribution of the additional length" not in text
    assert "## 2. Why the additional material cannot be moved adequately to Supporting Information" not in text
    assert "Potential reviewers, if requested by the submission portal" in text
    assert "Complete the number and fields requested by ScholarOne" in text
    assert not re.search(r"^[1-5]\. \[Name — institution — e-mail — expertise — conflict check\]$", text, flags=re.MULTILINE)


def test_fit_audit_records_current_package_and_acceptance_stage_archive() -> None:
    text = FIT.read_text(encoding="utf-8")
    assert "Rendered review-package audit" in text
    assert "Main Document" in text and "Appendix S1" in text
    assert "29 pages" in text
    assert "standard 30-page" in text
    assert "acceptance-stage" in text
    assert "## Identification invariants preserved" in text
    assert "Mechanism → Pattern fit is preserved" in text
    assert "constituent ecological channels recur" in text
