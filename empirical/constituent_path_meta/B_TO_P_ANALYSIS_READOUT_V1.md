# B-to-pollinator constituent-path analysis readout v1

## Status

**Not ready for manuscript use. The manuscript remains frozen.**

This readout records source-audited quantitative evidence for the `B_to_pollination` constituent pathway and the current independent-study gates. It is an analysis checkpoint, not a manuscript result section.

## Preference/choice lane: Gegear, Manson & Thomson 2007

DOI: `10.1111/j.1461-0248.2007.01027.x`

The author-hosted primary PDF is recovered and Table 1/Table 2 provide five bee-level choice assays. The study uses the same `Gelsemium sempervirens` nectar-defence system linked to Adler and Irwin and therefore passes the linked-primary B-role gate.

Effects are re-oriented so negative values mean that the higher-gelsemine option received fewer visits:

| Assay | Reward contrast | Hedges g | Approx. 95% CI |
|---|---|---:|---:|
| 1A | 0 vs 50 ng/uL; 30% sucrose in both | -2.060 | -3.028 to -1.091 |
| 1B | 0 vs 50 ng/uL; 50% sucrose in both | -0.707 | -1.334 to -0.080 |
| 1C | 0 vs 5 ng/uL; 30% sucrose in both | -1.472 | -2.404 to -0.540 |
| 2 | 0 ng/uL at 30% sucrose vs 50 ng/uL at 50% sucrose | +0.041 | -0.504 to +0.587 |
| 3 | 50 vs 125 ng/uL; 30% sucrose in both | -2.120 | -3.314 to -0.925 |

All five rows are dependent effects from one study cluster. Equal-sugar assays show strong deterrence, whereas increasing sugar in the higher-gelsemine option removes the preference difference. The source therefore supports a conditional defence-to-pollinator-use route, not a fixed negative trait effect.

No single primary Gegear contrast is selected after inspecting the results. The reported tests used arcsine-transformed proportions, so cross-study metric compatibility also remains to be fixed.

## Preference/choice context outside the strict B pool: Baracchi et al. 2017

DOI: `10.1038/s41598-017-01980-1`

The source reports a controlled bumblebee preference experiment with 20 bees per nicotine concentration and 100 consecutive choices per bee. The three dose groups belong to one independent study cluster.

| Nicotine dose | Source context | Preliminary Hedges g vs 50% | Approx. 95% CI | Direction |
|---|---|---:|---:|---|
| 1 ppm | low natural range | +1.138 | +0.583 to +1.693 | preference for higher-nicotine option |
| 2.5 ppm | high natural range | +0.206 | -0.220 to +0.632 | near-neutral |
| 50 ppm | supra-natural | -1.309 | -1.901 to -0.718 | deterrence by higher-nicotine option |

Baracchi is not primary-pool eligible because its focal experiment does not itself establish the required flower-specific antagonist-reduction role for nicotine. It remains quantitative concentration-dependent context.

## Manipulated field visitation: Adler & Irwin 2005

DOI: `10.1890/05-0118`

The authors experimentally manipulated gelsemine as nectar defence and measured nectar robbers and pollinators in the same field system.

| Year | Dose context | High gelsemine | Low gelsemine | lnRR high/low | Approx. 95% CI | Status |
|---|---|---:|---:|---:|---:|---|
| 2002 | supra-natural | 8.9 ± 1.0 visits, n=40 | 11.4 ± 1.1 visits, n=40 | -0.248 | -0.538 to +0.043 | within-study sensitivity |
| 2004 | natural range | 1.71 ± 0.25 visits, n=38 | 2.00 ± 0.31 visits, n=37 | -0.157 | -0.574 to +0.261 | primary visitation effect |

The 2004 effect is the primary row for this independence cluster. Residence time, proportion probed and pollen transfer remain separate outcomes.

## Route-corrected 2019 visit-number sensitivity

The broad 2019 outcome-lane reconstruction initially yielded three papers and a negative mean (`g=-0.315`, 95% CI `-0.592` to `-0.038`). That paper-level estimate mixed the Adler supra-natural year, the Jones Lepidoptera antagonist response and four Manson doses.

