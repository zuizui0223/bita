# BITA global bang-bang decoupling theorem v1

## Purpose

Move beyond optimizing the local linear recovery floor. Under the registered global convex coupling model, ask for the **actual finite decoupling intervention** that maximizes recoverable fitness under a linear intervention budget and biological box constraints.

The result is structural: there always exists a globally optimal intervention at a vertex of the feasible intervention polytope. Consequently, under a weighted-L1 budget, all but at most one coupling channel are either untouched or fully decoupled.

This is a global static theorem. It does not say which vertex wins without additional information about the full recovery surface.

## Setup

Let residual coupling be

\[
\boldsymbol\lambda_0\ge0
\]

and let a feasible finite decoupling move be

\[
x\in\mathbb R_+^m,
\qquad
0\le x_i\le\lambda_{0i}.
\]

Let per-unit intervention prices be

\[
a_i>0
\]

and impose a weighted-L1 budget

\[
\sum_i a_i x_i\le B.
\]

The feasible intervention polytope is

\[
\mathcal P_B
=
\left\{x:
0\le x_i\le\lambda_{0i},
\;a^\top x\le B
\right\}.
\]

Assume recoverable fitness

\[
R(\boldsymbol\lambda)
\]

is convex on the whole registered coupling box. The realized post-intervention objective is

\[
F(x)=R(\boldsymbol\lambda_0-x).
\]

Because composition with an affine map preserves convexity, `F` is convex on `P_B`.

## Theorem 1 — a global finite-recovery optimum exists at an extreme point

The compact polytope `P_B` has at least one maximizer of `F`.

Suppose a maximizer `x*` is not extreme. Then it can be written

\[
x^*=\theta y+(1-\theta)z,
\qquad
0<\theta<1,
\]

with distinct feasible `y,z`.

Convexity gives

\[
F(x^*)
\le
\theta F(y)+(1-\theta)F(z).
\]

Therefore at least one of `y,z` has objective value no smaller than `F(x*)` and is also a maximizer. Repeating this reduction on a finite-dimensional polytope reaches an extreme-point maximizer.

Hence

\[
\boxed{
\text{there exists a globally optimal finite decoupling intervention at a vertex of }\mathcal P_B.
}
\]

## Theorem 2 — weighted-L1 box vertices are bang-bang up to one channel

At an extreme point of

\[
0\le x_i\le\lambda_{0i},
\qquad
a^\top x\le B,
\]

at most one coordinate can satisfy

\[
0<x_i<\lambda_{0i}.
\]

Proof: if two coordinates `i,j` are both strictly inside their bounds, then for sufficiently small `epsilon` the perturbation

\[
h_i=\varepsilon/a_i,
\qquad
h_j=-\varepsilon/a_j
\]

preserves `a^T x` and remains inside both box constraints in both signs. Thus the point lies on a nontrivial feasible line segment and is not extreme.

If the budget inequality is slack, even one partial coordinate can be perturbed independently, so every coordinate must be at a box endpoint.

Therefore there exists a global optimizer with the form

\[
\boxed{
 x_i\in\{0,\lambda_{0i}\}
\text{ for all but at most one channel.}
}
\]

This is the **bang-bang decoupling principle** for global convex recovery under a linear intervention budget.

## Corollary 2a — finite global optimization reduces to saturation patterns

The actual gain-maximizing finite intervention need not be found by searching the full continuous box. It is sufficient in principle to compare extreme candidates consisting of:

- a subset of channels fully decoupled;
- a subset left untouched;
- at most one remaining channel partially decoupled to exhaust the budget.

The number of candidate saturation patterns can still be combinatorial, but the continuous optimization problem has a sparse structural certificate.

## Theorem 3 — this does not imply current-gradient greedy order

The existing box-constrained allocation theorem optimizes the certified linear floor

\[
\mathbf c_0^\top x
\]

and therefore saturates channels in descending current efficiency

\[
\eta_i=c_{0i}/a_i.
\]

The present theorem optimizes the **actual convex finite objective**

\[
R(\lambda_0-x).
\]

Convexity permits marginal recovery to increase as a channel is decoupled. Cross-channel curvature can also change relative values. Therefore the global winning vertex need not follow the initial-gradient greedy ordering.

Hence

\[
\boxed{
\text{local greedy saturation}\neq\text{global bang-bang identity selection}
}
\]

without extra assumptions such as stable marginal ordering or a registered separable form.

## Corollary 3a — a diagnostic for model failure

Under the declared convex static model and weighted-L1 intervention geometry, there must exist an extreme intervention whose recovery is at least as large as any distributed interior allocation with the same or lower budget.

Therefore, if a carefully measured distributed intervention with two or more genuinely partial channels reproducibly outperforms **every feasible extreme candidate** after uncertainty is accounted for, at least one assumption is wrong:

- the recovery surface is not convex over the intervention region;
- the feasible state space changes with the intervention;
- intervention costs are not actually linear-L1;
- architecture cost or another baseline term changes across interventions;
- the registered coupling coordinates omit a relevant state variable.

## Example — symmetric convex recovery favors a vertex

Let two coupling channels start at `(1,1)` and

\[
R(\lambda_1,\lambda_2)
=e^{-\lambda_1}+e^{-\lambda_2}.
\]

This function is convex and decreasing in each coupling coordinate.

Under

\[
x_1+x_2\le B<1,
\]

symmetry makes the two extreme allocations

\[
(B,0),\qquad(0,B)
\]

equivalent. A split allocation `(B/2,B/2)` has lower recovery because the objective as a function of `x` is convex, not concave.

Thus the global theorem can favor concentrated finite decoupling even when the local gradients are initially identical.

## Relation to intervention-budget duality

Budget geometry determines qualitative intervention structure:

```text
local linear objective + L1 budget   -> greedy saturation by c_i/a_i
actual global convex R + L1 box      -> an optimum exists at a bang-bang vertex
local linear objective + L2 budget   -> distributed proportional allocation
```

The last row does not contradict the second because the feasible geometry is different: an L2 ball has a curved boundary rather than the weighted-L1 polytope considered here.

## Architecture crossing

If the goal is not maximum recovery but crossing

\[
R(\lambda_0-x)-K>0,
\]

then searching the bang-bang extreme candidates also supplies a global finite-intervention route under the same assumptions. If no feasible extreme point crosses, no distributed interior intervention can cross with greater recovery under the same budget.

This is stronger than the tangent lower-bound certificate when enough of the finite recovery surface is known to compare extreme candidates.

## Claim ceiling

The theorem guarantees existence of an extreme-point optimizer; it does not identify the winning vertex from local derivatives alone. It requires global convexity of `R` on the entire feasible intervention polytope, fixed coupling coordinates and a weighted-L1 linear budget with box constraints. Nonlinear intervention costs, path-dependent accessibility, changing `K`, or nonconvex recovery can invalidate bang-bang optimality. The result concerns static optimized fitness, not invasion, coexistence, or PAYOFF dynamics.