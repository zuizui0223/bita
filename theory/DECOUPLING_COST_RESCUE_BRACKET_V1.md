# BITA decoupling-plus-cost rescue bracket v1

## Purpose

Quantify how much **architecture-cost relief** is still required when even maximal registered decoupling may not be enough to cross the static architecture boundary.

The full-decoupling reachability theorem brackets the maximum recoverable-fitness gain available inside the registered coupling box. The present result converts that gain interval into a bracket on the minimum additional reduction in architecture cost `K` needed to make differentiation competitive.

This separates two mechanistic bottlenecks:

```text
residual coupling is too strong
architecture cost is too high
```

and allows a system to be diagnosed as coupling-limited, cost-limited, or unresolved between them.

## Setup

At the current coupling state `lambda_0`, let

\[
R_0=R(\lambda_0),
\qquad
\delta=K-R_0>0.
\]

The architecture is currently shared-favored by deficit `delta`.

Let the full registered decoupling move have exact gain

\[
\Delta R_{\rm full}
=R(0)-R_0,
\]

or, more generally, gain to the minimum registered coupling endpoint.

Suppose existing curvature analysis gives

\[
\boxed{
L_{\rm full}
\le
\Delta R_{\rm full}
\le
U_{\rm full}.
}
\]

Now allow an independent architecture-cost reduction

\[
\kappa\ge0,
\qquad
K' = K-\kappa.
\]

Assume this cost intervention does not change the recovery landscape `R(lambda)`.

## Theorem 1 — exact cost relief required after full decoupling

At the full-decoupled endpoint, the new architecture margin is

\[
R_0+\Delta R_{\rm full}-(K-\kappa)
=
-\delta+\Delta R_{\rm full}+\kappa.
\]

Therefore the infimum cost relief needed for nonnegative crossing is

\[
\boxed{
\kappa_*=
\max\{0,\delta-\Delta R_{\rm full}\}.
}
\]

For a strictly positive differentiated advantage, use a strict inequality above this threshold.

## Theorem 2 — partial-identification bracket for required cost relief

Because `max(0,delta-x)` is monotone decreasing in `x`, the full-gain interval implies

\[
\boxed{
\max\{0,\delta-U_{\rm full}\}
\le
\kappa_*
\le
\max\{0,\delta-L_{\rm full}\}.
}
\]

Define

\[
\kappa_{\rm necessary}
=
\max\{0,\delta-U_{\rm full}\}
\]

and

\[
\kappa_{\rm sufficient}
=
\max\{0,\delta-L_{\rm full}\}.
\]

Then:

- any cost reduction below `kappa_necessary` cannot be enough even under the most optimistic allowed decoupling gain;
- a cost reduction above `kappa_sufficient`, combined with full registered decoupling, guarantees a nonnegative crossing under the lower gain bound;
- the interval between them is unresolved by the current curvature information.

## Corollary 2a — certified coupling-limited vs cost-limited cases

### Decoupling alone guaranteed sufficient

If

\[
L_{\rm full}>\delta,
\]

then

\[
\boxed{\kappa_*=0}
\]

and the registered architecture is not intrinsically cost-limited at full decoupling.

### Positive cost relief is mathematically necessary

If

\[
U_{\rm full}<\delta,
\]

then

\[
\boxed{
\kappa_*>0
}
\]

and, more strongly,

\[
\boxed{
\kappa_*
\ge
\delta-U_{\rm full}.
}
\]

Even the most favorable recovery allowed by the registered coupling model leaves a residual deficit. Some reduction in `K`, baseline-fitness change, or architecture redesign is therefore necessary.

This is a genuine mechanistic boundary result rather than a weak-manipulation null.

## Theorem 3 — residual architecture deficit after maximal decoupling

The post-full-decoupling residual deficit is

\[
D_{\rm residual}
=
\max\{0,\delta-\Delta R_{\rm full}\}.
\]

So the same quantity is both:

1. the remaining static architecture disadvantage after maximal registered coupling relief;
2. the exact minimal independent cost reduction needed to eliminate that disadvantage.

The bounds are

\[
\boxed{
\max\{0,\delta-U_{\rm full}\}
\le
D_{\rm residual}
\le
\max\{0,\delta-L_{\rm full}\}.
}
\]

This gives a common fitness-scale measure of how much of the architecture barrier **cannot be assigned to the registered residual coupling channels**.

## Corollary 3a — architecture redesign target

When the lower bound on residual deficit is positive, a new architecture must improve something outside the registered coupling box by at least

\[
\delta-U_{\rm full}
\]

fitness units to become competitive.

Possible routes include:

- lower maintenance/developmental cost `K`;
- a new phenotype dimension that raises recoverable fitness beyond the registered `R` surface;
- a baseline performance shift;
- removal of an omitted coupling channel.

The theorem does not decide which route evolution uses; it quantifies the minimum unexplained architecture improvement required.

## Theorem 4 — joint intervention frontier under independent cost relief

For any feasible decoupling move `x` with gain interval

\[
L(x)\le\Delta R(x)\le U(x),
\]

the corresponding required cost-relief interval is

\[
\boxed{
\max\{0,\delta-U(x)\}
\le
\kappa_*(x)
\le
\max\{0,\delta-L(x)\}.
}
\]

Thus decoupling effort and architecture-cost relief can be placed on a common fitness-scale tradeoff frontier without claiming that the two interventions are biologically interchangeable.

A richer optimization can add separate intervention costs for `x` and `kappa`; that is an engineering/design layer beyond this identification theorem.

## Empirical consequence

A BITA experiment can now preregister nested outcomes:

```text
full decoupling guarantees crossing
    -> coupling relief is sufficient within the registered architecture

full decoupling cannot possibly cross
    -> positive non-coupling architecture improvement is necessary

bounds overlap the threshold
    -> coupling-vs-cost limitation remains unresolved
```

The last two cases are scientifically useful negative/boundary results for the generality programme.

## Separation from BALANCE and PAYOFF

This theorem conditions on a static architecture deficit `delta` and asks how it can be overcome mechanistically. BALANCE identifies whether the shared world currently outranks accessible alternatives; it does not by itself decompose the gap. PAYOFF asks whether a differentiated strategy invades or coexists once population-frequency effects are introduced. Neither is replaced by this cost-rescue bracket.

## Claim ceiling

The result assumes cost relief `kappa` can be represented as an additive reduction in the same fitness-scale architecture cost `K` without changing `R(lambda)`. If reducing cost also changes coupling, feasible phenotype space, or baseline function surfaces, a joint structural model is required. Strict crossing requires strict inequality above the reported infimum threshold.
