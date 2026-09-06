# BITA finite decoupling gain guarantee v1

## Purpose

Upgrade the local optimal-decoupling rule into a **finite-intervention lower bound** using convexity of recoverable fitness in coupling space.

The result shows that the first-order active-penalty calculation is conservative, not merely heuristic, whenever the registered global convex coupling model applies along the intervention segment.

## Setup

Let

\[
R(\boldsymbol\lambda)
\]

be differentiable, convex and coordinatewise non-increasing in residual-coupling vector `lambda`.

At the current point `lambda_0`, define active penalties

\[
\mathbf c_0
=-\nabla R(\boldsymbol\lambda_0)
\ge0.
\]

Let a finite decoupling intervention be

\[
x\ge0,
\qquad
\boldsymbol\lambda_1=\boldsymbol\lambda_0-x,
\]

with the whole segment between the two points remaining inside the declared coupling domain.

## Theorem 1 — tangent lower bound for finite decoupling

Convexity gives the global tangent inequality

\[
R(y)
\ge
R(x_0)+\nabla R(x_0)^\top(y-x_0).
\]

Set `y=lambda_0-x`. Then

\[
R(\boldsymbol\lambda_0-x)
\ge
R(\boldsymbol\lambda_0)
+(-\mathbf c_0)^\top(-x).
\]

Therefore

\[
\boxed{
R(\boldsymbol\lambda_0-x)-R(\boldsymbol\lambda_0)
\ge
\mathbf c_0^\top x.
}
\]

So the current active-penalty vector supplies a **guaranteed minimum recovery** for any finite decoupling move in the convex model.

Because the slope can become steeper as coupling is weakened, the realized gain may exceed the initial tangent prediction.

## Corollary 1a — norm-budget guaranteed gain

Suppose the intervention budget is

\[
\|x\|_p\le\varepsilon
\]

and the unconstrained dual-norm optimizer is feasible componentwise (`x<=lambda_0`). Let `q` be the Holder-dual exponent.

Choose the linear-recovery-maximizing plan from the budget-duality theorem. Then

\[
\mathbf c_0^\top x^*
=
\varepsilon\|\mathbf c_0\|_q.
\]

The finite realized recovery obeys

\[
\boxed{
R(\lambda_0-x^*)-R(\lambda_0)
\ge
\varepsilon\|\mathbf c_0\|_q.
}
\]

Thus the previously local dual-norm value is a certified finite-intervention floor under global convexity.

## Theorem 2 — sufficient decoupling to cross from BALANCE-side to BITA-side

Let architecture cost `K` remain fixed during the decoupling intervention and suppose the current static architecture deficit is

\[
\delta
=
K-R(\boldsymbol\lambda_0)
>0.
\]

This is a shared-favored/BALANCE-side architecture comparison.

After finite decoupling `x`,

\[
R(\lambda_0-x)-K
\ge
-\delta+\mathbf c_0^\top x.
\]

Therefore the condition

\[
\boxed{
\mathbf c_0^\top x>\delta
}
\]

is sufficient to guarantee

\[
R(\lambda_0-x)-K>0,
\]

so the static architecture ordering crosses to the BITA side.

Under a feasible `Lp` budget plan, the simple sufficient condition is

\[
\boxed{
\varepsilon\|\mathbf c_0\|_q>\delta.
}
\]

This is a conservative **decoupling-to-differentiation certificate**.

It is not a necessary condition: curvature can make the exact finite gain larger than the tangent floor.

## Corollary 2a — minimum certified budget

Ignoring componentwise saturation for the moment, a sufficient budget is

\[
\boxed{
\varepsilon_{\rm cert}
>
\frac{\delta}{\|\mathbf c_0\|_q}.
}
\]

The required certified budget falls when active coupling penalties are large in the relevant dual norm.

This differs from the earlier adverse-coupling robustness bound. There the question was how much **more coupling** is required to erase an existing BITA advantage; here the question is how much **decoupling** is sufficient to overcome a current architecture deficit.

## Theorem 3 — exact gain as accumulated active penalty

Along the straight decoupling path

\[
\lambda(t)=\lambda_0-tx,
\qquad t\in[0,1],
\]

the path-integral theorem gives

\[
\boxed{
R(\lambda_0-x)-R(\lambda_0)
=
\int_0^1
\mathbf c(\lambda_0-tx)^\top x\,dt.
}
\]

Convexity implies that this directional active penalty is non-decreasing as `t` increases along the decoupling path, yielding the tangent lower bound above.

The gap

\[
\text{exact gain}-\mathbf c_0^\top x
\]

measures the contribution of coupling curvature over the intervention.

## Empirical consequence

A BITA experiment that can estimate current active coupling penalties can preregister three nested predictions:

1. **local ranking** — which coupling channels should be targeted first;
2. **finite gain floor** — minimum recoverable-fitness gain expected from a declared finite intervention;
3. **transition certificate** — whether the planned intervention is strong enough, under the model, to guarantee crossing the static architecture threshold.

If the observed finite gain falls below the tangent floor beyond uncertainty, at least one registered assumption is violated: the inferred `c_0` is wrong, the feasible/baseline landscape changed, `K` changed during the intervention, or the convex common-coupling model is inadequate.

## Saturation and feasibility

The dual-norm optimizer may request more decoupling in a channel than its current coupling allows. If

\[
x_i>\lambda_{0i},
\]

that plan is infeasible and must be solved with box constraints

\[
0\le x_i\le\lambda_{0i}.
\]

The tangent lower bound remains valid for every feasible plan, but the closed-form unconstrained dual-norm optimum must then be replaced by the corresponding constrained optimization.

## Claim ceiling

The guarantee requires convex `R` over the entire intervention segment, a common feasible phenotype space, non-negative coupling penalties, and fixed architecture cost `K` for the transition certificate. It concerns static optimized fitness, not population invasion or establishment; PAYOFF remains separate.
