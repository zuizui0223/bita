# BITA dimensional-release design v1

## Purpose

The current BITA floral work contains a strong two-level trait-interaction and mechanism-identification programme. That programme does not by itself test the more specific sister-paper prediction that a second trait dimension **moves the optimum of a retained trait toward the Chapter-1 function-facing reference**.

This document registers that missing empirical bridge.

## Question

After SCH has identified state-specific compromise geometry on one shared coordinate, does adding or strengthening a second preferentially loaded coordinate release the retained coordinate toward the SCH function-1-facing reference while improving the common reproductive outcome?

Default SCH reference:

```text
z_ref = z_P*.
```

A pure-function reference `z_F1*` is a separate optional lane and may be used only after SCH passes its stronger context-stable component-optimum gate.

## Stage D0 — freeze the SCH reference before BITA analysis

Required SCH receipt:

```text
z_P*
z_G*
z_C*
uncertainty for the state optima
common outcome definition
trait-coordinate definition and scale
intervention-state definitions.
```

The BITA analysis must not re-estimate `z_P*` from BITA outcomes. The cross-chapter reference is frozen before the dimensional-release test.

Optional stricter receipt:

```text
z_F1*
reference_kind = pure_function
SCH context-stability / equivalence gate = PASS.
```

Without that receipt, the pure-function lane is absent rather than imputed.

## Stage D1 — preferentially loaded two-axis phenotype

Declare:

```text
x = retained function-1-facing coordinate
y = added / strengthened function-2-facing coordinate.
```

For the floral implementation:

```text
x = attraction/display coordinate A
y = antagonist-reducing coordinate D.
```

Preferential loading must be justified experimentally or mechanistically; simply naming `x` attraction and `y` defence is insufficient.

The design must preserve the same `x` coordinate and measurement scale across `y` states.

## Stage D2 — multi-level x surface across y states

Minimum design:

```text
>=3 x levels x >=2 y states
```

Confirmatory default:

```text
>=5 x levels x 2 y states
```

on one common predeclared fitness/reproductive outcome.

Estimate

```text
x*(y0)
x*(y1)
```

using the same registered surface model / bounded-optimum rule in both states.

A boundary or non-concave surface must remain classified as such; do not force an interior optimum solely to compute a release distance.

## Primary dimensional-release estimand

For the default state-specific SCH reference,

```text
R_state
 = |x*(y0)-z_P*| - |x*(y1)-z_P*|.
```

Positive `R_state` means the retained coordinate is closer to the Chapter-1 function-1-facing state optimum after the second axis is added or strengthened.

The deterministic point estimand is implemented in:

```text
trait_architecture/dimensional_release.py
```

A prospectively declared threshold `r_min > 0` should define biologically meaningful release:

```text
R_state > r_min.
```

Sampling/design-based uncertainty must be added by the registered surface-analysis pipeline; the point-estimand module does not create confidence intervals.

## Secondary fitness-gain estimand

Movement toward `z_P*` and total fitness improvement are separate claims.

Let

```text
W*_0 = best common-scale outcome under y0
W*_1 = best common-scale outcome under y1.
```

Then

```text
Delta_W* = W*_1 - W*_0.
```

A strong contemporary dimensional-release result requires both:

```text
R_state > r_min
Delta_W* > w_min
```

with design-based uncertainty excluding the respective fail regions.

Possible outcomes must remain distinct:

```text
reference release + fitness gain
reference release without fitness gain
fitness gain without reference release
neither.
```

Only the first is the strongest direct match to the sister-paper release prediction.

## Optional pure-function estimand

If SCH exports `z_F1*` under its stronger identification gate,

```text
R_pure
 = |x*(y0)-z_F1*| - |x*(y1)-z_F1*|.
```

Report `R_state` and `R_pure` separately. They are not interchangeable even when they have the same sign.

## Relation to existing two-level BITA outcomes

The current local hierarchy remains:

```text
Level 1  Delta_AD W > 0
Level 2  A0 <= 0 < A1
Level 3  A0 < 0 < A1.
```

These answer whether the second trait improves the local reproductive return to the first trait around a declared two-level contrast.

They do **not** answer whether the optimum of the retained coordinate moves toward the SCH reference.

Therefore:

```text
positive A x D interaction
!= dimensional release

Level 2 / Level 3 local release
!= multi-level optimum release toward z_P*.
```

Both may be reported in the same biological system as complementary evidence.

## Stage D3 — mechanism allocation

After dimensional release is established or rejected, use the existing consumer-crossed BITA design to identify why:

```text
x x y x antagonist x pollinator.
```

The existing `A × D × G × P` logic remains:

- selective interventions;
- `m0` baseline handling;
- identified set / partial identification;
- four-way separability diagnostic;
- independent assay before naming the remaining joint channel.

A non-zero four-way term is evidence that the apparently differentiated coordinates remain context-dependent / cross-loaded rather than perfectly modular.

## Combined Chapter-2 evidence ladder

```text
D1  two coordinates exist and have preferential functional loading
D2  state-specific dimensional release toward SCH z_P*
D2b optional pure-function release toward z_F1*
D3  best attainable common fitness improves
D4  consumer/pathway interventions allocate the release mechanism
D5  historical integrated -> differentiated transition reconstructed.
```

Current BITA evidence is strongest at the local interaction/mechanism-design layers and theoretical architecture layer. The new D2 gate is the missing direct empirical bridge to the current SCH Chapter-1 estimand.

## Claim ceiling

A positive D2/D3 contemporary result licenses:

> adding or strengthening a second functional coordinate moves the optimum of the retained coordinate toward the intervention-defined Chapter-1 reference and improves the attainable outcome under the tested conditions.

It does not by itself establish:

```text
historical origin of y
ancestral one-trait -> two-trait splitting
pure-function release unless z_F1* was independently identified
zero residual cross-loading
general prevalence of modular architectures.
```

## Best paired experiment

The strongest SCH–BITA empirical programme uses the **same biological system and trait scale**:

```text
SCH
5 z x 2 P x 2 G
-> z_P*, z_G*, z_C*

BITA
5 x x 2 y
-> x*(y0), x*(y1)
-> release toward z_P*

BITA mechanism extension
x levels x y x P x G
-> explain the release and quantify residual coupling.
```

This closes the conceptual gap between a one-dimensional compromise and contemporary functional differentiation without requiring a historical transition claim.
