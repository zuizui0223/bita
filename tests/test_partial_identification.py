from math import inf

import pytest

from trait_architecture.partial_identification import (
    EscapeClaimHierarchy,
    Interval,
    classify_constraint_release,
    classify_escape_claim_hierarchy,
    classify_escape_criterion,
    classify_interaction_relief,
    classify_strict_reversal,
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


def test_legacy_positive_total_interval_identifies_only_algebraic_escape_token() -> None:
    assert classify_escape_criterion(Interval(0.05, 0.30)) == "ESCAPE_IDENTIFIED"
    assert classify_interaction_relief(Interval(0.05, 0.30)) == "POSITIVE_INTERACTION_RELIEF_IDENTIFIED"
    result = partial_identification_from_total(0.2)
    assert not result.point_identified


def test_nonpositive_total_interval_refutes_positive_interaction_relief() -> None:
    assert classify_escape_criterion(Interval(-0.30, 0.0)) == "ESCAPE_REFUTED"
    assert classify_interaction_relief(Interval(-0.30, 0.0)) == "POSITIVE_INTERACTION_RELIEF_REFUTED"


def test_total_interval_crossing_zero_leaves_interaction_relief_unresolved() -> None:
    assert classify_escape_criterion(Interval(-0.05, 0.30)) == "ESCAPE_UNRESOLVED"
    assert classify_escape_criterion(Interval(0.0, 0.30)) == "ESCAPE_UNRESOLVED"
    assert classify_interaction_relief(Interval(-0.05, 0.30)) == "POSITIVE_INTERACTION_RELIEF_UNRESOLVED"


def test_positive_interaction_does_not_by_itself_identify_constraint_release() -> None:
    hierarchy = classify_escape_claim_hierarchy(
        Interval(0.40, 0.80),
        a0_bounds=Interval(-1.00, -0.70),
        a1_bounds=Interval(-0.30, -0.10),
    )
    assert hierarchy == EscapeClaimHierarchy(
        interaction_relief="POSITIVE_INTERACTION_RELIEF_IDENTIFIED",
        constraint_release="CONSTRAINT_RELEASE_REFUTED",
        strict_reversal="STRICT_REVERSAL_REFUTED",
    )


def test_nonpositive_to_positive_transition_identifies_constraint_release() -> None:
    assert (
        classify_constraint_release(Interval(-0.20, 0.0), Interval(0.10, 0.30))
        == "CONSTRAINT_RELEASE_IDENTIFIED"
    )
    assert (
        classify_strict_reversal(Interval(-0.20, 0.0), Interval(0.10, 0.30))
        == "STRICT_REVERSAL_UNRESOLVED"
    )


def test_negative_to_positive_transition_identifies_strict_reversal() -> None:
    hierarchy = classify_escape_claim_hierarchy(
        Interval(0.25, 0.60),
        a0_bounds=Interval(-0.30, -0.05),
        a1_bounds=Interval(0.10, 0.30),
    )
    assert hierarchy.interaction_relief == "POSITIVE_INTERACTION_RELIEF_IDENTIFIED"
    assert hierarchy.constraint_release == "CONSTRAINT_RELEASE_IDENTIFIED"
    assert hierarchy.strict_reversal == "STRICT_REVERSAL_IDENTIFIED"


def test_kessler_like_rounded_ranges_support_relief_but_not_release() -> None:
    hierarchy = classify_escape_claim_hierarchy(
        Interval(0.19, 0.25),
        a0_bounds=Interval(-0.02, 0.02),
        a1_bounds=Interval(0.21, 0.23),
    )
    assert hierarchy.interaction_relief == "POSITIVE_INTERACTION_RELIEF_IDENTIFIED"
    assert hierarchy.constraint_release == "CONSTRAINT_RELEASE_UNRESOLVED"
    assert hierarchy.strict_reversal == "STRICT_REVERSAL_UNRESOLVED"
