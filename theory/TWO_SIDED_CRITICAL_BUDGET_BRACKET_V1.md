# BITA two-sided critical decoupling-budget bracket v1

## Purpose

Use lower and upper curvature bounds to interval-identify the minimum Euclidean decoupling budget required to cross a static architecture threshold.

This sharpens the one-sided finite-decoupling guarantee into a two-sided critical-budget bracket.

## Setup

At the current coupling state `lambda_0`, let

\[
\delta=K-R(\lambda_0)>0
\]

be the shared-favored architecture deficit and

\[
c=\|\mathbf c_0\|_2,
\qquad
\mathbf c_0=-\nabla R(\lambda_0).
\]

Assume along every gradient-aligned intervention segment up to the relevant crossing that

\[
\alpha I
\preceq
\nabla^2R
\preceq
\beta I,
\qquad
0\le\alpha\le\beta.
\]

Assume the gradient-aligned decoupling move is componentwise feasible over the budgets considered.

Define for curvature `gamma>=0` the positive solution of

\[
c\varepsilon+
\frac{\gamma}{2}\varepsilon^2
=\delta
\]

by

\[
r_\gamma(\delta,c)=
\begin{cases}
\dfrac{\sqrt{c^2+2\gamma\delta}-c}{\gamma}, & \gamma>0,\\[6pt]
\dfrac{\delta}{c}, & \gamma=0,\ c>0,\\[6pt]
+\infty, & \gamma=0,\ c=0.
\end{cases}
\]

## Theorem 1 — critical budget bracket

Let `epsilon_*` be the minimum Euclidean budget for which some feasible decoupling move reaches the static architecture boundary.

The curvature-upper gain envelope implies that no move inside a budget smaller than `r_beta` can cross, while the curvature-lower gain floor along the gradient-aligned move implies that a budget larger than `r_alpha` is sufficient.

Therefore

\[
\boxed{
r_\beta(\delta,c)
\le
\varepsilon_*
\le
r_\alpha(\delta,c).}
\]

Since `alpha<=beta`,

\[
r_\beta\le r_\alpha.
\]

The interval is therefore ordered correctly.

## Corollary 1a — exact quadratic/constant-curvature collapse

If the directional curvature is known exactly and constant,

\[
\alpha=\beta=\gamma,
\]

then

\[
\boxed{
\varepsilon_*=r_\gamma(\delta,c)
}
\]

for the unconstrained gradient-aligned Euclidean problem.

Thus the uncertainty band collapses to a point.

## Corollary 1b — convexity-only upper certificate

If only convexity is known on the lower side,

\[
\alpha=0,
\]

then

\[
\varepsilon_*
\le
\frac{\delta}{c}
\]

when `c>0`, reproducing the tangent sufficient budget.

The lower side remains

\[
\varepsilon_*
\ge
r_\beta.
\]

## Corollary 1c — zero current gradient

If

\[
c=0
\]

but `alpha>0`, curvature alone can guarantee eventual crossing:

\[
\boxed{
\sqrt{\frac{2\delta}{\beta}}
\le
\varepsilon_*
\le
\sqrt{\frac{2\delta}{\alpha}}.
}
\]

If both `c=0` and `alpha=0`, no finite sufficient budget follows from the registered lower information, even though positive curvature allowed by `beta` may still permit a crossing.

## Theorem 2 — monotonicity of the bracket

For fixed `delta` and `c`, `r_gamma` is non-increasing in `gamma`. Stronger guaranteed positive curvature lowers the sufficient budget; a larger allowed upper curvature lowers the budget below which crossing can be ruled out.

For fixed curvature and `c`, both endpoints increase with deficit `delta`.

For fixed deficit and curvature, both endpoints decrease with current active-penalty norm `c`.

Hence the critical intervention is hardest when:

- the current architecture deficit is large;
- active coupling penalties are weak;
- little positive curvature is guaranteed.

## Theorem 3 — width of the intervention uncertainty band

Define

\[
U=r_\alpha-r_\beta\ge0.
\]

`U` measures unresolved higher-order geometry in budget units under the scalar curvature bracket.

- `U=0` when the relevant curvature is exactly known (`alpha=beta`);
- `U` widens as the curvature interval broadens;
- reducing curvature uncertainty contracts the range of budgets in which the model cannot determine the crossing status from bounds alone.

This gives a direct design value for adding intermediate coupling levels: they are useful when they materially tighten `alpha` and `beta` and therefore shrink `U`.

## Empirical consequence

A preregistered multi-level coupling experiment can report three regions:

```text
epsilon < r_beta     static crossing impossible under registered upper curvature
epsilon > r_alpha    static crossing guaranteed under registered lower curvature
r_beta..r_alpha      crossing not decided by the curvature bounds alone
```

The middle region is not statistical uncertainty by itself. It is **structural uncertainty induced by bounded but incompletely known coupling curvature**.

## Claim ceiling

The theorem assumes a common coupling coordinate system, Hessian bounds valid over the relevant intervention region, fixed architecture cost `K`, and feasibility of the gradient-aligned move for the upper certificate. Box constraints or changing feasible phenotype space require constrained optimization. The crossing remains a static optimized-fitness crossing, not PAYOFF invasion or establishment.
