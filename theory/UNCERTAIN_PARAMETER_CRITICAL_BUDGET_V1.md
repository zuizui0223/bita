# BITA uncertain-parameter critical-budget theorem v1

## Purpose

Propagate uncertainty in architecture deficit, active coupling sensitivity and curvature bounds into a fail-closed interval for the static decoupling budget needed to cross the architecture boundary.

The earlier two-sided theorem assumed `delta`, `c`, `alpha` and `beta` were known. Here they are only bounded.

## Setup

Suppose the true quantities satisfy

\[
\delta\in[\delta_L,\delta_U],
\qquad
c\in[c_L,c_U],
\]

with

\[
0<\delta_L\le\delta_U,
\qquad
0\le c_L\le c_U.
\]

Assume Euclidean curvature bounds are themselves conservatively registered as

\[
\alpha\ge\alpha_L\ge0,
\qquad
\beta\le\beta_U,
\]

so that over the relevant intervention region

\[
\alpha_L I
\preceq
\nabla^2R
\preceq
\beta_U I.
\]

Define

\[
r_\gamma(\delta,c)
\]

as the positive solution to

\[
c\varepsilon+
\frac{\gamma}{2}\varepsilon^2
=
\delta.
\]

## Monotonicity facts

The root `r_gamma(delta,c)` is:

- increasing in `delta`;
- decreasing in `c`;
- decreasing in `gamma`.

These monotonicities determine which interval endpoints are conservative for exclusion and guarantee statements.

## Theorem 1 — robust no-cross budget

For a budget `epsilon`, the largest gain consistent with the registered uncertainty uses:

- the largest possible current gradient norm `c_U`;
- the largest allowed curvature `beta_U`.

The smallest possible deficit is `delta_L`.

Therefore if

\[
c_U\varepsilon+
\frac{\beta_U}{2}\varepsilon^2
\le
\delta_L,
\]

then no admissible parameter realization can cross.

Equivalently, define

\[
\boxed{
\varepsilon_{robust\;no}
=
r_{\beta_U}(\delta_L,c_U).
}
\]

Every budget

\[
\varepsilon\le\varepsilon_{robust\;no}
\]

is a **robust no-cross region** under the registered uncertainty set.

## Theorem 2 — robust sufficient budget

To guarantee crossing for every admissible parameter realization, use the hardest case:

- largest deficit `delta_U`;
- smallest active-penalty norm `c_L`;
- smallest guaranteed curvature `alpha_L`.

Define

\[
\boxed{
\varepsilon_{robust\;yes}
=
r_{\alpha_L}(\delta_U,c_L).
}
\]

If the corresponding aligned move is feasible for every admissible realization, then any

\[
\varepsilon>\varepsilon_{robust\;yes}
\]

guarantees a static crossing for the entire parameter uncertainty set.

## Theorem 3 — partial-identification band for the critical budget

Let `epsilon_*` denote the true minimum crossing budget. The registered uncertainty implies

\[
\boxed{
\varepsilon_{robust\;no}
\le
\varepsilon_*
\le
\varepsilon_{robust\;yes}
}
\]

provided the sufficient aligned move is feasible.

The interval combines two sources of structural uncertainty:

1. higher-order coupling geometry (`alpha_L`, `beta_U`);
2. uncertainty in current architecture deficit and active coupling sensitivity (`delta`, `c`).

## Corollary 3a — exact-parameter theorem recovered

If

\[
\delta_L=\delta_U=\delta,
\qquad
c_L=c_U=c,
\qquad
\alpha_L=\alpha,
\qquad
\beta_U=\beta,
\]

then the interval reduces to the earlier two-sided critical-budget bracket

\[
r_\beta(\delta,c)
\le
\varepsilon_*
\le
r_\alpha(\delta,c).
\]

## Theorem 4 — uncertainty-source attribution

Because the root is monotone in each argument, tightening any one uncertainty interval while holding the others fixed cannot widen the robust critical-budget band.

Thus the value of additional data can be evaluated by asking which bound currently controls the interval width:

- better `delta` estimation narrows architecture-gap uncertainty;
- better `c` estimation narrows local coupling-sensitivity uncertainty;
- better intermediate coupling levels narrow curvature uncertainty.

This provides a principled way to choose between more worldline replication and more coupling-resolution experiments.

## Empirical consequence

A prospective BITA analysis can report:

```text
[delta_L, delta_U]  architecture deficit interval
[c_L, c_U]          active penalty norm interval
alpha_L, beta_U     curvature bounds

epsilon_robust_no   below this: crossing excluded
epsilon_robust_yes  above this: crossing guaranteed
middle band          unresolved by current bounds
```

This avoids pretending that point-estimate intervention thresholds are identified when their ingredients are not.

## Metric extension

The same construction holds under a positive-definite intervention metric `Q` by replacing `c` with the dual metric norm

\[
c_Q=\sqrt{\mathbf c^\top Q^{-1}\mathbf c}
\]

and using curvature bounds relative to `Q`.

## Claim ceiling

The theorem assumes the uncertainty intervals are valid simultaneous bounds, not separate marginal confidence intervals naively combined without coverage control. It also assumes fixed `K`, a common feasible phenotype space and feasible aligned moves for the sufficient certificate. The result is a static BITA partial-identification statement, not a PAYOFF invasion threshold.
