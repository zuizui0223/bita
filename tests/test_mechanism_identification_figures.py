from pathlib import Path

from scripts import build_mechanism_identification_figures_svg as figures


def test_empirical_figure_inputs_are_authoritative_v2() -> None:
    rows = figures.legacy._read_coverage()
    counts = figures.legacy._pattern_counts()
    assert len(rows) == 17
    assert counts == {
        "records": 56,
        "clusters": 25,
        "a_poll": 5,
        "a_ant": 8,
        "d_ant": 18,
        "d_poll": 10,
        "same": 14,
        "switch": 17,
    }


def test_builds_five_active_mechanism_figures(tmp_path: Path) -> None:
    paths = figures.build(tmp_path)
    assert [p.name for p in paths] == figures.FIGURE_NAMES
    assert len(paths) == 5
    for path in paths:
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        assert text.startswith("<svg")
        assert "</svg>" in text


def test_figure_1_keeps_outcome_levels_distinct() -> None:
    text = figures.fig1()
    assert "Level 1 — interaction relief" in text
    assert "Level 2 — constraint release" in text
    assert "Level 3 — strict reversal" in text
    assert "Level 3 ⇒ Level 2 ⇒ Level 1" in text


def test_figure_2_is_identified_set_not_theorem_overclaim() -> None:
    text = figures.fig2()
    assert "identified set" in text.lower()
    assert "B = δ + κΔ" in text
    assert "κΔ ≥ 0 ⇒ ρΔ−ιΔ ≥ δ" in text
    assert "More precision in δ alone does not collapse I(δ)." in text


def test_figure_3_preserves_causal_gates() -> None:
    text = figures.fig3()
    assert "A×D×G×P = 0?" in text
    assert "m0,Δ" in text
    assert "Independent remaining-channel assay" in text
    assert "Residual by subtraction ≠ identified joint cost." in text


def test_figure_4_is_source_backed() -> None:
    text = figures.fig4()
    assert "56 routes / 25 clusters" in text
    assert "17-system" in text
    assert "independent κ assay 0" in text
    assert "full channel allocation 0" in text


def test_figure_5_enforces_programme_ownership() -> None:
    text = figures.fig5()
    assert "SCH — identify conflict" in text
    assert "SLK — transport evolutionary value" in text
    assert "BITA — identify mechanism" in text
    assert "Architecture-value equations are programme context here" in text
