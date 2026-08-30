# Kessler-type Stage-1 trial data contract v1

## Purpose

Stage 1 estimates a four-cell reproductive surface before mechanism allocation. It must answer three nested outcome questions without collapsing them:

```text
Level 1 — interaction relief:
Is the total additive A × D reproductive interaction > 0?

Level 2 — constraint release:
Is attraction non-beneficial without defence but beneficial with defence?

Level 3 — strict reversal:
Is attraction negative without defence and positive with defence?
```

The analysis entry point is `scripts/analyze_kessler_type_stage1.py`. One CSV package contains one predeclared binary reproductive endpoint for one four-cell A × D experiment.

## Required columns

| column | meaning |
|---|---|
| `observation_id` | unique analysis-row identifier |
| `block_id` | independent matched replicate block containing all four A × D cells |
| `plant_id` | experimental plant; its A/D coordinate cannot change |
| `flower_id` | flower/reproductive-unit identifier |
| `A` | attraction state, `0` or `1` |
| `D` | defence state, `0` or `1` |
| `retained` | `1` if included in the primary endpoint analysis, otherwise `0` |
| `outcome_binary` | primary binary reproductive outcome for retained rows, `0` or `1` |
| `outcome_id` | versioned primary endpoint identity; exactly one per package |
| `d_intervention_scope` | `FLOWER_RESTRICTED_VALIDATED`, `SYSTEMIC_SOURCE_FAITHFUL`, or `UNVERIFIED` |
| `assignment_mode` | `RANDOMIZED_INTERVENTION`, `SOURCE_FAITHFUL_GENOTYPE`, or `OTHER_PREDECLARED` |
| `exclusion_reason` | blank for retained rows; mandatory for excluded rows |

## Fixed estimands

For retained observations,

```text
p11 = Pr(outcome=1 | A=1,D=1)
p10 = Pr(outcome=1 | A=1,D=0)
p01 = Pr(outcome=1 | A=0,D=1)
p00 = Pr(outcome=1 | A=0,D=0)

A0 = p10 - p00
     attraction effect when defence is low

A1 = p11 - p01
     attraction effect when defence is high

Delta_AD = p11 - p10 - p01 + p00
         = A1 - A0
```

All three contrasts are computed from each common block-bootstrap draw. This preserves their sampling dependence. The implementation does not reconstruct one interval from two marginal intervals.

## Three nested decision levels

### Level 1 — positive interaction relief

```text
low(Delta_AD) > 0     -> POSITIVE_INTERACTION_RELIEF_IDENTIFIED
high(Delta_AD) <= 0   -> POSITIVE_INTERACTION_RELIEF_REFUTED
otherwise             -> POSITIVE_INTERACTION_RELIEF_UNRESOLVED
```

The historical output field is retained for backwards compatibility:

```text
low(Delta_AD) > 0     -> ESCAPE_IDENTIFIED
high(Delta_AD) <= 0   -> ESCAPE_REFUTED
otherwise             -> ESCAPE_UNRESOLVED
```

`ESCAPE_IDENTIFIED` is therefore a legacy token for Level 1 only. It does not by itself establish that attraction crossed from non-beneficial or negative to positive.

### Level 2 — constraint release

```text
high(A0) <= 0 and low(A1) > 0
    -> CONSTRAINT_RELEASE_IDENTIFIED
```

The claim is refuted when the supplied intervals cannot contain the conjunction—for example, when `low(A0) > 0` or `high(A1) <= 0`. All overlapping cases remain unresolved.

### Level 3 — strict negative-to-positive reversal

```text
high(A0) < 0 and low(A1) > 0
    -> STRICT_REVERSAL_IDENTIFIED
```

A zero-compatible `A0` may support Level 2 but cannot identify strict reversal.

## What no Stage-1 level identifies

None of the three outcome levels allocates the observed surface among:

```text
rho_delta    antagonist relief
iota_delta   pollinator interference
kappa_delta  remaining joint channel / independently validated joint cost
```

They also do not demonstrate cue privacy, a historical shared-to-private transition, a trait optimum, an evolutionary trajectory, or a universal sign across trait/outcome transformations.

## Matched-block requirement

The first-pass registered uncertainty lane resamples `block_id`. Each retained block must therefore contain observations from all four A × D cells. A block that loses an entire cell after exclusions is rejected by this analysis rather than silently converted into an unpaired pooled comparison.

This requirement is a contract for the registered block-bootstrap lane, not a statement that incomplete blocks can never be analyzed scientifically. If real attrition produces incomplete blocks, a predeclared hierarchical/randomization analysis may supersede this lane, but it must preserve `A0`, `A1`, `Delta_AD`, the outcome scale, and the three-level decision hierarchy. It must not borrow individual-flower independence.

## Plant-coordinate gate

A `plant_id` can belong to only one A/D cell. Any apparent treatment drift within a plant is treated as a data-contract error. The analysis does not average or relabel inconsistent plants post hoc.

## Retention and exclusions

Excluded rows remain in the source CSV with `retained=0` and a nonblank `exclusion_reason`. Retention fractions are reported separately for all four cells.

The current power planner assumes 90% retention only for prospective budgeting. Observed retention is not forced to 90%, and lower retention does not automatically invalidate the experiment. However, differential retention is visible in the receipt and must be addressed in the final design-based analysis.

## Defence-scope claim ceiling

The four-cell contrasts can be calculated for any registered D intervention, but the biological claim changes with scope:

- `FLOWER_RESTRICTED_VALIDATED`: eligible for a flower-associated defence interpretation on the declared endpoint;
- `SYSTEMIC_SOURCE_FAITHFUL`: source-faithful Kessler-type contrast, but not a flower-exclusive defence claim;
- `UNVERIFIED`: total manipulated-state contrast only; do not promote to flower-specific defence.

Thus statistical outcome classification and biological intervention scope remain separate gates.

## First-pass uncertainty and output

The registered script uses a percentile bootstrap over complete matched blocks, preserving all retained flowers inside each resampled block. The output records:

```text
cell probabilities and retention
point and 95% block-bootstrap interval for A0
point and 95% block-bootstrap interval for A1
point and 95% block-bootstrap interval for Delta_AD
legacy ESCAPE_IDENTIFIED / REFUTED / UNRESOLVED token
Level-1 interaction-relief status
Level-2 constraint-release status
Level-3 strict-reversal status
D-scope claim ceiling
```

A richer hierarchical model is expected when the final design contains additional plant/day/site nesting. Such a model may supersede the first-pass interval only if it keeps the same A/D coordinates, endpoint and outcome-claim hierarchy.

## Relationship to Stage 2 and Stage 3

```text
Stage 1: A0, A1 and total A × D outcome contrasts
Stage 2: pilot selective antagonist/pollinator and m0/four-way contrasts
Stage 3: re-powered 16-cell mechanism allocation + independent joint-cost assay
```

No Stage-1 result is allowed to manufacture channel values. Conversely, full channel point identification is not required to decide any valid outcome-level contrast whose uncertainty satisfies its registered inequalities.
