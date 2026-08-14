# Bejaria resinosa 2022 floral-stickiness audit v1

## Source

Chautá A, Kumar A, Mejia J, Stashenko EE, Kessler A. **Defensive functions and potential ecological conflicts of floral stickiness.** *Scientific Reports* 12:19853. DOI `10.1038/s41598-022-23261-2`.

The primary article is open access. A Cornell eCommons data record also exposes the raw survey and chemistry files associated with the study.

## Why this is a high-value floral-D system

Stickiness in *Bejaria resinosa* is restricted to petals and sepals rather than being a vegetative defense. The study uses both a natural sticky/non-sticky polymorphism and direct experimental removal of stickiness.

Accordingly, the focal barrier/defence axis is operationally clean:

```text
D = floral petal/sepal stickiness
manipulation = MeOH washing of phenotypically sticky flowers
```

The primary biological target is florivore damage to reproductive tissues.

## Direct field manipulation

The strongest source-level result is the manipulation of floral stickiness:

```text
sticky control flowers: 0% herbivore damage observed
MeOH-washed flowers:    21% attacked on average
```

MeOH-washed inflorescences also had 32.5% lower fruit set than non-washed controls (`chi-square = 4.877`, `df = 1`, `P = 0.027`).

Pattern state:

```text
D -> floral antagonism: strong protection
D -> reproductive consequence: protective association under the manipulation
```

The fitness response is downstream evidence of the manipulation; it is not the mixed partial `W_AD`.

## Population dependence

Across three natural populations, non-sticky flowers had more bud and flower damage. The magnitude of stickiness-mediated protection varied among populations, with a significant stickiness × population interaction for bud florivory (`P = 0.046`). Fruit set also depended on population and its interaction with stickiness.

Pattern class:

```text
population / ecological-context dependence of D efficacy
```

## Consumer-specific state changes

Targeted laboratory bioassays did not produce one universal response to sticky petals:

- generalist grasshoppers: no detected difference in petal consumption (`P = 0.6651`);
- snails: preferred consuming sticky petals (`P = 0.0001`);
- dominant field florivores: lower damage on sticky flowers, and direct removal of stickiness increased attack.

This is therefore another same-trait example where consumer identity changes whether a floral defence channel is expressed and even the direction of consumption preference.

## Pollinator boundary

Potential pollination costs are biologically plausible because bees and other insects can be trapped on sticky flowers, but the article explicitly states that evaluating this ecological cost would require a different experiment.

A bird-exclusion manipulation did not show a fruit-set response attributable to excluding hummingbirds, but this is **not** a direct estimate of `D -> pollination`.

Therefore this study contributes only `D -> antagonism` to the route ledger. It does not create a pollinator-cost route by inference.

## Theory-facing mapping

Admitted:

```text
flower-specific D can directly reduce florivory
D efficacy varies among populations
D response differs among consumer guilds
D-mediated antagonist reduction can translate into reproductive consequences
```

Not admitted:

```text
fruit-set difference = W_AD
stickiness = attraction A
trapped bees = measured D -> pollination cost
D -> florivory effect = rho
a non-significant bird-exclusion result = iota = 0
```

## Relationship to Pedicularis expansion

The two newly promoted physical/chemical floral barriers provide independent convergence:

```text
Pedicularis water-filled bract:
  protects against seed predators but is bypassed by nectar robbers;
  no detected legitimate-pollinator cost in the direct manipulation.

Bejaria floral stickiness:
  directly reduces field florivory;
  protection magnitude varies by population;
  laboratory consumer responses range from null to preference for sticky tissue.
```

Together they strengthen consumer/context dependence of floral defence without requiring a universal negative effect on pollinators.

## Current adjudication

```text
primary source:                  PASS
flower-specific D definition:   PASS
direct D manipulation:          PASS
D -> floral antagonism:         PASS
fitness consequence:            PASS as downstream outcome
consumer-context value:         HIGH
population-context value:       HIGH
D -> pollination:               NOT IDENTIFIED
direct A x D:                   NO
```

### Decision

**PROMOTE_TO_PATTERN_EXPANSION_LEDGER**
