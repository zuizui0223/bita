# Kessler-type replication and augmentation plan v1

## Decision

The next BITA experiment must separate **detecting a positive A×D interaction** from **demonstrating that defence actually releases a non-beneficial attraction state**. Kessler et al. (2008) already supplies a manipulated attraction-by-defence-like surface and a robust positive aggregate sign. The new partial-identification audit further shows that `A1` is positive under all declared aggregate-compatible allocations, while `A0` remains confined to about ±3 percentage points around zero.

That changes the design problem. A modest four-cell replication can identify Level 1. A strict Level-2/3 confirmation can be orders of magnitude more demanding when the true `A0` is near zero.

The staged programme is therefore:

```text
Stage 1a  identify total interaction relief (Delta_AD > 0)
Stage 1b  estimate A0/A1 and test whether strict Level 2/3 is statistically identifiable
Stage 2   pilot selective consumer-channel contrasts
Stage 3   power and run the full mechanism-allocation design only if needed
```

## Stage 1a — total interaction relief

Define

```text
A0       = W10 - W00
A1       = W11 - W01
Delta_AD = A1 - A0
```

Level-1 primary estimand:

```text
Delta_AD W = W11 - W10 - W01 + W00
```

Level-1 decision rule:

```text
two-sided 95% CI for additive probability-scale Delta_AD lies wholly above zero
```

The existing prospective planner remains valid for this narrower target:

| planning scenario | Delta_AD | power | design effect | retention | planned n/cell | total 4-cell n |
|---|---:|---:|---:|---:|---:|---:|
| published central | +0.22 | 0.80 | 1.5 | 0.90 | 154 | 616 |
| published central | +0.22 | 0.90 | 1.5 | 0.90 | 207 | 828 |
| attenuated | +0.17 | 0.80 | 1.5 | 0.90 | 250 | 1000 |
| attenuated | +0.17 | 0.90 | 1.5 | 0.90 | 334 | 1336 |
| smaller | +0.12 | 0.80 | 1.5 | 0.90 | 480 | 1920 |

These numbers power **Level 1 only**. They must not be presented as power for constraint release, sign reversal, or channel allocation.

## Stage 1b — strict Level-2/3 release is a different power problem

The registered sufficient outcome rules are

```text
Level 2: upper95(A0) <= 0 and lower95(A1) > 0
Level 3: upper95(A0) <  0 and lower95(A1) > 0
```

Under a continuous normal planning approximation, the `<=0` versus `<0` distinction has zero probability mass at the interval endpoint, so Level 2 and Level 3 have the same prospective decision probability for fixed true cell probabilities.

### Boundary problem at A0 = 0

The historical central planning state has

```text
p11 = .35
p10 = .13
p01 = .13
p00 = .13

A0 = 0
A1 = +.22
```

If true `A0=0`, no increase in sample size can make a two-sided 95% interval satisfy `upper95(A0) <= 0` with 80% or 90% probability. As sample size grows, the maximum probability of that one boundary event approaches

```text
alpha/2 = 0.025.
```

This is not a software limitation. It follows from trying to certify a nonpositive effect when the true value sits exactly on the zero boundary. Therefore the historical central Kessler scenario is **not high-power identifiable as strict Level 2/3 under the registered zero-bound CI rule**, even though Level 1 is easy to power.

### Negative-A0 sensitivity

The planner now includes prospective sensitivity scenarios in which the undefended attraction effect is genuinely negative. These are not historical effect estimates.

For `A1 = +0.22`:

| prospective scenario | A0 | target joint power | effective n/cell | planned n/cell, DE=1.5 retention=.90 | 4-cell total |
|---|---:|---:|---:|---:|---:|
| boundary | 0.00 | .80/.90 | not attainable | not attainable | not attainable |
| weak negative | -0.03 | .80 | 1772 | 2954 | 11816 |
| weak negative | -0.03 | .90 | 2372 | 3954 | 15816 |
| moderate negative | -0.05 | .80 | 587 | 979 | 3916 |
| moderate negative | -0.05 | .90 | 785 | 1309 | 5236 |

The driver is almost entirely the precision needed on `A0`; `A1=+0.22` is comparatively easy to establish as positive. As `A0` approaches zero from below, the required sample size diverges rapidly.

This implies a practical design choice:

```text
if the scientific goal is Level 1:
    Kessler-like replication is tractable at hundreds of observations

if the scientific goal is strict Level 2/3 and A0 is near zero:
    simply enlarging the same experiment becomes inefficient

if a strong release claim is essential:
    prioritize a system / contrast with a clearly negative undefended A effect,
    or justify a different prospective practical-release estimand before data collection
```

