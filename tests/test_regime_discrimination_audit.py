from trait_architecture.regime_discrimination_audit import audit, functional_signature


def config(*, zero_cost: bool = False) -> dict[str, object]:
    scenarios: list[dict[str, object]] = [
        {"scenario_id": "complementary", "overrides": {"attraction_tracking": 1.6, "defence_pollinator_cost": 0.2, "attraction_defence_shared_cost": 0.03}},
        {"scenario_id": "substitutable", "overrides": {"attraction_tracking": 0.8, "defence_pollinator_cost": 0.9, "attraction_defence_shared_cost": 0.25}},
    ]
    if zero_cost:
        scenarios.append({"scenario_id": "zero_cost", "overrides": {"defence_pollinator_cost": 0.0}})
    return {"parameter_scenarios": scenarios}


def summary(scenario_id: str, modal: str) -> dict[str, str]:
    return {
        "parameter_scenario_id": scenario_id,
        "modal_sign": modal,
        "functional_form_class": "tested_set_unanimous",
    }


def b_to_p_constraint(**overrides: str) -> dict[str, str]:
    row = {
        "route": "B_to_pollination",
        "trait_class": "chemical_barrier",
        "outcome_class": "pollinator_preference_or_foraging",
        "design_class": "manipulation",
        "direction_map_status": "mostly_compatible_with_channel_assumption",
        "positive_count": "0",
        "negative_count": "3",
        "independent_clusters": "3",
    }
    row.update(overrides)
    return row


def test_negative_b_to_p_constraint_does_not_choose_between_surviving_regime_types() -> None:
    report, scenarios, constraints = audit(
        config=config(),
        functional_rows=[summary("complementary", "complementary"), summary("substitutable", "substitutable")],
        direction_rows=[b_to_p_constraint()],
    )

    assert report["resolved_empirical_constraints"] == 1
    assert report["surviving_scenario_count"] == 2
    assert report["excluded_scenario_count"] == 0
    assert report["regime_discrimination"] == "not_identified_current_constraints_allow_both_complementary_and_substitutable_scenarios"
    assert {row["scenario_empirical_status"] for row in scenarios} == {"directionally_compatible_not_magnitude_identified"}
    assert {row["constraint_status"] for row in constraints} == {"matches_directional_constraint"}


def test_zero_pollination_cost_is_excluded_by_negative_b_to_p_constraint() -> None:
    report, scenarios, constraints = audit(
        config=config(zero_cost=True),
        functional_rows=[
            summary("complementary", "complementary"),
            summary("substitutable", "substitutable"),
            summary("zero_cost", "complementary"),
        ],
        direction_rows=[b_to_p_constraint()],
    )

    zero = next(row for row in scenarios if row["scenario_id"] == "zero_cost")
    zero_constraint = next(row for row in constraints if row["scenario_id"] == "zero_cost")
    assert zero["scenario_empirical_status"] == "excluded_by_current_directional_constraint"
    assert zero_constraint["scenario_expected_direction"] == "neutral"
    assert zero_constraint["constraint_status"] == "contradicts_directional_constraint"
    assert report["excluded_scenario_count"] == 1


def test_unresolved_strata_are_not_promoted_to_empirical_constraints() -> None:
    report, scenarios, constraints = audit(
        config=config(),
        functional_rows=[summary("complementary", "complementary"), summary("substitutable", "substitutable")],
        direction_rows=[b_to_p_constraint(direction_map_status="insufficient_directional_clusters")],
    )

    assert report["resolved_empirical_constraints"] == 0
    assert constraints == []
    assert {row["scenario_empirical_status"] for row in scenarios} == {"no_resolved_empirical_constraint"}


def test_functional_signature_preserves_mixed_modal_cases() -> None:
    signature = functional_signature([
        summary("one", "mixed"),
        summary("one", "complementary"),
    ])

    assert signature["one"] == {
        "total": 2,
        "complementary": 1,
        "substitutable": 0,
        "mixed": 1,
        "unanimous": 2,
    }
