from __future__ import annotations

import argparse
import json
import math


PLANNER_SCHEMA = "BITA_PEUCEDANUM_STAGE_B_COVERAGE_PLAN_V1"


def binomial_tail_at_least(n: int, retention_probability: float, target: int) -> float:
    if n < 0 or target < 0 or target > n:
        return 0.0
    if not 0 <= retention_probability <= 1:
        raise ValueError("retention_probability must be on [0,1]")
    return sum(
        math.comb(n, k)
        * retention_probability**k
        * (1.0 - retention_probability) ** (n - k)
        for k in range(target, n + 1)
    )


def minimum_recruitment(
    *,
    target_retained: int,
    retention_probability: float,
    groups: int,
    minimum_joint_probability: float,
    search_limit: int = 10000,
) -> dict:
    if target_retained < 1:
        raise ValueError("target_retained must be >= 1")
    if groups < 1:
        raise ValueError("groups must be >= 1")
    if not 0 < retention_probability <= 1:
        raise ValueError("retention_probability must be on (0,1]")
    if not 0 < minimum_joint_probability < 1:
        raise ValueError("minimum_joint_probability must be on (0,1)")

    for recruited in range(target_retained, search_limit + 1):
        one_group = binomial_tail_at_least(recruited, retention_probability, target_retained)
        joint = one_group**groups
        if joint >= minimum_joint_probability:
            return {
                "target_retained_per_group": target_retained,
                "retention_probability": retention_probability,
                "groups": groups,
                "minimum_joint_probability": minimum_joint_probability,
                "recruit_per_group": recruited,
                "total_recruit": recruited * groups,
                "expected_retained_per_group": recruited * retention_probability,
                "one_group_probability_at_least_target": one_group,
                "joint_probability_all_groups_at_least_target": joint,
            }
    raise ValueError("no recruitment size found inside search_limit")


def plan_stage_b_sampling(
    *,
    q_levels: int,
    g_states: int,
    target_observed_per_cell: int,
    post_randomization_attrition_fraction: float,
    minimum_joint_outcome_coverage_probability: float,
    pre_g_qualification_failure_fraction: float = 0.0,
    minimum_joint_pre_g_qualification_probability: float | None = None,
) -> dict:
    if q_levels < 3:
        raise ValueError("Stage-B quadratic optimum design requires at least 3 q levels")
    if g_states < 2:
        raise ValueError("Stage-B causal design requires at least 2 G states")
    for name, value in (
        ("post_randomization_attrition_fraction", post_randomization_attrition_fraction),
        ("pre_g_qualification_failure_fraction", pre_g_qualification_failure_fraction),
    ):
        if not 0 <= value < 1:
            raise ValueError(f"{name} must be on [0,1)")

    cells = q_levels * g_states
    post_retention = 1.0 - post_randomization_attrition_fraction
    outcome_plan = minimum_recruitment(
        target_retained=target_observed_per_cell,
        retention_probability=post_retention,
        groups=cells,
        minimum_joint_probability=minimum_joint_outcome_coverage_probability,
    )

    naive_recruit_per_cell = math.ceil(target_observed_per_cell / post_retention)
    naive_one_cell = binomial_tail_at_least(
        naive_recruit_per_cell, post_retention, target_observed_per_cell
    )
    naive_joint = naive_one_cell**cells

    randomized_per_cell = outcome_plan["recruit_per_group"]
    qualified_needed_per_q = randomized_per_cell * g_states
    if minimum_joint_pre_g_qualification_probability is None:
        minimum_joint_pre_g_qualification_probability = minimum_joint_outcome_coverage_probability

    pre_g_retention = 1.0 - pre_g_qualification_failure_fraction
    qualification_plan = minimum_recruitment(
        target_retained=qualified_needed_per_q,
        retention_probability=pre_g_retention,
        groups=q_levels,
        minimum_joint_probability=minimum_joint_pre_g_qualification_probability,
    )

    return {
        "planner_schema_version": PLANNER_SCHEMA,
        "interpretation": "coverage_and_attrition_planning_not_formal_power",
        "design": {
            "q_levels": q_levels,
            "g_states": g_states,
            "q_by_g_cells": cells,
            "target_observed_per_cell": target_observed_per_cell,
        },
        "post_randomization_outcome_stage": {
            "anticipated_attrition_fraction": post_randomization_attrition_fraction,
            **outcome_plan,
            "randomized_per_cell": randomized_per_cell,
            "randomized_total": randomized_per_cell * cells,
            "complete_six_cell_block_survival_probability_if_cells_equal_six": (
                post_retention**6 if cells == 6 else None
            ),
            "naive_expectation_only_plan": {
                "recruit_per_cell": naive_recruit_per_cell,
                "total_randomized": naive_recruit_per_cell * cells,
                "expected_observed_per_cell": naive_recruit_per_cell * post_retention,
                "one_cell_probability_at_least_target": naive_one_cell,
                "joint_probability_all_cells_at_least_target": naive_joint,
            },
        },
        "pre_g_manipulation_qualification_stage": {
            "anticipated_failure_fraction": pre_g_qualification_failure_fraction,
            "qualified_units_needed_per_q_level": qualified_needed_per_q,
            **qualification_plan,
            "initial_candidates_per_q_level": qualification_plan["recruit_per_group"],
            "initial_candidates_total": qualification_plan["total_recruit"],
        },
        "claim_boundary": (
            "This calculation targets operational cell coverage under independent Bernoulli loss. "
            "It is not statistical power for Delta_q_star and does not justify confirmatory effect thresholds."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Plan Peucedanum Stage-B recruitment under two-stage attrition")
    parser.add_argument("--q-levels", type=int, default=3)
    parser.add_argument("--g-states", type=int, default=2)
    parser.add_argument("--target-observed-per-cell", type=int, required=True)
    parser.add_argument("--post-randomization-attrition", type=float, required=True)
    parser.add_argument("--joint-outcome-coverage", type=float, default=0.90)
    parser.add_argument("--pre-g-qualification-failure", type=float, default=0.0)
    parser.add_argument("--joint-pre-g-qualification", type=float)
    args = parser.parse_args()

    result = plan_stage_b_sampling(
        q_levels=args.q_levels,
        g_states=args.g_states,
        target_observed_per_cell=args.target_observed_per_cell,
        post_randomization_attrition_fraction=args.post_randomization_attrition,
        minimum_joint_outcome_coverage_probability=args.joint_outcome_coverage,
        pre_g_qualification_failure_fraction=args.pre_g_qualification_failure,
        minimum_joint_pre_g_qualification_probability=args.joint_pre_g_qualification,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
