# BITA math -> causal intervention signatures v1

## Purpose

Translate BITA coupling mathematics into prospective causal tests. The core question is not merely whether a differentiated phenotype exists, but whether manipulating access/integration changes recoverable fitness and architecture ordering as predicted.

## Signature D1 — monotone coupling recovery

For residual-coupling vector `lambda`,

\[
\frac{\partial R}{\partial\lambda_i}=-c_i^*\le0.
\]

**Test:** strengthen or weaken one coupling channel while holding the declared feasible phenotype space and baseline landscape fixed enough for the model.

**Failure:** stronger coupling robustly increases optimized recovery under the same registered state space.

## Signature D2 — finite decoupling gain floor

For convex `R` and finite decoupling `x>=0`,

\[
R(\lambda_0-x)-R(\lambda_0)
\ge c_0^Tx.
\]

**Test:** estimate current active penalty vector, preregister an intervention, and compare realized optimized recovery with the certified floor.

**Failure:** realized gain falls below the floor beyond uncertainty, implying at least one assumption changed or the inferred gradient is wrong.

## Signature D3 — two-sided critical intervention budget

With curvature bounds

\[
\alpha Q\preceq\nabla^2R\preceq\beta Q
\]

and architecture deficit `delta=K-R(lambda_0)>0`, define

\[
c_Q=\sqrt{c_0^TQ^{-1}c_0}.
\]

Then

\[
r_\beta(\delta,c_Q)
\le\varepsilon_Q^*
\le r_\alpha(\delta,c_Q).
\]

**Test:** use multiple coupling levels to estimate/validate the gradient, curvature bracket and static architecture deficit.

**Failure:** crossing occurs below the no-cross bound or fails above the sufficient bound when the aligned move is feasible and `K` remains fixed.

## Signature D4 — uncertainty-aware budget band

When `delta`, active penalty and curvature are only bounded, report a robust no-cross threshold and robust sufficient threshold rather than a point critical budget.

**Test:** use simultaneous parameter bounds and propagate them through the registered theorem.

**Failure:** do not combine unrelated marginal intervals as if they were simultaneous bounds.

## Signature D5 — optimal channel ranking and saturation

For weighted-L1 intervention cost, target channels in descending

\[
\eta_i=c_i/a_i
\]

until each saturates at available coupling `lambda_0i`.

For diagonal quadratic cost,

\[
x_i^*=\min\{\lambda_{0i},\tau c_i/q_i\}.
\]

**Test:** preregister which channel should be targeted/saturate first and the expected allocation change after saturation.

**Failure:** a consistently lower-efficiency unsaturated channel outperforms a higher-efficiency available channel under the registered linear-gain/cost model.

## Signature D6 — recovery-frontier kinks

Under box constraints the certified recovery-vs-budget frontier changes slope when a high-value coupling channel becomes fully removed.

**Test:** use enough intervention levels to bracket predicted saturation breakpoints.

**Failure:** observed optimized recovery need not equal the linear certified frontier, but the inferred active-penalty/cost model should be revised if estimated local marginal values or saturation order contradict the registered channel ranking.

## Signature D7 — coupling-path integrability

In the smooth common-potential model,

\[
R(\lambda_B)-R(\lambda_A)
=-\int_A^B c^T d\lambda
\]

and closed-loop integral is zero.

**Test:** where two coupling channels can be manipulated in different orders, compare paths to the same endpoint.

**Failure:** persistent path dependence after returning to the same static state suggests history-dependent accessibility, changing baseline landscape, changing `K`, or another model extension—not PAYOFF by default.

## Pedicularis use

The first focal `x x water-y` experiment primarily tests dimensional release/loading and fitness consequence. D1-D7 require a richer manipulation in which residual integration/coupling itself can be graded. They are the next mechanistic tier, not prerequisites for the first functional-state BITA receipt.

## Promotion rule

A static coupling threshold is not an invasion threshold. Even a certified crossing from shared-favored to differentiated-favored optimized fitness does not establish rare-architecture invasion or coexistence; those remain PAYOFF questions.
