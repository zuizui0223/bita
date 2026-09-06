# BITA decoupling Bregman curvature-dividend theorem v1

## Purpose

Give an exact finite-intervention decomposition of recoverable-fitness gain under coupling release.

The existing BITA results show that convexity makes the current active coupling-penalty vector a guaranteed finite-gain floor. The present theorem identifies the **entire gap above that floor** as a nonnegative Bregman curvature term.

This separates two sources of gain from a finite decoupling intervention:

1. the gain predicted by the coupling pressure already active at the starting state;
2. additional gain created because the optimized phenotype continues to reorganize as coupling is released.

## Setup

Let

\[
R(\boldsymbol\lambda)
\]

be differentiable and convex on a declared coupling domain. The residual-coupling vector is `lambda` and the current point is `lambda_0`.

Define the active coupling-penalty vector

\[
\mathbf c_0=-\nabla R(\boldsymbol\lambda_0)\ge0.
\]

A feasible finite decoupling move is

\[
x\ge0,
\qquad
\boldsymbol\lambda_1=\boldsymbol\lambda_0-x.
\]

Write total recovered fitness as

\[
\Delta R
=R(\lambda_1)-R(\lambda_0).
\]

## Definition — curvature dividend

For a convex differentiable function, the Bregman divergence is

\[
D_R(y,x)
=R(y)-R(x)-\nabla R(x)^\top(y-x).
\]

For the decoupling move above, define

\[
\boxed{
\mathcal C_R(x)
=D_R(\lambda_0-x,\lambda_0).
}
\]

Because `R` is convex,

\[
\boxed{\mathcal C_R(x)\ge0.}
\]

We call this the **decoupling curvature dividend**.

## Theorem 1 — exact finite-gain decomposition

Substituting `y=lambda_0-x` gives

\[
\mathcal C_R(x)
=R(\lambda_0-x)-R(\lambda_0)
-\nabla R(\lambda_0)^\top(-x).
\]

Since `-grad R(lambda_0)=c_0`, this is

\[
\boxed{
\Delta R
=\mathbf c_0^\top x
+\mathcal C_R(x).
}
\]

Thus the tangent lower bound is not merely an inequality. The exact realized finite recovery equals

```text
current active coupling pressure contribution
+
nonnegative curvature dividend
```

with no remainder.

## Corollary 1a — affine criterion

\[
\boxed{\mathcal C_R(x)=0}
\]

whenever `R` is affine along the intervention segment.

If `R` is strictly convex along the nonzero direction `x`, then

\[
\boxed{\mathcal C_R(x)>0.}
\]

So a positive dividend is the finite signature of curvature beyond the local coupling-pressure term.

## Theorem 2 — Hessian integral form

If `R` is twice continuously differentiable along the segment,

\[
\boxed{
\mathcal C_R(x)
=
\int_0^1(1-t)
\,x^\top\nabla^2R(\lambda_0-tx)x\,dt.
}
\]

Therefore the curvature dividend is accumulated positive coupling-space curvature along the actual decoupling path.

This identity recovers the existing second-order bounds immediately. If

\[
A\preceq\nabla^2R\preceq B
\]

along the segment, then

\[
\boxed{
\frac12x^\top A x
\le
\mathcal C_R(x)
\le
\frac12x^\top B x.
}
\]

## Definition — curvature share of recovered fitness

When `Delta R>0`, define

\[
\boxed{
\phi_C
=
\frac{\mathcal C_R(x)}{\Delta R}.
}
\]

For a decoupling move with `c_0^T x>=0`, convexity implies

\[
\boxed{0\le\phi_C\le1.}
\]

Interpretation:

- `phi_C=0`: all recovery was already predicted by the starting coupling pressure; the recovery surface is affine along the move;
- `0<phi_C<1`: both current pressure and continuing phenotypic reorganization contribute;
- `phi_C=1`: the starting directional penalty is zero and all observed gain appears through curvature away from the start.

`phi_C` is a decomposition of optimized-fitness recovery, not a historical fraction of evolutionary causation.

## Theorem 3 — exact static-crossing decomposition

Suppose architecture cost `K` is fixed and the current shared-favored deficit is

\[
\delta=K-R(\lambda_0)>0.
\]

After decoupling, BITA-side static ordering occurs exactly when

\[
R(\lambda_0-x)-K>0.
\]

Using Theorem 1,

\[
\boxed{
\mathbf c_0^\top x
+\mathcal C_R(x)
>\delta
}
\]

is the exact crossing condition.

This clarifies the earlier sufficient certificate:

\[
\mathbf c_0^\top x>\delta
\]

ignores the curvature dividend and is therefore conservative.

A crossing below the tangent-only certified budget is not anomalous if a positive curvature dividend supplies the missing gain.

## Corollary 3a — observed crossing surplus

Define

\[
S_C
=\Delta R-\mathbf c_0^\top x.
\]

Under the registered convex model,

\[
\boxed{S_C=\mathcal C_R(x)\ge0.}
\]

Thus endpoint fitness and a baseline local-gradient estimate identify the total curvature dividend directly, even without resolving the full Hessian matrix.

A significantly negative `S_C` after uncertainty propagation rejects at least one registered assumption.

## Relation to the path-integral theorem

The existing path-integral identity gives

\[
\Delta R
=
\int_0^1
\mathbf c(\lambda_0-tx)^\top x\,dt.
\]

The Bregman decomposition therefore yields

\[
\boxed{
\mathcal C_R(x)
=
\int_0^1
[\mathbf c(\lambda_0-tx)-\mathbf c_0]^\top x\,dt.
}
\]

So the curvature dividend is exactly the accumulated increase in active directional coupling pressure encountered as decoupling proceeds.

## Empirical consequence

A graded coupling experiment does not need a full multidimensional Hessian to estimate this quantity. It needs:

1. a same-context baseline estimate of the directional active penalty `c_0^T x`;
2. a registered finite decoupling move `x`;
3. the endpoint optimized-fitness recovery `Delta R`.

Then

\[
\widehat{\mathcal C}_R
=\widehat{\Delta R}
-\widehat{\mathbf c_0^\top x}.
\]

Nested empirical tests become:

```text
C_R < 0 beyond uncertainty   -> convex/common-landscape model fails
C_R ~= 0                    -> locally affine recovery over this move
C_R > 0                     -> finite curvature/reorganization contributes
```

This can be used before attempting full coupling-channel curvature reconstruction.

## Claim ceiling

The decomposition is exact for the registered optimized-fitness value function `R`. Interpreting `C_R` biologically as phenotypic reorganization requires the common feasible-state and fixed-baseline assumptions used to derive that value function. If the intervention changes architecture cost `K`, feasible phenotype space, or baseline fitness landscape, the quantity is no longer a pure coupling-curvature dividend. The static crossing result is not a PAYOFF invasion or establishment result.
