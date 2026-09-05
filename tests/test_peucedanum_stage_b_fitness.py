from __future__ import annotations

import csv
import json
from copy import deepcopy
from pathlib import Path

import pytest

from scripts.analyze_peucedanum_stage_b_fitness import (
    G_REMOVED,
    G_RETAINED,
    RECEIPT_SCHEMA,
    analyze,
    read_assignment_rows,
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
ASSIGNMENT_FIELDS = VALIDATION_FIELDS + ("g_state", "outcome_observed")


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
        "assignment_ledger_required": True,
        "bootstrap_reps": 120,
        "bootstrap_seed": 991,
        "min_blocks": 12,
        "min_q_levels": 3,
        "min_units_per_q_by_g_cell": 10,
        "min_valid_predation_fraction_per_cell": 0.95,
        "max_post_randomization_attrition_fraction": 0.15,
        "max_attrition_rate_difference_across_cells": 0.10,
        "min_observed_fraction_per_cell": 0.80,
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


def _assignment_rows(outcome_source_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {**{field: row[field] for field in VALIDATION_FIELDS}, "g_state": row["g_state"], "outcome_observed": "1"}
        for row in outcome_source_rows
    ]


def _drop_outcomes(
    full_rows: list[dict[str, str]], assignment_rows: list[dict[str, str]], drop_ids: set[str]
) -> list[dict[str, str]]:
    for row in assignment_rows:
        if row["unit_id"] in drop_ids:
            row["outcome_observed"] = "0"
    return [row for row in full_rows if row["unit_id"] not in drop_ids]


def _write(path: Path, rows: list[dict[str, str]], fields: tuple[str, ...]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _read_pair(tmp_path: Path, full_rows: list[dict[str, str]], assignment_rows: list[dict[str, str]]):
    outcome_path = tmp_path / "outcomes.csv"
    assignment_path = tmp_path / "assignment.csv"
    _write(outcome_path, full_rows, ALL_FIELDS)
    _write(assignment_path, assignment_rows, ASSIGNMENT_FIELDS)
    return read_rows(outcome_path), read_assignment_rows(assignment_path)


def test_positive_control_recovers_full_causal_partial_differentiation_chain(tmp_path: Path) -> None:
    full = _rows(antagonism_changes_fitness=True)
    observed, assignments = _read_pair(tmp_path, full, _assignment_rows(full))
    receipt = analyze(observed, assignments, _validation_config(), _fitness_config())
    assert receipt["receipt_schema_version"] == RECEIPT_SCHEMA
    assert receipt["status"] == "CAUSAL_PARTIAL_FUNCTIONAL_DIFFERENTIATION_SUPPORTED"
    assert all(receipt["gates"].values())
    assert receipt["assignment_and_attrition"]["overall_attrition_fraction"] == 0
    assert receipt["primary_estimand"]["estimate"] < -0.10
    assert receipt["primary_estimand"]["block_bootstrap_ci95"]["upper_95"] < 0
    assert receipt["mechanism_estimands"]["initial_high_vs_low_gain_z"]["estimate"] > 0.75
    assert receipt["mechanism_estimands"]["oviposition_high_vs_low_gain_z"]["estimate"] > 0.75
    assert receipt["mechanism_estimands"]["predation_relief"]["estimate"] > 0.20
    assert receipt["mechanism_estimands"]["q_predation_interaction"]["estimate"] > 0.20
    assert receipt["mechanism_estimands"]["male_cell_range_z"]["estimate"] < 0.10
    assert "post_randomization_attrition_audit" in receipt["claim_ceiling"]


def test_balanced_modest_attrition_does_not_force_whole_block_deletion(tmp_path: Path) -> None:
    full = _rows(antagonism_changes_fitness=True)
    assignments = _assignment_rows(full)
    drop_ids = {
        f"U00_0.25_{G_REMOVED}",
        f"U01_0.25_{G_RETAINED}",
        f"U02_0.5_{G_REMOVED}",
        f"U03_0.5_{G_RETAINED}",
        f"U04_0.75_{G_REMOVED}",
        f"U05_0.75_{G_RETAINED}",
    }
    observed_rows = _drop_outcomes(full, assignments, drop_ids)
    observed, assignments_read = _read_pair(tmp_path, observed_rows, assignments)
    receipt = analyze(observed, assignments_read, _validation_config(), _fitness_config())
    assert receipt["status"] == "CAUSAL_PARTIAL_FUNCTIONAL_DIFFERENTIATION_SUPPORTED"
    assert receipt["gates"]["post_randomization_attrition_within_bounds"] is True
    assert receipt["assignment_and_attrition"]["overall_attrition_fraction"] == pytest.approx(6 / 84)
    assert receipt["assignment_and_attrition"]["minimum_cell_observed_fraction"] == pytest.approx(13 / 14)
    assert receipt["n_observed_blocks"] == 14
    assert receipt["n_outcome_units"] == 78


def test_differential_cell_attrition_blocks_promotion_even_if_outcome_model_runs(tmp_path: Path) -> None:
    full = _rows(antagonism_changes_fitness=True)
    assignments = _assignment_rows(full)
    drop_ids = {f"U{block:02d}_0.75_{G_RETAINED}" for block in range(4)}
    observed_rows = _drop_outcomes(full, assignments, drop_ids)
    observed, assignments_read = _read_pair(tmp_path, observed_rows, assignments)
    receipt = analyze(observed, assignments_read, _validation_config(), _fitness_config())
    assert receipt["status"] == "CAUSAL_PARTIAL_FUNCTIONAL_DIFFERENTIATION_NOT_FULLY_RECOVERED"
    assert receipt["gates"]["post_randomization_attrition_within_bounds"] is False
    assert receipt["assignment_and_attrition"]["overall_attrition_fraction"] < 0.15
    assert receipt["assignment_and_attrition"]["maximum_cell_attrition_rate_difference"] > 0.10


def test_negative_control_does_not_promote_without_antagonist_dependent_cost(tmp_path: Path) -> None:
    full = _rows(antagonism_changes_fitness=False)
    observed, assignments = _read_pair(tmp_path, full, _assignment_rows(full))
    receipt = analyze(observed, assignments, _validation_config(), _fitness_config())
    assert receipt["status"] == "CAUSAL_PARTIAL_FUNCTIONAL_DIFFERENTIATION_NOT_FULLY_RECOVERED"
    assert receipt["gates"]["egg_removal_reduces_predation"] is False
    assert receipt["gates"]["predation_cost_increases_with_q_under_G"] is False
    assert receipt["gates"]["female_fitness_optimum_shifts_to_lower_q_under_antagonism"] is False


def test_invalid_pre_g_manipulation_blocks_fitness_before_outcome_testing(tmp_path: Path) -> None:
    full = _rows()
    assignments = _assignment_rows(full)
    assignments[0]["eggs_before_manipulation"] = "1"
    observed, assignments_read = _read_pair(tmp_path, full, assignments)
    receipt = analyze(observed, assignments_read, _validation_config(), _fitness_config())
    assert receipt["status"] == "BLOCKED_BY_INVALID_STAGE_B_MANIPULATION"
    assert "primary_estimand" not in receipt


def test_assignment_ledger_must_match_observed_outcome_ids(tmp_path: Path) -> None:
    full = _rows()
    assignments = _assignment_rows(full)
    assignments[0]["outcome_observed"] = "0"
    observed, assignments_read = _read_pair(tmp_path, full, assignments)
    with pytest.raises(ValueError, match="outcome rows must match outcome_observed=1"):
        analyze(observed, assignments_read, _validation_config(), _fitness_config())


def test_assignment_ledger_requires_complete_factorial_at_randomization(tmp_path: Path) -> None:
    full = _rows(n_blocks=2)
    assignments = _assignment_rows(full)
    assignments = [row for row in assignments if row["unit_id"] != f"U00_0.75_{G_RETAINED}"]
    path = tmp_path / "assignment.csv"
    _write(path, assignments, ASSIGNMENT_FIELDS)
    with pytest.raises(ValueError, match="assignment ledger must contain exactly one randomized unit"):
        read_assignment_rows(path)


def test_outcome_reader_allows_incomplete_post_randomization_blocks(tmp_path: Path) -> None:
    full = _rows(n_blocks=2)
    reduced = [row for row in full if row["unit_id"] != f"U00_0.75_{G_RETAINED}"]
    path = tmp_path / "incomplete_outcomes.csv"
    _write(path, reduced, ALL_FIELDS)
    rows = read_rows(path)
    assert len(rows) == 11


def test_fitness_config_fails_closed_until_attrition_thresholds_are_preregistered(tmp_path: Path) -> None:
    full = _rows()
    observed, assignments = _read_pair(tmp_path, full, _assignment_rows(full))
    config = _fitness_config()
    config["max_post_randomization_attrition_fraction"] = "REQUIRED_BEFORE_USE"
    with pytest.raises(ValueError, match="preregistered"):
        analyze(observed, assignments, _validation_config(), config)


def test_registered_stage_b_fitness_and_assignment_templates_remain_fail_closed() -> None:
    root = Path(__file__).resolve().parents[1]
    fitness_template = root / "empirical" / "identification_design" / "PEUCEDANUM_STAGE_B_FITNESS_TEMPLATE_V1.csv"
    assignment_template = root / "empirical" / "identification_design" / "PEUCEDANUM_STAGE_B_ASSIGNMENT_LEDGER_TEMPLATE_V1.csv"
    config_path = root / "empirical" / "identification_design" / "PEUCEDANUM_STAGE_B_FITNESS_CONFIG_TEMPLATE_V1.json"
    with fitness_template.open(encoding="utf-8", newline="") as handle:
        assert tuple(next(csv.reader(handle))) == ALL_FIELDS
    with assignment_template.open(encoding="utf-8", newline="") as handle:
        assert tuple(next(csv.reader(handle))) == ASSIGNMENT_FIELDS
    config = json.loads(config_path.read_text(encoding="utf-8"))
    assert "DO_NOT_RUN" in config["status"]
    assert config["assignment_ledger_required"] is True
    assert config["max_post_randomization_attrition_fraction"] == "REQUIRED_BEFORE_USE"
    assert config["max_attrition_rate_difference_across_cells"] == "REQUIRED_BEFORE_USE"
    assert config["min_observed_fraction_per_cell"] == "REQUIRED_BEFORE_USE"
    assert config["min_negative_optimum_shift_q"] == "REQUIRED_BEFORE_USE"
