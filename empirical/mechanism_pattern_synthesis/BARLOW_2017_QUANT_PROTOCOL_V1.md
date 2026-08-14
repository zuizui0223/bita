# Barlow et al. 2017 Aconitum threshold-window quantitative protocol v1

## Fixed sources

```text
article DOI: 10.1016/j.cub.2017.07.012
public data DOI: 10.6084/m9.figshare.5165350
workbook: BarlowetalCurrent Biology.xlsx
plant species: Aconitum lycoctonum, A. napellus
pollinator: Bombus hortorum
nectar robber/bioassay consumer: Bombus terrestris
D axis: total or constituent Aconitum nectar alkaloid concentration
```

The article and workbook schema were audited before outcome values were read. The primary article states that linear models for pollinator visits versus nectar alkaloids used log-transformed data, and that robber responses were analysed separately with GLMs across experimental alkaloid concentrations.

## Scientific target

This study is not used to estimate a universal `D_to_pollination` or `D_to_antagonism` coefficient. Its main role is to test a more specific theory-relevant pattern:

> Is there a concentration range in which a flower-specific chemical defence already deters nectar robbers while legitimate pollinator use remains comparatively tolerant?

The source reports robber deterrence at concentrations as low as 20 ppm, whereas pollinator visitation declines sharply above roughly 200 ppm and is extrapolated to cease near 380 ppm. The deposited data allow the field pollinator slope and laboratory robber dose response to be kept as separate quantitative lanes.

## Lane 1 — field `D_to_pollination`

### Primary species

Use only `A. lycoctonum` for the primary field regression because the article identifies adequate power and a significant total-alkaloid relationship for this species (`n=12`). `A. napellus` (`n=8`) is a prespecified secondary low-power replication and is never pooled as an independent study.

Fixed worksheet and columns:

```text
sheet: bee visits nec alks
A. lycoctonum response: l_B.hort_nec
A. lycoctonum predictor: l_nec_alk TOTAL
A. napellus response: n_B.hort_nec
A. napellus predictor: n_nec_alk TOTAL
```

For each species:

1. retain rows with finite positive visitation rate and finite positive total nectar alkaloid concentration;
2. stop with an explicit scale mismatch if any otherwise eligible row contains zero or negative values rather than silently switching transformation;
3. fit the source-aligned simple linear model

```text
ln(B. hortorum visitation rate) ~ ln(total nectar alkaloids ppm)
```

4. report slope, ordinary OLS SE, 95% CI, R², adjusted R², F statistic, and n;
5. report the standardized slope/Pearson correlation for the same two transformed variables;
6. compare the reconstructed `A. lycoctonum` F statistic with the source-reported `F=5.8`, adjusted R²≈0.27, and `P<0.05` as an integrity check.

Effect orientation:

```text
negative = higher D is pollinator-interference compatible
positive = higher D is pollinator-facilitation compatible
```

For synthesis portability, also record Fisher's `z` of the transformed-variable Pearson correlation with sampling SE `1/sqrt(n-3)`. This is a scale-specific field association, not a causal chemical manipulation.

### Source-only reconstruction checkpoint

Before raw-data fitting, the published simple-regression statistic itself implies, for `A. lycoctonum`:

```text
n = 12
F = 5.8 with 1 and 10 df
r = -sqrt(F / (F + 10)) ≈ -0.606
Fisher z ≈ -0.702
SE(z) = 1/sqrt(9) = 0.333
```

The negative sign is fixed by the source-reported regression direction. This checkpoint must agree closely with the raw-data reanalysis or the row mapping is rejected.

## Lane 2 — laboratory `D_to_antagonism`

### Dose-response source

Use the deposited `Figure S2` sheet for total alkaloid mixtures:

```text
species code: 1=A. lycoctonum, 2=A. napellus
concentration code:
  1=sucrose control
  2=0.2 ppm
  3=2 ppm
  4=20 ppm
  5=200 ppm
  6=2000 ppm
primary response: volume (ul)
secondary behavioural responses: durationprob, numbercontacts, firstboutdur, no_bouts, cum_bouts
```

The primary robber outcome is consumption volume. Behavioural outcomes remain secondary and are not combined with consumption into one response.

### Primary dose summary

For each species × concentration cell, report:

- n;
- mean volume consumed;
- SD and SE;
- median and interquartile range as descriptive robustness summaries.

The sucrose control and each alkaloid concentration remain separate. Do not collapse 0.2–2000 ppm into one exposed category.

### Source-aligned threshold criterion

The main threshold result is source-concordance, not data-driven breakpoint search.

Prespecified checkpoints:

```text
0.2 ppm: below reported deterrence threshold
2 ppm: below reported deterrence threshold
20 ppm: first source-reported deterrent concentration
200 ppm: within the field pollinator decline region
2000 ppm: supra-field high dose
```

For each alkaloid dose versus sucrose, calculate a standardized mean difference in consumption volume using Hedges' g and its sampling variance when cell independence and sample-size structure are valid. If the workbook reveals repeated measures or shared-control dependence that prevents the usual independent-g formula, retain cell summaries and flag the contrast as dependent rather than forcing an effect size.

A concentration-response GLM may additionally reproduce the source test, but it is subordinate to the dose-specific effect table because the integrated theory needs the location of the mutualist/antagonist tolerance window rather than one global concentration coefficient.

## Threshold-window synthesis within this study

The two lanes are not pooled because one is field visitation and one is laboratory consumption. They are combined only at the **mechanism-pattern** level:

```text
robber deterrence begins near 20 ppm
pollinator field interference becomes pronounced above ~200 ppm
```

If raw-data reconstruction supports both source landmarks, register this as a source-verified `differential_consumer_tolerance_window` sign-switch/threshold pattern. It is compatible with a concentration range where antagonist relief can arise before strong pollinator interference.

This is not an estimate of `rho - iota`, because the endpoints, contexts, and scales differ.

## Independence and guardrails

- All Aconitum rows from this article form one study cluster.
- The two plant species are not independent studies.
- Pollinator field and robber laboratory effects are not combined into a common effect metric.
- No threshold is optimized from the observed data; the 20 ppm and ~200–380 ppm landmarks come from the primary article.
- No direct `A x D`, `W_AD`, `rho`, `iota`, or `kappa` is identified.
- Raw workbook rows remain in memory; committed outputs contain only aggregate coefficients and diagnostics.