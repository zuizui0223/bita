# B-to-pollinator constituent-path analysis readout v1

## Status

**Not ready for manuscript use. The manuscript remains frozen.**

This readout records the first source-reconstructed quantitative effect set for the `B_to_pollination` constituent pathway and the current independent-study gate. It is an analysis checkpoint, not a manuscript result section.

## What was already supported before this extraction

The current `main` directional registry contains a restricted manipulation stratum for flower chemical barriers and pollinator preference/foraging with three independent directional clusters, all coded in the negative direction. A separate visitation-rate manipulation stratum contains only one mixed cluster. The canonical quantitative effect table on `main` is empty, so these records are directional context rather than a quantitative meta-analysis.

Historical analysis branches also contain a source-verified observational `Impatiens capensis` floral-tannin to pollinator-visitation coefficient, but it is one observational panel and is not combined with experimental preference effects.

## First source-reconstructed numerical study

### Baracchi et al. 2017, nicotine preference assay

DOI: `10.1038/s41598-017-01980-1`

The source reports a controlled bumblebee preference experiment with 20 bees per nicotine concentration and 100 consecutive choices per bee. The experimental unit is the bee, not the individual choice. The three dose groups belong to **one independent study cluster**.

The source directly reports one-sample t statistics against the neutral 50% choice benchmark (`t=5.3`, `0.96`, and `-6.1`, each with `df=19`). The preliminary standardized effects below are reconstructed from those reported t statistics rather than from rounded mean±SEM values. They remain preliminary until a common cross-study preference metric and dependence model are finalized.

| Nicotine dose | Source context | Mean preference | Reported t | Preliminary Hedges g vs 50% | Approx. 95% CI | Direction |
|---|---|---:|---:|---:|---:|---|
| 1 ppm | low natural range | 55.65% | 5.3 | +1.138 | 0.583 to 1.693 | preference for higher-nicotine option |
| 2.5 ppm | high natural range | 51.05% | 0.96 | +0.206 | -0.220 to 0.632 | near-neutral |
| 50 ppm | supra-natural | 41.35% | -6.1 | -1.309 | -1.901 to -0.718 | deterrence by higher-nicotine option |

The important biological feature is not a single pooled sign. Within one study, nicotine changes from positive preference at low natural concentration to approximately neutral at the higher natural-range treatment and negative preference at a supra-natural treatment. Dose context therefore must be preserved in the constituent-path synthesis.

The Baracchi study is **not yet marked primary-pool eligible**. It demonstrates a flower-chemistry-to-pollinator response, but the fixed `B` role still requires a source-audited antagonist-reduction/defence role rather than classification from the label "secondary metabolite" alone. That gate remains explicit in the study ledger and protocol.

## Pooling gate after v1 extraction

```text
preference-choice effect rows reconstructed:     3
source-complete independent study clusters:       1
primary-pool eligible independent clusters:       0
exploratory pooling threshold:                    3
stability threshold:                              5
current status:                                   NOT POOLABLE
```

The three Baracchi dose rows are not three replications. They count as one study cluster.

## Why outcome lanes remain separate

Prior source screening contains examples where visit number, residence time, nectar removal, and preference do not move together. Therefore the analysis will not combine:

- binary preference/choice;
- visitation rate;
- residence time or consumption;
- pollen transfer;
- reproductive outcome;
- learning/memory or physiological performance.

A single broad `pollinator response` effect would erase biologically important sign differences.

## High-priority independent-study recovery queue

The next source-level targets are prioritized because they can add independent clusters without relaxing the fixed B-role definition:

1. **Gegear et al. 2007, `Gelsemium sempervirens`** — direct defensive nectar-alkaloid deterrence; alternative-flower context must remain explicit.
2. **Jones, Warburton & Martin 2023** — milkweed-relevant ouabain/cardenolide choice experiments; publicly listed supporting CSV should be used rather than figure digitization if recoverable.
3. **Villalona et al. 2020** — milkweed/cardenolide bee responses; preference and consumption must be separated and pollinator species retained as dependent effects within one study.
4. **Manson et al. 2012 / Manson et al. 2013** — nectar alkaloid assays; preserve natural versus strongly elevated dose contexts and do not substitute time-per-flower for preference/visitation.
5. **Adler & Irwin 2005** — field manipulation of defensive nectar chemistry; visitation, residence, and pollen-analogue outcomes must remain separate.
6. **Jones & Agrawal 2016** — high-priority joint-route study because mutualist bees and antagonistic butterflies are both measured; audit whether compatible direct B-to-P and B-to-H effects can be recovered from the same independent panel.

Parachnowitsch, Manson & Sletvold (2019; doi:10.1093/aob/mcy132) is a verified external benchmark: it reports a meta-analysis in which nectar secondary metabolites generally reduced pollinator preference while explicitly noting concentration dependence and positive/neutral low-dose responses, and it provides individual effect-size data in its supplementary material. Those effects must still be re-audited against the stricter `B`-role, outcome-lane, and independence rules here before reuse.

## Current scientific interpretation

The current evidence does **not** support the statement that floral defence chemistry universally reduces pollinator use.

What is supported at this stage is narrower:

- a flower-chemistry-to-pollinator pathway exists in the source literature;
- the repository's directional records are often consistent with deterrence;
- the first reconstructed quantitative study shows strong dose dependence, including positive, near-neutral, and negative responses within the same compound;
- a quantitative cross-study synthesis is not yet identified because the independent-study and `B`-role gates have not been met.

This pattern is compatible with the fixed conditional theory, but it does not estimate the theory's mixed-partial interference term `iota` and does not validate the full attraction-defence sign criterion.

## Manuscript decision

No manuscript text, manuscript figures, journal framing, or submission materials should be updated from this readout. Return to manuscript work only after `ANALYSIS_COMPLETION_GATE.md` is satisfied.
