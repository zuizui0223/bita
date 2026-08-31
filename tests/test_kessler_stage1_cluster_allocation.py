from __future__ import annotations

import pytest

from scripts.plan_kessler_stage1_cluster_allocation import (
    build_cluster_plan,
    cluster_allocation,
    exchangeable_design_effect,
)


def test_exchangeable_design_effect_matches_declared_formula() -> None:
    assert exchangeable_design_effect(5, 0.10) == pytest.approx(1.4)
    assert exchangeable_design_effect(10, 0.20) == pytest.approx(2.8)


def test_central_80pct_anchor_translates_to_plant_budget() -> None:
    plan = build_cluster_plan()
    row = next(
        row
        for row in plan["rows"]
        if row["scenario"] == "published_central"
        and row["power"] == 0.80
        and row["flowers_per_plant"] == 5
        and row["icc"] == 0.10
    )
    assert row["effective_n_per_cell"] == 92
    assert row["design_effect"] == pytest.approx(1.4)
    assert row["plants_per_cell"] == 29
    assert row["total_plants_four_cells"] == 116
    assert row["total_introduced_flowers_four_cells"] == 580
    assert row["matched_blocks_if_one_plant_per_cell_per_block"] == 29


def test_attenuated_80pct_anchor_is_more_demanding() -> None:
    plan = build_cluster_plan()
    row = next(
        row
        for row in plan["rows"]
        if row["scenario"] == "attenuated_delta_0_17"
        and row["power"] == 0.80
        and row["flowers_per_plant"] == 5
        and row["icc"] == 0.10
    )
    assert row["effective_n_per_cell"] == 150
    assert row["plants_per_cell"] == 47
    assert row["total_plants_four_cells"] == 188
    assert row["total_introduced_flowers_four_cells"] == 940


def test_high_icc_penalizes_many_flowers_per_plant() -> None:
    low = cluster_allocation(92, flowers_per_plant=10, icc=0.05)
    high = cluster_allocation(92, flowers_per_plant=10, icc=0.20)
    assert high["design_effect"] > low["design_effect"]
    assert high["total_introduced_flowers_four_cells"] > low["total_introduced_flowers_four_cells"]


def test_invalid_cluster_assumptions_fail_closed() -> None:
    with pytest.raises(ValueError):
        exchangeable_design_effect(0, 0.1)
    with pytest.raises(ValueError):
        exchangeable_design_effect(5, 1.0)
