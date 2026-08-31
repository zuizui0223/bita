from scripts.plan_kessler_type_replication import (
    asymptotic_level23_decision_probability,
    balanced_effective_n_per_cell,
    balanced_effective_n_per_cell_level23,
    build_plan,
    level23_component_decision_probabilities,
    planned_observations_per_cell,
    stage1_contrasts,
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
    assert len(plan["level23_rows"]) == 18
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


def test_stage1_contrasts_match_registered_hierarchy() -> None:
    a0, a1, delta = stage1_contrasts(0.35, 0.10, 0.13, 0.13)
    assert round(a0, 12) == -0.03
    assert round(a1, 12) == 0.22
    assert round(delta, 12) == 0.25


def test_true_A0_zero_cannot_have_high_power_under_strict_zero_ci_rule() -> None:
    asymptotic = asymptotic_level23_decision_probability(
        p11=0.35, p10=0.13, p01=0.13, p00=0.13
    )
    assert abs(asymptotic - 0.025) < 1e-12
    assert balanced_effective_n_per_cell_level23(
        p11=0.35, p10=0.13, p01=0.13, p00=0.13, power=0.80
    ) is None
    assert balanced_effective_n_per_cell_level23(
        p11=0.35, p10=0.13, p01=0.13, p00=0.13, power=0.90
    ) is None


def test_negative_A0_sensitivity_exposes_level23_sample_size_cost() -> None:
    weak80 = balanced_effective_n_per_cell_level23(
        p11=0.35, p10=0.10, p01=0.13, p00=0.13, power=0.80
    )
    weak90 = balanced_effective_n_per_cell_level23(
        p11=0.35, p10=0.10, p01=0.13, p00=0.13, power=0.90
    )
    moderate80 = balanced_effective_n_per_cell_level23(
        p11=0.35, p10=0.08, p01=0.13, p00=0.13, power=0.80
    )
    moderate90 = balanced_effective_n_per_cell_level23(
        p11=0.35, p10=0.08, p01=0.13, p00=0.13, power=0.90
    )
    assert weak80 == 1772
    assert weak90 == 2372
    assert moderate80 == 587
    assert moderate90 == 785
    assert moderate80 < weak80

    p0, p1, joint = level23_component_decision_probabilities(
        weak80,
        p11=0.35,
        p10=0.10,
        p01=0.13,
        p00=0.13,
    )
    assert p0 >= 0.80
    assert p1 > 0.999
    assert joint >= 0.80


def test_level23_plan_reports_boundary_and_design_inflation() -> None:
    plan = build_plan()
    boundary = [
        row for row in plan["level23_rows"]
        if row["scenario"] == "boundary_A0_zero"
        and row["target_joint_power"] == 0.80
        and row["design_effect"] == 1.5
    ][0]
    assert boundary["effective_n_per_trait_cell"] is None
    assert boundary["planned_observations_per_cell"] is None
    assert boundary["asymptotic_max_joint_decision_probability"] == 0.025
    assert boundary["status"] == "TARGET_POWER_NOT_ATTAINABLE_UNDER_STRICT_ZERO_CI_RULE"

    weak = [
        row for row in plan["level23_rows"]
        if row["scenario"] == "weak_negative_A0_minus_0_03"
        and row["target_joint_power"] == 0.80
        and row["design_effect"] == 1.5
    ][0]
    assert weak["effective_n_per_trait_cell"] == 1772
    assert weak["planned_observations_per_cell"] == 2954
    assert weak["planned_total_four_cell_trait_factorial"] == 11816
    assert weak["status"] == "POWERABLE_UNDER_DECLARED_NORMAL_APPROXIMATION"
