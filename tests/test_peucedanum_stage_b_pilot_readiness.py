from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from scripts.assemble_peucedanum_stage_b_pilot_readiness import (
    ATTEMPT_FIELDS,
    PILOT_SCHEMA,
    assemble,
    read_attempt_rows,
)
from scripts.evaluate_peucedanum_stage_b_manipulation import REQUIRED_FIELDS as VALIDATION_FIELDS


def _common_support() -> dict:
    ids = [f"U{q}_{i:02d}" for q in (20, 40, 60) for i in range(9)]
    return {
        "schema_version": "BITA_PEUCEDANUM_STAGE_B_COMMON_SUPPORT_V1",
        "retained_total": 20,
        "q_targets": [0.2, 0.4, 0.6],
        "presurvey": {
            "eligible_unit_ids": ids,
            "common_eligible_fraction": 0.50,
            "common_eligible_fraction_wilson_lower95": 0.38,
        },
    }


def _attempts() -> list[dict[str, str]]:
    rows = []
    for q_code, q in ((20, 0.2), (40, 0.4), (60, 0.6)):
        for i in range(9):
            qualified = i < 8
            rows.append(
                {
                    "unit_id": f"U{q_code}_{i:02d}",
                    "q_target": str(q),
                    "common_support_eligible": "1",
                    "manipulation_attempted": "1",
                    "manipulation_qualified": "1" if qualified else "0",
                    "failure_reason": "" if qualified else "q_realization_outside_pilot_bound",
                }
            )
    return rows


def _validation_rows() -> list[dict[str, str]]:
    rows = []
    for q_code, q, perfect in ((20, 0.2, 4), (40, 0.4, 8), (60, 0.6, 12)):
        male = 20 - perfect
        for i in range(8):
            rows.append(
                {
                    "unit_id": f"U{q_code}_{i:02d}",
                    "block_id": f"B{i:02d}",
                    "q_target": str(q),
                    "q_realized": str(q),
                    "total_before": "30",
                    "total_retained": "20",
                    "perfect_retained": str(perfect),
                    "male_retained": str(male),
                    "classification_checked_n": "20",
                    "classification_correct_n": "20",
                    "eggs_before_manipulation": "0",
                    "removal_load": "10",
                    "handling_actions": "12",
                    "mechanical_damage_count": "0",
                    "male_phase_complete": "1",
                    "flower_height": str(10 + i),
                    "flowering_day": str(20 + i),
                }
            )
    return rows


def _validation_config() -> dict:
    return {
        "status": "TEST_ONLY",
        "min_q_levels": 3,
        "min_units_per_q_level": 8,
        "target_total_retained_count": 20,
        "max_abs_q_realization_error": 0.01,
        "min_q_target_separation": 0.19,
        "min_classification_accuracy_lower95": 0.98,
        "max_pre_manipulation_egg_positive_fraction": 0.0,
        "max_mean_pre_manipulation_eggs": 0.0,
        "max_total_retained_relative_deviation": 0.0,
        "max_handling_group_relative_range": 0.05,
        "max_abs_pretreatment_group_smd": 0.05,
        "max_mechanical_damage_rate": 0.01,
        "max_mechanical_damage_group_difference": 0.01,
        "min_male_phase_complete_fraction": 0.95,
    }


def _pilot_config() -> dict:
    return {
        "status": "TEST_ONLY",
        "min_attempted_per_q_level": 9,
        "min_qualified_per_q_level": 8,
        "min_overall_qualification_fraction": 0.85,
        "min_qualification_fraction_per_q_level": 0.85,
        "max_qualification_fraction_difference_across_q": 0.05,
    }


def _write(path: Path, rows: list[dict[str, str]], fields: tuple[str, ...]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def test_positive_pilot_recovers_feasibility_and_failure_rate() -> None:
    receipt = assemble(
        _common_support(),
        _attempts(),
        _validation_rows(),
        _validation_config(),
        _pilot_config(),
    )
    assert receipt["receipt_schema_version"] == PILOT_SCHEMA
    assert receipt["status"] == "PEUCEDANUM_STAGE_B_TECHNICAL_PILOT_PASSED"
    assert all(receipt["gates"].values())
    assert receipt["pilot_attempts"]["attempted_total"] == 27
    assert receipt["pilot_attempts"]["qualified_total"] == 24
    assert receipt["pilot_attempts"]["overall_qualification_fraction"] == pytest.approx(24 / 27)
    assert receipt["pilot_attempts"]["observed_pre_g_qualification_failure_fraction"] == pytest.approx(3 / 27)
    assert receipt["pilot_attempts"]["conservative_planning_failure_fraction_from_wilson_lower95"] > 3 / 27


def test_attempted_unit_outside_common_support_is_rejected() -> None:
    attempts = _attempts()
    attempts[0]["unit_id"] = "NOT_ELIGIBLE"
    with pytest.raises(ValueError, match="outside common support"):
        assemble(_common_support(), attempts, _validation_rows(), _validation_config(), _pilot_config())


def test_pilot_q_levels_must_match_common_support_design() -> None:
    attempts = _attempts()
    for row in attempts:
        if row["q_target"] == "0.6":
            row["q_target"] = "0.7"
    with pytest.raises(ValueError, match="must exactly match"):
        assemble(_common_support(), attempts, _validation_rows(), _validation_config(), _pilot_config())


def test_validation_rows_must_match_qualified_attempts() -> None:
    validation = _validation_rows()[1:]
    with pytest.raises(ValueError, match="exactly the manipulation-qualified"):
        assemble(_common_support(), _attempts(), validation, _validation_config(), _pilot_config())


def test_attempt_ledger_rejects_noneligible_attempt(tmp_path: Path) -> None:
    rows = _attempts()
    rows[0]["common_support_eligible"] = "0"
    path = tmp_path / "attempts.csv"
    _write(path, rows, ATTEMPT_FIELDS)
    with pytest.raises(ValueError, match="cannot be manipulation_attempted"):
        read_attempt_rows(path)


def test_pilot_config_fails_closed_until_thresholds_are_preregistered() -> None:
    config = _pilot_config()
    config["min_overall_qualification_fraction"] = "REQUIRED_BEFORE_USE"
    with pytest.raises(ValueError, match="must be preregistered"):
        assemble(_common_support(), _attempts(), _validation_rows(), _validation_config(), config)


def test_registered_attempt_and_config_templates_are_fail_closed() -> None:
    root = Path(__file__).resolve().parents[1]
    attempt_path = root / "empirical" / "identification_design" / "PEUCEDANUM_STAGE_B_PILOT_ATTEMPT_LEDGER_V1.csv"
    config_path = root / "empirical" / "identification_design" / "PEUCEDANUM_STAGE_B_PILOT_CONFIG_TEMPLATE_V1.json"
    with attempt_path.open(encoding="utf-8", newline="") as handle:
        assert tuple(next(csv.reader(handle))) == ATTEMPT_FIELDS
    config = json.loads(config_path.read_text(encoding="utf-8"))
    assert "DO_NOT_RUN" in config["status"]
    assert config["min_attempted_per_q_level"] == "REQUIRED_BEFORE_USE"
