# Kessler-type Stage-1 trial data contract v1

## Purpose

Stage 1 exists to answer one question before mechanism allocation:

```text
Is the total additive A × D reproductive interaction > 0 with design-based uncertainty?
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

## Fixed estimand

For retained observations,

```text
p11 = Pr(outcome=1 | A=1,D=1)
p10 = Pr(outcome=1 | A=1,D=0)
p01 = Pr(outcome=1 | A=0,D=1)
p00 = Pr(outcome=1 | A=0,D=0)

Delta_AD = p11 - p10 - p01 + p00
```

The Stage-1 decision is supplied by the 95% uncertainty interval for this same additive probability-scale interaction:

```text
low > 0     -> ESCAPE_IDENTIFIED
high <= 0   -> ESCAPE_REFUTED
otherwise   -> ESCAPE_UNRESOLVED
```

This is the strict total-sign decision only. It does not identify `rho_delta`, `iota_delta`, or `kappa_delta`.

## Matched-block requirement

The first-pass registered uncertainty lane resamples `block_id`. Each retained block must therefore contain observations from all four A × D cells. A block that loses an entire cell after exclusions is rejected by this analysis rather than silently converted into an unpaired pooled comparison.

This requirement is a contract for the registered block-bootstrap lane, not a statement that incomplete blocks can never be analyzed scientifically. If real attrition produces incomplete blocks, a predeclared hierarchical/randomization analysis may supersede this lane, but it must preserve the same total estimand and decision rule and must not borrow individual-flower independence.

## Plant-coordinate gate

A `plant_id` can belong to only one A/D cell. Any apparent treatment drift within a plant is treated as a data-contract error. The analysis does not average or relabel inconsistent plants post hoc.

## Retention and exclusions

Excluded rows remain in the source CSV with `retained=0` and a nonblank `exclusion_reason`. Retention fractions are reported separately for all four cells.

The current power planner assumes 90% retention only for prospective budgeting. Observed retention is not forced to 90%, and lower retention does not automatically invalidate the experiment. However, differential retention is visible in the receipt and must be addressed in the final design-based analysis.

## Defence-scope claim ceiling

The total sign can be calculated for any registered D intervention, but the biological claim changes with scope:

- `FLOWER_RESTRICTED_VALIDATED`: eligible for a flower-associated defence interpretation on the declared endpoint;
- `SYSTEMIC_SOURCE_FAITHFUL`: source-faithful Kessler-type sign, but not a flower-exclusive defence claim;
- `UNVERIFIED`: total manipulated-state sign only; do not promote to flower-specific defence.

Thus statistical sign identification and biological intervention scope remain separate gates.

## First-pass uncertainty

The registered script uses a percentile bootstrap over complete matched blocks, preserving all retained flowers inside each resampled block. The output records:

```text
cell probabilities and retention
point Delta_AD
95% block-bootstrap interval
ESCAPE_IDENTIFIED / REFUTED / UNRESOLVED
D-scope claim ceiling
```

A richer hierarchical model is expected when the final design contains additional plant/day/site nesting. Such a model may supersede the first-pass interval only if it keeps the same A/D coordinates, endpoint and total-sign decision rule.

## Relationship to Stage 2 and Stage 3

```text
Stage 1: total A × D sign
Stage 2: pilot selective antagonist/pollinator and m0/four-way contrasts
Stage 3: re-powered 16-cell mechanism allocation + independent joint-cost assay
```

No Stage-1 result is allowed to manufacture channel values. Conversely, full channel point identification is not required to decide a valid total sign.
