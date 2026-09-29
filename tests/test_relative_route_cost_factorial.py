from __future__ import annotations

import csv
from pathlib import Path

import pytest

from scripts.analyze_relative_route_cost_factorial import (
    analyze_choice_events,
)
from scripts.validate_relative_route_cost_calibration import (
    validate_calibration,
)
from scripts.generate_relative_route_cost_randomization import generate_schedule


def _calibration_rows(*, bypass_high_time: float = 1.45) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    trial = 0
    times = {
        ("legitimate", "low"): 1.00,
        ("legitimate", "high"): 1.50,
        ("bypass", "low"): 1.00,
        ("bypass", "high"): bypass_high_time,
    }
    for bee_i in range(20):
        for route in ("legitimate", "bypass"):
            for level in ("low", "high"):
                for _ in range(5):
                    trial += 1
                    rows.append(
                        {
                            "bee_id": f"C{bee_i:02d}",
                            "colony_id": f"COL{bee_i % 2}",
                            "geometry_version": "G1",
                            "route": route,
                            "cost_level": level,
                            "trial_id": f"CT{trial:04d}",
                            "handling_time_s": str(times[(route, level)]),
                            "reward_acquired": "true",
                            "failure_code": "",
                        }
                    )
    return rows


def _choice_rows(
    *,
    ll_bypass: int = 4,
    hl_bypass: int = 7,
    lh_bypass: int = 1,
    hh_bypass: int = 4,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    counts = {
        "LL": ll_bypass,
        "HL": hl_bypass,
        "LH": lh_bypass,
        "HH": hh_bypass,
    }
    levels = {
        "LL": ("low", "low"),
        "HL": ("high", "low"),
        "LH": ("low", "high"),
        "HH": ("high", "high"),
    }
    trial = 0
    for bee_i in range(60):
        for condition in ("LL", "HL", "LH", "HH"):
            bypass_n = counts[condition]
            for within_i in range(10):
                trial += 1
                route = "bypass" if within_i < bypass_n else "legitimate"
                l_level, b_level = levels[condition]
                rows.append(
                    {
                        "bee_id": f"B{bee_i:02d}",
                        "colony_id": f"COL{bee_i % 3}",
                        "session_id": f"S{bee_i // 10}",
                        "bout_id": f"BO{within_i // 5}",
                        "trial_id": f"T{trial:05d}",
                        "trial_order": str(trial),
                        "condition": condition,
                        "legitimate_cost_level": l_level,
                        "bypass_cost_level": b_level,
                        "flower_module_id": f"F{within_i % 4}",
                        "array_position": str(within_i % 6),
                        "reward_concentration": "50%",
                        "reward_volume_ul": "10",
                        "first_contact_route": route,
                        "successful_route": route,
                        "reward_acquired": "true",
                        "handling_time_s": "1.0",
                        "switch_count": "0",
                        "trial_valid": "true",
                        "exclusion_code": "",
                        "video_id": "",
                        "coder_id": "",
                        "notes": "",
                    }
                )
    return rows


def test_stage0_calibration_passes_matched_positive_increments() -> None:
    result = validate_calibration(_calibration_rows())
    assert result["eligible_bees"] == 20
    assert result["delta_legitimate_log_handling_time"] > 0
    assert result["delta_bypass_log_handling_time"] > 0
    assert 0.80 <= result["delta_ratio_legitimate_over_bypass"] <= 1.25
    assert result["passes_freeze_gate"] is True


def test_stage0_calibration_fails_badly_unmatched_increments() -> None:
    result = validate_calibration(_calibration_rows(bypass_high_time=3.0))
    assert result["passes_freeze_gate"] is False
    assert result["gates"]["matched_increment_ratio_0_80_to_1_25"] is False


def test_confirmatory_synthetic_sign_reversal_passes() -> None:
    result = analyze_choice_events(
        _choice_rows(),
        permutations=999,
        bootstraps=999,
        seed=123,
    )
    assert result["completed_bees"] == 60
    assert result["valid_trials"] == 2400
    assert result["primary_contrasts"]["C_L_HL_minus_LL"]["estimate"] > 0
    assert result["primary_contrasts"]["C_B_LH_minus_LL"]["estimate"] < 0
    assert result["primary_relative_route_cost_support"] is True
    assert result["compensation_diagnostic"]["supported"] is True


def test_confirmatory_wrong_bypass_sign_fails() -> None:
    result = analyze_choice_events(
        _choice_rows(lh_bypass=7),
        permutations=999,
        bootstraps=999,
        seed=456,
    )
    assert result["primary_contrasts"]["C_B_LH_minus_LL"]["estimate"] > 0
    assert result["primary_relative_route_cost_support"] is False


def test_confirmatory_requires_exactly_60_completed_bees() -> None:
    rows = _choice_rows()
    rows = [row for row in rows if row["bee_id"] != "B59"]
    with pytest.raises(ValueError, match="exactly 60 completed bees"):
        analyze_choice_events(rows, permutations=99, bootstraps=99, seed=1)


def test_condition_labels_must_match_cost_levels() -> None:
    rows = _choice_rows()
    rows[0]["legitimate_cost_level"] = "high"
    with pytest.raises(ValueError, match="condition/level mismatch"):
        analyze_choice_events(rows, permutations=99, bootstraps=99, seed=1)


def test_confirmatory_requires_at_least_three_colonies() -> None:
    rows = _choice_rows()
    for row in rows:
        row["colony_id"] = "ONE_COLONY"
    with pytest.raises(ValueError, match="at least 3 colonies"):
        analyze_choice_events(rows, permutations=99, bootstraps=99, seed=1)


def test_randomization_schedule_balances_all_four_conditions_per_block() -> None:
    bees = [
        {"bee_id": f"B{i:02d}", "colony_id": f"C{i % 3}"}
        for i in range(60)
    ]
    rows = generate_schedule(bees, seed=123)
    assert len(rows) == 2400
    for bee in bees:
        bee_rows = [row for row in rows if row["bee_id"] == bee["bee_id"]]
        assert len(bee_rows) == 40
        for block in range(1, 11):
            block_conditions = {
                row["planned_condition"]
                for row in bee_rows
                if row["block"] == block
            }
            assert block_conditions == {"LL", "HL", "LH", "HH"}
    first_routes = {
        row["bee_id"]: row["familiarization_first_route"]
        for row in rows
    }
    assert set(first_routes.values()) == {"legitimate", "bypass"}
