from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from scripts.analyze_bita_dimensional_release import read_rows
from trait_architecture.dimensional_release import REQUIRED_FIELDS


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "empirical" / "identification_design" / "BITA_DIMENSIONAL_RELEASE_TEMPLATE_V1.csv"
CONFIG = ROOT / "empirical" / "identification_design" / "BITA_DIMENSIONAL_RELEASE_CONFIG_TEMPLATE_V1.json"
CONTRACT = ROOT / "docs" / "BITA_EMPIRICAL_DIMENSIONAL_RELEASE_ANALYSIS_V1.md"
SPINE = ROOT / "docs" / "BITA_EXECUTION_SPINE_V1.md"


def test_template_and_config_are_registered_fail_closed_inputs() -> None:
    with TEMPLATE.open(encoding="utf-8", newline="") as handle:
        assert tuple(next(csv.reader(handle))) == REQUIRED_FIELDS
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    assert config["min_dimensional_release"] == "REQUIRED_BEFORE_USE"
    assert config["min_y_function2_gain"] == "REQUIRED_BEFORE_USE"
    assert "DO_NOT_RUN" in config["status"]


def test_contract_keeps_within_bita_gain_separate_from_delta_mod() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    assert "within_bita_optimum_fitness_gain" in text
    assert "and **not** `Delta_mod`" in text
    assert "NOT_IDENTIFIED_UNLESS_SHARED_AND_DIFFERENTIATED_FITNESS_SCALES_ARE_EXPLICITLY_COMMENSURABLE" in text
    assert "contemporary dimensional release is not historical modularization" in text


def test_execution_spine_requires_sch_handoff_before_release() -> None:
    text = SPINE.read_text(encoding="utf-8")
    assert "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE" in text
    assert "BITA does not re-estimate or redefine the Chapter-1 optimum" in text
    assert "x optimum moves toward SCH z_function1" in text
    assert "MECHANISM_ALLOCATION_UNRESOLVED" in text


def test_cli_reader_rejects_duplicate_units(tmp_path: Path) -> None:
    path = tmp_path / "bad.csv"
    path.write_text(
        ",".join(REQUIRED_FIELDS)
        + "\n"
        + "P1,U1,X0,0,0,1,1,1\n"
        + "P1,U1,X1,1,1,1,1,1\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="duplicate unit_id"):
        read_rows(path)
