# Peucedanum multivittatum partial-modularization audit v1

## Decision

`Peucedanum multivittatum` is promoted as a **high-value natural Chapter-2 architecture**, not as a completed BITA dimensional-release experiment.

Its strength is that the same plant carries two floral classes with different functional loadings:

```text
perfect flower
  = male pollen/display function
  + female seed function
  + seed-predator target

male flower
  = male pollen/display function
  + no direct seed-bearing target.
```

This is a biologically intuitive case of **partial functional differentiation**.

## Primary evidence

- Kudo & Shibata 2021, DOI `10.1002/ece3.7468`
- Kudo & Shibata 2025, DOI `10.1111/1365-2745.70130`
- Dryad DOI `10.5061/dryad.b5mkkwhcq`
- Dryad DOI `10.5061/dryad.w3r2280v5`

## Existing D1-style evidence

The published studies recover several preferential-loading facts.

### Male-function loading

Perfect and male flowers have similar pollen production during their male phase. The later study reports that greater total flower production increases siring success.

Thus both floral classes contribute to the pollen-donor/display lane.

### Female/seed loading

Only perfect flowers proceed to fruit/seed production. Increasing perfect-flower production therefore increases potential female output but also increases exposure of developing fruits to predispersal seed predators.

### Antagonist filtering

The 2025 study reports:

```text
more perfect flowers -> more oviposition / predation
more male flowers    -> lower predation damage
```

while the male-flower effect on predation was independent of measured male fitness.

This makes male flowers a strong candidate for a differentiated display/pollen component that reduces the fraction of the floral display coupled to seed-bearing antagonist exposure.

## Architecture interpretation

The system is not a clean two-module endpoint.

Perfect flowers still retain male function, so the architecture is:

```text
shared module: perfect flowers = male + female
specialized module: male flowers = male only
```

rather than:

```text
x = female-only
y = male-only.
```

Therefore the correct label is:

```text
PARTIAL_FUNCTIONAL_DIFFERENTIATION
```

not complete modularity.

## Environmental prediction already supported

Seed-predator pressure varies strongly with flowering phenology. Early-flowering populations have intense predation and are more male-biased; late-flowering populations have negligible predation and more perfect flowers.

The later study reports that selection on perfect-flower production changes from negative under strong predation to positive under weak predation.

This matches the BITA prediction that the value of a differentiated coordinate increases with the cost of forcing functions through a shared architecture.

## What is still missing for canonical D2

The existing studies do **not** directly estimate the registered BITA release metric:

```text
R_state = |x0* - z_reference| - |x1* - z_reference|.
```

There is no prior SCH state-optimum receipt for Peucedanum, and the presence of male flowers is not an experimentally added `y` state in the published work.

So current status is:

```text
D1 preferential / differential loading: STRONGLY SUPPORTED NATURALLY
D2 experimental dimensional release:    NOT IDENTIFIED
D3 mechanism allocation:                 PARTIAL NATURAL EVIDENCE
D4 contemporary partial modularity:      SUPPORTED AS ARCHITECTURE INTERPRETATION
D5 historical modularization:            NOT IDENTIFIED
```

## Japan-accessible experimental route

A practical field experiment could manipulate terminal-umbel composition while approximately controlling total display size.

Candidate design:

```text
high perfect / low male
intermediate composition
low perfect / high male
```

using preregistered selective bud/flower removal.

Measure:

```text
moth egg number / oviposition
intact fruit production
pollen removal / donor function
paternity-based siring success where feasible
visitor rate
final male + female fitness components.
```

The key test would be whether shifting display from perfect toward male flowers preserves the pollen-donor/display function while reducing seed-predator cost.

Because changing flower sex composition directly changes ovule supply, a single raw seed-count fitness scale is insufficient. The experiment needs an explicit sex-allocation fitness model or separate male/female fitness outcomes before any total-fitness claim.

## Historical lane

Andromonoecy is evolutionarily suggestive because male-only flowers represent a specialized descendant floral class, but the current data do not show that the focal lineage evolved from an ancestral all-perfect shared architecture under seed-predator selection.

Historical modularization would require:

```text
phylogenetic reconstruction of sexual system
ancestral-state inference
comparative seed-predator / pollinator context
ideally repeated transitions.
```

## Programme role

```text
Pedicularis rex
-> causal contemporary shared-compromise / added-defence test if field gates close

Peucedanum multivittatum
-> strongest Japan-accessible natural partial-differentiation and selection-mosaic example

Nicotiana attenuata
-> strongest existing interaction/release special-case anchor.
```

## Claim ceiling

Peucedanum can currently anchor the statement:

> differentiated floral classes can preserve display/pollen function while reducing coupling of that display to seed-bearing antagonist exposure, and the favored allocation changes with antagonist pressure.

It cannot yet anchor:

```text
causal BITA R_state
empirical Delta_mod
complete structural modularity
historical shared-to-separated transition.
```
