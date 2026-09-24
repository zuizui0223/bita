from __future__ import annotations

import csv
import json

import pytest

from scripts.plan_third_network_camera_effort import (
    EXPECTED_COLUMNS,
    load_rates,
    plan_effort,
)


def _rows(
    *,
    sites: int = 2,
    plants: int = 7,
    mammals: int = 6,
    rate: float = 0.03,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for s in range(sites):
        for p in range(plants):
            for m in range(mammals):
                rows.append(
                    {
                        "site": f"S{s}",
                        "plant": f"P{p}",
                        "mammal": f"M{m}",
                        "rate": rate + 0.001 * ((p + m + s) % 3),
                    }
                )
    return rows


def test_effort_success_probability_is_monotone_with_more_uniform_hours() -> None:
    result = plan_effort(
        _rows(),
        hours_grid=[24, 48, 96, 168, 240],
        qualifying_fraction=0.5,
        simulations=600,
        seed=123,
        target_success_probability=0.8,
    )

    probs = [
        float(row["planning_target_success_probability"])
        for row in result["hours_grid"]
    ]
    minimum_probs = [
        float(row["minimum_gate_success_probability"])
        for row in result["hours_grid"]
    ]

    assert probs == sorted(probs)
    assert minimum_probs == sorted(minimum_probs)
    assert result["candidate_structure"]["candidate_units"] == 84
    assert result["candidate_structure"]["distinct_plant_site_deployments"] == 14
    assert result["route_blind_contract"]["uses_route_outcome"] is False
    assert result["route_blind_contract"]["uses_access_mismatch"] is False
    assert result["route_blind_contract"]["uses_morphology"] is False


def test_effort_plan_is_deterministic_for_same_seed() -> None:
    kwargs = dict(
        hours_grid=[48, 96, 168],
        qualifying_fraction=0.5,
        simulations=300,
        seed=20260924,
        target_success_probability=0.7,
        camera_count=10,
    )
    first = plan_effort(_rows(), **kwargs)
    second = plan_effort(_rows(), **kwargs)
    assert first == second


def test_structurally_insufficient_candidate_pool_never_manufactures_target() -> None:
    result = plan_effort(
        _rows(sites=1, plants=5, mammals=5, rate=0.2),
        hours_grid=[24, 240, 2400],
        qualifying_fraction=1.0,
        simulations=200,
        seed=7,
    )

    assert result["candidate_structure"]["candidate_units"] == 25
    assert result["candidate_structure"]["planning_target_structurally_possible"] is False
    assert result["status"] == "PLANNING_TARGET_STRUCTURALLY_IMPOSSIBLE"
    assert result["recommended_uniform_effort"] is None
    assert all(
        float(row["planning_target_success_probability"]) == 0.0
        for row in result["hours_grid"]
    )


def test_camera_count_changes_calendar_projection_not_scientific_success() -> None:
    common = dict(
        rows=_rows(),
        hours_grid=[96],
        qualifying_fraction=0.5,
        simulations=250,
        seed=4,
    )
    five = plan_effort(camera_count=5, **common)
    ten = plan_effort(camera_count=10, **common)

    assert (
        five["hours_grid"][0]["planning_target_success_probability"]
        == ten["hours_grid"][0]["planning_target_success_probability"]
    )
    assert (
        float(five["hours_grid"][0]["approx_elapsed_hours_at_camera_count"])
        == 2.0
        * float(ten["hours_grid"][0]["approx_elapsed_hours_at_camera_count"])
    )


def test_rate_loader_rejects_outcome_or_morphology_columns(tmp_path) -> None:
    path = tmp_path / "leaky.csv"
    fields = list(EXPECTED_COLUMNS) + ["route_code"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerow(
            {
                "site_id": "S1",
                "plant_species": "P1",
                "mammal_species": "M1",
                "route_blind_detection_rate_per_camera_hour": "0.1",
                "route_code": "B",
            }
        )

    with pytest.raises(
        ValueError,
        match="OUTCOME_OR_MORPHOLOGY_COLUMN_FORBIDDEN_IN_EFFORT_PLANNER",
    ):
        load_rates(path)


def test_rate_loader_accepts_exact_route_blind_schema(tmp_path) -> None:
    path = tmp_path / "rates.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(EXPECTED_COLUMNS))
        writer.writeheader()
        writer.writerow(
            {
                "site_id": "S1",
                "plant_species": "P1",
                "mammal_species": "M1",
                "route_blind_detection_rate_per_camera_hour": "0.1",
            }
        )

    rows = load_rates(path)
    assert rows == [
        {"site": "S1", "plant": "P1", "mammal": "M1", "rate": 0.1}
    ]


def test_qualifying_fraction_is_explicit_planning_assumption() -> None:
    with pytest.raises(ValueError, match="qualifying_fraction"):
        plan_effort(
            _rows(),
            hours_grid=[24],
            qualifying_fraction=0.0,
            simulations=10,
        )
