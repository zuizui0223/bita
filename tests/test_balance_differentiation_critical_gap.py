import math

from trait_architecture.criticality import critical_shared_load


def test_positive_cost_creates_nonzero_balance_only_interval() -> None:
    s = 0.25
    k = 0.2
    c0 = 0.0
    c2 = critical_shared_load(k, s)
    assert math.isclose(c2, 0.8)
    assert c2 - c0 > 0


def test_zero_cost_collapses_architecture_threshold_to_conflict_onset() -> None:
    for s in (0.1, 0.5, 1.0):
        assert critical_shared_load(0.0, s) == 0.0


def test_no_decoupling_with_positive_cost_pushes_threshold_to_infinity() -> None:
    assert math.isinf(critical_shared_load(0.1, 0.0))
