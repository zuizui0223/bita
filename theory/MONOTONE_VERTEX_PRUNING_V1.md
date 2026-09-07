# BITA monotone vertex-pruning theorem v1

## Purpose

Reduce the number of intervention vertices that must be evaluated after the existing vertex-complete theorem.

The current BITA theory already shows that, for a compact convex intervention polytope `P` and convex recoverable-fitness surface, a static recovery maximum occurs at a vertex. The present result adds the biological monotonicity of decoupling: more decoupling in every channel cannot reduce recoverable fitness. Under that extra structure, any vertex that is componentwise dominated by another vertex is mathematically irrelevant to the global static optimum and to crossing feasibility.

## Setup

Let the decoupling intervention be

\[
x\in P\subset\mathbb R_+^m,
\]

with residual coupling

\[
\lambda=\lambda_0-x.
\]

Define

\[
F(x)=R(\lambda_0-x).
\]

Assume:

1. `P` is nonempty, compact and convex;
2. `R` is convex in residual-coupling space on the registered domain;
3. `R` is coordinatewise non-increasing in `lambda`.

Then `F` is convex and coordinatewise non-decreasing in `x`.

## Definition — intervention dominance

For two interventions `x,y`, say `y` dominates `x` if

\[
y_i\ge x_i\quad\forall i,
\]

with strict inequality in at least one coordinate.

For vertices, call a vertex **Pareto-maximal** if no other vertex dominates it.

## Theorem 1 — dominated vertices can be pruned

If vertex `v` is dominated by another vertex `u`, then monotonicity gives

\[
F(u)\ge F(v).
\]

Therefore removing `v` cannot lower the maximum recoverable fitness over the vertex set.

By repeatedly removing dominated vertices,

\[
\boxed{
\max_{v\in\operatorname{Vert}(P)}F(v)
=
\max_{v\in\operatorname{MaxVert}(P)}F(v),
}
\]

where `MaxVert(P)` is the set of componentwise Pareto-maximal vertices.

## Theorem 2 — exact static crossing certificate on maximal vertices

The existing vertex-complete theorem gives

\[
\max_{x\in P}F(x)
=
\max_{v\in\operatorname{Vert}(P)}F(v).
\]

Combining with Theorem 1,

\[
\boxed{
\max_{x\in P}F(x)
=
\max_{v\in\operatorname{MaxVert}(P)}F(v).
}
\]

For fixed architecture cost `K`, a BITA-side static crossing is feasible somewhere in `P` iff at least one Pareto-maximal vertex satisfies

\[
\boxed{F(v)>K.}
\]

Thus dominated vertices do not need to be executed merely to certify the global static crossing ceiling.

## Corollary 2a — box intervention

For a full box

\[
0\le x_i\le b_i,
\]

there is a unique componentwise maximal vertex

\[
x=b.
\]

Hence monotonicity alone implies

\[
\max_{x\in P}F(x)=F(b).
\]

Under a pure box with no competing resource budget, the fully decoupled corner is the only vertex required for the global static optimum claim. Interior and partially decoupled treatments remain valuable for mechanism, curvature and model checks, not for locating a larger static recovery.

## Corollary 2b — weighted-L1 budget

For

\[
P=\{x:0\le x\le b,\;a^\top x\le B\},
\]

vertices with unused budget that can be increased in at least one unsaturated channel are not Pareto-maximal. Candidate global optima therefore lie among budget-saturated and/or fully box-saturated extreme points.

This prunes the existing bang-bang candidate set further whenever some extreme points are componentwise dominated by others.

## Theorem 3 — dominance pruning does not require convexity

The pairwise pruning statement

\[
y\ge x\Rightarrow F(y)\ge F(x)
\]

uses monotonicity only.

Convexity is needed to reduce the entire continuous polytope to vertices. Therefore the logic separates cleanly:

```text
monotonicity -> remove dominated interventions
convexity -> restrict continuous search to vertices
both -> evaluate only Pareto-maximal vertices
```

## Empirical consequence

A preregistered multi-channel BITA experiment can now classify intervention treatments into:

1. **maximal vertices** — required for exact static recovery/crossing search under the model;
2. **dominated vertices** — unnecessary for locating a larger static recovery;
3. **interior treatments** — useful as held-out convexity/path/mechanism audits.

This can reduce confirmatory treatment count without weakening the registered static certificate.

## Negative diagnostic

If a dominated intervention empirically produces higher matched optimized fitness than its dominating intervention beyond uncertainty, the monotone coupling model is violated. Possible causes include:

- the stronger decoupling changes architecture cost `K` or baseline fitness;
- intervention side effects alter the feasible phenotype space;
- one nominal decoupling coordinate is not actually monotone;
- context matching failed.

## Claim ceiling

This theorem concerns static optimized recoverable fitness under a fixed intervention definition. It does not imply that the most decoupled architecture invades, persists, or is evolutionarily reachable. Those population-game questions remain PAYOFF. Dominance comparisons also require interventions to be comparable on the same context and fitness scale.
