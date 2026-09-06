# BITA optimal-decoupling and joint robustness theorem v1

## Purpose

Turn the multi-coupling gradient

\[
\nabla_{\lambda}R=-\mathbf c^*
\]

into an intervention rule: **which integration channels should be weakened first to recover the most fitness per unit intervention cost?**

Also characterize the local shortest joint perturbation in coupling and architecture cost required to erase a currently positive differentiation margin.

## Setup

Let

\[
\boldsymbol\lambda=(\lambda_1,\ldots,\lambda_m)
\]

be residual-coupling strengths and

\[
R(\boldsymbol\lambda)
\]

the recoverable shared-compromise loss. Under the registered regular multi-coupling model,

\[
\nabla R=-\mathbf c^*,
\qquad
\mathbf c^*=(c_1^*,\ldots,c_m^*)\ge0.
\]

A small decoupling intervention has

\[
\delta\boldsymbol\lambda\le0
\]

componentwise. Let intervention cost be measured locally by a positive-definite metric `Q`:

\[
\|\delta\boldsymbol\lambda\|_Q^2
=
\delta\boldsymbol\lambda^\top Q\delta\boldsymbol\lambda.
\]

For the explicit intervention rule below, take `Q` diagonal or otherwise require that the unconstrained optimizer is biologically feasible as a decoupling move.

## Theorem 1 — optimal local decoupling direction

To first order,

\[
\Delta R
\approx
-\mathbf c^{*\top}\delta\boldsymbol\lambda.
\]

Under the budget

\[
\delta\boldsymbol\lambda^\top Q\delta\boldsymbol\lambda\le\varepsilon^2,
\]

Cauchy-Schwarz in the `Q` metric gives

\[
\boxed{
\Delta R_{\max}^{(1)}
=
\varepsilon\sqrt{\mathbf c^{*\top}Q^{-1}\mathbf c^*}
}
\]

with optimizer

\[
\boxed{
\delta\boldsymbol\lambda^*
=
-\varepsilon
\frac{Q^{-1}\mathbf c^*}
{\sqrt{\mathbf c^{*\top}Q^{-1}\mathbf c^*}}.
}
\]

Thus the locally optimal route to greater differentiation is not necessarily to weaken the numerically largest coupling. It is to weaken channels in proportion to **active coupling penalty divided by intervention cost geometry**.

For diagonal

\[
Q=\operatorname{diag}(q_i),
\]

this becomes

\[
\delta\lambda_i^*
\propto
-\frac{c_i^*}{q_i}.
\]

## Corollary 1a — best single channel

If only one coupling channel may be changed under the same quadratic budget, channel `j` gives first-order gain

\[
\varepsilon\frac{c_j^*}{\sqrt{q_j}}.
\]

Therefore the best one-channel target is

\[
\boxed{
\operatorname*{arg\,max}_j
\frac{c_j^*}{\sqrt{q_j}}.
}
\]

This supplies a preregistrable ranking for mechanistic decoupling interventions.

## Theorem 2 — critical cost surface

With architecture cost `K`, define the static differentiation margin

\[
M(\boldsymbol\lambda,K)=R(\boldsymbol\lambda)-K.
\]

The critical surface is

\[
\boxed{K_c(\boldsymbol\lambda)=R(\boldsymbol\lambda).}
\]

Because `R` is convex and coordinatewise non-increasing,

- `K_c` is convex in coupling space;
- its local slope is
  \[
  \boxed{\nabla K_c=-\mathbf c^*};
  \]
- increasing any coupling channel weakly lowers the maximum architecture cost that differentiation can pay.

So the BITA critical surface is a downward-sloping convex cost ceiling over the coupling coordinates.

## Theorem 3 — shortest joint adverse perturbation to the architecture boundary

Suppose the present state has positive static margin

\[
m=M(\boldsymbol\lambda_0,K_0)>0.
\]

Allow both coupling and architecture cost to worsen. Use the local quadratic perturbation metric

\[
\|\delta q\|_H^2
=
\delta\boldsymbol\lambda^\top Q\delta\boldsymbol\lambda
+q_K(\delta K)^2,
\qquad q_K>0.
\]

The margin gradient in augmented parameter space is

\[
\nabla M=(-\mathbf c^*,-1).
\]

The linearized shortest distance to `M=0` is therefore

\[
\boxed{
d_{\rm joint}
=
\frac{m}
{\sqrt{\mathbf c^{*\top}Q^{-1}\mathbf c^*+1/q_K}}.
}
\]

The corresponding minimum-cost adverse perturbation is

\[
\boxed{
\delta\boldsymbol\lambda^*
=
\frac{m Q^{-1}\mathbf c^*}
{\mathbf c^{*\top}Q^{-1}\mathbf c^*+1/q_K},
}
\]

\[
\boxed{
\delta K^*
=
\frac{m/q_K}
{\mathbf c^{*\top}Q^{-1}\mathbf c^*+1/q_K}.
}
\]

Both terms are non-negative under diagonal positive intervention metrics and active penalties, as expected for an adverse move that strengthens integration and/or raises architecture cost.

## Interpretation

The theorem distinguishes three robustness questions:

1. **coupling-only robustness** — how much extra integration is required to lose the BITA advantage;
2. **cost-only robustness** — exactly the present margin `m` in common fitness units;
3. **joint robustness** — the shortest biologically weighted combination of stronger coupling and higher cost that reaches the critical surface.

A system can be robust to either coupling or cost alone but fragile to a coordinated change in both.

## Empirical consequence

If several integration channels are experimentally manipulable, estimate their active penalties near the current optimum and preregister an intervention-cost metric. The theory predicts:

- the local ranking of single-channel decoupling targets;
- the optimal combination of channel reductions under a fixed intervention budget;
- the local orientation of the architecture critical surface;
- the joint coupling-plus-cost distance to loss of differentiation advantage.

These predictions concern static architecture fitness. They do not determine invasion from rarity; that remains PAYOFF's layer.

## Claim ceiling

The optimal-direction result is first-order and assumes changing coupling does not simultaneously change the baseline landscape, feasible phenotype set, architecture cost, or the definition of the active penalties. Off-diagonal intervention metrics are allowed mathematically, but biological one-sided decoupling constraints must be checked explicitly. The joint-distance formula is a local linearization of the critical surface, not a global distance for strongly nonlinear perturbations.
