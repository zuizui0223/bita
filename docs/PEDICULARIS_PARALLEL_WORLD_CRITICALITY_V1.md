# Pedicularis same-versus-parallel criticality experiment v1

## Purpose

`Pedicularis rex` is the strongest current same-species route for asking whether the Chapter-1 balance boundary and Chapter-2 differentiation boundary occur at the same ecological context.

The ecological control axis is antagonist pressure, because primary literature already shows strong geographic variation in pre-dispersal seed predation while pollinator-mediated selection direction is comparatively consistent.

The current published range (roughly 0.8% to 27.42% seed predation across populations) is a **design anchor**, not itself the critical-point estimate.

## Declared control variable

Use a prospectively defined context index `e` based on antagonist pressure measured independently of the confirmatory outcome manipulation.

Preferred operational form:

```text
e = pre-confirmatory exposed-control seed-predation pressure
```

estimated from sentinel flowers/plants in the same population/season before the confirmatory SCH/BITA analyses are opened.

Do not define `e` from the treatment contrast whose sign will later be used to locate the critical point.

## Context selection

Use a presurvey to rank available population/season contexts and choose at least five contexts spanning the observed antagonist-pressure distribution when feasible.

Selection should be based on the frozen presurvey `e` only, for example approximately low / lower-middle / middle / upper-middle / high quantiles. Do not choose contexts after seeing the confirmatory criticality margins.

The aim is to bracket at least one zero crossing, not to maximize a desired sign.

## World S — Chapter 1 shared-coordinate experiment

Within each selected context:

```text
z = corolla exsertion
P = pollination state
G = independently manipulated seed-predator state
water-defence y held fixed across SCH cells
```

Run the registered multi-level `z x P x G` causal compromise design.

Required outputs per context:

```text
z_P*, z_G*, z_C*
causal optimum shifts
component gradients
context-stable component-optimum gate
L_S,component* on the frozen common fitness scale.
```

The SCH antagonist intervention must remain independent of the water-defence state later used as Chapter-2 `y`; otherwise the chain is circular.

## World D — Chapter 2 differentiated functional-state experiment

In the same population/season context, use:

```text
x = exsertion on the SCH z scale
y0 = water-defence function disabled/drained
y1 = water-defence function active/protected.
```

Run the registered multi-level `x x y` dimensional-release experiment.

Required outputs:

```text
x0*, x1*
R_state toward frozen SCH z_P*
function-2 loading gain
function-1 cross-effect
direct net common-fitness margin
best W(x|y1) - best W(x|y0).
```

For this experiment the direct net margin is the Chapter-2 observable criticality lane. It supports functional-state differentiation, not historical origin of the water-bearing architecture.

## Independent projected lane

To avoid making the SCH-side projection algebraically identical to the direct BITA observation, test-context projected parameters must come from independent calibration/assays rather than from the direct BITA margin in that same test context.

For each held-out test context provide:

```text
L_S,component*        from SCH
release_efficiency    from preregistered independent calibration/model
K_state or K_arch     from independent cost assay
```

and compute

```text
Phi_projected(e)
 = release_efficiency(e) * L_S,component*(e) - K(e).
```

The direct BITA lane independently supplies

```text
Phi_direct(e)
 = best W_D(e) - best W_S-like(e)
```

on the same fitness scale.

This is why contexts are marked `CALIBRATION` versus `TEST`.

## Critical contexts

Locate zero crossings:

```text
e_c,S = zero of Phi_projected(e)
e_c,D = zero of Phi_direct(e).
```

Then

```text
Delta_e_c = e_c,D - e_c,S.
```

### Same-critical-context result

```text
|Delta_e_c| <= preregistered context tolerance
```

supports the claim that the same latent architecture boundary is adequate for both world descriptions.

### Parallel-world result

A persistent nonzero `Delta_e_c` supports an effective parallel-world threshold: changing the architecture has altered something not captured by the simple shared mapping.

Candidate explanations include context-dependent deployment cost, moving functional objectives, residual cross-loading, non-nested architectures, or new interactions created by the second axis.

## Cross-world offset guard

Two separate response curves do not identify their relative fitness offset automatically. The paired design therefore requires one of:

1. direct net comparison of y0/y1 on an identical absolute reproductive-fitness endpoint in the same blocks; or
2. an independently validated between-world cost/offset bridge.

Without this bridge, the location of `e_c,D` relative to `e_c,S` is not identified even if both within-world curves are estimated precisely.

## Data contract

Template:

```text
empirical/identification_design/PEDICULARIS_CRITICAL_CONTEXT_TEMPLATE_V1.csv
```

Analysis:

```text
scripts/analyze_pedicularis_parallel_world_criticality.py
```

Test contexts require exact provenance labels:

```text
projected_parameter_source = INDEPENDENT_CALIBRATION_PLUS_COST_ASSAY
direct_margin_source       = DIRECT_NET_COMMON_FITNESS_COMPARISON.
```

## Current status

```text
published geographic antagonist gradient:       RECOVERED
SCH causal surface analyzer:                     IMPLEMENTED
SCH fitness-scale conflict-budget analyzer:      IMPLEMENTED
BITA dimensional-release analyzer:               IMPLEMENTED
same-vs-parallel zero-crossing comparator:       IMPLEMENTED
paired biological context data:                  NOT YET COLLECTED
natural e_c,S:                                   NOT YET IDENTIFIED
natural e_c,D:                                   NOT YET IDENTIFIED
natural Delta_e_c:                               NOT YET IDENTIFIED.
```

The remaining barrier is now field information, not an undefined analysis.
