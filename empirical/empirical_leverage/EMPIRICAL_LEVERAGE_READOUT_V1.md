# Empirical leverage readout v1: what the constituent-pathway estimate would settle

Reproduce with:

```bash
python scripts/run_empirical_leverage.py \
  configs/part_i_robustness_grid.json 0.45 0.25 empirical/empirical_leverage
```

The interval centre 0.45 is the implemented corollary's declared scaffold value for
`defence_pollinator_cost`. It is **not** an estimate. When the meta-analysis produces a pooled
log response ratio, convert it with `cost_from_log_response_ratio` and re-run with the real
interval.

## 1. The question

The declared empirical target estimates one parameter, `c_D`. Before spending the extraction
effort, it is worth knowing what an estimate of that parameter can buy. For each point of the
declared phenotype-and-regime grid, this analysis asks which values of `c_D` make the local
interaction complementary, and how tight an interval around `c_D` must be before that point's
sign is settled.

## 2. The boundary is a window, not a threshold

Setting `S = P b_A (1 - c_R R)` and `K = (H d_A e_F - c_AD) / S`, the sign condition is

```text
W_AD > 0   <=>   K > c_D * exp(-c_D * D).
```

The right-hand side is not monotone in `c_D`: it peaks at `c_D = 1/D` with value `1/(D e)`, then
decays. So for `0 < K < 1/(D e)` the complementary set is `c_D < c_low` **or** `c_D > c_high`.

The upper branch is real, not a numerical artefact: a very large pollinator cost drives
`exp(-c_D D)` toward zero, the mutualist channel is almost entirely shut off at the focal defence
level, and its cross curvature vanishes with it. It is reported rather than truncated, and an
interval that spans the whole window is flagged `unsettled_interval_spans_boundary` even though
both of its endpoints agree — a sign flip is hidden strictly inside it.

The closed form is checked against finite-difference mixed partials of the implemented model at
378 grid-and-parameter combinations, including the upper branch, in
`tests/test_empirical_leverage.py`.

## 3. Result: 45% of the declared grid cannot be moved by this measurement

Of 216 declared grid points, **97 are insensitive to `c_D` altogether**. Their sign is fixed by
antagonist relief and joint-cost curvature regardless of the pollinator-cost parameter: 36 are
substitutable for every `c_D` (the high-obstruction, high-shared-cost scenario), and 61 are
complementary for every `c_D`.

This is a useful negative result. Those points are not waiting on the meta-analysis at all. They
are governed by the other two channels and require a different measurement — which is exactly
what the manuscript's factorial design recommendation is for.

## 4. Result: precision, not direction, is the binding constraint

Fraction of the declared grid whose sign classification is settled, as a function of the
half-width of the `c_D` interval:

| interval half-width on `c_D` | unsettled points | settled fraction |
|---|---|---|
| 0.05 | 5 | 0.977 |
| 0.10 | 18 | 0.917 |
| 0.20 | 43 | 0.801 |
| 0.40 | 91 | 0.579 |
| 0.80 | 105 | 0.514 |

Against the precision a meta-analysis of this size can actually deliver. Taking the generative
model of the power analysis (per-study standard error near 0.20 on the log-response-ratio scale)
and a manipulated defence contrast of 0.5 on the declared 0–1 trait scale, the achievable
half-width on `c_D` is:

| independent clusters | `tau` = 0.00 | `tau` = 0.25 | `tau` = 0.50 |
|---|---|---|---|
| 5 | 0.351 | 0.561 | 0.944 |
| 12 | 0.226 | 0.362 | 0.609 |
| 20 | 0.175 | 0.281 | 0.472 |
| 50 | 0.111 | 0.177 | 0.299 |

## 5. What this means for the claim the empirical half can make

Reading the two tables together: at the cluster counts this literature plausibly supports, the
constituent-pathway meta-analysis can establish the **direction** of the route and whether that
direction is **context dependent**. It cannot resolve the regime map. Settling 80% of the
`c_D`-sensitive grid needs a half-width of 0.20, which requires roughly 20 clusters at zero
heterogeneity and is out of reach at `tau = 0.5` for any cluster count in this table.

So the empirical half of the project should be stated as: one channel's realised direction and
context dependence, anchored across independent studies — not as an empirically resolved
complementarity map. That was already the declared inference boundary in
`docs/IOTA_PATHWAY_EMPIRICAL_TARGET.md`; this analysis puts numbers behind it and shows the
boundary is imposed by achievable precision, not by caution.

## 6. Boundary

This is a property of the declared corollary and the declared finite grid. It states which sign
classifications a given precision on `c_D` would settle. It is not an estimate of `c_D`, not
evidence about nature, and not a statement about how common either sign is. Grid fractions are
unweighted occupancies of the declared finite design, consistent with the Part I convention.

The attraction axis of the Part I grid is omitted here: in the implemented corollary `A` enters
every channel linearly, so it cancels from the mixed partial and would only replicate identical
rows.
