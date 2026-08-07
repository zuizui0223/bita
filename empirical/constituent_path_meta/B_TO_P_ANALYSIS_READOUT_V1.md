# B-to-pollinator constituent-path analysis readout v1

## Status

**Not ready for manuscript use. The manuscript remains frozen.**

This readout records source-audited quantitative and source-complete evidence for the `B_to_pollination` constituent pathway and the current independent-study gates. It is an analysis checkpoint, not a manuscript result section.

## What was already supported before this extraction

The current `main` directional registry contains a restricted manipulation stratum for flower chemical barriers and pollinator preference/foraging with several directional records, but the canonical quantitative effect table on `main` is empty. Historical branches also contain one observational `Impatiens capensis` floral-tannin coefficient. These records are inputs for re-audit, not a completed meta-analysis.

## Preference/choice lane: Baracchi et al. 2017

DOI: `10.1038/s41598-017-01980-1`

The source reports a controlled bumblebee preference experiment with 20 bees per nicotine concentration and 100 consecutive choices per bee. The experimental unit is the bee, not the individual choice. The three dose groups belong to **one independent study cluster**.

The source directly reports one-sample t statistics against the neutral 50% choice benchmark (`t=5.3`, `0.96`, and `-6.1`, each with `df=19`). Preliminary standardized effects are reconstructed from those reported t statistics rather than rounded mean±SEM values.

| Nicotine dose | Source context | Mean preference | Reported t | Preliminary Hedges g vs 50% | Approx. 95% CI | Direction |
|---|---|---:|---:|---:|---:|---|
| 1 ppm | low natural range | 55.65% | 5.3 | +1.138 | 0.580 to 1.697 | preference for higher-nicotine option |
| 2.5 ppm | high natural range | 51.05% | 0.96 | +0.206 | -0.219 to 0.632 | near-neutral |
| 50 ppm | supra-natural | 41.35% | -6.1 | -1.309 | -1.900 to -0.718 | deterrence by higher-nicotine option |

The important biological feature is not a single pooled sign. Within one study, nicotine changes from positive preference at low natural concentration to approximately neutral at the higher natural-range treatment and negative preference at a supra-natural treatment.

The Baracchi study is **not primary-pool eligible** under the strict focal-trait rule. It demonstrates a flower-chemistry-to-pollinator response, but its focal experiment does not itself establish the required flower-specific antagonist-reduction role for nicotine. It remains a quantitative context study, not a strict `B` effect.

## Manipulated visitation lane: Adler & Irwin 2005

DOI: `10.1890/05-0118`

This study passes the strict role gate more directly. The authors experimentally manipulated gelsemine as a nectar defence and measured both nectar robbers and pollinators in the same `Gelsemium sempervirens` field system. High gelsemine altered robber and pollinator behaviour, so the source itself establishes the defence/interference conflict rather than requiring a defensive label to be imported from another system.

The total-pollinator-visit response can be reconstructed as a log response ratio from source-reported means, SEs, randomization, and reported deaths.

| Year | Dose context | High gelsemine | Low gelsemine | lnRR high/low | Approx. 95% CI | Primary status |
|---|---|---:|---:|---:|---:|---|
| 2002 | supra-natural | 8.9 ± 1.0 visits, n=40 | 11.4 ± 1.1 visits, n=40 | -0.248 | -0.538 to 0.043 | within-study sensitivity |
| 2004 | natural range | 1.71 ± 0.25 visits, n=38 | 2.00 ± 0.31 visits, n=37 | -0.157 | -0.574 to 0.261 | primary visitation effect |

The natural-range 2004 effect is retained as the primary effect for this independence cluster. The 2002 effect is retained but not counted as separate replication. Proportion of flowers probed, residence time, and pollen-analogue transfer remain separate outcome lanes.

## Strict-B observational source: Barlow et al. 2017

DOI: `10.1016/j.cub.2017.07.012`

