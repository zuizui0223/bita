# BITA Pedicularis dimensional-release contract v1

## Purpose

This contract maps a `Pedicularis rex` multi-level exsertion-by-water-defence experiment onto the registered BITA dimensional-release analyzer.

The analysis starts only after SCH has identified a positive Pedicularis compromise in the **same population and season** using an antagonist intervention that is independent of the Chapter-2 water-defence axis.

## Coordinates

```text
x = realized corolla exsertion
y0 = cupulate bract drained / water defence disabled
y1 = water retained / water defence active.
```

The acute water manipulation is a functional-state intervention. It does not by itself establish a genetically or developmentally independent module.

## Required non-circular SCH input

The SCH receipt must satisfy:

```text
receipt_schema_version = SCH_CAUSAL_COMPROMISE_STATE_OPTIMA_V1
status = MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE
system = Pedicularis rex
system_wrapper_schema_version = SCH_PEDICULARIS_FULL_SURFACE_WRAPPER_V2
population_id and season_id match the BITA experiment.
```

The Pedicularis SCH provenance must additionally show:

```text
G0 = SEED_PREDATOR_INDEPENDENTLY_EXCLUDED
G1 = SEED_PREDATOR_EXPOSED
water_y = HELD_FIXED_ACROSS_ALL_SCH_CELLS
readiness_reference.g_schema = SCH_PEDICULARIS_PREDATOR_METHOD_V3
readiness_reference.predator_method_requirement contains POLLINATOR_ACCESS_PRESERVED.
```

`SCH_PEDICULARIS_PREDATOR_METHOD_V3` means the antagonist intervention passed both:

```text
predator-effect/selectivity gates
and
method-timing gates showing that the barrier was applied in a registered post-pollination / pre-ovary-swelling window (or an equivalently qualified local barrier) without covering the pollinator-entry zone.
```

A positive predator-effect receipt without that timing / access qualification is insufficient for the same-species SCH -> BITA chain.

Legacy Pedicularis SCH receipts that used water retained / drained as the Chapter-1 antagonist `G` are rejected.

This is essential because BITA now manipulates water defence as `y`. The SCH reference must therefore be estimated without using the same water-y contrast that BITA later tests.

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

Because the required SCH reference comes from `SCH_PEDICULARIS_FULL_SURFACE_WRAPPER_V2`, where water-y was held fixed and antagonist exposure was manipulated independently with a method-qualified predator intervention, this is a **non-circular** release test.

## Preferential loading

The registered BITA gate additionally requires:

```text
y improves function 2
while
y does not reduce function 1 beyond the preregistered tolerance.
```

For Pedicularis this means water protection must increase seed survival without an equivalent pollen-receipt penalty.

Published no-detected-effect results from the earlier drainage experiment are background evidence only; the new experiment must use a prospective cross-effect tolerance or equivalence criterion rather than infer equivalence from non-significance.

## Fitness-release gate

The protected functional state must also increase the best attainable common reproductive outcome by at least the prospectively frozen amount.

This is reported as:

```text
within_bita_optimum_fitness_gain
```

and not as `Delta_mod`.

## Structural-trait promotion is separate

Water ON/OFF is a causal functional-state `y`. Stronger trait differentiation requires a repeatable structural/performance coordinate such as standardized water-holding capacity or retention duration.

Use the separate structural-y promotion contract/evaluator for that claim. A positive functional-state release does not by itself establish a second heritable trait module.

## Run command

```bash
python scripts/analyze_pedicularis_dimensional_release.py \
  <pedicularis_xy.csv> \
  <sch_pedicularis_v2_receipt.json> \
  <frozen_config.json> \
  --output <bita_pedicularis_receipt.json>
```

## Claim ceiling

A positive result supports:

```text
contemporary non-circular outcome-level functional-state differentiation / dimensional release.
```

It does not yet establish:

```text
structural trait differentiation without the structural-y promotion gate
mechanism allocation across pollination and antagonist channels
architecture-level Delta_mod
structural or developmental independence
historical modularization from an ancestral shared state.
```
