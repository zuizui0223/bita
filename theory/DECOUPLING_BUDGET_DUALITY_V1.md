# BITA decoupling-budget duality theorem v1

## Purpose

Show that the **shape of the intervention budget itself** determines whether optimal decoupling should be concentrated on one coupling channel or distributed across many channels.

This complements the metric optimal-decoupling theorem by making the norm dependence explicit.

## Setup

Let the active coupling-penalty vector at the current optimum be

\[
\mathbf c^*=(c_1^*,\ldots,c_m^*)\ge0.
\]

Write a decoupling intervention as

\[
x=-\delta\boldsymbol\lambda\ge0,
\]

so the first-order gain in recoverable fitness is

\[
\Delta R^{(1)}=\mathbf c^{*\top}x.
\]

Suppose the available intervention budget is

\[
\|x\|_p\le\varepsilon.
\]

Let `q` be the Holder-dual exponent:

\[
\frac1p+\frac1q=1.
\]

## Theorem 1 — dual-norm maximum gain

Holder's inequality gives

\[
\mathbf c^{*\top}x
\le
\|\mathbf c^*\|_q\|x\|_p.
\]

Therefore

\[
\boxed{
\Delta R_{\max}^{(1)}
=
\varepsilon\|\mathbf c^*\|_q.
}
\]

The biological meaning is that the same coupling landscape can favour qualitatively different intervention strategies depending on how intervention cost accumulates across channels.

## Corollary 1a — L1 budget gives sparse decoupling

For

\[
\|x\|_1\le\varepsilon,
\]

the dual norm is `L_infinity`, so

\[
\boxed{
\Delta R_{\max}^{(1)}
=
\varepsilon\max_i c_i^*.
}
\]

An optimum is obtained by spending the entire budget on any channel with maximal active penalty.

Thus an additive resource budget predicts **single-channel targeting**.

## Corollary 1b — L2 budget gives proportional distributed decoupling

For

\[
\|x\|_2\le\varepsilon,
\]

the dual is also `L2`, giving

\[
\boxed{
\Delta R_{\max}^{(1)}
=
\varepsilon\|\mathbf c^*\|_2
}
\]

with optimizer

\[
\boxed{
x^*=\varepsilon\frac{\mathbf c^*}{\|\mathbf c^*\|_2}.}
\]

So a quadratic intervention budget predicts distributed decoupling proportional to active penalties.

## Corollary 1c — L-infinity budget gives broad parallel decoupling

For

\[
\|x\|_\infty\le\varepsilon,
\]

the dual is `L1`, hence

\[
\boxed{
\Delta R_{\max}^{(1)}
=
\varepsilon\sum_i c_i^*.
}
\]

If all penalties are non-negative, an optimizer sets

\[
\boxed{x_i^*=\varepsilon}
\]

for every channel with positive penalty.

Thus a per-channel cap rather than a total resource budget favours **parallel weakening of all active couplings**.

## Theorem 2 — intervention architecture is not a property of the biological system alone

The vector `c*` describes the biological marginal penalties, but the optimal intervention also depends on the feasible-budget geometry.

The same `c*` can therefore imply:

```text
L1 budget        -> sparse one-channel decoupling
L2 budget        -> graded distributed decoupling
L-infinity budget -> simultaneous broad decoupling
```

Hence the statement "channel i is the best decoupling target" is incomplete unless the intervention budget or cost geometry is declared.

## Weighted extension

A diagonal quadratic metric

\[
\sum_i q_i x_i^2\le\varepsilon^2
\]

is equivalent to an `L2` budget after coordinate rescaling and recovers the previously registered rule

\[
x_i^*\propto\frac{c_i^*}{q_i}.
\]

More general weighted `Lp` budgets yield the corresponding weighted dual norm.

## Empirical consequence

A multi-channel BITA experiment should preregister not only which couplings can be manipulated, but also how intervention effort is counted.

Different experimental constraints answer different biological questions:

- limited total manipulation effort asks for the strongest single bottleneck;
- quadratic costs ask for a distributed optimal release profile;
- independent per-channel caps ask how much total recovery is available when every coupling can be weakened simultaneously.

Observed departures from the predicted first-order allocation can indicate nonlinear coupling interactions, shifting active phenotypes, off-target effects or an incorrect intervention-cost model.

## Claim ceiling

The theorem is local and first-order in the coupling changes. It assumes the active penalty vector is evaluated at the current optimum and remains a valid local gradient. Large interventions can change the optimum, penalty vector, feasible set or architecture cost. The result concerns static recoverable fitness and does not determine PAYOFF invasion dynamics.
