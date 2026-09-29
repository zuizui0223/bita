from __future__ import annotations

import pytest

from scripts.select_relative_route_cost_candidates import select_candidate_pair

def _rows(*, bypass_multiplier: float = 1.0) -> list[dict[str, str]]:
    rows = []
    trial = 0
    for route in ("legitimate", "bypass"):
        for bee_i in range(12):
            for distance in range(2, 11):
                time_s = 1.0 + 0.14 * (distance - 2)
                adjusted = time_s
                if route == "bypass":
                    adjusted = 1.0 + (time_s - 1.0) * bypass_multiplier
                for rep in range(3):
                    trial += 1
                    rows.append({
                        "bee_id": f"{route[0].upper()}{bee_i:02d}",
                        "colony_id": f"C{bee_i % 3}",
                        "route": route,
                        "distance_mm": str(distance),
                        "trial_id": f"T{trial}",
                        "trial_order": str(rep + 1),
                        "reward_acquired": "true",
                        "handling_time_s": str(adjusted),
                        "failure_code": "",
                        "geometry_version": "G1",
                        "notes": "",
                    })
    return rows

def test_candidate_selector_is_deterministic_and_matched() -> None:
    a = select_candidate_pair(_rows())
    b = select_candidate_pair(_rows())
    assert a["selected"] == b["selected"]
    assert 0.80 <= a["selected"]["ratio"] <= 1.25
    assert a["selected"]["legitimate"]["delta_log_time"] >= 0.20
    assert a["selected"]["bypass"]["delta_log_time"] >= 0.20

def test_candidate_selector_fails_when_route_increments_cannot_match() -> None:
    with pytest.raises(ValueError, match="matched-increment ratio"):
        select_candidate_pair(_rows(bypass_multiplier=0.15))


def test_candidate_selector_rejects_overlapping_route_cohorts() -> None:
    rows = _rows()
    for row in rows:
        if row["route"] == "bypass":
            row["bee_id"] = row["bee_id"].replace("B", "L", 1)
    with pytest.raises(ValueError, match="must use different bees"):
        select_candidate_pair(rows)


def test_candidate_selector_requires_full_2_to_10_grid() -> None:
    rows = [row for row in _rows() if row["distance_mm"] != "10"]
    with pytest.raises(ValueError, match="full 2-10 mm candidate grid"):
        select_candidate_pair(rows)
