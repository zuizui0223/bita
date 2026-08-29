# Kessler-type replication and augmentation plan v1

## Decision

The next BITA experiment should not be described as searching for the first manipulated attraction-by-defence surface. Kessler et al. (2008) already supplies that surface and a robust positive female aggregate sign. The unresolved step is to obtain a **design-based uncertainty-bearing total interaction**, then allocate that interaction mechanistically only if the first gate is passed.

This implies a staged design rather than immediately multiplying the four-cell trait experiment into an underpowered 16-cell mechanism experiment.

## Stage 1 — confirm the total escape sign

Primary estimand:

```text
Delta_AD W = W11 - W10 - W01 + W00
```

Primary decision rule:

```text
two-sided 95% CI for additive probability-scale Delta_AD W lies wholly above zero
```

For a Kessler-like female outcross capsule endpoint, the registered prospective planner gives:

| planning scenario | Delta_AD | power | design effect | retention | planned n/cell | total 4-cell n |
|---|---:|---:|---:|---:|---:|---:|
| published central | +0.22 | 0.80 | 1.5 | 0.90 | 154 | 616 |
| published central | +0.22 | 0.90 | 1.5 | 0.90 | 207 | 828 |
| attenuated | +0.17 | 0.80 | 1.5 | 0.90 | 250 | 1000 |
| attenuated | +0.17 | 0.90 | 1.5 | 0.90 | 334 | 1336 |
| smaller | +0.12 | 0.80 | 1.5 | 0.90 | 480 | 1920 |

The 0.22 scenario reproduces the published central female proportions approximately as 0.35 versus 0.13/0.13/0.13. The 0.17 and 0.12 scenarios are attenuation sensitivities, not claims about the historical source.

The machine-readable receipt is `empirical/identification_design/KESSLER_TYPE_REPLICATION_POWER_V1.json`; the generating code is `scripts/plan_kessler_type_replication.py`.

## Trait-intervention requirement

The original Kessler design has a known organ-scope caveat because nicotine suppression was systemic. A confirmatory replication should therefore predeclare one of two claim ceilings:

1. **source-faithful replication** — retain the original intervention architecture and accept that the D intervention is not flower-exclusive; or
2. **identification-oriented replication** — use a floral-local or flower-restricted manipulation calibrated to the natural nicotine/repellent range, and verify that vegetative defence state is not altered by the D treatment.

The second option is preferable for the BITA escape interpretation. The exact manipulation technology is a biological implementation choice; the analysis contract does not assume that a specific local method is already validated.

The A and D contrasts must remain identical across all later consumer states. Changing chemical dose, delivery method, flower age, reward volume, or tissue state when consumer treatments are added changes the estimand.

## Experimental units and uncertainty

The historical source does not expose enough information to recover day/plant dependence. Therefore the power planner treats dependence through an explicit design-effect sensitivity rather than pretending observations are independent.

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

Randomization and analysis should preserve plant/day/block structure. The confirmatory interval must come from the actual randomized design or a prespecified hierarchical model, not the simple independent-binomial planning approximation.

## Why not power all 16 cells from the Kessler effect?

If the same `n/cell` used for the total four-cell factorial were blindly copied into the full `A x D x antagonist x pollinator` experiment, sample sizes become large very quickly. For example, under Delta=0.17, 80% power, design effect 1.5 and 90% retention, the four-cell total is 1,000 observations; the arithmetic 16-cell budget is 4,000.

More importantly, that 4,000 figure still does **not** establish power for:

```text
A x D x antagonist
A x D x pollinator
A x D x antagonist x pollinator
```

because their effect sizes are not identified by the historical total interaction.

Thus the 16-cell number is a budget warning, not a sample-size recommendation.

## Stage 2 — pilot the missing channel contrasts

Only after Stage 1 confirms or tightly estimates the total interaction should selective consumer toggles be added on the same A/D coordinate.

The first augmentation block should estimate enough information to plan the mechanism experiment, not claim final channel identification. It should provide preliminary estimates/variance for:

```text
rho_delta candidate: A x D dependence of antagonist-mediated loss
iota_delta candidate: A x D dependence of pollinator-mediated benefit
m0_delta: A x D interaction in pollinator-absent reproduction
four-way coupling: A x D x antagonist x pollinator
```

Consumer interventions must be biologically selective. A generic exclusion treatment that simultaneously changes pollinator and antagonist access does not identify either channel.

After this pilot, re-run prospective power using the observed mechanism-scale effects and their uncertainty. Do not borrow the Kessler total Delta as the assumed three- or four-way effect.

## Stage 3 — full mechanism allocation

A confirmatory mechanism experiment then crosses:

```text
A x D x antagonist x pollinator
```

with:

- a measured or justified pollinator-absent baseline;
- the four-way separability diagnostic;
- uncertainty propagation for the derived channel contrasts;
- an **independent** A x D joint-cost/allocation assay rather than naming the reproductive residual as cost.

The interpretation order remains:

```text
Does escape occur?  -> total Delta_AD W
Why?                -> rho_delta / iota_delta / kappa_delta allocation
```

A Stage-1 positive interval is sufficient for the first question on the declared reproductive scale. It is not sufficient for the second.

## Stop and promotion rules

- If the Stage-1 interval is wholly above zero: classify `ESCAPE_IDENTIFIED` on that outcome scale and continue to mechanism augmentation.
- If the interval is wholly at or below zero: classify `ESCAPE_REFUTED` on that outcome scale; channel work can still explain why but cannot rescue the total sign.
- If it crosses zero: classify `ESCAPE_UNRESOLVED`; do not infer escape from favourable marginal channels.
- A positive mechanism pilot does not override an unresolved or nonpositive total interaction.
- A large 16-cell budget extrapolation is not a reason to skip the total-interaction replication; it is a reason to stage the design.
