# Declared design power readout v1

Simulation of the pre-registered moderator design, run through the deployed analysis
functions. 2,000 replicates per cell. Reproduce with:

```bash
python scripts/run_declared_design_power.py empirical/design_power 2000
```

Detection rates are properties of the declared design and the committed code under a declared
generative model. They are not evidence about nature and do not estimate any route effect.

## 1. Why this was run before extraction

The protocol's capacity thresholds ("three independent clusters per moderator level") grant
*permission to estimate*. They say nothing about whether an estimate at that size can separate a
real context effect from noise. If it cannot, a future null result would be uninformative, and
the time to find that out is before the reading queue is worked, not after.

## 2. Two defects the simulation exposed

Both were in code committed earlier in this branch. Both are fixed, and both now have regression
guards in `tests/test_design_power.py`.

**The between-level test was invalid.** The classic `Q_between` statistic was computed from
fixed-effect weights, which treat all within-level scatter as sampling noise. Under the null of
no level effect its rejection rate is:

| between-cluster SD `tau` | fixed-effect `Q_between` rejection rate |
|---|---|
| 0.00 | 0.044 – 0.052 |
| 0.25 | 0.268 – 0.296 |
| 0.50 | 0.518 – 0.596 |

At any heterogeneity this literature plausibly carries, that statistic rejects a true null more
often than not. What had looked like high power in the first grid run was largely false-positive
rate. `Q_between` is now computed and reported as a descriptive partition of heterogeneity, is
labelled `descriptive_only_not_used_for_inference`, and issues no verdict. Inference for a
categorical moderator comes from the random-effects meta-regression contrast, whose false-positive
rate across the same null grid peaks at **0.062** against a nominal 0.05.

**The direction-reversal verdict fired on noise.** The rule required only that two pooled levels
differ in sign. With a true level effect of exactly zero, pooled directions differ by chance about
half the time, so the verdict `context_dependent_direction_reversal` — the strongest claim the
analysis can make — appeared in **21% to 35%** of null replicates. The rule now additionally
requires both level intervals to exclude zero with opposite signs. Its null rate across the same
grid peaks at **0.014**.

## 3. Power of the corrected design

Smallest cluster count per moderator level reaching 80% power on the calibrated test:

| true level contrast (log response ratio) | `tau` = 0.00 | `tau` = 0.25 | `tau` = 0.50 |
|---|---|---|---|
| −0.35 (about a 30% drop in pollinator use) | 8 | not reached by 12 | not reached by 12 |
| −0.69 (a halving) | 3 | 5 | 12 |
| −1.10 (about a two-thirds reduction) | 3 | 3 | 5 |

## 4. What this changes in the pre-registration

The declared minimum of three clusters per level detects a halving-or-larger contrast only when
between-study heterogeneity is near zero. That is not a safe assumption here, so the protocol is
revised:

- the primary dose-realism moderator and the assay-context moderator move to **5 clusters per
  level, 10 clusters total**;
- the exploratory pollinator-group moderator stays at 3 per level and is explicitly labelled as
  detecting only large contrasts;
- the protocol now carries a **declared detectable effect**: at the revised thresholds the design
  targets level contrasts of about 0.69 or larger on the log-response-ratio scale, and a null
  result does not exclude a contrast of 0.35.

That last sentence is the point of running this before extraction. It is the difference between
reporting "no context dependence detected" and reporting "no context dependence detected, at a
design that could not have detected a 30% shift anyway."

## 5. Boundary

The generative model is declared, not fitted: effects are normal around a level mean with
between-cluster SD `tau`, and per-study standard errors are uniform on [0.10, 0.30]. Real
extractions may have different precision, in which case these thresholds should be recomputed
with the observed distribution rather than reused.
