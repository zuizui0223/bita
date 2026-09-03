# From compromise to modularity: functional differentiation as an escape from multifunctional constraint

## Abstract

Multifunctional traits are evolutionarily constrained when distinct functions favor different values of one shared phenotype. Chapter 1 / SCH identifies this one-dimensional compromise. Here we ask the complementary Chapter-2 question: **when does an additional trait dimension allow the functions to become more independently tunable?** We define functional differentiation as a shift from one shared coordinate `z` toward partially distinct coordinates `x` and `y` that preferentially load on different functions. In the ideal local quadratic benchmark, the one-dimensional architecture pays a mismatch penalty `[ab/(a+b)](z1*-z2*)^2`; differentiation can recover that loss only if its extra developmental, construction, regulatory, or ecological cost is smaller than the avoided compromise. This produces two experimentally distinct claims. First, a second coordinate should release the focal `x` trait from the opposing function and shift its optimum toward the function-1 optimum identified by SCH. Second, the differentiated architecture should improve fitness beyond the shared-state benchmark while maintaining preferential functional loading. We operationalize these predictions in the floral attraction-defence system, where attraction `A` and antagonist-reducing trait `D` are the first concrete `x,y` implementation. The existing two-level `A x D` interaction, its `A0/A1` release hierarchy, partial-identification framework, and `A x D x antagonist x pollinator` 16-cell design remain the core measurable machinery. The four-way consumer interaction additionally diagnoses residual functional coupling: an architecture with two traits can still be only partially modular. Existing evidence shows that antagonist-reducing traits, pollinator-preserving guarded states, component partitioning, conditional gating, and route separation occur in nature, and a manipulated `A x D`-like reproductive surface exists in *Nicotiana attenuata*. What remains missing is one complete system that starts from an identified Chapter-1 compromise, adds a preferentially loaded second trait coordinate, demonstrates uncertainty-bearing dimensional release, allocates the responsible channels, and independently measures the added cost. We therefore separate contemporary functional differentiation from the stronger historical claim of modularization from an ancestral shared trait.

## 1. The Chapter-2 problem

Chapter 1 begins with one shared phenotype:

```text
function 1 ---\
               >--- trait z ---> compromise / balance
function 2 ---/
```

When the function-specific optima differ, `z` cannot maximize both functions simultaneously. The resulting compromise creates a simple evolutionary opportunity: increase the dimensionality of the phenotype.

Chapter 2 asks whether the architecture changes toward

```text
function 1 -> trait x
function 2 -> trait y,
```

so that the two functions can be tuned more independently.

The central question is:

> **Does functional differentiation release the fitness penalty created when multiple functions were forced to share one trait coordinate?**

This framing is broader than attraction and defence. The floral system remains the first operational implementation because existing data and identification tools already resolve several pieces of the problem.

## 2. What counts as functional differentiation

Two observed traits are not automatically two functional modules. A differentiated architecture requires three nested properties.

### 2.1 Distinct coordinates

The phenotype contains at least two independently measurable and manipulable coordinates `x` and `y`.

### 2.2 Preferential functional loading

The functional response matrix should be approximately diagonal:

```text
          function 1   function 2
trait x      strong       weak
trait y      weak         strong.
```

Cross-loading need not be zero, but it must be measured rather than assumed away.

### 2.3 Functional release

The additional dimension must improve the attainable phenotype relative to the constrained shared state. The strongest form is an optimum shift: after `y` carries more of function 2, the preferred `x` state moves toward the function-1 optimum recovered in SCH.

Thus differentiation is an architectural claim, not merely a positive interaction between two traits.

## 3. Shared-to-differentiated benchmark

Under the Chapter-1 local quadratic model,

```text
L_shared(z)
  = a (z - z1*)^2
  + b (z - z2*)^2.
```

The shared optimum is

```text
zc* = (a z1* + b z2*) / (a + b)
```

and the unavoidable one-dimensional mismatch is

```text
L_compromise*
  = [a b / (a + b)] (z1* - z2*)^2.
```

Now allow two differentiated coordinates:

```text
L_diff(x,y)
  = a (x - z1*)^2
  + b (y - z2*)^2
  + K,
```

where `K` is the additional cost of maintaining the differentiated architecture.

Under ideal independent loading,

```text
x* = z1*
y* = z2*
```

and the maximum advantage of differentiation is

```text
Delta_mod
  = [a b / (a + b)] (z1* - z2*)^2 - K.
```

Differentiation is favored in this benchmark when

```text
K < [a b / (a + b)] (z1* - z2*)^2.
```

The biological prediction is direct: **the stronger the one-axis conflict identified by SCH, the larger the potential return to adding a preferentially loaded trait dimension, unless the cost or residual coupling of that dimension is too large.**

