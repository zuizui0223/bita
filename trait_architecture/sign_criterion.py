"""Local sign criteria for mechanistically oriented attraction--defence models.

The arithmetic here is used only after ecological channels have been derived from
an explicit model. ``SignCriterion`` evaluates already-oriented channel
magnitudes. ``RegimeScaledCriterion`` adds a stronger, predictive restriction:
mutualist service and antagonist pressure scale fixed local channel sensitivities.

Under that restriction,

    W_AD = H * relief_rate - P * interference_rate - joint_cost,

so increasing antagonist pressure pushes the local interaction toward
complementarity, while increasing mutualist service pushes it toward
substitutability. These comparative statics are conditional predictions, unlike
the bare arithmetic decomposition.

Neither class by itself predicts population-level trait covariance, genetic
correlation, or an evolutionary endpoint.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SignCriterion:
    """Evaluate oriented channel magnitudes for the local A x D mixed partial."""

    antagonist_relief: float
    mutualist_interference: float
    joint_cost: float

    def __post_init__(self) -> None:
        for name, value in (
            ("antagonist_relief", self.antagonist_relief),
            ("mutualist_interference", self.mutualist_interference),
            ("joint_cost", self.joint_cost),
        ):
            if value < 0:
                raise ValueError(f"{name} must be non-negative after orientation")

    @property
    def mixed_partial(self) -> float:
        return self.antagonist_relief - self.mutualist_interference - self.joint_cost

    def classify(self, *, tolerance: float = 1e-12) -> str:
        if tolerance < 0:
            raise ValueError("tolerance must be non-negative")
        value = self.mixed_partial
        if value > tolerance:
            return "locally_complementary"
        if value < -tolerance:
            return "locally_substitutable"
        return "locally_neutral"

    @property
    def break_even_antagonist_relief(self) -> float:
        return self.mutualist_interference + self.joint_cost


@dataclass(frozen=True)
class RegimeScaledCriterion:
    """Evaluate a regime-scaled local criterion with testable comparative statics.

    ``relief_rate`` is antagonist-relief curvature per unit antagonist pressure H.
    ``interference_rate`` is mutualist-interference curvature per unit mutualist
    service P. Both are non-negative local sensitivities after biological
    orientation. ``joint_cost`` is a non-negative direct cross-cost.

    The model is

        W_AD = H * relief_rate - P * interference_rate - joint_cost.

    The resulting directional predictions are conditional on the rates and local
    phenotype neighbourhood remaining comparable while P or H changes.
    """

    pollinator_service: float
    antagonist_pressure: float
    relief_rate: float
    interference_rate: float
    joint_cost: float

    def __post_init__(self) -> None:
        for name, value in self.__dict__.items():
            if value < 0:
                raise ValueError(f"{name} must be non-negative")

    @property
    def antagonist_relief(self) -> float:
        return self.antagonist_pressure * self.relief_rate

    @property
    def mutualist_interference(self) -> float:
        return self.pollinator_service * self.interference_rate

    @property
    def mixed_partial(self) -> float:
        return self.antagonist_relief - self.mutualist_interference - self.joint_cost

    @property
    def d_mixed_partial_d_antagonist_pressure(self) -> float:
        return self.relief_rate

    @property
    def d_mixed_partial_d_pollinator_service(self) -> float:
        return -self.interference_rate

    @property
    def break_even_antagonist_pressure(self) -> float:
        if self.relief_rate == 0:
            return float("inf")
        return (
            self.pollinator_service * self.interference_rate + self.joint_cost
        ) / self.relief_rate
