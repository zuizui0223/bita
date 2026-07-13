"""General local sign criterion for attraction--defence interaction.

The module separates the theorem-level decomposition from any particular response
function used by the numerical robustness sweep.  It evaluates the mixed partial
of a broad local fitness decomposition

    W(A, D) = M(A, D) - G(A, D) - C(A, D),

where ``M`` is the mutualist-mediated contribution, ``G`` is antagonist-mediated
loss, and ``C`` is direct investment or allocation cost.

A positive mixed partial means *local fitness complementarity*: increasing D raises
the marginal fitness return to A.  A negative mixed partial means *local fitness
substitutability*.  Neither sign is, by itself, a prediction of population-level
trait covariance, genetic correlation, or an evolutionary endpoint.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SignCriterion:
    """Channel decomposition of the local A x D mixed partial.

    Parameters are signed contributions to ``d2W / dA dD`` after biological
    orientation has been declared:

    ``antagonist_relief``
        Positive when attraction increases antagonist exposure and defence reduces
        the resulting damage, so defence raises the marginal return to attraction.

    ``mutualist_interference``
        Non-negative magnitude of the opposing pathway in which defence reduces
        the mutualist-mediated return to attraction.

    ``joint_cost``
        Non-negative magnitude of a direct A x D allocation or construction cost.
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
        """Return the local A x D mixed partial."""

        return self.antagonist_relief - self.mutualist_interference - self.joint_cost

    def classify(self, *, tolerance: float = 1e-12) -> str:
        """Classify the local score interaction without implying trait covariance."""

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
        """Return the antagonist-relief magnitude required for a zero mixed partial."""

        return self.mutualist_interference + self.joint_cost
