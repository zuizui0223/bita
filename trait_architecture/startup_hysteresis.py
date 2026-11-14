"""Equilibrium persistence in the frozen BITA exponential startup model.

THEORY ONLY. History dependence additionally assumes local projected-gradient
ascent and quasi-static environmental changes, not genetic evolution or fixation.
The cost is paid as a state-dependent cost, NOT an irreversible sunk expenditure.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import exp, expm1, isfinite, log, log1p, ulp

from .startup_thresholds import conflict_distance_thresholds, startup_cost_window


@dataclass(frozen=True)
class ContinuationThresholds:
    persistence_distance: float | None
    log_persistence_distance: float | None
    global_gain_distance: float
    entry_distance: float
    fold_fraction: float
    has_hysteresis: bool
    numerically_resolved: bool
    data_level: str = 'THEORY_ONLY'


@dataclass(frozen=True)
class Equilibria:
    phase: str
    shared_locally_stable: bool
    unstable_fraction: float | None
    differentiated_fraction: float | None
    data_level: str = 'THEORY_ONLY'


def _fold_log_ratio(r: float) -> float:
    """log(d_fold^2/d_entry^2)=1-1/r-log(r), for 0<r<1."""
    delta=1-r
    if delta < .01:
        # -sum_{n>=2} ((n-1)/n)*delta**n avoids cancellation as r -> 1.
        return -sum((n-1)/n*delta**n for n in range(2,21))
    return -delta/r-log1p(-delta) if delta < 1 else 1-1/r-log(r)


def continuation_thresholds(
    *, cost_cap: float, weight_1: float=1., weight_2: float=1.,
    coupling: float=.5, activation_scale: float=.05,
) -> ContinuationThresholds:
    """Three boundaries; a strict bistable interval exists iff c>0 and tau<s.

    For tau<s, u_fold=s-tau and d_fold^2=c*exp(1-s/tau)/(2*(h+lambda)*tau^2).
    A fold lost to float underflow is returned as None with its finite log,
    never as a mathematically zero threshold. Coincident float thresholds are
    flagged unresolved rather than falsely treated as no hysteresis.
    """
    kw=dict(weight_1=weight_1,weight_2=weight_2,coupling=coupling,
            activation_scale=activation_scale)
    old=conflict_distance_thresholds(cost_cap=cost_cap,**kw)
    w=startup_cost_window(**kw)
    active=cost_cap>0 and w.exists_in_model
    if not active:
        d=old.local_gradient_distance
        return ContinuationThresholds(d,log(d) if d>0 else None,
                                      old.global_gain_distance,d,0.,False,True)
    r=w.tau_over_s
    logfold=log(old.local_gradient_distance)+.5*_fold_log_ratio(r)
    if not isfinite(logfold):
        raise ValueError('rescale parameters: log persistence threshold unrepresentable')
    fold=exp(logfold)
    fold=fold if fold>0 else None
    resolved=(fold is not None and old.numerically_resolved and
              old.global_gain_distance-fold>64*ulp(old.global_gain_distance) and
              old.local_gradient_distance-old.global_gain_distance>64*ulp(old.local_gradient_distance))
    return ContinuationThresholds(fold,logfold,old.global_gain_distance,
                                  old.local_gradient_distance,w.s-activation_scale,
                                  True,resolved)


def _ell(t: float,r: float) -> float:
    """Stationarity: ell(t)=log(d^2/d_entry^2), t=-log(1-u/s)."""
    if t < .01:
        term=t*t/2
        tail=term
        for n in range(3,19):
            term *= -t/n
            tail += term
        return ((r-1)*t+tail)/r
    return t+expm1(-t)/r


def _root(target: float,r: float,lo: float,hi: float,*,increasing: bool) -> float:
    for _ in range(180):
        mid=lo+(hi-lo)/2
        if mid==lo or mid==hi:
            break
        if (_ell(mid,r)<target)==increasing:
            lo=mid
        else:
            hi=mid
    return lo+(hi-lo)/2


def equilibria(
    *, distance: float,cost_cap: float,weight_1: float=1.,weight_2: float=1.,
    coupling: float=.5,activation_scale: float=.05,
) -> Equilibria:
    """Find both stationary branches without a fixed u-grid or forward walk.

    Marginal numerical neighborhoods are labelled explicitly. 'Stable' refers
    only to the declared projected-gradient phenotype dynamics.
    """
    if not isfinite(distance) or distance<0:
        raise ValueError('distance must be finite and nonnegative')
    kw=dict(weight_1=weight_1,weight_2=weight_2,coupling=coupling,
            activation_scale=activation_scale)
    t=continuation_thresholds(cost_cap=cost_cap,**kw)
    w=startup_cost_window(**kw)
    if cost_cap==0:
        if distance==0:
            return Equilibria('NEUTRAL_LANDSCAPE',False,None,None)
        return Equilibria('DIFFERENTIATED_ONLY',False,None,w.s)
    if distance==0:
        return Equilibria('SHARED_ONLY',True,None,None)
    r=w.tau_over_s
    invr=1/r
    if not isfinite(invr):
        raise ValueError('rescale parameters: normalized curvature unrepresentable')
    target=2*(log(distance)-log(t.entry_distance))
    tol=64*ulp(max(1.,abs(target)))
    local_boundary=abs(target)<=tol
    shared=target<0 or (local_boundary and r>=1)
    low_t=0.
    if r<1:
        minimum=_fold_log_ratio(r)
        foldtol=64*ulp(max(1.,abs(target),abs(minimum)))
        if abs(target-minimum)<=foldtol:
            return Equilibria('FOLD_MARGINAL',True,None,None)
        if target<minimum:
            return Equilibria('SHARED_ONLY',True,None,None)
        low_t=-log(r)
    elif target<=tol:
        return Equilibria('LOCAL_MARGINAL' if local_boundary else 'SHARED_ONLY',
                          True,None,None)
    high_t=max(low_t+1.,target+invr+1.)
    if not isfinite(high_t):
        raise ValueError('rescale parameters: stationary bracket unrepresentable')
    stable_t=_root(target,r,low_t,high_t,increasing=True)
    stable=w.s*(-expm1(-stable_t))
    unstable=None
    if r<1 and target < -tol:
        unstable_t=_root(target,r,0.,low_t,increasing=False)
        unstable=w.s*(-expm1(-unstable_t))
    phase=('LOCAL_MARGINAL' if local_boundary else
           'BISTABLE' if unstable is not None else 'DIFFERENTIATED_ONLY')
    return Equilibria(phase,shared,unstable,stable)


def local_attractor(initial_fraction: float,**parameters) -> float:
    """Limit under fixed-environment projected-gradient flow, not fixation.

    Sampling these limits along a fine d-ramp is a quasi-static approximation.
    At an exact separatrix or marginal threshold no unqualified attractor is
    selected. The neutral zero-cost/zero-conflict landscape retains its input.
    """
    if not isfinite(initial_fraction) or not 0<=initial_fraction<=1:
        raise ValueError('initial fraction must be finite and in [0,1]')
    e=equilibria(**parameters)
    if e.phase.endswith('MARGINAL'):
        raise ValueError('marginal threshold: no strict attractor assigned')
    if e.phase=='NEUTRAL_LANDSCAPE':
        return initial_fraction
    if e.phase=='SHARED_ONLY':
        return 0.
    if e.unstable_fraction is None:
        return e.differentiated_fraction
    if abs(initial_fraction-e.unstable_fraction)<=64*ulp(max(1.,abs(initial_fraction))):
        raise ValueError('initial fraction lies on the unstable separatrix')
    return e.differentiated_fraction if initial_fraction>e.unstable_fraction else 0.
