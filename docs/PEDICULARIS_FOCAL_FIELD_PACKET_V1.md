# Pedicularis BITA focal field packet v1

## Objective

Execute the first same-system BITA test after E0 and E1 are valid. This packet concerns E2-E5 only and must not be used to bypass the SCH handoff.

## Unlock conditions

Do not enroll focal BITA flowers until both exist:

```text
1. frozen Pedicularis threshold config with status
   FROZEN_BEFORE_FOCAL_OUTCOME_ANALYSIS
2. same-population / same-season SCH receipt with status
   MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE
   and SCH_PEDICULARIS_FULL_SURFACE_WRAPPER_V2 provenance
```

## Experimental structure

Primary confirmatory surface:

```text
>= 5 prospectively assigned x levels
× 2 water-defence states

DRAINED   = water defence disabled
PROTECTED = intact/retained water defence
```

Prefer blocked allocation within plant whenever floral material permits. The same plant should contribute across multiple cells so plant-level heterogeneity is blocked rather than confounded with x or y.

Do not change x-level definitions after inspecting reproductive outcomes.

## Per-flower sequence

For each focal flower:

```text
1. assign plant_id / flower_id
2. record population_id / season_id
3. assign x level and y treatment from the frozen allocation sheet
4. measure pre-treatment realized exsertion
5. apply the registered x manipulation
6. apply DRAINED or PROTECTED water treatment
7. measure post-manipulation realized exsertion
8. record water depth and mechanical damage
9. record pollinator visits when observed
10. quantify pollen receipt using the registered protocol
11. retain flower/capsule to seed maturation
12. count ovules, undamaged mature seeds and damaged seeds
```

The raw row is not complete until all required columns in `PEDICULARIS_DIMENSIONAL_RELEASE_TEMPLATE_V1.csv` are populated.

## Manipulation integrity

A focal row is flagged before outcome analysis if any of the following occurs:

```text
assigned x level not achieved within the prospectively allowed tolerance
water state not maintained through the registered antagonist window
mechanical damage caused by manipulation
flower identity lost
capsule lost for reasons unrelated to registered ecological channels
protocol deviation that changes pollinator access
```

Do not silently delete flagged rows. Preserve them with a deviation ledger and apply the prospectively declared inclusion rule.

## Randomization and blocking

Before outcomes are visible:

```text
randomize x × y cell allocation within available flowers
block by plant
balance treatment counts through the field day / flowering period when feasible
record allocation failures rather than substituting cells opportunistically
```

Population and season must match the SCH handoff exactly for the confirmatory chain.

## Primary and companion outcomes

Primary fitness outcome:

```text
undamaged mature seed count per focal flower
```

Function 1:

```text
pollen grains received
```

Function 2:

```text
undamaged / (undamaged + damaged) among initiated seeds
```

Companion diagnostics:

```text
pollinator visits
water depth
mechanical damage
realized exsertion
ovule count
```

## Analysis order

The confirmatory analysis is run in this order:

```text
A. input/readiness validation
B. preferential loading gate
C. W(x|y0), W(x|y1) surface fits
D. R_state relative to the frozen SCH reference
E. within_bita_optimum_fitness_gain
F. promotion decision
```

Do not inspect a successful D/E result and then relax a failed B gate.

## Negative outcomes are retained

Registered interpretations:

```text
y protects seeds but fails function-1 tolerance
-> defence exists, preferential loading not established

preferential loading passes but R_state does not
-> second functional state does not release the exsertion compromise in this context

R_state passes but optimum fitness gain does not
-> geometric release without registered reproductive benefit

all E0-E5 pass
-> FUNCTIONAL_DIFFERENTIATION_OUTCOME_SUPPORTED
```

None of these outcomes identifies historical modularization or architecture cost K.

## Immediate follow-up after a positive focal result

Only then unlock:

```text
crossed pollinator × antagonist mechanism allocation
structural-y retention-performance promotion
independent K lane if an architecture-level R-K claim is required
```
