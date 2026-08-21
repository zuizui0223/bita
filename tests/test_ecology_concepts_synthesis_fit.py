from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"
PORTAL = ROOT / "submission" / "AUTHOR_AND_PORTAL_METADATA_TEMPLATE.md"
COVER = ROOT / "submission" / "COVER_LETTER_ECOLOGY_CONCEPTS_SYNTHESIS.md"
STRATEGY = ROOT / "submission" / "TARGET_JOURNAL_STRATEGY.md"
FIT = ROOT / "submission" / "ECOLOGY_CONCEPTS_SYNTHESIS_FIT_AUDIT.md"


def _abstract(text: str) -> str:
    return text.split("## Abstract\n\n", 1)[1].split("\n\n**Keywords:**", 1)[0].strip()


def _words(text: str) -> list[str]:
    text = re.sub(r"\\\(|\\\)|[{}*_`]", " ", text)
    return re.findall(r"\b[\w+×-]+\b", text, flags=re.UNICODE)


def test_ecology_target_and_article_type_are_active() -> None:
    portal = PORTAL.read_text(encoding="utf-8")
    strategy = STRATEGY.read_text(encoding="utf-8")
    assert "- Article type: **Concepts & Synthesis**" in portal
    assert "- Target journal: **Ecology**" in portal
    assert "**Ecology — Concepts & Synthesis**" in strategy
    assert "Oikos — Forum" in strategy
    assert "Theoretical Ecology — Regular Article" in strategy


def test_ecology_abstract_and_keywords_fit_current_limits() -> None:
    text = MAN.read_text(encoding="utf-8")
    abstract = _abstract(text)
    assert 150 <= len(_words(abstract)) <= 350
    keyword_line = next(line for line in text.splitlines() if line.startswith("**Keywords:**"))
    keywords = [item.strip() for item in keyword_line.split(":", 1)[1].split(";") if item.strip()]
    assert 6 <= len(keywords) <= 12
    assert keywords == sorted(keywords, key=str.casefold)


def test_portal_abstract_stays_exactly_synchronized() -> None:
    manuscript = MAN.read_text(encoding="utf-8")
    portal = PORTAL.read_text(encoding="utf-8")
    pabs = portal.split("### Abstract\n\n", 1)[1].split("\n\n### Keywords", 1)[0].strip()
    assert pabs == _abstract(manuscript)


def test_broad_concepts_and_synthesis_framing_is_bounded() -> None:
    text = MAN.read_text(encoding="utf-8")
    assert "A recurring problem in ecology is that net interaction outcomes can conceal opposing causal channels" in text
    assert "This ordering is also the paper's broader contribution to ecological synthesis" in text
    assert "### 6.5 What transfers beyond the floral case" in text
    assert "constraint before pattern" in text
    assert "not the particular floral route signs or the inequality derived from them" in text
    assert "unsupported universal law" in text


def test_open_research_and_esa_ai_disclosure_surfaces_are_present() -> None:
    text = MAN.read_text(encoding="utf-8")
    front = text.split("## Abstract", 1)[0]
    assert "**Open Research statement:**" in front
    methods = text.split("### 4.3 Computational and AI-assisted workflow transparency", 1)[1].split("## 5.", 1)[0]
    assert "OpenAI" in methods and "Anthropic" in methods
    ack = text.split("## Acknowledgments", 1)[1].split("## Statements and Declarations", 1)[0]
    assert "OpenAI ChatGPT" in ack
    assert "Anthropic Claude" in ack
    assert "authors retain responsibility" in ack


def test_ecology_cover_letter_has_conceptual_advance_and_current_length_justification() -> None:
    text = COVER.read_text(encoding="utf-8")
    assert "Concepts & Synthesis" in text
    assert "constraint before pattern" in text
    assert "goes beyond review" in text
    assert "## 1. Broad ecological contribution of the additional length" in text
    assert "## 2. Why the additional material cannot be moved adequately to Supporting Information" in text
    assert "Potential reviewers, if requested by the submission portal" in text
    assert "Complete the number and fields requested by ScholarOne" in text
    assert not re.search(r"^[1-5]\. \[Name — institution — e-mail — expertise — conflict check\]$", text, flags=re.MULTILINE)


def test_fit_audit_records_rendered_review_package_and_acceptance_stage_archive() -> None:
    text = FIT.read_text(encoding="utf-8")
    assert "Rendered review-package audit" in text
    assert "Main Document" in text and "Appendix S1" in text
    assert "31–50-page" in text
    assert "acceptance-stage" in text
    assert "Scientific invariants preserved" in text
