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

Chapter 1 identifies a causal one-dimensional compromise on a shared coordinate `z`. Chapter 2 asks whether two partially distinct coordinates `x` and `y` make the functions more independently tunable.

A differentiated architecture requires more than two traits. It requires **preferential functional loading** with cross-functional effects measured rather than assumed away.

## Theory bridge and empirical reference

At the theory level, pure function-specific objectives may have optima:

```text
z_F1*
z_F2*.
```

The ideal local quadratic benchmark is:

```text
L_shared(z)
  = a (z - z_F1*)^2
  + b (z - z_F2*)^2
```

with theoretical compromise penalty:

```text
L_compromise,theory*
  = [a b / (a + b)] (z_F1* - z_F2*)^2.
```

If differentiated coordinates can independently approach the pure function optima but cost an additional amount `K`, the ideal theory-level gain is:

```text
Delta_mod
  = [a b / (a + b)] (z_F1* - z_F2*)^2 - K.
```

This is a theory benchmark. The crossed SCH experiment directly identifies state-specific reproductive optima:

```text
z_P* = observed_estimands.z_pollinator_context
z_G* = observed_estimands.z_antagonist_context
z_C* = observed_estimands.z_combined.
```

Because direct/background effects can remain in those state surfaces:

```text
z_P* != automatically z_F1*
z_G* != automatically z_F2*.
```

The **default empirical dimensional-release test** therefore asks whether adding `y` moves `x*` toward `z_P*`.

A stricter pure-function release test is allowed only when SCH independently exports `identified_pure_function_optima.z_F1`.

This distinction is implemented in `trait_architecture/dimensional_release.py` with:

```text
sch_reference_mode = state_specific   # default
sch_reference_mode = pure_function    # requires independent SCH z_F1*
```

## Floral attraction-defence implementation

```text
function 1 = pollinator-mediated reproductive gain
function 2 = antagonist avoidance / reduced antagonist-mediated loss

trait x = attraction trait A
trait y = antagonist-reducing trait D.
```

For two declared attraction and defence levels, retain:

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

A positive interaction alone does not prove modularity.

## Empirical dimensional release

Use multiple `x` levels and at least two `y` states:

```text
x0* = argmax W(x | y0)
x1* = argmax W(x | y1).
```

Default release estimand:

```text
R_state
  = |x0* - z_P*| - |x1* - z_P*|.
```

Positive `R_state` means the added function-2-facing coordinate moves `x` toward the function-1-facing state identified in SCH.

Optional strict lane, only with independently identified `z_F1*`:

```text
R_pure
  = |x0* - z_F1*| - |x1* - z_F1*|.
```

State-specific and pure-function release are reported separately.

Within-BITA improvement is reported as:

```text
within_bita_optimum_fitness_gain
```

and is not called empirical `Delta_mod` unless shared and differentiated architecture fitness scales are explicitly commensurable and added architecture costs are included.

## Mechanism identification

The full floral design crosses:

```text
A x D x antagonist x pollinator
```

in 16 cells.

The total interaction does not point-identify antagonist relief (`rho_delta`), pollinator interference (`iota_delta`), and the remaining joint channel. The inference ladder remains:

```text
interaction detection
-> identified set
-> partial identification under declared bounds
-> point identification after selective crossed interventions
-> independent joint-channel validation.
```

The residual:

```text
U_delta = rho_delta - iota_delta - Delta_AD W
```

remains unallocated. It is not called `kappa` by subtraction.

## Functional modularity as an empirical property

A strongly differentiated `D` should reduce antagonist-mediated loss without an equivalent pollinator penalty. A strongly differentiated `A` should preserve its pollination function while `D` carries more of the antagonist-reduction function.

The `A x D x antagonist x pollinator` four-way term is therefore also a **residual functional-coupling diagnostic**. A non-zero term means the two-trait architecture remains context-coupled and only partially modular.

## Functional-differentiation ladder

