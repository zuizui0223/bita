# BITA monotone order partial-identification theorem v1

## Purpose

Use sparse multi-channel intervention data to bound the static architecture margin at **unmeasured interventions** using only product-order monotonicity.

This is deliberately weaker than convex interpolation: no convexity, differentiability or parametric coupling model is required. The only structural assumption is that more decoupling in every channel cannot lower the static optimized architecture margin while `K` and context remain fixed.

## Setup

Let intervention amount be

\[
x\in\mathcal X\subset\mathbb R_+^m
\]

and static architecture margin

\[
F(x)=R(\lambda_0-x)-K.
\]

Assume

\[
x\le y
\quad\Longrightarrow\quad
F(x)\le F(y).
\]

Suppose margins are measured at a finite set of interventions

\[
\{(x_i,F_i)\}_{i=1}^N.
\]

For an unmeasured query `x`, define the observed lower and upper order neighborhoods

\[
I_-(x)=\{i:x_i\le x\},
\qquad
I_+(x)=\{i:x\le x_i\}.
\]

## Theorem 1 — exact-data isotonic bounds

Monotonicity implies

\[
F_i\le F(x)
\quad\forall i\in I_-(x)
\]

and

\[
F(x)\le F_j
\quad\forall j\in I_+(x).
\]

Therefore

\[
\boxed{
L_{ord}(x)
\le F(x)\le
U_{ord}(x)
}
\]

with

\[
\boxed{
L_{ord}(x)=\max_{i\in I_-(x)}F_i,
\qquad
U_{ord}(x)=\min_{j\in I_+(x)}F_j.
}
\]

If a neighborhood is empty, the corresponding bound is `-infinity` or `+infinity`.

## Corollary 1a — sign identification without measuring the query

If

\[
L_{ord}(x)>0,
\]

then the query is certified BITA-favored.

If

\[
U_{ord}(x)\le0,
\]

then it is certified shared-favored or exactly on the static boundary.

Otherwise the architecture state at `x` remains unresolved from order information alone.

## Corollary 1b — monotonicity inconsistency certificate

If both neighborhoods are nonempty but

\[
\boxed{L_{ord}(x)>U_{ord}(x),}
\]

then no coordinatewise non-decreasing function can pass through all registered exact margins.

This is a direct model/context audit, not a statistical ambiguity.

## Theorem 2 — interval-valued observations

Suppose each observed margin is known only within a valid interval

\[
F(x_i)\in[\ell_i,u_i].
\]

Then every monotone margin function compatible with those intervals must satisfy

\[
\boxed{
\max_{i\in I_-(x)}\ell_i
\le F(x)\le
\min_{j\in I_+(x)}u_j.
}
\]

Thus uncertainty propagates through the product order without fitting a response surface.

A sufficient inconsistency condition is

\[
\max_{i\in I_-(x)}\ell_i
>
\min_{j\in I_+(x)}u_j.
\]

## Theorem 3 — observed positive and nonpositive closures

Let `P_obs` be observed interventions with certified positive lower margin and let `S_obs` be observed interventions with certified nonpositive upper margin.

Monotonicity expands these observations into certified regions:

\[
\boxed{
\uparrow P_{obs}
=\{x:\exists p\in P_{obs},\ x\ge p\}
}
\]

is BITA-favored, while

\[
\boxed{
\downarrow S_{obs}
=\{x:\exists s\in S_{obs},\ x\le s\}
}
\]

is shared-favored/boundary.

Only the gap between these upward and downward closures requires additional experimentation.

## Corollary 3a — adaptive next-treatment principle

A treatment lying entirely inside an already certified upward or downward closure adds no new architecture-state classification under monotonicity alone.

For state-boundary localization, new treatments should be allocated to the unresolved order frontier between the two closures, unless they are intentionally reserved as falsification/replication checks.

## Relation to convex BITA theory

Order bounds and convexity bounds are complementary:

- **monotonicity** uses comparable treatments and gives product-order lower/upper bounds;
- **convexity** uses mixtures/chords and gives geometric bounds even between non-comparable interventions;
- combining both can only tighten partial identification.

A monotonicity violation is stronger than a convexity miss because the order theorem does not depend on curvature.

## Empirical consequence

A multi-channel causal design can be run adaptively while preserving preregistered logic:

1. seed the design with a small set of extreme/maximal treatments;
2. compute upward positive and downward nonpositive closures;
3. identify unresolved frontier treatments;
4. sample only the frontier treatments needed to locate the static architecture boundary;
5. retain some dominated/interior treatments as explicit falsification checks.

This converts the multichannel criticality problem into a partially ordered boundary-learning problem rather than a full factorial grid by default.

## Claim ceiling

All bounds require matched context, common fitness scale, fixed architecture-cost semantics and genuine coordinatewise decoupling monotonicity. They identify static architecture ordering only. They do not infer invasion, coexistence, establishment, historical accessibility or PAYOFF dynamics.
