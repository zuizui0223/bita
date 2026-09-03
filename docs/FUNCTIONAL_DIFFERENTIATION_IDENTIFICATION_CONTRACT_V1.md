# Functional differentiation identification contract v1

## Purpose

Chapter 2 should not stop at showing that two traits interact. The central architectural claim is that a second trait dimension can release the compromise identified in Chapter 1 by allowing the two functions to be tuned more independently.

This document converts that idea into an operational identification sequence.

## Input from Chapter 1

BITA should import, not re-infer, the Chapter-1 shared-trait result.

The ideal SCH handoff contains

```text
z1*  function-1 preferred trait value
z2*  function-2 preferred trait value
zc*  combined shared-trait compromise optimum
```

plus evidence that weakening each function shifts the shared-trait optimum toward the other function's preferred state.

In the floral implementation, `z` is the attraction/display axis `A` and the second function is antagonist avoidance / reduced antagonist-mediated loss.

## Chapter-2 architecture

Introduce a second functional coordinate `y` while preserving the Chapter-1 coordinate as `x`.

```text
x = retained / refined function-1-facing coordinate
y = added function-2-facing coordinate.
```

In the current BITA special case,

```text
x = attraction trait A
y = antagonist-reducing trait D.
```

The key question is whether `y` lets the optimum of `x` move toward the function-1 optimum that was unattainable under the shared compromise.

## Stage F1 — preferential functional loading

Before interpreting any fitness interaction as differentiation, identify how each trait loads on each function.

Estimate a causal response matrix

```text
          function 1   function 2
trait x      r11          r12
trait y      r21          r22.
```

For the floral implementation, useful directional expectations are

```text
A -> pollinator gain:        strong positive target
A -> antagonist exposure:    conflict route may remain
D -> antagonist loss:        strong reduction target
D -> pollinator gain:        small penalty / weak cross-effect target.
```

A differentiated architecture is supported when the intended within-function effects are stronger than the cross-function penalties on the chosen scale. Perfect selectivity is not required.

Do not collapse these four contrasts into one modularity score before reporting them separately with uncertainty.

## Stage F2 — multi-level dimensional release

A two-level `A x D` experiment identifies local interaction relief. A stronger differentiation result should recover how the attraction optimum changes across defence states.

Use multiple `x` levels and at least two `y` states:

```text
x1, x2, ..., xK
x
y0, y1 [or multiple y levels].
```

Estimate

```text
W(x | y0)
W(x | y1).
```

Define

```text
x0* = argmax_x W(x | y0)
x1* = argmax_x W(x | y1).
```

If Chapter 1 showed that the shared compromise holds `x` below the function-1 optimum, the functional-differentiation prediction is

```text
x1* shifts toward the function-1 optimum relative to x0*.
```

The direction reverses when the Chapter-1 ordering reverses. The prediction must therefore be registered from the Chapter-1 geometry rather than hard-coded as “higher x is always better.”

## Stage F3 — architecture-level fitness gain

When a genuine shared-architecture comparator is available on the same fitness scale, estimate

```text
W_shared* = best attainable fitness under the shared coordinate
W_diff*   = best attainable fitness under x,y differentiation
Delta_mod = W_diff* - W_shared*.
```

A positive `Delta_mod` supports architecture-level release only when the added trait's construction, maintenance and pleiotropic costs are included.

If no commensurable shared-architecture comparator exists, do not report `Delta_mod`. Use the narrower within-BITA outcome hierarchy instead.

## Stage F4 — current BITA two-level outcome hierarchy

For the attraction-defence implementation,

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

These are local functional-release claims. They become evidence for the broader differentiation hypothesis only when Stage F1 has shown that the second trait is functionally distinct enough to interpret the extra dimension.

## Stage F5 — mechanism-resolved differentiation

Run the selective crossed design

```text
x x y x function-2 environment x function-1 environment.
```

In the current floral implementation:

```text
A x D x antagonist x pollinator
16 cells.
```

Estimate the existing channels

```text
rho_delta    antagonist relief
iota_delta   pollinator interference
m0_delta     pollinator-independent baseline interaction
U_delta      remaining unallocated residual.
```

Only after an independent assay may the appropriate residual be biologically interpreted as a joint cost / allocation channel.

The mechanism-resolved differentiation claim is strongest when

```text
antagonist relief is positive and substantial
pollinator interference is small enough not to erase the relief
remaining joint cost is independently bounded
```

and the attraction optimum / effect is released in the direction predicted from Chapter 1.

## Residual coupling diagnostic

The four-way

```text
x x y x E1 x E2
```

interaction is an internal diagnostic of incomplete functional separability.

In the floral case this is the registered

```text
A x D x G x P
```

interaction.

If non-zero, the effect of one functional coordinate depends on the state of the other functional environment. This is not a failure of the theory; it is evidence for **partial modularity** rather than clean modularization.

## Minimum positive Chapter-2 decision

A strong contemporary functional-differentiation result requires

```text
F1  Chapter-1 compromise established;
F2  x and y have different functional loading profiles;
F3  adding / increasing y shifts x's optimum or reproductive effect toward
    the function-1 preferred state predicted by Chapter 1;
F4  the joint differentiated phenotype improves total reproductive outcome;
F5  selective intervention shows the improvement is generated by the
    intended functional relief rather than an unidentified side pathway.
```

If F2-F4 hold but F5 is incomplete, report

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
-> recover z1*, z2*, zc*

BITA F1
-> validate x/y functional loading

BITA F2
-> multi-level x x y surface
-> test whether x optimum shifts away from compromise

BITA F4/F5
-> two-level outcome hierarchy + full 16-cell mechanism allocation

historical extension
-> test integration -> differentiation through evolutionary time.
```

This sequence makes Chapter 2 a direct mechanistic answer to Chapter 1 rather than a separate attraction-defence study.
