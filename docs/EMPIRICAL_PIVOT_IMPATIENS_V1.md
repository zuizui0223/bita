# Empirical pivot: *Impatiens capensis* as the primary analysis core

## Decision

The verified *Impatiens capensis* individual-plant panel becomes the primary
empirical product. The literature synthesis remains an evidence map and
scope-of-generalisation audit; it is no longer the project’s central numerical test.

```text
primary empirical product:  one linked individual-level floral interaction panel
literature product:         directional evidence map + evidence-gap audit
not claimed:                pooled universal four-arrow parameters
not claimed:                D2/D3 proof of the Part A mixed partial
```

## Why this panel

The title-validated Dryad archive contains an individual-plant panel with:

```text
A: early-season flower redness
D candidate: early-season floral condensed tannins
P: pollinator visits per hour
H: natural floral tissue loss
fitness components: CH fruits per plant per day; seeds per CH fruit
shared context: randomized supplemental robbing, florivory, pollination; first-flower date
unit: individual plant (Plot_Number)
```

Trait paths are treatment-adjusted observational associations. Randomized treatment
assignments do not make flower redness or tannins randomized traits.

## Primary empirical products

### 1. Response-scale D1 channel map

The channel analysis uses the response scale defined by the archived measurements,
rather than treating every response as a standardized Gaussian outcome.

```text
pollinator use:      60-minute-standardized integer visit rate
natural florivory:   individual-flower tissue-loss fraction, clustered within plant
seed component:      individual-CH-fruit seed count, clustered within plant
```

The predeclared models estimate:

```text
P rate              ~ A + D candidate + assignments + phenology
H fraction          ~ A + D candidate + assignments + phenology
CH seed count       ~ A * D candidate + assignments + phenology
```

For the raw flower and fruit responses, plant-level predictors are standardized
once per plant before they are expanded over repeated flowers or fruits. The
analysis therefore does not give plants with more recorded flowers/fruits extra
weight when defining a one-standard-deviation trait contrast.

### 2. Pollinator-rate adequacy sensitivity

The 60-minute pollinator rate has substantial zero mass and overdispersion. The
primary robust mean-rate model remains reported, but a declared two-part sensitivity
separates:

```text
any observed pollinator visit
positive visit intensity conditional on at least one visit
```

This sensitivity describes whether a trait association is concentrated in zero
visitation, positive intensity, both, or neither. It is not a replacement primary
model and cannot be used for result selection.

### 3. Randomized downstream reproductive effects

The study’s supplemental robbing, florivory, and pollination assignments are analysed
separately from trait paths in a full 2×2×2 factorial model. All main effects, all
pairwise interactions, and the three-way interaction remain in each model.

```text
CH fruits per day    ~ robbing * florivory * pollination + pre-treatment phenology
seeds per CH fruit   ~ robbing * florivory * pollination + pre-treatment phenology
```

The observed processed table contains all 200 plants in valid treatment assignment
cells: each of the eight `Robbing × Florivory × Pollination` combinations has
exactly 25 plants. The descriptive baseline-complete audit retains 170 plants, with
19–24 per cell; it is recorded for implementation transparency and is not used for
post-randomization covariate selection.

Treatment coefficients are causal assignment contrasts for reproductive components
within this experiment. They are not causal effects of flower redness or tannins,
and the component outcomes remain distinct from total lifetime reproductive fitness.

### 4. Theory-to-empirics ledger

The output includes a single channel-ledger figure and readout that explicitly
separate:

```text
observational A/D trait-channel associations      dashed arrows
randomized imposed-florivory effect on fruit      solid arrow
unidentified Part A terms                         explicit gaps
```

No output multiplies regression coefficients across incompatible link scales or
calibrates the shared allocation term `c_AD`.

## Inference boundary

```text
D1: aligned treatment-adjusted observational channel panel; response-scale models.
D2: not established; no total reproductive-fitness response.
D3: not established; no independent allocation/shared-cost measure.
trait causality: not identified for flower redness or floral tannins.
treatment causality: identified only for randomized assignment contrasts on the stated components.
```

## Deliverables

```text
1. title-validated archive retrieval and raw-in-memory rerun
2. raw response/denominator and variable-definition audit
3. primary response-scale channel models plus declared pollinator hurdle sensitivity
4. full randomized 2×2×2 treatment models for CH fruit and seed components
5. treatment-cell and baseline-summary audit
6. theory-to-empirics bridge and monochrome channel-ledger figure
7. literature evidence map as the generalisation boundary, not the central test
```
