from __future__ import annotations

import math

import pytest

from trait_architecture.critical_definition_concordance import (
    analyze_definitions,
    crossing_bracket,
)


def test_default_crossing_is_invariant_to_margin_units() -> None:
    contexts = ("A", "B")
    for scale in (1e-16, 1e-8, 1.0, 1e8, 1e16):
        bracket = crossing_bracket(
            "scaled",
            contexts,
            {"A": -2.0 * scale, "B": 6.0 * scale},
            context_values={"A": 10.0, "B": 14.0},
        )
        assert bracket.status == "UNIQUE_ADJACENT_ZERO_CROSSING"
        assert not bracket.exact_context
        assert math.isclose(bracket.numeric_critical_context, 11.0, rel_tol=0.0, abs_tol=2e-14)


def test_definitions_can_be_rescaled_independently_without_changing_concordance() -> None:
    contexts = ("A", "B")
    reference = analyze_definitions(
        contexts,
        {
            "one": {"A": -1.0, "B": 1.0},
            "two": {"A": -3.0, "B": 1.0},
        },
        context_values={"A": 0.0, "B": 4.0},
        numeric_tolerance=0.5,
    )
    assert reference.classification == "PARALLEL_NUMERIC_CRITICAL_CONTEXTS"

    for first_scale, second_scale in (
        (1e-16, 1e16),
        (1e16, 1e-16),
        (1e-8, 1e8),
    ):
        result = analyze_definitions(
            contexts,
            {
                "one": {"A": -first_scale, "B": first_scale},
                "two": {"A": -3.0 * second_scale, "B": second_scale},
            },
            context_values={"A": 0.0, "B": 4.0},
            numeric_tolerance=0.5,
        )
        assert result.classification == reference.classification
        assert math.isclose(result.brackets[0].numeric_critical_context, 2.0)
        assert math.isclose(result.brackets[1].numeric_critical_context, 3.0)
        assert math.isclose(result.max_pairwise_numeric_gap, 1.0)


def test_strict_tiny_sign_change_is_not_collapsed_by_old_absolute_floor() -> None:
    bracket = crossing_bracket(
        "tiny",
        ("A", "B"),
        {"A": -1e-13, "B": 1e-13},
    )
    assert bracket.status == "UNIQUE_ADJACENT_ZERO_CROSSING"
    assert not bracket.exact_context


def test_explicit_absolute_margin_tolerance_keeps_historical_semantics() -> None:
    with pytest.raises(ValueError, match="multiple/ambiguous zero regions"):
        crossing_bracket(
            "tiny",
            ("A", "B"),
            {"A": -1e-13, "B": 1e-13},
            tolerance=1e-12,
        )


def test_exact_zero_context_remains_exact_at_tiny_margin_scale() -> None:
    bracket = crossing_bracket(
        "exact",
        ("A", "B", "C"),
        {"A": -1e-200, "B": 0.0, "C": 1e-200},
        context_values={"A": 1.0, "B": 2.0, "C": 3.0},
    )
    assert bracket.status == "EXACT_ZERO_CONTEXT"
    assert bracket.exact_context
    assert bracket.left_context == bracket.right_context == "B"
    assert bracket.numeric_critical_context == 2.0


def test_convex_context_interpolation_survives_extreme_finite_endpoints() -> None:
    bracket = crossing_bracket(
        "extreme",
        ("A", "B"),
        {"A": -1.0, "B": 1.0},
        context_values={"A": -1e308, "B": 1e308},
    )
    assert bracket.status == "UNIQUE_ADJACENT_ZERO_CROSSING"
    assert bracket.numeric_critical_context == 0.0
    assert math.isfinite(bracket.numeric_critical_context)
