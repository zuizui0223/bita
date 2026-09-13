"""Estimate and compare critical contexts from two chapter-specific margins.

This module does not decide how SCH or BITA margins are constructed. It accepts
predeclared scalar control contexts and chapter-specific signed margins, locates
zero crossings by deterministic linear interpolation, and compares whether the
two chapters are compatible with one critical context or require separated
("parallel-world") crossings.

Positive/negative sign orientation must be frozen before use:
- SCH projected architecture margin: positive means differentiated world would
  be favoured if available.
- BITA architecture margin: positive means differentiated architecture favoured.
Raw SCH state-optimum separation and raw BITA R_state should not be mixed here
unless they have first been mapped to the same declared margin meaning.
"""

from __future__ import annotations

from dataclasses import dataclass
import math


def _finite(value: float, name: str) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


@dataclass(frozen=True)
class ZeroCrossing:
    context: float
    left_context: float
    right_context: float
    left_margin: float
    right_margin: float
    exact_grid_hit: bool


@dataclass(frozen=True)
class CriticalContextComparison:
    sch_crossing: ZeroCrossing
    bita_crossing: ZeroCrossing
    delta_context: float
    absolute_delta_context: float
    tolerance: float
    classification: str


def _clean_points(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    if len(points) < 2:
        raise ValueError("at least two context-margin points are required")
    cleaned = [(_finite(x, "context"), _finite(y, "margin")) for x, y in points]
    cleaned.sort(key=lambda item: item[0])
    xs = [x for x, _ in cleaned]
    if len(set(xs)) != len(xs):
        raise ValueError("context values must be unique")
    return cleaned


def zero_crossing(points: list[tuple[float, float]], zero_tolerance: float = 1e-12) -> ZeroCrossing:
    """Locate the first signed zero crossing along increasing context.

    ``zero_tolerance`` is a dimensionless numerical tolerance relative to the
    largest supplied margin magnitude. Exact/near-zero grid points are preferred.
    Otherwise adjacent points must have opposite signs and the crossing is
    linearly interpolated. Multiple crossings are rejected because a single
    critical context is not identified without an additional branch-selection
    rule.
    """

    zero_tolerance = abs(_finite(zero_tolerance, "zero_tolerance"))
    values = _clean_points(points)
    margin_scale = max(abs(y) for _, y in values)

    def near_zero(y: float) -> bool:
        if margin_scale == 0.0:
            return y == 0.0
        return abs(y) <= zero_tolerance * margin_scale

    crossings: list[ZeroCrossing] = []
    for x, y in values:
        if near_zero(y):
            crossings.append(
                ZeroCrossing(
                    context=x,
                    left_context=x,
                    right_context=x,
                    left_margin=y,
                    right_margin=y,
                    exact_grid_hit=True,
                )
            )

    for (x0, y0), (x1, y1) in zip(values, values[1:]):
        if near_zero(y0) or near_zero(y1):
            continue
        opposite_signs = (y0 < 0.0 < y1) or (y1 < 0.0 < y0)
        if opposite_signs:
            pair_scale = max(abs(y0), abs(y1))
            y0_scaled = y0 / pair_scale
            y1_scaled = y1 / pair_scale
            fraction = -y0_scaled / (y1_scaled - y0_scaled)
            xcrit = (1.0 - fraction) * x0 + fraction * x1
            crossings.append(
                ZeroCrossing(
                    context=xcrit,
                    left_context=x0,
                    right_context=x1,
                    left_margin=y0,
                    right_margin=y1,
                    exact_grid_hit=False,
                )
            )

    if not crossings:
        raise ValueError("no zero crossing is bracketed by the supplied contexts")
    if len(crossings) > 1:
        raise ValueError("multiple zero crossings found; one critical context is not uniquely identified")
    return crossings[0]


def compare_critical_contexts(
    sch_points: list[tuple[float, float]],
    bita_points: list[tuple[float, float]],
    context_tolerance: float,
    zero_tolerance: float = 1e-12,
) -> CriticalContextComparison:
    context_tolerance = abs(_finite(context_tolerance, "context_tolerance"))
    sch = zero_crossing(sch_points, zero_tolerance=zero_tolerance)
    bita = zero_crossing(bita_points, zero_tolerance=zero_tolerance)
    delta = bita.context - sch.context
    absolute = abs(delta)
    if absolute <= context_tolerance:
        classification = "SAME_CRITICAL_CONTEXT_COMPATIBLE"
    else:
        classification = "PARALLEL_WORLD_CRITICAL_CONTEXTS"
    return CriticalContextComparison(
        sch_crossing=sch,
        bita_crossing=bita,
        delta_context=delta,
        absolute_delta_context=absolute,
        tolerance=context_tolerance,
        classification=classification,
    )
