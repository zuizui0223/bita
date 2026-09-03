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

The attraction (`A`) by antagonist-reducing trait (`D`) framework is the first floral implementation of this broader problem.

## Scientific target

Chapter 1 identifies a multifunctional conflict on one shared coordinate `z`. Chapter 2 asks whether two partially distinct coordinates `x` and `y` make the functions more independently tunable.

A differentiated architecture requires more than two traits. It requires **preferential functional loading**:

```text
trait x -> function 1 strongly / selectively
trait y -> function 2 strongly / selectively
```

with cross-functional effects measured rather than assumed away.

## Analytic bridge from SCH

Under the local Chapter-1 benchmark

```text
L_shared(z)
  = a (z - z1*)^2
  + b (z - z2*)^2,
```

the one-dimensional compromise penalty is

```text
L_compromise*
  = [a b / (a + b)] (z1* - z2*)^2.
```

If two differentiated coordinates can independently approach the function-specific optima but cost an additional amount `K`, the ideal architecture-level gain is

```text
Delta_mod
  = [a b / (a + b)] (z1* - z2*)^2 - K.
```

Thus the potential value of differentiation grows with the strength of the compromise identified in SCH and disappears if the extra architecture cost is too large.

The strongest cross-chapter prediction is an **optimum release**:

```text
adding the function-2 coordinate y
-> x* shifts toward the function-1 optimum z1* identified in SCH.
```

This is stronger than merely detecting a favorable `x x y` interaction.

## Floral attraction-defence implementation

The current mapping is

```text
function 1 = pollinator-mediated reproductive gain
function 2 = antagonist avoidance / reduced antagonist-mediated loss

trait x = attraction trait A
trait y = antagonist-reducing trait D.
```

For two declared attraction and defence levels, retain

```text
Delta_AD W = W11 - W10 - W01 + W00
A0 = W10 - W00
A1 = W11 - W01
Delta_AD W = A1 - A0.
```

The existing outcome hierarchy remains:

```text
Level 1 — positive interaction relief
Delta_AD W > 0

Level 2 — constraint release
A0 <= 0 < A1

Level 3 — strict reversal
A0 < 0 < A1.
```

Under the broader framing, these test whether the second functional coordinate improves, releases, or reverses the outcome of the focal attraction trait. A positive interaction alone does not prove modularity.

## Mechanism identification

The full floral design crosses

```text
A x D x antagonist x pollinator
```

in 16 cells.

The total interaction does not point-identify antagonist relief (`rho_delta`), pollinator interference (`iota_delta`), and the remaining joint channel (`kappa_delta`). Compatible allocations satisfy

```text
rho_delta - iota_delta - kappa_delta = Delta_AD W.
```

The inference ladder remains

```text
interaction detection
-> identified set
-> partial identification under declared bounds
-> point identification after selective crossed interventions
-> independent joint-channel validation.
```

The residual

```text
U_delta = rho_delta - iota_delta - Delta_AD W
```

remains unallocated. It is not called `kappa` by subtraction.

## Functional modularity as an empirical property

The same 16-cell decomposition now has an architecture-level interpretation.

A strongly differentiated `D` should reduce antagonist-mediated loss without an equivalent pollinator penalty. A strongly differentiated `A` should preserve its pollination function while `D` carries more of the antagonist-reduction function.

The `A x D x antagonist x pollinator` four-way term is therefore also a **residual functional-coupling diagnostic**. A non-zero term means the two-trait architecture remains context-coupled and only partially modular.

## Functional-differentiation ladder

```text
D0  distinct measured trait coordinates
D1  preferential functional loading
D2  functional / dimensional release beyond the constrained reference
D3  mechanism-resolved differentiation
D4  stable ecological / developmental modularity across contexts
D5  historical modularization from an ancestral integrated state.
```

BITA can experimentally target D0-D3. D5 requires independent historical evidence.

## Real-world evidence role

The route ledger and primary-source audits now serve as a **real-world functional-architecture evidence layer**.

They show that:

- antagonist-reducing traits recur across systems;
- defence is not uniformly costly to pollination;
- separated, overlapped, and bypassable effective domains recur;
- component partitioning and conditional gating occur in floral systems;
- a manipulated `A x D`-like reproductive surface exists in *Nicotiana attenuata*;
- existing studies occupy complementary identification faces rather than one complete design.

