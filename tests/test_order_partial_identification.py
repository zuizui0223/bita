import math

import pytest

from trait_architecture.order_partial_identification import (
    exact_order_margin_bounds,
    order_margin_bounds,
)


def test_exact_order_bounds_certify_unmeasured_bita_state():
    points = [(0.0, 0.0), (0.4, 0.2), (0.8, 0.8)]
    margins = [-0.6, 0.2, 1.0]
    result = exact_order_margin_bounds((0.6, 0.5), points, margins)
    assert result.lower == pytest.approx(0.2)
    assert result.upper == pytest.approx(1.0)
    assert result.classification == "BITA_SIDE_CERTIFIED"


def test_exact_order_bounds_certify_shared_side_from_dominating_sample():
    points = [(0.0, 0.0), (0.5, 0.5), (1.0, 1.0)]
    margins = [-1.0, -0.2, 0.8]
    result = exact_order_margin_bounds((0.3, 0.3), points, margins)
    assert result.lower == pytest.approx(-1.0)
    assert result.upper == pytest.approx(-0.2)
    assert result.classification == "SHARED_OR_BOUNDARY_CERTIFIED"


def test_incomparable_samples_leave_query_unresolved():
    points = [(1.0, 0.0), (0.0, 1.0)]
    margins = [0.4, 0.5]
    result = exact_order_margin_bounds((0.5, 0.5), points, margins)
    assert math.isinf(result.lower) and result.lower < 0
    assert math.isinf(result.upper) and result.upper > 0
    assert result.classification == "ORDER_UNRESOLVED"


def test_interval_order_bounds_propagate_uncertainty():
    points = [(0.0, 0.0), (0.4, 0.4), (1.0, 1.0)]
    intervals = [(-1.0, -0.8), (0.1, 0.3), (0.9, 1.2)]
    result = order_margin_bounds((0.7, 0.7), points, intervals)
    assert result.lower == pytest.approx(0.1)
    assert result.upper == pytest.approx(1.2)
    assert result.classification == "BITA_SIDE_CERTIFIED"


def test_monotonicity_inconsistency_is_fail_closed():
    points = [(0.2, 0.2), (0.8, 0.8)]
    intervals = [(0.5, 0.7), (-0.3, -0.1)]
    result = order_margin_bounds((0.5, 0.5), points, intervals)
    assert result.lower > result.upper
    assert result.classification == "MONOTONICITY_INCONSISTENT"


def test_invalid_intervals_fail_closed():
    with pytest.raises(ValueError):
        order_margin_bounds(
            (0.5, 0.5),
            [(0.0, 0.0)],
            [(1.0, 0.0)],
        )