After retaining Adler 2004, retaining only the Jones Bee row and exposing Manson's 0.1, 1, 2 and 4 ug/uL contrasts separately, every three-paper interval includes zero:

| Manson contrast | Random-effects Hedges g | 95% CI | I² |
|---|---:|---:|---:|
| 0.1 vs 0 ug/uL | +0.030 | -0.218 to +0.279 | 0.0% |
| 1 vs 0 ug/uL | -0.183 | -0.456 to +0.090 | 15.6% |
| 2 vs 0 ug/uL | -0.307 | -0.882 to +0.269 | 80.4% |
| 4 vs 0 ug/uL | -0.354 | -1.037 to +0.328 | 86.0% |

The primary source reports no behavioural difference at 0, 0.1 and 1 ug/uL and strong reductions at 2 and 4 ug/uL. The corrected synthesis therefore supports dose-dependent heterogeneity, not a stable universal negative visit-number mean.

This three-paper lane is defence-associated rather than a canonical strict-B pool because Manson does not identify same-system antagonist reduction and the studies remain heterogeneous in assay structure.

## Strict-B observational source: Barlow et al. 2017

DOI: `10.1016/j.cub.2017.07.012`

In `Aconitum`, nectar alkaloids deter nectar-robbing `Bombus terrestris` at lower concentrations than those tolerated by the legitimate pollinator `Bombus hortorum`, while field pollinator visitation declines with increasing alkaloid concentration. The field relationship is observational and is not pooled with manipulation effects. The accepted manuscript reports `n=12`, adjusted `R²=0.27` and `F=5.8`; raw Figshare data remain the preferred route to a fixed standardized association.

## Current pooling gates

```text
strict-B preference/choice lane:
    source-complete independent clusters:       1  (Gegear 2007)
    dependent numerical effect rows:            5
    single primary contrast fixed:              no
    status:                                     NOT POOLABLE

strict-B manipulation visitation lane:
    source-complete independent clusters:       1  (Adler & Irwin 2005)
    primary pool-eligible independent clusters: 1
    status:                                     NOT POOLABLE

defence-associated route-corrected visit-number lane:
    independent papers:                         3
    exploratory threshold:                      reached
    stable direction after route correction:    no
    canonical strict-B status:                  no

strict-B observational visitation lane:
    source-complete independent clusters:       1  (Barlow et al. 2017)
    fixed raw association effect:               pending
    status:                                     NOT POOLABLE
```

## Why outcome lanes remain separate

The source audit gives a direct reason not to create one generic `pollinator response` meta-analysis. Visit frequency, choice proportion, residence time, nectar consumption, pollen transfer, reproduction and learning can move in different directions within the same study. They remain separate lanes.

## High-priority next recovery queue

1. **Jones, Warburton & Martin 2023** — recover the supporting data or an exact model contrast for natural-range ouabain choice/consumption.
2. **Villalona et al. 2020** — convert the source-reported dose-by-species model results into one dependence-aware study record if a common preference contrast can be recovered.
3. **Köhler, Pirk & Nicolson 2012** — identify one source-supported primary feeding contrast without counting dose-by-sugar rows as replication.
4. **Barlow et al. 2017** — recover the Figshare field data to fix the observational association.
5. **Kessler & Baldwin 2007** — keep visit number separate from residence and consumption and retain only compound-specific defence-linked outcomes.

## Current scientific interpretation

The current source audit supports three statements:

1. a flower-defence-to-pollinator conflict is demonstrably real in some systems;
2. its observed sign and magnitude depend on concentration, alternative reward quality, pollinator-response construct and route coding;
3. the repository still lacks enough independent, effect-compatible strict-B studies for a stable pooled estimate.

These observations are consistent with the fixed conditional theory, but they do not estimate `iota`, `rho`, `kappa`, or the full `W_AD` criterion.

## Manuscript decision

No manuscript text, manuscript figures, journal framing or submission materials are updated. Return to manuscript work only after `ANALYSIS_COMPLETION_GATE.md` is satisfied.
