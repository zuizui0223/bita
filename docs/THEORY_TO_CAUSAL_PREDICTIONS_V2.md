# BITA theory -> causal predictions v2

## Purpose

Translate the current BITA coupling/recovery mathematics into causal measurements and intervention tests without replacing the registered same-system release/loading/mechanism chain.

The advanced theory now answers three nested questions:

1. does adding a second functional dimension release the shared compromise?
2. which residual coupling channels limit that release?
3. how much decoupling and/or architecture-cost relief is required to cross the static architecture boundary?

No unexecuted biological result is promoted here.

---

## A. Focal Pedicularis causal layer

The primary causal route remains:

```text
frozen same-context SCH reference
-> x x y surface
-> dimensional release
-> preferential loading
-> registered total-fitness consequence
-> mechanism allocation
-> independent K lane only if architecture-cost decomposition is claimed
```

### A1. Dimensional release

Using the frozen SCH reference, estimate whether activating the second functional state/dimension moves the focal trait optimum back toward the function-specific reference.

Primary state quantity remains the registered `R_state`/release measure, not theoretical `R` unless equivalence assumptions are separately satisfied.

### A2. Preferential loading

The added dimension must preferentially improve the target function while keeping cross-effect on the other function within the registered tolerance.

Release without preferential loading is not a completed BITA mechanism claim.

### A3. Total-fitness consequence

A mechanistic release that does not improve the registered fitness outcome is reported as release without architecture advantage, not silently promoted to differentiation favored.

---

## B. Coupling-response layer

This layer requires multiple manipulable levels of one or more integration/coupling channels.

Let residual coupling be `lambda` and recoverable fitness be `R(lambda)`.

### B1. Active coupling penalty

Estimate the local gradient

\[
\mathbf c_0=-\nabla R(\lambda_0)\ge0.
\]

Channel `i` with larger `c_i` currently suppresses more recoverable fitness per unit coupling.

Under intervention metric `Q`, the relevant gain per unit intervention effort is

\[
c_Q=\sqrt{\mathbf c_0^\top Q^{-1}\mathbf c_0}.
\]

### B2. Convex recovery / finite-gain floor

For a finite feasible decoupling move `x`, test

\[
\Delta R(x)
\ge
\mathbf c_0^\top x.
\]

Observed gain below the registered floor beyond uncertainty falsifies at least one of:

- the estimated active penalty;
- common feasible phenotype space;
- fixed baseline recovery landscape;
- convex coupling model;
- fixed `K` if an architecture crossing is being interpreted.

### B3. Curvature bounds

With multi-level coupling interventions, estimate conservative bounds

\[
A\preceq\nabla^2R\preceq B
\]

or metric/scalar versions.

Then preregister the finite gain interval

\[
\mathbf c_0^\top x+\tfrac12x^\top A x
\le\Delta R(x)\le
\mathbf c_0^\top x+\tfrac12x^\top B x.
\]

This converts qualitative coupling relief into a quantitative prospective prediction.

### B3a. Exact curvature dividend without full Hessian recovery

For any registered finite decoupling move, define

\[
\boxed{
\mathcal C_R
=\Delta R-\mathbf c_0^\top x.
}
\]

Under the convex common-landscape model,

\[
\boxed{\mathcal C_R\ge0}
\]

and exactly

\[
\Delta R
=\mathbf c_0^\top x+\mathcal C_R.
\]

`C_R` is the Bregman curvature dividend: the part of finite recovery not already predicted by the active coupling pressure at the starting state.

A graded experiment can therefore estimate it with only:

1. a baseline directional slope `c_0^T x`;
2. the registered finite decoupling move;
3. endpoint optimized-fitness recovery `Delta R`.

No full multidimensional Hessian estimate is required.

Prospective interpretation:

```text
C_R < 0 beyond uncertainty  -> convex/common-landscape model rejected
C_R ~= 0                    -> recovery is approximately affine over the move
C_R > 0                     -> additional curvature/reoptimization contributes
```

When `Delta R>0`, the optional descriptive share

\[
\phi_C=\mathcal C_R/\Delta R
\]

lies in `[0,1]` under the registered decoupling model. It is a decomposition of optimized-fitness recovery, not a historical fraction of evolutionary causation.

For a fixed architecture cost `K` and current deficit `delta=K-R(lambda_0)`, the exact static crossing condition becomes

\[
\boxed{
\mathbf c_0^\top x+\mathcal C_R>\delta.
}
\]

Thus a crossing below the tangent-only certified budget is compatible with BITA theory if a positive measured curvature dividend supplies the missing recovery.

### B4. Fixed-ray criticality and graded-dose shape

When an experiment changes coupling along one preregistered feasible direction

\[
\lambda(t)=\lambda_0-tv,
\qquad v\ge0,
\]

with fixed `K`, define the static architecture margin

\[
m(t)=R(\lambda(t))-K.
\]

Theory predicts that `m(t)` is both non-decreasing and convex. Therefore:

- the shared-to-BITA static crossing occurs at most once;
- if both negative and positive margins occur on the ray, the exact zero is a single critical point;
- a nontrivial zero plateau is compatible only when no negative side precedes it in the observed feasible ray;
- consecutive secant slopes across ordered dose levels are non-decreasing;
- a negative sampled margin followed by a positive sampled margin gives a fail-closed critical bracket;
- sign re-entry or a robust decrease in secant slopes falsifies the registered fixed-ray convex model rather than creating a second critical threshold.

Where differentiable,

\[
\frac{dm}{dt}=\mathbf c(\lambda(t))^\top v,
\]

