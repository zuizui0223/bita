# Part I manuscript readout v1

## Scope

This readout summarizes the reproduced Part I sign-sensitivity sweep. It is a qualitative theoretical result, not an empirical parameter calibration and not an estimate of observed trait covariance. The nonlinear response-shape variants are normalized to common endpoint scales on the declared 0–1 trait domain. Agreement labels refer only to the finite predeclared tested set and are not claims of mathematical structural robustness.

## Overall sweep

- local phenotype/regime cases: **162**
- biological parameter scenarios: **4**
- endpoint-normalized response-shape variants: **4**
- total mixed-partial evaluations: **2,592**
- complementary evaluations: **1,342 (51.8%)**
- substitutable evaluations: **1,250 (48.2%)**

Across the full predeclared envelope, neither sign is universal. The model therefore supports conditional attraction-defence regimes rather than a universal trade-off or a universal complementarity claim.

## Biological parameter scenarios

| Scenario | Complementary | Substitutable | N |
|---|---:|---:|---:|
| `baseline` | 344 (53.1%) | 304 (46.9%) | 648 |
| `high_obstruction_high_shared_cost` | 38 (5.9%) | 610 (94.1%) | 648 |
| `high_tracking_low_obstruction_low_shared_cost` | 617 (95.2%) | 31 (4.8%) | 648 |
| `low_tracking_low_obstruction_low_shared_cost` | 343 (52.9%) | 305 (47.1%) | 648 |

The strongest sign shifts follow the declared route logic: scenarios with greater attraction-linked antagonist relief relative to pollination obstruction and direct cross-cost occupy more complementary evaluations, whereas the opposing balance occupies more substitutable evaluations.

## Pollinator service × floral damage pressure

Values below pool only over the predeclared phenotype points, biological parameter scenarios, and endpoint-normalized response-shape variants. They are theoretical sign frequencies, not empirical probabilities.

| Pollinator service | Floral damage pressure | Complementary | Substitutable | N |
|---:|---:|---:|---:|---:|
| 0.2 | 0.2 | 109 (37.8%) | 179 (62.2%) | 288 |
| 0.2 | 0.5 | 196 (68.1%) | 92 (31.9%) | 288 |
| 0.2 | 0.8 | 247 (85.8%) | 41 (14.2%) | 288 |
| 0.5 | 0.2 | 65 (22.6%) | 223 (77.4%) | 288 |
| 0.5 | 0.5 | 170 (59.0%) | 118 (41.0%) | 288 |
| 0.5 | 0.8 | 195 (67.7%) | 93 (32.3%) | 288 |
| 0.8 | 0.2 | 52 (18.1%) | 236 (81.9%) | 288 |
| 0.8 | 0.5 | 126 (43.8%) | 162 (56.2%) | 288 |
| 0.8 | 0.8 | 182 (63.2%) | 106 (36.8%) | 288 |

Within this declared grid and scenario family, increasing floral damage pressure shifts the evaluated balance toward complementarity, whereas increasing pollinator service shifts it toward substitutability when defence carries a pollination cost. This is a property of the tested model family, not an unconditional theorem for arbitrary regime scalings.

## Endpoint-normalized response-shape sensitivity

| Response-shape variant | Complementary | Substitutable | N |
|---|---:|---:|---:|
| `baseline` | 360 (55.6%) | 288 (44.4%) | 648 |
| `saturating_attraction` | 384 (59.3%) | 264 (40.7%) | 648 |
| `saturating_both_curved_cost` | 310 (47.8%) | 338 (52.2%) | 648 |
| `saturating_defence` | 288 (44.4%) | 360 (55.6%) | 648 |

The nonlinear variants preserve the declared endpoint effect scales at `A=1`, `D=1`, and `A=D=1`, while redistributing local marginal effects across trait space. They therefore test response-shape sensitivity more cleanly than the earlier unnormalized alternatives, although they still represent only a finite set of possible biological functions.

