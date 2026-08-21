from __future__ import annotations

from pathlib import Path
import importlib.util


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_ecology_submission_sources.py"

spec = importlib.util.spec_from_file_location("ecology_builder", SCRIPT)
assert spec and spec.loader
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def test_main_submission_source_matches_ecology_component_order() -> None:
    text = builder.build_main_submission_source()
    ordered = [
        "**Journal:** Ecology",
        "**Manuscript type:** Concepts & Synthesis",
        "**Open Research statement:**",
        "**Key words/phrases:**",
        builder.TITLE_SECTION_BREAK,
        "## Abstract",
        "## 1. Introduction",
        "## Acknowledgments",
        "## Author Contributions",
        "## Conflict of Interest Statement",
        "## References",
        builder.REF_SECTION_BREAK,
        "## Table 1.",
        "## Table 2.",
        "## Table 3.",
        "## Table 4.",
        "## Figure captions",
        "**Figure 1**",
        "**Figure 2**",
        "**Figure 3**",
    ]
    positions = [text.index(token) for token in ordered]
    assert positions == sorted(positions)


def test_ecology_submission_uses_appendix_callout_style() -> None:
    text = builder.build_main_submission_source()
    assert "Supplementary Fig." not in text
    assert "Supplementary Figs." not in text
    assert "Tables S1–S6" not in text
    assert "Appendix S1: Figures S1–S2" in text
    assert "Appendix S1: Figures S3–S4" in text
    assert "machine-readable Open Research data products" in text


def test_appendix_is_reader_facing_not_spreadsheet_container() -> None:
    text = builder.build_appendix_source()
    assert text.startswith("# Appendix S1")
    assert "**Journal:** Ecology" in text
    for idx in range(1, 5):
        assert f"### Figure S{idx}" in text
    for idx in range(1, 7):
        assert f"Table S{idx}" not in text
    assert "machine-readable data products" in text
    assert "## References" in text


def test_open_research_deposition_names_do_not_use_item_s_labels(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(builder, "OUT", tmp_path)
    monkeypatch.setattr(builder, "DATA_OUT", tmp_path / "open_research_data")
    manifest = builder.build_open_research_manifest()
    expected = {
        "model_parameters_and_scaling.csv",
        "finite_grid_local_cases.csv",
        "mechanism_pattern_route_ledger.csv",
        "conditionality_context_records.csv",
        "direct_identification_audits.csv",
        "pattern_expansion_screening.csv",
    }
    assert expected == {p.name for p in (tmp_path / "open_research_data").glob("*.csv")}
    assert "TABLE_S" not in "\n".join(expected)
    assert "ESA's Open Research policy" in manifest


def test_title_page_keywords_are_not_repeated_after_abstract() -> None:
    text = builder.build_main_submission_source()
    assert text.count("**Key words/phrases:**") == 1
    abstract = text.split("## Abstract", 1)[1].split("## 1. Introduction", 1)[0]
    assert "**Keywords:**" not in abstract
