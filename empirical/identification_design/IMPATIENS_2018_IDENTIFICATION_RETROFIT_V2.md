# Impatiens 2018 identification retrofit v2

## Why v2 exists

The previous retrofit analyzed CH fruit production and seeds per CH fruit. The fixed Dryad v4805 processed table also contains `Total_Fruits_Per_Day`, defined in the deposited schema as a CH+CL fruit-production endpoint. Version 2 reruns the unchanged hierarchical HC3 model on that additional endpoint rather than treating the CH-only component as the broadest available reproductive readout.

A secondary sensitivity analysis additionally reconstructs a CH+CL mature-seed-output proxy from deposited mature fruit rates and average seeds per fruit. This fourth outcome is explicitly **derived**, not a deposited response, and is used only to test whether the A×D sign is robust to moving from fruit number toward seed output.

Source dataset: Soper Gorden & Adler, Dryad doi:10.5061/dryad.0j96d17. The exact public version archive used by the reproducible workflow is `https://datadryad.org/api/v2/versions/4805/download`.

## Identification boundary

The additions improve **outcome coverage and sensitivity checking**, not causal identification.

- `A = Early_Season_Flower_Redness` and `D = Early_Season_Condensed_Tannins` are observational pre-treatment traits.
- Robbing, florivory and pollination are randomized supplemental interaction treatments, not selective consumer present/excluded interventions.
- `Total_Fruits_Per_Day` combines CH and CL fruit production, but does not integrate seeds per fruit or lifetime reproduction.
- The reconstructed seed-output quantity combines deposited components but is not itself a deposited endpoint and remains incomplete as lifetime fitness.
- Therefore a positive interval on either endpoint would still be an observational A×D reproductive association rather than causal evidence that `Delta_AD W > 0` under manipulated A and D.

## Reanalysis result

All outcomes use the same hierarchical HC3 model with the full randomized Robbing × Florivory × Pollination factorial, the A/D hierarchy, `A:D`, `A:D:Robbing`, `A:D:Florivory`, `A:D:Pollination`, and pre-treatment phenology adjustment.

| Endpoint | n | `A:D` estimate | HC3 95% CI | Sign readout | Status |
|---|---:|---:|---:|---|---|
| `Average_CH_Fruits_Per_Day` | 170 | -0.1628 | [-0.3675, +0.0419] | crosses zero | deposited component |
| `Total_Fruits_Per_Day` | 170 | **-0.1737** | **[-0.3791, +0.0316]** | **crosses zero** | deposited CH+CL endpoint |
| `Average_Seeds_Per_CH_Fruit` | 85 | -0.0936 | [-0.6643, +0.4771] | crosses zero | deposited component |
| reconstructed CH+CL mature seed output/day | 70 | **+0.1528** | **[-0.5487, +0.8544]** | **crosses zero** | derived sensitivity proxy |

The reconstructed proxy is:

```text
Mature_CH_Fruits_Per_Day * Average_Seeds_Per_CH_Fruit
+ Mature_CL_Fruits_Per_Day * Average_Seeds_Per_CL_Fruit
```

For the deposited total-fruit endpoint, the randomized context modifiers also remain unresolved:

| Term | Estimate | HC3 95% CI |
|---|---:|---:|
| `A:D:Robbing` | -0.0272 | [-0.4353, +0.3809] |
| `A:D:Florivory` | -0.3353 | [-0.7760, +0.1054] |
| `A:D:Pollination` | +0.1960 | [-0.2601, +0.6520] |

Randomized-cell sample sizes for `Total_Fruits_Per_Day` range from 19 to 24 plants; residual df = 149. The derived seed-output proxy has only 70 complete plants and correspondingly much wider uncertainty.

## What changed scientifically

The result is stronger than the earlier statement that the sign was unresolved because only narrower reproductive components had been inspected. The deposited CH+CL total-fruit endpoint has now been checked directly and its A×D interval still crosses zero. Its point estimate is negative.

The derived mature-seed-output proxy moves the point estimate to positive, but its 95% interval spans a very broad negative-to-positive range. That sign reversal across reproductive summaries is itself informative: the current observational panel does not support a stable positive A×D conclusion as the outcome is made more integrative.

Thus this public system does **not** supply the missing positive escape-sign anchor. It instead strengthens the bounded conclusion:

```text
Impatiens deposited total-fruit A×D sign: CROSSES_ZERO
Impatiens derived seed-output A×D sign:   CROSSES_ZERO
point-estimate stability across outcomes: NO
causal escape status:                     NOT_IDENTIFIED
BITA cross-system escape sign:            UNRESOLVED_TOTAL_SIGN_CURRENT_EVIDENCE
```

This is not evidence that attraction–defence escape is absent in nature. It is evidence that the closest public observational trait-pair system remains unable to establish it even after upgrading to the broadest deposited fruit-production endpoint and then stress-testing a more seed-proximal derived outcome.

## Stopping rule

Further construction of nearby observational reproductive summaries from this same panel is now low value. The next valid empirical gate is not another *Impatiens* endpoint. It is a genuinely manipulated `A × D` design measured on one common reproductive surface, followed by selective consumer interventions and a cost assay if mechanism allocation is required.

## Reproducibility receipt

The deposited total-fruit result was first recomputed in GitHub Actions run `33165656343`. The expanded four-outcome sensitivity was recomputed in run `33166169176` by `.github/workflows/reanalyze-impatiens-total-fruit.yml`. The workflow downloaded the fixed Dryad version, located the exact processed CSV, ran `scripts/reanalyze_impatiens_identification_retrofit.py`, executed endpoint-boundary tests, and uploaded aggregate outputs only.

Machine-readable receipts:

- `IMPATIENS_TOTAL_FRUIT_SIGN_RECEIPT_V1.json`
- `IMPATIENS_RECONSTRUCTED_SEED_OUTPUT_SIGN_RECEIPT_V1.json`
