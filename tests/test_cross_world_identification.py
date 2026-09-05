import math

from trait_architecture.cross_world_identification import (
    add_offset,
    cross_world_identification_status,
    offset_sensitivity,
    within_world_differences,
)


def test_additive_offset_preserves_within_world_differences_but_moves_critical_point() -> None:
    points = [(0.0, -1.0), (2.0, 1.0)]
    shifted = add_offset(points, 0.5)
    assert within_world_differences(points) == within_world_differences(shifted)

    results = offset_sensitivity(points, [0.0, 0.5])
    assert math.isclose(results[0].crossing.context, 1.0)
    assert math.isclose(results[1].crossing.context, 0.5)


def test_disconnected_worlds_do_not_identify_relative_offset() -> None:
    assert (
        cross_world_identification_status(
            same_units_randomized_architecture=False,
            validated_common_fitness_scale=True,
            relative_offset_independently_estimated=False,
        )
        == "CROSS_WORLD_OFFSET_NOT_IDENTIFIED"
    )


def test_randomized_common_endpoint_identifies_direct_cross_world_offset() -> None:
    assert (
        cross_world_identification_status(
            same_units_randomized_architecture=True,
            validated_common_fitness_scale=True,
            relative_offset_independently_estimated=False,
        )
        == "CROSS_WORLD_OFFSET_IDENTIFIED_DIRECTLY"
    )


def test_independent_bridge_can_identify_offset_without_direct_architecture_randomization() -> None:
    assert (
        cross_world_identification_status(
            same_units_randomized_architecture=False,
            validated_common_fitness_scale=True,
            relative_offset_independently_estimated=True,
        )
        == "CROSS_WORLD_OFFSET_IDENTIFIED_BY_BRIDGE"
    )
