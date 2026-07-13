from __future__ import annotations

import importlib.util
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "build_part_i_manuscript_readout.py"
SPEC = importlib.util.spec_from_file_location("build_part_i_manuscript_readout", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def test_build_readout_derives_results_without_hard_coded_manuscript_numbers() -> None:
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
    full_tested_set_rows = [
        {"full_tested_set_class": "mixed_or_sensitive"},
        {"full_tested_set_class": "mixed_or_sensitive"},
    ]

    text = MODULE.build_readout(case_rows, form_summary_rows, full_tested_set_rows)

    assert "Part I sensitivity readout v2" in text
    assert "conditional attraction–defence regimes" in text
    assert "endpoint-normalized response-shape" in text
    assert "unweighted occupancy fractions" in text
    assert "not an empirical parameter calibration" in text
    assert "tested_set_unanimous" in text
    assert "mathematical structural robustness" in text
    assert "No arbitrary majority threshold" in text
    assert "conditional_majority" not in text
    assert "predeclared" not in text
    assert "`high_tracking`" in text
    assert "100.0%" in text
    assert "92.1%" not in text
    assert "395 of 648" not in text
    assert "Impatiens" not in text
