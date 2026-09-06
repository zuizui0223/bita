# BITA box-constrained certified-recovery frontier v1

## Purpose

Characterize how the maximum certified decoupling gain changes as intervention budget increases when coupling channels saturate at their biological limits.

The object is the optimal value of the linear certified gain floor

\[
V(B)=\max_x \mathbf c^T x
\]

under a declared intervention-cost geometry and box constraints

\[
0\le x_i\le\lambda_{0i}.
\]

This is an intervention-design frontier, not a claim about the full nonlinear realized gain.

---

## Part I — weighted L1 cost

Let

\[
\sum_i a_i x_i\le B,
\qquad a_i>0,
\]

and define efficiencies

\[
\eta_i=c_i/a_i.
\]

Order channels by decreasing efficiency.

### Theorem 1 — piecewise-linear concave frontier

The greedy saturation theorem implies that `V(B)` is:

- non-decreasing;
- continuous;
- piecewise linear;
- concave in `B`.

Its right derivative, wherever defined, is the efficiency of the currently marginal unsaturated channel:

\[
\boxed{
V_+'(B)=\eta_{m(B)}.
}
\]

Because channels are entered in decreasing efficiency order, this marginal return can only fall as budget increases.

### Corollary 1a — saturation breakpoints

If channels are ordered `(1),(2),...`, cumulative saturation costs are

\[
B_k=\sum_{r=1}^k a_{(r)}\lambda_{0,(r)}.
\]

These are the kinks of the certified-recovery frontier. Between `B_{k-1}` and `B_k`, only channel `(k)` is marginal.

### Corollary 1b — no benefit beyond full useful decoupling

Let

\[
B_{max}=\sum_{i:c_i>0}a_i\lambda_{0i}.
\]

For

\[
B\ge B_{max},
\]

all positive-gain channels are saturated and

\[
\boxed{V(B)=\sum_i c_i\lambda_{0i}.}
\]

Extra intervention budget has zero certified linear value unless the biological model itself changes.

---

## Part II — diagonal quadratic cost

Let

\[
\sum_i q_i x_i^2\le E,
\qquad q_i>0,
\]

where `E=epsilon^2` is squared effort budget.

For a fixed saturated set `S` and unsaturated set `U`, define

\[
Q_S=\sum_{i\in S}q_i\lambda_{0i}^2,
\]

\[
C_S=\sum_{i\in S}c_i\lambda_{0i},
\]

and

\[
A_U=\sum_{i\in U}\frac{c_i^2}{q_i}.
\]

### Theorem 2 — exact frontier between saturation events

Within a region where the active saturated set does not change, the KKT solution gives

\[
\boxed{
V(E)
=
C_S+
\sqrt{A_U(E-Q_S)}
}
\]

for `E>=Q_S`.

Thus `V` is concave in **squared intervention effort** `E` between saturation events.

Its marginal value is

\[
\boxed{
\frac{dV}{dE}
=
\frac{\sqrt{A_U}}{2\sqrt{E-Q_S}}.
}
\]

This decreases as effort grows while the active set is fixed.

### Corollary 2a — biological saturation reduces the active dual norm

When a channel saturates it leaves `U`, so

\[
A_U=\sum_{i\in U}c_i^2/q_i
\]

weakly decreases.

Hence later intervention phases are supported by a smaller pool of unsaturated active coupling penalties.

### Theorem 3 — global continuity across saturation events

The capped-proportional KKT solution is continuous as a channel reaches its box limit. Therefore the value frontier `V(E)` is continuous across active-set changes, though its derivative can kink.

These kinks identify points where a biologically limiting coupling channel becomes fully removed and the intervention must redirect effort to remaining channels.

---

## Part III — crossing budget on the certified frontier

Let current architecture deficit be

\[
\delta=K-R(\lambda_0)>0.
\]

If

\[
V(B)>\delta
\]

for an L1 budget, or

\[
V(E)>\delta
\]

for a quadratic budget, the convex finite-gain theorem guarantees a static crossing.

Therefore the smallest budget at which the **certified frontier** exceeds `delta` is a sufficient physically feasible crossing budget incorporating channel saturation.

If an independent curvature-based upper frontier remains below `delta` even at full decoupling, crossing is impossible within the registered architecture and coupling range.

## Biological interpretation

This gives BITA a diminishing-return intervention geometry:

```text
small budget   -> target highest-value coupling channels
channel saturates
larger budget  -> redirect effort to weaker remaining channels
all useful channels saturated -> certified gain ceiling
```

The order and breakpoints are mechanistically interpretable because they depend on active coupling penalties, intervention cost and current available coupling.

## Empirical consequence

A multi-channel manipulation can prospectively predict:

- which channel should saturate first;
- where recovery-vs-effort kinks should occur;
- the marginal gain before and after each kink;
- whether the available intervention range can ever certify a static architecture crossing.

Observed smooth gains with no predicted kink, or a kink at the wrong saturation threshold, would challenge the registered coupling/cost model.

## Claim ceiling

`V` is the frontier of the certified **linear** gain floor. Convex nonlinear recovery can make realized gain larger. The theorem assumes fixed current penalty coefficients for allocation ranking and the declared box/cost constraints. Re-optimizing the allocation using updated penalties after large interventions is a sequential-control extension. PAYOFF invasion and establishment remain separate.