This is currently the strongest source-level demonstration of the exact biological conflict. In `Aconitum`, nectar alkaloids deter nectar-robbing `Bombus terrestris` at substantially lower concentrations than those tolerated by the legitimate pollinator `Bombus hortorum`, while field pollinator visitation declines with increasing nectar alkaloid concentration. The source explicitly concludes that nectar toxins function as defence against robbery but can impose a cost through fewer pollinator visits.

The field pollinator relationship is observational rather than a high/low manipulation, so it is **not pooled with the Adler manipulation lnRR**. The accepted manuscript reports `n=12`, adjusted `R²=0.27`, and `F=5.8` for the negative total-alkaloid–pollinator-visitation model, and the article identifies public Figshare data (`10.6084/m9.figshare.5165350`). Raw-data recovery remains the preferred route before fixing a standardized association effect.

## Current pooling gates

```text
strict-B manipulation visitation lane:
    source-complete independent clusters:       1  (Adler & Irwin 2005)
    primary pool-eligible independent clusters: 1
    exploratory threshold:                      3
    stability threshold:                        5
    status:                                     NOT POOLABLE

strict-B observational visitation lane:
    source-complete independent clusters:       1  (Barlow et al. 2017)
    primary pool-eligible independent clusters: 0 until raw association effect is fixed
    status:                                     NOT POOLABLE

preference/choice lane:
    numerical independent clusters:             1  (Baracchi et al. 2017)
    strict-B primary pool-eligible clusters:     0
    status:                                     NOT POOLABLE
```

## Why outcome lanes remain separate

Source auditing now gives a direct reason not to create a generic `pollinator response` meta-analysis. Kessler & Baldwin (2007), for example, report that nectar repellents decrease nectaring time and nectar volume removed but can increase visit number. Adler & Irwin (2005) likewise separate total visits, proportion probed, residence time, and pollen-analogue transfer. These constructs are therefore not silently combined.

Separate lanes remain:

- binary preference/choice;
- visitation rate/count;
- residence time or consumption;
- pollen transfer;
- reproductive outcome;
- learning/memory or physiological performance.

## High-priority next recovery queue

1. **Gegear et al. 2007, `Gelsemium sempervirens`** — obtain numerical choice/visitation contrasts while preserving alternative-flower context.
2. **Jones, Warburton & Martin 2023** — recover the listed supporting CSV and extract natural-range ouabain choice effects without figure digitization.
3. **Villalona et al. 2020** — recover species-specific choice effects while retaining bee species as dependent effects within one study.
4. **Barlow et al. 2017 Figshare data** — recover raw field visitation/alkaloid data to fix the exact standardized association rather than infer it from rounded model statistics.
5. **Kessler & Baldwin 2007** — retain as a same-source defence/filter case, but separate visitation frequency from residence/consumption and verify the compound-specific antagonist link before primary pooling.
6. **Jones & Agrawal 2016** — audit the same-system mutualist-bee and antagonist-butterfly responses for compatible direct `B_to_P` and `B_to_H` effects.

Parachnowitsch, Manson & Sletvold (2019; doi:10.1093/aob/mcy132) remains a verified external benchmark. It reports a meta-analysis in which nectar secondary metabolites generally reduced pollinator preference while explicitly noting concentration dependence and positive/neutral low-dose responses. Its study-level effects are useful for source recovery but must be re-audited against the stricter `B`-role, outcome-lane, and independence rules here before reuse.

## Current scientific interpretation

The current source audit now supports three distinct statements without overclaiming:

1. a strict flower-defence-to-pollinator interference conflict is demonstrably real in at least some systems (Adler & Irwin 2005; Barlow et al. 2017);
2. the sign and magnitude of pollinator response are context- and concentration-dependent, and different pollinator-response constructs can move in opposite directions;
3. the repository still lacks enough independent, effect-compatible strict-B studies for a quantitative pooled estimate under its existing thresholds.

These observations are consistent with the fixed conditional theory, but they do not estimate `iota`, `rho`, `kappa`, or the full `W_AD` criterion.

## Manuscript decision

No manuscript text, manuscript figures, journal framing, or submission materials should be updated from this readout. Return to manuscript work only after `ANALYSIS_COMPLETION_GATE.md` is satisfied.
