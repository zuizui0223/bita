from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_IDENTIFICATION_DESIGN.md"
PORTAL = ROOT / "submission" / "AUTHOR_AND_PORTAL_METADATA_TEMPLATE.md"
COVER = ROOT / "submission" / "COVER_LETTER_ECOLOGY_CONCEPTS_SYNTHESIS.md"
CAPTIONS = ROOT / "manuscript" / "IDENTIFICATION_DESIGN_FIGURE_CAPTIONS.md"
EXPORTER = ROOT / "scripts" / "export_manuscript_figures.sh"
PREPARE_SVG = ROOT / "scripts" / "prepare_submission_svg.py"
FIGURES = ROOT / "manuscript" / "identification_figures"


def _abstract(text: str) -> str:
    return text.split("## Abstract\n\n", 1)[1].split("\n\n**Keywords:**", 1)[0].strip()


def _plain_words(text: str) -> list[str]:
    text = re.sub(r"\\\(|\\\)|[{}*_`]", " ", text)
    return re.findall(r"\b[\w+×-]+\b", text, flags=re.UNICODE)


def _manuscript_keywords(text: str) -> list[str]:
    line = next(line for line in text.splitlines() if line.startswith("**Keywords:**"))
    payload = line.removeprefix("**Keywords:**").strip()
    return [item.strip() for item in payload.split(";") if item.strip()]


def test_abstract_and_keywords_fit_current_ecology_limits() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    abstract = _abstract(text)
    assert 150 <= len(_plain_words(abstract)) <= 350
    assert "56 route records from 25 independent biological clusters" in abstract
    assert "recurrence, not channel identification" in abstract
    assert "16 screened high-information systems" in abstract
    assert "The main empirical gap" in abstract

    keywords = _manuscript_keywords(text)
    assert 6 <= len(keywords) <= 12
    assert keywords == sorted(keywords, key=str.casefold)


def test_portal_abstract_matches_manuscript_and_keywords() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    portal = PORTAL.read_text(encoding="utf-8")
    portal_abstract = portal.split("### Abstract\n\n", 1)[1].split("\n\n### Keywords", 1)[0].strip()
    assert portal_abstract == _abstract(manuscript)
    keyword_block = portal.split("### Keywords\n\n", 1)[1].split("\n\n## Authors", 1)[0]
    portal_keywords = [line[2:].strip() for line in keyword_block.splitlines() if line.startswith("- ")]
    assert portal_keywords == _manuscript_keywords(manuscript)


def test_identification_source_has_explicit_human_metadata_placeholders() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    front = text.split("## Abstract", 1)[0]
    assert "**Authors and affiliations:** [Author-controlled" in front
    assert "**Corresponding author:** [Author-controlled" in front
    assert "**ORCID(s):**" in front
    assert "[Author-controlled; complete before submission.]" in text


def test_required_ai_assistance_disclosure_is_in_methods() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    disclosure = "### 5.4 Computational and AI-assisted workflow transparency"
    assert disclosure in text
    assert text.index(disclosure) < text.index("## 6. Discussion")
    block = text.split(disclosure, 1)[1].split("## 6. Discussion", 1)[0]
    assert "OpenAI ChatGPT" in block
    assert "Anthropic Claude" in block
    assert "not treated as empirical evidence" in block
    assert "authors retain responsibility" in block.lower()


def test_figure_captions_and_eps_names_match_submission_convention() -> None:
    captions = CAPTIONS.read_text(encoding="utf-8")
    for n in range(1, 6):
        assert f"**Figure {n}." in captions
    exporter = EXPORTER.read_text(encoding="utf-8")
    assert 'outputs=("Fig1" "Fig2" "Fig3" "Fig4" "Fig5")' in exporter
    assert "Fig1.eps, Fig2.eps, Fig3.eps, Fig4.eps, Fig5.eps" in exporter
    assert "prepare_submission_svg.py" in exporter
    assert "manuscript/identification_figures" in exporter


def test_submission_svg_preprocessor_removes_only_new_outer_titles(tmp_path: Path) -> None:
    cases = (
        ("FIGURE_1_IDENTIFICATION_DESIGN.svg", "A total trait interaction does not identify its mechanism", "Interaction detection ≠ mechanism allocation"),
        ("FIGURE_2_IDENTIFICATION_DESIGN.svg", "Crossed interventions identify channels and test separability", "Internal separability diagnostic"),
        ("FIGURE_3_IDENTIFICATION_DESIGN.svg", "Do not define the joint cost as a residual", "Sign diagnostic"),
        ("FIGURE_4_IDENTIFICATION_DESIGN.svg", "Constituent channels recur, but mechanism allocation remains unidentified", "recurrence ≠ channel identification"),
        ("FIGURE_5_IDENTIFICATION_DESIGN.svg", "An executable path from interaction detection to mechanism identification", "Run A×D×G×P"),
    )
    for filename, visible_title, retained_token in cases:
        out = tmp_path / filename
        subprocess.run([sys.executable, str(PREPARE_SVG), str(FIGURES / filename), str(out)], check=True)
        prepared = out.read_text(encoding="utf-8")
        assert visible_title not in prepared
        assert retained_token in prepared


def test_cover_letter_uses_live_portal_reviewer_boundary() -> None:
    text = COVER.read_text(encoding="utf-8")
    assert "## Potential reviewers, if requested by the submission portal" in text
    assert "Complete the number and fields requested by ScholarOne" in text
    assert not re.search(r"^[1-5]\. \[Name — institution — e-mail — expertise — conflict check\]$", text, flags=re.MULTILINE)
