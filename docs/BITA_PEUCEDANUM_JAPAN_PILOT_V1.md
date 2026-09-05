# BITA Peucedanum Japan pilot v1

## Purpose

This pilot tests whether the differentiated male-flower class in `Peucedanum multivittatum` can preserve male/display function while reducing coupling of the floral display to seed-bearing antagonist exposure.

It is **not** the canonical SCH-receipt -> `R_state` BITA experiment. It is a parallel Chapter-2 test of partial functional differentiation in an already andromonoecious architecture.

## Biological motivation

Published work in northern Japan recovers:

```text
perfect flowers
  -> pollen function
  -> female fruit/seed function
  -> seed-predator target

male flowers
  -> pollen/display function
  -> no seed-bearing target.
```

Under strong predispersal seed predation, populations become more male-biased and selection on perfect-flower production can become negative. Under weak predation, selection on perfect-flower production becomes positive.

## Experimental precedent

Direct sex-class manipulation is not yet established in `P. multivittatum`, but experiments in other andromonoecious systems show that flower-gender function can be manipulated or isolated experimentally:

- `Solanum carolinense`: staminate-like flowers were created from perfect flowers by removing pistils, with matched handling controls; pollinator behavior and siring success were measured.
- `Chaerophyllum bulbosum` (Apiaceae): hand pollination, pollinator exclusion and umbel removal were used to alter reproductive allocation and floral architecture.
- `Passiflora incarnata`: male and hermaphroditic flower classes were compared experimentally for pollen-donor and siring performance.

These are method precedents only, not evidence that the same manipulation is valid in `P. multivittatum`.

## Stage J0 — feasibility without changing developmental sex

Do not begin by surgically converting flower sex.

First test a removal-based design using naturally produced male and perfect buds.

### Eligibility screen

Before anthesis, count on each terminal umbel:

```text
male buds
perfect buds
total buds
umbel diameter
plant size
flowering date.
```

Only plants with enough flowers of both classes to reach prospectively declared target compositions are eligible.

Eligibility must be defined before treatment assignment.

## Stage J1 — fixed-display composition manipulation

The cleanest first design holds **total retained flower number approximately constant** while varying the fraction of perfect flowers.

Candidate target compositions:

```text
q_perfect low
q_perfect intermediate
q_perfect high
```

where:

```text
q_perfect = perfect flowers / retained total flowers.
```

Remove excess buds from the required class before anthesis. Use matched sham handling in all treatments and distribute removals across umbel sectors rather than stripping one side.

The exact target counts are set from the field availability distribution before outcome data are inspected.

## Why fixed total display matters

Without fixed display size:

```text
fewer perfect flowers
-> fewer seed targets
```

is mechanically confounded with a smaller total floral display.

Holding total retained flower number approximately constant asks a sharper question:

> can display be shifted from seed-bearing perfect units toward male-only units while retaining pollinator/pollen-donor performance and lowering antagonist exposure?

## Primary outcomes

### Antagonist lane

Measure at least:

```text
moth eggs per terminal umbel
eggs per perfect flower
predated fruits
total developing fruits
intact mature fruits.
```

Eggs per perfect flower are important because total egg number can fall trivially when perfect-flower number falls.

### Male-function lane

Minimum:

```text
pollinator visitation
pollen removal / export proxy.
```

Preferred:

```text
paternity-based siring success.
```

The 2025 study already demonstrates paternity analysis feasibility in the species/programme.

### Female-function lane

Measure:

```text
initial fruit production
final intact fruit production
intact fruits per retained perfect flower.
```

## Primary partial-differentiation tests

A useful positive result requires all of the following directions:

```text
1. lower q_perfect / more male-only display lowers antagonist exposure or damage beyond a trivial target-number explanation;
2. male/display function is preserved within a preregistered tolerance or increases;
3. female fitness loss is smaller than expected from simply deleting the same fraction of total floral display;
4. pollinator visitation is not reduced enough to explain the antagonist result indirectly.
```

This supports:

```text
FUNCTIONAL_PARTITIONING_BY_FLOWER_CLASS
```

not canonical `R_state`.

## Stronger two-coordinate design

If Stage J1 is feasible, move to a factorial target-count design:

```text
x = retained perfect-flower number
y = retained male-flower number.
```

Use only combinations attainable by removal from eligible plants.

The response matrix becomes:

```text
                 female function   male function   predator exposure
perfect x              +               +                 +
male y                 0/+             +                 0/-
```

The important empirical question is whether `y` carries a larger share of male/display function than female function while reducing or not increasing predator exposure.

## Claim ceiling

Even a positive experiment supports contemporary partial functional differentiation only.

It does not establish:

```text
canonical SCH -> BITA dimensional release
ancestral all-perfect architecture in the focal lineage
historical origin of andromonoecy under seed-predator selection
complete male/female modularity.
```

Perfect flowers retain male function, so the system remains partially shared.

## Historical upgrade

A historical modularization claim would require comparative work across the lineage:

```text
sexual-system phylogeny
ancestral-state reconstruction
repeated transitions if available
pollinator / seed-predator context
```

and explicit alternatives such as resource allocation, mating-system selection and architectural constraints.

## Practical role in the programme

```text
Pedicularis rex
-> canonical causal-method route if access and predator-exclusion gates close

Peucedanum multivittatum
-> Japan-accessible partial-differentiation experiment and natural selection-mosaic validation
```

This makes Peucedanum a valuable Chapter-2 companion without forcing it into the wrong estimand family.
