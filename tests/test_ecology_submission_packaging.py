from __future__ import annotations

from pathlib import Path
import importlib.util
import sys


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

SCRIPT = SCRIPTS / "build_ecology_review_package_sources.py"
COVER = ROOT / "submission" / "COVER_LETTER_ECOLOGY_CONCEPTS_SYNTHESIS.md"

spec = importlib.util.spec_from_file_location("ecology_review_builder", SCRIPT)
assert spec and spec.loader
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def test_main_submission_source_is_identification_design() -> None:
    text = builder.build_main_submission_source()
    ordered = [
        "From floral trait interactions to mechanism identification",
        "**Journal:** Ecology",
        "**Manuscript type:** Concepts & Synthesis",
        "**Open Research statement:**",
        builder.TITLE_BREAK,
        "## Abstract",
        "## 1. Introduction",
        "## 3. A crossed intervention design for channel identification",
        "## Acknowledgments",
        "## Author Contributions",
        "## Funding",
        "## Conflict of Interest Statement",
        "## References",
        builder.REF_BREAK,
        "**Figure 1.",
        "**Figure 2.",
        "**Figure 3.",
        "**Figure 4.",
        "**Figure 5.",
    ]
    positions = [text.index(token) for token in ordered]
    assert positions == sorted(positions)
    assert "Theorem 1" not in text
    assert "77.2%" not in text
    assert "2,592" not in text.split("## References", 1)[0]


def test_main_has_five_identification_figures_and_no_main_tables() -> None:
    text = builder.build_main_submission_source()
    for idx in range(1, 6):
        assert f"FIGURE_{idx}_IDENTIFICATION_DESIGN.svg" in text
        assert f"**Figure {idx}." in text
    assert "## Table 1." not in text
    # References section break starts Figure 1; Figures 2–5 use explicit breaks.
    assert text.count(builder.PAGE_BREAK) == 4


def test_appendix_is_identification_supplement() -> None:
    text = builder.build_appendix_source()
    assert text.startswith("# Appendix S1 — Identification design")
    assert "2,592" in text
    assert "77.2%" in text
    assert "KESSLER_2008_IDENTIFICATION_REAUDIT_V2.md" in text
    assert "IMPATIENS_2018_IDENTIFICATION_RETROFIT_V1.json" in text
    assert "HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V1.csv" in text
    assert "FIGURE_S1_DERIVATIVE_AGREEMENT.svg" in text
    assert "FIGURE_S2_SCENARIO_SIGN_MAPS.svg" in text


def test_open_research_package_includes_identification_outputs(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(builder, "OUT", tmp_path)
    monkeypatch.setattr(builder, "DATA_OUT", tmp_path / "open_research_data")
    manifest = builder.build_open_research_manifest()
    names = {p.name for p in (tmp_path / "open_research_data").iterdir()}
    for expected in (
        "model_parameters_and_scaling.csv",
        "finite_grid_local_cases.csv",
        "mechanism_pattern_route_ledger.csv",
        "conditionality_context_records.csv",
        "direct_identification_audits.csv",
        "pattern_expansion_screening.csv",
        "high_information_identification_coverage.csv",
        "impatiens_identification_retrofit.json",
    ):
        assert expected in names
    assert "Identification-design additions" in manifest
    assert "screened-set coverage, not literature prevalence" in manifest


def test_cover_letter_matches_under_30_page_identification_package() -> None:
    text = COVER.read_text(encoding="utf-8")
    assert "From floral trait interactions to mechanism identification" in text
    assert "currently renders to **27 Main Document pages**" in text
    assert "11-page Appendix S1" in text
    assert "within the standard 30-page Concepts & Synthesis target" in text
    assert "## 1. Broad ecological contribution of the additional length" not in text
    assert "one-sided mechanistic bound" not in text
    assert "acceptance stage" in text
    assert "Potential reviewers, if requested by the submission portal" in text


def test_canonical_builder_preserves_historical_manuscript_file() -> None:
    assert (ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md").exists()
    source = SCRIPT.read_text(encoding="utf-8")
    assert "build_identification_candidate_package_sources" in source
    assert "historical theorem-led manuscript remains" in source
