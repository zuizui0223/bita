"""Verification of the one-sided selectivity-window bound.

States and checks the claim in ``docs/SELECTIVITY_WINDOW_BOUND.md``: complementarity
never occurs outside the selectivity window, the window is exactly the criterion in
the zero-joint-cost limit, and a negative joint-cost curvature is the only thing that
can break either statement.

The bound is checked exhaustively over the declared grid and every declared
response-shape variant rather than by sampling, because it is a theorem about the
term structure and a single counterexample would refute it.
"""

import itertools
import json
from pathlib import Path

import pytest

from trait_architecture.model import ModelParameters
from trait_architecture.robustness import (
    RobustnessCase,
    default_functional_forms,
    mixed_partial,
)


ROOT = Path(__file__).resolve().parents[1]
GRID_CONFIG = ROOT / "configs" / "part_i_robustness_grid.json"
GRID_AXES = (
    "attraction", "defence", "assurance", "pollinator_service", "floral_damage_pressure",
)


def _config() -> dict:
    return json.loads(GRID_CONFIG.read_text(encoding="utf-8"))


def _declared_evaluations(*, zero_joint_cost: bool = False):
    """Yield every (result, inside_window, complementary) over the declared design."""

    config = _config()
    grid = config["phenotype_and_regime_grid"]
    for scenario in config["parameter_scenarios"]:
        overrides = dict(scenario["overrides"])
        if zero_joint_cost:
            overrides["attraction_defence_shared_cost"] = 0.0
        parameters = ModelParameters(**overrides)
        for values in itertools.product(*(grid[axis] for axis in GRID_AXES)):
            case = RobustnessCase(case_id="grid", **dict(zip(GRID_AXES, values)))
            for form in default_functional_forms():
                result = mixed_partial(case, parameters, form)
                inside = result.antagonism_term > result.pollination_obstruction_term
                yield result, inside, result.mixed_partial > 0


def test_declared_design_is_the_size_the_readout_reports() -> None:
    assert sum(1 for _ in _declared_evaluations()) == 2592


def test_all_three_terms_are_non_negative_under_every_variant() -> None:
    """The premise the theorem rests on, checked rather than assumed."""

    for result, _, _ in _declared_evaluations():
        assert result.antagonism_term >= 0
        assert result.pollination_obstruction_term >= 0
        assert result.joint_cost_curvature_term >= 0


def test_complementarity_never_occurs_outside_the_selectivity_window() -> None:
    """The one-sided bound. A single failure here refutes the claim."""

    outside_and_complementary = [
        result for result, inside, positive in _declared_evaluations()
        if positive and not inside
    ]
    assert outside_and_complementary == []


def test_the_bound_holds_under_each_response_shape_variant_separately() -> None:
    """Guards against a variant being masked by aggregation across variants."""

    config = _config()
    grid = config["phenotype_and_regime_grid"]
    for form in default_functional_forms():
        for scenario in config["parameter_scenarios"]:
            parameters = ModelParameters(**scenario["overrides"])
            for values in itertools.product(*(grid[axis] for axis in GRID_AXES)):
                case = RobustnessCase(case_id="grid", **dict(zip(GRID_AXES, values)))
                result = mixed_partial(case, parameters, form)
                if result.mixed_partial > 0:
                    assert result.antagonism_term > result.pollination_obstruction_term, (
                        form.form_id, scenario["scenario_id"], values
                    )


def test_window_is_exactly_the_criterion_when_joint_cost_is_zero() -> None:
    """In the zero-joint-cost limit the implication runs both ways."""

    for result, inside, positive in _declared_evaluations(zero_joint_cost=True):
        assert inside == positive, result


def test_the_bound_is_strictly_loose_with_the_declared_joint_cost() -> None:
    """A bound that were also tight would make the joint-cost term redundant."""

    evaluations = list(_declared_evaluations())
    complementary = sum(1 for _, _, positive in evaluations if positive)
    loose = sum(1 for _, inside, positive in evaluations if inside and not positive)
    assert loose > 0
    precision = complementary / (complementary + loose)
    # Committed in docs/SELECTIVITY_WINDOW_BOUND.md as 77.2%.
    assert precision == pytest.approx(0.772, abs=0.001)


def test_only_a_negative_joint_cost_could_place_complementarity_outside_the_window() -> None:
    """The failure mode, checked on the term algebra rather than argued.

    Outside the window means ``antagonism <= obstruction``. Complementarity there
    requires ``antagonism - obstruction - cost > 0``, so ``cost < antagonism -
    obstruction <= 0``. This reconstructs that implication from the committed
    evaluations: wherever a point is outside the window, the joint cost that would
    be needed to make it complementary is negative.
    """

    checked = 0
    for result, inside, _ in _declared_evaluations():
        if inside:
            continue
        required_cost = result.antagonism_term - result.pollination_obstruction_term
        assert required_cost <= 0
        assert result.joint_cost_curvature_term >= 0
        assert result.mixed_partial <= 0
        checked += 1
    assert checked > 0


def test_declared_parameterization_forbids_the_failure_mode() -> None:
    """The bound is carried by a declared constraint, not by biology."""

    with pytest.raises(ValueError):
        ModelParameters(attraction_defence_shared_cost=-0.01)


def test_document_reports_the_verified_numbers() -> None:
    text = (ROOT / "docs" / "SELECTIVITY_WINDOW_BOUND.md").read_text(encoding="utf-8")
    for token in ("2592", "77.2%", "100.0%", "51.8%", "67.1%"):
        assert token in text, token
    # The claim must stay one-sided in the prose, not just in the code.
    assert "Complementarity does not occur outside the selectivity window" in text
