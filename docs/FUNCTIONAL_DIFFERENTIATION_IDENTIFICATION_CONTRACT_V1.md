# Functional differentiation identification contract v1

## Purpose

Chapter 2 should not stop at showing that two traits interact. The central architectural claim is that a second trait dimension can release the compromise identified in Chapter 1 by allowing the two functions to be tuned more independently.

This contract distinguishes the **default state-specific empirical reference** from the stricter **pure-function reference**.

## Input from Chapter 1

BITA imports, rather than re-infers, the Chapter-1 result.

The default SCH handoff contains:

```text
z_P* = z_pollinator_context
z_G* = z_antagonist_context
z_C* = z_combined
```

plus evidence that selective removal of the antagonist or pollinator shifts the combined optimum toward the corresponding state-specific optimum.

These are intervention-defined reproductive optima. They are not automatically pure function optima because direct/background trait effects can remain in the reproductive state surfaces.

Theory may separately define:

```text
z_F1* = pure function-1 optimum
z_F2* = pure function-2 optimum.
```

BITA may use `z_F1*` only if SCH independently identifies and explicitly exports it.

## Chapter-2 architecture

Introduce a second functional coordinate `y` while preserving the Chapter-1 coordinate as `x`.

```text
x = retained / refined function-1-facing coordinate
y = added function-2-facing coordinate.
```

In the current BITA special case:

```text
x = attraction trait A
y = antagonist-reducing trait D.
```

The default question is whether `y` lets the optimum of `x` move toward the SCH state-specific function-1-facing reference `z_P*`.

## Stage F1 — preferential functional loading

Before interpreting any fitness interaction as differentiation, identify how each trait loads on each function.

Estimate a causal response matrix:

```text
          function 1   function 2
trait x      r11          r12
trait y      r21          r22.
```

For the floral implementation, useful directional expectations are:

```text
A -> pollinator gain:        strong positive target
A -> antagonist exposure:    conflict route may remain
D -> antagonist loss:        strong reduction target
D -> pollinator gain:        small penalty / weak cross-effect target.
```

A differentiated architecture is supported when the intended within-function effects are stronger than the cross-function penalties on the chosen scale. Perfect selectivity is not required.

Do not collapse these four contrasts into one modularity score before reporting them separately with uncertainty.

## Stage F2 — multi-level dimensional release

Use multiple `x` levels and at least two `y` states:

```text
x1, x2, ..., xK
x
y0, y1.
```

Estimate:

```text
W(x | y0)
W(x | y1)
```

and recover:

```text
x0* = argmax_x W(x | y0)
x1* = argmax_x W(x | y1).
```

### Default empirical reference

By default,

```text
z_ref = z_P* = SCH P1G0 state-specific optimum.
```

The release estimand is:

```text
R_state
  = |x0* - z_P*| - |x1* - z_P*|.
```

Positive `R_state` means the added function-2 coordinate moves `x` toward the function-1-facing state favored when antagonism was suppressed in SCH.

### Optional pure-function reference

If SCH independently supplies `z_F1*`, report separately:

```text
R_pure
  = |x0* - z_F1*| - |x1* - z_F1*|.
```

Do not relabel `R_state` as `R_pure`.

## Stage F3 — architecture-level fitness gain

When a genuine shared-architecture comparator is available on the same fitness scale, estimate:

```text
W_shared* = best attainable fitness under the shared coordinate
W_diff*   = best attainable fitness under x,y differentiation
Delta_mod = W_diff* - W_shared*.
```

A positive `Delta_mod` supports architecture-level release only when the added trait's construction, maintenance and pleiotropic costs are included.

If no commensurable shared-architecture comparator exists, do not report `Delta_mod`. Use the narrower within-BITA optimum fitness gain and release estimand.

## Stage F4 — current BITA two-level outcome hierarchy

For the attraction-defence implementation:

```text
A0 = W10 - W00
A1 = W11 - W01
Delta_AD W = A1 - A0.
```

The existing decision ladder is retained:

```text
positive interaction relief:
Delta_AD W > 0

constraint release:
A0 <= 0 < A1

strict reversal:
A0 < 0 < A1.
```

These are local functional-release claims. They become evidence for the broader differentiation hypothesis only when preferential loading and the relevant release reference are established.

## Stage F5 — mechanism-resolved differentiation

Run the selective crossed design:

```text
x x y x function-2 environment x function-1 environment.
```

In the floral implementation:

```text
A x D x antagonist x pollinator
16 cells.
```

Estimate the existing channels:

```text
rho_delta    antagonist relief
iota_delta   pollinator interference
m0_delta     pollinator-independent baseline interaction
U_delta      remaining unallocated residual.
```

Only after an independent assay may the appropriate residual be biologically interpreted as a joint cost / allocation channel.

The mechanism-resolved differentiation claim is strongest when antagonist relief is positive and substantial, pollinator interference is small enough not to erase the relief, and the observed x-optimum release is in the direction predicted from the declared SCH reference.

## Residual coupling diagnostic

The four-way:

```text
x x y x E1 x E2
```

or, in the floral case:

```text
A x D x G x P
```

is an internal diagnostic of incomplete functional separability.

If non-zero, the effect of one functional coordinate depends on the state of the other functional environment. This supports **partial modularity** rather than clean modularization.

## Minimum positive Chapter-2 decision

A strong contemporary functional-differentiation result requires:

```text
F1  Chapter-1 causal compromise established;
F2  x and y have different functional loading profiles;
F3  adding / increasing y shifts x toward the declared SCH reference;
F4  the joint differentiated phenotype improves total reproductive outcome;
F5  selective intervention shows the improvement is generated by the
    intended functional relief rather than an unidentified side pathway.
```

If F2-F4 hold but F5 is incomplete, report:

```text
FUNCTIONAL_DIFFERENTIATION_OUTCOME_SUPPORTED
MECHANISM_ALLOCATION_UNRESOLVED.
```

If only a positive `x x y` interaction is recovered, report interaction relief, not modularization.

## Historical promotion gate

Historical modularization requires additional evidence:

```text
H1  ancestral integrated / shared architecture established;
H2  derived increase in trait dimensionality or functional independence;
H3  transition reconstructed across lineages or developmental states;
H4  alternative explanations for trait addition / loss tested.
```

Without H1-H4, the appropriate claim is contemporary functional differentiation, not an ancestral trait split.

## Practical SCH -> BITA sequence

```text
SCH binary pilot
-> identify local conflict and variance

SCH multi-level design
-> recover z_P*, z_G*, z_C*
-> optionally identify pure z_F1*, z_F2* in an independent lane

BITA F1
-> validate x/y functional loading

BITA F2
-> multi-level x x y surface
-> default test: x optimum shifts toward z_P*
-> optional strict test: x optimum shifts toward independently identified z_F1*

BITA F4/F5
-> two-level outcome hierarchy + full 16-cell mechanism allocation

historical extension
-> test integration -> differentiation through evolutionary time.
```

This sequence makes Chapter 2 a direct mechanistic answer to Chapter 1 without confusing a theory-level pure optimum with a state-specific experimental estimand.
