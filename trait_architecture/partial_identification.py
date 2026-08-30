"""Partial identification and outcome-claim classification for attraction–defence studies.

The canonical identification paper distinguishes the observed total two-level
interaction

    Delta_AD W = rho_delta - iota_delta - kappa_delta

from its channel allocation. Full crossed interventions can point-identify the
biotic channels under the declared gates, but incomplete studies need not be
classified only as "identified" or "not identified". When external knowledge
supplies bounds on one or more channels, the equality above defines an exact
identified set and corresponding projection intervals.

A separate distinction concerns the biological language attached to a positive
total interaction. Let

    A0 = W10 - W00   (effect of attraction when defence is low)
    A1 = W11 - W01   (effect of attraction when defence is high)

so that Delta_AD W = A1 - A0. A positive interaction shows that defence improves
the attraction effect. It does not, by itself, show that an otherwise
non-beneficial attraction effect became beneficial. The latter requires A0 <= 0
and A1 > 0; a strict negative-to-positive reversal requires A0 < 0 and A1 > 0.
The classifiers below preserve those three nested claim levels.

This module keeps all logic deliberately assumption-indexed. It never treats a
sign restriction, cost bound, consumer bound, or confidence interval as
empirical fact unless the caller supplies it.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import inf, isnan


@dataclass(frozen=True)
class Interval:
    """Closed interval on the extended real line."""

    low: float = -inf
    high: float = inf

    def __post_init__(self) -> None:
        if isnan(self.low) or isnan(self.high):
            raise ValueError("interval bounds cannot be NaN")
        if self.low > self.high:
            raise ValueError(f"invalid interval: low={self.low} > high={self.high}")
        if self.low == inf or self.high == -inf:
            raise ValueError("interval must contain at least one finite or extended-real value")

    @property
    def is_point(self) -> bool:
        return self.low == self.high

    def intersect(self, other: "Interval") -> "Interval | None":
        low = max(self.low, other.low)
        high = min(self.high, other.high)
        if low > high:
            return None
        return Interval(low, high)

    @property
    def sign_status(self) -> str:
        if self.low > 0:
            return "positive"
        if self.high < 0:
            return "negative"
        if self.low == 0 and self.high == 0:
            return "zero"
        if self.low == 0 and self.high > 0:
            return "nonnegative"
        if self.low < 0 and self.high == 0:
            return "nonpositive"
        return "sign_unresolved"


@dataclass(frozen=True)
class PartialIdentificationResult:
    """Projection of the feasible channel-allocation set.

    The full identified set is

        {(rho, iota, kappa): rho - iota - kappa = delta_w}

    intersected with the caller-supplied box constraints. ``rho``, ``iota`` and
    ``kappa`` are exact coordinate projections of that set, not independent
    uncertainty intervals from a sampling model. ``biotic_balance`` is the
    exact projection of rho - iota; because the equality implies
    rho - iota = delta_w + kappa, its bounds are determined one-to-one by the
    feasible kappa projection.
    """

    delta_w: float
    feasible: bool
    rho: Interval | None
    iota: Interval | None
    kappa: Interval | None
    biotic_balance: Interval | None

    @property
    def point_identified(self) -> bool:
        return bool(
            self.feasible
            and self.rho is not None
            and self.iota is not None
            and self.kappa is not None
            and self.rho.is_point
            and self.iota.is_point
            and self.kappa.is_point
        )


@dataclass(frozen=True)
class EscapeClaimHierarchy:
    """Three nested outcome claims for one declared A-by-D response surface.

    ``interaction_relief`` concerns only whether Delta_AD W is positive.
    ``constraint_release`` additionally asks whether attraction is non-beneficial
    without defence (A0 <= 0) but beneficial with defence (A1 > 0).
    ``strict_reversal`` requires the stronger negative-to-positive transition
    A0 < 0 < A1.

    The intervals are treated as already justified uncertainty sets. The class
    does not assume independence, derive a confidence region, or identify any
    ecological channel.
    """

    interaction_relief: str
    constraint_release: str
    strict_reversal: str


def classify_interaction_relief(delta_w_bounds: Interval) -> str:
    """Classify positive improvement of the attraction effect by defence.

    This is the sign of Delta_AD W = A1 - A0. A positive result is a necessary
    component of constraint release and strict reversal, but it is not by itself
    either stronger claim.
    """
    if delta_w_bounds.low > 0:
        return "POSITIVE_INTERACTION_RELIEF_IDENTIFIED"
    if delta_w_bounds.high <= 0:
        return "POSITIVE_INTERACTION_RELIEF_REFUTED"
    return "POSITIVE_INTERACTION_RELIEF_UNRESOLVED"


def classify_constraint_release(a0_bounds: Interval, a1_bounds: Interval) -> str:
    """Classify the transition A0 <= 0 and A1 > 0.

    ``IDENTIFIED`` requires both inequalities to hold over the supplied
    intervals. ``REFUTED`` means that no values in the intervals can satisfy the
    conjunction. All overlapping cases remain unresolved rather than being
    promoted from a positive interaction alone.
    """
    if a0_bounds.high <= 0 and a1_bounds.low > 0:
        return "CONSTRAINT_RELEASE_IDENTIFIED"
    if a0_bounds.low > 0 or a1_bounds.high <= 0:
        return "CONSTRAINT_RELEASE_REFUTED"
    return "CONSTRAINT_RELEASE_UNRESOLVED"


def classify_strict_reversal(a0_bounds: Interval, a1_bounds: Interval) -> str:
    """Classify the strict negative-to-positive transition A0 < 0 < A1."""
    if a0_bounds.high < 0 and a1_bounds.low > 0:
        return "STRICT_REVERSAL_IDENTIFIED"
    if a0_bounds.low >= 0 or a1_bounds.high <= 0:
        return "STRICT_REVERSAL_REFUTED"
    return "STRICT_REVERSAL_UNRESOLVED"


def classify_escape_claim_hierarchy(
    delta_w_bounds: Interval,
    *,
    a0_bounds: Interval,
    a1_bounds: Interval,
) -> EscapeClaimHierarchy:
    """Return all three outcome-claim levels without collapsing their meanings.

    The caller must supply uncertainty intervals for the total interaction,
    attraction without defence, and attraction with defence on compatible trait
    and outcome scales. The function intentionally does not reconstruct one
    interval from the others because their joint sampling covariance may matter.
    """
    return EscapeClaimHierarchy(
        interaction_relief=classify_interaction_relief(delta_w_bounds),
        constraint_release=classify_constraint_release(a0_bounds, a1_bounds),
        strict_reversal=classify_strict_reversal(a0_bounds, a1_bounds),
    )


def classify_escape_criterion(delta_w_bounds: Interval) -> str:
    """Legacy classifier for the algebraic total-interaction inequality.

    The bookkeeping inequality

        rho_delta > iota_delta + kappa_delta

    is exactly equivalent to ``Delta_AD W > 0`` on the same declared outcome
    scale. Historical repository outputs call this state ``ESCAPE_IDENTIFIED``.
    That token means only that the positive *interaction-level* inequality is
    identified. It does not establish A0 <= 0 < A1, a strict sign reversal,
    channel allocation, cue privacy, an evolutionary trajectory, or a global
    optimum. New analyses should additionally call
    :func:`classify_escape_claim_hierarchy` whenever A0 and A1 are available.

    This helper only classifies an already justified interval for the total
    interaction. It does not create that interval, assume commensurability, or
    promote a channel-specific interaction to total fitness.
    """
    if delta_w_bounds.low > 0:
        return "ESCAPE_IDENTIFIED"
    if delta_w_bounds.high <= 0:
        return "ESCAPE_REFUTED"
    return "ESCAPE_UNRESOLVED"


def partial_identification_from_total(
    delta_w: float,
    *,
    rho_bounds: Interval = Interval(),
    iota_bounds: Interval = Interval(),
    kappa_bounds: Interval = Interval(),
) -> PartialIdentificationResult:
    """Project channel bounds conditional on one observed total interaction.

    With no supplied restrictions, all three channel projections and the biotic
    balance remain unbounded even when ``delta_w`` is known exactly. Added
    biological or experimental information shrinks the set transparently.

    A particularly useful projection does not require sign restrictions on rho
    or iota. Since

        rho_delta - iota_delta = delta_w + kappa_delta,

    any lower/upper bound on kappa maps directly to a sharp bound on the biotic
    balance. Thus if ``kappa_delta >= 0`` and ``delta_w > 0``, then

        rho_delta - iota_delta >= delta_w > 0,

    while rho and iota can each remain individually unbounded. This is the clean
    partial-identification interpretation of the historical one-sided result.
    """
    if isnan(delta_w):
        raise ValueError("delta_w cannot be NaN")

    rho_from_others = Interval(
        delta_w + iota_bounds.low + kappa_bounds.low,
        delta_w + iota_bounds.high + kappa_bounds.high,
    )
    rho = rho_bounds.intersect(rho_from_others)
    if rho is None:
        return PartialIdentificationResult(delta_w, False, None, None, None, None)

    iota_from_others = Interval(
        rho_bounds.low - kappa_bounds.high - delta_w,
        rho_bounds.high - kappa_bounds.low - delta_w,
    )
    iota = iota_bounds.intersect(iota_from_others)

    kappa_from_others = Interval(
        rho_bounds.low - iota_bounds.high - delta_w,
        rho_bounds.high - iota_bounds.low - delta_w,
    )
    kappa = kappa_bounds.intersect(kappa_from_others)

    if iota is None or kappa is None:
        # For interval box constraints and one linear equality this should agree
        # with the rho projection feasibility check. Keep an explicit guard so
        # future changes cannot silently return inconsistent projections.
        return PartialIdentificationResult(delta_w, False, None, None, None, None)

    balance = Interval(delta_w + kappa.low, delta_w + kappa.high)
    return PartialIdentificationResult(delta_w, True, rho, iota, kappa, balance)