## Tested-set agreement classes

Within biological parameter scenarios, sign agreement across the four tested endpoint-normalized response-shape variants was:

- `tested_set_unanimous`: **480 / 648 (74.1%)**
- `conditional_majority`: **0 / 648 (0.0%)**
- `mixed_or_sensitive`: **168 / 648 (25.9%)**

Across the entire biological-parameter × response-shape envelope, local cases were:

- `tested_set_unanimous`: **0 / 162 (0.0%)**
- `conditional_majority`: **42 / 162 (25.9%)**
- `mixed_or_sensitive`: **120 / 162 (74.1%)**

No local case was unanimous across every tested biological-parameter × response-shape evaluation in the full envelope. This is expected for a theory whose central hypothesis is that changing route strengths can switch the local interaction sign. Across fixed biological parameter scenarios, **480 of 648 case × scenario combinations** retained one non-neutral sign across all four endpoint-normalized response-shape variants. This is finite tested-set evidence, not proof that every admissible functional form preserves the sign.

## Scenario-level modal signs after explicit tie handling

Exact complementary/substitutable ties across the four response-shape variants are reported as `mixed`, not assigned to either sign.

| Scenario | Modal complementary | Modal substitutable | Mixed tie | Tested-set unanimous |
|---|---:|---:|---:|---:|
| `baseline` | 65 | 56 | 41 | 97 |
| `high_obstruction_high_shared_cost` | 2 | 150 | 10 | 138 |
| `high_tracking_low_obstruction_low_shared_cost` | 149 | 0 | 13 | 144 |
| `low_tracking_low_obstruction_low_shared_cost` | 66 | 58 | 38 | 101 |

This table corrects the earlier implementation bias that resolved exact modal ties in favour of complementarity.

## Manuscript-ready Results statement

> Across 162 local phenotype–interaction cases, four biological parameter scenarios, and four endpoint-normalized response-shape variants (2,592 mixed-partial evaluations), attraction and defence were not universally complementary or substitutable. The high-tracking, low-obstruction, low-shared-cost scenario was complementary in 95.2% of evaluations, whereas the high-obstruction, high-shared-cost scenario was substitutable in 94.1%. Within the declared pollinator-service × floral-damage grid, increasing floral damage pressure shifted the evaluated balance toward complementarity, whereas increasing pollinator service shifted it toward substitutability. Exact boundaries remained sensitive to the declared biological parameters and response shapes.

## Interpretation for the paper

1. **Both regimes remain present after endpoint normalization.** The full tested envelope contains substantial numbers of both signs rather than mechanically forcing one result.
2. **The sign changes for mechanistically interpretable reasons within the declared model family.** Greater antagonist relief relative to pollination obstruction and cross-cost favours complementarity; the opposing balance favours substitutability.
3. **The conditional result is not confined to one response curve within the tested family.** A majority of case × parameter-scenario combinations preserve one sign across all four endpoint-normalized response-shape variants.
4. **Biological parameter sensitivity is part of the hypothesis, not a sensitivity failure.** A universal sign across deliberately contrasting biological scenarios would contradict the paper's central conditional-regime claim.

## Role of the literature layer

The retained literature evidence is used only as abstract-level route evidence. One predeclared three-cluster manipulation stratum is directionally consistent with a flower-associated chemical barrier reducing pollinator preference or foraging. That does not identify the focal `M_AD` curvature and does not calibrate the complete mixed partial or regime map.

## Inference boundary

- These are theoretical sign frequencies over a declared grid, not empirical event probabilities.
- The response-shape variants share endpoint scales but not identical local derivatives.
- The sweep does not estimate model parameters from the abstract-level route evidence.
- Parameter sensitivity is part of the causal hypothesis: changing route strengths is expected to change the regime.
- Tested-set unanimity is finite-set sensitivity evidence, not mathematical structural robustness.
- The sign and the numerical zero tolerance remain properties of the declared trait and score scales.
