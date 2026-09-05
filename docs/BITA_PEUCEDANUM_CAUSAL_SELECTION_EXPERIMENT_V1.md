# BITA Peucedanum causal antagonism-dependent selection experiment v1

## Purpose

`Peucedanum multivittatum` already provides strong real-world evidence for partial functional modularization:

```text
perfect flower -> male function + female/seed function + seed-predator target
male flower    -> male/display function without a direct seed-bearing target.
```

The next causal question is **not** the canonical Pedicularis `R_state` question. It is:

> does seed predation causally change the fitness value of allocating a terminal umbel toward perfect versus male flowers?

The first decisive experiment therefore randomizes antagonist damage while retaining the naturally expressed floral sex allocation.

## Stage A — randomized antagonist context on natural sex allocation

For each focal plant define:

```text
q = perfect flowers / (perfect + male flowers)
```

and randomize, within preregistered blocks:

```text
G0 = EGGS_REMOVED
     predator eggs are counted shortly after flowering and removed with forceps
     before hatching

G1 = EGGS_RETAINED
     predator eggs are counted at the same stage but left in place.
```

The egg-removal method itself has direct precedent in the 2025 Peucedanum field experiment. The new element is the randomized retained control, which makes antagonist-mediated modification of the fitness landscape identifiable.

### Timing

The sequence is:

```text
flowering / male-function period
-> record floral composition and display
-> record predator eggs
-> randomize / apply egg removal versus retention
-> record initial fruit production before predation damage
-> record final intact and predated fruits
-> estimate male fitness by paternity or a preregistered male-function proxy.
```

Because egg treatment occurs after flowering, it should not alter the earlier pollen-donor opportunity. This is checked rather than assumed.

## Primary estimand

Fit the same preregistered standardized model in the two antagonist states or, equivalently, one interaction model:

```text
female_final_z
  ~ q_z + G + q_z:G
    + total_flower_z
    + flower_height_z
    + flowering_day_z.
```

Code:

```text
G = 0 for EGGS_REMOVED
G = 1 for EGGS_RETAINED.
```

Then:

```text
beta_removed  = beta_q
beta_retained = beta_q + beta_qG
Delta_beta_q  = beta_retained - beta_removed = beta_qG.
```

The primary prediction is:

```text
Delta_beta_q < 0.
```

That result means predator presence causally makes allocation toward seed-bearing perfect flowers less favourable.

This is a **randomized antagonism-dependent selection result**. Because `q` itself is not randomized in Stage A, it is not yet a fully causal effect of sex allocation.

## Selectivity and mechanism guards

### 1. Pre-treatment randomization balance

The two G groups must be acceptably balanced on:

```text
q
perfect flowers
male flowers
total flowers
flower height
flowering day
eggs counted before treatment.
```

### 2. Initial female opportunity is upstream of G damage

Fit:

```text
initial_fruit_z ~ q_z + G + q_z:G + controls.
```

The G main effect and `q:G` interaction must remain inside prospectively frozen bounds. If egg removal changes initial fruit production, the intervention timing or handling is contaminated.

### 3. Male function is not changed by post-flowering G

Preferred male outcome:

```text
sired seed count from paternity assignment.
```

Fit:

```text
male_fitness_z ~ q_z + G + q_z:G + controls.
```

For the partial-modularization interpretation:

```text
G effect ≈ 0
q:G effect ≈ 0
q effect after controlling total display is small enough to support preserved male function.
```

The last statement is an equivalence/tolerance claim and must not be inferred merely from `p > 0.05`.

### 4. Antagonist treatment must actually change damage

Predation relief is:

```text
mean(predated / initial fruits | EGGS_RETAINED)
-
mean(predated / initial fruits | EGGS_REMOVED).
```

The lower confidence bound must exceed the preregistered minimum.

### 5. Pre-treatment oviposition remains a mechanistic secondary outcome

Because egg number is recorded before G is applied, the association

```text
eggs_before_treatment ~ q + total display + height + flowering time
```

is observational with respect to `q`, but helps connect the manipulated damage result to predator host selection.

## Stage-A positive claim

A positive receipt supports:

```text
CAUSAL_ANTAGONISM_DEPENDENT_SELECTION_ON_SEX_ALLOCATION
```

if:

```text
randomization balance passes
+ egg removal strongly reduces predation damage
+ Delta_beta_q is sufficiently negative
+ initial fruit production is not altered by G beyond tolerance
+ male fitness is not altered by post-flowering G beyond tolerance.
```

It does not yet support:

```text
q itself causally determines fitness
canonical SCH -> BITA R_state
complete x/y modularity
historical origin of andromonoecy.
```

## Stage B — stronger causal sex-composition manipulation

The stronger upgrade manipulates floral composition itself.

A biologically useful window exists because perfect and male flowers have overlapping male-phase function, while perfect flowers later become morphologically distinguishable during the female phase and predator moths often oviposit then.

The proposed pilot is therefore:

```text
complete the common male phase
-> before substantial oviposition, identify flower sex at female transition
-> retain a fixed total number of floral units
-> vary the retained perfect-flower fraction q
-> apply equal handling / removal load across treatments
-> then cross with EGGS_REMOVED versus EGGS_RETAINED.
```

Candidate q levels for a pilot should be chosen from the feasible natural range only after field reconnaissance. Do not freeze arbitrary levels before confirming that enough male and perfect flowers are simultaneously available.

### Stage-B validity gates

Do not promote this manipulation unless all pass:

```text
sex classification accuracy validated against later morphology / fruiting
negligible predator eggs present before q manipulation
total retained flower count equal within tolerance across q treatments
removal / handling load matched across q treatments
flower-height and phenology balance preserved
male-phase pollen opportunity completed before manipulation
no treatment-specific mechanical damage beyond tolerance.
```

If these fail, retain Stage A as the causal antagonist-selection experiment and do not call the q manipulation causal.

## Why this is a Chapter-2 result

The design does not ask whether one shared trait is held at an intermediate optimum. It asks whether an already differentiated flower-class architecture changes the cost of carrying female/seed function under antagonism while retaining pollen-donor display.

Thus the Chapter-2 hierarchy is:

```text
published partial modularization
-> Stage A: causal antagonism-dependent value of the architecture
-> Stage B: causal flower-class composition effect if manipulation validates
-> optional historical analysis of the origin of andromonoecy.
```

## Claim ceiling

Even a positive Stage B supports contemporary causal partial functional differentiation, not complete evolutionary modularity. Perfect flowers still carry both male and female functions, so the architecture is intrinsically partially coupled.
