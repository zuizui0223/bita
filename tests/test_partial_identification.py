from math import inf

import pytest

from trait_architecture.partial_identification import (
    Interval,
    classify_escape_criterion,
    partial_identification_from_total,
)


def test_total_interaction_alone_does_not_bound_channels() -> None:
    result = partial_identification_from_total(0.2)
    assert result.feasible
    assert result.rho == Interval(-inf, inf)
    assert result.iota == Interval(-inf, inf)
    assert result.kappa == Interval(-inf, inf)
    assert not result.point_identified


def test_nonnegative_channels_turn_positive_total_into_rho_lower_bound() -> None:
    nonnegative = Interval(0.0, inf)
    result = partial_identification_from_total(
        0.2,
        rho_bounds=nonnegative,
        iota_bounds=nonnegative,
        kappa_bounds=nonnegative,
    )
    assert result.feasible
    assert result.rho == Interval(0.2, inf)
    assert result.iota == Interval(0.0, inf)
    assert result.kappa == Interval(0.0, inf)
    assert result.rho.sign_status == "positive"


def test_bounded_interference_and_cost_sharpen_rho_interval() -> None:
    result = partial_identification_from_total(
        0.2,
        rho_bounds=Interval(0.0, inf),
        iota_bounds=Interval(0.0, 0.10),
        kappa_bounds=Interval(0.0, 0.05),
    )
    assert result.feasible
    assert result.rho.low == pytest.approx(0.20)
    assert result.rho.high == pytest.approx(0.35)


def test_selective_rho_measurement_plus_cost_bound_sharpens_iota() -> None:
    result = partial_identification_from_total(
        0.2,
        rho_bounds=Interval(0.25, 0.30),
        iota_bounds=Interval(0.0, inf),
        kappa_bounds=Interval(0.0, 0.05),
    )
    assert result.feasible
    assert result.iota.low == pytest.approx(0.0)
    assert result.iota.high == pytest.approx(0.10)


def test_incompatible_channel_bounds_are_detected() -> None:
    result = partial_identification_from_total(
        1.0,
        rho_bounds=Interval(0.0, 0.1),
        iota_bounds=Interval(0.0, 0.1),
        kappa_bounds=Interval(0.0, 0.1),
    )
    assert not result.feasible
    assert result.rho is None
    assert result.iota is None
    assert result.kappa is None


def test_positive_total_interval_identifies_escape_without_channel_allocation() -> None:
    assert classify_escape_criterion(Interval(0.05, 0.30)) == "ESCAPE_IDENTIFIED"
    result = partial_identification_from_total(0.2)
    assert not result.point_identified


def test_nonpositive_total_interval_refutes_strict_escape() -> None:
    assert classify_escape_criterion(Interval(-0.30, 0.0)) == "ESCAPE_REFUTED"


def test_total_interval_crossing_zero_leaves_escape_unresolved() -> None:
    assert classify_escape_criterion(Interval(-0.05, 0.30)) == "ESCAPE_UNRESOLVED"
    assert classify_escape_criterion(Interval(0.0, 0.30)) == "ESCAPE_UNRESOLVED"
