# Impatiens 2018 identification retrofit v1

## Question

Can the strongest current public-data anchor go beyond a treatment-adjusted observational A×D association? We test whether that association changes across the source experiment's randomized supplemental robbing, florivory, and pollination assignments.

This is **not** a rho/iota/kappa reconstruction. The randomized treatments simulated increased interaction intensity rather than selectively excluding consumer channels, and A/D themselves were not randomized.

## Registered model

For each of the two previously audited reproductive components, standardized outcome is regressed on standardized early flower redness (A), standardized early floral condensed tannins (D), the full randomized Robbing × Florivory × Pollination factorial, all A- and D-by-treatment lower-order interactions needed for hierarchy, A×D, the three targeted A×D×treatment modifiers, and standardized pre-treatment flowering date. HC3 intervals are reported.

Because treatments are effect-coded N=-0.5 / Y=+0.5, each A×D×treatment coefficient is the difference in the observational A×D slope between the randomized Y and N assignment levels, conditional on the declared model.

## Results

### ch_fruits_per_plant_per_day

Complete cases: 170; residual df: 149; randomized-cell n range: 19–24.

| target term | estimate | HC3 SE | 95% CI |
|---|---:|---:|---:|
| `A_z:D_z` | -0.1628 | 0.1045 | [-0.3675, +0.0419] |
| `A_z:D_z:Robbing_c` | -0.0434 | 0.1918 | [-0.4194, +0.3325] |
| `A_z:D_z:Florivory_c` | -0.3078 | 0.1939 | [-0.6879, +0.0723] |
| `A_z:D_z:Pollination_c` | +0.0748 | 0.2295 | [-0.3750, +0.5246] |

Randomized treatment cell counts: N/N/N=19, N/N/Y=23, N/Y/N=23, N/Y/Y=20, Y/N/N=20, Y/N/Y=24, Y/Y/N=21, Y/Y/Y=20.

### seeds_per_ch_fruit

Complete cases: 85; residual df: 64; randomized-cell n range: 6–14.

| target term | estimate | HC3 SE | 95% CI |
|---|---:|---:|---:|
| `A_z:D_z` | -0.0936 | 0.2912 | [-0.6643, +0.4771] |
| `A_z:D_z:Robbing_c` | -0.2539 | 0.7325 | [-1.6896, +1.1818] |
| `A_z:D_z:Florivory_c` | -0.3551 | 0.6602 | [-1.6492, +0.9390] |
| `A_z:D_z:Pollination_c` | -0.1696 | 0.4155 | [-0.9840, +0.6448] |

Randomized treatment cell counts: N/N/N=12, N/N/Y=12, N/Y/N=14, N/Y/Y=9, Y/N/N=12, Y/N/Y=13, Y/Y/N=7, Y/Y/Y=6.

## Identification interpretation

The A×D term is still an observational trait association. The A×D×Robbing, A×D×Florivory, and A×D×Pollination terms ask whether randomized supplemental agent assignments modify that association. Even if one of these terms is nonzero, it cannot be renamed rho or iota because the source treatments are intensity additions rather than selective present/excluded channel toggles.

This retrofit therefore has a deliberately asymmetric role: it shows how far a high-information public dataset can be pushed toward the new identification design while preserving the point at which identification fails.

