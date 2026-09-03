import math

import pytest

from trait_architecture.functional_differentiation import (
    compromise_penalty,
    differentiation_favored,
    differentiation_gain,
    shared_optimum,
)


def test_equal_weights_place_shared_optimum_midway():
    assert shared_optimum(0.0, 2.0, 1.0, 1.0) == pytest.approx(1.0)


def test_shared_optimum_is_weighted_toward_stronger_function():
    assert shared_optimum(0.0, 2.0, 3.0, 1.0) == pytest.approx(0.5)


def test_compromise_penalty_matches_closed_form_example():
    # a=b=1 and optimum separation=2 -> (1/2)*4 = 2
    assert compromise_penalty(0.0, 2.0, 1.0, 1.0) == pytest.approx(2.0)


def test_compromise_penalty_is_symmetric_between_functions():
    left = compromise_penalty(-1.0, 3.0, 2.0, 5.0)
    right = compromise_penalty(3.0, -1.0, 5.0, 2.0)
    assert left == pytest.approx(right)


def test_compromise_penalty_shrinks_when_one_function_is_weak():
    strong_both = compromise_penalty(0.0, 2.0, 1.0, 1.0)
    weak_second = compromise_penalty(0.0, 2.0, 1.0, 1e-6)
    assert weak_second < strong_both
    assert weak_second < 1e-4


def test_differentiation_gain_equals_avoided_penalty_minus_cost():
    penalty = compromise_penalty(0.0, 2.0, 1.0, 1.0)
    gain = differentiation_gain(0.0, 2.0, 1.0, 1.0, extra_cost=0.75)
    assert gain == pytest.approx(penalty - 0.75)


def test_differentiation_threshold():
    penalty = compromise_penalty(0.0, 2.0, 1.0, 1.0)
    assert differentiation_favored(0.0, 2.0, 1.0, 1.0, extra_cost=penalty - 0.01)
    assert not differentiation_favored(0.0, 2.0, 1.0, 1.0, extra_cost=penalty)
    assert not differentiation_favored(0.0, 2.0, 1.0, 1.0, extra_cost=penalty + 0.01)


@pytest.mark.parametrize("a,b", [(0.0, 1.0), (1.0, 0.0), (-1.0, 1.0), (1.0, -1.0)])
def test_nonpositive_curvatures_are_rejected(a, b):
    with pytest.raises(ValueError):
        shared_optimum(0.0, 1.0, a, b)
    with pytest.raises(ValueError):
        compromise_penalty(0.0, 1.0, a, b)
