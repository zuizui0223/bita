# Pedicularis Experiment B shared surface handoff v1

## Purpose

One `Pedicularis rex` x-by-water-y experiment should serve both Chapter 2 / BALANCE and Chapter 3 / BITA. The experiment is not duplicated by chapter.

```text
Experiment A / SCH
z x P x independent seed-predator G
water-y held fixed
-> state-specific SCH reference + fitness-scale conflict L
-> THREE_WORLD_CONFLICT_HANDOFF_V1

Experiment B / shared by BALANCE + BITA
x = realized exsertion
y0 = drained / water defence disabled
y1 = protected / water defence active
>=5 x levels x y0/y1
same population, season and common fitness outcome
-> BITA_PEDICULARIS_DIMENSIONAL_RELEASE_WRAPPER_V2
-> PEDICULARIS_XY_SURFACE_HANDOFF_V1
```

## Common fitness outcome

The registered Experiment-B outcome is:

```text
UNDAMAGED_MATURE_SEED_COUNT_PER_FOCAL_FLOWER
```

The handoff config must prospectively freeze a `fitness_scale_id` for this outcome and it must exactly match the SCH three-world conflict handoff.

## What the shared handoff contains

`PEDICULARIS_XY_SURFACE_HANDOFF_V1` exports the surface **regardless of whether the BITA positive gates pass**.

It freezes:

```text
context_id
population_id
season_id
fitness_scale_id

W_S* = best fitted fitness under y0
W_D* = best fitted fitness under y1
Delta_W = W_D* - W_S* + bootstrap interval

x0*
x1*
SCH state-specific reference
R_state + bootstrap interval

y -> function-1 effect + interval
y -> function-2 effect + interval
```

This is necessary to avoid circular validation. A negative `Delta_W` is scientifically useful to BALANCE even if BITA's differentiation outcome is not supported.

## Chapter-specific use of the same receipt

### Chapter 2 / BALANCE

Given a positive matched SCH conflict handoff:

```text
L > 0
Delta_W < 0
```

supports a **functional-state BALANCE** receipt. Chapter 2 may then calculate direct reserve, middle position and two-sided depth.

### Chapter 3 / BITA

The same surface is used to test:

```text
R_state > threshold
preferential y loading
best W(y1) - best W(y0)
interior released optimum
```

A positive BITA result is not required for the surface to be exported.

## Claim ceiling

The water manipulation changes the functional defence state while the cupulate bract architecture remains present. Therefore this shared Experiment-B receipt supports only contemporary **functional-state** worldline/dimensional-release inference. Structural architecture cost, strict developmental modularity and historical shared-to-differentiated transition require separate evidence.
