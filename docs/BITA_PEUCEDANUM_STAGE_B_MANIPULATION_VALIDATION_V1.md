# BITA Peucedanum Stage-B manipulation validation v1

## Question

Before using a post-male-phase floral sex-composition manipulation to estimate the causal effect of `q`, validate that the manipulation itself is biologically and technically clean.

```text
q = perfect flowers / (perfect + male flowers)
```

A Stage-B fitness result is not interpretable as a causal effect of `q` unless this validation layer passes first.

## Registered implementation

```text
empirical/identification_design/PEUCEDANUM_STAGE_B_VALIDATION_TEMPLATE_V1.csv
empirical/identification_design/PEUCEDANUM_STAGE_B_VALIDATION_CONFIG_TEMPLATE_V1.json
scripts/evaluate_peucedanum_stage_b_manipulation.py
```

The config intentionally contains `REQUIRED_BEFORE_USE` values. Thresholds must be frozen before confirmatory field data are evaluated.

## Required biological sequence

```text
common male phase completed
-> classify flower sex at female transition
-> verify negligible predator oviposition has occurred
-> manipulate retained perfect:male composition
-> hold retained total display approximately fixed
-> match handling effort across q treatments
-> validate classification against later morphology / fruiting
-> only then proceed to q x antagonist fitness analysis.
```

## Validation gates

### 1. q-level coverage and separation

At least the preregistered number of q levels and units per level must be achieved. Realized q must remain within the frozen error tolerance of target q, and realized group means must preserve the intended ordering.

### 2. Sex-classification accuracy

Classification is checked against later morphology or fruiting. The aggregate Wilson 95% lower confidence bound for accuracy must exceed the preregistered minimum.

### 3. Pre-manipulation oviposition

Eggs are counted immediately before q manipulation. Both the fraction of units with any egg and the mean egg count must remain below preregistered maxima.

If oviposition has already occurred before q manipulation, the design cannot cleanly claim that later predator exposure acts on the experimentally created composition.

### 4. Fixed retained total display

For every unit:

```text
total_retained = perfect_retained + male_retained.
```

The retained total must remain within the preregistered relative deviation of the fixed target count.

### 5. Handling balance

`handling_actions` records total removal plus sham manipulation effort. Mean handling effort across q groups must remain within the preregistered relative-range tolerance.

Raw `removal_load` is retained separately because different natural starting compositions may require different actual removals; sham handling is what makes total manipulation effort comparable.

### 6. Pretreatment balance

The validator checks maximum pairwise standardized mean differences across q groups for:

```text
total_before
flower_height
flowering_day.
```

This prevents q treatment from being silently confounded with initial display size, plant stature or phenology.

### 7. Mechanical damage

Both overall mechanical-damage rate and between-q-group differences must remain below preregistered limits.

### 8. Male-phase completion

Every q group must meet the frozen minimum fraction of units for which the common male phase was completed before manipulation.

This is essential because the proposed causal interpretation is that the manipulation changes later female/seed-bearing exposure after earlier pollen-donor opportunity has already occurred.

## Positive receipt

All gates must pass before returning:

```text
PEUCEDANUM_STAGE_B_SEX_COMPOSITION_MANIPULATION_VALIDATED
```

Failure of any gate returns:

```text
PEUCEDANUM_STAGE_B_MANIPULATION_NOT_VALIDATED.
```

## What this does and does not establish

A positive validation receipt establishes only that the q manipulation is technically qualified for a subsequent randomized fitness experiment.

It does **not** by itself show:

```text
q causally changes fitness
q x G changes fitness
complete functional modularity
historical origin of andromonoecy.
```

The next experiment must cross validated randomized q treatments with antagonist state and estimate the resulting female and male fitness surfaces.
