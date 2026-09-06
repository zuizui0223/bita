# BITA interval shared-chord identification theorem v1

## Purpose

Make the joint shared-region convexity and strong-convex chord tests fail closed under interval uncertainty. The architecture margin is often estimated with bootstrap or model uncertainty; point estimates should not be allowed to manufacture a convexity violation or a hidden-BITA exclusion.

## Setup

Let the static architecture margin be

\[
F(x)=R(\lambda)-K,
\]

where `x=(lambda,K)` or, at fixed `K`, simply a coupling state. For endpoint states and an interior chord state,

\[
F_0\in[L_0,U_0],\qquad
F_1\in[L_1,U_1],\qquad
F_t\in[L_t,U_t].
\]

Define the convex sag

\[
S=[(1-t)F_0+tF_1]-F_t.
\]

A registered strong-convexity model requires

\[
B_L\le S\le B_U,
\]

with

\[
B_L=\frac{\alpha}{2}t(1-t)d_Q^2,
\qquad
B_U=\frac{\beta}{2}t(1-t)d_Q^2.
\]

## Theorem 1 — sharp marginal identified set for the sag

The sag increases with both endpoint margins and decreases with the interior margin. Therefore

\[
\boxed{S\in[S_L,S_U]}
\]

with

\[
\boxed{
S_L=(1-t)L_0+tL_1-U_t
}
\]

and

\[
\boxed{
S_U=(1-t)U_0+tU_1-L_t.
}
\]

This is the sharp interval from marginal bounds alone.

## Theorem 2 — fail-closed strong-convexity classification

Compare `[S_L,S_U]` with the model-required `[B_L,B_U]`:

- `S_U < B_L` -> `LOWER_BOUND_VIOLATED`;
- `S_L > B_U` -> `UPPER_BOUND_VIOLATED`;
- `[S_L,S_U]` wholly inside `[B_L,B_U]` -> `IDENTIFIED_WITHIN_INTERVALS`;
- otherwise -> `UNRESOLVED`.

For ordinary convexity, `B_L=0`. Thus

\[
\boxed{S_U<0}
\]

robustly rejects convexity: no admissible values inside the supplied intervals can place the interior margin below the endpoint chord.

## Theorem 3 — robust hidden-BITA exclusion from shared endpoints

The shared-favored state is `F<=0`. If endpoint **upper bounds** satisfy

\[
\boxed{U_0\le0,\qquad U_1\le0,}
\]

then every admissible true endpoint pair is shared-favored.

Under the independently accepted convexity model,

\[
F(x_t)\le(1-t)F(x_0)+tF(x_1)
\le(1-t)U_0+tU_1\le0.
\]

Therefore the entire chord is robustly shared-favored and a hidden interior BITA island is excluded.

A conservative segment-wide upper bound is

\[
\boxed{\max(U_0,U_1)\le0.}
\]

This result uses upper bounds because positive `F` is the BITA side.

## Corollary — strong-convex shared basin with interval endpoints

If `alpha>0`, the interior upper bound can be sharpened to

\[
F(x_t)
\le
(1-t)U_0+tU_1
-\frac{\alpha}{2}t(1-t)d_Q^2.
\]

Thus even endpoints whose upper bounds touch zero can imply a strictly negative interior upper bound for every strict interior point.

## Empirical consequence

A three-state coupling or coupling-cost experiment should report:

```text
endpoint architecture-margin intervals
interior architecture-margin interval
possible sag interval [S_L,S_U]
registered sag interval [B_L,B_U]
convexity classification
robust hidden-BITA exclusion status
```

This separates uncertainty in measured static margins from uncertainty in the convexity model itself.

## Claim ceiling

The interval arithmetic uses marginal bounds only and may be conservative if estimates are correlated. A sharper simultaneous region may be substituted only if prospectively justified. Shared endpoint intervals do not establish convexity; the shape assumption remains an independent gate. All conclusions concern static optimized-fitness ordering, not PAYOFF invasion, establishment or coexistence.
