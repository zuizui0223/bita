# BITA Pedicularis dimensional-release contract v1

## Purpose

This contract maps a `Pedicularis rex` multi-level exsertion-by-water-defence experiment onto the registered BITA dimensional-release analyzer.

The analysis starts only after SCH has identified a positive Pedicularis compromise in the **same population and season**.

## Coordinates

```text
x = realized corolla exsertion
y0 = cupulate bract drained / water defence disabled
y1 = water retained / water defence active.
```

The acute water manipulation is a functional-state intervention. It does not by itself establish a genetically or developmentally independent module.

## Required SCH input

The SCH receipt must satisfy:

```text
receipt_schema_version = SCH_CAUSAL_COMPROMISE_STATE_OPTIMA_V1
status = MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE
system = Pedicularis rex
population_id and season_id match the BITA experiment.
```

Default release reference:

```text
z_P* = observed_estimands.z_pollinator_context.
```

If SCH additionally exports `identified_pure_function_optima.z_F1`, the preregistered `pure_function` reference mode may be run as a separate stronger lane.

## Raw data

Template:

```text
empirical/identification_design/PEDICULARIS_DIMENSIONAL_RELEASE_TEMPLATE_V1.csv
```

Required fields:

```text
population_id
season_id
plant_id
flower_id
assigned_x_level
realized_exsertion
water_treatment
ovule_count
undamaged_seed_count
damaged_seed_count
pollen_grains
pollinator_visits
water_depth
mechanical_damage.
```

`water_treatment` is exactly `DRAINED` or `PROTECTED`.

## Mapping to BITA

The system wrapper maps:

```text
x_level        = assigned_x_level
x_measured     = realized_exsertion
y_state        = 0 for DRAINED, 1 for PROTECTED
function1      = pollen_grains
function2      = undamaged / (undamaged + damaged) among initiated seeds
fitness_value  = undamaged mature seed count per focal flower.
```

Larger values therefore mean better performance for both declared functions.

## Primary estimand

Fit:

```text
W(x | y0)
W(x | y1)
```

and estimate:

```text
x0* = optimum with water defence disabled
x1* = optimum with water defence active

R_state = |x0* - z_P*| - |x1* - z_P*|.
```

Positive `R_state` means the water-defence axis releases exsertion toward the pollination-facing SCH reference.

## Preferential loading

The registered BITA gate additionally requires:

```text
y improves function 2
while
y does not reduce function 1 beyond the preregistered tolerance.
```

For Pedicularis this means water protection must increase seed survival without an equivalent pollen-receipt penalty.

## Fitness-release gate

The protected architecture must also increase the best attainable common reproductive outcome by at least the prospectively frozen amount.

This is reported as:

```text
within_bita_optimum_fitness_gain
```

and not as `Delta_mod`.

## Run command

```bash
python scripts/analyze_pedicularis_dimensional_release.py \
  <pedicularis_xy.csv> \
  <sch_pedicularis_receipt.json> \
  <frozen_config.json> \
  --output <bita_pedicularis_receipt.json>
```

## Claim ceiling

A positive result supports:

```text
contemporary outcome-level functional differentiation / dimensional release.
```

It does not yet establish:

```text
mechanism allocation across pollination and antagonist channels
architecture-level Delta_mod
structural or developmental independence
historical modularization from an ancestral shared state.
```
