# SCH Chapter 1 -> BITA Chapter 2 positioning v1

## One programme

The sister projects answer one architectural question:

```text
How do organisms solve conflicting functional demands on phenotype?
```

The chapter sequence is

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

The ideal handoff contains

```text
z1* = function-1 preferred value
z2* = function-2 preferred value
zc* = combined shared-trait optimum
```

with

```text
z1* != z2*
```

and causal evidence that weakening each function moves the shared optimum / gradient toward the other function's preferred state.

This is the constraint BITA tries to release.

## BITA response

Chapter 2 introduces a second functional coordinate.

```text
x = function-1-facing coordinate
y = function-2-facing coordinate.
```

The key prediction is not merely `x x y != 0`. It is that `y` changes the accessible optimum of `x` in the direction predicted by the Chapter-1 compromise.

If Chapter 1 showed

```text
function 1 favors larger z
function 2 holds the combined optimum lower,
```

then Chapter 2 predicts

```text
x*(y high function-2 protection)
    >
x*(y low function-2 protection)
```

with the sign reversed when the Chapter-1 geometry is reversed.

Thus the direction of the BITA prediction must be inherited from SCH rather than declared generically.

## Floral implementation

For the current floral programme:

```text
function 1 = pollinator-mediated reproduction
function 2 = antagonist avoidance / reduction of antagonist-mediated loss

z = shared attraction/display coordinate in SCH
x = attraction trait A in BITA
y = antagonist-reducing trait D in BITA.
```

The conceptual sequence is

```text
stronger attraction
-> more pollinator gain
-> also more antagonist exposure
-> attraction optimum held at compromise

add a functionally differentiated D
-> reduce antagonist penalty
-> attraction can move toward its pollinator-facing optimum
-> joint phenotype may exceed the old compromise.
```

## Local and global tests

The existing BITA two-level interaction is the local test:

```text
Delta_AD W = W11 - W10 - W01 + W00.
```

A positive value means `D` makes the attraction effect more positive.

The stronger architecture-level test is multi-level:

```text
A0* = argmax_A W(A | D low)
A1* = argmax_A W(A | D high).
```

The Chapter-1 geometry predicts the direction of

```text
A1* - A0*.
```

The full 16-cell consumer design then identifies **why** the optimum / effect shifts.

## Result hierarchy across chapters

```text
SCH-L1  same trait serves both functions
SCH-L2  function-specific optima differ
SCH-L3  combined optimum is a causal compromise

BITA-D1 two traits have different functional loading
BITA-D2 second trait releases the constrained outcome / optimum
BITA-D3 selective interventions identify the release mechanism
BITA-D4 residual coupling is quantified

History   ancestral integration -> derived differentiation reconstructed.
```

## Why this positioning matters

This chapter sequence prevents three common overclaims.

1. An intermediate phenotype is not called compromise until functional optima and intervention shifts are recovered.
2. A positive two-trait interaction is not called modularization until functional loading and dimensional release are shown.
3. Contemporary functional differentiation is not called an ancestral trait split without historical evidence.

The programme can therefore make strong contemporary ecological claims while keeping historical evolutionary claims fail-closed.
