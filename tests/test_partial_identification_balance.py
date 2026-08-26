from math import inf

import pytest

from trait_architecture.partial_identification import Interval, partial_identification_from_total


def test_total_only_leaves_biotic_balance_unbounded() -> None:
    result = partial_identification_from_total(0.2)
    assert result.feasible
    assert result.biotic_balance == Interval(-inf, inf)


def test_nonnegative_kappa_sharply_bounds_biotic_balance_without_bounding_channels() -> None:
    result = partial_identification_from_total(
        0.2,
        kappa_bounds=Interval(0.0, inf),
    )
    assert result.feasible
    assert result.rho == Interval(-inf, inf)
    assert result.iota == Interval(-inf, inf)
    assert result.kappa == Interval(0.0, inf)
    assert result.biotic_balance == Interval(0.2, inf)
    assert result.biotic_balance.sign_status == "positive"


def test_bounded_cost_maps_one_to_one_to_biotic_balance() -> None:
    result = partial_identification_from_total(
        0.2,
        kappa_bounds=Interval(-0.05, 0.10),
    )
    assert result.feasible
    assert result.biotic_balance.low == pytest.approx(0.15)
    assert result.biotic_balance.high == pytest.approx(0.30)


def test_negative_total_with_nonnegative_kappa_does_not_force_positive_balance() -> None:
    result = partial_identification_from_total(
        -0.2,
        kappa_bounds=Interval(0.0, 0.10),
    )
    assert result.feasible
    assert result.biotic_balance == Interval(-0.2, -0.1)
    assert result.biotic_balance.sign_status == "negative"


def test_infeasible_result_has_no_biotic_balance() -> None:
    result = partial_identification_from_total(
        1.0,
        rho_bounds=Interval(0.0, 0.1),
        iota_bounds=Interval(0.0, 0.1),
        kappa_bounds=Interval(0.0, 0.1),
    )
    assert not result.feasible
    assert result.biotic_balance is None
