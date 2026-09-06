# BITA convex-ray threshold refinement theorem v1

## Purpose

Use the monotone-convex shape of a fixed decoupling ray to sharpen a static critical-dose bracket beyond the two sampled levels that merely straddle zero.

The ray theorem gives a unique critical value `t_c` when a valid fixed-`K` convex ray contains both shared-favored and BITA-favored margins. Here we show that three ordered samples can produce a narrower deterministic bracket without fitting a parametric recovery curve.

## Setup

Let

\[
t_0<t_1<t_2
\]

with margins

\[
m_0\le m_1<0<m_2,
\]

on a non-decreasing convex ray margin `m(t)`.

Define the crossing-interval secant slope

\[
s_{12}
=
\frac{m_2-m_1}{t_2-t_1}>0
\]

and the previous secant slope

\[
s_{01}
=
\frac{m_1-m_0}{t_1-t_0}\ge0.
\]

Convexity requires

\[
s_{01}\le s_{12}.
\]

## Theorem 1 — chord zero is a lower bound on the true critical dose

For a convex function, the graph lies below the chord joining two sampled points. The chord through `(t_1,m_1)` and `(t_2,m_2)` crosses zero at

\[
\boxed{
t_L
=
t_1-
\frac{m_1}{s_{12}}
=
t_1+(t_2-t_1)
\frac{-m_1}{m_2-m_1}.
}
\]

At `t_L` the chord is zero, while convexity implies

\[
m(t_L)\le0.
\]

Because the ray margin is non-decreasing and crosses zero only once,

\[
\boxed{t_c\ge t_L.}
\]

Thus linear interpolation between the straddling observations is not an unbiased estimate under convex recovery: it is a **lower bound** on the true critical dose.

## Theorem 2 — previous secant gives an upper bound

Convexity implies that for any `t>=t_1`,

\[
\frac{m(t)-m_1}{t-t_1}
\ge s_{01}.
\]

Hence

\[
m(t)
\ge
m_1+s_{01}(t-t_1).
\]

If `s_01>0`, the right-hand line reaches zero at

\[
\boxed{
t_U^{sec}
=
t_1-
\frac{m_1}{s_{01}}.
}
\]

At that point `m(t_U^sec)>=0`, so

\[
\boxed{t_c\le t_U^{sec}.}
\]

The observed positive point already gives `t_c<t_2`, so the practical upper bound is

\[
\boxed{
t_U
=
\min\left(t_2,
 t_1-\frac{m_1}{s_{01}}
\right).
}
\]

If `s_01=0`, the previous interval supplies no finite improvement and `t_U=t_2`.

## Corollary — deterministic three-point refined bracket

Under the registered monotone-convex ray assumptions,

\[
\boxed{
t_L\le t_c\le t_U.}
\]

Because `s_01<=s_12`, the lower bound never exceeds the secant-derived upper candidate. The interval is therefore internally ordered whenever the sampled data satisfy the convexity audit.

The refined bracket can be strictly narrower than `[t_1,t_2]` on both sides.

## Optional local-gradient refinement

If an independently estimated valid subgradient/derivative `g_1` at `t_1` is available, convexity gives

\[
m(t)\ge m_1+g_1(t-t_1).
\]

For `g_1>0`, an even sharper upper bound is

\[
\boxed{
t_c\le t_1-\frac{m_1}{g_1}.}
\]

This should only be used when the derivative estimate is registered independently of the threshold fit.

## Empirical consequence

A graded coupling experiment can report:

```text
raw sign bracket       [t1, t2]
convex chord lower     tL
previous-secant upper  tU
refined bracket        [tL, tU]
```

No parametric quadratic fit is required.

If `s_01>s_12` beyond uncertainty, the three points violate convexity and no refined threshold should be issued. The correct output is a ray-model audit failure.

This creates a sequential design rule: once a negative/positive pair is found, one earlier negative level can materially tighten the next intervention range.

## Claim ceiling

The result requires the same fixed decoupling direction, fixed `K`, and a continuous non-decreasing convex static architecture margin across all three levels. Measurement uncertainty must be propagated before sign and slope-order claims. The bracket concerns static optimized fitness, not invasion or establishment; PAYOFF remains separate.
