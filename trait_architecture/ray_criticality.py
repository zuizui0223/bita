from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class RayCriticalityResult:
    classification: str
    crossing_lower: float | None
    crossing_upper: float | None
    monotone_ok: bool
    convex_ok: bool
    slopes: tuple[float, ...]


def analyze_decoupling_ray(
    levels: Sequence[float],
    margins: Sequence[float],
    *,
    tolerance: float = 1e-12,
) -> RayCriticalityResult:
    """Audit sampled margins from a fixed BITA decoupling ray.

    The registered static ray model requires margins to be non-decreasing and
    consecutive secant slopes to be non-decreasing. A threshold bracket is
    returned only after these shape checks pass.
    """

    t = tuple(float(x) for x in levels)
    m = tuple(float(x) for x in margins)
    if len(t) != len(m) or len(t) < 2:
        raise ValueError("levels and margins must have the same length >= 2")
    if tolerance < 0:
        raise ValueError("tolerance must be nonnegative")
    if any(t[i + 1] <= t[i] for i in range(len(t) - 1)):
        raise ValueError("levels must be strictly increasing")

    monotone_ok = all(m[i + 1] + tolerance >= m[i] for i in range(len(m) - 1))
    slopes = tuple(
        (m[i + 1] - m[i]) / (t[i + 1] - t[i])
        for i in range(len(t) - 1)
    )
    convex_ok = all(
        slopes[i + 1] + tolerance >= slopes[i]
        for i in range(len(slopes) - 1)
    )

    if not monotone_ok or not convex_ok:
        return RayCriticalityResult(
            classification="RAY_MODEL_VIOLATION",
            crossing_lower=None,
            crossing_upper=None,
            monotone_ok=monotone_ok,
            convex_ok=convex_ok,
            slopes=slopes,
        )

    negative = [i for i, value in enumerate(m) if value < -tolerance]
    positive = [i for i, value in enumerate(m) if value > tolerance]
    zero = [i for i, value in enumerate(m) if abs(value) <= tolerance]

    if negative and positive:
        i_neg = max(negative)
        i_pos = min(positive)
        if i_neg >= i_pos:
            return RayCriticalityResult(
                classification="RAY_MODEL_VIOLATION",
                crossing_lower=None,
                crossing_upper=None,
                monotone_ok=False,
                convex_ok=convex_ok,
                slopes=slopes,
            )
        if zero:
            # Under exact convexity, a sampled zero between negative and positive
            # is a contact point; an extended interior zero plateau would force
            # a decreasing secant slope and would already fail the convex audit.
            return RayCriticalityResult(
                classification="EXACT_ZERO_OBSERVED",
                crossing_lower=t[min(zero)],
                crossing_upper=t[max(zero)],
                monotone_ok=True,
                convex_ok=True,
                slopes=slopes,
            )
        return RayCriticalityResult(
            classification="UNIQUE_CROSSING_BRACKET",
            crossing_lower=t[i_neg],
            crossing_upper=t[i_pos],
            monotone_ok=True,
            convex_ok=True,
            slopes=slopes,
        )

    if zero:
        return RayCriticalityResult(
            classification="ZERO_PLATEAU_WITHOUT_BOTH_SIDES",
            crossing_lower=t[min(zero)],
            crossing_upper=t[max(zero)],
            monotone_ok=True,
            convex_ok=True,
            slopes=slopes,
        )

    if all(value < -tolerance for value in m):
        classification = "NO_CROSSING_SHARED_SIDE_IN_RANGE"
    elif all(value > tolerance for value in m):
        classification = "BITA_SIDE_THROUGH_RANGE"
    else:
        classification = "NO_IDENTIFIED_CROSSING"

    return RayCriticalityResult(
        classification=classification,
        crossing_lower=None,
        crossing_upper=None,
        monotone_ok=True,
        convex_ok=True,
        slopes=slopes,
    )
