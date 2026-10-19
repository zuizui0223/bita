"""Bounded-step accessibility of trait differentiation after SCH-style compromise.

This is an explicit selection-on-a-trait-landscape toy model, NOT a population
genetic analysis, simulation of speciation, or claim of observed historical evolution.
The same two functional optima as the existing quadratic BITA model are used.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import exp, expm1, isfinite, sqrt


@dataclass(frozen=True)
class LandscapeResult:
    optimum_distance: float
    shared_conflict_loss: float
    baseline_recoverable_loss: float
    baseline_decoupling: float
    activation_cost_cap: float
    activation_scale: float
    initial_selection_gradient: float
    selected_separation_fraction: float
    maximum_relative_fitness: float
    first_positive_invasion_fraction: float | None
    classification: str


def _terms(
    distance: float, weight_1: float, weight_2: float, coupling: float,
    activation_cost_cap: float, activation_scale: float,
) -> tuple[float, float, float, float, float]:
    values = (distance, weight_1, weight_2, coupling,
              activation_cost_cap, activation_scale)
    if not all(isfinite(v) for v in values):
        raise ValueError("parameters must be finite")
    if (distance < 0 or weight_1 <= 0 or weight_2 <= 0 or coupling < 0
            or activation_cost_cap < 0 or activation_scale <= 0):
        raise ValueError("invalid weights, distance, coupling, or activation cost")
    h = weight_1 / (1.0 + weight_1 / weight_2)
    d2 = distance * distance
    if not isfinite(d2) or not isfinite(h*d2) or not isfinite(coupling*d2):
        raise ValueError("rescale trait or fitness units")
    return h, d2, coupling, activation_cost_cap, activation_scale


def gain_at_fraction(
    fraction: float, *, distance: float, weight_1: float = 1.0,
    weight_2: float = 1.0, coupling: float = 0.5,
    activation_cost_cap: float = 0.15, activation_scale: float = 0.05,
) -> float:
    """Gain over optimized shared phenotype at separation fraction u in [0,1].

    x-y = u*(theta1-theta2); the weighted functional center stays fixed.
    K(u)=K_cap*(1-exp(-u/tau)) is an ASSUMED saturating architecture cost.
    """
    h, d2, lam, cap, tau = _terms(
        distance, weight_1, weight_2, coupling,
        activation_cost_cap, activation_scale,
    )
    if not isfinite(fraction) or not 0 <= fraction <= 1:
        raise ValueError("separation fraction must be in [0,1]")
    u = fraction
    return d2*(2*h*u - (h+lam)*u*u) + cap*expm1(-u/tau)


def initial_gradient(
    *, distance: float, weight_1: float = 1.0,
    weight_2: float = 1.0, coupling: float = 0.5,
    activation_cost_cap: float = 0.15, activation_scale: float = 0.05,
) -> float:
    """Fitness slope of arbitrarily small separation from shared u=0."""
    h, d2, _, cap, tau = _terms(
        distance, weight_1, weight_2, coupling,
        activation_cost_cap, activation_scale,
    )
    return 2*h*d2 - cap/tau


def _bisect(function, left: float, right: float) -> float:
    fl, fr = function(left), function(right)
    if fl == 0:
        return left
    if fr == 0:
        return right
    if (fl < 0) == (fr < 0):
        raise ValueError("no bracketing sign change")
    for _ in range(65):
        mid = (left+right)/2
        fm = function(mid)
        if fm == 0:
            return mid
        if (fm < 0) == (fl < 0):
            left, fl = mid, fm
        else:
            right = mid
    return (left+right)/2


def landscape(
    *, distance: float, weight_1: float = 1.0,
    weight_2: float = 1.0, coupling: float = 0.5,
    activation_cost_cap: float = 0.15, activation_scale: float = 0.05,
) -> LandscapeResult:
    """Global phenotype optimum versus local invasion from the shared state.

    A fitness valley is not automatically an evolutionary impossibility:
    sufficiently large mutations, stochastic valley crossing or drift can cross.
    """
    h, d2, lam, cap, tau = _terms(
        distance, weight_1, weight_2, coupling,
        activation_cost_cap, activation_scale,
    )
    params = dict(
        distance=distance, weight_1=weight_1, weight_2=weight_2,
        coupling=coupling, activation_cost_cap=cap, activation_scale=tau,
    )
    f = lambda u: gain_at_fraction(u, **params)
    deriv = lambda u: d2*(2*h-2*(h+lam)*u)-(cap/tau)*exp(-u/tau)

    # f'' decreases monotonically: f' has at most two interior roots.
    grid = [i/1024 for i in range(1025)]
    stationary = []
    for a, b in zip(grid, grid[1:]):
        fa, fb = deriv(a), deriv(b)
        if fa == 0 and 0 < a < 1:
            stationary.append(a)
        if (fa < 0 < fb) or (fb < 0 < fa):
            stationary.append(_bisect(deriv, a, b))
    candidates = sorted(set([0.0, 1.0] + stationary))
    opt = max(candidates, key=f)
    best = f(opt)
    grad0 = deriv(0.0)
    tol = 1e-10*max(1.0, abs(best), h*d2, cap)

    first = None
    if best <= tol:
        outcome = "SHARED_GLOBAL_OPTIMUM"
    elif grad0 > tol:
        outcome = "SMALL_STEPS_CAN_INVADE"
        first = 0.0
    elif grad0 < -tol:
        outcome = "GLOBAL_GAIN_BUT_LOCAL_TRAP"
        for a, b in zip(candidates, candidates[1:]):
            if f(a) < 0 < f(b):
                first = _bisect(f, a, b)
                break
        if first is None:
            raise ArithmeticError("positive global peak without a crossing")
    else:
        outcome = "LOCAL_MARGINAL"
    conflict = h*d2
    s = h/(h+lam) if lam > 0 else 1.0
    return LandscapeResult(
        optimum_distance=sqrt(d2), shared_conflict_loss=conflict,
        baseline_recoverable_loss=s*conflict, baseline_decoupling=s,
        activation_cost_cap=cap, activation_scale=tau,
        initial_selection_gradient=grad0,
        selected_separation_fraction=opt, maximum_relative_fitness=best,
        first_positive_invasion_fraction=first, classification=outcome,
    )


def deterministic_uphill_walk(
    *, maximum_step: float, iterations: int = 100,
    proposals: int = 100, **landscape_params,
) -> tuple[float, ...]:
    """Deterministic uphill-only bounded mutant walk; NOT genetic fixation."""
    if not isfinite(maximum_step) or not 0 < maximum_step <= 1:
        raise ValueError("maximum_step must lie in (0,1]")
    if iterations < 1 or proposals < 1:
        raise ValueError("iterations and proposals must be >= 1")
    trajectory = [0.0]
    for _ in range(iterations):
        current = trajectory[-1]
        options = [
            min(1.0, current+maximum_step*j/proposals)
            for j in range(1, proposals+1)
        ]
        candidate = max(options, key=lambda u: gain_at_fraction(u, **landscape_params))
        if (gain_at_fraction(candidate, **landscape_params)
                <= gain_at_fraction(current, **landscape_params)+1e-12):
            break
        trajectory.append(candidate)
    return tuple(trajectory)


def example_readout() -> dict:
    """Five prespecified hypothetical contrasts, never labelled empirical."""
    params = dict(
        weight_1=1.0, weight_2=1.0, coupling=0.5,
        activation_cost_cap=0.15, activation_scale=0.05,
    )
    result = [landscape(distance=d, **params) for d in (0.5, 0.8, 1.0, 1.5, 2.0)]
    h = 0.5
    s = 0.5
    return {
        "model": "BITA_ACTIVATION_COST_UPHILL_PROXY_V1",
        "data_level": "THEORY_SIMULATION_ONLY",
        "assumptions": "quadratic functions and coupling, saturating activation cost, uphill mutant proposals",
        "parameters": params,
        "scenarios": [asdict(v) for v in result],
        "d1_uphill_small_step": deterministic_uphill_walk(
            maximum_step=0.1, distance=1.0, **params,
        ),
        "d1_uphill_large_step": deterministic_uphill_walk(
            maximum_step=0.25, distance=1.0, **params,
        ),
        # This is a SUFFICIENT global-favour bound; actual threshold can be lower.
        "sufficient_global_favour_distance": sqrt(params["activation_cost_cap"]/(h*s)),
        "local_gradient_sign_flip_distance": sqrt(
            params["activation_cost_cap"]/(2*h*params["activation_scale"])
        ),
    }
