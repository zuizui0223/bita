# Part I manuscript readout v1

## Scope

This readout summarizes the predeclared Part I sign-robustness sweep. It is a
qualitative theoretical result, not an empirical parameter calibration and not an
estimate of observed trait covariance.

## Overall sweep

- local phenotype/regime cases: **162**
- total mixed-partial evaluations: **2,592**
- complementary evaluations: **1,279 (49.3%)**
- substitutable evaluations: **1,313 (50.7%)**

Across the full predeclared envelope, neither sign is universal. The model therefore
supports conditional attraction-defence regimes rather than a universal trade-off or
a universal complementarity claim.

## Biological parameter scenarios

| Scenario | Complementary | Substitutable | N |
|---|---:|---:|---:|
| `baseline` | 315 (48.6%) | 333 (51.4%) | 648 |
| `high_obstruction_high_shared_cost` | 42 (6.5%) | 606 (93.5%) | 648 |
| `high_tracking_low_obstruction_low_shared_cost` | 597 (92.1%) | 51 (7.9%) | 648 |
| `low_tracking_low_obstruction_low_shared_cost` | 325 (50.2%) | 323 (49.8%) | 648 |

The strongest sign shifts follow the route logic of the model. High attraction
tracking combined with low pollination obstruction and low shared cost strongly
favours a positive A×D mixed partial. High pollination obstruction and high shared
cost strongly favours a negative A×D mixed partial.

## Pollinator service × floral damage pressure

Values below pool only over the predeclared phenotype points, parameter scenarios, and
functional-form variants; they are theoretical sign frequencies, not empirical
probabilities.

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

The central regime pattern is monotonic in the expected direction over this declared
grid: raising floral damage pressure shifts evaluations toward complementarity,
whereas raising pollinator service shifts evaluations toward substitutability when
defence carries a pollination cost.

## Functional-form sensitivity

| Functional form | Complementary | Substitutable | N |
|---|---:|---:|---:|
| `baseline` | 360 (55.6%) | 288 (44.4%) | 648 |
| `saturating_attraction` | 447 (69.0%) | 201 (31.0%) | 648 |
| `saturating_both_curved_cost` | 208 (32.1%) | 440 (67.9%) | 648 |
| `saturating_defence` | 264 (40.7%) | 384 (59.3%) | 648 |

Functional-form changes alter the location and prevalence of signs, but they do not
erase the conditional-regime result. Saturating attraction weakens the
pollination-obstruction term locally, whereas saturating defence and curved shared
cost make positive mixed partials harder to sustain in parts of phenotype space.

## Robustness classes

Within biological parameter scenarios, sign stability across the four functional
forms was:

- `structurally_robust`: **395 / 648 (61.0%)**
- `conditional_majority`: **0 / 648 (0.0%)**
- `mixed_or_sensitive`: **253 / 648 (39.0%)**

Across the entire parameter × functional-form envelope, local cases were:

- `structurally_robust`: **0 / 162 (0.0%)**
- `conditional_majority`: **27 / 162 (16.7%)**
- `mixed_or_sensitive`: **135 / 162 (83.3%)**

No local case was structurally robust across the full biological-parameter envelope.
This is not a failure of the model: biological parameter changes are the hypothesized
mechanism that switches attraction-defence regimes. The more relevant robustness
result is that **395 of 648 case × parameter-scenario combinations retained one sign
across every predeclared functional form**, while the full envelope still contained
both regimes.

## Manuscript-ready Results statement

> Across 162 local phenotype–interaction cases, four biological parameter scenarios,
> and four predeclared functional-form variants (2,592 mixed-partial evaluations),
> attraction and defence were not universally complementary or substitutable. Regime
> sign shifted in the predicted direction with the balance between antagonist-mediated
> benefit and pollination/shared costs. The high-tracking, low-obstruction,
> low-shared-cost scenario was complementary in 92.1% of evaluations, whereas the
> high-obstruction, high-shared-cost scenario was substitutable in 93.5%. Across the
> declared pollinator-service × floral-damage grid, increasing floral damage pressure
> shifted evaluations toward complementarity, whereas increasing pollinator service
> shifted them toward substitutability. These qualitative regime shifts persisted
> despite changes in attraction saturation, defence saturation, and shared-cost
> curvature, although the precise sign boundary remained assumption-sensitive.

## Interpretation for the paper

This gives the independent paper a stronger theoretical result than a single baseline
mixed-partial equation alone:

1. **Both regimes occupy substantial parts of the declared model space.** The near-even
   overall split is not the result to emphasize by itself; it confirms that the model
   does not mechanically force one sign.
2. **The sign changes for mechanistically interpretable reasons.** More antagonist
   tracking/damage benefit favours complementarity; more pollination obstruction and
   shared cost favours substitutability.
3. **The conditional result is not an artefact of one response curve.** A majority of
   case × parameter-scenario combinations preserve their sign across all four
   predeclared functional forms.
4. **Biological parameter sensitivity is part of the hypothesis, not a robustness
   failure.** A universal sign across all biological scenarios would contradict the
   paper's central conditional-regime claim.

## Link to the Impatiens case study

The theoretical sweep should be presented first. The *Impatiens* analysis then asks
which route components are visible in one linked empirical system:

- a floral-tannin candidate shows a pollination-cost-like association;
- the corresponding protective association against natural floral damage is not
  resolved;
- imposed florivory experimentally reduces CH fruit production.

The case study therefore does not calibrate the full theoretical model. Instead, it
places one empirical system on an asymmetric subset of the route structure identified
by the theory.

## Role of the literature synthesis

The literature synthesis should be used only as route-level pattern support. It can
show whether route types such as defence/access-related pollination costs or
antagonism-mediated reproductive costs recur across systems. It should not be used to
claim universal causal parameters, and the inability to pool every route is not itself
the main result.

## Inference boundary

- These are theoretical sign frequencies over a declared grid, not empirical event
  probabilities.
- The sweep does not estimate model parameters from the *Impatiens* data or literature
  synthesis.
- Parameter sensitivity is part of the causal hypothesis: changing route strengths is
  expected to change the regime.
- Functional-form robustness and biological parameter sensitivity must remain reported
  separately.
