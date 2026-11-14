"""Sharp thresholds for BITA's assumed exponential startup-cost model.

This is an additive THEORY-ONLY calculator, not an estimate of real evolutionary
costs, mutation rates, fixation or historical trait origins. No grid optimizer is
used. The existence result is analytic; returned numbers are float estimates.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import exp, expm1, isfinite, sqrt, ulp


@dataclass(frozen=True)
class StartupCostWindow:
    h: float
    s: float
    tau_over_s: float
    recoverable_loss: float
    lower_cost: float
    upper_cost: float
    normalized_upper_cost: float
    tangent_fraction: float
    exists_in_model: bool
    numerically_resolved: bool
    resolution: str
    transition_type: str
    data_level: str = 'THEORY_ONLY'


@dataclass(frozen=True)
class ConflictDistanceThresholds:
    global_gain_distance: float
    local_gradient_distance: float
    tangent_fraction: float
    has_strict_gap: bool
    numerically_resolved: bool
    data_level: str = 'THEORY_ONLY'


def _stationary_sign(v: float, r: float) -> float:
    """Sign of Q'(v); rescale its numerator to avoid exp overflow/cancellation."""
    x = v / r
    if x < .01:
        # H/v^2 = [(1-r)-v+(1-v)*(2*(exp(x)-1-x)/x^2-1)]/r.
        # The series starts at x/3; never subtract near-equal exponentials.
        term = x / 3.0
        tail = term
        for n in range(4, 17):
            term *= x / n
            tail += term
        return ((1.0-r)-v) + (1.0-v)*tail
    e = exp(-x)
    return 2.0*r*(1.0-v)*(-expm1(-x)) - v*(2.0-v)*e


def _positive_maximizer(r: float) -> float:
    """Unique maximizer of Q(v) for 0<r<1, inside (1-r,1).

    H(v)=2*r*(1-v)*(exp(v/r)-1)-v*(2-v) has derivative
    H'(v)=2*(1-v-r)*(exp(v/r)-1). Thus it increases to 1-r,
    decreases thereafter and crosses zero once before 1. Values rounded to an
    endpoint are retained at float resolution, not claimed mathematically exact.
    """
    lo, hi = 1.0-r, 1.0
    for _ in range(180):
        mid = lo+(hi-lo)/2.0
        if mid == lo or mid == hi:
            break
        if _stationary_sign(mid, r) > 0:
            lo = mid
        else:
            hi = mid
    return lo+(hi-lo)/2.0


def startup_cost_window(
    *, distance: float = 1.0, weight_1: float = 1.0,
    weight_2: float = 1.0, coupling: float = .5,
    activation_scale: float = .05,
) -> StartupCostWindow:
    """Return strict cap interval lower_cost < c < upper_cost for a trap.

    Gain is d^2*[2*h*u-(h+lambda)*u^2]-c*(1-exp(-u/tau)).
    There is a nonempty interval iff tau<s. For tau>=s, upper_cost is the
    limiting global bound at u=0 and the strict trap interval is empty.
    A mathematically present interval below float resolution is flagged, never
    relabelled as absent. Unrepresentable derived scales fail closed.
    """
    values = (distance, weight_1, weight_2, coupling, activation_scale)
    if not all(isfinite(x) for x in values):
        raise ValueError('parameters must be finite')
    if (distance <= 0 or weight_1 <= 0 or weight_2 <= 0
            or coupling < 0 or activation_scale <= 0):
        raise ValueError('distance, weights and scale must be positive; coupling >= 0')
    small, large = sorted((weight_1, weight_2))
    h = small/(1.0+small/large)
    total = h+coupling
    if not all(isfinite(x) and x > 0 for x in (h, total)):
        raise ValueError('rescale fitness units: weights unrepresentable')
    s = h/total
    d2 = distance*distance
    if not all(isfinite(x) and x > 0 for x in (h, total, s, d2)):
        raise ValueError('rescale trait or fitness units: derived terms unrepresentable')
    r = activation_scale/s
    recoverable = h*d2*s
    if not all(isfinite(x) and x > 0 for x in (r, recoverable)):
        raise ValueError('rescale trait or fitness units: normalized terms unrepresentable')
    lower = 2.0*recoverable*r
    exists = r < 1.0
    if not exists:
        q, upper, u = 2.0*r, lower, 0.0
    else:
        v = _positive_maximizer(r)
        q = v*(2.0-v)/(-expm1(-v/r))
        upper = max(lower, recoverable*q)
        u = s*v
    if not all(isfinite(x) and x > 0 for x in (lower, upper, q)):
        raise ValueError('rescale trait or fitness units: critical cost unrepresentable')
    resolved = exists and upper-lower > 64.0*max(ulp(lower), ulp(upper))
    resolution = ('RESOLVED' if resolved else 'EXISTS_BELOW_FLOAT_RESOLUTION') if exists else 'NO_STRICT_WINDOW'
    return StartupCostWindow(
        h=h, s=s, tau_over_s=r, recoverable_loss=recoverable,
        lower_cost=lower, upper_cost=upper, normalized_upper_cost=q,
        tangent_fraction=u, exists_in_model=exists,
        numerically_resolved=resolved, resolution=resolution,
        transition_type='FINITE_SEPARATION' if exists else 'CONTINUOUS',
    )


def conflict_distance_thresholds(
    *, cost_cap: float, weight_1: float = 1.0, weight_2: float = 1.0,
    coupling: float = .5, activation_scale: float = .05,
) -> ConflictDistanceThresholds:
    """Critical d for positive global gain and positive initial gradient.

    Global gain requires d>d_global; local gradient requires d>d_local.
    At d_global there is no strict global gain. At d_local the initial slope
    is zero; higher-order small changes can still benefit when tau<s.
    For tau<s and c>0 a strict intermediate interval exists mathematically;
    numerically_resolved indicates whether its float calculation is usable.
    """
    if not isfinite(cost_cap) or cost_cap < 0:
        raise ValueError('cost cap must be finite and nonnegative')
    w = startup_cost_window(
        distance=1.0, weight_1=weight_1, weight_2=weight_2,
        coupling=coupling, activation_scale=activation_scale,
    )
    global_d = sqrt(cost_cap)/sqrt(w.upper_cost)
    local_d = sqrt(cost_cap)/sqrt(w.lower_cost)
    if not all(isfinite(x) for x in (global_d, local_d)):
        raise ValueError('rescale trait or fitness units: distance threshold unrepresentable')
    has_gap = cost_cap > 0 and w.exists_in_model
    return ConflictDistanceThresholds(
        global_gain_distance=global_d, local_gradient_distance=local_d,
        tangent_fraction=w.tangent_fraction,
        has_strict_gap=has_gap,
        numerically_resolved=has_gap and w.numerically_resolved,
    )
