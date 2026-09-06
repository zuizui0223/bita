# BITA coupling path-integral theorem v1

## Purpose

Show that, under the smooth multi-coupling BITA model, the cumulative loss of recoverable fitness caused by stronger integration is the line integral of the **active coupling-penalty vector**.

Let

\[
R(\lambda)
\]

be recoverable compromise loss for a vector of coupling strengths

\[
\lambda\in\mathbb R_+^m.
\]

Under the regular multi-coupling theorem,

\[
\boxed{\nabla_\lambda R(\lambda)=-c^*(\lambda)}
\]

where

\[
c^*(\lambda)=c(u^*_\lambda)
\]

is the residual-coupling penalty vector evaluated at the optimized differentiated phenotype.

## Theorem 1 — path-integral identity

Let `lambda(t)` be any continuously differentiable path from `lambda_A` to `lambda_B`. By the chain rule,

\[
\frac{d}{dt}R(\lambda(t))
=
\nabla R(\lambda(t))^T\dot\lambda(t)
=
-c^*(\lambda(t))^T\dot\lambda(t).
\]

Integrating,

\[
\boxed{
R(\lambda_B)-R(\lambda_A)
=
-\int_A^B c^*(\lambda)^T\,d\lambda.
}
\]

Equivalently, the amount of recoverable fitness lost between the two coupling states is

\[
\boxed{
R(\lambda_A)-R(\lambda_B)
=
\int_A^B c^*(\lambda)^T\,d\lambda.
}
\]

This generalizes the scalar identity

\[
R(\lambda_A)-R(\lambda_B)
=
\int_{\lambda_A}^{\lambda_B}c(u^*_\lambda)\,d\lambda.
\]

## Corollary 1a — path independence

Because `c^*=-\nabla R`, the line integral depends only on the endpoints as long as the smooth optimized branch and model assumptions hold:

\[
\boxed{
\int_{\gamma_1}c^{*T}d\lambda
=
\int_{\gamma_2}c^{*T}d\lambda
}
\]

for any two paths with the same endpoints within the same regular region.

Hence for every closed loop,

\[
\boxed{
\oint c^{*T}d\lambda=0.
}
\]

This is an **integrability condition** for the optimized coupling response.

## Theorem 2 — cross-channel reciprocity

If `R` is twice continuously differentiable, then its Hessian is symmetric. Since

\[
c_i^*(\lambda)=-\frac{\partial R}{\partial\lambda_i},
\]

we obtain

\[
\boxed{
\frac{\partial c_i^*}{\partial\lambda_j}
=
\frac{\partial c_j^*}{\partial\lambda_i}.
}
\]

Thus the response of the active penalty in channel `i` to coupling channel `j` equals the reciprocal response under the smooth common-potential model.

## Theorem 3 — penalty Jacobian is negative semidefinite

The general coupling theorem gives convexity of `R`, so

\[
\nabla^2R\succeq0.
\]

Because

\[
\nabla c^*=-\nabla^2R,
\]

we have

\[
\boxed{
\nabla_\lambda c^*(\lambda)\preceq0.
}
\]

In particular,

\[
\boxed{
\frac{\partial c_i^*}{\partial\lambda_i}\le0.
}
\]

As a coupling channel becomes more strongly penalized, the optimized differentiated phenotype cannot increase its active use of that same penalty under the declared smooth model; it adapts weakly away from it.

Cross-channel responses can have either sign, but the full Jacobian must remain symmetric negative semidefinite.

## Corollary 3a — scalar recovery loss is the area under the active-penalty curve

For one coupling parameter,

\[
\boxed{
R(\lambda_A)-R(\lambda_B)
=
\int_{\lambda_A}^{\lambda_B}c^*(\lambda)\,d\lambda.
}
\]

So a sequence of local coupling-penalty estimates can reconstruct total lost recovery without fitting the quadratic `s(lambda)` formula.

## Empirical falsification logic

Suppose two integration channels can be manipulated in different orders while returning to the same final coupling state.

Under the theorem, after accounting for common baseline fitness and architecture cost:

```text
path A: increase channel 1, then channel 2
path B: increase channel 2, then channel 1
```

must imply the same endpoint change in `R` and the same integrated penalty work.

Robust path dependence would indicate that at least one declared assumption fails, for example:

- different feasible phenotypes are accessed along different histories;
- developmental or genetic hysteresis changes the state space;
- baseline loss `B` changes with the manipulation path;
- architecture cost changes;
- the optimized branch is discontinuous or nonunique.

This is not PAYOFF switching hysteresis. It is a within-BITA test of whether the static coupling model is a valid state-function description.

## Claim ceiling

Path independence and reciprocal cross-derivatives require a smooth common recovery potential `R(lambda)` over the region being compared. Nonunique optima, irreversible developmental changes, accessibility constraints, or path-dependent feasible sets can violate these results without contradicting the more basic pointwise nesting theorem.
