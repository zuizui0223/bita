# Biotic Interaction Trait Architecture (BITA)

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

The general BITA question is:

> **Can increasing trait dimensionality release a compromise created when multiple functions were constrained to one shared phenotype?**

The existing attraction (`A`) by antagonist-reducing trait (`D`) framework is the first floral implementation of this broader functional-differentiation problem. The current canonical paper and identification machinery remain valid; the new framing places them inside a larger Chapter-1 -> Chapter-2 evolutionary sequence.

The generalized framework is `docs/FUNCTIONAL_DIFFERENTIATION_MODULARIZATION_FRAMEWORK_V1.md`.

## Scientific target

Chapter 1 identifies a multifunctional conflict on one shared coordinate `z`. Chapter 2 asks whether two partially distinct coordinates `x` and `y` make the functions more independently tunable.

A differentiated architecture is not defined merely by having two measured traits. It requires **preferential functional loading**:

```text
trait x -> function 1 strongly / selectively
trait y -> function 2 strongly / selectively
```

with cross-functional effects small enough that the joint phenotype can move beyond the one-dimensional compromise.

On commensurable fitness surfaces, the architecture-level target is conceptually

```text
W_shared* = max_z W_shared(z)
W_diff*   = max_x,y W_diff(x,y)
Delta_mod = W_diff* - W_shared*.
```

A direct `Delta_mod` claim requires an actual shared-state comparator and all additional costs of the differentiated architecture. The current BITA experiment therefore uses a narrower and directly measurable two-trait factorial hierarchy unless that stronger comparator is available.

## Attraction-defence implementation

The current floral mapping is

```text
function 1 = pollinator-mediated reproductive gain
function 2 = antagonist avoidance / reduced antagonist-mediated loss

trait x = attraction trait A
trait y = antagonist-reducing trait D.
```

For two experimentally meaningful attraction and defence levels, the primary estimand remains

```text
Delta_AD W = W11 - W10 - W01 + W00.
```

Define

```text
A0 = W10 - W00
A1 = W11 - W01
Delta_AD W = A1 - A0.
```

The outcome hierarchy is unchanged:

```text
Level 1 — positive interaction relief
Delta_AD W > 0

Level 2 — constraint release
A0 <= 0 < A1

Level 3 — strict reversal
A0 < 0 < A1.
```

Under the broader chapter framing, these ask whether the second functional coordinate improves, releases or reverses the attraction outcome that was constrained in the low-defence state.

A positive interaction does **not** by itself prove historical modularization.

## Mechanism identification

The full BITA design crosses

```text
A x D x antagonist x pollinator
```

in 16 cells. The total `Delta_AD W` does not point-identify antagonist relief (`rho_delta`), pollinator interference (`iota_delta`) and the remaining joint channel (`kappa_delta`). If `Delta_AD W = delta`, compatible allocations satisfy

```text
rho_delta - iota_delta - kappa_delta = delta.
```

The inference ladder therefore remains

```text
interaction detection
-> identified set
-> partial identification under declared bounds
-> point identification after selective crossed interventions
-> independent joint-channel validation.
```

The remaining residual

```text
U_delta = rho_delta - iota_delta - Delta_AD W
```

is kept unallocated. It is not called `kappa` by subtraction. A joint construction / allocation channel requires an independent assay.

## Mechanism decomposition as a modularity test

The existing decomposition now has a broader architectural interpretation.

```text
rho_delta    antagonist relief
iota_delta   pollinator interference
kappa_delta  independently validated remaining joint channel.
```

A strongly differentiated defence coordinate should produce antagonist relief without an equivalent pollinator penalty. A strongly differentiated attraction coordinate should preserve its pollination function while the second trait carries more of the antagonist-reduction function.

The `A x D x antagonist x pollinator` four-way interaction is therefore also an internal **residual coupling diagnostic**. A non-zero four-way term means the putatively differentiated architecture remains context-coupled; functional modularity is partial rather than complete.

## Functional-differentiation ladder

```text
D0  two distinct trait coordinates
D1  preferential functional loading
D2  functional release beyond the constrained reference
D3  mechanism-resolved differentiation
D4  stable ecological / developmental modularity across contexts
D5  historical modularization from an ancestral integrated state.
```

BITA can establish D0-D3 experimentally. D5 requires phylogenetic, developmental or genetic evidence and must not be inferred from extant `A + D` alone.

## Mechanism -> Pattern -> Identification bridge

The source-adjudicated recurrence layer contains

```text
56 route records
25 independent biological clusters
A -> pollination:         5 clusters
A -> antagonism:          8
D -> antagonism:         18
D -> pollination:        10
same-system multi-route: 14
context/sign switch:     17.
```