## No post-hoc epsilon rescue

One could define a practical-release rule such as

```text
upper95(A0) <= epsilon
lower95(A1) > 0
```

for a positive biologically justified margin `epsilon`. That is a legitimate prospective noninferiority-style target, but it is **not strict Level 2** as currently defined. The historical Kessler identified-set width of about 0.03 must not be reused post hoc as the margin merely because it makes the result pass.

If an epsilon target is scientifically needed, the margin must be justified independently before confirmatory data are examined and the resulting claim must be labelled practical/approximate release rather than strict nonpositive-to-positive release.

## Trait-intervention requirement

The original Kessler design has an organ-scope caveat because nicotine suppression was systemic. A confirmatory replication should predeclare one of two ceilings:

1. **source-faithful replication** — retain the original intervention architecture and accept that D is not flower-exclusive; or
2. **identification-oriented replication** — use a floral-local or flower-restricted manipulation calibrated to the natural nicotine/repellent range and verify that vegetative defence state is unchanged.

The second is preferable for BITA's functional-release interpretation. The A and D contrasts must remain identical across all later consumer states. Changing dose, delivery, flower age, reward volume, or tissue state when consumer treatments are added changes the estimand.

## Experimental units and uncertainty

The historical source does not expose enough information to recover day/plant dependence. Planning therefore represents dependence through an explicit design-effect sensitivity rather than treating flowers as truly independent.

A prospective experiment should record at minimum:

```text
plant ID
flower ID
day / block
A treatment
D treatment
consumer treatments when present
flower age / phenology
capsule success
seed number or another predeclared secondary reproductive endpoint
```

Randomization and analysis must preserve plant/day/block structure. Final intervals must come from the actual randomized design or a prespecified hierarchical model, not the independent-normal planning approximation.

## Why not power all 16 cells from the Kessler effect?

The total four-cell `Delta_AD` does not identify effect sizes for

```text
A x D x antagonist
A x D x pollinator
A x D x antagonist x pollinator.
```

Multiplying a Stage-1 `n/cell` into 16 cells is therefore only a budget extrapolation. This is even more important after the Level-2/3 audit: copying a strict-release sample size into 16 mechanism cells could imply tens of thousands of observations without providing a valid mechanism power calculation.

## Stage 2 — pilot the missing channel contrasts

Only after Stage 1 estimates the outcome surface should selective consumer toggles be added on the same A/D coordinates. The first augmentation block should estimate variance/effect scales for

```text
rho_delta candidate: A x D dependence of antagonist-mediated loss
iota_delta candidate: A x D dependence of pollinator-mediated benefit
m0_delta: A x D interaction in pollinator-absent reproduction
four-way coupling: A x D x antagonist x pollinator
```

Consumer interventions must be selective. A generic exclusion treatment that simultaneously alters pollinator and antagonist access identifies neither channel cleanly.

Do not borrow the Kessler total Delta as a three- or four-way mechanism effect size.

## Stage 3 — full mechanism allocation

A confirmatory mechanism experiment then crosses

```text
A x D x antagonist x pollinator
```

with a measured pollinator-absent baseline, four-way separability diagnostic, uncertainty propagation for derived channels, and an independent A×D joint-cost/allocation assay rather than naming a reproductive residual as cost.

The interpretation order is now explicit:

```text
Does D improve the return to A?             -> Level 1 / Delta_AD
Does D make non-beneficial A beneficial?    -> Level 2 / A0,A1
Is the change strictly negative-to-positive?-> Level 3 / A0,A1
Why does the sign change?                   -> rho/iota/kappa allocation
```

## Stop and promotion rules

- `Delta_AD` interval wholly above zero: Level 1 identified. Legacy token `ESCAPE_IDENTIFIED` may be emitted only as a backwards-compatible Level-1 alias.
- `upper95(A0) <= 0` and `lower95(A1) > 0`: Level 2 identified.
- `upper95(A0) < 0` and `lower95(A1) > 0`: Level 3 identified.
- If A1 is positive but A0 remains zero-compatible: report **partial identification**, not failed escape and not strict release.
- If the total interaction crosses zero: Level 1 unresolved; favourable marginal channels cannot override it.
- A positive mechanism pilot does not manufacture an unsupported outcome level.

The generating code is `scripts/plan_kessler_type_replication.py`; its current output contains separate Level-1 and Level-2/3 planning tables.
