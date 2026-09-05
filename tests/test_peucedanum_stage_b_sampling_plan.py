from __future__ import annotations

import pytest

from scripts.plan_peucedanum_stage_b_sampling import (
    PLANNER_SCHEMA,
    binomial_tail_at_least,
    plan_stage_b_sampling,
)


def test_binomial_tail_is_exact_for_simple_case() -> None:
    assert binomial_tail_at_least(2, 0.5, 1) == pytest.approx(0.75)
    assert binomial_tail_at_least(2, 0.5, 2) == pytest.approx(0.25)


def test_15_percent_attrition_requires_25_per_cell_for_18_target_at_80_percent_joint_coverage() -> None:
    plan = plan_stage_b_sampling(
        q_levels=3,
        g_states=2,
        target_observed_per_cell=18,
        post_randomization_attrition_fraction=0.15,
        minimum_joint_outcome_coverage_probability=0.80,
        pre_g_qualification_failure_fraction=0.0,
    )
    assert plan["planner_schema_version"] == PLANNER_SCHEMA
    outcome = plan["post_randomization_outcome_stage"]
    assert outcome["randomized_per_cell"] == 25
    assert outcome["randomized_total"] == 150
    assert outcome["joint_probability_all_groups_at_least_target"] == pytest.approx(0.8565990577611134)
    assert outcome["complete_six_cell_block_survival_probability_if_cells_equal_six"] == pytest.approx(0.85**6)
    assert plan["interpretation"] == "coverage_and_attrition_planning_not_formal_power"


def test_15_percent_attrition_requires_26_per_cell_for_18_target_at_90_percent_joint_coverage() -> None:
    plan = plan_stage_b_sampling(
        q_levels=3,
        g_states=2,
        target_observed_per_cell=18,
        post_randomization_attrition_fraction=0.15,
        minimum_joint_outcome_coverage_probability=0.90,
        pre_g_qualification_failure_fraction=0.0,
    )
    outcome = plan["post_randomization_outcome_stage"]
    assert outcome["randomized_per_cell"] == 26
    assert outcome["randomized_total"] == 156
    assert outcome["joint_probability_all_groups_at_least_target"] == pytest.approx(0.9380783978142112)


def test_naive_expectation_only_plan_understates_joint_cell_coverage() -> None:
    plan = plan_stage_b_sampling(
        q_levels=3,
        g_states=2,
        target_observed_per_cell=18,
        post_randomization_attrition_fraction=0.15,
        minimum_joint_outcome_coverage_probability=0.80,
        pre_g_qualification_failure_fraction=0.0,
    )
    naive = plan["post_randomization_outcome_stage"]["naive_expectation_only_plan"]
    assert naive["recruit_per_cell"] == 22
    assert naive["expected_observed_per_cell"] == pytest.approx(18.7)
    assert naive["joint_probability_all_cells_at_least_target"] == pytest.approx(0.21470029037585315)


def test_two_stage_plan_accounts_for_pre_g_manipulation_failure() -> None:
    plan = plan_stage_b_sampling(
        q_levels=3,
        g_states=2,
        target_observed_per_cell=18,
        post_randomization_attrition_fraction=0.15,
        minimum_joint_outcome_coverage_probability=0.90,
        pre_g_qualification_failure_fraction=0.10,
        minimum_joint_pre_g_qualification_probability=0.90,
    )
    pre_g = plan["pre_g_manipulation_qualification_stage"]
    assert pre_g["qualified_units_needed_per_q_level"] == 52
    assert pre_g["initial_candidates_per_q_level"] == 63
    assert pre_g["initial_candidates_total"] == 189
    assert pre_g["joint_probability_all_groups_at_least_target"] >= 0.90


def test_target_20_per_cell_is_more_expensive_and_not_silently_called_power() -> None:
    plan = plan_stage_b_sampling(
        q_levels=3,
        g_states=2,
        target_observed_per_cell=20,
        post_randomization_attrition_fraction=0.15,
        minimum_joint_outcome_coverage_probability=0.90,
        pre_g_qualification_failure_fraction=0.0,
    )
    assert plan["post_randomization_outcome_stage"]["randomized_per_cell"] == 29
    assert plan["post_randomization_outcome_stage"]["randomized_total"] == 174
    assert "not statistical power" in plan["claim_boundary"]


def test_invalid_inputs_fail_closed() -> None:
    with pytest.raises(ValueError, match="at least 3 q levels"):
        plan_stage_b_sampling(
            q_levels=2,
            g_states=2,
            target_observed_per_cell=18,
            post_randomization_attrition_fraction=0.10,
            minimum_joint_outcome_coverage_probability=0.90,
        )
    with pytest.raises(ValueError, match="post_randomization_attrition_fraction"):
        plan_stage_b_sampling(
            q_levels=3,
            g_states=2,
            target_observed_per_cell=18,
            post_randomization_attrition_fraction=1.0,
            minimum_joint_outcome_coverage_probability=0.90,
        )
