import pytest

from trait_architecture.dimensional_release import (
    evaluate_dimensional_release,
    evaluate_sch_handoff_release,
)


def test_state_specific_release_is_distance_to_zp_not_axd_interaction() -> None:
    result = evaluate_dimensional_release(
        reference=1.0,
        x_opt_before=0.2,
        x_opt_after=0.7,
        reference_kind="state_specific",
    )
    assert result.distance_before == pytest.approx(0.8)
    assert result.distance_after == pytest.approx(0.3)
    assert result.release_amount == pytest.approx(0.5)
    assert result.moves_toward_reference is True
    assert result.status == "STATE_SPECIFIC_RELEASE"


def test_moving_away_from_reference_fails_release() -> None:
    result = evaluate_dimensional_release(
        reference=1.0,
        x_opt_before=0.6,
        x_opt_after=0.1,
    )
    assert result.release_amount < 0.0
    assert result.moves_toward_reference is False
    assert result.status == "NO_DIMENSIONAL_RELEASE"


def test_biological_release_threshold_is_fail_closed() -> None:
    result = evaluate_dimensional_release(
        reference=1.0,
        x_opt_before=0.5,
        x_opt_after=0.6,
        min_release=0.15,
    )
    assert result.release_amount == pytest.approx(0.1)
    assert result.moves_toward_reference is False


def test_reference_release_and_fitness_gain_are_separate_claims() -> None:
    result = evaluate_dimensional_release(
        reference=1.0,
        x_opt_before=0.3,
        x_opt_after=0.8,
        fitness_before=0.50,
        fitness_after=0.62,
        min_release=0.1,
        min_fitness_gain=0.05,
    )
    assert result.moves_toward_reference is True
    assert result.fitness_improves is True
    assert result.fitness_gain == pytest.approx(0.12)
    assert result.status == "STATE_SPECIFIC_RELEASE_WITH_FITNESS_GAIN"


def test_fitness_gain_without_reference_release_is_not_dimensional_release() -> None:
    result = evaluate_dimensional_release(
        reference=1.0,
        x_opt_before=0.8,
        x_opt_after=0.5,
        fitness_before=0.50,
        fitness_after=0.70,
    )
    assert result.moves_toward_reference is False
    assert result.fitness_improves is True
    assert result.status == "FITNESS_GAIN_WITHOUT_REFERENCE_RELEASE"


def test_state_specific_and_pure_function_lanes_are_reported_separately() -> None:
    paired = evaluate_sch_handoff_release(
        z_p=0.8,
        z_f1=1.0,
        x_opt_before=0.2,
        x_opt_after=0.7,
    )
    assert paired.state_specific.reference_kind == "state_specific"
    assert paired.pure_function is not None
    assert paired.pure_function.reference_kind == "pure_function"
    assert paired.state_specific.release_amount != paired.pure_function.release_amount


def test_pure_function_lane_is_absent_without_stronger_sch_reference() -> None:
    paired = evaluate_sch_handoff_release(
        z_p=0.8,
        x_opt_before=0.2,
        x_opt_after=0.7,
    )
    assert paired.state_specific.moves_toward_reference is True
    assert paired.pure_function is None


def test_fitness_inputs_must_be_paired() -> None:
    with pytest.raises(ValueError, match="supplied together"):
        evaluate_dimensional_release(
            reference=1.0,
            x_opt_before=0.2,
            x_opt_after=0.7,
            fitness_before=0.5,
        )


def test_invalid_reference_kind_fails_closed() -> None:
    with pytest.raises(ValueError, match="reference_kind"):
        evaluate_dimensional_release(
            reference=1.0,
            x_opt_before=0.2,
            x_opt_after=0.7,
            reference_kind="invented",  # type: ignore[arg-type]
        )
