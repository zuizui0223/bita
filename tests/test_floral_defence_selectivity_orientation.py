from __future__ import annotations

import pytest

from trait_architecture.floral_defence_selectivity import (
    derive_defence_state,
    derive_pollinator_state,
    orient_effect,
)


def test_antagonist_use_effect_is_reoriented_so_suppression_is_positive() -> None:
    assert orient_effect("antagonist", -1.2, "higher_is_antagonist_use") == pytest.approx(1.2)


def test_pollinator_function_effect_keeps_positive_benefit_orientation() -> None:
    assert orient_effect("pollinator", 0.7, "higher_is_pollinator_function") == pytest.approx(0.7)


def test_incompatible_orientation_is_rejected() -> None:
    with pytest.raises(ValueError, match="incompatible"):
        orient_effect("antagonist", 0.2, "higher_is_pollinator_function")


def test_defence_state_requires_supported_suppression() -> None:
    assert derive_defence_state({
        "antagonist_effect_direction": "suppressed",
        "antagonist_uncertainty_class": "DIRECTION_SUPPORTED",
    }) == "EFFECTIVE"
    assert derive_defence_state({
        "antagonist_effect_direction": "no_detected_change",
        "antagonist_uncertainty_class": "NULL_COMPATIBLE",
    }) == "NULL_OR_WEAK"


def test_null_compatible_pollinator_result_stays_no_detected_change() -> None:
    assert derive_pollinator_state({
        "pollinator_effect_direction": "no_detected_change",
        "pollinator_uncertainty_class": "NULL_COMPATIBLE",
        "source_supported_preservation": "false",
    }) == "NO_DETECTED_CHANGE"


def test_supported_improvement_is_preserved_or_improved() -> None:
    assert derive_pollinator_state({
        "pollinator_effect_direction": "improved",
        "pollinator_uncertainty_class": "DIRECTION_SUPPORTED",
        "source_supported_preservation": "true",
    }) == "PRESERVED_OR_IMPROVED"
