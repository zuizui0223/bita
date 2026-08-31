# Sasidharan et al. 2023 publication-cluster sensitivity

## Gate-C result

The source workbook was recovered directly from the article supplement (DOI `10.1093/aob/mcad064`). Table S1 contains 517 populated FVOC/insect rows and multiple rows per publication. FVOC × insect tests are therefore not treated as independent study replication.

The original article reports a higher row-level FVOC detection proportion for florivores than pollinators. Recomputing the source rows and resampling whole publication-reference clusters gives:

| outcome | florivore | pollinator | F-P difference | 95% publication-cluster bootstrap |
|---|---:|---:|---:|---:|
| detection | 0.819 | 0.706 | +0.113 | [-0.082, +0.311] |
| attraction | 0.233 | 0.356 | -0.123 | [-0.397, +0.078] |
| repulsion | 0.055 | 0.059 | -0.004 | [-0.106, +0.079] |

All three cluster-bootstrap intervals cross zero. The row-level detection contrast is therefore not stable to publication-level dependence. This does **not** establish equal guild responses. It means that the broad between-guild difference is not independently replicated strongly enough for a publication-level generality claim under this dependence-preserving analysis.

## What is positively recovered

The workbook provides a large, source-linked map of response-state heterogeneity across compounds, insect guilds, plant genera and publications. This supports the fixed conditional BITA interpretation at the constituent-route level: receiver response is not a universal property of the compound label and can change with compound, receiver and context.

This result must not be promoted to a direct estimate of `rho`, `iota`, `kappa`, `W_AD`, or attraction-defence complementarity/substitutability. Sasidharan 2023 is a broad FVOC response synthesis, not a complete A × B experiment and not a strict flower-specific B-role meta-analysis.

## Gate C adjudication

```text
source workbook recovered: YES
source rows reproduced: YES
publication dependence reconstructed: YES
row-level universal guild contrast robust to publication clustering: NO
context/sign heterogeneity module: PASS
universal-effect module: FAIL_CLOSED
GATE_C = PASS_AS_HETEROGENEITY_MODULE_NOT_AS_UNIVERSAL_GUILD_EFFECT
```

## Provenance

The recovery-and-analysis workflow run was `33351104986` at branch head `d4e1eb22268eff19e8ec054cfcfbd334873eb271`. The uploaded artifact was `9743632857` (`sasidharan2023-gate-c`; artifact digest `sha256:fd0159aaf65705fb8923646ccd2c7e835f6bc7300efc22b5ab3be1e5a96516dd`). The recovered XLSX SHA-256 was `c6c0a2e48268c479786379b3995ca90732cdf2d724e5addc2e0f1c7e04f0cc19` (173,597 bytes; five worksheets).

No manuscript text is changed by this analysis.
