# SCH → BITA empirical handoff v1

## Purpose

This contract synchronizes BITA Chapter 2 with the current SCH Chapter 1 estimands. It separates the **theory-level architecture bridge** from the **default empirical handoff** so that pure function optima are not silently equated with intervention-defined reproductive optima.

## 1. Theory-level symmetry

SCH theory defines idealized pure function objectives on one shared coordinate `z`:

```text
z_F1* = argmax F1(z)
z_F2* = argmax F2(z)
```

with local quadratic mismatch benchmark

```text
L_shared(z)
  = a (z-z_F1*)^2
  + b (z-z_F2*)^2
```

and

```text
z_C,theory* = (a z_F1* + b z_F2*)/(a+b)
L_compromise,theory*
  = [ab/(a+b)] (z_F1*-z_F2*)^2.
```

BITA's quadratic architecture model is the same theory-level operation in different notation:

```text
theta1 <-> z_F1*
theta2 <-> z_F2*
L_S*   <-> L_compromise,theory*
```

With partial differentiation,

```text
R = s L_S*
Delta_arch = s L_S* - K.
```

This is a **theory benchmark** unless the relevant pure objectives, shared loss and architecture cost are identified on commensurable empirical scales.

## 2. What SCH directly identifies by default

The multi-level `z × P × G` SCH experiment directly estimates reproductive state surfaces:

```text
W00(z) = P0G0
W10(z) = P1G0
W01(z) = P0G1
W11(z) = P1G1
```

and therefore state-specific optima:

```text
z_P* = argmax W10(z)
z_G* = argmax W01(z)
z_C* = argmax W11(z).
```

Because direct and background consequences of `z` may remain in these surfaces,

```text
z_P* != automatically z_F1*
z_G* != automatically z_F2*.
```

BITA must not relabel these state optima as pure function optima.

The decisive contemporary SCH compromise is supported when, on the same coordinate and outcome scale,

```text
z_P* != z_G*
W11(z) has a supported interior z_C*
G off -> z_C* shifts toward z_P*
P off -> z_C* shifts toward z_G*
functional-component gradients near z_C* oppose one another.
```

## 3. Default empirical BITA release test

Let `x` be the retained function-1-facing trait coordinate in the more differentiated phenotype and `y` the added or strengthened second coordinate.

The default empirical Chapter-2 release question is:

```text
Does increasing / adding y move the optimum of x toward the SCH
function-1-facing state reference z_P*?
```

A direct distance form is

```text
|x*(y1) - z_P*| < |x*(y0) - z_P*|.
```

This is **state-specific dimensional release**. It uses a quantity SCH can identify without pretending that the pollinator-only reproductive state is a pure pollination objective.

For the floral implementation:

```text
SCH z    = shared attraction/display coordinate
BITA x   = attraction coordinate A
BITA y   = antagonist-reducing coordinate D
SCH z_P* = attraction optimum under pollinator-present / antagonist-suppressed state
```

The BITA two-level interaction hierarchy

```text
Level 1: Delta_AD W > 0
Level 2: A0 <= 0 < A1
Level 3: A0 < 0 < A1
```

remains useful for local functional relief, but it does not replace the multi-level dimensional-release test toward `z_P*`.

## 4. Optional stricter pure-function lane

SCH may optionally identify context-stable functional-component optima using contrasts such as

```text
M_G0(z) = W10(z)-W00(z)
M_G1(z) = W11(z)-W01(z)
H_P0(z) = W01(z)-W00(z)
H_P1(z) = W11(z)-W10(z).
```

If the function-1 component optimum is stable across the other consumer state and passes the prospectively declared equivalence/uncertainty gate, SCH may export an empirical `z_F1*`.

Only then may BITA add the stricter question

```text
|x*(y1) - z_F1*| < |x*(y0) - z_F1*|.
```

The state-specific and pure-function release analyses must be reported separately.

## 5. Mechanism identification after dimensional release

Even a positive dimensional-release result does not identify why the multi-trait phenotype works. The existing BITA mechanism layer remains necessary:

```text
A × D × antagonist × pollinator
-> identified set / partial identification
-> four-way separability diagnostic
-> selective channel allocation
-> independent remaining-channel assay.
```

A non-zero four-way `A × D × G × P` term is also evidence that the ostensibly differentiated axes retain context-dependent cross-loading; functional differentiation is therefore partial rather than perfectly modular.

## 6. Symmetric claim ceiling

```text
SCH state-specific compromise
!= pure function-optimum identification

SCH compromise
!= proof that a new axis historically evolved

BITA positive Delta_arch or dimensional release
!= proof that the historical transition occurred

BITA positive A × D interaction
!= dimensional release toward z_P*

structural separation
!= functional independence

case/route recurrence
!= prevalence.
```

## 7. Unified experimental sequence

```text
SCH Stage 1
local z × P × G conflict identification
        ↓
SCH Stage 2
multi-level z × P × G
recover z_P*, z_G*, z_C* and causal compromise geometry
        ↓
optional SCH upgrade
identify context-stable component optimum z_F1*
        ↓
BITA Stage 1
validate two preferentially loaded coordinates x,y
        ↓
BITA Stage 2
test dimensional release of x toward z_P*
(optional stricter lane toward z_F1*)
        ↓
BITA Stage 3
crossed mechanism allocation and residual-coupling diagnostic
        ↓
historical extension
reconstruct integrated -> differentiated architecture only with transition evidence.
```

## Bottom line

The sister-paper symmetry is not simply `SCH estimates L_S* and BITA uses it`. The defensible pairing is:

```text
THEORY
SCH pure-function mismatch benchmark
<-> BITA shared-versus-differentiated architecture benchmark

EMPIRICS
SCH state-specific causal compromise geometry
-> BITA state-specific dimensional-release test
-> optional pure-function release only after the stronger SCH identification gate.
```
