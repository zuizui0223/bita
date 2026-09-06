# BITA multi-coupling robustness theorem v1

## Purpose

Generalize the scalar residual-coupling result to several distinct integration channels.

Let the differentiated phenotype be `u` and let residual integration be represented by a non-negative vector of penalties

\[
c(u)=(c_1(u),\dots,c_m(u)),\qquad c_r(u)\ge0.
\]

Let coupling strengths be

\[
\lambda=(\lambda_1,\dots,\lambda_m)\in\mathbb R_+^m.
\]

Define

\[
D^*(\lambda)
=
\inf_u\{B(u)+\lambda^Tc(u)\}
\]

and

\[
R(\lambda)=L_S^*-D^*(\lambda).
\]

Assume the shared subspace is feasible in the differentiated space and every coupling penalty vanishes there.

## Theorem 1 — coordinatewise monotonicity

If

\[
\lambda'\ge\lambda
\]

componentwise, then for every phenotype `u`,

\[
B(u)+\lambda'^Tc(u)
\ge
B(u)+\lambda^Tc(u).
\]

Taking infima gives

\[
D^*(\lambda')\ge D^*(\lambda)
\]

and therefore

\[
\boxed{R(\lambda')\le R(\lambda).}
\]

So increasing any collection of residual-coupling strengths cannot increase the fitness recoverable by differentiation.

## Theorem 2 — vector convexity

For fixed `u`,

\[
B(u)+\lambda^Tc(u)
\]

is affine in the vector `lambda`. The pointwise infimum of affine functions is concave, so `D*` is concave in `lambda`. Hence

\[
\boxed{R(\lambda)\text{ is convex on }\mathbb R_+^m.}
\]

## Theorem 3 — gradient equals the active penalty vector

At a regular unique optimum `u^*_lambda`, the multivariate envelope theorem gives

\[
\nabla_\lambda D^*(\lambda)=c(u^*_\lambda).
\]

Therefore

\[
\boxed{
\nabla_\lambda R(\lambda)=-c(u^*_\lambda)
}
\]

componentwise.

Each active penalty is the marginal rate at which recoverable fitness is lost when that particular integration channel strengthens.

## Theorem 4 — local half-space lower bound for crossing

Let architecture cost `K` be fixed and suppose at `lambda_0`

\[
m_0=R(\lambda_0)-K>0.
\]

Write

\[
c_0=c(u^*_{\lambda_0}).
\]

Convexity gives the supporting-hyperplane inequality

\[
R(\lambda_0+\Delta\lambda)
\ge
R(\lambda_0)-c_0^T\Delta\lambda.
\]

If a non-negative coupling change `Delta lambda>=0` reaches a static architecture crossing,

\[
R(\lambda_0+\Delta\lambda)=K,
\]

then necessarily

\[
\boxed{
c_0^T\Delta\lambda\ge m_0.}
\]

Thus the current active penalty vector defines a **forbidden near region**: no increase in residual coupling whose penalty-weighted magnitude is smaller than the current net margin can erase the differentiated advantage under the declared model.

## Corollary 4a — directional lower bound

For a declared coupling direction `v>=0`, consider

\[
\lambda(t)=\lambda_0+t v.
\]

If

\[
c_0^Tv>0,
\]

then any later crossing satisfies

\[
\boxed{
t_c\ge\frac{m_0}{c_0^Tv}.}
\]

If

\[
c_0^Tv=0,
\]

then the local tangent predicts no loss of recoverable fitness in that direction; under the convex/non-increasing regular model, a later crossing along that ray cannot appear without another assumption changing.

## Corollary 4b — norm lower bound

For any norm `||.||` with dual norm `||.||_*`, Holder's inequality gives

\[
c_0^T\Delta\lambda
\le
\|c_0\|_*\|\Delta\lambda\|.
\]

Therefore every crossing must satisfy

\[
\boxed{
\|\Delta\lambda\|
\ge
\frac{m_0}{\|c_0\|_*}.
}
\]

For Euclidean norm,

\[
\boxed{
\|\Delta\lambda\|_2
\ge
\frac{m_0}{\|c_0\|_2}.
}
\]

This is the multi-channel generalization of the scalar `m_0/c_0` robustness bound.

## Corollary 4c — differentiation-favored coupling states are downward closed

If a coupling vector `lambda` satisfies

\[
R(\lambda)>K,
\]

then every componentwise smaller vector

\[
0\le\widetilde\lambda\le\lambda
\]

also satisfies

\[
R(\widetilde\lambda)\ge R(\lambda)>K.
\]

So the differentiation-favored set is an **order ideal** in non-negative coupling space. Once a phenotype is differentiation-favored at some integration level, weakening any subset of couplings cannot reverse that static ordering under the declared assumptions.

## Empirical consequence

Different kinds of integration can be separated experimentally or comparatively, for example:

- developmental covariance;
- mechanical cross-talk;
- shared regulatory control;
- genetic correlation;
- resource coupling.

If their effective strengths can be varied independently, BITA predicts a monotone recovery surface and a local penalty vector. This permits tests of which integration channel most rapidly erodes dimensional release.

The strongest channel is not necessarily the one with largest raw coupling coefficient; it is the one with largest active penalty component at the optimized differentiated phenotype.

## Claim ceiling

The theorem assumes fixed baseline loss, fixed architecture cost, a common feasible differentiated set, non-negative coupling penalties, and zero penalty on the shared subspace. Changing a coupling mechanism may alter other parts of the phenotype map in real systems; such changes require an extended model.
