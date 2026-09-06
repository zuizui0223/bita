# BITA finite decoupling effective-curvature theorem v1

## Purpose

Convert the Bregman curvature dividend from one finite decoupling move into an exact **weighted-average coupling curvature** along that move.

This is the inverse counterpart of the second-order gain bounds: rather than assuming curvature to predict gain, use observed finite gain beyond the tangent term to recover an integrated curvature quantity.

## Setup

Let

\[
\lambda_1=\lambda_0-x,
\qquad x\ne0,
\]

be a registered feasible decoupling move. The recoverable-fitness gain decomposes as

\[
\Delta R
=\mathbf c_0^\top x+\mathcal C_R(x),
\]

where

\[
\mathcal C_R(x)
=\int_0^1(1-t)
\,x^\top\nabla^2R(\lambda_0-tx)x\,dt
\ge0.
\]

Register a positive-definite coupling/intervention metric `Q` and let

\[
\|x\|_Q^2=x^\top Qx>0.
\]

Define instantaneous normalized directional curvature

\[
\kappa_Q(t)
=
\frac{x^\top\nabla^2R(\lambda_0-tx)x}
{x^\top Qx}.
\]

## Definition — finite effective coupling curvature

Define

\[
\boxed{
\kappa^{R}_{\rm eff,Q}
=
\frac{2\mathcal C_R(x)}
{x^\top Qx}
=
\frac{2[\Delta R-\mathbf c_0^\top x]}
{x^\top Qx}.
}
\]

## Theorem 1 — weighted-average identity

Substitution yields

\[
\boxed{
\kappa^{R}_{\rm eff,Q}
=
2\int_0^1(1-t)\kappa_Q(t)\,dt.
}
\]

Because `2(1-t)` integrates to one on `[0,1]`, this is a genuine weighted average of the directional Hessian curvature along the decoupling path, weighted toward the starting coupling state.

## Corollary 1a — curvature-range identification

If along the segment

\[
\alpha\le\kappa_Q(t)\le\beta,
\]

then

\[
\boxed{
\alpha
\le
\kappa^{R}_{\rm eff,Q}
\le
\beta.
}
\]

Thus one finite intervention does not identify the full curvature function but does identify one exact weighted average of it.

## Corollary 1b — constant-curvature case

If

\[
\nabla^2R=\kappa_0 Q
\]

along the whole move, then

\[
\boxed{
\kappa^{R}_{\rm eff,Q}=\kappa_0.
}
\]

So the quadratic/constant-curvature model can be estimated from only a baseline directional slope and one finite endpoint gain.

## Theorem 2 — threshold-refinement use

Suppose the current static architecture deficit is

\[
\delta=K-R(\lambda_0)>0
\]

with fixed `K`. If the finite move has measured effective curvature `kappa_eff`, then a constant-curvature surrogate along the same metric-normalized direction predicts gain

\[
\Delta R_{sur}(s)
=c_Qs+
\frac12\kappa^{R}_{\rm eff,Q}s^2,
\]

where `s=||x||_Q` and `c_Q` is the current tangent gain per unit metric distance in that direction.

Its zero-crossing estimate solves

\[
c_Qs+
\frac12\kappa^{R}_{\rm eff,Q}s^2
=\delta.
\]

This is an **interpolation summary**, not a certified threshold unless constant curvature is separately justified. The certified lower/upper budget bounds remain those derived from valid global curvature bounds.

## Corollary 2a — curvature-dividend fraction

The curvature share of observed finite gain can be written

\[
\phi_C
=
\frac{\frac12\kappa^{R}_{\rm eff,Q}\|x\|_Q^2}
{\mathbf c_0^\top x+
\frac12\kappa^{R}_{\rm eff,Q}\|x\|_Q^2}.
\]

Thus `phi_C` increases with finite effective curvature and intervention length relative to the baseline tangent contribution.

## Empirical consequence

A graded coupling experiment can recover `kappa_eff` from:

1. baseline directional active penalty `c_0^T x`;
2. finite optimized-fitness gain `Delta R`;
3. registered intervention metric length `x^T Q x`.

No full Hessian reconstruction is required.

Nested checks become:

```text
kappa_eff < 0 beyond uncertainty -> convex coupling model rejected
kappa_eff ~= 0                  -> approximately affine recovery over the move
kappa_eff > 0                   -> finite acceleration of recovery under decoupling
```

Repeating this for adjacent finite moves can reveal whether effective coupling curvature itself rises or falls as decoupling proceeds.

## Relation to SCH

The algebraic weighted-average form resembles SCH's finite weight effective curvature, but the biological objects are different:

- SCH curvature is curvature of optimized **conflict load in functional-weight space**;
- BITA curvature is curvature of **recoverable fitness in residual-coupling space**.

They must not be merged into one estimand merely because both are Bregman/tangent-gap quantities.

## Claim ceiling

The result requires a differentiable convex `R` on the full intervention segment, fixed interpretation of the coupling coordinates and a preregistered metric `Q`. It identifies directional integrated curvature, not the complete Hessian or a historical evolutionary rate. Static architecture crossing remains distinct from PAYOFF invasion and establishment.
