from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from scripts.analyze_peucedanum_stage_b_fitness import (
    G_REMOVED,
    G_RETAINED,
    RECEIPT_SCHEMA,
    analyze,
    read_rows,
)
from scripts.evaluate_peucedanum_stage_b_manipulation import REQUIRED_FIELDS as VALIDATION_FIELDS


OUTCOME_FIELDS = (
    "g_state",
    "eggs_before_g_treatment",
    "initial_fruits",
    "final_intact_fruits",
    "predated_fruits",
    "male_fitness",
)
ALL_FIELDS = VALIDATION_FIELDS + OUTCOME_FIELDS


def _validation_config() -> dict:
    return {
        "status": "TEST_ONLY",
        "min_q_levels": 3,
        "min_units_per_q_level": 20,
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


def _fitness_config() -> dict:
    return {
        "status": "TEST_ONLY",
        "design": "WITHIN_BLOCK_RANDOMIZED_Q_BY_G_FACTORIAL",
        "bootstrap_reps": 120,
        "bootstrap_seed": 991,
        "min_blocks": 12,
        "min_q_levels": 3,
        "min_units_per_q_by_g_cell": 10,
        "min_valid_predation_fraction_per_cell": 0.95,
        "min_negative_optimum_shift_q": 0.10,
        "min_initial_high_vs_low_gain_z": 0.75,
        "min_positive_q_oviposition_gain_z": 0.75,
        "min_predation_relief": 0.20,
        "min_positive_q_predation_interaction": 0.20,
        "initial_g_effect_tolerance_z": 0.10,
        "male_cell_range_tolerance_z": 0.10,
        "require_optimum_shift_bootstrap_upper_below_zero": True,
        "require_initial_gain_bootstrap_lower_above_minimum": True,
        "require_oviposition_gain_bootstrap_lower_above_minimum": True,
        "require_predation_interaction_bootstrap_lower_above_minimum": True,
        "require_equivalence_bootstrap_upper_below_tolerance": True,
    }


def _rows(*, antagonism_changes_fitness: bool = True, n_blocks: int = 14) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for block in range(n_blocks):
        total_before = 52 + (block % 3)
        height = 10 + (block % 4)
        day = 20 + (block % 5)
        initial_multiplier = 0.58 + 0.01 * (block % 5)
        male_fitness = 50 + 0.8 * block
        for q in (0.25, 0.50, 0.75):
            perfect = 40 * q
            male = 40 - perfect
            initial = perfect * initial_multiplier
            eggs_after_q = 1.0 + 8.0 * q + 0.03 * (block % 4)
            for state in (G_REMOVED, G_RETAINED):
                if antagonism_changes_fitness:
                    damage_rate = 0.03 if state == G_REMOVED else 0.05 + q
                else:
                    damage_rate = 0.03
                predated = initial * damage_rate
                intact = initial - predated
                rows.append(
                    {
                        "unit_id": f"U{block:02d}_{q}_{state}",
                        "block_id": f"B{block:02d}",
                        "q_target": f"{q:.2f}",
                        "q_realized": f"{q:.2f}",
                        "total_before": str(total_before),
                        "total_retained": "40",
                        "perfect_retained": f"{perfect:.8f}",
                        "male_retained": f"{male:.8f}",
                        "classification_checked_n": "20",
                        "classification_correct_n": "20",
                        "eggs_before_manipulation": "0",
                        "removal_load": str(total_before - 40),
                        "handling_actions": "20",
                        "mechanical_damage_count": "0",
                        "male_phase_complete": "1",
                        "flower_height": str(height),
                        "flowering_day": str(day),
                        "g_state": state,
                        "eggs_before_g_treatment": f"{eggs_after_q:.8f}",
                        "initial_fruits": f"{initial:.8f}",
                        "final_intact_fruits": f"{intact:.8f}",
                        "predated_fruits": f"{predated:.8f}",
                        "male_fitness": f"{male_fitness:.8f}",
                    }
                )
    return rows


def _write(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=ALL_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def test_positive_control_recovers_full_causal_partial_differentiation_chain(tmp_path: Path) -> None:
    path = tmp_path / "positive.csv"
    _write(path, _rows(antagonism_changes_fitness=True))
    receipt = analyze(read_rows(path), _validation_config(), _fitness_config())
    assert receipt["receipt_schema_version"] == RECEIPT_SCHEMA
    assert receipt["status"] == "CAUSAL_PARTIAL_FUNCTIONAL_DIFFERENTIATION_SUPPORTED"
    assert all(receipt["gates"].values())
    assert receipt["primary_estimand"]["estimate"] < -0.10
    assert receipt["primary_estimand"]["block_bootstrap_ci95"]["upper_95"] < 0
    assert receipt["mechanism_estimands"]["initial_high_vs_low_gain_z"]["estimate"] > 0.75
    assert receipt["mechanism_estimands"]["oviposition_high_vs_low_gain_z"]["estimate"] > 0.75
    assert receipt["mechanism_estimands"]["predation_relief"]["estimate"] > 0.20
    assert receipt["mechanism_estimands"]["q_predation_interaction"]["estimate"] > 0.20
    assert receipt["mechanism_estimands"]["male_cell_range_z"]["estimate"] < 0.10
    assert "not_historical_origin_of_andromonoecy" in receipt["claim_ceiling"]


def test_negative_control_does_not_promote_without_antagonist_dependent_cost(tmp_path: Path) -> None:
    path = tmp_path / "negative.csv"
    _write(path, _rows(antagonism_changes_fitness=False))
    receipt = analyze(read_rows(path), _validation_config(), _fitness_config())
    assert receipt["status"] == "CAUSAL_PARTIAL_FUNCTIONAL_DIFFERENTIATION_NOT_FULLY_RECOVERED"
    assert receipt["gates"]["egg_removal_reduces_predation"] is False
    assert receipt["gates"]["predation_cost_increases_with_q_under_G"] is False
    assert receipt["gates"]["female_fitness_optimum_shifts_to_lower_q_under_antagonism"] is False


def test_invalid_manipulation_blocks_fitness_inference_before_outcome_testing(tmp_path: Path) -> None:
    rows = _rows()
    rows[0]["eggs_before_manipulation"] = "1"
    path = tmp_path / "blocked.csv"
    _write(path, rows)
    receipt = analyze(read_rows(path), _validation_config(), _fitness_config())
    assert receipt["status"] == "BLOCKED_BY_INVALID_STAGE_B_MANIPULATION"
    assert "primary_estimand" not in receipt


def test_fitness_config_fails_closed_until_thresholds_are_preregistered(tmp_path: Path) -> None:
    path = tmp_path / "positive.csv"
    _write(path, _rows())
    config = _fitness_config()
    config["min_negative_optimum_shift_q"] = "REQUIRED_BEFORE_USE"
    with pytest.raises(ValueError, match="preregistered"):
        analyze(read_rows(path), _validation_config(), config)


def test_reader_requires_complete_q_by_g_factorial_inside_every_block(tmp_path: Path) -> None:
    rows = _rows(n_blocks=2)
    rows = [row for row in rows if row["unit_id"] != f"U00_0.75_{G_RETAINED}"]
    path = tmp_path / "incomplete.csv"
    _write(path, rows)
    with pytest.raises(ValueError, match="exactly one unit for every q_target x G combination"):
        read_rows(path)


def test_registered_stage_b_fitness_templates_remain_fail_closed() -> None:
    root = Path(__file__).resolve().parents[1]
    template = root / "empirical" / "identification_design" / "PEUCEDANUM_STAGE_B_FITNESS_TEMPLATE_V1.csv"
    config_path = root / "empirical" / "identification_design" / "PEUCEDANUM_STAGE_B_FITNESS_CONFIG_TEMPLATE_V1.json"
    with template.open(encoding="utf-8", newline="") as handle:
        assert tuple(next(csv.reader(handle))) == ALL_FIELDS
    config = json.loads(config_path.read_text(encoding="utf-8"))
    assert "DO_NOT_RUN" in config["status"]
    assert config["design"] == "WITHIN_BLOCK_RANDOMIZED_Q_BY_G_FACTORIAL"
    assert config["min_negative_optimum_shift_q"] == "REQUIRED_BEFORE_USE"
    assert config["min_positive_q_oviposition_gain_z"] == "REQUIRED_BEFORE_USE"
