import math

import pytest

from trait_architecture.balance_domain import (
    analyze_balance_domain_path,
    classify_balance_point,
    monotone_no_reentry_guarantee,
)


def test_point_definitions_recover_balance_and_criticality_index():
    r, phi, q, reserve, state = classify_balance_point(
        conflict_load=0.6,
        decoupling=0.5,
        architecture_cost=0.4,
    )
    assert r == pytest.approx(0.3)
    assert phi == pytest.approx(-0.1)
    assert q == pytest.approx(0.75)
    assert reserve == pytest.approx(0.1)
    assert state == "balance"


def test_monotone_path_has_single_balance_to_differentiation_transition():
    result = analyze_balance_domain_path(
        environment=[0, 1, 2, 3],
        conflict_load=[0.0, 0.4, 0.8, 1.2],
        decoupling=[0.5, 0.5, 0.5, 0.5],
        architecture_cost=[0.4, 0.4, 0.4, 0.4],
    )
    assert result.topology == "balance_to_differentiation"
    assert result.zero_crossings == pytest.approx((2.0,))
    assert result.monotone_no_reentry_guarantee is True
    assert result.balance_width == pytest.approx(2.0)


def test_all_balance_when_cost_exceeds_recoverable_loss_everywhere():
    result = analyze_balance_domain_path(
        environment=[0, 1, 2, 3],
        conflict_load=[0.0, 0.2, 0.4, 0.6],
        decoupling=[0.5, 0.5, 0.5, 0.5],
        architecture_cost=[1.0, 1.0, 1.0, 1.0],
    )
    assert result.topology == "all_balance"
    assert not result.zero_crossings
    assert result.monotone_no_reentry_guarantee is True


def test_reentrant_balance_requires_breaking_monotone_sufficient_condition():
    result = analyze_balance_domain_path(
        environment=[0, 1, 2, 3, 4],
        conflict_load=[1, 1, 1, 1, 1],
        decoupling=[0.2, 0.8, 0.8, 0.2, 0.2],
        architecture_cost=[0.5, 0.5, 0.5, 0.5, 0.5],
    )
    assert result.topology == "reentrant"
    assert len(result.zero_crossings) == 2
    assert result.zero_crossings == pytest.approx((0.5, 2.5))
    assert result.monotone_no_reentry_guarantee is False


def test_cost_increase_can_generate_differentiation_to_balance_reentry():
    result = analyze_balance_domain_path(
        environment=[0, 1, 2],
        conflict_load=[1, 1, 1],
        decoupling=[0.8, 0.8, 0.8],
        architecture_cost=[0.2, 0.6, 1.0],
    )
    assert result.topology == "differentiation_to_balance"
    assert result.monotone_no_reentry_guarantee is False


def test_monotone_no_reentry_gate_is_only_sufficient_not_required():
    assert monotone_no_reentry_guarantee(
        conflict_load=[0.1, 0.2, 0.3],
        decoupling=[0.2, 0.3, 0.4],
        architecture_cost=[1.0, 0.9, 0.8],
    )
    assert not monotone_no_reentry_guarantee(
        conflict_load=[0.1, 0.2, 0.3],
        decoupling=[0.4, 0.3, 0.4],
        architecture_cost=[1.0, 0.9, 0.8],
    )


def test_fail_closed_on_invalid_scales():
    with pytest.raises(ValueError):
        classify_balance_point(conflict_load=-0.1, decoupling=0.5, architecture_cost=1)
    with pytest.raises(ValueError):
        classify_balance_point(conflict_load=1, decoupling=1.1, architecture_cost=1)
    with pytest.raises(ValueError):
        analyze_balance_domain_path(
            environment=[0, 0],
            conflict_load=[0, 1],
            decoupling=[0.5, 0.5],
            architecture_cost=[1, 1],
        )
