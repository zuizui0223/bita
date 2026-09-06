from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CurvatureDividend:
    total_gain: float
    tangent_gain: float
    curvature_dividend: float
    curvature_share: float


def decompose_decoupling_gain(
    *,
    total_gain: float,
    tangent_gain: float,
    tolerance: float = 1e-12,
) -> CurvatureDividend:
    """Decompose finite recoverable-fitness gain into tangent + curvature terms.

    Under the registered convex BITA coupling model, ``total_gain`` must be at
    least ``tangent_gain``.  A larger shortfall than ``tolerance`` fails closed.
    """

    if total_gain < -tolerance:
        raise ValueError("total_gain must be nonnegative for the registered decoupling move")
    if tangent_gain < -tolerance:
        raise ValueError("tangent_gain must be nonnegative for the registered decoupling move")
    if total_gain + tolerance < tangent_gain:
        raise ValueError("observed gain violates the convex tangent lower bound")

    total = max(0.0, total_gain)
    tangent = max(0.0, tangent_gain)
    dividend = max(0.0, total - tangent)
    share = 0.0 if total == 0.0 else dividend / total
    return CurvatureDividend(
        total_gain=total,
        tangent_gain=tangent,
        curvature_dividend=dividend,
        curvature_share=share,
    )


def static_crossing_surplus(*, deficit: float, total_gain: float) -> float:
    """Post-intervention static architecture margin contributed by recovery.

    ``deficit = K - R(lambda_0)`` is positive on the shared-favored side.
    A positive return value means the finite recovery is large enough to cross
    the static architecture boundary when K is fixed.
    """

    if deficit < 0:
        raise ValueError("deficit must be nonnegative")
    return total_gain - deficit
