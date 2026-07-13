# Part I manuscript readout v1

## Scope

This readout summarizes the predeclared Part I sign-sensitivity sweep. It is a qualitative theoretical result, not an empirical parameter calibration and not an estimate of observed trait covariance. Agreement labels refer only to the finite predeclared tested set and are not claims of mathematical structural robustness.

## Overall sweep

- local phenotype/regime cases: **162**
- total mixed-partial evaluations: **2,592**
- complementary evaluations: **1,279 (49.3%)**
- substitutable evaluations: **1,313 (50.7%)**

Across the full predeclared envelope, neither sign is universal. The model therefore supports conditional attraction-defence regimes rather than a universal trade-off or a universal complementarity claim.

## Biological parameter scenarios

| Scenario | Complementary | Substitutable | N |
|---|---:|---:|---:|
| `baseline` | 315 (48.6%) | 333 (51.4%) | 648 |
| `high_obstruction_high_shared_cost` | 42 (6.5%) | 606 (93.5%) | 648 |
| `high_tracking_low_obstruction_low_shared_cost` | 597 (92.1%) | 51 (7.9%) | 648 |
| `low_tracking_low_obstruction_low_shared_cost` | 325 (50.2%) | 323 (49.8%) | 648 |

The strongest sign shifts follow the route logic of the model. High attraction tracking combined with low pollination obstruction and low shared cost strongly favours a positive `A×D` mixed partial. High pollination obstruction and high shared cost strongly favours a negative `A×D` mixed partial.

## Pollinator service × floral damage pressure

Values below pool only over the predeclared phenotype points, parameter scenarios, and functional-form variants; they are theoretical sign frequencies, not empirical probabilities.

| Pollinator service | Floral damage pressure | Complementary | Substitutable | N |
|---:|---:|---:|---:|---:|
| 0.2 | 0.2 | 106 (36.8%) | 182 (63.2%) | 288 |
| 0.2 | 0.5 | 180 (62.5%) | 108 (37.5%) | 288 |
| 0.2 | 0.8 | 223 (77.4%) | 65 (22.6%) | 288 |
| 0.5 | 0.2 | 64 (22.2%) | 224 (77.8%) | 288 |
| 0.5 | 0.5 | 168 (58.3%) | 120 (41.7%) | 288 |
| 0.5 | 0.8 | 187 (64.9%) | 101 (35.1%) | 288 |
| 0.8 | 0.2 | 48 (16.7%) | 240 (83.3%) | 288 |
| 0.8 | 0.5 | 133 (46.2%) | 155 (53.8%) | 288 |
| 0.8 | 0.8 | 170 (59.0%) | 118 (41.0%) | 288 |

Within this declared grid and scenario family, raising floral damage pressure shifts evaluations toward complementarity, whereas raising pollinator service shifts evaluations toward substitutability when defence carries a pollination cost. This is a property of the tested model family, not an unconditional theorem for arbitrary regime scalings.

## Functional-form sensitivity

| Functional form | Complementary | Substitutable | N |
|---|---:|---:|---:|
| `baseline` | 360 (55.6%) | 288 (44.4%) | 648 |
| `saturating_attraction` | 447 (69.0%) | 201 (31.0%) | 648 |
| `saturating_both_curved_cost` | 208 (32.1%) | 440 (67.9%) | 648 |
| `saturating_defence` | 264 (40.7%) | 384 (59.3%) | 648 |

Functional-form changes alter the location and prevalence of signs, but they do not erase the conditional-regime result within the tested family. Saturating attraction weakens the pollination-obstruction term locally, whereas saturating defence and curved shared cost make positive mixed partials harder to sustain in parts of phenotype space.

## Tested-set agreement classes

Within biological parameter scenarios, sign agreement across the four tested functional forms was:

- `tested_set_unanimous`: **395 / 648 (61.0%)**
- `conditional_majority`: **0 / 648 (0.0%)**
- `mixed_or_sensitive`: **253 / 648 (39.0%)**

Across the entire parameter × functional-form envelope, local cases were:

- `tested_set_unanimous`: **0 / 162 (0.0%)**
- `conditional_majority`: **27 / 162 (16.7%)**
- `mixed_or_sensitive`: **135 / 162 (83.3%)**

No local case was unanimous across every tested parameter-scenario × functional-form evaluation in the full envelope. This is not a failure of the model: biological parameter changes are the hypothesized mechanism that switches attraction-defence regimes. More relevantly, **395 of 648 case × parameter-scenario combinations retained one sign across every predeclared functional form**, while the full envelope still contained both regimes. Unanimity over those four tested forms is not a proof that all admissible functional forms would preserve the sign.

## Manuscript-ready Results statement

> Across 162 local phenotype–interaction cases, four biological parameter scenarios, and four predeclared functional-form variants (2,592 mixed-partial evaluations), attraction and defence were not universally complementary or substitutable. Regime sign shifted in the predicted direction with the balance between antagonist-mediated benefit and pollination/shared costs. The high-tracking, low-obstruction, low-shared-cost scenario was complementary in 92.1% of evaluations, whereas the high-obstruction, high-shared-cost scenario was substitutable in 93.5%. Within the declared pollinator-service × floral-damage grid, increasing floral damage pressure shifted evaluations toward complementarity, whereas increasing pollinator service shifted them toward substitutability. These qualitative regime shifts persisted across the four predeclared functional forms, although the precise sign boundary remained assumption-sensitive.

## Interpretation for the paper

1. **Both regimes occupy substantial parts of the declared model space.** The near-even overall split confirms that the model does not mechanically force one sign.
2. **The sign changes for mechanistically interpretable reasons.** More antagonist tracking and damage relief favour complementarity; more pollination obstruction and direct joint cost favour substitutability.
3. **The conditional result is not confined to one response curve within the tested family.** A majority of case × parameter-scenario combinations preserve their sign across all four predeclared functional forms.
4. **Biological parameter sensitivity is part of the hypothesis, not a sensitivity failure.** A universal sign across all biological scenarios would contradict the paper's central conditional-regime claim.

## Role of the literature layer

The retained literature evidence is used only as route-level mechanism support. It can establish that a declared pathway, such as a flower-associated defence/barrier reducing pollinator use, occurs in some systems. It does not calibrate the complete mixed partial or the regime map.

## Inference boundary

- These are theoretical sign frequencies over a declared grid, not empirical event probabilities.
- The sweep does not estimate model parameters from the retained route-level literature evidence.
- Parameter sensitivity is part of the causal hypothesis: changing route strengths is expected to change the regime.
- Agreement across the tested functional forms is finite-set sensitivity evidence, not proof of mathematical structural robustness.
- Functional-form sensitivity and biological parameter sensitivity must remain reported separately.
