# Manuscript Results tables v1

These tables are manuscript-facing summaries derived from the locked *Impatiens*
outputs. They are not new analyses.

## Table 2. Response-scale channel models

| Route | Response scale | Unit | Effect scale | Estimate | 95% CI | Status |
|---|---|---|---|---:|---|---|
| A: early flower redness -> pollinator use | 60-min standardized visit count/rate | plant | RR per 1 SD | 0.981 | 0.626, 1.539 | unresolved |
| D candidate: log1p early floral tannins -> pollinator use | 60-min standardized visit count/rate | plant | RR per 1 SD | 0.682 | 0.479, 0.972 | pollination-cost-like association |
| A: early flower redness -> natural floral damage | individual-flower tissue-loss fraction | flower, clustered by plant | OR per 1 SD | 1.064 | 0.933, 1.213 | unresolved |
| D candidate: log1p early floral tannins -> natural floral damage | individual-flower tissue-loss fraction | flower, clustered by plant | OR per 1 SD | 1.121 | 0.990, 1.269 | no resolved protective association |
| A × D candidate -> seeds per CH fruit | individual CH-fruit seed count | fruit, clustered by plant | RR per 1 SD × 1 SD | 1.008 | 0.968, 1.049 | unresolved component surface |

Notes: A and D candidate coefficients are observational associations adjusted for
declared treatment assignments and phenology. RR = rate ratio; OR = odds ratio.
These results do not identify causal effects of flower redness or floral tannins.

## Table 3. Pollinator hurdle model-adequacy sensitivity

| Hurdle component | Predictor | Effect scale | Estimate | 95% CI | Status |
|---|---|---|---:|---|---|
| Any observed pollinator visit | D candidate: log1p early floral tannins | OR per 1 SD | 0.780 | 0.511, 1.191 | unresolved |
| Positive visit intensity, conditional on at least one visit | D candidate: log1p early floral tannins | RR per 1 SD | 0.515 | 0.332, 0.799 | lower intensity among visited plants |

Notes: The hurdle analysis is a post-primary model-adequacy sensitivity motivated by
52 zero-visit plants among 81 complete plants and primary Pearson dispersion of
23.18. It must not replace the primary response-scale pollinator-rate model or be
used for selective reporting.

## Table 4. Randomized factorial reproductive-component models

| Treatment/covariate | Response component | Model | Estimate scale | Estimate | 95% CI | Status |
|---|---|---|---|---:|---|---|
| Supplemental florivory assignment | CH fruits per plant per day | full Robbing × Florivory × Pollination factorial | standardized coefficient | -0.290 | -0.540, -0.040 | randomized reproductive-component cost |
| Supplemental florivory assignment | seeds per CH fruit | full Robbing × Florivory × Pollination factorial | standardized coefficient | -0.142 | -0.622, 0.338 | unresolved |
| Phenology | CH fruits per plant per day | full Robbing × Florivory × Pollination factorial | standardized coefficient | -0.493 | -0.617, -0.369 | strong reproductive-component association |

Notes: The randomized treatment design has all eight assignment cells represented:
200 valid assignments, 25 plants in each Robbing × Florivory × Pollination cell. The
descriptive baseline-complete subset contains 170 plants, with 19–24 plants per cell.
Treatment coefficients are causal assignment contrasts for the stated reproductive
components only. They are not causal effects of flower redness or floral tannins and
are not total lifetime-fitness estimates.

## Table 5. Part A component interpretation ledger

| Part A component | Empirical analogue in *Impatiens* | Result | Interpretation |
|---|---|---|---|
| `b_A`: A -> pollinator use | redness -> pollinator rate | unresolved | no precise attraction-use association in this panel |
| `c_D`: D -> pollinator cost | tannin candidate -> pollinator rate | RR 0.682 [0.479, 0.972] | cost-like observational association |
| `d_A`: A -> antagonism | redness -> natural floral damage | unresolved | no precise attraction-antagonism association in this panel |
| `e_F`: D -> antagonism suppression | tannin candidate -> natural floral damage | OR 1.121 [0.990, 1.269] | no resolved protective direction |
| A × D reproductive component | redness × tannin candidate -> seeds per CH fruit | RR 1.008 [0.968, 1.049] | unresolved component surface |
| H -> reproductive component | imposed florivory -> CH fruits/day | beta -0.290 [-0.540, -0.040] | randomized downstream cost of floral damage |

Notes: This ledger is not a complementarity/substitutability test. It maps which
routes are visible, unresolved, or experimentally supported in one case study.
