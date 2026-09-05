# BITA Peucedanum Stage-B operational sampling plan v1

## Purpose

This document plans **operational sample coverage**, not statistical power for the unknown causal optimum-shift estimand `Delta_q*`.

The current Stage-B experiment has:

```text
3 q levels x 2 antagonist states = 6 cells.
```

The primary analysis requires a validated q manipulation, explicit assignment ledger, attrition audit, and enough observed outcomes in every cell to estimate the two q-fitness surfaces and their mechanism chain.

Registered calculator:

```text
scripts/plan_peucedanum_stage_b_sampling.py
```

## Empirical scale anchor

The current published-numeric receipt records the 2025 high-predation focal study at:

```text
n = 106 plants
predation rate without egg removal = 0.57 +/- 0.28
egg-removal fruit set = 0.51 +/- 0.35
estimated final fruit set without removal = 0.19 +/- 0.16.
```

That study supplies a useful field-scale feasibility anchor but **does not identify the Stage-B `Delta_q*` effect size**. It therefore cannot justify a formal power calculation for the new randomized q x G experiment.

A target of:

```text
18 observed outcomes per cell x 6 cells = 108 analyzable outcomes
```

is deliberately close to the published `n=106` empirical scale. This is a coverage anchor, not proof that `n=108` has any particular power for `Delta_q*`.

## Why expected sample size is not enough

Suppose post-randomization outcome attrition is 15%.

A naive expectation calculation gives:

```text
ceil(18 / 0.85) = 22 randomized per cell.
```

This yields:

```text
expected observed per cell = 22 x 0.85 = 18.7.
```

But expectation is misleading. Under independent Bernoulli retention, with 22 randomized per cell:

```text
P(one cell retains >=18) ~= 0.774
P(all 6 cells retain >=18) ~= 0.215.
```

Thus `22/cell = 132 total` has only about a 21% chance of meeting the 18-per-cell target simultaneously in all six cells under the planning model.

## Recommended post-randomization target

### 80% joint cell-coverage target

With 15% anticipated attrition:

```text
25 randomized per cell
= 150 randomized total
expected observed per cell = 21.25
P(all 6 cells >=18) ~= 0.857.
```

### 90% joint cell-coverage target

With the same attrition:

```text
26 randomized per cell
= 156 randomized total
expected observed per cell = 22.10
P(all 6 cells >=18) ~= 0.938.
```

Because one additional randomization block adds only six plants but raises joint operational coverage materially, the preferred confirmatory target is:

```text
26 complete randomization blocks
x 6 cells
= 156 G-randomized plants.
```

The outcome analysis does **not** require all 26 blocks to remain complete; the attrition-aware V2 analyzer retains incomplete outcome blocks and audits missingness through the assignment ledger.

## Pre-G q-manipulation qualification reserve

The 156 plants above are the number that should reach **qualified q manipulation and G randomization**. Field recruitment must additionally allow some q manipulations to fail the preregistered realization / classification / damage gates before G assignment.

For the preferred 26-per-cell plan:

```text
qualified G-randomizable units needed per q level
= 26 x 2 G states
= 52.
```

If pre-G q-manipulation qualification failure is anticipated at 10%, and the goal is at least 90% joint probability that all three q pools contain >=52 qualified units, the binomial coverage calculation gives:

```text
63 initial candidates per q level
x 3 q levels
= 189 initial candidates.
```

Thus the practical two-stage field target is:

```text
initial candidates:     189  (63 per q treatment)
            ↓ q validation / qualification
G-randomized target:    156  (26 per q x G cell)
            ↓ post-randomization outcome attrition
analysis target:        >=108 (>=18 observed per cell)
```

These stages must be recorded separately. Pre-G qualification failure is not post-randomization attrition.

## Scenario table

| Target observed / cell | Post-G attrition | Joint target across 6 cells | Randomize / cell | Randomized total |
|---:|---:|---:|---:|---:|
| 18 | 10% | >=80% | 23 | 138 |
| 18 | 10% | >=90% | 24 | 144 |
| 18 | 15% | >=80% | 25 | 150 |
| 18 | 15% | >=90% | 26 | 156 |
| 20 | 15% | >=80% | 28 | 168 |
| 20 | 15% | >=90% | 29 | 174 |

The 18-per-cell / 15% / 90% line is the current preferred confirmatory planning point.

## Pilot before freezing the full design

The following quantities are still unknown and should be learned in a small Stage-B technical pilot before the confirmatory thresholds are frozen:

```text
achievable q levels and q realization error
pre-G sex-classification accuracy
pre-G qualification failure rate
post-randomization outcome attrition rate
cell-specific attrition imbalance
frequency of initial_fruits > 0
variance of final intact fruit output
variance and recoverability of paternity-based male fitness.
```

The pilot is for logistics and variance / attrition estimation. It should not be used to choose a favorable confirmatory sign threshold after seeing the primary outcome.

A reasonable first technical pilot is approximately:

```text
6-8 candidate plants per q level
= 18-24 plants total
```

for manipulation feasibility alone, before the full q x G crossing is deployed.

## Claim boundary

The planner assumes independent Bernoulli qualification / retention probabilities only to translate operational loss rates into recruitment counts. Real attrition may be correlated within block or treatment, which is why the confirmatory analysis still requires an empirical attrition audit.

This is not a formal power analysis for `Delta_q*`. A formal power or simulation-based design becomes defensible only after pilot information supplies a preregistered plausible effect surface and variance structure without using the final confirmatory outcomes themselves.