## 4. The strongest cross-chapter test: optimum release

The most informative Chapter-2 prediction is not simply that the two-trait state has higher fitness. It is that the focal trait optimum moves when the second functional coordinate becomes available.

Let `x` inherit most of the original function-1 role. If the shared `z` optimum was displaced away from `z1*` because it also had to satisfy function 2, then adding `y` should produce

```text
|x*(y_high) - z1*| < |x*(y_low) - z1*|.
```

That is, the second coordinate releases `x` toward its function-1 optimum.

The corresponding function-2 prediction is symmetric when `y` can be studied across multiple levels.

This **dimensional-release test** is stronger than a generic `x x y` interaction because it explicitly uses the Chapter-1 optimum as the reference state.

## 5. Floral implementation: attraction and defence

The current mapping is

```text
function 1 = pollinator-mediated reproductive gain
function 2 = avoidance / reduction of antagonist-mediated loss

trait x = attraction trait A
trait y = antagonist-reducing trait D.
```

This mapping does not require antagonists to stop detecting `A`. Functional differentiation can occur because `D` acts later in the interaction pathway: access, handling, ingestion, oviposition, damage, or another antagonist-reducing process.

The floral problem is therefore a particularly useful test of **functional** rather than necessarily informational modularity.

## 6. Existing BITA outcome hierarchy

For two declared levels of attraction and defence, retain

```text
W00, W10, W01, W11.
```

Define

```text
A0 = W10 - W00
A1 = W11 - W01
Delta_AD W = A1 - A0
           = W11 - W10 - W01 + W00.
```

The existing outcome hierarchy remains unchanged:

```text
Level 1 — positive interaction relief
Delta_AD W > 0

Level 2 — constraint release
A0 <= 0 < A1

Level 3 — strict reversal
A0 < 0 < A1.
```

Under the broader architecture framing, these quantities ask whether the second trait dimension makes the focal attraction axis more favorable. They do **not** by themselves demonstrate preferential loading, optimum release, or historical modularization.

## 7. Mechanism allocation and residual coupling

The complete floral mechanism design crosses

```text
A x D x antagonist x pollinator
```

in 16 cells.

The total interaction can be written as

```text
Delta_AD W = rho_delta - iota_delta - kappa_delta,
```

where

```text
rho_delta   = antagonist relief
iota_delta  = pollinator interference
kappa_delta = independently validated remaining joint channel.
```

Without additional information, a measured total interaction defines an identified set rather than a unique allocation. Selective consumer interventions, pollinator-independent baseline handling, explicit restrictions, and an independent joint-cost assay progressively shrink that set.

The remaining residual must not be called `kappa` by subtraction.

### 7.1 The four-way interaction as a modularity diagnostic

The `A x D x antagonist x pollinator` interaction tests whether the putatively differentiated traits remain context-coupled across the two functions. If the pollination consequence of `D` depends on antagonist state, or the antagonist consequence of `D` depends on pollinator state, the architecture is only partially modular.

Thus the existing four-way separability diagnostic becomes an empirical measure of **residual functional coupling**.

## 8. Preferential-loading tests

A strong Chapter-2 result should estimate, directly or through selective intervention, all four functional arrows:

```text
x -> function 1
x -> function 2
y -> function 1
y -> function 2.
```

The target architecture has

```text
|x -> function 1| > |x -> function 2|
|y -> function 2| > |y -> function 1|,
```

with uncertainty appropriate to the intended comparison.

In the floral implementation, this means attraction should retain a strong pollinator-facing effect, while the defence coordinate should reduce antagonist-mediated loss without an equivalent pollinator penalty.

The current BITA route-separation result already supplies a real-world qualitative prediction: when pollinators and antagonists occupy separable effective access/response domains, defence is more likely to preserve legitimate function; overlapped domains create interference, and bypassable defences fail to carry the intended function.

## 9. Real-world evidence for functional differentiation

### 9.1 Component partitioning

Existing floral systems show that one complex display can contain components with different ecological functions. In *Petunia*, targeted perturbation of scent components recovers compounds with host-location versus deterrent effects. This is direct component-function differentiation, although a common pollinator-antagonist fitness test is still missing.

### 9.2 Conditional gating

In *Biscutella*, a cue shared by bees and crab spiders is conditionally induced after florivore attack, and population differences in inducibility occur under common-garden conditions. This is a state-dependent architectural solution: the plant changes when a shared cue is deployed rather than making the cue fully private.

### 9.3 Route separation and guarded function

The BITA source synthesis recovers recurrent cases in which spatial, temporal, chemical, or geometric separation allows an antagonist-reducing trait to preserve pollination. It also recovers overlapped and bypassable cases in which defence interferes with pollinators or fails to block the antagonist. These systems ground preferential loading as a real ecological property rather than an abstract matrix condition.

