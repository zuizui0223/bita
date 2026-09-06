# BITA decoupling-ray criticality theorem v1

## Purpose

Establish uniqueness and shape constraints for the static architecture threshold along any fixed feasible direction of coupling relief.

The multi-channel theory treats recoverable fitness as a convex, coordinatewise non-increasing function

\[
R(\boldsymbol\lambda).
\]

A graded experiment often cannot explore all coupling directions. Instead it changes coupling along one declared direction. The present theorem shows that this one-dimensional intervention path has a highly constrained critical geometry.

## Setup

Choose a nonnegative decoupling direction

\[
v\ge0
\]

and define the feasible ray

\[
\boldsymbol\lambda(t)=\boldsymbol\lambda_0-tv,
\qquad
0\le t\le t_{\max},
\]

with every point remaining inside the registered coupling box.

Hold architecture cost `K` fixed and define the static optimized-fitness margin

\[
m(t)=R(\boldsymbol\lambda(t))-K.
\]

Positive `m` favors the differentiated architecture; negative `m` favors the shared architecture.

## Theorem 1 — ray margin is non-decreasing and convex

Because `R` is coordinatewise non-increasing in residual coupling and `lambda(t)` decreases componentwise with `t`,

\[
\boxed{m(t)\text{ is non-decreasing in }t.}
\]

Because a convex function composed with an affine map is convex,

\[
\boxed{m(t)\text{ is convex in }t.}
\]

Thus any fixed decoupling ray has a static architecture margin whose slope can stay constant or increase, but cannot turn downward under the registered model.

## Theorem 2 — projected active penalty is the ray derivative

Where differentiable,

\[
\frac{dm}{dt}
=
-\nabla R(\lambda(t))^\top v
=
\mathbf c(\lambda(t))^\top v
\ge0,
\]

where

\[
\mathbf c=-\nabla R
\]

is the active coupling-penalty vector.

Convexity of `m` implies

\[
\boxed{
\mathbf c(\lambda(t))^\top v
\text{ is non-decreasing along the ray.}
}
\]

So graded decoupling predicts increasing or constant marginal benefit along a fixed intervention direction, not diminishing marginal benefit, within the convex BITA model.

## Theorem 3 — at most one static crossing

A non-decreasing continuous function cannot change sign from negative to positive and then return to negative. Therefore the ray can contain at most one shared-to-differentiated transition.

More precisely, the zero set

\[
Z=\{t:m(t)=0\}
\]

is either empty, a single point, or a closed interval. The state ordering along the ray must have the form

```text
shared side -> optional zero/tie interval -> BITA side
```

and never

```text
shared -> BITA -> shared
```

under fixed `K` and the registered convex coupling model.

If

\[
\mathbf c(\lambda(t))^\top v>0
\]

through the relevant neighborhood, `m` is strictly increasing there and the zero is unique.

## Corollary 3a — existence and uniqueness from endpoint signs

If

\[
m(0)<0
\quad\text{and}\quad
m(t_{\max})>0,
\]

continuity guarantees at least one zero. Monotonicity makes the crossing unique up to a possible zero plateau. With strict directional penalty, there is exactly one critical value

\[
\boxed{t_c\in(0,t_{\max}).}
\]

## Theorem 4 — sampled secant-slope signature

For ordered intervention levels

\[
t_0<t_1<\cdots<t_n,
\]

convexity implies non-decreasing secant slopes on consecutive intervals:

\[
\boxed{
\frac{m(t_{i+1})-m(t_i)}{t_{i+1}-t_i}
\le
\frac{m(t_{i+2})-m(t_{i+1})}{t_{i+2}-t_{i+1}}.
}
\]

Therefore a graded experiment can test not only the sign crossing but also the predicted convex shape along the declared decoupling ray.

## Corollary 4a — threshold bracketing is fail-closed

If sampled margins obey monotonicity and one adjacent pair satisfies

\[
m(t_i)<0<m(t_{i+1}),
\]

then

\[
\boxed{t_c\in(t_i,t_{i+1}).}
\]

Additional intervention levels can refine the bracket without changing the estimand. If sampled margins violate the required order beyond uncertainty, the analysis should flag model failure rather than force a threshold estimate.

## Relation to BALANCE and PAYOFF

The ray theorem is owned by BITA because `t` manipulates residual coupling inside the differentiated architecture and asks when recoverable fitness exceeds `K`.

It does not identify BALANCE occupancy without an independent positive SCH conflict and direct shared/alternative worldline comparison in the same context. It also does not imply population invasion, establishment or coexistence after the static crossing; those remain PAYOFF questions.

## Empirical consequence

A graded multi-level coupling experiment can preregister:

1. a single physical decoupling direction `v`;
2. ordered intervention levels `t`;
3. same-scale net architecture margins `m(t)`;
4. monotonicity and convexity checks;
5. a threshold bracket only if the shape checks pass.

The theorem makes repeated coupling levels informative even when a full multi-dimensional coupling surface is impractical.

## Claim ceiling

The result requires a fixed architecture cost `K`, one fixed feasible decoupling direction, and convex coordinatewise monotone `R` along the entire ray. If the intervention changes `K`, opens new phenotype states, changes baseline fitness or rotates the biological coupling direction with dose, sign re-entry or slope reversal need not contradict biology; it contradicts the registered static ray model. PAYOFF dynamics are outside scope.
