import math

import pytest

from trait_architecture.critical_context import compare_critical_contexts, zero_crossing


def test_linear_zero_crossing_interpolates_between_contexts() -> None:
    crossing = zero_crossing([(0.0, -1.0), (2.0, 1.0)])
    assert math.isclose(crossing.context, 1.0)
    assert crossing.exact_grid_hit is False


def test_exact_grid_zero_is_retained() -> None:
    crossing = zero_crossing([(0.0, -1.0), (1.0, 0.0), (2.0, 1.0)])
    assert crossing.context == 1.0
    assert crossing.exact_grid_hit is True


def test_same_latent_critical_context_is_recovered_despite_margin_rescaling() -> None:
    result = compare_critical_contexts(
        sch_points=[(0.0, -1.0), (1.0, 0.0), (2.0, 1.0)],
        bita_points=[(0.0, -2.0), (1.0, 0.0), (2.0, 2.0)],
        context_tolerance=0.05,
    )
    assert result.sch_crossing.context == 1.0
    assert result.bita_crossing.context == 1.0
    assert result.delta_context == 0.0
    assert result.classification == "SAME_CRITICAL_CONTEXT_COMPATIBLE"


def test_parallel_world_crossings_are_detected() -> None:
    result = compare_critical_contexts(
        sch_points=[(0.0, -1.0), (2.0, 1.0)],
        bita_points=[(0.0, -1.5), (3.0, 1.5)],
        context_tolerance=0.1,
    )
    assert math.isclose(result.sch_crossing.context, 1.0)
    assert math.isclose(result.bita_crossing.context, 1.5)
    assert math.isclose(result.delta_context, 0.5)
    assert result.classification == "PARALLEL_WORLD_CRITICAL_CONTEXTS"


def test_multiple_crossings_fail_closed() -> None:
    with pytest.raises(ValueError, match="multiple zero crossings"):
        zero_crossing([(0.0, -1.0), (1.0, 1.0), (2.0, -1.0)])
