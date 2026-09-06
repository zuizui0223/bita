# BITA general coupling-recovery theorem v1

## Purpose

Generalize the statement that stronger residual coupling reduces the fitness recoverable by trait differentiation without relying on the quadratic closed form.

## Setup

Let `D` be the differentiated phenotype space and `S subset D` the shared phenotype subspace. Write a baseline loss

\[
B(u)
\]

for `u in D`, and a non-negative residual-coupling penalty

\[
c(u)\ge0.
\]

Assume every shared phenotype has zero coupling penalty:

\[
c(u)=0 \quad \text{for } u\in S.
\]

For coupling strength `lambda>=0`, define the optimized differentiated loss

\[
D^*(\lambda)
=
\inf_{u\in D}\{B(u)+\lambda c(u)\},
\]

and the best shared loss

\[
L_S^*=\inf_{u\in S}B(u).
\]

Define recoverable shared-compromise loss

\[
R(\lambda)=L_S^*-D^*(\lambda).
\]

## Theorem 1 — nesting guarantees non-negative recovery

Because `S subset D` and `c=0` on `S`, every shared phenotype is feasible in the differentiated optimization at exactly its shared baseline loss. Therefore

\[
D^*(\lambda)\le L_S^*
\]

for every `lambda>=0`, hence

\[
\boxed{R(\lambda)\ge0}.
\]

This is the architecture-nesting result with residual coupling included explicitly.

## Theorem 2 — stronger coupling cannot increase recovery

For `lambda_2>lambda_1` and every phenotype `u`,

\[
B(u)+\lambda_2c(u)
\ge
B(u)+\lambda_1c(u).
\]

Taking infima over the same feasible set gives

\[
D^*(\lambda_2)\ge D^*(\lambda_1).
\]

Therefore

\[
\boxed{R(\lambda_2)\le R(\lambda_1)}.
\]

So recoverable compromise loss is non-increasing in residual-coupling strength under only nesting and non-negative coupling penalty assumptions. Convexity of the biological landscape is not required for this monotonic ordering itself.

## Theorem 3 — recovery is convex in coupling strength

For each fixed phenotype `u`,

\[
B(u)+\lambda c(u)
\]

is affine in `lambda`. The pointwise infimum of affine functions is concave. Hence

\[
D^*(\lambda)
\]

is concave in `lambda`, and therefore

\[
\boxed{R(\lambda)=L_S^*-D^*(\lambda)\text{ is convex in }\lambda}.
\]

This means the amount of remaining recoverable fitness can decline nonlinearly with coupling, but under this model its slope cannot become more negative as `lambda` increases.

## Theorem 4 — envelope sensitivity when the optimum is regular

If the differentiated optimum `u_lambda^*` is unique and regular enough for the envelope theorem, then

\[
\frac{dD^*}{d\lambda}=c(u_\lambda^*)
\]

and therefore

\[
\boxed{
\frac{dR}{d\lambda}
=-c(u_\lambda^*)\le0.
}
\]

If the active differentiated optimum retains strictly positive coupling penalty, then recovery decreases strictly at that point.

This gives the coupling penalty itself an interpretable marginal meaning: it is the instantaneous rate at which recoverable fitness is lost when integration strength increases.

## Architecture gain and critical coupling

With an extra architecture cost `K>=0`,

\[
\Delta_{\rm arch}(\lambda)=R(\lambda)-K.
\]

Suppose `R` is continuous and strictly decreasing on the relevant interval, with

\[
R(0)>K>R(\lambda_{\max}).
\]

Then there is a unique critical coupling `lambda_c` satisfying

\[
\boxed{R(\lambda_c)=K}.
\]

The differentiated architecture is statically favored for lower coupling and disfavored for higher coupling:

\[
\lambda<\lambda_c \Rightarrow \Delta_{\rm arch}>0,
\qquad
\lambda>\lambda_c \Rightarrow \Delta_{\rm arch}<0.
\]

If `R` is differentiable and `R'(lambda_c)<0`, implicit differentiation gives

\[
\boxed{
\frac{d\lambda_c}{dK}
=
\frac{1}{R'(\lambda_c)}<0.
}
\]

Thus raising architecture cost lowers the maximum residual coupling compatible with a differentiation-favored state.

## Strong-coupling limit

If the zero set of `c` coincides with the shared phenotype set (or has the same optimized baseline loss), and standard compactness/coercivity conditions prevent escape to infinity, then

\[
D^*(\lambda)\to L_S^*
\quad\text{as}\quad
\lambda\to\infty,
\]

so

\[
R(\lambda)\to0.
\]

This recovers the intuitive shared-coordinate limit as integration becomes arbitrarily strong.

## Quadratic bridge as a special case

For the registered two-coordinate quadratic model,

\[
c(x,y)=(x-y)^2,
\]

and the closed-form `R=sL` obeys all results above. The quadratic formula provides explicit `s(lambda)`; the theorem here explains which monotonic statements survive without that formula.

## Empirical consequence

BITA can distinguish two levels of evidence:

1. **ordering prediction:** contexts or genotypes with stronger residual coupling should not show greater optimized recovery, all else held fixed;
2. **marginal prediction:** where a smooth optimum path is identifiable, the observed coupling penalty at the optimum determines the local loss of recoverable fitness with increasing integration.

Neither prediction identifies architecture cost `K` from the net worldline gap alone. The decomposition non-identifiability result remains in force.

## Claim ceiling

The monotonicity/convexity results are conditional on a common differentiated feasible set, non-negative coupling penalty, and zero penalty on the shared subspace. If changing `lambda` also changes feasible phenotypes, developmental accessibility, baseline fitness `B`, or architecture cost `K`, the simple theorem does not apply without extending the model.
