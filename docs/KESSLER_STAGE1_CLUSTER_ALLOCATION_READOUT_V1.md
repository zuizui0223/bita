# Kessler Stage-1 plant/cluster allocation readout v1

## Decision

The prospective Stage-1 flower counts are not independent-unit counts. The registered cluster sensitivity therefore translates the four-cell effective sample size into plants and matched blocks using

```text
DE = 1 + (m - 1) * ICC
```

where `m` is introduced flowers per plant. This is an exchangeable planning approximation, not a substitute for the final randomized/hierarchical analysis.

## Practical anchor: 5 flowers per plant, ICC = 0.10

At 90% retention, the central and attenuated Kessler-like scenarios become:

| scenario | power | effective n/cell | DE | plants/cell | total plants | total introduced flowers |
|---|---:|---:|---:|---:|---:|---:|
| Δ=0.22 central | 0.80 | 92 | 1.40 | 29 | 116 | 580 |
| Δ=0.22 central | 0.90 | 124 | 1.40 | 39 | 156 | 780 |
| Δ=0.17 attenuated | 0.80 | 150 | 1.40 | 47 | 188 | 940 |
| Δ=0.17 attenuated | 0.90 | 200 | 1.40 | 63 | 252 | 1260 |

If a block contains one plant from each A×D cell, `plants/cell` is also the required matched-block count under this planning construction.

This makes the current operational Stage-1 target much more interpretable than a flower-only total. Under the default central 80% scenario, a field implementation would aim around **29 plants per A×D state / 116 plants total**, with about five introduced flowers per plant before retention. Under the attenuated 80% scenario, the corresponding anchor is **47 plants per state / 188 plants total**.

## Why more flowers on the same plant are not automatically efficient

Within-plant dependence matters. For the central 80% scenario, moving to 10 flowers per plant with ICC=0.20 gives:

```text
DE = 2.80
plants/cell = 29
total plants = 116
total introduced flowers = 1160
```

The plant count is not reduced relative to the 5-flower/ICC=.10 anchor, while the flower workload doubles. The precise optimum depends on real ICC, attrition, plant availability and operational cost, but the direction is clear: repeated flowers cannot be counted as independent replication.

## Relationship to the Stage-1 analyzer

The prospective planner and realized analysis now meet at the same design object:

```text
planning:  plants/cell + flowers/plant + ICC sensitivity
                 ↓
field data: block_id + plant_id + flower_id + A + D + retained + outcome
                 ↓
analysis: complete-block bootstrap of additive probability-scale ΔAD
                 ↓
ESCAPE_IDENTIFIED / ESCAPE_REFUTED / ESCAPE_UNRESOLVED
```

The registered first-pass analyzer is `scripts/analyze_kessler_type_stage1.py`, and its data contract is `docs/KESSLER_TYPE_STAGE1_DATA_CONTRACT_V1.md`.

## Claim boundary

This grid does not include additional day/site dependence, does not replace a mixed-model or randomization-based power analysis, and does not power `A×D×antagonist`, `A×D×pollinator`, or the four-way separability interaction. Those remain Stage-2/3 targets and must be re-powered from channel-scale pilot information.

The machine receipt `empirical/identification_design/KESSLER_STAGE1_CLUSTER_ALLOCATION_RECEIPT_V1.json` records the Actions run, artifact digest and frozen anchor values.