so the projected active coupling penalty is itself predicted to stay constant or increase as decoupling progresses.

This is particularly suitable for a scalar graded coupling manipulation when a full multi-channel surface is impractical.

### B5. Three-point convex threshold refinement

Once ordered dose levels satisfy

\[
t_0<t_1<t_2,
\qquad
m_0\le m_1<0<m_2,
\]

define consecutive secant slopes

\[
s_{01}=\frac{m_1-m_0}{t_1-t_0},
\qquad
s_{12}=\frac{m_2-m_1}{t_2-t_1}.
\]

The convexity audit requires

\[
s_{01}\le s_{12}.
\]

The chord through the straddling pair crosses zero at

\[
t_L=t_1-\frac{m_1}{s_{12}},
\]

and convexity makes this a **lower bound**, not a point estimate:

\[
t_c\ge t_L.
\]

If `s_01>0`, the previous secant gives an upper bound

\[
t_U=\min\left(t_2,\;t_1-\frac{m_1}{s_{01}}\right).
\]

If `s_01=0`, use `t_U=t_2`. Therefore

\[
\boxed{t_L\le t_c\le t_U.}
\]

This can tighten the raw sign bracket `[t_1,t_2]` on both sides without fitting a quadratic or other parametric curve. If `s_01>s_12` beyond uncertainty, no refined bracket is issued; the sampled ray fails the convexity gate.

A useful sequential design is therefore:

1. locate one negative and one positive dose;
2. retain or add one earlier negative dose;
3. use the three-point convex bracket to choose the next dose level.

---

## C. Critical intervention budget

Let current static architecture deficit be

\[
\delta=K-R(\lambda_0)>0.
\]

When `K` is independently identified and fixed during the coupling manipulation, estimate the critical decoupling budget.

Under metric `Q` and curvature bounds

\[
\alpha Q\preceq\nabla^2R\preceq\beta Q,
\]

the true minimum crossing budget obeys

\[
 r_\beta(\delta,c_Q)
 \le
 \varepsilon_Q^*
 \le
 r_\alpha(\delta,c_Q).
\]

Empirical programme:

1. estimate `c_Q` locally;
2. estimate/preregister `[alpha,beta]` over the intervention range;
3. manipulate multiple budget levels spanning the predicted interval;
4. test whether crossing is absent below the no-cross region and appears by the sufficient region.

A crossing below the model's impossible-budget bound is a strong falsifier.

The fixed-ray and three-point results in B4-B5 provide shape and nonparametric threshold audits for experiments that realize these budget levels along one direction.

---

## D. Box-constrained and full-decoupling reachability

Biological coupling channels have finite removable ranges

\[
0\le x_i\le\lambda_{0i}.
\]

### D1. Saturation frontier

Under registered intervention costs, predict:

- which channel is targeted first;
- where each channel saturates;
- kinks in certified recovery-vs-effort;
- the marginal return after each saturation event.

These are directly testable intervention signatures.

### D2. Full-decoupling reachability

Use the full registered coupling vector plus curvature bounds to classify:

```text
UNREACHABLE_WITHIN_REGISTERED_DECOUPLING
FULL_DECOUPLING_GUARANTEES_CROSSING
REACHABILITY_UNRESOLVED_BY_CURVATURE_BOUNDS
```

A certified unreachable case is not a weak null result. It means coupling relief alone cannot make the registered differentiated architecture competitive within the measured coupling space.

---

## E. Residual architecture-cost requirement

If full decoupling gain lies in

\[
L_{full}\le\Delta R_{full}\le U_{full},
\]

the minimum additional independent cost relief satisfies

\[
\max(0,\delta-U_{full})
\le
\kappa_*
\le
\max(0,\delta-L_{full}).
\]

This directly tests whether a failed architecture transition is:

- coupling-limited;
- necessarily cost-limited even after maximal registered decoupling;
- unresolved between the two.

A positive lower bound on `kappa_*` quantifies the minimum architecture improvement that must come from outside the registered coupling channels.

---

## F. Joint decoupling vs K-relief intervention design

If independent intervention prices can be justified, compare coupling-channel efficiency

\[
\eta_i=c_i/a_i
\]

with cost-relief efficiency

\[
\eta_K=1/a_K.
\]

The certified weighted-L1 allocation uses lanes in descending efficiency order, respecting coupling saturation.

Prospective predictions include:

```text
COUPLING_FIRST
COST_FIRST
MIXED_AFTER_SATURATION
```

and a certified joint crossing budget.

This is an experimental-design calculation. It does not mean evolution literally pays the experimental manipulation prices.

---

## G. Which results are focal vs generality extensions?

### Pedicularis focal route can plausibly test

- one-dimensional/scalar dimensional release;
- water-state preferential loading;
- direct total-fitness consequence;
- with sufficient graded manipulation, a scalar coupling-response curve, finite curvature dividend, fixed-ray shape audit and threshold bracket/refinement.

### Later generality systems are preferable for

- multiple independently manipulable coupling channels;
- vector path-integrability/reciprocity;
- box-constrained channel-allocation kinks;
- full multi-channel reachability and joint coupling-vs-cost optimization.

The focal system should not be forced to test every mathematical extension.

## H. Promotion ladder

```text
BITA-T
nesting + coupling/recovery/criticality theory

BITA-C1/C2
same-system dimensional release + preferential loading

BITA-C3/C4/C5
fitness consequence + mechanism + independent K where claimed

BITA-G
same release/loading/mechanism and, where possible, coupling-budget signatures recur elsewhere
```

PAYOFF invasion, coexistence and ESS remain outside this ladder.
