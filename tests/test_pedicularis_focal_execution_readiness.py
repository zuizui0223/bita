from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_pedicularis_focal_execution_readiness.py"
TEMPLATE = ROOT / "empirical" / "identification_design" / "PEDICULARIS_DIMENSIONAL_RELEASE_TEMPLATE_V1.csv"
CONFIG = ROOT / "empirical" / "identification_design" / "PEDICULARIS_DIMENSIONAL_RELEASE_CONFIG_TEMPLATE_V1.json"

SPEC = importlib.util.spec_from_file_location("pedicularis_focal_readiness", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_repository_template_is_explicitly_not_ready() -> None:
    result = MODULE.evaluate(TEMPLATE, CONFIG)
    assert result["status"] == "NOT_READY_FOR_FOCAL_C1_C3_ANALYSIS"
    assert result["gates"]["E0_thresholds_frozen"]["pass"] is False
    assert result["gates"]["E1_non_circular_sch_handoff"]["pass"] is False
    assert result["gates"]["E2_registered_xy_surface_present"]["pass"] is False
    assert result["gates"]["E2_registered_xy_surface_present"]["n_rows"] == 0


def test_ready_package_passes_all_three_preanalysis_gates(tmp_path: Path) -> None:
    raw = tmp_path / "raw.csv"
    header = TEMPLATE.read_text(encoding="utf-8").strip()
    rows = [header]
    flower = 0
    for water in ("DRAINED", "PROTECTED"):
        for x in range(5):
            flower += 1
            rows.append(
                f"POP1,2026,P{flower},F{flower},X{x},{float(x)},{water},20,10,2,100,3,1.0,0"
            )
    raw.write_text("\n".join(rows) + "\n", encoding="utf-8")

    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    cfg["bita_release"].update(
        {
            "min_dimensional_release": 0.1,
            "min_within_bita_fitness_gain": 1.0,
            "min_y_function2_gain": 0.01,
            "max_y_function1_penalty": 5.0,
            "min_y1_interior_bootstrap_fraction": 0.7,
        }
    )
    cfg["status"] = "FROZEN_BEFORE_FOCAL_OUTCOME_ANALYSIS"
    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(json.dumps(cfg), encoding="utf-8")

    sch = {
        "receipt_schema_version": "SCH_CAUSAL_COMPROMISE_STATE_OPTIMA_V1",
        "status": "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE",
        "system": "Pedicularis rex",
        "population_id": "POP1",
        "season_id": "2026",
        "system_wrapper_schema_version": "SCH_PEDICULARIS_FULL_SURFACE_WRAPPER_V2",
        "pedicularis_state_mapping": {
            "G0": "SEED_PREDATOR_INDEPENDENTLY_EXCLUDED",
            "G1": "SEED_PREDATOR_EXPOSED",
            "water_y": "HELD_FIXED_ACROSS_ALL_SCH_CELLS",
        },
        "readiness_reference": {
            "g_schema": "SCH_PEDICULARIS_PREDATOR_METHOD_V3",
            "predator_method_requirement": "POST_POLLINATION_WITH_POLLINATOR_ACCESS_PRESERVED",
        },
    }
    sch_path = tmp_path / "sch.json"
    sch_path.write_text(json.dumps(sch), encoding="utf-8")

    result = MODULE.evaluate(raw, cfg_path, sch_path)
    assert result["status"] == "READY_FOR_FOCAL_C1_C3_ANALYSIS"
    assert all(gate["pass"] for gate in result["gates"].values())