### 9.4 A manipulated two-trait reproductive surface

Kessler et al. (2008) crosses floral benzylacetone and nicotine production in all four combinations in *Nicotiana attenuata*. Under the registered aggregate-compatible analysis, the attraction effect in the defended state `A1` is uniformly positive, the low-defence effect `A0` remains close to and spans zero, and the aggregate `Delta_AD` sign remains positive. Exact source/design-based uncertainty and clean flower-restricted defence scope remain unresolved.

This is therefore a strong existing anchor for interaction-level release, not a complete proof of functional differentiation from an identified Chapter-1 compromise.

## 10. Experimental hierarchy for Chapter 2

A complete programme should proceed in stages.

```text
Stage 0 — inherit the SCH reference
identify z1*, z2*, zc* and the local functional conflict

Stage 1 — establish two trait coordinates
validate x and y as stable, manipulable dimensions

Stage 2 — test preferential loading
estimate all four trait-to-function arrows

Stage 3 — test dimensional release
measure whether x* shifts toward z1* when y carries more of function 2
and whether common fitness improves beyond the shared benchmark

Stage 4 — allocate the release mechanism
A x D x antagonist x pollinator
plus pollinator-independent baseline and independent joint-cost assay

Stage 5 — evolutionary/historical extension
show stable developmental/genetic modularity or reconstruct
an ancestral shared architecture -> differentiated descendants.
```

The two-level `A x D` experiment is therefore a powerful Stage-3 local test, while the 16-cell experiment addresses Stage 4.

## 11. A functional-differentiation ladder

```text
D0  distinct measured trait coordinates
D1  preferential functional loading
D2  functional release beyond the constrained reference
D3  mechanism-resolved differentiation
D4  stable ecological / developmental modularity across contexts
D5  historical modularization from an ancestral integrated state.
```

Existing BITA evidence reaches parts of D0-D2 across different systems. No screened system currently closes D0-D3 in one complete chain anchored to a directly identified SCH compromise.

D5 is a separate historical question.

## 12. Relationship to the current identification paper

The existing canonical BITA identification manuscript remains the detailed operational treatment of the floral special case. Its primary contribution is still valid:

- `Delta_AD W` is directly measurable;
- a total interaction does not uniquely identify the mechanism;
- partial identification is possible under declared restrictions;
- selective crossed interventions can identify the biotic channels;
- the remaining joint channel requires an independent assay.

The present chapter-level manuscript adds the broader evolutionary interpretation: **the same design is testing whether added trait dimensionality releases a multifunctional compromise and how complete that functional differentiation actually is.**

## 13. Main predictions

1. Systems with stronger Chapter-1 compromise penalties should have greater potential benefit from functional differentiation, conditional on the extra cost `K`.
2. A valid differentiated architecture should show preferential functional loading rather than two equally pleiotropic traits.
3. Adding the function-2 coordinate should shift the optimum of the function-1 trait toward the function-1 optimum identified by SCH.
4. Functional release should be greatest when cross-loading and residual consumer coupling are small.
5. Large `A x D` interaction relief without preferential loading is insufficient evidence of modularity.
6. Contemporary differentiation and historical modularization should be tested separately.

## 14. Current claim ceiling

The current evidence supports the positive statement that ecological systems repeatedly implement partial functional separation: different floral components can carry different roles, conditional gating changes when shared cues are deployed, and antagonist-reducing traits can preserve pollination when effective domains are separated. A manipulated attraction-by-defence-like reproductive surface also exists.

What remains missing is one complete cross-chapter demonstration:

```text
identified shared-trait compromise in SCH
+
validated x,y coordinates
+
preferential functional loading
+
uncertainty-bearing dimensional release
+
mechanism allocation
+
independent architecture cost.
```

The current conceptual status is

```text
REAL_WORLD_FUNCTIONAL_SEPARATION_RECOVERED
INTERACTION_LEVEL_RELEASE_ANCHOR_RECOVERED
COMPLETE_DIFFERENTIATION_CHAIN_NOT_YET_IDENTIFIED.
```

## 15. Conclusion

Functional differentiation is a natural evolutionary response to multifunctional constraint, but it should not be inferred merely because two traits exist or because their interaction is favorable. The causal sequence begins in Chapter 1: quantify the compromise generated by forcing two functions onto one phenotype. Chapter 2 then asks whether a second dimension makes those functions more independently tunable, whether the original trait optimum is released toward its preferred state, and which mechanisms and costs determine the realized gain. This architecture-level framing turns attraction and defence from a special ecological interaction into a general test case for how evolution moves from integrated compromise toward modular organization.
