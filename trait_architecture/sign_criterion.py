"""Local mixed-curvature criteria for a declared pair of floral traits.

The focal variables are one attraction trait ``A`` and one flower-specific
barrier/defence trait ``D`` on one declared outcome scale ``W``. The classes
below evaluate local bookkeeping after the biological channels, trait/output
parameterisation, and required orientation signs have been specified.

``OrientedSignCriterion`` evaluates already-oriented non-negative channel
magnitudes. ``RegimeDerivativeBalance`` is the general local derivative balance
for environmental change after those channels have been defined.
``RegimeScaledCriterion`` and ``SeparableLocalRegimeCriterion`` are restricted
special cases that impose separable regime scaling.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


def _require_nonnegative_finite(value: float, name: str) -> None:
    if not isfinite(value) or value < 0:
        raise ValueError(f"{name} must be finite and non-negative")


def _require_finite(value: float, name: str) -> None:
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")


@dataclass(frozen=True)
class OrientedSignCriterion:
    """Evaluate already-oriented magnitudes for the local ``A x D`` mixed partial.

    ``joint_cost_curvature`` is the non-negative contribution ``C_AD`` to the
    mixed partial. It is not the total cost function ``C(A,D)`` or a total
    energetic cost. The three channel magnitudes are not identifiable from total
    ``W`` alone unless the channel decomposition is independently specified.
    """

    antagonist_relief: float
    mutualist_interference: float
    joint_cost_curvature: float

    def __post_init__(self) -> None:
        for name, value in (
            ("antagonist_relief", self.antagonist_relief),
            ("mutualist_interference", self.mutualist_interference),
            ("joint_cost_curvature", self.joint_cost_curvature),
        ):
            _require_nonnegative_finite(value, name)

    @property
    def mixed_partial(self) -> float:
        return self.antagonist_relief - self.mutualist_interference - self.joint_cost_curvature

    def classify(self, *, tolerance: float = 1e-12) -> str:
        if not isfinite(tolerance) or tolerance < 0:
            raise ValueError("tolerance must be finite and non-negative")
        value = self.mixed_partial
        if value > tolerance:
            return "locally_complementary"
        if value < -tolerance:
            return "locally_substitutable"
        return "locally_neutral"

    @property
    def break_even_antagonist_relief(self) -> float:
        return self.mutualist_interference + self.joint_cost_curvature


@dataclass(frozen=True)
class RegimeDerivativeBalance:
    """General local environmental derivative balance for the oriented channels.

    If

        W_AD = R(P,H) - I(P,H) - C_AD(P,H),

    then, at the same focal phenotype and outcome scale,

        dW_AD/dH = R_H - I_H - C_AD,H
        dW_AD/dP = R_P - I_P - C_AD,P.

    All supplied slopes are signed local derivatives. No separability assumption
    is imposed: antagonist pressure may change mutualist interference, and
    pollinator service may change antagonist relief.
    """

    relief_h_slope: float
    interference_h_slope: float
    joint_cost_curvature_h_slope: float
    relief_p_slope: float
    interference_p_slope: float
    joint_cost_curvature_p_slope: float

    def __post_init__(self) -> None:
        for name, value in self.__dict__.items():
            _require_finite(value, name)

    @property
    def d_mixed_partial_d_antagonist_pressure(self) -> float:
        return (
            self.relief_h_slope
            - self.interference_h_slope
            - self.joint_cost_curvature_h_slope
        )

    @property
    def d_mixed_partial_d_pollinator_service(self) -> float:
        return (
            self.relief_p_slope
            - self.interference_p_slope
            - self.joint_cost_curvature_p_slope
        )


@dataclass(frozen=True)
class RegimeScaledCriterion:
    """Linear separable oriented special case.

    ``P`` and ``H`` are exogenous reference-regime indices. At fixed focal ``A``
    and ``D`` and fixed local rates,

        W_AD = H * relief_rate
             - P * interference_rate
             - joint_cost_curvature.

    This special case assumes no H-dependence of mutualist interference, no
    P-dependence of antagonist relief, and regime-invariant cross-cost curvature.
    """

    pollinator_service: float
    antagonist_pressure: float
    relief_rate: float
    interference_rate: float
    joint_cost_curvature: float

    def __post_init__(self) -> None:
        for name, value in self.__dict__.items():
            _require_nonnegative_finite(value, name)

    @property
    def antagonist_relief(self) -> float:
        return self.antagonist_pressure * self.relief_rate

    @property
    def mutualist_interference(self) -> float:
        return self.pollinator_service * self.interference_rate

    @property
    def mixed_partial(self) -> float:
        return self.antagonist_relief - self.mutualist_interference - self.joint_cost_curvature

    @property
    def derivative_balance(self) -> RegimeDerivativeBalance:
        return RegimeDerivativeBalance(
            relief_h_slope=self.relief_rate,
            interference_h_slope=0.0,
            joint_cost_curvature_h_slope=0.0,
            relief_p_slope=0.0,
            interference_p_slope=self.interference_rate,
            joint_cost_curvature_p_slope=0.0,
        )

    @property
    def d_mixed_partial_d_antagonist_pressure(self) -> float:
        return self.derivative_balance.d_mixed_partial_d_antagonist_pressure

    @property
    def d_mixed_partial_d_pollinator_service(self) -> float:
        return self.derivative_balance.d_mixed_partial_d_pollinator_service

    @property
    def break_even_antagonist_pressure(self) -> float | None:
        """Return the unique finite linear threshold, or ``None`` if none exists."""

        if self.relief_rate == 0:
            return None
        return (
            self.pollinator_service * self.interference_rate
            + self.joint_cost_curvature
        ) / self.relief_rate


@dataclass(frozen=True)
class SeparableLocalRegimeCriterion:
    """Nonlinear but separable local regime-scaling special case.

    Around a focal environment and fixed focal phenotype,

        W_AD = a(H) * relief_rate
             - b(P) * interference_rate
             - joint_cost_curvature(P,H).

    This representation still imposes ``dI/dH = 0`` and ``dR/dP = 0``. It is
    therefore more flexible than the linear special case but less general than
    :class:`RegimeDerivativeBalance`.
    """

    antagonist_scale: float
    mutualist_scale: float
    antagonist_scale_slope: float
    mutualist_scale_slope: float
    relief_rate: float
    interference_rate: float
    joint_cost_curvature: float
    joint_cost_curvature_h_slope: float = 0.0
    joint_cost_curvature_p_slope: float = 0.0

    def __post_init__(self) -> None:
        for name in (
            "antagonist_scale",
            "mutualist_scale",
            "relief_rate",
            "interference_rate",
            "joint_cost_curvature",
        ):
            _require_nonnegative_finite(getattr(self, name), name)
        for name in (
            "antagonist_scale_slope",
            "mutualist_scale_slope",
            "joint_cost_curvature_h_slope",
            "joint_cost_curvature_p_slope",
        ):
            _require_finite(getattr(self, name), name)

    @property
    def mixed_partial(self) -> float:
        return (
            self.antagonist_scale * self.relief_rate
            - self.mutualist_scale * self.interference_rate
            - self.joint_cost_curvature
        )

    @property
    def derivative_balance(self) -> RegimeDerivativeBalance:
        return RegimeDerivativeBalance(
            relief_h_slope=self.antagonist_scale_slope * self.relief_rate,
            interference_h_slope=0.0,
            joint_cost_curvature_h_slope=self.joint_cost_curvature_h_slope,
            relief_p_slope=0.0,
            interference_p_slope=self.mutualist_scale_slope * self.interference_rate,
            joint_cost_curvature_p_slope=self.joint_cost_curvature_p_slope,
        )

    @property
    def d_mixed_partial_d_antagonist_pressure(self) -> float:
        return self.derivative_balance.d_mixed_partial_d_antagonist_pressure

    @property
    def d_mixed_partial_d_pollinator_service(self) -> float:
        return self.derivative_balance.d_mixed_partial_d_pollinator_service