These overlapping counts establish that the constituent pathways of functional differentiation recur in nature. They are not natural-prevalence estimates and do not estimate `Delta_AD W`, `rho_delta`, `iota_delta` or `kappa_delta`.

The stricter identification audit shows design fragmentation: existing studies occupy complementary faces of the full design. Kessler et al. (2008) supplies the closest manipulated trait-factorial side; Egan et al. (2021) the complementary consumer-factorial side; public *Impatiens capensis* data reach randomized context modification of observational traits; *Pedicularis rex* supplies a selective-defence anchor. No screened system closes all allocation dimensions plus an independent joint-cost assay.

The bounded cross-system conclusion remains:

> **The functional components recur and current studies constrain different parts of the architecture, but the complete mechanism of two-trait release is not yet point-identified.**

## Chapter 1 -> Chapter 2

BITA should now be read explicitly as the second step after SCH.

```text
SCH
one shared trait z
-> identify opposing functional demands
-> recover compromise / balance

BITA
two partially distinct traits x,y
-> test preferential functional loading
-> test whether extra dimensionality releases the compromise
-> identify why the release occurs.
```

In the floral implementation, SCH establishes why one attraction/display coordinate can be constrained by pollination and antagonism. BITA then asks whether a distinct antagonist-reducing coordinate lets attraction and protection be tuned more independently.

This is a stronger interpretation than “defence helps attraction”: it is **functional differentiation as an escape from multifunctional compromise**.

## Current positive evidence

The current evidence answers several lower-level questions positively:

- antagonist-reducing traits recur across real systems;
- defence is not uniformly costly to pollination;
- separated, overlapped and bypassable route architectures recur;
- a manipulated `A x D`-like common reproductive surface exists in *Nicotiana attenuata*;
- the Kessler 2008 aggregate interaction sign is robustly positive under registered aggregate-compatible allocations;
- existing studies provide complementary identification components rather than one complete design.

What remains unresolved is the strongest architecture-level event in one complete system:

```text
shared compromise established in Chapter 1
+
preferentially differentiated x,y functions
+
uncertainty-identified release
+
selective channel allocation
+
independent joint-cost assay.
```

Historical integration -> modularization remains a separate later claim.

## Canonical paper

The current attraction-defence identification paper remains the canonical operational implementation:

- `manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md` — canonical scientific text
- `docs/FUNCTIONAL_DIFFERENTIATION_MODULARIZATION_FRAMEWORK_V1.md` — generalized Chapter-2 interpretation
- `docs/DEFENCE_ESCAPE_ROUTE_HYPOTHESIS_RECOVERY.md` — attraction-defence special-case recovery
- `docs/PARTIAL_IDENTIFICATION_FRONTIER_V1.md` — identified-set / bound derivation
- `docs/MECHANISM_PATTERN_IDENTIFICATION_BRIDGE.md` — recurrence / identification boundary
- `docs/QUESTION_METHOD_EXPLANATION_MATRIX.md` — method-specific explanatory reach
- `docs/BITA_DEFENCE_ESCAPE_ROUTE_PRIMARY_SOURCE_AUDIT_V1.md` — high-information primary-source adjudication
- `docs/PUBLICATION_MATERIAL_RECOVERY_LEDGER.md` — paperization state and remaining gates

The generalized framing does not retroactively convert existing attraction-defence evidence into historical modularization evidence.

## Reproducibility core

Primary identification implementation and tests remain:

- `trait_architecture/identification.py`
- `trait_architecture/partial_identification.py`
- `tests/test_identification.py`
- `tests/test_identification_four_way.py`
- `tests/test_identification_coverage.py`
- `tests/test_partial_identification.py`
- `tests/test_partial_identification_balance.py`
- `tests/test_partial_identification_manuscript_integration.py`

## Inference boundaries

```text
marginal route recurrence
!= total A x D interaction
!= functional release
!= channel allocation
!= contemporary functional modularity
!= historical modularization.
```

Accordingly:

- route counts are not prevalence estimates;
- total `Delta_AD W` alone leaves an identified set rather than a unique mechanism;
- positive interaction relief does not imply zero crossing;
- randomized context modification is not selective consumer exclusion;
- a non-zero `A x D x G x P` contrast rejects the simplest separable-channel representation;
- `U_delta` is not `kappa` by definition;
- zero independent joint-cost assays does not imply zero joint cost;
- extant two-trait specialization does not prove an ancestral one-trait split.

## Submission state

The current operational identification manuscript remains a technically mature attraction-defence paper. The new functional-differentiation framing is a programme-level interpretation and should be propagated into the canonical manuscript only where it sharpens, rather than overstates, the empirical evidence.
