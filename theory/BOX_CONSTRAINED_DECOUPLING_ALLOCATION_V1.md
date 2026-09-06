# BITA box-constrained decoupling allocation theorem v1

## Purpose

Extend optimal decoupling from unconstrained norm balls to biologically feasible interventions that cannot remove more coupling from a channel than currently exists.

For current residual coupling `lambda_0`, any decoupling move must satisfy

\[
0\le x_i\le \lambda_{0i}.
\]

This box constraint is unavoidable in real interventions and changes the optimal allocation once high-value channels saturate.

## Linearized recovery objective

At the current state let

\[
c_i=-\frac{\partial R}{\partial\lambda_i}\ge0.
\]

The certified first-order/convex finite-gain floor is

\[
G(x)=\mathbf c^\top x.
\]

We optimize this guaranteed gain subject to intervention budget and box feasibility.

---

## Part I — weighted L1 budget

Let intervention costs per unit decoupling be `a_i>0` and impose

\[
\sum_i a_i x_i\le B,
\qquad
0\le x_i\le\lambda_{0i}.
\]

### Theorem 1 — greedy saturation is globally optimal

Define channel efficiency

\[
\boxed{\eta_i=\frac{c_i}{a_i}.}
\]

Order channels so that

\[
\eta_{(1)}\ge\eta_{(2)}\ge\cdots\ge\eta_{(m)}.
\]

Then an optimal solution is obtained by:

1. fully decoupling channel `(1)` until either it saturates at `lambda_(1)` or the budget is exhausted;
2. then channel `(2)`;
3. continue in decreasing `eta` order;
4. at most one channel is partially filled before the budget is exhausted.

This is the continuous/fractional-knapsack solution.

### Proof sketch

Suppose a feasible solution spends positive budget on channel `j` while a more efficient channel `i` with `eta_i>eta_j` is not saturated. Moving an infinitesimal budget amount from `j` to `i` increases gain by the positive difference in efficiency. Therefore no optimum can have lower-efficiency allocation while a higher-efficiency channel remains unsaturated.

### Corollary 1a — piecewise-linear recovery frontier

As budget `B` increases, maximum certified gain is continuous, non-decreasing and piecewise linear. Its slope is the efficiency of the currently marginal unsaturated channel.

Hence marginal returns weakly decrease as the best channels saturate.

---

## Part II — diagonal quadratic / L2-type budget

Let intervention effort be

\[
\sum_i q_i x_i^2\le\varepsilon^2,
\qquad q_i>0,
\]

with the same box constraints.

Without boxes, the optimal direction is

\[
x_i\propto\frac{c_i}{q_i}.
\]

### Theorem 2 — capped proportional active-set solution

There exists `tau>=0` such that an optimal solution has

\[
\boxed{
x_i^*=\min\left\{\lambda_{0i},\ \tau\frac{c_i}{q_i}\right\}.}
\]

If the budget constraint is active, `tau` is chosen so that

\[
\sum_iq_i(x_i^*)^2=\varepsilon^2.
\]

Thus unsaturated channels retain the unconstrained proportional rule, while channels whose requested decoupling exceeds available coupling are capped at their biological maximum.

### KKT interpretation

For unsaturated channels, stationarity gives

\[
c_i=2\mu q_i x_i,
\]

so all have the same proportionality constant `tau=1/(2mu)`. Saturated channels leave the active proportional set and contribute fixed decoupling.

### Corollary 2a — active-set monotonicity

As budget increases, once a channel saturates it remains saturated. The active unsaturated set can only shrink.

Therefore the optimal intervention path is piecewise smooth with kinks at channel-saturation budgets.

---

## Part III — full decoupling ceiling

The maximum feasible decoupling vector is

\[
x=\lambda_0.
\]

Its certified convex finite-gain floor is

\[
\boxed{G_{max}^{floor}=\mathbf c_0^\top\lambda_0.}
\]

If the current architecture deficit satisfies

\[
\delta\ge G_{max}^{upper},
\]

where `G_max^upper` is any valid curvature-based upper bound on gain from full decoupling, then **no physically feasible decoupling intervention can cross** under the registered model.

Conversely, if the certified lower gain from some feasible allocation exceeds `delta`, that allocation guarantees a static crossing.

## Experimental interpretation

The theorem gives a concrete intervention order:

```text
L1 / linear cost     -> highest gain-per-cost channels first, saturating sequentially
L2 / quadratic cost  -> spread effort proportional to c_i/q_i, then cap saturated channels
```

So “which integration mechanism should be experimentally weakened first?” is not a verbal judgment. It depends on:

- active coupling penalty `c_i`;
- intervention cost geometry;
- available amount of coupling `lambda_0i`.

## Claim ceiling

The allocation theorem optimizes the certified linear gain floor at the current state. Under convex R the realized finite gain is at least this floor, but the truly gain-maximizing finite intervention can differ because curvature varies across directions. The L2 capped formula assumes a diagonal quadratic cost; correlated intervention costs require the general constrained quadratic program. Architecture cost `K` must remain fixed for static crossing statements. PAYOFF invasion dynamics remain separate.
