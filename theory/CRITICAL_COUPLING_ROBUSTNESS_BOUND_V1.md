# BITA critical-coupling robustness bound v1

## Purpose

Turn the general convex coupling-recovery theorem into a directly interpretable **distance-to-threshold bound**.

Let recoverable compromise loss under residual-coupling strength `lambda` be

\[
R(\lambda),
\]

with fixed architecture cost

\[
K\ge0,
\]

and architecture margin

\[
\Delta(\lambda)=R(\lambda)-K.
\]

Assume the general BITA coupling theorem conditions so that `R` is non-increasing and convex in `lambda`. At a regular point `lambda_0`, let

\[
R'(\lambda_0)=-c_0,
\qquad c_0\ge0,
\]

where `c_0=c(u^*_{lambda_0})` is the active residual-coupling penalty from the envelope theorem.

Suppose the differentiated architecture is currently favored:

\[
m_0=R(\lambda_0)-K>0.
\]

## Theorem 1 — tangent lower bound on distance to the critical coupling

Convexity gives the supporting-line inequality

\[
R(\lambda)
\ge
R(\lambda_0)+R'(\lambda_0)(\lambda-\lambda_0)
=R(\lambda_0)-c_0(\lambda-\lambda_0).
\]

If a later critical point `lambda_c>lambda_0` exists with

\[
R(\lambda_c)=K,
\]

then

\[
K
\ge
R(\lambda_0)-c_0(\lambda_c-\lambda_0).
\]

Therefore, for `c_0>0`,

\[
\boxed{
\lambda_c-\lambda_0
\ge
\frac{m_0}{c_0}.
}
\]

The current net architecture margin divided by the active coupling penalty gives a **conservative lower bound** on how much additional coupling is required before the differentiated state can lose its static advantage.

This is not a linear approximation to the threshold. Convexity makes it a one-sided bound: because the recovery curve can flatten as coupling increases, the true crossing cannot occur sooner than the tangent crossing.

## Corollary 1a — zero local coupling penalty implies no later crossing under the declared smooth model

If

\[
c_0=0
\]

then

\[
R'(\lambda_0)=0.
\]

For a convex function, future derivatives cannot be smaller than the current derivative. Since `R` is also non-increasing, every future derivative must remain zero wherever differentiable. Hence `R` is constant to the right under the declared regular model and a lower critical crossing cannot occur.

So if `m_0>0` and `c_0=0`,

\[
\boxed{\text{no finite later critical coupling exists under the stated assumptions}.}
\]

A future crossing in real data would then imply that another quantity changed: feasible phenotype set, baseline landscape, architecture cost, or the coupling model itself.

## Theorem 2 — critical coupling is a decreasing convex function of architecture cost

Assume `R` is twice differentiable and strictly decreasing around the unique critical coupling defined implicitly by

\[
R(\lambda_c(K))=K.
\]

First differentiation gives

\[
\boxed{
\frac{d\lambda_c}{dK}
=
\frac{1}{R'(\lambda_c)}<0.
}
\]

Thus higher architecture cost lowers the maximum coupling compatible with static differentiation advantage.

Differentiate again:

\[
\frac{d^2\lambda_c}{dK^2}
=
-\frac{R''(\lambda_c)}{[R'(\lambda_c)]^3}.
\]

Because

\[
R''\ge0,
\qquad
R'<0,
\]

we obtain

\[
\boxed{
\frac{d^2\lambda_c}{dK^2}\ge0.
}
\]

Hence the critical-coupling curve is decreasing but convex in `K`.

## Interpretation

Two systems with the same current net margin `m_0` need not have the same robustness to added integration. The system with the smaller active coupling penalty `c_0` has the larger guaranteed distance to the crossing.

This separates two notions:

- **current advantage**: `m_0=R-K`;
- **coupling robustness**: how far `lambda` can increase before the advantage disappears.

The ratio

\[
\frac{m_0}{c_0}
\]

is a local lower-bound measure of the second quantity.

## Quadratic check

For the symmetric quadratic bridge with

\[
R(\lambda)=\frac{L}{1+2\lambda},
\]

`R` is decreasing and convex. At any `lambda_0` with `R(lambda_0)>K`, the tangent-bound distance is no larger than the exact distance to

\[
\lambda_c=\frac{L/K-1}{2}.
\]

Thus the general theorem recovers a valid conservative threshold bound in the closed-form case.

## Empirical consequence

If a matched experimental series can estimate:

1. current net architecture margin `m_0` on a common fitness scale;
2. the active residual-coupling penalty or local derivative `c_0=-dR/dlambda`;

then BITA can bound the minimum additional coupling needed to erase the current advantage without separately solving the full nonlinear recovery curve.

The bound still does not identify `K` from `Delta_W` alone. If `m_0` is estimated only as a direct net gap, the decomposition non-identifiability theorem remains in force.

## Claim ceiling

The bound requires the same feasible set and baseline landscape while `lambda` changes, fixed architecture cost `K`, convex/non-increasing recovery, and a regular local derivative. If changing integration also changes cost or accessible phenotypes, the bound does not apply without extension.
