# BITA vertex-complete intervention certificate v1

## Purpose

Strengthen the global bang-bang theorem into an exact finite-design certificate.

For a convex recoverable-fitness surface over a compact intervention polytope, the maximum realized recovery over **all** feasible interventions is exactly the maximum recovery among the polytope vertices. Therefore a static architecture crossing is possible somewhere inside the intervention region if and only if at least one vertex crosses.

This converts a continuous intervention search into a finite extreme-treatment design.

## Setup

Let current residual coupling be `lambda_0`, let `P` be any compact convex polytope of feasible decoupling vectors, and define

\[
F(x)=R(\lambda_0-x).
\]

Assume `R` is convex over the corresponding coupling region. Then `F` is convex on `P`.

Let the finite vertex set of `P` be

\[
V(P)=\{v_1,\ldots,v_M\}.
\]

## Theorem 1 — exact vertex maximum identity

Every `x in P` can be expressed as a convex combination of vertices:

\[
x=\sum_j\alpha_jv_j,
\qquad
\alpha_j\ge0,
\qquad
\sum_j\alpha_j=1.
\]

Convexity gives

\[
F(x)
\le
\sum_j\alpha_jF(v_j)
\le
\max_jF(v_j).
\]

Since every vertex belongs to `P`, the reverse inequality is immediate. Therefore

\[
\boxed{
\max_{x\in P}R(\lambda_0-x)
=
\max_{v\in V(P)}R(\lambda_0-v).
}
\]

This is stronger than merely saying an extreme-point maximizer exists: the finite vertex set is **complete** for the global static optimization problem.

## Theorem 2 — static crossing is vertex-complete

Let architecture cost `K` be fixed across the intervention comparison. A static BITA-side crossing is feasible somewhere in `P` if

\[
R(\lambda_0-x)-K>0
\]

for at least one feasible `x`.

By Theorem 1,

\[
\boxed{
\exists x\in P:\ R(\lambda_0-x)>K
\iff
\exists v\in V(P):\ R(\lambda_0-v)>K.
}
\]

Thus no hidden distributed interior intervention can cross if every extreme treatment remains shared-favored.

## Corollary 2a — finite no-cross certificate

If every vertex satisfies

\[
R(\lambda_0-v_j)-K\le0,
\]

then

\[
\boxed{
R(\lambda_0-x)-K\le0
\quad\forall x\in P.
}
\]

This is a global no-cross result over the whole registered intervention polytope.

With interval estimates, if an upper confidence/identification bound for every vertex margin is nonpositive, the same fail-closed no-cross certificate follows under the registered common convex model.

## Corollary 2b — interior treatments become model audits

Because vertices are sufficient for the global maximum, interior interventions are not required to discover a larger static recovery under convexity.

They are instead valuable as held-out convexity checks. For

\[
x=\sum_j\alpha_jv_j,
\]

convexity predicts

\[
\boxed{
F(x)\le\sum_j\alpha_jF(v_j).
}
\]

An interior observation that exceeds the corresponding vertex chord beyond uncertainty falsifies the registered convex recovery model or the comparability of the intervention states.

## Weighted-L1 + box specialization

For

\[
0\le x_i\le\lambda_{0i},
\qquad
a^\top x\le B,
\]

the global bang-bang theorem shows every vertex has all but at most one channel at either

\[
0
\]

or

\[
\lambda_{0i}.
\]

Therefore the exact vertex-complete design consists of saturation patterns plus at most one budget-filling partial channel.

The continuous biological intervention space may be large, but under the theorem its global static optimum is represented by this finite set.

## Relation to local intervention theory

BITA now has three nested intervention levels:

```text
local active penalties c*           -> rank channels / tangent gain
curvature bounds                    -> certified threshold interval
full convex vertex evaluations      -> exact global optimum/crossing over P
```

The strongest level requires more finite treatments but fewer shape assumptions beyond convexity: once every relevant vertex is measured on a common scale, no unmeasured interior treatment can exceed all of them under the model.

## Experimental consequence

For a modest number of coupling channels, a confirmatory generality experiment can prospectively register an intervention polytope and split treatments into:

1. **vertex treatments** — identify the maximum finite recovery and whether any static crossing is possible;
2. **interior hold-outs** — audit convexity and common-state comparability;
3. **mechanism assays** — determine why the winning extreme intervention recovers fitness.

This is especially useful when a full factorial continuum of partial decoupling doses is infeasible.

## Scope limitation

The number of vertices can grow combinatorially with channel count. The theorem removes continuous optimization, not necessarily combinatorial complexity. Dominance, symmetry, mechanistic impossibility or preregistered channel restrictions may reduce the candidate set but require separate justification.

## Claim ceiling

The certificate requires a compact convex intervention polytope, global convexity of `R` across that region, fixed coupling coordinates and fixed `K` for architecture-crossing claims. If interventions change developmental accessibility, architecture cost, baseline fitness semantics or the feasible phenotype set, vertex interpolation can fail. The result concerns static optimized-fitness architecture ordering, not invasion, establishment or PAYOFF dynamics.