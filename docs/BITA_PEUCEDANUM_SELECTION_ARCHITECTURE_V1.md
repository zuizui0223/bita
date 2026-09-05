# BITA Peucedanum selection architecture v1

## Core classification

`Peucedanum multivittatum` is best treated as a **partial functional modularization** system, not as a complete `x -> F1`, `y -> F2` split.

The architecture is:

```text
perfect flower
  -> male function
  -> female / seed function
  -> seed-predator target

male flower
  -> male / display function
  -> no direct seed-bearing target
```

Perfect flowers therefore retain the ancestral-looking multifunctional combination at the contemporary phenotype level, while male flowers provide a specialized route for retaining male/display function without adding equivalent seed-bearing exposure.

This wording is architectural only. It does **not** claim that perfect flowers are ancestrally primitive or that andromonoecy evolved by a documented historical split from hermaphroditism.

## Why the loading interpretation is biologically plausible

The 2025 study reports that perfect and male flowers each have five stamens and similarly sized anthers, with similar pollen production per anther:

```text
perfect: 1945 +/- 424 SE pollen grains per anther (n=11)
male:    2140 +/- 438 SE pollen grains per anther (n=10)
```

Their male-phase flowering also overlaps within the terminal umbel. Thus a male flower is not simply an empty non-seed-bearing display unit; it retains the pollen-donor apparatus while omitting female seed production.

## Direct antagonism loading recovered in 2025

In the high-predation focal population, predator oviposition increased with perfect-flower number and decreased with male-flower number:

```text
oviposition GLMM
perfect flowers: z = +5.97, p < 0.0001
male flowers:    z = -2.38, p = 0.017
flower height:   z = +2.11, p = 0.035
```

Selection-gradient estimates on predation rate point in the same directions:

```text
beta(predation ~ perfect flowers) = +0.178 +/- 0.038
beta(predation ~ male flowers)    = -0.042 +/- 0.020
```

For final fruit-set rate under severe predation:

```text
beta(final fruit-set ~ perfect flowers) = -0.108 +/- 0.022
beta(final fruit-set ~ male flowers)    = +0.006 +/- 0.013
```

The interpretation is therefore not merely that high-predation populations happen to have more male flowers. Within the high-predation system, seed-bearing perfect-flower investment directly loads onto predator risk, while male-flower investment loads in the antagonist-reducing direction.

## Male fitness is display-level, not a simple male-flower coefficient

The 2025 paternity analysis reports that siring success increased with **total flower production**, whereas neither perfect- nor male-flower number alone explained male fitness after the relevant analyses.

This matters for the Chapter-2 interpretation. The differentiated benefit is not:

```text
male flower count -> male fitness
```

as a one-to-one pathway.

It is more accurately:

```text
male-flower allocation
  -> preserves / expands pollen-bearing display
  -> avoids adding equivalent seed-bearing target
  -> helps maintain the architecture's male-function opportunity under predation.
```

## Link to the 2021 geographic mosaic

The earlier study reported:

```text
population male-flower proportion vs seed predation:
r^2 = 0.64, p < 0.0001, positive direction
```

while individual flower numbers did not predict predation within populations and flowering time was the strong individual/context predictor.

Together, the two studies support a scale-consistent story:

```text
phenology sets predator exposure among populations
        ↓
recurrent high exposure changes the value of flower-class allocation
        ↓
high-predation populations become more male-biased
        ↓
within a high-predation population, perfect and male flowers load predator risk in opposite directions.
```

## BITA claim level

Current status:

```text
REAL_WORLD_PARTIAL_FUNCTIONAL_MODULARIZATION_SUPPORTED
SELECTION_MOSAIC_SUPPORTED
CAUSAL_R_STATE_NOT_IDENTIFIED
COMPLETE_X_Y_MODULARITY_NOT_IDENTIFIED
HISTORICAL_ORIGIN_NOT_IDENTIFIED
```

Peucedanum is therefore a strong **natural Chapter-2 architecture anchor**, especially because it is a Japanese alpine system with field access potential. It complements rather than replaces the Pedicularis causal `R_state` route.

## Next causal upgrade

The most informative new manipulation is a fixed-total-display experiment that varies the fraction of perfect versus male flowers while holding total flower number approximately constant.

Measure at minimum:

```text
predator eggs / perfect flower
predated fruits
intact fruits
pollinator visitation
pollen export or siring proxy
total flower display
```

A positive causal partial-differentiation result would require reduced antagonist cost under a more male-biased allocation without a commensurate loss of male/display function.
