from scripts.plan_kessler_type_replication import (
    balanced_effective_n_per_cell,
    build_plan,
    planned_observations_per_cell,
)


def test_published_central_effective_sample_sizes_are_reproducible() -> None:
    assert balanced_effective_n_per_cell(
        p11=0.35, p10=0.13, p01=0.13, p00=0.13, power=0.80
    ) == 92
    assert balanced_effective_n_per_cell(
        p11=0.35, p10=0.13, p01=0.13, p00=0.13, power=0.90
    ) == 124


def test_attenuated_effects_require_larger_samples() -> None:
    n17 = balanced_effective_n_per_cell(
        p11=0.30, p10=0.13, p01=0.13, p00=0.13, power=0.80
    )
    n12 = balanced_effective_n_per_cell(
        p11=0.25, p10=0.13, p01=0.13, p00=0.13, power=0.80
    )
    assert n17 == 150
    assert n12 == 288
    assert 92 < n17 < n12


def test_design_effect_and_retention_are_explicit_inflations() -> None:
    assert planned_observations_per_cell(92, design_effect=1.5, retention=0.90) == 154


def test_sixteen_cell_number_is_budget_only_not_mechanism_power_claim() -> None:
    plan = build_plan()
    assert len(plan["rows"]) == 18
    assert "budgeting extrapolation" in plan["claim_boundary"]
    assert "not a power guarantee" in plan["claim_boundary"]
    central = [
        row for row in plan["rows"]
        if row["scenario"] == "published_central"
        and row["power"] == 0.80
        and row["design_effect"] == 1.5
    ][0]
    assert central["planned_observations_per_cell"] == 154
    assert central["planned_total_four_cell_trait_factorial"] == 616
    assert central["budget_if_same_n_in_all_16_cells"] == 2464
