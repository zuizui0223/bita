# BITA metric critical decoupling-budget bracket v1

## Purpose

Generalize the Euclidean two-sided critical-budget bracket to an arbitrary positive-definite intervention-cost metric.

This unifies the earlier optimal-decoupling metric with the second-order finite-gain bounds.

## Setup

Let intervention cost be measured by

\[
\|x\|_Q
=
\sqrt{x^\top Qx},
\qquad Q\succ0.
\]

At current coupling state `lambda_0`, define

\[
\delta=K-R(\lambda_0)>0,
\qquad
\mathbf c_0=-\nabla R(\lambda_0).
\]

The dual metric norm of the active-penalty vector is

\[
\boxed{
 c_Q
 =
 \sqrt{\mathbf c_0^\top Q^{-1}\mathbf c_0}.
}
\]

Assume the Hessian is bounded relative to the intervention metric throughout the relevant region:

\[
\boxed{
\alpha Q
\preceq
\nabla^2R(\lambda)
\preceq
\beta Q,
\qquad 0\le\alpha\le\beta.
}
\]

## Theorem 1 — metric finite-gain bracket

For any feasible decoupling move `x`,

\[
\boxed{
\mathbf c_0^\top x
+
\frac{\alpha}{2}\|x\|_Q^2
\le
\Delta R(x)
\le
\mathbf c_0^\top x
+
\frac{\beta}{2}\|x\|_Q^2.
}
\]

This is the coordinate-invariant version of the scalar Euclidean curvature bracket.

## Theorem 2 — extremal linear gain under a Q-budget

For

\[
\|x\|_Q\le\varepsilon,
\]

Cauchy-Schwarz in the `Q` / `Q^{-1}` dual pair gives

\[
\mathbf c_0^\top x
\le
\varepsilon c_Q.
\]

Equality is attained by the metric-aligned move

\[
\boxed{
 x_Q^*
 =
 \varepsilon
 \frac{Q^{-1}\mathbf c_0}{c_Q}
}
\]

when that move is componentwise feasible.

## Theorem 3 — metric critical-budget bracket

Define

\[
r_\gamma(\delta,c_Q)
\]

as the nonnegative solution to

\[
c_Q\varepsilon+
\frac{\gamma}{2}\varepsilon^2
=
\delta.
\]

Explicitly,

\[
r_\gamma=
\begin{cases}
\dfrac{\sqrt{c_Q^2+2\gamma\delta}-c_Q}{\gamma}, & \gamma>0,\\[6pt]
\dfrac{\delta}{c_Q}, & \gamma=0,\ c_Q>0,\\[6pt]
+\infty, & \gamma=0,\ c_Q=0.
\end{cases}
\]

Let `epsilon_Q*` be the minimum `Q`-metric budget needed for a static crossing. Then

\[
\boxed{
 r_\beta(\delta,c_Q)
 \le
 \varepsilon_Q^*
 \le
 r_\alpha(\delta,c_Q)
}
\]

provided the metric-aligned sufficient move is feasible.

Thus the same two-sided critical-budget geometry survives arbitrary linear rescaling and correlation of intervention costs.

## Corollary 3a — reparameterization invariance

Under an invertible linear change of coupling coordinates

\[
\tilde\lambda=A\lambda,
\]

with the intervention metric transformed consistently, the scalar quantities

\[
\delta,
\qquad
c_Q,
\qquad
\varepsilon_Q^*
\]

are invariant.

Therefore the critical-budget bracket is not an artifact of whether coupling variables are measured in millimeters, standardized units, biochemical activity units, or another invertibly related coordinate system.

## Corollary 3b — exact metric-quadratic collapse

If the recovery Hessian is exactly proportional to the intervention metric,

\[
\nabla^2R=\gamma Q
\]

along the relevant aligned path, then

\[
\alpha=\beta=\gamma
\]

and

\[
\boxed{
\varepsilon_Q^*=r_\gamma(\delta,c_Q)
}
\]

for the unconstrained metric-aligned problem.

## Theorem 4 — experimental design value of the metric

The quantity

\[
\boxed{c_Q=\sqrt{\mathbf c_0^\top Q^{-1}\mathbf c_0}}
\]

is the current recoverable-fitness gradient measured per unit intervention cost.

A larger `c_Q` lowers both critical-budget endpoints. Therefore two systems with identical biological coupling gradients can have different practical ease of decoupling because the intervention/developmental cost geometry differs.

This distinguishes:

```text
biological sensitivity to coupling      c_0
intervention accessibility / cost       Q
recoverable gain per accessible effort  c_Q
```

## Empirical consequence

A BITA experiment with several manipulable coupling channels can preregister a metric `Q` from intervention difficulty, developmental covariance, or another justified cost model. The theory then supplies:

- an optimal local intervention direction `Q^-1 c_0`;
- a finite gain bracket;
- a two-sided static crossing-budget interval in the same metric.

## Claim ceiling

The metric must be declared independently of the desired result; choosing `Q` post hoc to make a favored intervention look efficient is circular. Hessian bounds must hold relative to the same `Q` over the relevant intervention region. Componentwise saturation and changing architecture cost require constrained extensions. The result is static BITA theory, not PAYOFF invasion dynamics.
