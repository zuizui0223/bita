import importlib.util
import math
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).parents[1] / "scripts" / "run_part_i_robustness.py"
SPEC = importlib.util.spec_from_file_location("part_i_robustness_runner", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def minimal_config() -> dict:
    return {
        "neutral_tolerance": 1e-12,
        "phenotype_and_regime_grid": {
            "attraction": [0.5],
            "defence": [0.5],
            "assurance": [0.0],
            "pollinator_service": [0.5],
            "floral_damage_pressure": [0.5],
        },
        "parameter_scenarios": [
            {"scenario_id": "baseline", "overrides": {}},
            {"scenario_id": "high_damage", "overrides": {"attraction_tracking": 2.0}},
        ],
        "functional_forms": [
            {
                "form_id": "baseline",
                "attraction_saturation": 0.0,
                "defence_saturation": 0.0,
                "joint_cost_curvature": 0.0,
            },
            {
                "form_id": "saturated",
                "attraction_saturation": 1.0,
                "defence_saturation": 2.0,
                "joint_cost_curvature": 1.0,
            },
        ],
    }


def test_run_emits_evaluation_response_shape_and_full_tested_set_summaries() -> None:
    config = minimal_config()
    rows, form_summaries, full_tested_set_summaries = MODULE.run(config)

    assert len(rows) == 4
    assert len(form_summaries) == 2
    assert len(full_tested_set_summaries) == 1
    assert full_tested_set_summaries[0]["total_evaluation_count"] == 4
    assert full_tested_set_summaries[0]["parameter_scenario_count"] == 2
    assert {row["parameter_scenario_id"] for row in rows} == {"baseline", "high_damage"}
    assert {row["parameter_scenario_id"] for row in form_summaries} == {"baseline", "high_damage"}
    assert {row["form_id"] for row in rows} == {"baseline", "saturated"}
    assert {row["defence_saturation"] for row in rows} == {0.0, 2.0}
    assert {row["joint_cost_curvature"] for row in rows} == {0.0, 1.0}
    assert "joint_cost_curvature_term" in rows[0]
    assert "shared_cost_term" not in rows[0]
    assert "full_tested_set_class" in full_tested_set_summaries[0]
    assert "envelope_class" not in full_tested_set_summaries[0]

    report = MODULE.build_report(config, rows, form_summaries, full_tested_set_summaries)
    assert report["run_id"] == "endpoint_normalized_grid_v2"
    assert report["neutral_tolerance"] == 1e-12
    assert report["neutral_tolerance_scale"] == "absolute_on_declared_score_scale"
    assert report["response_shape_normalization"] == "common_endpoints_on_unit_trait_domain"
    assert report["finite_design_measure"] == "unweighted_count_over_declared_grid"
    assert set(report["functional_form_class_counts"]) == {
        "tested_set_unanimous",
        "mixed_or_sensitive",
    }
    assert set(report["full_tested_set_class_counts"]) == {
        "tested_set_unanimous",
        "mixed_or_sensitive",
    }


def test_rejects_unknown_model_parameter_override() -> None:
    config = minimal_config()
    config["parameter_scenarios"][0]["overrides"] = {"not_a_parameter": 1.0}
    with pytest.raises(ValueError, match="unknown ModelParameters field"):
        MODULE.run(config)


def test_rejects_nonfinite_neutral_tolerance() -> None:
    config = minimal_config()
    config["neutral_tolerance"] = math.nan
    with pytest.raises(ValueError, match="finite and non-negative"):
        MODULE.run(config)
