# BITA strong-convex shared-chord sag theorem v1

## Purpose

Strengthen joint shared-region convexity from a sign/topology statement into a quantitative three-point prediction. If the static architecture margin has bounded convex curvature along a coupling-cost chord, interior states must sit a predictable amount **below** the straight endpoint interpolation.

This produces a direct curvature test and a quantitative shared-side buffer between two shared-favored endpoints.

## Setup

Let

\[
F(\lambda,K)=R(\lambda)-K
\]

be the static differentiated-minus-shared architecture margin.

Choose two joint states

\[
x_0=(\lambda_0,K_0),
\qquad
x_1=(\lambda_1,K_1)
\]

and the chord

\[
x_t=(1-t)x_0+t x_1,
\qquad
v=x_1-x_0.
\]

Let

\[
g(t)=F(x_t).
\]

Assume along the segment

\[
\alpha Q\preceq\nabla^2F(x_t)\preceq\beta Q,
\qquad 0\le\alpha\le\beta,
\]

for a preregistered positive-semidefinite intervention metric/curvature reference `Q`.

Because `-K` is affine, these curvature bounds are inherited from `R(lambda)` in the coupling block when the cost coordinate has zero second derivative.

## Theorem 1 — quantitative convex sag

Define the endpoint chord

\[
\ell_F(t)=(1-t)F(x_0)+tF(x_1)
\]

and the convex sag

\[
S_F(t)=\ell_F(t)-F(x_t).
\]

Then

\[
\boxed{
\frac{\alpha}{2}t(1-t)v^TQv
\le S_F(t)\le
\frac{\beta}{2}t(1-t)v^TQv.
}
\]

At the midpoint,

\[
\boxed{
\frac{\alpha}{8}v^TQv
\le
\frac{F(x_0)+F(x_1)}{2}
-F\!\left(\frac{x_0+x_1}{2}\right)
\le
\frac{\beta}{8}v^TQv.
}
\]

Thus strong convexity predicts how far an interior architecture margin must fall below the endpoint chord.

## Corollary 1a — strict shared-side buffer between shared endpoints

If both endpoints are shared-favored,

\[
F(x_0)\le0,
\qquad
F(x_1)\le0,
\]

then

\[
F(x_t)
\le
(1-t)F(x_0)+tF(x_1)
-\frac{\alpha}{2}t(1-t)v^TQv.
\]

If `alpha>0` and the endpoints are on the architecture boundary `F=0`, every strict interior point satisfies

\[
\boxed{F(x_t)<0.}
\]

So a strongly convex recovery landscape produces a genuine shared-favored basin between two boundary points.

## Corollary 1b — fixed-K coupling chord

When `K` is fixed, the same result applies to any coupling chord

\[
\lambda_t=(1-t)\lambda_0+t\lambda_1.
\]

No cost manipulation is required. A factorial or mixture experiment across coupling channels can therefore test the sag theorem directly.

## Theorem 2 — three-point curvature audit

Given endpoint architecture margins and one held-out interior margin, define

\[
\widehat S_F(t)
=[(1-t)\widehat F(x_0)+t\widehat F(x_1)]-\widehat F(x_t).
\]

The registered curvature interval requires

\[
\frac{\alpha}{2}t(1-t)v^TQv
\le\widehat S_F(t)\le
\frac{\beta}{2}t(1-t)v^TQv
\]

after uncertainty propagation.

- negative sag rejects convexity;
- sag below the lower bound rejects the strong-convexity floor;
- sag above the upper bound rejects the curvature ceiling.

This is a direct finite-difference audit of the same coupling geometry used by critical-budget calculations.

## Relation to threshold theory

The chord-sag theorem is not another critical-threshold estimator. It is a shape test for the global convex model that underwrites finite decoupling guarantees, ray criticality and joint shared-region convexity.

A robust violation therefore downgrades those downstream certificates unless a more flexible model is registered.

## Empirical consequence

A minimal advanced BITA design can use two shared-favored endpoint coupling states plus one midpoint mixture. If `K` is constant and the same optimized fitness definition applies, the midpoint provides a direct strong-convexity test without requiring the full coupling surface.

This design is especially useful in a later multi-channel generality system, but can also be used in a focal system if a reproducible graded integration manipulation exists.

## Claim ceiling

The theorem requires the stated Hessian bounds along the full chord, a common feasible phenotype space and an additive `K` coordinate. It concerns static optimized-fitness architecture ordering. Frequency dependence, invasion and establishment remain PAYOFF questions.
