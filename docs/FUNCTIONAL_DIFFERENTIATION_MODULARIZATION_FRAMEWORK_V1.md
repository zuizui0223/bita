# Functional differentiation / modularization framework v1

## Chapter-2 question

BITA is Chapter 2 of the SCH -> BITA trait-architecture programme.

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
functional differentiation / modularization
```

The general hypothesis is:

> **A multifunctional compromise can be released when the functions become more independently tunable on partially distinct trait coordinates.**

## From one dimension to two

Theory may write:

```text
W_shared(z) = w1 F1(z) + w2 F2(z) - C(z)
```

with pure function optima:

```text
z_F1*
z_F2*.
```

But the default empirical SCH handoff is state-specific:

```text
z_P* = argmax W10(z)
z_G* = argmax W01(z)
z_C* = argmax W11(z).
```

Because direct/background effects can remain:

```text
z_P* != automatically z_F1*
z_G* != automatically z_F2*.
```

Chapter 2 then allows two coordinates:

```text
W_diff(x,y) = w1 F1(x,y) + w2 F2(x,y) - C(x,y).
```

Functional differentiation means the response architecture becomes more selective:

```text
x primarily controls function 1
y primarily controls function 2
```

while cross-effects are reduced enough that `x` and `y` can reach combinations inaccessible under one shared coordinate.

The key change is effective dimensionality, not trait count alone.

## Preferential functional loading

Define a functional-response matrix:

```text
          function 1   function 2
trait x      r11          r12
trait y      r21          r22
```

where each `rij` is a declared causal response or fitness-channel effect.

The idealized pattern is:

```text
|r11| large relative to |r12|
|r22| large relative to |r21|.
```

Perfect zero cross-loading is not required. Partial modules are expected; report all four response contrasts with uncertainty.

## Dimensional-release criterion

### Default state-specific empirical release

Let:

```text
x0* = argmax W(x | y0)
x1* = argmax W(x | y1).
```

Use the default SCH reference:

```text
z_ref = z_P*.
```

Define:

```text
R_state = |x0* - z_P*| - |x1* - z_P*|.
```

Positive `R_state` means the added coordinate moves `x` toward the function-1-facing state identified by SCH.

### Optional pure-function release

Only if SCH independently identifies `z_F1*`, report separately:

```text
R_pure = |x0* - z_F1*| - |x1* - z_F1*|.
```

Do not infer `R_pure` from `R_state`.

## Architecture-level gain

The most general theoretical comparison is:

```text
W_shared* = max_z W_shared(z)
W_diff*   = max_x,y W_diff(x,y)
Delta_mod = W_diff* - W_shared*.
```

A positive empirical `Delta_mod` requires the two architectures to be measured on a commensurable fitness scale with added construction / maintenance / regulatory costs included.

Without that comparator, report:

```text
within_bita_optimum_fitness_gain
```

and the dimensional-release estimand, not `Delta_mod`.

## Evidence ladder

```text
D0  two-trait architecture
    x and y are experimentally distinguishable

D1  preferential functional loading
    x and y affect the two functions differently

D2  dimensional release
    x moves toward the declared SCH reference and joint outcome improves

D3  mechanism-resolved differentiation
    selective interventions identify why the improvement occurs

D4  stable modularity
    functional independence is replicated across contexts/populations

D5  historical modularization
    ancestral shared architecture -> derived differentiated architecture
    reconstructed independently.
```

Contemporary experiments can establish D0-D3. They do not establish D5.

## Attraction-defence implementation

```text
function 1 = pollinator-mediated reproductive gain
function 2 = antagonist avoidance / reduction of antagonist-mediated loss

trait x = attraction trait A
trait y = antagonist-reducing trait D.
```

The two-level interaction remains:

```text
Delta_AD W = W11 - W10 - W01 + W00
A0 = W10 - W00
A1 = W11 - W01
Delta_AD W = A1 - A0.
```

Outcome hierarchy:

```text
Level 1  positive interaction relief: Delta_AD W > 0
Level 2  constraint release:          A0 <= 0 < A1
Level 3  strict reversal:             A0 < 0 < A1.
```

These local outcomes do not by themselves establish preferential loading or dimensional release.

## Mechanism decomposition as a modularity test

The full BITA experiment crosses:

```text
A x D x antagonist x pollinator
```

in 16 cells.

Retain:

```text
rho_delta    antagonist relief
iota_delta   pollinator interference
U_delta      remaining unallocated residual.
```

An independently validated joint channel may be named only after its own assay. `U_delta` is not converted into a construction cost by subtraction.

The four-way interaction remains an internal residual-coupling diagnostic. Non-zero coupling means the architecture is partially rather than completely modular.

## What a positive BITA result means

A strong Chapter-2 result shows:

```text
1. SCH already identified a causal shared-trait compromise;
2. x and y provide different functional loading profiles;
3. y moves x toward the declared SCH reference;
4. joint fitness improves;
5. selective intervention explains the release mechanism.
```

By default the declared SCH reference is `z_P*`. Pure `z_F1*` is a separate stronger lane.

## What it does not mean

Do not infer from a positive `A x D` interaction alone that:

- `A` and `D` evolved by splitting one ancestral trait;
- the antagonist no longer detects the attraction cue;
- the architecture is perfectly modular;
- state-specific release equals pure-function release;
- the two functions are developmentally independent;
- the historical transition occurred repeatedly.

## Relationship to existing BITA evidence

The current route ledger and source audits remain real-world evidence that components of functional differentiation occur in nature: antagonist-reducing traits recur, some defended states preserve pollination, separated/overlapped/bypassable architectures recur, and existing experiments occupy complementary parts of the full design.

Kessler et al. 2008 remains the strongest manipulated attraction-by-defence-like reproductive surface. Its positive aggregate interaction is an interaction-level release anchor, not a complete proof of functional differentiation from an identified SCH compromise.

## Relationship to SCH

```text
SCH
one shared z
-> identify z_P*, z_G*, z_C*
-> causal compromise

BITA
two coordinates x,y
-> preferential functional loading
-> state-specific release toward z_P* by default
-> optional pure-function release toward z_F1* when independently identified
-> mechanism allocation.
```

The chapters therefore address one problem:

> **When does multifunctional integration favor compromise, and when does increasing functional dimensionality release it?**
