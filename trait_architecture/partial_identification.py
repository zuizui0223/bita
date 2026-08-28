"""Partial identification for attraction-defence channel allocation.

The canonical identification paper distinguishes the observed total two-level
interaction

    Delta_AD W = rho_delta - iota_delta - kappa_delta

from its channel allocation. Full crossed interventions can point-identify the
biotic channels under the declared gates, but incomplete studies need not be
classified only as "identified" or "not identified". When external knowledge
supplies bounds on one or more channels, the equality above defines an exact
identified set and corresponding projection intervals.

This module keeps that logic deliberately assumption-indexed. It never treats a
sign restriction, cost bound, or consumer bound as empirical fact unless the
caller supplies it.
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


def classify_escape_criterion(delta_w_bounds: Interval) -> str:
    """Classify the strict escape inequality from a total-interaction interval.

    Because the declared bookkeeping identity is

        Delta_AD W = rho_delta - iota_delta - kappa_delta,

    the biological escape criterion

        rho_delta > iota_delta + kappa_delta

    is exactly equivalent to ``Delta_AD W > 0`` on the same declared outcome
    scale. Point-identifying rho, iota and kappa is therefore *not* required to
    decide whether the strict inequality holds. Full allocation is required to
    explain which channel generated the sign.

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
