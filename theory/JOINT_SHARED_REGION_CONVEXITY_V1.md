# BITA joint shared-region convexity theorem v1

## Purpose

Describe the global geometry of the shared-favored side of the static architecture comparison in coupling-cost space.

The result complements the decoupling-ray theorem. Instead of following one monotone ray, it considers arbitrary convex combinations of two coupling/cost states and shows that the shared-favored region cannot contain hidden BITA islands when recoverable fitness is convex in coupling and architecture cost enters additively.

## Setup

Let residual coupling be

\[
\boldsymbol\lambda\in\Lambda\subset\mathbb R^m,
\]

with convex domain `Lambda`.

Let recoverable fitness

\[
R(\boldsymbol\lambda)
\]

be convex and coordinatewise non-increasing on `Lambda`.

Let architecture cost be `K`, and define the static differentiated-minus-shared margin

\[
F(\boldsymbol\lambda,K)
=R(\boldsymbol\lambda)-K.
\]

The BITA side is `F>0`; the shared-favored side is

\[
\mathcal S
=
\{(\boldsymbol\lambda,K):F(\boldsymbol\lambda,K)\le0\}.
\]

## Theorem 1 — joint architecture margin is convex

Because `R(lambda)` is convex and `-K` is affine,

\[
\boxed{F(\boldsymbol\lambda,K)=R(\boldsymbol\lambda)-K\text{ is jointly convex}.}
\]

This remains true when `K` varies across the comparison, provided `K` is itself the registered additive architecture-cost coordinate rather than a proxy changing the definition of `R`.

## Theorem 2 — the shared-favored region is convex

A sublevel set of a convex function is convex. Therefore

\[
\boxed{\mathcal S=\{F\le0\}\text{ is convex}.}
\]

Take any two shared-favored states

\[
x_0=(\lambda_0,K_0),
\qquad
x_1=(\lambda_1,K_1)
\]

with

\[
F(x_0)\le0,
\qquad
F(x_1)\le0.
\]

For any `t in [0,1]`, define

\[
x_t=(1-t)x_0+tx_1.
\]

Convexity gives

\[
F(x_t)
\le
(1-t)F(x_0)+tF(x_1)
\le0.
\]

Hence

\[
\boxed{x_t\in\mathcal S.}
\]

## Corollary 2a — no hidden BITA island between shared endpoints

If two endpoints of a straight intervention chord in joint coupling-cost space are shared-favored, every point between them must also be shared-favored under the registered convex static model.

Therefore the pattern

```text
shared-favored endpoint
BITA-favored interior point
shared-favored endpoint
```

is impossible under the theorem.

Observing such a pattern falsifies at least one of:

- convexity of recoverable fitness in coupling;
- additive fixed meaning of the `K` coordinate;
- common feasible phenotype space;
- matched context/fitness scale;
- the static architecture model.

This is a multivariate global shape test, not a PAYOFF invasion statement.

## Corollary 2b — fixed-K shared coupling region is convex

For a fixed architecture cost `K_0`,

\[
\mathcal S_{K_0}
=
\{\lambda:R(\lambda)\le K_0\}
\]

is convex in coupling space.

Thus arbitrary straight mixtures of two shared-favored coupling vectors remain shared-favored, even when the path is not a coordinatewise monotone decoupling ray.

This strictly generalizes the topological information available from one-dimensional graded coupling experiments.

## Theorem 3 — chord upper bound and direct convexity audit

Let endpoint margins be

\[
m_0=F(x_0),
\qquad
m_1=F(x_1).
\]

For an interior point `x_t`, convexity requires

\[
\boxed{
F(x_t)
\le
(1-t)m_0+tm_1.
}
\]

Define the chord residual

\[
r_F(t)
=F(x_t)-[(1-t)m_0+tm_1].
\]

Then

\[
\boxed{r_F(t)\le0.}
\]

This gives a direct held-out shape test for graded or factorial coupling-cost experiments.

## Corollary 3a — endpoint exclusion certificate

If both endpoint margins are nonpositive, the largest chord upper bound is at most

\[
\max(m_0,m_1)\le0.
\]

Hence endpoints alone exclude a hidden positive architecture margin over the straight segment **once joint convexity has been independently accepted or preregistered**.

Unlike the decoupling finite-gain lower bound, this result works from the shared side and controls arbitrary chords rather than only moves toward weaker coupling.

## What is not convex in general

The BITA-favored set

\[
\{F>0\}
\]

is a superlevel set of a convex function and need not be convex.

Therefore the theorem is asymmetric:

```text
shared + shared -> every mixture shared
```

is guaranteed, but

```text
BITA + BITA -> every mixture BITA
```

is not guaranteed without stronger assumptions.

That asymmetry is itself a useful topology prediction.

## Empirical consequence

A factorial experiment manipulating two integration channels, or one integration channel plus an independent architecture-cost perturbation, can reserve endpoint states and use interior combinations as held-out convexity tests.

Nested predictions are:

1. `F(interior)` must not exceed the endpoint chord;
2. if both endpoints are shared-favored, no interior state can be BITA-favored;
3. a violation downgrades all convex-coupling critical-budget certificates that rely on the same model family.

## Claim ceiling

The theorem requires a common convex coupling domain, convex `R(lambda)`, and an additive architecture-cost coordinate `K`. If changing `K` also changes the phenotype feasible set or the recovery function, joint convexity need not hold. Population invasion, coexistence and establishment remain PAYOFF questions and are not implied by convex static architecture geometry.
