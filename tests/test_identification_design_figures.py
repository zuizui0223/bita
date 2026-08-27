from pathlib import Path
import xml.etree.ElementTree as ET

from scripts.build_identification_design_figures_svg import build, _impatiens_targets, _read_coverage


def test_figure_inputs_have_expected_fixed_states() -> None:
    assert len(_read_coverage()) == 17
    targets = _impatiens_targets()
    assert len(targets) == 8
    assert all(float(row["lo"]) < 0 < float(row["hi"]) for row in targets)


def test_builds_five_valid_svg_files(tmp_path: Path) -> None:
    paths = build(tmp_path)
    assert len(paths) == 5
    for path in paths:
        assert path.exists()
        root = ET.fromstring(path.read_text(encoding="utf-8"))
        assert root.tag.endswith("svg")


def test_main_messages_are_present(tmp_path: Path) -> None:
    paths = build(tmp_path)
    texts = [path.read_text(encoding="utf-8") for path in paths]
    assert "Interaction detection ≠ mechanism allocation" in texts[0]
    assert "A×D×G×P four-way coupling" in texts[1]
    assert "Do not define the joint cost as a residual" in texts[2]
    assert "closure of these faces in one valid A×D×G×P experiment" in texts[3]
    assert "A×G×Pₛ — Theis 2012" in texts[3]
    assert "17-system frontier" in texts[3]
    assert "All eight target intervals cross zero" in texts[3]
    assert "An executable path from interaction detection to mechanism identification" in texts[4]