```text
D0  distinct measured trait coordinates
D1  preferential functional loading
D2  dimensional release toward the declared SCH reference
D3  mechanism-resolved differentiation
D4  stable ecological / developmental modularity across contexts
D5  historical modularization from an ancestral integrated state.
```

BITA can experimentally target D0-D3. D5 requires independent historical evidence.

## Real-world evidence role

The route ledger and primary-source audits are a **real-world functional-architecture evidence layer**. They show that antagonist-reducing traits recur, defence is not uniformly costly to pollination, separated/overlapped/bypassable effective domains recur, component partitioning and conditional gating occur, and a manipulated `A x D`-like reproductive surface exists in *Nicotiana attenuata*.

Current bounded status:

```text
REAL_WORLD_FUNCTIONAL_SEPARATION_RECOVERED
INTERACTION_LEVEL_RELEASE_ANCHOR_RECOVERED
STATE_SPECIFIC_DIMENSIONAL_RELEASE_ANALYZER_READY
PURE_FUNCTION_RELEASE_REQUIRES_STRONGER_SCH_INPUT
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

These are recurrence and anchor results; route counts are not prevalence estimates.

## SCH -> BITA experiment

```text
SCH
recover z_P*, z_G*, z_C*
show causal optimum shifts when either function is weakened
        ↓
BITA
validate x and y
estimate all four trait-to-function arrows
        ↓
show x* moves toward z_P* when y carries more function 2
        ↓
optional stricter lane if SCH identifies z_F1*
show x* moves toward pure z_F1*
        ↓
A x D x antagonist x pollinator
allocate why the release occurs
        ↓
independent architecture / joint-cost assay.
```

## Canonical reader path

- `manuscript/MANUSCRIPT_FUNCTIONAL_DIFFERENTIATION.md` — **canonical Chapter-2 manuscript**
- `docs/BITA_EMPIRICAL_DIMENSIONAL_RELEASE_ANALYSIS_V1.md` — empirical release estimand and claim boundary
- `docs/BITA_EXECUTION_SPINE_V1.md` — end-to-end execution sequence
- `docs/FUNCTIONAL_DIFFERENTIATION_IDENTIFICATION_CONTRACT_V1.md` — experiment and claim hierarchy
- `docs/FUNCTIONAL_DIFFERENTIATION_MODULARIZATION_FRAMEWORK_V1.md` — generalized architecture theory
- `manuscript/FUNCTIONAL_DIFFERENTIATION_FIGURE_MAP_V1.md` — main figure plan
- `docs/BROAD_FUNCTIONAL_DIFFERENTIATION_REALITY_CHECK_V1.md` — broad architecture grounding
- `empirical/identification_design/BITA_FUNCTIONAL_DIFFERENTIATION_PREDICTION_LEDGER_V1.csv` — machine-readable prediction contract
- `manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md` — detailed attraction-defence identification implementation.

## Reproducibility core

Primary implementation includes:

- `trait_architecture/functional_differentiation.py`
- `trait_architecture/dimensional_release.py`
- `scripts/analyze_bita_dimensional_release.py`
- `tests/test_functional_differentiation.py`
- `tests/test_dimensional_release.py`
- existing identification and partial-identification code/tests.

## Inference boundaries

```text
marginal route recurrence
!= total A x D interaction
!= state-specific dimensional release
!= pure-function dimensional release
!= preferential functional loading
!= channel allocation
!= contemporary functional modularity
!= historical modularization.
```

Accordingly, positive interaction relief does not imply modularization; state-specific release does not imply pure-function release; extant two-trait specialization does not prove an ancestral one-trait split; and zero independent joint-cost assays does not imply zero architecture cost.

## Submission state

The existing attraction-defence identification manuscript remains technically mature as a detailed special-case paper. The new Chapter-2 manuscript supplies the broader evolutionary interpretation without retroactively upgrading the current empirical claim ceiling.
