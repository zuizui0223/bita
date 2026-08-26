from pathlib import Path

from scripts.build_identification_candidate_package_sources import (
    build_main_source,
    build_supplement_source,
)


def test_candidate_main_is_identification_led() -> None:
    text = build_main_source()
    assert "From floral trait interactions to mechanism identification" in text
    assert "## 3. A crossed intervention design for channel identification" in text
    assert "A×D×G×P" in text
    assert "Kessler et al. (2008)" in text
    assert "Egan et al. (2021)" in text
    assert "2,592" not in text.split("## References", 1)[0]
    assert "77.2%" not in text.split("## References", 1)[0]
    assert "Theorem 1" not in text


def test_candidate_main_has_five_figure_pages_without_blank_leader() -> None:
    text = build_main_source()
    for idx in range(1, 6):
        assert f"FIGURE_{idx}_IDENTIFICATION_DESIGN.svg" in text
        assert f"**Figure {idx}." in text
    # The References section break already starts Figure 1 on a new page.
    # Only Figures 2–5 need explicit page breaks; requiring five creates an
    # otherwise blank page between References and Figure 1.
    assert text.count("[[ECOLOGY_PAGE_BREAK]]") == 4
    ref_break = text.index("[[ECOLOGY_SECTION_BREAK_AFTER_REFERENCES]]")
    fig1 = text.index("**Figure 1.")
    assert ref_break < fig1
    assert "[[ECOLOGY_PAGE_BREAK]]" not in text[ref_break:fig1]


def test_candidate_main_has_focused_references() -> None:
    text = build_main_source()
    assert text.count("https://doi.org/") == 12
    assert "10.1126/science.1160072" in text
    assert "10.1002/evl3.262" in text
    assert "Leal et al." not in text
    assert "Sasidharan" not in text


def test_candidate_supplement_keeps_demoted_technical_material() -> None:
    text = build_supplement_source()
    assert "2,592" in text
    assert "77.2%" in text
    assert "KESSLER_2008_IDENTIFICATION_REAUDIT_V2.md" in text
    assert "IMPATIENS_2018_IDENTIFICATION_RETROFIT_V1.json" in text
    assert "HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V1.csv" in text
    assert "FIGURE_S1_DERIVATIVE_AGREEMENT.svg" in text
    assert "FIGURE_S2_SCENARIO_SIGN_MAPS.svg" in text


def test_candidate_package_does_not_overwrite_canonical_paths() -> None:
    source = Path("scripts/build_identification_candidate_package_sources.py").read_text(encoding="utf-8")
    assert '"identification_candidate"' in source
    assert 'OUT / "MANUSCRIPT_IDENTIFICATION_CANDIDATE.md"' in source
    assert 'OUT / "APPENDIX_IDENTIFICATION_CANDIDATE.md"' in source
