"""Local sign criteria for mechanistically oriented attraction--defence models.

The arithmetic here is used only after ecological channels have been derived from
an explicit model. ``SignCriterion`` evaluates already-oriented channel
magnitudes. ``RegimeScaledCriterion`` is the linear special case in which
mutualist service and antagonist pressure scale fixed local channel sensitivities.
``MonotoneRegimeCriterion`` records the more general local comparative statics for
nonlinear regime scalings.

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
    """Linear special case with testable local comparative statics.

    The model is

        W_AD = H * relief_rate - P * interference_rate - joint_cost.

    The resulting directional predictions are conditional on the rates, joint cost,
    and local phenotype neighbourhood remaining comparable while P or H changes.
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


@dataclass(frozen=True)
class MonotoneRegimeCriterion:
    """Local nonlinear regime scaling and its directional derivatives.

    Around a focal environment, write

        W_AD = a(H) * relief_rate
             - b(P) * interference_rate
             - joint_cost(P, H).

    ``antagonist_scale`` and ``mutualist_scale`` are the local values of ``a(H)``
    and ``b(P)``. Their slopes are the local derivatives ``a'(H)`` and ``b'(P)``.
    ``joint_cost_h_slope`` and ``joint_cost_p_slope`` allow the direct cross-cost to
    vary with the two regime variables.

    The local comparative statics are therefore

        dW_AD/dH = a'(H) * relief_rate - dC_AD/dH
        dW_AD/dP = -b'(P) * interference_rate - dC_AD/dP.

    This class deliberately does not require the scale slopes to be positive. The
    signs of the returned derivatives are the actual local predictions.
    """

    antagonist_scale: float
    mutualist_scale: float
    antagonist_scale_slope: float
    mutualist_scale_slope: float
    relief_rate: float
    interference_rate: float
    joint_cost: float
    joint_cost_h_slope: float = 0.0
    joint_cost_p_slope: float = 0.0

    def __post_init__(self) -> None:
        for name in (
            "antagonist_scale",
            "mutualist_scale",
            "relief_rate",
            "interference_rate",
            "joint_cost",
        ):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be non-negative")

    @property
    def mixed_partial(self) -> float:
        return (
            self.antagonist_scale * self.relief_rate
            - self.mutualist_scale * self.interference_rate
            - self.joint_cost
        )

    @property
    def d_mixed_partial_d_antagonist_pressure(self) -> float:
        return (
            self.antagonist_scale_slope * self.relief_rate
            - self.joint_cost_h_slope
        )

    @property
    def d_mixed_partial_d_pollinator_service(self) -> float:
        return (
            -self.mutualist_scale_slope * self.interference_rate
            - self.joint_cost_p_slope
        )
