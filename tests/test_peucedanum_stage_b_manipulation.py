from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from scripts.evaluate_peucedanum_stage_b_manipulation import (
    RECEIPT_SCHEMA,
    REQUIRED_FIELDS,
    analyze,
    read_rows,
)


def _config() -> dict:
    return {
        "status": "TEST_ONLY",
        "min_q_levels": 3,
        "min_units_per_q_level": 12,
        "target_total_retained_count": 40,
        "max_abs_q_realization_error": 0.01,
        "min_q_target_separation": 0.20,
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


def _rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for q in (0.25, 0.50, 0.75):
        perfect = 40 * q
        male = 40 - perfect
        for i in range(12):
            total_before = 50 + (i % 4)
            rows.append(
                {
                    "unit_id": f"U_{q}_{i}",
                    "block_id": f"B{i:02d}",
                    "q_target": f"{q:.2f}",
                    "q_realized": f"{q:.2f}",
                    "total_before": str(total_before),
                    "total_retained": "40",
                    "perfect_retained": f"{perfect:.6f}",
                    "male_retained": f"{male:.6f}",
                    "classification_checked_n": "20",
                    "classification_correct_n": "20",
                    "eggs_before_manipulation": "0",
                    "removal_load": str(total_before - 40),
                    "handling_actions": "20",
                    "mechanical_damage_count": "0",
                    "male_phase_complete": "1",
                    "flower_height": str(10 + (i % 3)),
                    "flowering_day": str(20 + (i % 5)),
                }
            )
    return rows


def _write(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REQUIRED_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def test_positive_control_validates_post_male_phase_q_manipulation() -> None:
    receipt = analyze(_rows(), _config())
    assert receipt["receipt_schema_version"] == RECEIPT_SCHEMA
    assert receipt["status"] == "PEUCEDANUM_STAGE_B_SEX_COMPOSITION_MANIPULATION_VALIDATED"
    assert all(receipt["gates"].values())
    assert receipt["q_realization"]["max_abs_error"] == 0
    assert receipt["classification"]["wilson_lower_95"] > 0.98
    assert receipt["pre_manipulation_oviposition"]["positive_fraction"] == 0
    assert receipt["fixed_total"]["max_relative_deviation"] == 0
    assert receipt["pretreatment_balance"]["max_abs_smd"] == 0
    assert "does_not_itself_estimate_q_fitness_effect" in receipt["claim_ceiling"]


def test_negative_control_rejects_bad_sex_classification() -> None:
    rows = _rows()
    for row in rows:
        row["classification_correct_n"] = "15"
    receipt = analyze(rows, _config())
    assert receipt["status"] == "PEUCEDANUM_STAGE_B_MANIPULATION_NOT_VALIDATED"
    assert receipt["gates"]["sex_classification_accuracy"] is False


def test_negative_control_rejects_preexisting_oviposition() -> None:
    rows = _rows()
    rows[0]["eggs_before_manipulation"] = "1"
    receipt = analyze(rows, _config())
    assert receipt["status"] == "PEUCEDANUM_STAGE_B_MANIPULATION_NOT_VALIDATED"
    assert receipt["gates"]["negligible_pre_manipulation_oviposition"] is False


def test_config_fails_closed_before_preregistration() -> None:
    config = _config()
    config["max_abs_q_realization_error"] = "REQUIRED_BEFORE_USE"
    with pytest.raises(ValueError, match="preregistered"):
        analyze(_rows(), config)


def test_reader_rejects_inconsistent_realized_q(tmp_path: Path) -> None:
    rows = _rows()
    rows[0]["q_realized"] = "0.90"
    path = tmp_path / "bad.csv"
    _write(path, rows)
    with pytest.raises(ValueError, match="q_realized"):
        read_rows(path)


def test_registered_template_and_config_remain_fail_closed() -> None:
    root = Path(__file__).resolve().parents[1]
    template = root / "empirical" / "identification_design" / "PEUCEDANUM_STAGE_B_VALIDATION_TEMPLATE_V1.csv"
    config_path = root / "empirical" / "identification_design" / "PEUCEDANUM_STAGE_B_VALIDATION_CONFIG_TEMPLATE_V1.json"
    with template.open(encoding="utf-8", newline="") as handle:
        assert tuple(next(csv.reader(handle))) == REQUIRED_FIELDS
    config = json.loads(config_path.read_text(encoding="utf-8"))
    assert "DO_NOT_RUN" in config["status"]
    assert config["target_total_retained_count"] == "REQUIRED_BEFORE_USE"
    assert config["min_classification_accuracy_lower95"] == "REQUIRED_BEFORE_USE"
