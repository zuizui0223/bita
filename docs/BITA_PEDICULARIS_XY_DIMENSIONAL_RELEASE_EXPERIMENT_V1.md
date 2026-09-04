# BITA Pedicularis x-y dimensional-release experiment v1

## Purpose

`Pedicularis rex` can potentially connect SCH Chapter 1 and BITA Chapter 2 within one biological system.

The proposed architecture is:

```text
Chapter 1 shared/conflicted coordinate
x = corolla exsertion above the cupulate bract

Chapter 2 second functional axis
y = water-retention defence function of the cupulate bract.
```

The central Chapter-2 prediction is:

> when the water-defence axis is active, the optimum of exsertion should move toward the pollination-facing SCH reference because part of the seed-predator cost is carried by y rather than by keeping x low.

## Existing empirical foundation

### Shared conflict

Sun, Armbruster & Huang 2016 (DOI `10.1093/aob/mcw097`) report:

```text
greater exsertion -> more pollen arrival
greater exsertion -> more seed predation
seed predation -> fewer final viable seeds.
```

Thus the low-dimensional system contains the conflict required by SCH.

### Preferential y loading

Sun & Huang 2015 (DOI `10.1093/aobpla/plv019`) experimentally disabled the water-defence state by draining cupulate bracts.

Across sites:

```text
pollinator visitation treatment:
beta = 0.012, P = 0.958

initial seed set treatment:
beta = 0.001, P = 0.906

seed predation treatment:
beta = -0.072, P < 0.0001

final seed set treatment:
beta = 0.025, P < 0.0001.
```

The source states that drainage increased seed predation and reduced protection; the predation treatment effect was significant in 5/6 populations.

This is already strong D1-style evidence:

```text
y -> function 2: strong
y -> function 1: small / unresolved around zero in the measured visit metric.
```

### x-manipulation precedent

Huang, Wang & Sun 2016 (DOI `10.1111/jipb.12460`) manipulated corolla tube length in congeners, including non-destructive shortening by bending the tube and fixing it with clear sticky tape.

This is a method precedent, not yet validation in `P. rex`.

## Stage B0 — inherit the SCH receipt

BITA begins only after a focal `P. rex` SCH experiment returns:

```text
receipt_schema_version = SCH_CAUSAL_COMPROMISE_STATE_OPTIMA_V1
status = MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE
```

with at least:

```text
z_P* = z_pollinator_context
z_G* = z_antagonist_context
z_C* = z_combined.
```

Default Chapter-2 release reference:

```text
z_P*.
```

If SCH additionally passes the context-stable component-optimum upgrade, retain a separate pure-function lane toward `z_F1*`.

## Stage B1 — validate x and y as operational coordinates

### x coordinate

```text
x = realized exsertion
```

Use the SCH-validated multi-level manipulation only. Do not invent a new x manipulation after seeing BITA outcomes.

### y coordinate

Operational knockout:

```text
y0 = water-defence disabled / bract drained
y1 = water-defence intact / retained water.
```

This is an acute functional-state manipulation of the defence axis. It does not by itself prove a genetically independent trait module.

Manipulation checks must verify:

```text
same realized x distribution within each assigned x level
no material shift in corolla opening / lip geometry
no material change in pollinator visitation caused by y
predation protection restored in y1
water state persists through the relevant oviposition window.
```

## Stage B2 — primary multi-level x x y surface

Run:

```text
>=5 x levels x y0/y1
```

under the same focal ecological context used for the SCH handoff when possible.

Primary common outcome:

```text
mature intact viable seeds per focal flower / capsule.
```

Secondary outcomes:

```text
pollen receipt
initial seed set
seed-predation fraction
pollinator visitation / handling
oviposition or attack evidence when measurable.
```

Fit:

```text
W(x | y0)
W(x | y1).
```

Recover:

```text
x0* = optimum with water defence disabled
x1* = optimum with water defence active.
```

## Primary dimensional-release estimand

Use the registered BITA state-specific release metric:

```text
R_state
= |x0* - z_P*| - |x1* - z_P*|.
```

Positive release requires:

```text
R_state > preregistered meaningful threshold
```

with uncertainty and an interior supported `x1*` surface.

Biological prediction for the known Pedicularis geometry:

```text
water defence active
-> seed-predator penalty of exposed flowers reduced
-> x1* shifts toward greater exsertion / z_P*
relative to x0*.
```

The direction must still be inherited from the actual SCH receipt rather than hard-coded before SCH is observed.

## Preferential-loading gate

Replicate the 2015 selectivity result inside the BITA experiment.

A strong D1 gate requires:

```text
y1 strongly lowers antagonist-mediated loss
while the pollinator-facing response remains within a predeclared equivalence / tolerance region.
```

Do not rely on non-significance alone. The new experiment should use a prospective equivalence or bounded-cross-effect criterion for the y -> function-1 lane.

## Stage B3 — fitness-release gate

Require both:

```text
x optimum released toward the SCH reference
and
best W(x|y1) > best W(x|y0) by the predeclared minimum.
```

Call the latter:

```text
within_bita_optimum_fitness_gain
```

not `Delta_mod`.

A true architecture-level `Delta_mod` requires an explicitly commensurable shared-architecture comparator and accounting for construction / maintenance cost of the water-holding bract architecture.

## Stage B4 — mechanism allocation

After D1-D2 are recovered, add selective functional interventions.

Conceptual design:

```text
x levels
x y state
x pollination-weight state
x antagonist-weight / antagonist-exposure state.
```

This is the Pedicularis analogue of the current floral:

```text
A x D x antagonist x pollinator
```

mechanism design.

Primary mechanism questions:

```text
how much of release is seed-predator relief?
does y alter pollination beyond the visit-rate metric?
is there residual x-y-P-G coupling?
```

A non-zero high-order coupling term indicates partial modularity, not automatic failure.

## Geographic prediction

The 2016 study reports seed predation from approximately:

```text
0.80% to 27.42%
```

across populations.

Therefore release should be context dependent.

Prediction:

```text
higher antagonist weight
-> larger benefit of y
-> larger R_state / stronger x-optimum release

lower antagonist weight
-> smaller y benefit
-> weaker or absent dimensional release.
```

This is a direct test of the theory that the value of an extra trait dimension rises with the magnitude of the shared-trait conflict it removes.

## Why this system is especially useful

Pedicularis separates the programme's levels unusually well:

```text
SCH:
shared exsertion conflict

BITA D1:
water defence preferentially loads on antagonist protection

BITA D2:
not yet tested — x optimum should move when y is active

BITA D3:
not yet tested — crossed functional interventions allocate why.
```

This is stronger programme continuity than using one species for Chapter 1 and a different species for Chapter 2.

## Important limitation

The architecture is not structurally independent in a strict sense.

Both exsertion and water defence involve the cupulate bract. Therefore:

```text
functional differentiation may be strong
while structural / developmental modularity remains partial.
```

This makes Pedicularis a useful test of **partial modularization**, not a clean textbook two-module system.

## Claim hierarchy

```text
existing literature:
    SHARED_CONFLICT_RECOVERED
    PREFERENTIAL_Y_LOADING_RECOVERED

new x-y experiment positive:
    FUNCTIONAL_DIFFERENTIATION_OUTCOME_SUPPORTED

mechanism crossed experiment positive:
    MECHANISM_RESOLVED_PARTIAL_MODULARITY_SUPPORTED

historical transition:
    still NOT IDENTIFIED without ancestral-state evidence.
```
