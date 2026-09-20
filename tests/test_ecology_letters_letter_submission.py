from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LETTER = ROOT / "manuscript" / "MANUSCRIPT_ACCESS_ROUTING_LETTER_V0.md"
TITLE_PAGE = ROOT / "submission" / "ECOLOGY_LETTERS_LETTER_TITLE_PAGE_V1.md"
COVER = ROOT / "submission" / "ECOLOGY_LETTERS_LETTER_COVER_V0.md"
ARCHIVE_README = ROOT / "submission" / "access_routing_archive" / "README.md"
DEPOSIT_CHECKLIST = ROOT / "submission" / "access_routing_archive" / "DEPOSIT_CHECKLIST_V1.md"


def _words(text: str) -> list[str]:
    return re.findall(r"\b[\w×–/-]+\b", text, flags=re.UNICODE)


def _abstract(text: str) -> str:
    match = re.search(r"## Abstract\n\n([\s\S]*?)\n\n## Introduction", text)
    assert match is not None
    return match.group(1)


def _main_text(text: str) -> str:
    start = text.index("## Introduction")
    end = text.index("## Data accessibility and reproducibility")
    return text[start:end]


def test_letter_title_page_matches_current_manuscript_counts() -> None:
    letter = LETTER.read_text(encoding="utf-8")
    title = TITLE_PAGE.read_text(encoding="utf-8")

    assert "Article type:** Letter" in title
    assert "Access constraints reroute floral exploitation across bird and insect visitor networks" in title
    assert len("Access constraints reroute exploitation") < 45

    abstract_words = len(_words(_abstract(letter)))
    main_words = len(_words(_main_text(letter)))
    references = len(re.findall(r"^- ", letter.split("## References", 1)[1], flags=re.MULTILINE))

    assert f"abstract words: {abstract_words}" in title
    assert f"main-text words: {main_words:,}" in title
    assert f"references: {references}" in title
    assert "figures: 3" in title
    assert "tables: 0" in title
    assert "text boxes: 0" in title
    assert abstract_words <= 150
    assert main_words <= 5000

    keyword_line = next(line for line in title.splitlines() if line.startswith("**Keywords:**"))
    keywords = [item.strip() for item in keyword_line.split(":", 1)[1].split(";") if item.strip()]
    assert len(keywords) <= 10


def test_letter_submission_remains_fail_closed_until_archive_doi_and_author_metadata() -> None:
    title = TITLE_PAGE.read_text(encoding="utf-8")
    cover = COVER.read_text(encoding="utf-8")
    letter = LETTER.read_text(encoding="utf-8")

    assert "ARCHIVE DOI REQUIRED BEFORE SUBMISSION" in title
    assert "[ACCESS-ROUTING ARCHIVE DOI]" in title
    assert "[ACCESS-ROUTING ARCHIVE DOI]" in letter
    assert "ACCESS-ROUTING ARCHIVE DOI — REQUIRED BEFORE SUBMISSION" in cover

    assert "AUTHOR-CONTROLLED — REQUIRED BEFORE SUBMISSION" in title
    assert "Author-relative novelty statement — AUTHOR-CONTROLLED BEFORE SUBMISSION" in cover
    assert "Conflict-of-interest statement — AUTHOR-CONTROLLED BEFORE SUBMISSION" in cover


def test_archive_contract_contains_exact_analysis_tables_metadata_and_reproduction_code() -> None:
    text = ARCHIVE_README.read_text(encoding="utf-8")
    for token in (
        "sakhalkar_species_analysis.csv",
        "aubert_ephi_pair_site_analysis.csv",
        "metadata.csv",
        "archive_manifest.json",
        "archive_reproduction.json",
        "scripts/export_access_routing_archive.py",
        "scripts/reproduce_access_routing_archive.py",
        "10.5281/zenodo.8398202",
        "10.5281/zenodo.14185547",
        "ACCESS_ROUTING_ARCHIVE_DOI = REQUIRED_BEFORE_SUBMISSION",
    ):
        assert token in text

    assert (ROOT / "scripts" / "export_access_routing_archive.py").exists()
    assert (ROOT / "scripts" / "reproduce_access_routing_archive.py").exists()


def test_archive_has_one_file_deposit_contract() -> None:
    readme = ARCHIVE_README.read_text(encoding="utf-8")
    checklist = DEPOSIT_CHECKLIST.read_text(encoding="utf-8")

    for token in (
        "access-routing-letter-data-code-v1.zip",
        "access-routing-letter-data-code-v1.sha256",
        "FILE_SHA256SUMS.txt",
        "DEPOSIT_CHECKLIST_V1.md",
    ):
        assert token in readme

    assert "exact submission commit" in checklist
    assert "10.5281/zenodo.8398202" in checklist
    assert "10.5281/zenodo.14185547" in checklist
    assert "Do not submit while any of these remain" in checklist
