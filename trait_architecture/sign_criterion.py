"""Local sign criterion for a mechanistically oriented attraction--defence model.

The arithmetic implemented here is used after ecological channels have been derived
from an explicit model such as

    W(A, D) = P B(A) Q(D) - H F(A) S(D) - C(A, D).

In the oriented region B' >= 0, Q' <= 0, F' >= 0, and S' <= 0, define

    antagonist_relief      = -H F'(A) S'(D),
    mutualist_interference = -P B'(A) Q'(D),
    joint_cost             = C_AD.

The mixed partial is then antagonist relief minus mutualist interference minus
joint cost. The class does not turn an arbitrary fitness decomposition into a new
theorem; callers are responsible for establishing the mechanistic mapping and
local derivative signs before supplying non-negative channel magnitudes.

A positive mixed partial means local fitness complementarity and a negative mixed
partial local fitness substitutability. Neither sign alone predicts population-
level trait covariance, genetic correlation, or an evolutionary endpoint.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SignCriterion:
    """Evaluate oriented channel magnitudes for the local A x D mixed partial.

    ``antagonist_relief`` is the non-negative magnitude ``-H F' S'`` when
    attraction increases antagonist exposure and defence reduces residual damage.

    ``mutualist_interference`` is the non-negative magnitude ``-P B' Q'`` when
    attraction increases mutualist return and defence/access limitation reduces the
    retained return.

    ``joint_cost`` is ``C_AD`` when the local direct cross-cost is non-negative.

    If those derivative signs do not hold, the affected channel must be reoriented
    rather than forced into these labels.
    """

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
        """Return the local A x D mixed partial for the oriented model region."""

        return self.antagonist_relief - self.mutualist_interference - self.joint_cost

    def classify(self, *, tolerance: float = 1e-12) -> str:
        """Classify the local fitness interaction without implying trait covariance."""

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
        """Return antagonist relief required for a zero mixed partial."""

        return self.mutualist_interference + self.joint_cost