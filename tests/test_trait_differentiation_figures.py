"""Basic publication guards for the new Chapter 2 SVG figure sources."""

from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
FIGDIR = ROOT / "manuscript" / "trait_differentiation_figures"
FIG1 = FIGDIR / "FIGURE_1_BALANCE_TO_DIFFERENTIATION.svg"
FIG2 = FIGDIR / "FIGURE_2_ARCHITECTURE_BOUNDARY.svg"
FIG3 = FIGDIR / "FIGURE_3_ROBUSTNESS_AND_REALITY.svg"


def _parse(path: Path) -> str:
    ElementTree.parse(path)
    return path.read_text(encoding="utf-8")


def test_trait_differentiation_figures_are_valid_svg_xml() -> None:
    for path in (FIG1, FIG2, FIG3):
        assert path.exists(), path
        _parse(path)


def test_figure1_contains_the_chapter2_identity_and_partial_differentiation() -> None:
    text = _parse(FIG1)
    for token in (
        "Shared axis: BALANCE",
        "Two axes: DIFFERENTIATION",
        "decoupling fraction",
        "R = s L",
        "architecture cost",
        "partial differentiation",
    ):
        assert token in text, token


def test_figure2_contains_the_architecture_boundary_and_coupling_shift() -> None:
    text = _parse(FIG2)
    for token in (
        "shared-axis conflict load",
        "extra architecture cost",
        "s = 1.0",
        "s = 0.6",
        "s = 0.3",
        "Residual coupling",
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
