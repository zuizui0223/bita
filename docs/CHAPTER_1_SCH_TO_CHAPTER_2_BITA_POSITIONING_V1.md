# SCH Chapter 1 -> BITA Chapter 2 positioning v1

## One programme

The sister projects answer one architectural question:

```text
How do organisms solve conflicting functional demands on phenotype?
```

The chapter sequence is:

```text
Chapter 1 / SCH
function 1 ---\
               >--- shared trait z ---> compromise / balance
function 2 ---/

Chapter 2 / BITA
shared compromise
      ↓
function 1 ---> trait x
function 2 ---> trait y
      ↓
functional differentiation / modularization.
```

## Handoff object from SCH

Chapter 1 should deliver an experimentally identified compromise geometry rather than only a narrative statement.

The default empirical handoff is:

```text
z_P* = pollinator-present / antagonist-suppressed state optimum
z_G* = pollinator-suppressed / antagonist-present state optimum
z_C* = combined shared-trait optimum.
```

A positive SCH result requires distinct state optima, a supported combined optimum, opposing causal optimum shifts, and opposing functional-component gradients.

Theory may additionally define pure function optima:

```text
z_F1*
z_F2*.
```

But:

```text
z_P* != automatically z_F1*
z_G* != automatically z_F2*.
```

Pure function optima require an additional identifying assay for direct/background pathways.

## BITA response

Chapter 2 introduces a second functional coordinate:

```text
x = function-1-facing coordinate
y = function-2-facing coordinate.
```

The key prediction is not merely `x x y != 0`. It is that `y` changes the accessible optimum of `x` in the direction predicted by the Chapter-1 compromise.

### Default empirical prediction

Use the directly identified SCH state-specific reference:

```text
z_ref = z_P*.
```

Then test:

```text
|x*(y1) - z_P*| < |x*(y0) - z_P*|.
```

### Optional stricter prediction

Only if SCH independently identifies `z_F1*`, additionally test:

```text
|x*(y1) - z_F1*| < |x*(y0) - z_F1*|.
```

The sign/direction of the BITA prediction is therefore inherited from SCH rather than declared generically.

## Floral implementation

```text
function 1 = pollinator-mediated reproduction
function 2 = antagonist avoidance / reduction of antagonist-mediated loss

z = shared attraction/display coordinate in SCH
x = attraction trait A in BITA
y = antagonist-reducing trait D in BITA.
```

The conceptual sequence is:

```text
stronger attraction
-> more pollinator gain
-> also more antagonist exposure
-> attraction held at a shared compromise

add a functionally differentiated D
-> reduce antagonist penalty
-> attraction optimum moves toward z_P* by default
-> joint phenotype may exceed the old compromise.
```

## Local and multi-level tests

The existing BITA two-level interaction is the local test:

```text
Delta_AD W = W11 - W10 - W01 + W00.
```

A positive value means `D` makes the attraction effect more positive.

The stronger multi-level test is:

```text
A0* = argmax_A W(A | D low)
A1* = argmax_A W(A | D high).
```

and the primary release estimand is distance to the declared SCH reference, not simply the raw sign of `A1* - A0*`.

The full 16-cell consumer design then identifies **why** the optimum / effect shifts.

## Result hierarchy across chapters

```text
SCH-L1  same trait serves both focal functional routes
SCH-L2  intervention-defined state optima differ
SCH-L3  combined optimum is a causal compromise
SCH-Lx  optional pure function optima independently identified

BITA-D1 two traits have different functional loading
BITA-D2 second trait releases x toward declared SCH reference
BITA-D3 selective interventions identify the release mechanism
BITA-D4 residual coupling is quantified

History   ancestral integration -> derived differentiation reconstructed.
```

## Why this positioning matters

This chapter sequence prevents four overclaims.

1. An intermediate phenotype is not called compromise until state-specific optima and intervention shifts are recovered.
2. State-specific optima are not relabeled as pure function optima without an independent identifying assay.
3. A positive two-trait interaction is not called modularization until functional loading and dimensional release are shown.
4. Contemporary functional differentiation is not called an ancestral trait split without historical evidence.

The programme can therefore make strong contemporary ecological claims while keeping theory-level and historical claims fail-closed.
