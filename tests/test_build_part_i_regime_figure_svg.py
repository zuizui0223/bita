from __future__ import annotations

import importlib.util
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "build_part_i_regime_figure_svg.py"
SPEC = importlib.util.spec_from_file_location("build_part_i_regime_figure_svg", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def test_build_svg_contains_three_manuscript_panels() -> None:
    rows = []
    for scenario, form, p, h, sign in [
        ("baseline", "baseline", "0.2", "0.2", "substitutable"),
        ("baseline", "saturating_attraction", "0.2", "0.8", "complementary"),
        ("high_tracking", "baseline", "0.8", "0.8", "complementary"),
        ("high_obstruction", "saturating_attraction", "0.8", "0.2", "substitutable"),
    ]:
        rows.append({
            "parameter_scenario_id": scenario,
            "form_id": form,
            "pollinator_service": p,
            "floral_damage_pressure": h,
            "sign": sign,
        })

    svg = MODULE.build_svg(rows)

    assert svg.startswith("<svg")
    assert "A  Biological parameter scenarios" in svg
    assert "B  Interaction environment" in svg
    assert "C  Endpoint-normalized response shapes" in svg
    assert "common endpoint scales" in svg
    assert "not empirical probabilities" in svg
