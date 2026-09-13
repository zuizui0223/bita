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


def test_interpolated_crossing_is_invariant_to_margin_units() -> None:
    baseline = zero_crossing([(0.0, -1.0), (2.0, 1.0)])
    for scale in (1e-16, 1e-13, 1.0, 1e16):
        crossing = zero_crossing([(0.0, -scale), (2.0, scale)])
        assert math.isclose(crossing.context, baseline.context, abs_tol=1e-15)
        assert crossing.exact_grid_hit is False


def test_small_unit_bracket_is_not_promoted_to_two_exact_grid_hits() -> None:
    crossing = zero_crossing([(0.0, -1e-13), (2.0, 1e-13)])
    assert crossing.context == 1.0
    assert crossing.exact_grid_hit is False


def test_large_finite_crossing_is_overflow_safe() -> None:
    crossing = zero_crossing([(-1e308, -1e308), (1e308, 1e308)])
    assert math.isfinite(crossing.context)
    assert crossing.context == 0.0
    assert crossing.exact_grid_hit is False


def test_margin_tolerance_is_not_used_to_deduplicate_context_coordinates() -> None:
    with pytest.raises(ValueError, match="multiple zero crossings"):
        zero_crossing([(0.0, 0.0), (5e-13, 0.0), (1.0, 1.0)])


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
