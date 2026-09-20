from __future__ import annotations

import json
import re
from pathlib import Path

from scripts.count_access_routing_letter_submission import summarize

ROOT = Path(__file__).resolve().parents[1]
LETTER = ROOT / "manuscript" / "MANUSCRIPT_ACCESS_ROUTING_LETTER_V0.md"
PLAN = ROOT / "manuscript" / "FIGURE_PLAN_ACCESS_ROUTING_LETTER_V0.md"
TITLE = ROOT / "submission" / "ECOLOGY_LETTERS_LETTER_TITLE_PAGE_V1.md"
COUNTS = ROOT / "submission" / "access_routing_letter_submission_counts.json"
COVER = ROOT / "submission" / "ECOLOGY_LETTERS_LETTER_COVER_V0.md"


def test_frozen_submission_counts_match_sources() -> None:
    observed = summarize(
        LETTER.read_text(encoding="utf-8"),
        PLAN.read_text(encoding="utf-8"),
    )
    frozen = json.loads(COUNTS.read_text(encoding="utf-8"))
    assert observed == frozen
    assert observed["main_text_words"] <= 5000
    assert observed["abstract_words"] <= 150
    assert observed["display_item_count"] <= 6


def test_letter_references_are_complete_working_entries() -> None:
    text = LETTER.read_text(encoding="utf-8")
    refs = text.split("## References", 1)[1]
    assert "Use the focused BITA reference pool" not in refs
    for doi in [
        "10.1890/05-0118",
        "10.1002/oik.11552",
        "10.1016/j.cub.2017.07.012",
        "10.1086/657993",
        "10.1111/j.1461-0248.2007.01027.x",
        "10.1146/annurev-ecolsys-112414-054215",
        "10.1002/ecy.1483",
        "10.1016/j.tplants.2015.10.013",
        "10.1111/1365-2435.13035",
        "10.1002/ecs2.4696",
    ]:
        assert doi in refs


def test_title_page_contains_required_non_author_controlled_fields() -> None:
    text = TITLE.read_text(encoding="utf-8")
    for token in [
        "Article title",
        "Article type",
        "Letter",
        "Running title",
        "Keywords",
        "Submission counts",
        "Brief authorship statement",
        "Data accessibility statement",
        "Corresponding author",
    ]:
        assert token in text
    assert "Access constraints reroute floral exploitation across insect and bird visitor networks" in text
    assert "10.5281/zenodo.8398202" in text
    assert "10.5281/zenodo.14185547" in text


def test_running_title_and_keywords_fit_limits() -> None:
    text = TITLE.read_text(encoding="utf-8")
    running = re.search(r"## Running title\n\n\*\*(.+?)\*\*", text)
    assert running is not None
    assert len(running.group(1)) < 45

    keyword_block = text.split("## Keywords", 1)[1].split("## Submission counts", 1)[0]
    keywords = [
        line[2:].strip()
        for line in keyword_block.splitlines()
        if line.startswith("- ")
    ]
    assert 1 <= len(keywords) <= 10
    assert keywords == sorted(keywords, key=str.casefold)


def test_author_controlled_fields_are_not_silently_invented() -> None:
    text = TITLE.read_text(encoding="utf-8")
    assert "AUTHOR-CONTROLLED" in text
    for token in [
        "[AUTHOR-CONTROLLED: insert numbered affiliation(s)]",
        "Email: [AUTHOR-CONTROLLED]",
        "Telephone: [AUTHOR-CONTROLLED]",
    ]:
        assert token in text


def test_cover_letter_is_for_letter_not_synthesis() -> None:
    text = COVER.read_text(encoding="utf-8")
    assert "**Article type:** Letter" in text
    assert "as a Letter in *Ecology Letters*" in text
    assert "equal network weight" in text
    assert "rho_J = 0.349" in text
