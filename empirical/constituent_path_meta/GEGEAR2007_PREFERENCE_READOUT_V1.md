# Gegear, Manson & Thomson (2007): source-complete pollinator-choice audit

## Status

**The primary source is recovered and five source-reported preference effects are reconstructed. They form one independent study cluster and are not a cross-study meta-analysis. The manuscript remains frozen.**

The article is `Ecological context influences pollinator deterrence by alkaloids in floral nectar` (doi: `10.1111/j.1461-0248.2007.01027.x`). The author-hosted PDF was recovered from James D. Thomson's publication page. Its checksum and workflow provenance are recorded in `GEGEAR2007_SOURCE_RECEIPT_V1.json`.

## Biological role gate

The study tests gelsemine in the floral nectar system of `Gelsemium sempervirens` using `Bombus impatiens`, an important legitimate pollinator. The article explicitly frames gelsemine as a defensive alkaloid and links the experimental system to Adler and Irwin's same-species nectar-defence work. It therefore passes the existing linked-primary B-role gate; no generic secondary-metabolite label is used as sufficient evidence.

## Experimental structure

Each bee first experienced both reward conditions and was then recorded for at least 80 visits on a mixed artificial-flower array. Table 2 reports a one-sample test of the proportion of visits to the lower-gelsemine option against 0.5. Sample size is recovered as `df + 1` because the bee is the experimental unit.

The five assays deliberately change ecological context:

| Assay | Lower-gelsemine option | Higher-gelsemine option | Mean visits to higher-gelsemine option |
|---|---|---|---:|
| 1A | 30% sucrose, 0 ng/uL | 30% sucrose, 50 ng/uL | 14% |
| 1B | 50% sucrose, 0 ng/uL | 50% sucrose, 50 ng/uL | 24% |
| 1C | 30% sucrose, 0 ng/uL | 30% sucrose, 5 ng/uL | 16% |
| 2 | 30% sucrose, 0 ng/uL | 50% sucrose, 50 ng/uL | 50% |
| 3 | 30% sucrose, 50 ng/uL | 30% sucrose, 125 ng/uL | 18% |

The source identifies 5 ng/uL as the lowest natural concentration, 50 ng/uL as the middle natural range, and 125 ng/uL as a plausible high concentration or herbivory-associated increase.

## Reconstructed preference effects

The reported one-sample t statistics were converted using the repository's existing t-to-Hedges-g calculation and re-oriented so that a negative value means the higher-gelsemine option received fewer visits. The source applied its tests to arcsine-transformed proportions; raw percentages are retained only for ecological interpretation.

| Assay | Hedges g | Approx. 95% CI | Interpretation |
|---|---:|---:|---|
| 1A | -2.060 | -3.028 to -1.091 | Strong deterrence at equal 30% sucrose and 50 ng/uL gelsemine |
| 1B | -0.707 | -1.334 to -0.080 | Deterrence remains at equal 50% sucrose but is weaker |
| 1C | -1.472 | -2.404 to -0.540 | Deterrence is detected even at 5 ng/uL when rewards are equal |
| 2 | +0.041 | -0.504 to +0.587 | No preference difference when the gelsemine option has more sugar |
| 3 | -2.120 | -3.314 to -0.925 | Strong preference for 50 over 125 ng/uL at equal sugar |

All five effects are retained as dependent rows from `Gegear_2007_Gelsemium`. They are not five replications.

## What this adds

This source gives a direct, experimentally controlled demonstration of the fixed biological hypothesis at the constituent-route level:

- a defence-linked floral chemical can sharply reduce legitimate-pollinator use when alternative flowers offer the same sugar reward;
- that reduction is not a fixed property of the defence label, because increasing the reward of the higher-defence option removes the observed preference difference;
- concentration and alternative-resource quality therefore determine whether a pollinator cost is expressed.

The result is stronger than an abstract-level direction code because treatment conditions, bee-level sample sizes, means, standard errors, and test statistics are source-located. It also shows why a single pooled arrow that ignores reward context would be biologically misleading.

## Why this is not yet pooled with Baracchi et al. (2017)

The preference lane now contains numerical effects from Gegear and Baracchi, but only Gegear currently passes the strict linked B-role gate. In addition, Gegear's reported test used arcsine-transformed proportions, whereas the Baracchi effect reconstruction is not yet documented on the same transformed outcome scale. A cross-study estimate is therefore withheld until metric compatibility and one primary contrast per study are fixed without looking for the most favourable result.

```text
source-complete strict-B preference clusters    1
numerical context clusters outside strict B     1  (Baracchi)
exploratory pooling threshold                   3
status                                          NOT POOLABLE
```

## Inference boundary

These effects establish a conditional marginal `B -> legitimate pollinator choice` route in one system. They do not estimate `iota`, `rho`, `kappa`, the attraction-by-defence mixed partial, or the frequency of complementarity in nature. No theorem, equation, manuscript section, or journal claim is changed.
