# Reproduction and strict-B re-audit of the 2019 nectar meta-analysis

## Status

**The published broad meta-analysis is reproduced. The strict bita pathway meta-analysis is not yet complete, and the manuscript remains frozen.**

This checkpoint uses the recovered study-level supplement for Parachnowitsch, Manson and Sletvold (2019; doi: `10.1093/aob/mcy132`). It adds no new biological mechanism and does not change the fixed attraction--defence theory. Its purpose is to distinguish a reproducible broad literature result from the narrower evidence that bita can legitimately use.

## 1. Exact reproduction of the published secondary-metabolite result

The published figure reports 63 secondary-metabolite effect sizes from nine studies. The recovered worksheet contains 72 rows labelled `secondary metabolites`; the nine extra rows all belong to Good et al. (2014), so label membership alone is not the published inclusion rule. Excluding those nine rows recovers the declared 63 effects and nine papers.

For each worksheet row, Hedges' g was calculated as the first worksheet mean minus the second worksheet mean. Dependent rows were first combined by inverse-variance fixed pooling within paper. The nine paper-level estimates were then combined with a DerSimonian--Laird random-effects model.

```text
published effect rows                         63
published independent papers                   9
random-effects pooled Hedges g            -0.4444
standard error                             0.1132
95% CI                              -0.6662 to -0.2226
tau-squared (DL)                           0.0889
Q                                           56.74
I-squared                                  85.90%
```

The recovered data therefore reproduce the published conclusion that nectar secondary metabolites are associated, on average, with a lower pollinator preference/use response. The high heterogeneity is equally important: the broad average is not a universal negative response.

## 2. Why the reproduced result is not yet bita's strict pathway estimate

The recovered workbook is organized for the published review question, not for bita's narrower inference contract. Its paper-level summaries can combine:

- different dose levels from the same experiment;
- visit number, visit length, and volume consumed;
- legitimate pollinators and other consumers;
- field and laboratory assays;
- trait labels whose flower-specific antagonist-reduction role is not established in the worksheet.

The worksheet headers are also not a safe biological treatment orientation. In Adler and Irwin (2005), primary-source comparison shows that the values under `Mean Control` are the high-gelsemine groups, whereas the repeated values under `Mean Treatment` are the lower-gelsemine references. The broad reproduction can use the worksheet order because it reproduces the published forest plot, but a bita effect must be re-oriented from the primary study.

## 3. Study-level re-audit result

The nine paper-level summaries now have an explicit re-audit state in `PARACHNOWITSCH2019_STUDY_REAUDIT_V1.csv`. The current consequences are:

- **Adler and Irwin (2005):** same-study strict defence evidence, but the published summary pools a supra-natural year with a natural-range year. The existing year-specific lnRRs remain the canonical route.
- **Johnson et al. (2006):** a verified floral visitor filter and an important counterexample to a universal pollinator cost; effective pollinators and mismatched visitors must not be collapsed.
- **Jones and Agrawal (2016):** same-study defence evidence, but the published summary combines a bee-pollinator row with a butterfly-antagonist row. The two theory pathways must be separated.
- **Manson et al. (2013):** a strong dose-dependence case, but the published summary averages dose levels and combines visit number with visit length. Near-natural and highly elevated concentrations give biologically different conclusions.
- **The remaining five papers:** require primary-source role, outcome, orientation, or dependence audits before strict-B use.

Thus the 2019 meta-analysis is a high-value source map and a reproducible broad empirical benchmark. It is not a ready-made strict flower-defence meta-analysis.

## 4. Current inference

The empirical literature already supports a narrower statement than the broad published average:

> Flower-associated defensive chemistry can impose a pollinator-use cost in some systems, but that cost is not a fixed consequence of the trait label. It depends on dose, consumer role, assay, and response construct.

This supports the biological plausibility of the existing conditional theory. It does **not** estimate `rho`, `iota`, `kappa`, or `W_AD`, and it does not resolve whether attraction and defence are complementary in any population.

## 5. Next extraction target

The next primary task remains effect recovery, not further analysis infrastructure. The highest-yield route is to obtain outcome-specific preference/choice effects for the independent milkweed and *Gelsemium* studies already identified in the repository:

1. Gegear et al. (2007);
2. Villalona et al. (2020);
3. Jones, Warburton and Martin (2023).

Those three studies can potentially establish the first exploratory, outcome-compatible preference/choice synthesis without mixing visit counts, consumption, pollen transfer, or reproduction. Any moderator analysis remains secondary to establishing the main effect and study independence.

## Manuscript decision

No manuscript text, figures, journal framing, or submission materials are changed. Manuscript work remains frozen under `ANALYSIS_COMPLETION_GATE.md`.
