"""Identification of a critical point across shared and differentiated worlds.

Within-world response shapes are invariant to additive fitness offsets. Therefore,
if the shared and differentiated worlds are observed in disconnected experiments,
the relative offset between their fitness scales can move the cross-world zero
of W_D - W_S without changing any within-world contrasts. A bridge/comparator is
required to fix that offset before a common architecture critical context is
identified.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from .critical_context import ZeroCrossing, zero_crossing


def _finite(value: float, name: str) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


@dataclass(frozen=True)
class OffsetSensitivity:
    offset: float
    crossing: ZeroCrossing


def add_offset(points: list[tuple[float, float]], offset: float) -> list[tuple[float, float]]:
    offset = _finite(offset, "offset")
    return [(float(context), float(margin) + offset) for context, margin in points]


def within_world_differences(points: list[tuple[float, float]]) -> list[float]:
    ordered = sorted((float(x), float(y)) for x, y in points)
    return [ordered[i + 1][1] - ordered[i][1] for i in range(len(ordered) - 1)]


def offset_sensitivity(
    margin_points: list[tuple[float, float]],
    offsets: list[float],
    zero_tolerance: float = 1e-12,
) -> list[OffsetSensitivity]:
    if not offsets:
        raise ValueError("at least one offset is required")
    out: list[OffsetSensitivity] = []
    for offset in offsets:
        shifted = add_offset(margin_points, offset)
        crossing = zero_crossing(shifted, zero_tolerance=zero_tolerance)
        out.append(OffsetSensitivity(offset=float(offset), crossing=crossing))
    return out


def cross_world_identification_status(
    same_units_randomized_architecture: bool,
    validated_common_fitness_scale: bool,
    relative_offset_independently_estimated: bool,
) -> str:
    """Return whether the between-world fitness offset is identified.

    A randomized within-unit/within-block architecture comparison identifies the
    cross-world contrast directly when the endpoint is common. Otherwise an
    independently estimated relative offset plus a validated common scale is
    required.
    """

    if same_units_randomized_architecture and validated_common_fitness_scale:
        return "CROSS_WORLD_OFFSET_IDENTIFIED_DIRECTLY"
    if validated_common_fitness_scale and relative_offset_independently_estimated:
        return "CROSS_WORLD_OFFSET_IDENTIFIED_BY_BRIDGE"
    return "CROSS_WORLD_OFFSET_NOT_IDENTIFIED"
