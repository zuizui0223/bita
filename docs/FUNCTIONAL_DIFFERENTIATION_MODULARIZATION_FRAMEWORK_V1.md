# Functional differentiation / modularization framework v1

## Chapter-2 question

BITA is Chapter 2 of the SCH -> BITA trait-architecture programme.

Chapter 1 asks what happens when two functions are constrained to one shared trait coordinate. Chapter 2 asks what happens when the system gains additional phenotypic dimensions.

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

The general Chapter-2 hypothesis is:

> **A multifunctional compromise can be released when the functions become more independently tunable on partially distinct trait coordinates.**

The current attraction-defence model is the first ecological implementation of this broader architecture.

## From one dimension to two

In Chapter 1, both functions depend on one coordinate `z`:

```text
W_shared(z) = w1 F1(z) + w2 F2(z) - C(z).
```

When the function-specific optima differ, the shared optimum is a compromise.

Chapter 2 allows two coordinates:

```text
W_diff(x,y) = w1 F1(x,y) + w2 F2(x,y) - C(x,y).
```

Functional differentiation means that the response architecture becomes more selective:

```text
x primarily controls function 1
y primarily controls function 2
```

while cross-effects are reduced enough that `x` and `y` can move the system toward combinations that were inaccessible under one shared coordinate.

The key change is therefore **effective dimensionality**, not simply trait number.

## Preferential functional loading

A differentiated architecture requires evidence that the two traits load differently on the two functions.

In local notation, define a functional-response matrix

```text
          function 1   function 2
trait x      r11          r12
trait y      r21          r22
```

where each `rij` is a declared causal response or fitness-channel effect rather than a raw correlation.

The idealized modular pattern is

```text
|r11| large relative to |r12|
|r22| large relative to |r21|.
```

Perfect zero cross-loading is not required. Biological modules can be partial. The empirical question is whether the added coordinate reduces the functional coupling that caused Chapter-1 compromise.

A single scalar modularity index is not required for the main claim; report the four response contrasts with uncertainty and their biological scales.

## Dimensional-release criterion

The most general comparison is between the best attainable state under the shared constraint and the best state under the differentiated architecture.

```text
W_shared* = max_z W_shared(z)
W_diff*   = max_x,y W_diff(x,y).
```

Define

```text
Delta_mod = W_diff* - W_shared*.
```

A positive `Delta_mod` is an architecture-level release only when the two fitness surfaces are measured on a commensurable scale and the additional construction / maintenance cost of the differentiated architecture is included in `C(x,y)`.

Without a measured shared-state comparator, BITA should make the narrower within-architecture claims based on its factorial interaction and channel decomposition rather than claiming `Delta_mod` directly.

## Evidence ladder

```text
D0  two-trait architecture
    x and y are experimentally distinguishable coordinates

D1  preferential functional loading
    x and y affect the two functions differently

D2  functional release
    the joint x,y state improves the outcome relative to the constrained
    or low-dimensional reference on the same scale

D3  mechanism-resolved differentiation
    selective functional interventions identify why the improvement occurs
    and quantify residual cross-functional interference

D4  stable modularity
    developmental / genetic / ecological independence is replicated across
    contexts or populations

D5  historical modularization
    ancestral shared architecture -> derived differentiated architecture
    is reconstructed phylogenetically / developmentally / genetically
```

Contemporary experiments can establish D0-D3. They do not by themselves establish D5.

## Attraction-defence implementation

The existing BITA model maps naturally onto the generalized architecture.

```text
function 1 = pollinator-mediated reproductive gain
function 2 = antagonist avoidance / reduction of antagonist-mediated loss

trait x = attraction trait A
trait y = antagonist-reducing trait D.
```

The two-level trait interaction remains

```text
Delta_AD W = W11 - W10 - W01 + W00.
```

Define

```text
A0 = W10 - W00
A1 = W11 - W01
Delta_AD W = A1 - A0.
```

The existing outcome hierarchy remains valid:

```text
Level 1  positive interaction relief
         Delta_AD W > 0

Level 2  constraint release
         A0 <= 0 < A1

Level 3  strict reversal
         A0 < 0 < A1.
```

These are now interpreted as tests of whether a second functional coordinate improves or releases the effect of attraction relative to the low-defence state.

They do not, by themselves, establish historical modularization.

## Mechanism decomposition as a modularity test

The full BITA experiment crosses

```text
A x D x antagonist x pollinator
```

in 16 cells.

Its existing channel decomposition remains

```text
rho_delta    antagonist relief
iota_delta   pollinator interference
kappa_delta  independently validated remaining joint channel.
```

This is now also the operational test of **how functionally differentiated the architecture really is**.

A strongly differentiated `D` should produce antagonist relief while imposing limited pollinator interference. A strongly differentiated `A` should preserve the attraction function while the defence coordinate handles antagonist reduction. Residual cross-functional coupling is biologically meaningful rather than nuisance variation.

The `A x D x antagonist x pollinator` four-way interaction remains an internal separability diagnostic. If it is non-zero, the functional effects of one trait depend on the state of the other consumer channel; the architecture is only partially modular.

## What a positive BITA result means

A strong Chapter-2 result would show that:

```text
1. Chapter 1 has already identified a multifunctional compromise;
2. A and D provide partially distinct functional coordinates;
3. the A+D state improves or releases the constrained attraction outcome;
4. selective consumer interventions show that the improvement is generated
   by antagonist relief that is not cancelled by pollinator interference or
   unmeasured joint cost.
```

This is **functional differentiation as an escape from compromise**.

## What it does not mean

Do not infer from a positive `A x D` interaction alone that:

- `A` and `D` evolved by splitting one ancestral trait;
- the antagonist no longer detects the attraction cue;
- the architecture is perfectly modular;
- the two functions are developmentally independent;
- the historical transition has occurred repeatedly.

Those are stronger architectural or historical claims.

## Relationship to existing BITA evidence

The current route ledger and source audits remain useful as real-world evidence that the components of functional differentiation occur in nature:

- antagonist-reducing traits recur;
- some defended states preserve pollination better than others;
- separated, overlapped and bypassable route architectures recur;
- existing experiments occupy complementary parts of the full identification design.

Kessler et al. 2008 remains the strongest manipulated attraction-by-defence-like reproductive surface. Its positive aggregate interaction sign is evidence that a two-coordinate architecture can improve the attraction effect in one real system, but source/design uncertainty and trait-scope caveats prevent promotion to a fully identified release or modularization event.

## Relationship to SCH

The sister projects are now nested by trait dimensionality.

```text
SCH
one shared z
-> identify opposing functional demands
-> recover the compromise surface

BITA
two coordinates x,y
-> test preferential functional loading
-> test whether added dimensionality releases the compromise
-> allocate the mechanism of that release.
```

The two chapters therefore address one general evolutionary problem:

> **When does multifunctional integration favor compromise, and when does functional differentiation favor modularity?**
