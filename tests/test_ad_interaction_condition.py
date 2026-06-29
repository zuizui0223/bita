from math import isclose

import pytest

from trait_architecture.ad_interaction_condition import (
    ADLocalRelation,
    attraction_defence_cross_partial,
    floral_pressure_threshold_for_complementarity,
)
from trait_architecture.model import Architecture, InteractionRegime, ModelParameters, fitness


def _finite_difference_cross_partial(
    architecture: Architecture,
    regime: InteractionRegime,
    parameters: ModelParameters,
    epsilon: float = 1e-4,
) -> float:
    a, d, r = architecture.attraction, architecture.defence, architecture.assurance

    def score(a_value: float, d_value: float) -> float:
        return fitness(Architecture(a_value, d_value, r), regime, parameters).total

    return (
        score(a + epsilon, d + epsilon)
        - score(a + epsilon, d - epsilon)
        - score(a - epsilon, d + epsilon)
        + score(a - epsilon, d - epsilon)
    ) / (4.0 * epsilon * epsilon)


def test_closed_form_cross_partial_matches_fitness_score() -> None:
    architecture = Architecture(0.5, 0.5, 0.4)
    regime = InteractionRegime(0.7, 0.6, 0.9)
    parameters = ModelParameters(
        defence_pollinator_cost=0.4,
        attraction_tracking=1.3,
        floral_defence_efficacy=0.8,
        attraction_defence_shared_cost=0.12,
    )

    derived = attraction_defence_cross_partial(architecture, regime, parameters)
    numerical = _finite_difference_cross_partial(architecture, regime, parameters)

    assert derived.cross_partial == pytest.approx(numerical, abs=1e-7)


def test_strong_floral_damage_relief_can_create_complementarity() -> None:
    condition = attraction_defence_cross_partial(
        Architecture(0.5, 0.5, 0.2),
        InteractionRegime(0.1, 1.0, 0.0),
        ModelParameters(
            defence_pollinator_cost=0.05,
            attraction_tracking=2.0,
            floral_defence_efficacy=1.0,
            attraction_defence_shared_cost=0.0,
        ),
    )

    assert condition.relation is ADLocalRelation.COMPLEMENTARY
    assert condition.floral_damage_relief > condition.pollination_access_penalty


def test_pollination_access_and_shared_cost_can_create_substitutability() -> None:
    condition = attraction_defence_cross_partial(
        Architecture(0.5, 0.5, 0.0),
        InteractionRegime(1.0, 0.0, 1.0),
        ModelParameters(
            defence_pollinator_cost=1.0,
            attraction_defence_shared_cost=0.2,
        ),
    )

    assert condition.relation is ADLocalRelation.SUBSTITUTABLE
    assert condition.cross_partial < 0.0


def test_leaf_pressure_does_not_enter_direct_cross_partial() -> None:
    architecture = Architecture(0.5, 0.5, 0.2)
    parameters = ModelParameters()
    low_leaf = attraction_defence_cross_partial(
        architecture,
        InteractionRegime(0.6, 0.5, 0.0),
        parameters,
    )
    high_leaf = attraction_defence_cross_partial(
        architecture,
        InteractionRegime(0.6, 0.5, 1.0),
        parameters,
    )

    assert low_leaf.cross_partial == high_leaf.cross_partial


def test_threshold_marks_boundary_between_negative_and_positive_relations() -> None:
    architecture = Architecture(0.5, 0.5, 0.2)
    parameters = ModelParameters(
        defence_pollinator_cost=0.2,
        attraction_tracking=1.0,
        floral_defence_efficacy=0.8,
        attraction_defence_shared_cost=0.05,
    )
    regime = InteractionRegime(0.6, 0.0, 0.0)

    threshold = floral_pressure_threshold_for_complementarity(architecture, regime, parameters)
    assert threshold is not None

    at_boundary = attraction_defence_cross_partial(
        architecture,
        InteractionRegime(0.6, threshold, 0.0),
        parameters,
    )
    assert isclose(at_boundary.cross_partial, 0.0, abs_tol=1e-12)
    assert at_boundary.relation is ADLocalRelation.NEUTRAL


def test_threshold_is_undefined_without_tracking_or_effective_floral_defence() -> None:
    architecture = Architecture(0.5, 0.5, 0.2)
    regime = InteractionRegime(0.6, 0.5, 0.0)

    assert floral_pressure_threshold_for_complementarity(
        architecture,
        regime,
        ModelParameters(attraction_tracking=0.0),
    ) is None
    assert floral_pressure_threshold_for_complementarity(
        architecture,
        regime,
        ModelParameters(floral_defence_efficacy=0.0),
    ) is None