Current bounded status:

```text
REAL_WORLD_FUNCTIONAL_SEPARATION_RECOVERED
INTERACTION_LEVEL_RELEASE_ANCHOR_RECOVERED
COMPLETE_DIFFERENTIATION_CHAIN_NOT_YET_IDENTIFIED
HISTORICAL_MODULARIZATION_NOT_YET_IDENTIFIED.
```

## Current positive attraction-defence evidence

The existing BITA results remain intact:

- 56 directional route records across 25 independent biological clusters;
- recurrent `D -> antagonism` and `D -> pollination` routes;
- recurrent separated / overlapped / bypassable route architectures;
- Kessler et al. (2008) as the strongest manipulated `A x D`-like common reproductive surface;
- robustly positive aggregate `Delta_AD` sign under registered aggregate-compatible allocations;
- `A1` uniformly positive while `A0` remains close to and spanning zero under the recovered aggregate bounds;
- complete channel allocation and an independent joint-cost assay remain absent.

These are positive pieces of the functional-differentiation story, but no current system starts from a directly identified SCH compromise and closes the whole D0-D3 sequence.

## SCH -> BITA experiment

```text
SCH
recover z1*, z2*, zc*
show causal optimum shifts when either function is weakened
        ↓
BITA
validate x and y
estimate all four trait-to-function arrows
        ↓
show x* moves toward z1* when y carries more function 2
        ↓
measure total dimensional release
        ↓
A x D x antagonist x pollinator
allocate why the release occurs
        ↓
independent architecture / joint-cost assay.
```

This is the main programme-level sequence.

## Canonical reader path

- `manuscript/MANUSCRIPT_FUNCTIONAL_DIFFERENTIATION.md` — **canonical Chapter-2 manuscript**
- `docs/FUNCTIONAL_DIFFERENTIATION_MODULARIZATION_FRAMEWORK_V1.md` — generalized architecture theory
- `docs/FUNCTIONAL_DIFFERENTIATION_IDENTIFICATION_CONTRACT_V1.md` — experiment and claim hierarchy
- `docs/CHAPTER_1_SCH_TO_CHAPTER_2_BITA_POSITIONING_V1.md` — cross-chapter positioning
- `manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md` — detailed attraction-defence identification implementation
- `docs/DEFENCE_ESCAPE_ROUTE_HYPOTHESIS_RECOVERY.md` — attraction-defence evidence recovery
- `docs/PARTIAL_IDENTIFICATION_FRONTIER_V1.md` — identified-set / bound derivation
- `docs/MECHANISM_PATTERN_IDENTIFICATION_BRIDGE.md` — recurrence / identification boundary
- `docs/QUESTION_METHOD_EXPLANATION_MATRIX.md` — explanatory reach and claim ceilings
- `docs/BITA_DEFENCE_ESCAPE_ROUTE_PRIMARY_SOURCE_AUDIT_V1.md` — high-information source audit.

## Reproducibility core

Primary identification implementation and tests remain:

- `trait_architecture/identification.py`
- `trait_architecture/partial_identification.py`
- `tests/test_identification.py`
- `tests/test_identification_four_way.py`
- `tests/test_identification_coverage.py`
- `tests/test_partial_identification.py`
- `tests/test_partial_identification_balance.py`
- `tests/test_partial_identification_manuscript_integration.py`.

## Inference boundaries

```text
marginal route recurrence
!= total A x D interaction
!= functional release
!= preferential functional loading
!= channel allocation
!= contemporary functional modularity
!= historical modularization.
```

Accordingly:

- route counts are not prevalence estimates;
- `Delta_AD W` alone leaves an identified set rather than a unique mechanism;
- positive interaction relief does not imply zero crossing;
- extant two-trait specialization does not prove an ancestral one-trait split;
- a non-zero four-way interaction indicates residual coupling rather than complete modularity;
- zero independent joint-cost assays does not imply zero architecture cost.

## Submission state

The existing attraction-defence identification manuscript remains technically mature as a detailed special-case paper. The new Chapter-2 manuscript supplies the broader evolutionary interpretation without retroactively upgrading the current empirical claim ceiling.
