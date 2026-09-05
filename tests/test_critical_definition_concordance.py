import math

import pytest

from trait_architecture.critical_definition_concordance import (
    analyze_definitions,
    crossing_bracket,
)


CONTEXTS = ("HA", "HL", "HC", "KD", "HD")


def test_peucedanum_three_definitions_share_hl_hc_bracket() -> None:
    result = analyze_definitions(
        CONTEXTS,
        {
            "final_fruit_beta": {
                "HA": -0.035,
                "HL": -0.029,
                "HC": 0.034,
                "KD": 0.008,
                "HD": 0.026,
            },
            "final_fruit_S": {
                "HA": -0.027,
                "HL": -0.051,
                "HC": 0.036,
                "KD": 0.021,
                "HD": 0.024,
            },
            "female_gain_b_minus_1": {
                "HA": -0.37,
                "HL": -0.55,
                "HC": 0.15,
                "KD": 0.26,
                "HD": 0.55,
            },
        },
    )
    assert result.classification == "SAME_COARSE_CRITICAL_BRACKET"
    assert result.common_contexts == ("HL", "HC")
    assert all(
        (bracket.left_context, bracket.right_context) == ("HL", "HC")
        for bracket in result.brackets
    )
    assert result.max_pairwise_numeric_gap is None


def test_numeric_contexts_allow_interpolation_but_ordered_labels_alone_do_not() -> None:
    margins = {"A": -1.0, "B": 1.0}
    without = crossing_bracket("m", ("A", "B"), margins)
    assert without.numeric_critical_context is None

    with_numeric = crossing_bracket(
        "m",
        ("A", "B"),
        margins,
        context_values={"A": 10.0, "B": 14.0},
    )
    assert math.isclose(with_numeric.numeric_critical_context, 12.0)


def test_separated_brackets_are_parallel_definition_brackets() -> None:
    result = analyze_definitions(
        ("A", "B", "C", "D"),
        {
            "one": {"A": -1.0, "B": 1.0, "C": 2.0, "D": 3.0},
            "two": {"A": -3.0, "B": -2.0, "C": -1.0, "D": 1.0},
        },
    )
    assert result.classification == "PARALLEL_DEFINITION_BRACKETS"
    assert result.common_contexts == ()


def test_overlapping_nonidentical_brackets_are_reported_without_forcing_equality() -> None:
    first = crossing_bracket(
        "one", ("A", "B", "C"), {"A": -1.0, "B": 0.0, "C": 1.0}
    )
    second = crossing_bracket(
        "two", ("A", "B", "C"), {"A": -1.0, "B": -0.5, "C": 1.0}
    )
    from trait_architecture.critical_definition_concordance import compare_definition_brackets

    result = compare_definition_brackets((first, second), ("A", "B", "C"))
    assert result.classification == "OVERLAPPING_CRITICAL_BRACKETS"
    assert result.common_contexts == ("B",)


def test_numeric_tolerance_can_distinguish_same_from_parallel_numeric_contexts() -> None:
    contexts = ("A", "B")
    result = analyze_definitions(
        contexts,
        {
            "one": {"A": -1.0, "B": 1.0},
            "two": {"A": -3.0, "B": 1.0},
        },
        context_values={"A": 0.0, "B": 4.0},
        numeric_tolerance=0.5,
    )
    assert result.classification == "PARALLEL_NUMERIC_CRITICAL_CONTEXTS"
    assert math.isclose(result.brackets[0].numeric_critical_context, 2.0)
    assert math.isclose(result.brackets[1].numeric_critical_context, 3.0)


def test_multiple_crossings_fail_closed() -> None:
    with pytest.raises(ValueError, match="multiple zero crossings"):
        crossing_bracket(
            "oscillating",
            ("A", "B", "C", "D"),
            {"A": -1.0, "B": 1.0, "C": -1.0, "D": 1.0},
        )


def test_no_crossing_fails_closed() -> None:
    with pytest.raises(ValueError, match="no zero crossing"):
        crossing_bracket(
            "always_positive",
            ("A", "B", "C"),
            {"A": 1.0, "B": 2.0, "C": 3.0},
        )
