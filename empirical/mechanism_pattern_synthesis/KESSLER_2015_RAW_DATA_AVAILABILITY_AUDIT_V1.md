# Kessler 2015 raw-data availability audit v1

## Purpose

Determine whether Kessler et al. 2015 (`10.7554/eLife.07641`) can be reanalysed to obtain a formal uncertainty-bearing `A x D` interaction rather than only arithmetic contrasts of published factorial cell means.

## Public source routes checked

The targeted audit checked the following public routes:

1. eLife Version of Record full text and Figures/Data page;
2. eLife accepted-manuscript / figures page and the article-level additional-files index;
3. PMC full-text mirror;
4. eLife peer-review / author-response record;
5. MPG.PuRe article record and its persistent dataset/version handles;
6. Bio-protocol / Bio-protocol Exchange records linked to the article;
7. targeted web searches for Dryad, institutional, and general repository copies of the article title/DOI plus `data`, `dataset`, `source data`, and `raw data` terms.

## What is publicly recoverable

The article reports the experimental design, sample sizes at the experiment level, normalized cell means, omnibus Friedman tests, and pairwise comparisons.

Key pollination results include:

```text
native visitor community:
  CHAL        22.9% of EV
  SWEET9       9.7% of EV
  CHALxSWEET9 11.6% of EV
  Friedman chi2 = 10.22, df = 3, n = 16-20, p = 0.017

Manduca sexta:
  CHAL        17.4% of EV
  SWEET9      44.6% of EV
  CHALxSWEET9  5.2% of EV
  Friedman chi2 = 29.90, df = 3, n = 30, p < 0.001

Hyles lineata:
  CHAL        96.6% of EV
  SWEET9     111.69% of EV
  CHALxSWEET9 21.3% of EV
  Friedman chi2 = 12.35, df = 3, n = 35, p = 0.006
```

The article also states that experiments were conducted over several days, day did not significantly influence line effects, each plant was used as a replicate for pollination assays, and the average seed number from five flowers per plant was used for analysis.

## What was not recovered

No public route above yielded the replicate-level plant-by-genotype seed table or an equivalent numeric source-data spreadsheet for Figure 2. The eLife article-level additional-files page advertises a supplementary ZIP, but the indexed figure record lists figure supplements rather than a numerical `Figure 2—source data` table of the type routinely exposed in more recent eLife articles. MPG.PuRe exposes the publisher PDF and persistent record handles, not a separate replicate-level dataset in the indexed record. Bio-protocol exposes methods, not the pollination-response table. Targeted repository searches did not recover a separate raw dataset.

## Consequence for direct-factorial inference

With `A = BA scent presence` and `D = floral nectar restriction`, the exact arithmetic contrast of the published normalized means is identifiable:

```text
Delta_AD = W(A+,D+) - W(A+,D-) - W(A-,D+) + W(A-,D-)

native community  =  0.097 - 1.000 - 0.116 + 0.229 = -0.7900
Manduca sexta     =  0.446 - 1.000 - 0.052 + 0.174 = -0.4320
Hyles lineata     =  1.1169 - 1.000 - 0.213 + 0.966 = +0.8699
```

Thus the **factorial sign reversal is source-mean identified**.

However, the replicate-level covariance / dispersion needed for a formal `A x D` interaction SE, CI, permutation distribution, or blocked factorial reanalysis is not recoverable from the public summary statistics alone. The Friedman omnibus and post-hoc p-values cannot be inverted uniquely into an interaction uncertainty.

## Registered inference state

```text
crossed floral factorial:          yes
A manipulation:                    BA scent
D manipulation:                    nectar restriction / reward access
antagonist-reduction role for D:   supported by lower M. sexta oviposition when nectar is absent
shared reproductive outcome:       yes
source-mean interaction sign:      identified and context-reversing
formal interaction SE/CI:          not identified from recovered public data
raw-data search:                   targeted routes exhausted
```

## Manuscript wording boundary

Admissible:

> Source-reported factorial cell means imply a negative discrete A-by-D contrast for the native visitor community and Manduca sexta but a positive contrast for Hyles lineata, demonstrating context-dependent sign reversal in the crossed floral-trait means.

Not admissible:

> The A-by-D interaction was statistically significant.

unless replicate-level data or a source-reported interaction test is later recovered.
