# Supplementary material — identification-design manuscript

This supplement supports `MANUSCRIPT_IDENTIFICATION_DESIGN.md`. It preserves technical analyses from the earlier theorem-led manuscript without treating them as headline biological results.

## S1. Continuous formulation as a limiting case of the discrete estimand

The Main manuscript uses the two-level interaction

\[
\Delta_{AD}W=W_{11}-W_{10}-W_{01}+W_{00}
\]

because it corresponds directly to a factorial experiment. For sufficiently small trait contrasts around a smooth reference state, the scaled discrete contrast approaches the mixed partial \(\partial^2W/(\partial A\partial D)\). The original continuous decomposition

\[
W_{AD}=M_{AD}-G_{AD}-C_{AD}
\]

therefore remains a useful local limit, but it is not the primary estimand for the experimental design.

The existing derivative-agreement analysis evaluates the analytic mixed partial against a finite-difference implementation across 2,592 declared sensitivity evaluations and four response-shape variants. This is retained as a software and model-family sensitivity check. It is not empirical validation, a prevalence estimate, or evidence that the chosen finite grid represents the distribution of ecological systems in nature. The previously reported 77.2% selectivity-window precision is likewise a property of that finite design and is not used as a Main-text biological result.

Relevant existing sources:

```text
manuscript/supplementary/figures/FIGURE_S1_DERIVATIVE_AGREEMENT.svg
manuscript/supplementary/figures/FIGURE_S2_SCENARIO_SIGN_MAPS.svg
configs/part_i_robustness_grid.json
trait_architecture/robustness.py
```

## S2. Kessler et al. 2008 aggregate reconstruction

Kessler, Gase & Baldwin (2008; DOI `10.1126/science.1160072`) independently blocked benzylacetone and nicotine production in all four combinations in *Nicotiana attenuata*. The published female-outcrossing summary places the BA+/nicotine+ state at about 35% capsule maturation and each state lacking BA, nicotine, or both around 12–14%.

For a two-by-two probability surface, the discrete interaction is

\[
\Delta_{AD}p=p_{11}-p_{10}-p_{01}+p_{00}.
\]

Across the published rounded ranges, the project audit gives

```text
probability-scale Delta_AD: +0.19 to +0.25
logit interaction beta_AD:  +1.019 to +1.551
interaction odds ratio:     2.77 to 4.71
```

The interaction sign is positive throughout these aggregate constraints. The accessible article reports 601 antherectomized flowers across five experimental days, including 127 flowers on one windy day with no active pollinators and no capsules; 474 flowers on the remaining days produced 87 mature capsules before subsequent losses. Exact genotype-by-day values are referred to supplementary Fig. S8A.

A broad integer-allocation stress test preserved the positive interaction sign but did not make formal significance allocation-robust. Exact source uncertainty therefore remains unresolved. The transformed nicotine-suppression state is also systemic rather than flower-restricted. These limitations are retained explicitly.

Primary audit files:

```text
empirical/mechanism_pattern_synthesis/KESSLER_2008_DIRECT_AXD_CANDIDATE_AUDIT_V1.md
empirical/mechanism_pattern_synthesis/KESSLER_2008_FACTORIAL_SIGN_ROBUSTNESS_V1.md
empirical/identification_design/KESSLER_2008_IDENTIFICATION_REAUDIT_V2.md
```

## S3. Impatiens public-data identification retrofit

### S3.1 Source and variables

Soper Gorden & Adler (2018; DOI `10.1002/ajb2.1182`; Dryad DOI `10.5061/dryad.0j96d17`) provides an individual-plant panel with pre-treatment early-season flower redness (`A` candidate), early-season floral condensed tannins (`D` candidate), randomized supplemental robbing/florivory/pollination assignments, phenology, and reproductive components.

The trait roles remain observational. Randomized treatments simulated increased interaction intensity rather than selectively toggling consumers present versus absent. The reanalysis therefore tests randomized context modification of an observational `A×D` association; it does not identify `rho_delta`, `iota_delta`, `m0_delta`, or `kappa_delta`.

### S3.2 Registered hierarchical model

For each reproductive component, the model included:

```text
standardized A
standardized D
A×D
full randomized Robbing×Florivory×Pollination factorial
all A- and D-by-treatment lower-order terms required for hierarchy
A×D×Robbing
A×D×Florivory
A×D×Pollination
standardized pre-treatment flowering date
```

Randomized treatment factors were effect-coded `N=-0.5`, `Y=+0.5`. HC3 robust intervals were calculated. No individual Dryad rows are committed to the project repository.

### S3.3 Results

For chasmogamous fruits per plant per day (`n=170`, residual df 149; randomized-cell `n=19–24`):

| term | estimate | HC3 95% CI |
|---|---:|---:|
| `A×D` | -0.1628 | [-0.3675, +0.0419] |
| `A×D×Robbing` | -0.0434 | [-0.4194, +0.3325] |
| `A×D×Florivory` | -0.3078 | [-0.6879, +0.0723] |
| `A×D×Pollination` | +0.0748 | [-0.3750, +0.5246] |

