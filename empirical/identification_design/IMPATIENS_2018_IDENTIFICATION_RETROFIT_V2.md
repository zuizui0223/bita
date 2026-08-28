# Impatiens 2018 identification retrofit v2

## Why v2 exists

The previous retrofit analyzed CH fruit production and seeds per CH fruit. The fixed Dryad v4805 processed table also contains `Total_Fruits_Per_Day`, defined in the deposited schema as a CH+CL fruit-production endpoint. Version 2 reruns the unchanged hierarchical HC3 model on that additional endpoint rather than treating the CH-only component as the broadest available reproductive readout.

Source dataset: Soper Gorden & Adler, Dryad doi:10.5061/dryad.0j96d17. The exact public version archive used by the reproducible workflow is `https://datadryad.org/api/v2/versions/4805/download`.

## Identification boundary

The addition improves **outcome coverage**, not causal identification.

- `A = Early_Season_Flower_Redness` and `D = Early_Season_Condensed_Tannins` are observational pre-treatment traits.
- Robbing, florivory and pollination are randomized supplemental interaction treatments, not selective consumer present/excluded interventions.
- `Total_Fruits_Per_Day` combines CH and CL fruit production, but does not integrate seeds per fruit or lifetime reproduction.
- Therefore a positive interval would still be an observational A×D reproductive association rather than causal evidence that `Delta_AD W > 0` under manipulated A and D.

## Reanalysis result

All three outcomes use the same hierarchical HC3 model with the full randomized Robbing × Florivory × Pollination factorial, the A/D hierarchy, `A:D`, `A:D:Robbing`, `A:D:Florivory`, `A:D:Pollination`, and pre-treatment phenology adjustment.

| Endpoint | n | `A:D` estimate | HC3 95% CI | Sign readout |
|---|---:|---:|---:|---|
| `Average_CH_Fruits_Per_Day` | 170 | -0.1628 | [-0.3675, +0.0419] | crosses zero |
| `Total_Fruits_Per_Day` | 170 | **-0.1737** | **[-0.3791, +0.0316]** | **crosses zero** |
| `Average_Seeds_Per_CH_Fruit` | 85 | -0.0936 | [-0.6643, +0.4771] | crosses zero |

For the newly added total-fruit endpoint, the randomized context modifiers also remain unresolved:

| Term | Estimate | HC3 95% CI |
|---|---:|---:|
| `A:D:Robbing` | -0.0272 | [-0.4353, +0.3809] |
| `A:D:Florivory` | -0.3353 | [-0.7760, +0.1054] |
| `A:D:Pollination` | +0.1960 | [-0.2601, +0.6520] |

Randomized-cell sample sizes for `Total_Fruits_Per_Day` range from 19 to 24 plants; residual df = 149.

## What changed scientifically

The result is stronger than the earlier statement that the sign was unresolved because only narrower reproductive components had been inspected. The deposited CH+CL total-fruit endpoint has now been checked directly and its A×D interval still crosses zero. Its point estimate is negative, not positive.

Thus this public system does **not** supply the missing positive escape-sign anchor. It instead strengthens the bounded conclusion:

```text
Impatiens total-fruit A×D sign: CROSSES_ZERO
causal escape status:          NOT_IDENTIFIED
BITA cross-system escape sign: UNRESOLVED_TOTAL_SIGN_CURRENT_EVIDENCE
```

This is not evidence that attraction–defence escape is absent in nature. It is evidence that the closest public observational trait-pair system remains unable to establish it even after upgrading to the broader deposited fruit-production endpoint.

## Reproducibility receipt

The result was recomputed in GitHub Actions run `33165656343` by `.github/workflows/reanalyze-impatiens-total-fruit.yml`. The job downloaded the fixed Dryad version, located the exact processed CSV, ran `scripts/reanalyze_impatiens_identification_retrofit.py`, executed its endpoint-boundary tests, and uploaded aggregate outputs only. The machine-readable sign receipt is `IMPATIENS_TOTAL_FRUIT_SIGN_RECEIPT_V1.json`.
