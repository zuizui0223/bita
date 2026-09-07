# BITA coupling value-function observational-equivalence theorem v1

## Purpose

State exactly what optimized-fitness experiments across residual-coupling conditions can identify about the latent coupling mechanism.

BITA already distinguishes the observable recoverable-fitness function

\[
R(\boldsymbol\lambda)
\]

from its net architecture comparison `R-K`. The present theorem goes one layer deeper: even a perfectly known `R(lambda)` does not in general identify a unique latent decomposition into phenotype states, baseline losses and coupling penalties.

This establishes a formal reason why the causal mechanism lane cannot be replaced by increasingly dense static fitness mapping.

## Setup

A latent coupling model `M` consists of a feasible phenotype/state set `U_M`, baseline differentiated loss

\[
B_M(u),
\]

and a nonnegative residual-coupling penalty vector

\[
\mathbf c_M(u)\ge0.
\]

For residual-coupling vector

\[
\boldsymbol\lambda\in\Lambda\subseteq\mathbb R_+^m,
\]

define optimized differentiated loss

\[
D_M^*(\boldsymbol\lambda)
=
\inf_{u\in U_M}
\left[
B_M(u)+\boldsymbol\lambda^\top\mathbf c_M(u)
\right].
\]

For fixed shared-axis benchmark `L_S*`, define

\[
R_M(\boldsymbol\lambda)
=
L_S^*-D_M^*(\boldsymbol\lambda).
\]

## Theorem 1 — static coupling-value observational equivalence

Two latent coupling models `M` and `N` are observationally equivalent on the registered intervention domain `Lambda` for all optimized-fitness coupling experiments iff

\[
\boxed{
R_M(\boldsymbol\lambda)
=
R_N(\boldsymbol\lambda)
\quad\forall\boldsymbol\lambda\in\Lambda.
}
\]

Equivalently, because the same `L_S*` is used,

\[
D_M^*(\boldsymbol\lambda)
=
D_N^*(\boldsymbol\lambda)
\quad\forall\boldsymbol\lambda\in\Lambda.
\]

Any static experiment that observes only optimized total fitness, architecture margin, or recoverable fitness over `Lambda` has identical predictions under the two models.

Thus the complete static intervention map identifies a **value function**, not necessarily a unique latent mechanism representation.

## Corollary 1a — dominated latent states are invisible

Suppose model `N` is created from `M` by adding a latent state `v` whose affine loss plane

\[
B_N(v)+\boldsymbol\lambda^\top\mathbf c_N(v)
\]

never attains the lower envelope over `Lambda`.

Then

\[
D_N^*=D_M^*
\]

on `Lambda`, so the added latent state is observationally invisible to every static optimized-fitness coupling experiment.

Hence absence of evidence for a latent mechanism state from optimized fitness alone is not evidence that the state is biologically absent.

## Explicit finite-dimensional example

For one coupling coordinate `lambda>=0`, consider model `M` with two latent affine loss states:

\[
(B,c)=(0,1),
\qquad
(B,c)=(1,0).
\]

Then

\[
D_M^*(\lambda)=\min\{\lambda,1\}.
\]

Now create model `N` by adding a third state

\[
(B,c)=(2,1/2).
\]

For every `lambda>=0`,

\[
2+\frac12\lambda
>
\min\{\lambda,1\},
\]

so

\[
D_N^*(\lambda)=D_M^*(\lambda)
\]

for the entire intervention domain even though the latent mechanism sets differ.

## Theorem 2 — what a differentiable value function does identify

At a regular point where the optimized latent state is unique and the envelope is differentiable,

\[
\nabla_{\boldsymbol\lambda}D^*(\boldsymbol\lambda)
=
\mathbf c^*(\boldsymbol\lambda)
\]

by the envelope theorem.

Therefore

\[
\boxed{
-\nabla_{\boldsymbol\lambda}R(\boldsymbol\lambda)
=
\mathbf c^*(\boldsymbol\lambda).
}
\]

So the local active penalty vector of the **currently optimized state** is identified from the slope of the recoverable-fitness value function.

This does not identify:

- penalties of inactive latent states;
- a unique developmental or structural coordinate system behind those penalties;
- the baseline-vs-penalty decomposition away from the active envelope;
- the biological mechanism generating the measured penalty channel.

## Corollary 2a — kinks identify an active face, not a unique mechanism

At a coupling point where several latent affine states tie on the lower envelope, `D*` is generally nondifferentiable.

The subgradient set is the convex hull of active penalty vectors. Equivalently, the supergradient set of `R` is the negative of that hull.

Thus a kink identifies a **set of compatible active penalty vectors**, not a unique latent state.

Architecture or mechanism labels at such a switch require additional measurements.

## Theorem 3 — second-order response identifies value-function curvature, not latent coordinates

Where `R` is twice differentiable, experiments can identify

\[
\nabla^2R(\boldsymbol\lambda),
\]

which controls finite-gain curvature, path-integrability tests and critical-budget refinement.

But two latent models with the same `R` necessarily have the same gradient and Hessian wherever differentiable while remaining mechanistically distinct.

Therefore even complete first- and second-order static response information does not generally identify the latent phenotype/state representation.

## Theorem 4 — mechanism equivalence is strictly finer than value-function equivalence

Define:

```text
value-function equivalence:
    same R(lambda) over the registered intervention domain
mechanism equivalence:
    same biologically interpreted latent states / penalty channels / baseline mechanism
```

Mechanism equivalence implies value-function equivalence, but the converse fails by Theorem 1 and the explicit example.

Therefore a successful fit of the BITA coupling value function is a necessary quantitative description of static release but not a proof of the registered causal mechanism.

## Empirical consequence

BITA now has a clean identification hierarchy:

```text
matched shared vs differentiated optimized fitness
        -> net architecture ordering / Delta_W
coupling sweep of optimized fitness
        -> R(lambda) and, locally, active penalty slopes/curvature
crossed functional loading + ecological mechanism assays
        -> mechanism-specific causal interpretation
independent architecture-cost lane
        -> K rather than only R-K
```

Dense coupling experiments cannot substitute for the crossed mechanism design if the scientific claim is about **why** the extra dimension works rather than only **how much** optimized fitness is recovered.

## Falsifiable signatures

Under one registered static coupling-value model:

- repeated paths to the same `lambda` must return the same `R(lambda)` absent state/history dependence;
- differentiable local slopes must match independently estimated active coupling penalties if those penalties are directly measurable;
- kinks predict active-state multiplicity or optimizer switching;
- two proposed mechanisms that imply different `R(lambda)` somewhere in the registered domain are experimentally distinguishable by an intervention placed there;
- two mechanisms with identical `R(lambda)` cannot be separated by optimized-fitness coupling data alone.

## Relation to existing non-identifiability

The existing theorem

\[
\Delta_W=R-K
\]

shows that the net architecture gap does not separate recovery `R` from cost `K`.

The present theorem is distinct and deeper:

\[
R(\lambda)
\]

itself does not generally separate the latent baseline/penalty/state mechanism that generates the optimized value function.

So BITA contains two nested identification problems:

1. `Delta_W` versus `R` and `K`;
2. `R(lambda)` versus its latent causal mechanism.

## Claim ceiling

The theorem concerns static optimized-fitness observations on a declared coupling domain. Mechanistic non-identifiability may be reduced by direct state measurements, structural assays, loading data or interventions that change the feasible latent-state set. Historical transitions, invasion and coexistence remain outside this theorem and belong to other evidence lanes, including PAYOFF for frequency-dependent population dynamics.