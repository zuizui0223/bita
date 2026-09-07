# BITA monotone decoupling order theorem v1

## Purpose

Generalize fixed-ray criticality to **arbitrary coordinatewise monotone decoupling paths**.

BITA already treats recoverable fitness `R(lambda)` as coordinatewise non-increasing in residual coupling `lambda`. Equivalently, recoverable fitness is coordinatewise non-decreasing in decoupling amount `x=lambda_0-lambda`. This order structure alone implies a strong topology for the static architecture states: the BITA-favored region is an upper set in decoupling space, the shared-favored region is a lower set, and a monotone decoupling trajectory cannot cross to BITA and later return to shared while architecture cost is fixed.

## Setup

Let

\[
F(x)=R(\lambda_0-x)-K
\]

be the static optimized-fitness architecture margin, where larger `x>=0` means more decoupling and `K` is fixed.

Assume only that recoverable fitness is coordinatewise monotone:

\[
x\le y
\quad\Longrightarrow\quad
R(\lambda_0-x)\le R(\lambda_0-y).
\]

No convexity is required for the order results below.

Define

\[
\mathcal D_+=\{x:F(x)>0\}
\]

for BITA-favored interventions and

\[
\mathcal D_-=\{x:F(x)\le0\}
\]

for shared-favored or boundary interventions.

## Theorem 1 — BITA-favored region is an upper set

If

\[
x\in\mathcal D_+
\]

and `y>=x` componentwise, then

\[
F(y)\ge F(x)>0.
\]

Therefore

\[
\boxed{
x\in\mathcal D_+,\ y\ge x
\Rightarrow y\in\mathcal D_+.}
\]

Once a static architecture is differentiation-favored, any intervention with at least as much decoupling in every channel remains differentiation-favored under the model.

## Theorem 2 — shared-favored region is a lower set

If

\[
y\in\mathcal D_-
\]

and `x<=y`, then

\[
F(x)\le F(y)\le0.
\]

Thus

\[
\boxed{
y\in\mathcal D_-,\ x\le y
\Rightarrow x\in\mathcal D_-.}
\]

## Theorem 3 — no re-entry along arbitrary monotone decoupling paths

Let

\[
x(t),\qquad t\in[0,1],
\]

be any path satisfying

\[
t_2\ge t_1
\Rightarrow
x(t_2)\ge x(t_1)
\]

componentwise.

Then

\[
F(x(t))
\]

is non-decreasing in `t`.

Hence along the path the state order can only be

```text
shared-favored -> boundary/plateau -> BITA-favored
```

and never

```text
BITA-favored -> shared-favored
```

without violating a registered assumption.

This is stronger than a fixed-ray result because the relative allocation among coupling channels may change arbitrarily as long as total decoupling is coordinatewise non-decreasing.

## Corollary 3a — one-sided sequential stopping

In a sequential decoupling experiment, once a treatment is certified BITA-favored, every later treatment that dominates it componentwise is predicted to remain BITA-favored. Such later treatments are unnecessary for proving **existence** of a static crossing, although they can still test mechanism, curvature or monotonicity.

Conversely, observing a shared-favored treatment does not rule out crossing at a more-decoupled treatment.

## Theorem 4 — strict monotonicity makes the critical frontier an antichain

Suppose additionally that for any distinct comparable interventions `x<y` in the relevant domain,

\[
F(y)>F(x).
\]

Then two distinct points on the exact critical frontier

\[
\mathcal C=\{x:F(x)=0\}
\]

cannot be componentwise comparable.

Therefore

\[
\boxed{\mathcal C\text{ is an antichain under the product order}.}
\]

Under weak monotonicity, comparable boundary points may occur only as plateaus.

## Theorem 5 — minimal critical interventions form the lower boundary of the upper set

Define a BITA-favored intervention `x` as **minimal** if no strictly smaller `y<x` is BITA-favored.

The collection of minimal BITA-favored interventions forms the order frontier separating the lower shared region from the upper BITA region. Any BITA-favored intervention dominates at least one minimal crossing intervention when such minima exist in the compact registered domain.

This gives a nonparametric notion of `critical architecture intervention` without choosing a single scalar coupling index.

## Empirical consequence

A multi-channel causal experiment can preregister a monotone treatment lattice or staircase. The theory predicts:

1. architecture-margin signs must be order-consistent;
2. a positive crossing cannot be followed by a negative state at a dominating treatment;
3. critical treatments should form an order frontier rather than isolated re-entrant islands;
4. dominated post-crossing treatments can be held out as falsification checks instead of confirmatory crossing searches.

An observed order reversal is especially informative because convexity is not needed for this diagnostic.

## Failure interpretation

If `y>=x` but matched optimized fitness gives

\[
F(x)>0,
\qquad
F(y)<0,
\]

then at least one assumption changed. Candidate explanations include:

- architecture cost `K` increased with stronger decoupling;
- baseline fitness or feasible phenotype space changed;
- a nominal coupling coordinate is not actually monotone;
- treatment side effects introduced a new cost/channel;
- contexts or fitness scales are mismatched.

## Separation from PAYOFF

The order theorem concerns static optimized-fitness architecture ordering. It does not imply invasion, establishment, coexistence or evolutionary reachability. A more-decoupled static architecture may still fail to invade because PAYOFF frequency-dependent terms differ.

## Claim ceiling

The theorem requires a common matched context, fixed `K` for the stated architecture margin, and coordinatewise monotonic recoverable fitness over the registered intervention domain. If decoupling itself changes architecture cost, accessibility or baseline landscape, the simple product-order result must be extended rather than applied mechanically.
