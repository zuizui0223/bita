from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"
PORTAL = ROOT / "submission" / "AUTHOR_AND_PORTAL_METADATA_TEMPLATE.md"
COVER = ROOT / "submission" / "COVER_LETTER_THEORETICAL_ECOLOGY.md"
EXPORTER = ROOT / "scripts" / "export_manuscript_figures.sh"
PREPARE_SVG = ROOT / "scripts" / "prepare_submission_svg.py"
FIGURES = ROOT / "manuscript" / "figures"


def _abstract(text: str) -> str:
    return text.split("## Abstract\n\n", 1)[1].split("\n\n**Keywords:**", 1)[0].strip()


def _plain_words(text: str) -> list[str]:
    text = re.sub(r"\\\(|\\\)|[{}*_`]", " ", text)
    return re.findall(r"\b[\w+×-]+\b", text, flags=re.UNICODE)


def test_abstract_and_keywords_fit_current_journal_limits() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    abstract = _abstract(text)
    assert 150 <= len(_plain_words(abstract)) <= 250
    assert "log response ratio" in abstract

    keyword_line = next(line for line in text.splitlines() if line.startswith("**Keywords:**"))
    keywords = [item.strip() for item in keyword_line.split(":", 1)[1].split(";") if item.strip()]
    assert 4 <= len(keywords) <= 6


def test_portal_abstract_matches_manuscript_and_has_six_keywords() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    portal = PORTAL.read_text(encoding="utf-8")
    portal_abstract = portal.split("### Abstract\n\n", 1)[1].split("\n\n### Keywords", 1)[0].strip()
    assert portal_abstract == _abstract(manuscript)
    keyword_block = portal.split("### Keywords\n\n", 1)[1].split("\n\n## Authors", 1)[0]
    assert sum(line.startswith("- ") for line in keyword_block.splitlines()) == 6


def test_statements_and_declarations_follow_references() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    assert text.index("## References") < text.index("## Statements and Declarations")
    statements = text.split("## Statements and Declarations", 1)[1]
    for heading in (
        "### Funding",
        "### Competing interests",
        "### Author contributions",
        "### Data and code availability",
    ):
        assert heading in statements
    assert "The authors declare no competing interests." not in text
    assert "[Author confirmation required." in statements


def test_required_ai_assistance_disclosure_is_in_methods() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    disclosure = "### 4.3 Computational and AI-assisted workflow transparency"
    assert disclosure in text
    assert text.index(disclosure) < text.index("## 5. Part II results")
    block = text.split(disclosure, 1)[1].split("## 5. Part II results", 1)[0]
    assert "OpenAI" in block
    assert "Anthropic" in block
    assert "AI-generated output was not treated as empirical evidence" in block


def test_figure_captions_and_eps_names_match_journal_convention() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    captions = text.split("## Figure captions\n\n", 1)[1].split("\n\n## Table captions", 1)[0]
    for n in (1, 2, 3, 4, 5):
        marker = f"**Fig. {n}**"
        assert marker in captions
        assert f"**Figure {n}." not in captions
    exporter = EXPORTER.read_text(encoding="utf-8")
    assert 'outputs=("Fig1" "Fig2" "Fig3" "Fig4" "Fig5")' in exporter
    assert "Fig1.eps, Fig2.eps, Fig3.eps, Fig4.eps, Fig5.eps" in exporter
    assert "prepare_submission_svg.py" in exporter


def test_main_text_calls_out_all_main_and_supplementary_assets() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    body = text.split("## Figure captions", 1)[0]

    for token in ("Fig. 1", "Fig. 2", "Fig. 3", "Fig. 4", "Fig. 5"):
        assert token in body, token
    for token in ("Table 1", "Table 2", "Table 3", "Table 4"):
        assert token in body, token
    for token in (
        "Supplementary Figs. S1–S2",
        "Supplementary Figs. S1–S3",
        "Tables S1–S2",
        "Tables S3–S6",
    ):
        assert token in body, token


def test_submission_svg_preprocessor_removes_only_outer_visible_titles(tmp_path: Path) -> None:
    cases = (
        ("FIGURE_1_MECHANISTIC_ARCHITECTURE.svg", "Figure 1. From floral traits to an oriented local interaction", "Attraction trait A"),
        ("FIGURE_2_THEORY_REGIME_MAP.svg", "Figure 2. Conditional attraction–defence regimes across the declared finite tested set", "A  Biological parameter scenarios"),
        ("FIGURE_3_EMPIRICAL_MECHANISM_ARCHITECTURE.svg", "Meta-analytic pattern architecture and identification boundary", "Source-adjudicated Pattern scaffold"),
    )
    for filename, visible_title, retained_token in cases:
        out = tmp_path / filename
        subprocess.run([sys.executable, str(PREPARE_SVG), str(FIGURES / filename), str(out)], check=True)
        prepared = out.read_text(encoding="utf-8")
        assert visible_title not in prepared
        assert retained_token in prepared


def test_cover_letter_reserves_exactly_five_conflict_checked_reviewers() -> None:
    text = COVER.read_text(encoding="utf-8")
    assert "## Potential reviewers" in text
    slots = re.findall(r"^[1-5]\. \[Name — institution — e-mail — expertise — conflict check\]$", text, flags=re.MULTILINE)
    assert len(slots) == 5


def test_title_page_placeholders_are_explicit_not_invented() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    front = text.split("## Abstract", 1)[0]
    assert "**Authors and affiliations:** [Author-controlled" in front
    assert "**Corresponding author:** [Author-controlled" in front
    assert "**ORCID(s):**" in front