For seeds per chasmogamous fruit (`n=85`, residual df 64; randomized-cell `n=6–14`):

| term | estimate | HC3 95% CI |
|---|---:|---:|
| `A×D` | -0.0936 | [-0.6643, +0.4771] |
| `A×D×Robbing` | -0.2539 | [-1.6896, +1.1818] |
| `A×D×Florivory` | -0.3551 | [-1.6492, +0.9390] |
| `A×D×Pollination` | -0.1696 | [-0.9840, +0.6448] |

All eight intervals include zero. The result supports neither one stable interaction sign nor a resolved agent-specific modifier. Its methodological value is the explicit boundary between a total interaction/context-modification analysis and channel identification.

Machine-readable aggregate results:

```text
empirical/identification_design/IMPATIENS_2018_IDENTIFICATION_RETROFIT_V1.json
empirical/identification_design/IMPATIENS_2018_IDENTIFICATION_RETROFIT_V1.md
```

## S4. Identification-coverage audit

### S4.1 Coding dimensions

The current high-information matrix records, for each candidate system:

```text
A status
D status and organ/function validity
A×D trait-factorial status
total A×D status
antagonist intervention status
pollinator intervention status
m0_delta status
independent joint-cost assay status
highest recoverable identification layer
primary blocker
```

The matrix is a deliberately high-information design audit rather than a systematic prevalence sample.

### S4.2 Current coverage state

The current matrix contains 16 systems. Fixed conclusions are:

```text
closest full A×D-like trait factorial:      Kessler et al. 2008
closest crossed G×P-like consumer factorial: Egan et al. 2021
independent kappa assay:                    0
full rho/iota/kappa identification:         0
```

The main empirical pattern is not absence of sophisticated experiments, but separation of the required components across different studies.

Authoritative table:

```text
empirical/identification_design/HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V1.csv
```

### S4.3 Distinct near-miss classes

Representative failures include:

1. **Trait factorial without consumer factorial** — Kessler et al. 2008.
2. **Consumer factorial without manipulated floral A×D** — Egan et al. 2021.
3. **Observed A×D plus randomized interaction intensity, not exclusion** — Soper Gorden & Adler 2018.
4. **2×2 floral phenotype but second axis is reward rather than D** — Kessler et al. 2015.
5. **Selective flower-associated D but no A manipulation** — Sun & Huang 2015.
6. **Whole-plant defence rather than flower-specific D** — Santangelo et al. 2019 and Strauss et al. 1999.
7. **A and D jointly measured but no A×D term** — Irwin & Adler 2006 and García et al. 2024.
8. **One dual-function chemical trait rather than two axes** — Gronquist et al. 2001.

These classes motivate the experimental roadmap in Main Fig. 5.

## S5. Broader mechanism-route evidence retained as background

The earlier mechanism-pattern synthesis contains 56 source-adjudicated route records from 25 independent biological study clusters, including 14 same-system multi-route clusters and 17 context/sign-switch clusters. These records remain useful for demonstrating that attraction, pollination, antagonism and defence pathways recur in nature.

They are not used in the identification manuscript as estimates of `rho_delta`, `iota_delta`, `Delta_AD W`, or `kappa_delta`. Marginal `A→pollination`, `A→antagonism`, `D→antagonism`, and `D→pollination` evidence does not estimate a cross-trait channel interaction. The full route ledger therefore moves from the old Main argument to supplementary/background evidence.

Authoritative sources remain:

```text
empirical/mechanism_pattern_synthesis/
manuscript/supplementary/tables/TABLE_S3_MECHANISM_PATTERN_LEDGER.csv
manuscript/supplementary/tables/TABLE_S4_CONDITIONALITY_AND_CONTEXT.csv
```

## S6. Quantitative modules not used as identification evidence

The Leal et al. (2025) floral-larceny reanalysis and Sasidharan et al. (2023) floral-volatile physiological-detection reconstruction remain preserved and reproducible in the repository. They quantify important ecological consequences and heterogeneity, but neither estimates the channel-resolved attraction-by-defence interaction introduced in the new Main manuscript.

They are therefore not pooled into the identification argument. Their future disposition is separate: they may remain supplementary context, support a companion synthesis, or be developed independently. This editorial move does not alter any previously reproduced estimate.

## S7. Reproducibility boundary

The candidate manuscript is backed by:

```text
trait_architecture/identification.py
tests/test_identification.py
tests/test_identification_four_way.py
tests/test_identification_coverage.py
scripts/reanalyze_impatiens_identification_retrofit.py
scripts/build_identification_design_figures_svg.py
empirical/identification_design/
```

The current code deliberately distinguishes deterministic software checks from empirical uncertainty. In empirical applications, the four-way separability condition should be evaluated with uncertainty-aware equivalence or contrast procedures rather than the hard floating-point tolerance used in regression tests.
