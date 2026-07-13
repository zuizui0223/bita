"""Local mixed-curvature criteria for a declared pair of floral traits.

The focal variables are one attraction trait ``A`` and one flower-specific
barrier/defence trait ``D``. The classes below evaluate local mixed-partial
bookkeeping after the biological channels, trait parameterisation, and required
orientation signs have been specified. They do not turn broad trait categories
into a common quantitative axis and they do not predict population-level
covariance or evolutionary endpoints.

``OrientedSignCriterion`` evaluates already-oriented non-negative channel
magnitudes. ``RegimeScaledCriterion`` is the linear special case in which
exogenous regime indices scale fixed local channel sensitivities.
``LocalRegimeCriterion`` stores more general local regime scalings and their
local derivatives.
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
    energetic cost.
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
        return (
            self.antagonist_relief
            - self.mutualist_interference
            - self.joint_cost_curvature
        )

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
class RegimeScaledCriterion:
    """Linear oriented local special case with conditional comparative statics.

    ``P`` and ``H`` are exogenous reference-regime indices, not realised
    visitation or damage after the focal traits act. At fixed focal ``A`` and
    ``D`` and fixed local rates,

        W_AD = H * relief_rate
             - P * interference_rate
             - joint_cost_curvature.

    ``joint_cost_curvature`` is ``C_AD`` in the local mixed-partial expression,
    not total cost. The resulting directional statements are partial derivatives
    at the same phenotype neighbourhood; they are not derivatives along an
    optimum or an observed environmental trait cline.
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
        return (
            self.antagonist_relief
            - self.mutualist_interference
            - self.joint_cost_curvature
        )

    @property
    def d_mixed_partial_d_antagonist_pressure(self) -> float:
        return self.relief_rate

    @property
    def d_mixed_partial_d_pollinator_service(self) -> float:
        return -self.interference_rate

    @property
    def break_even_antagonist_pressure(self) -> float | None:
        """Return the unique finite linear threshold, or ``None`` if none exists.

        With zero relief rate the equation is independent of antagonist pressure:
        either no pressure can reach break-even or every pressure is neutral.
        Neither case has a unique finite threshold.
        """

        if self.relief_rate == 0:
            return None
        return (
            self.pollinator_service * self.interference_rate
            + self.joint_cost_curvature
        ) / self.relief_rate


@dataclass(frozen=True)
class LocalRegimeCriterion:
    """Oriented local nonlinear regime scaling and directional derivatives.

    Around a focal environment and fixed focal phenotype, write

        W_AD = a(H) * relief_rate
             - b(P) * interference_rate
             - joint_cost_curvature(P, H).

    ``antagonist_scale`` and ``mutualist_scale`` are the local values of
    ``a(H)`` and ``b(P)``. Their slopes are the local derivatives ``a'(H)`` and
    ``b'(P)``. ``joint_cost_curvature_*_slope`` terms are local derivatives of
    the cross-cost curvature ``C_AD`` with respect to the regime indices.

    Scale slopes are allowed to be negative because the returned derivatives,
    rather than the class name, determine the actual local prediction.
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
    def d_mixed_partial_d_antagonist_pressure(self) -> float:
        return (
            self.antagonist_scale_slope * self.relief_rate
            - self.joint_cost_curvature_h_slope
        )

    @property
    def d_mixed_partial_d_pollinator_service(self) -> float:
        return (
            -self.mutualist_scale_slope * self.interference_rate
            - self.joint_cost_curvature_p_slope
        )
