"""Publication guards for the integrated Chapter 2 SVG figure sources."""

from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
FIGDIR = ROOT / "manuscript" / "trait_differentiation_figures"
FIG1 = FIGDIR / "FIGURE_1_BALANCE_TO_DIFFERENTIATION.svg"
FIG2 = FIGDIR / "FIGURE_2_ARCHITECTURE_BOUNDARY.svg"
FIG3 = FIGDIR / "FIGURE_3_ROBUSTNESS_AND_REALITY.svg"
FIG4 = FIGDIR / "FIGURE_4_MECHANISM_IDENTIFICATION.svg"
FIG5 = FIGDIR / "FIGURE_5_FRAGMENTED_IDENTIFICATION.svg"


def _parse(path: Path) -> str:
    ElementTree.parse(path)
    return path.read_text(encoding="utf-8")


def test_trait_differentiation_figures_are_valid_svg_xml() -> None:
    for path in (FIG1, FIG2, FIG3, FIG4, FIG5):
        assert path.exists(), path
        _parse(path)


def test_figure1_separates_general_rule_from_quadratic_corollary() -> None:
    text = _parse(FIG1)
    for token in (
        "Shared axis: BALANCE",
        "Two axes: DIFFERENTIATION",
        "recoverable compromise loss",
        "R ≥ 0",
        "Δ",
        "= R − K",
        "quadratic corollary",
        "R = s L",
        "partial differentiation",
    ):
        assert token in text, token


def test_figure2_is_explicitly_a_quadratic_boundary_visualization() -> None:
    text = _parse(FIG2)
    for token in (
        "Quadratic corollary",
        "General rule: Δarch = R − K",
        "quadratic baseline: R = s L_S*",
        "shared-axis conflict load",
        "extra architecture cost",
        "s = 1.0",
        "s = 0.6",
        "s = 0.3",
        "not a universal linear boundary",
    ):
        assert token in text, token


def test_figure3_reports_registered_robustness_without_estimating_empirical_s() -> None:
    text = _parse(FIG3)
    for token in (
        "N = 300",
        "300 / 300",
        "60 / 60",
        "cichlid oral + pharyngeal jaws",
        "Dalechampia",
        "not an estimate of s",
    ):
        assert token in text, token


def test_figure4_keeps_differentiation_separate_from_mechanism_identification() -> None:
    text = _parse(FIG4)
    for token in (
        "Once multiple trait axes exist",
        "do not infer differentiation from their interaction",
        "A×D×G×P",
        "four-way separability",
        "independent A×D assay",
        "Trait differentiation answers where functions are carried",
    ):
        assert token in text, token


def test_figure5_reports_fragmented_identification_not_differentiation_prevalence() -> None:
    text = _parse(FIG5)
    for token in (
        "Kessler 2008",
        "Egan 2021",
        "Impatiens public reanalysis",
        "56 source-adjudicated route records",
        "25 independent biological clusters",
        "17 high-information systems screened",
        "fragmented identification",
    ):
        assert token in text, token
