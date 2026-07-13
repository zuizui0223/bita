from __future__ import annotations

import importlib.util
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "build_part_i_manuscript_readout.py"
SPEC = importlib.util.spec_from_file_location("build_part_i_manuscript_readout", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def test_build_readout_reports_conditional_regimes_without_structural_overclaim() -> None:
    case_rows = [
        {
            "sign": "complementary",
            "parameter_scenario_id": "high_tracking",
            "form_id": "baseline",
            "pollinator_service": "0.2",
            "floral_damage_pressure": "0.8",
        },
        {
            "sign": "substitutable",
            "parameter_scenario_id": "high_obstruction",
            "form_id": "baseline",
            "pollinator_service": "0.8",
            "floral_damage_pressure": "0.2",
        },
    ]
    form_summary_rows = [
        {"functional_form_class": "tested_set_unanimous"},
        {"functional_form_class": "mixed_or_sensitive"},
    ]
    envelope_rows = [
        {"envelope_class": "conditional_majority"},
        {"envelope_class": "mixed_or_sensitive"},
    ]

    text = MODULE.build_readout(case_rows, form_summary_rows, envelope_rows)

    assert "conditional attraction-defence regimes" in text
    assert "High attraction tracking" in text
    assert "theoretical sign frequencies" in text
    assert "not an empirical parameter calibration" in text
    assert "tested_set_unanimous" in text
    assert "not proof of mathematical structural robustness" in text
    assert "Impatiens" not in text
