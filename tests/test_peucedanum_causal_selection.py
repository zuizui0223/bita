from __future__ import annotations

import csv
import json
import random
from pathlib import Path

import pytest

from scripts.analyze_peucedanum_causal_selection import (
    G_REMOVED,
    G_RETAINED,
    RECEIPT_SCHEMA,
    REQUIRED_FIELDS,
    analyze,
    read_rows,
)


def _config() -> dict:
    return {
        "status": "TEST_ONLY",
        "randomization_scheme": "WITHIN_BLOCK_EGG_REMOVAL_VS_RETENTION",
        "bootstrap_reps": 120,
        "bootstrap_seed": 731,
        "min_blocks": 20,
        "min_units_per_g_state": 20,
        "min_valid_predation_units_per_g_state": 20,
        "max_abs_pretreatment_smd": 0.05,
        "min_negative_delta_beta_q": 0.08,
        "min_predation_relief": 0.10,
        "initial_effect_tolerance_z": 0.20,
        "male_effect_tolerance_z": 0.20,
        "require_delta_beta_bootstrap_upper_below_zero": True,
        "require_predation_relief_bootstrap_lower_above_minimum": True,
        "require_equivalence_ci_inside_tolerance": True,
    }


def _synthetic_rows(*, antagonist_changes_damage: bool, n_blocks: int = 36) -> list[dict[str, str]]:
    rng = random.Random(4419)
    rows: list[dict[str, str]] = []
    for block in range(n_blocks):
        total = 90.0 + rng.uniform(-18.0, 18.0)
        q = 0.18 + 0.62 * rng.random()
        perfect = total * q
        male = total - perfect
        height = 10.0 + rng.uniform(-3.0, 4.0)
        day = 20.0 + rng.uniform(-8.0, 9.0)
        eggs = 0.5 + 7.0 * q + 0.008 * total + 0.04 * height + rng.uniform(-0.4, 0.4)
        initial = perfect * (0.48 + 0.03 * ((block % 5) - 2))
        male_fitness = 15.0 + 0.75 * total + 0.30 * height - 0.08 * day

        for state in (G_REMOVED, G_RETAINED):
            if antagonist_changes_damage:
                damage_rate = 0.04 if state == G_REMOVED else 0.16 + 0.52 * q
            else:
                damage_rate = 0.08
            predated = initial * damage_rate
            intact = initial - predated
            rows.append(
                {
                    "plant_id": f"P{block:03d}_{state}",
                    "block_id": f"B{block:03d}",
                    "g_state": state,
                    "perfect_flowers": f"{perfect:.10f}",
                    "male_flowers": f"{male:.10f}",
                    "total_flowers": f"{total:.10f}",
                    "q_perfect": f"{q:.10f}",
                    "flower_height": f"{height:.10f}",
                    "flowering_day": f"{day:.10f}",
                    "eggs_before": f"{eggs:.10f}",
                    "initial_fruits": f"{initial:.10f}",
                    "final_intact_fruits": f"{intact:.10f}",
                    "predated_fruits": f"{predated:.10f}",
                    "male_fitness": f"{male_fitness:.10f}",
                }
            )
    return rows


def _write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REQUIRED_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def test_positive_control_recovers_randomized_antagonism_dependent_selection() -> None:
    receipt = analyze(_synthetic_rows(antagonist_changes_damage=True), _config())
    assert receipt["receipt_schema_version"] == RECEIPT_SCHEMA
    assert receipt["status"] == "CAUSAL_ANTAGONISM_DEPENDENT_SELECTION_ON_SEX_ALLOCATION"
    assert all(receipt["gates"].values())
    assert receipt["primary_estimand"]["estimate"] < -0.08
    assert receipt["primary_estimand"]["block_bootstrap_ci95"]["upper_95"] < 0
    assert receipt["predation_relief"]["retained_minus_removed"] > 0.10
    assert receipt["predation_relief"]["block_bootstrap_ci95"]["lower_95"] > 0.10
    assert receipt["secondary_oviposition_association"]["causal_with_respect_to_q"] is False
    assert "q_itself_not_randomized" in receipt["claim_ceiling"]


def test_negative_control_does_not_promote_when_antagonist_context_changes_nothing() -> None:
    receipt = analyze(_synthetic_rows(antagonist_changes_damage=False), _config())
    assert receipt["status"] == "CAUSAL_ANTAGONISM_DEPENDENT_SELECTION_NOT_FULLY_RECOVERED"
    assert receipt["gates"]["predation_relief"] is False
    assert receipt["gates"]["negative_antagonism_dependent_selection_shift"] is False
    assert abs(receipt["primary_estimand"]["estimate"]) < 1e-8


def test_config_fails_closed_until_thresholds_are_preregistered() -> None:
    config = _config()
    config["min_negative_delta_beta_q"] = "REQUIRED_BEFORE_USE"
    with pytest.raises(ValueError, match="preregistered"):
        analyze(_synthetic_rows(antagonist_changes_damage=True), config)


def test_reader_rejects_inconsistent_q_and_requires_both_states_per_block(tmp_path: Path) -> None:
    rows = _synthetic_rows(antagonist_changes_damage=True, n_blocks=2)
    rows[0]["q_perfect"] = "0.99"
    path = tmp_path / "bad_q.csv"
    _write_rows(path, rows)
    with pytest.raises(ValueError, match="q_perfect"):
        read_rows(path)

    rows = _synthetic_rows(antagonist_changes_damage=True, n_blocks=2)
    rows = [row for row in rows if not (row["block_id"] == "B000" and row["g_state"] == G_RETAINED)]
    path = tmp_path / "bad_block.csv"
    _write_rows(path, rows)
    with pytest.raises(ValueError, match="both egg-removal and retained"):
        read_rows(path)


def test_registered_templates_are_fail_closed_and_schema_complete() -> None:
    root = Path(__file__).resolve().parents[1]
    template = root / "empirical" / "identification_design" / "PEUCEDANUM_CAUSAL_SELECTION_TEMPLATE_V1.csv"
    config_path = root / "empirical" / "identification_design" / "PEUCEDANUM_CAUSAL_SELECTION_CONFIG_TEMPLATE_V1.json"
    contract = root / "docs" / "BITA_PEUCEDANUM_CAUSAL_SELECTION_EXPERIMENT_V1.md"

    with template.open(encoding="utf-8", newline="") as handle:
        assert tuple(next(csv.reader(handle))) == REQUIRED_FIELDS
    config = json.loads(config_path.read_text(encoding="utf-8"))
    assert "DO_NOT_RUN" in config["status"]
    assert config["min_negative_delta_beta_q"] == "REQUIRED_BEFORE_USE"
    assert config["male_effect_tolerance_z"] == "REQUIRED_BEFORE_USE"

    text = contract.read_text(encoding="utf-8")
    assert "Delta_beta_q" in text
    assert "CAUSAL_ANTAGONISM_DEPENDENT_SELECTION_ON_SEX_ALLOCATION" in text
    assert "q itself causally determines fitness" in text
