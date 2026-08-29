from __future__ import annotations

from pathlib import Path

import scripts.build_theoretical_ecology_submission_sources as te


ROOT = Path(__file__).resolve().parents[1]
COVER = ROOT / "submission" / "COVER_LETTER_THEORETICAL_ECOLOGY.md"
CONTRACT = ROOT / "submission" / "THEORETICAL_ECOLOGY_SUBMISSION_CONTRACT_V2.md"


def test_target_abstract_and_keywords_match_current_springer_contract() -> None:
    assert 150 <= te.word_count(te.TARGET_ABSTRACT) <= 250
    assert len(te.TARGET_KEYWORDS) == 6
    assert "identified set" in te.TARGET_ABSTRACT
    assert "Kessler et al. (2008)" in te.TARGET_ABSTRACT
    assert "source/design-based interaction uncertainty remains unresolved" in te.TARGET_ABSTRACT
    assert "Impatiens capensis" in te.TARGET_ABSTRACT


def test_generated_main_source_is_identification_first_theoretical_ecology() -> None:
    text = te.build_main_source()
    assert text.startswith(f"# {te.TARGET_TITLE}")
    assert "**Journal:** Theoretical Ecology" in text
    assert "**Article type:** Regular Article" in text
    assert "**Keywords:** " + "; ".join(te.TARGET_KEYWORDS) in text
    assert "## 2. The estimand: a trait interaction that can actually be measured" in text
    assert "## Statements and Declarations" in text
    assert text.index("## Statements and Declarations") > text.index("## References")
    assert "### Funding" in text
    assert "### Competing Interests" in text
    assert "### Author Contributions" in text
    assert "### Data and code availability" in text
    assert "AI-assisted workflow transparency" in text
    assert "Concepts & Synthesis" not in text
    assert "30_PAGE" not in text


def test_cover_letter_matches_current_identification_framing_and_has_five_reviewer_slots() -> None:
    text = COVER.read_text(encoding="utf-8")
    assert te.TARGET_TITLE in text
    assert "Regular Article" in text
    assert "identified set" in text
    assert "robustly positive aggregate probability-scale interaction" in text
    assert "source day/genotype uncertainty cannot be recovered" in text
    assert "2,592" not in text
    assert "one-sided mechanistic bound" not in text
    assert text.count("[Name — institution — e-mail — expertise — conflict check]") == 5


def test_submission_contract_keeps_ecology_package_separate_and_human_fields_blocked() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    assert "Regular Article" in text
    assert "Ecology Concepts & Synthesis package remains a fallback/legacy artifact" in text
    assert "BLOCKED_AUTHOR_METADATA" in text
    assert "five real reviewer suggestions" in text
    assert "4–6 keywords" in text


def test_qa_receipt_is_technically_ready_before_human_metadata() -> None:
    main = te.build_main_source()
    receipt = te.build_qa_receipt(
        main,
        copied_data=[{"source": "x", "package_file": "x"}],
        figures=[f"Fig{i}.svg" for i in range(1, 6)],
    )
    assert receipt["automated_status"] == "TECHNICALLY_READY"
    assert receipt["human_status"] == "BLOCKED_AUTHOR_METADATA"
    assert receipt["keyword_count"] == 6
    assert 150 <= receipt["abstract_word_count"] <= 250
    assert receipt["reviewer_placeholder_count"] == 5
