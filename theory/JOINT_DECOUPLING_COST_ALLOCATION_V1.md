# BITA joint decoupling-cost allocation theorem v1

## Purpose

Choose how a finite intervention budget should be split between:

1. weakening residual-coupling channels; and
2. reducing independent architecture cost `K`.

The result is a prospective intervention-design theorem built on the **certified linear recovery floor**, not a claim that biological coupling relief and architecture-cost relief are the same mechanism.

## Setup

Let current active coupling penalties be

\[
c_i\ge0,
\]

and let feasible decoupling amounts satisfy

\[
0\le x_i\le\lambda_{0i}.
\]

Under convexity, decoupling has certified gain at least

\[
\sum_i c_i x_i.
\]

Let an independent cost-reduction intervention lower architecture cost by

\[
\kappa\ge0,
\]

which improves architecture margin exactly by `kappa` fitness units under the additive-cost model.

Assign intervention prices

\[
a_i>0
\]

per unit decoupling and

\[
a_K>0
\]

per unit reduction in `K`.

The total intervention budget is

\[
\sum_i a_i x_i+a_K\kappa\le B.
\]

The certified architecture-margin improvement is

\[
\boxed{
M(x,\kappa)=\sum_i c_i x_i+\kappa.
}
\]

## Theorem 1 — joint allocation is a fractional-knapsack problem

Define certified efficiencies

\[
\eta_i=\frac{c_i}{a_i}
\]

for coupling channels and

\[
\boxed{
\eta_K=\frac{1}{a_K}
}
\]

for architecture-cost relief.

The linear certified optimization

\[
\max M(x,\kappa)
\]

subject to the budget and box constraints is solved by allocating budget in descending efficiency order among:

```text
coupling channel 1   efficiency c1/a1   finite capacity lambda01
coupling channel 2   efficiency c2/a2   finite capacity lambda02
...
K relief             efficiency 1/aK    unbounded unless a biological cap is registered
```

Thus `K` relief can be treated as an additional intervention lane with unit fitness benefit and its own intervention price.

## Corollary 1a — when cost relief should be used before a coupling channel

Architecture-cost relief dominates coupling channel `i` in certified first-order benefit per intervention cost exactly when

\[
\boxed{
\frac1{a_K}>\frac{c_i}{a_i}.
}
\]

Equivalently,

\[
\boxed{
a_i>a_Kc_i.}
\]

So a biologically strong coupling channel can still be a poor intervention target if it is extremely expensive to manipulate, while modest cost relief can dominate if it is accessible.

## Corollary 1b — saturation creates mechanism switching

A high-efficiency decoupling channel is used until either:

- the intervention budget is exhausted; or
- the channel reaches its biological cap `lambda_0i`.

After saturation, budget moves to the next-highest remaining efficiency, which may be `K` relief.

Hence the optimal intervention mechanism can switch with budget size even when all biological coefficients stay fixed.

## Theorem 2 — certified joint-margin frontier is concave and piecewise linear

Let

\[
V_{joint}(B)
=
\max_{x,\kappa}M(x,\kappa)
\]

under the weighted-L1 budget.

Because finite coupling channels are consumed in decreasing efficiency order and `K` relief supplies a constant-efficiency fallback lane, `V_joint(B)` is:

- nondecreasing;
- continuous;
- piecewise linear;
- concave.

Its marginal certified return is the efficiency of the currently active intervention lane and therefore never increases with budget.

If `K` relief is uncapped, the long-run marginal return approaches

\[
\boxed{1/a_K}
\]

after all coupling channels with higher efficiency have saturated.

## Theorem 3 — minimum certified budget to overcome a current deficit

Let current static architecture deficit be

\[
\delta=K-R(\lambda_0)>0.
\]

Any budget `B` satisfying

\[
\boxed{V_{joint}(B)>\delta}
\]

guarantees a static architecture crossing under the certified convexity floor and additive-cost assumptions.

The infimum certified crossing budget is therefore

\[
\boxed{
B_{cert}
=
\inf\{B:V_{joint}(B)\ge\delta\}.
}
\]

It is obtained directly from the piecewise-linear efficiency/saturation schedule.

## Theorem 4 — mechanism diagnosis from the optimal schedule

The schedule provides a prospective classification of what limits the architecture transition:

### `COUPLING_FIRST`

At least one coupling channel has

\[
\eta_i>\eta_K.
\]

The cheapest certified route begins by decoupling.

### `COST_FIRST`

\[
\eta_K>\max_i\eta_i.
\]

The cheapest certified route begins by reducing architecture cost rather than further decoupling.

### `MIXED_AFTER_SATURATION`

High-efficiency coupling channels are used first, but after saturation the optimum switches to cost relief or weaker coupling channels.

This is an intervention-design classification, not an evolutionary-history claim.

## Corollary — value of separately identifying R and K

If only the net gap

\[
\Delta_W=R-K
\]

is observed, the coefficients needed for the allocation theorem are unavailable:

- channel-specific `c_i` belongs to the recovery surface `R`;
- `a_K` refers to manipulation of the independent cost lane `K`.

Thus the earlier nonidentifiability theorem is not merely a semantic concern. Separating `R` and `K` is required to decide **which mechanism is worth targeting**.

## Empirical consequence

A causal BITA programme can estimate:

1. active coupling penalties `c_i` from multi-level coupling manipulation;
2. available coupling ranges `lambda_0i`;
3. intervention costs/effort weights `a_i` declared independently of outcomes;
4. architecture-cost manipulation price `a_K`, if a genuine independent cost lane exists;
5. current architecture deficit `delta`.

These quantities generate a preregistered intervention schedule and certified crossing budget.

Observed responses can then be compared against the schedule without retroactively selecting the easiest-looking channel.

## Claim ceiling

The theorem optimizes the certified **linear lower bound**. Positive curvature in `R` can make decoupling more valuable than this conservative schedule predicts, so the result is sufficient rather than globally exact for nonlinear recovery. Intervention prices are experimental/developmental effort metrics, not fitness costs unless explicitly calibrated. Reducing `K` must not alter `R` for the additive decomposition used here. PAYOFF invasion and coexistence remain separate.
