from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_supplementary_figures_svg.py"
RUNNER = ROOT / "scripts" / "run_part_i_robustness.py"
CONFIG = ROOT / "configs" / "part_i_robustness_grid.json"


def _load_builder():
    spec = importlib.util.spec_from_file_location("suppfig", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _evaluation_csv(tmp_path: Path) -> Path:
    out = tmp_path / "part_i"
    subprocess.run([sys.executable, str(RUNNER), str(CONFIG), str(out)], cwd=ROOT, check=True)
    return out / "part_i_sensitivity_evaluations.csv"


def test_derivative_agreement_is_numerically_tight(tmp_path: Path) -> None:
    builder = _load_builder()
    rows = builder.read_evaluations(_evaluation_csv(tmp_path))
    assert len(rows) == 2592
    grouped = builder.derivative_agreement(rows)
    assert len(grouped) == 4
    assert all(len(points) == 648 for points in grouped.values())
    max_error = max(error for points in grouped.values() for _, _, error in points)
    assert max_error < 2e-6


def test_same_system_matrix_uses_saturated_14_cluster_universe() -> None:
    builder = _load_builder()
    matrix = builder.same_system_routes()
    assert len(matrix) == 14
    assert all(len(routes) >= 2 for routes in matrix.values())


def test_all_four_supplementary_figures_build(tmp_path: Path) -> None:
    builder = _load_builder()
    outdir = tmp_path / "figures"
    outputs = builder.write_all(_evaluation_csv(tmp_path), outdir)
    assert set(outputs) == {
        "FIGURE_S1_DERIVATIVE_AGREEMENT.svg",
        "FIGURE_S2_SCENARIO_SIGN_MAPS.svg",
        "FIGURE_S3_SAME_SYSTEM_ROUTE_MATRIX.svg",
        "FIGURE_S4_QUANTITATIVE_ROBUSTNESS.svg",
    }
    for path in outputs.values():
        text = path.read_text(encoding="utf-8")
        assert text.startswith("<svg")
        assert "not prevalence" in text or "not empirical validation" in text or "not effect sizes" in text or "not W_AD" in text

    s4 = outputs["FIGURE_S4_QUANTITATIVE_ROBUSTNESS.svg"].read_text(encoding="utf-8")
    assert "32/32" in s4
    assert "99.5%" in s4
    assert "99.3%" in s4
    assert "97.5%" in s4
    assert "+0.129" in s4
