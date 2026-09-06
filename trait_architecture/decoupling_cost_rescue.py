from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CostRescueBracket:
    necessary_cost_relief: float
    sufficient_cost_relief: float
    deficit: float
    lower_full_gain: float
    upper_full_gain: float

    @property
    def decoupling_alone_guaranteed(self) -> bool:
        return self.sufficient_cost_relief == 0.0

    @property
    def positive_cost_relief_necessary(self) -> bool:
        return self.necessary_cost_relief > 0.0


def cost_rescue_bracket(
    *,
    deficit: float,
    lower_full_gain: float,
    upper_full_gain: float,
) -> CostRescueBracket:
    if deficit <= 0:
        raise ValueError("deficit must be positive")
    if lower_full_gain < 0 or upper_full_gain < 0:
        raise ValueError("full-decoupling gain bounds must be nonnegative")
    if lower_full_gain > upper_full_gain:
        raise ValueError("lower_full_gain cannot exceed upper_full_gain")

    necessary = max(0.0, deficit - upper_full_gain)
    sufficient = max(0.0, deficit - lower_full_gain)
    return CostRescueBracket(
        necessary_cost_relief=necessary,
        sufficient_cost_relief=sufficient,
        deficit=deficit,
        lower_full_gain=lower_full_gain,
        upper_full_gain=upper_full_gain,
    )
