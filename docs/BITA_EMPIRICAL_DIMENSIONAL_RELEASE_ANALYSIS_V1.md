# BITA empirical dimensional-release analysis v1

## Purpose

This analysis is the direct Chapter-2 continuation of a positive SCH causal-compromise receipt.

SCH supplies an intervention-defined function-1 optimum and shared combined optimum. BITA then asks whether adding a second trait coordinate `y` changes the optimum of retained coordinate `x` in the predicted direction.

Implementation:

```text
trait_architecture/dimensional_release.py
```

## Required SCH input

The analyzer requires a positive SCH receipt:

```text
status = MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE
```

and imports:

```text
z_function1 = observed_estimands.z_pollinator_context
z_shared    = observed_estimands.z_combined.
```

BITA does not re-estimate these Chapter-1 quantities.

## BITA data

Template:

```text
empirical/identification_design/BITA_DIMENSIONAL_RELEASE_TEMPLATE_V1.csv
```

Required fields:

```text
plant_id
unit_id
x_level
x_measured
y_state
function1_value
function2_value
fitness_value.
```

`function1_value` and `function2_value` must be pre-oriented so that larger values represent better performance of the declared function. They remain separately reported; the analyzer does not collapse them into one modularity score.

## Multi-level release surface

For `y=0` and `y=1`, fit the local quadratic fitness surfaces:

```text
W(x | y0)
W(x | y1).
```

Recover:

```text
x0* = optimum under y0
x1* = optimum under y1.
```

The x coordinate must be on the SCH z scale or mapped to it by a preregistered affine transformation:

```text
x_SCH = offset + multiplier * x.
```

The primary dimensional-release estimand is:

```text
R = |x0*_SCH - z1*| - |x1*_SCH - z1*|.
```

Positive `R` means the added y state moves x closer to the function-1 optimum identified in Chapter 1.

## Functional-loading check

At every matched x level, estimate:

```text
y effect on function 1
y effect on function 2.
```

The first-pass summary gives equal weight to each x level rather than allowing unequal replication across x to define the loading contrast.

A positive differentiation interpretation requires:

```text
y improves function 2 by at least the preregistered target
and
y does not reduce function 1 beyond the preregistered cross-function tolerance.
```

Perfect selectivity is not required.

The analyzer also reports the observed x-driven range in each function under y0. These are descriptive loading diagnostics and should be interpreted on their declared scales rather than combined into one uncalibrated ratio.

## Within-BITA fitness improvement

The analyzer computes:

```text
best W(x|y1) - best W(x|y0).
```

This is called:

```text
within_bita_optimum_fitness_gain
```

and **not** `Delta_mod`.

A true architecture-level `Delta_mod` additionally requires a commensurable shared-architecture fitness comparator that includes added construction, maintenance, regulatory, and pleiotropic costs. Without that comparator the output explicitly returns:

```text
NOT_IDENTIFIED_UNLESS_SHARED_AND_DIFFERENTIATED_FITNESS_SCALES_ARE_EXPLICITLY_COMMENSURABLE.
```

## Bootstrap

Resample whole `plant_id` clusters. Every bootstrap replicate refits both y-state surfaces and recomputes:

```text
x0*
x1*
dimensional release
within-BITA fitness gain
y loading on function 1
y loading on function 2.
```

The analyzer reports 95% percentile intervals and the fraction of y1 fits retaining an interior concave optimum.

## Outcome-level decision

The status

```text
FUNCTIONAL_DIFFERENTIATION_OUTCOME_SUPPORTED
```

requires all registered gates:

```text
y targets function 2
y preserves function 1 within tolerance
x optimum shifts toward SCH function-1 optimum
joint y1 optimum improves within-BITA fitness
y1 fitness surface retains an interior optimum with sufficient bootstrap support.
```

If any gate fails:

```text
FUNCTIONAL_DIFFERENTIATION_OUTCOME_NOT_FULLY_RECOVERED.
```

## Claim ceiling

A positive result supports contemporary outcome-level dimensional release.

It does not by itself allocate the mechanism among:

```text
antagonist relief
pollinator interference
joint construction / allocation cost
other residual pathways.
```

That still requires the selective crossed Chapter-2 design, including the current `A x D x antagonist x pollinator` 16-cell special case.

Likewise, contemporary dimensional release is not historical modularization. An ancestral shared architecture and repeated derived increases in functional independence remain separate historical claims.

## Cross-chapter interpretation

The two chapters now share an explicit quantity:

```text
SCH: z1* and zc*
BITA: distance of x* from z1* before and after adding y.
```

This makes the Chapter-2 result a measured release of the Chapter-1 constraint rather than a generic positive trait interaction.
