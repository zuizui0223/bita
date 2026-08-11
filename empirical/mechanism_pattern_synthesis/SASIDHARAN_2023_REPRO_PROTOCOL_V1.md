# Sasidharan et al. 2023 cross-consumer floral-volatile synthesis reproduction protocol v1

## Fixed source

```text
article DOI: 10.1093/aob/mcad064
PMCID: PMC10550281
supplement: mcad064_suppl_Supplementary_Data.xlsx
source synthesis: 32 studies contributing pollinator/florivore FVOC response data
```

The primary article states that Tables S1-S5 are the datasets used for its meta-analyses. This protocol is fixed before the supplementary observation rows are inspected for bita-specific reanalysis.

## Role in bita

This is a **deposited-synthesis reproduction module**, not a new search-based meta-analysis and not an independent primary effect row for every FVOC × insect test.

Its theory-facing target is the attraction-side architecture:

> Do floral volatile signals tend to be tracked only by pollinators, only by florivores, by both consumer roles, or in opposite directions?

This module is biologically distinct from PR #124's antagonist-pressure / nectar-larceny synthesis. If the deposited analysis is independently reproduced and the dependence sensitivity is satisfactory, it is eligible to satisfy the second quantitative-module requirement in Completion Gate C.

## Stage 1 — exact source reproduction

The first stage reproduces the article's published first meta-analysis **on the source's own unit of analysis** before any bita-specific aggregation is attempted.

### Detection table

The article reports unique FVOC × insect-species tests for the eight eligible plant genera:

```text
pollinator tests: 220
pollinator detected responses: 151 (68.6%)
pollinator not detected:        69

florivore tests: 102
florivore detected responses: 83 (81.4%)
florivore not detected:        19

reported chi-square: 5.069
reported P: 0.024
```

The supplement reconstruction must reproduce the exact integer numerator/denominator totals by consumer role and the genus-level counts in published Table 2.

The published `chi-square = 5.069` is exactly the 2 × 2 Pearson chi-square **with Yates continuity correction**, i.e. the default correction used by R's `chisq.test` for a 2 × 2 table. The uncorrected statistic is different and must not be substituted silently.

### Behavioural attractive / repellent / no-response table

The rounded percentages and denominators in published Table 2 imply the exact source-total count table:

```text
                    attractive   repellent   no response   total
pollinator              37           9           66        112
florivore               35           9          115        159
```

These reproduce the published percentages:

```text
pollinator attractive: 33.0%
pollinator repellent:   8.0%

florivore attractive:  22.0%
florivore repellent:     5.7%
```

The source explicitly states that `no response` was included as a category in the attractive/repellent statistical test even though those no-response counts were not printed in Table 2.

The source's reported behavioural comparison (`chi-square = 5.33`, `P = 0.07`) is reproduced by the **2 visitor roles × 3 response categories** Pearson chi-square table above (`df=2`), not by a 2 × 2 attractive-versus-not-attractive comparison.

`no response` therefore remains an explicit category throughout the reproduction and is never silently dropped from the source-unit test.

### Shared-compound table

Published Table 3 is the most direct theory-facing source result.

For each of the eight plant genera, reproduce:

```text
number of behavioural FVOCs tested for the genus
number also tested on both pollinator and florivore roles
number of those shared FVOCs attractive to both roles
number of those shared FVOCs repellent to both roles
```

The article's total checkpoint is:

```text
shared behavioural FVOCs: 32 of 102 = 31.4%
shared attractive:          8 of 32 = 25.0%
shared repellent:           1 of 32 = 3.1%
reported two-sided binomial test attractive vs repellent: P=0.04
```

Among the nine concordant shared-attractive/shared-repellent cases, an exact two-sided binomial test with null probability 0.5 gives `P = 0.0390625`, reproducing the rounded published `P=0.04`.

The primary bita mechanism statement from this source is based on these counts, not on a fabricated continuous effect size.

## Stage 2 — source-unit statistical checks

Recompute only the tests corresponding exactly to published summaries:

1. **Detection:** 2 × 2 Pearson chi-square with Yates continuity correction on visitor role × detected/not-detected. Expected checkpoint: `chi-square = 5.0687`, `P = 0.02436`, rounded by the source to `5.069`, `0.024`.
2. **Behaviour:** 2 × 3 Pearson chi-square without continuity correction on visitor role × `{attractive, repellent, no_response}`. Expected checkpoint from the source-implied integer table: `chi-square = 5.32977`, `df = 2`, `P = 0.06961`, rounded by the source to `5.33`, `0.07`.
3. **Shared concordant behaviour:** exact two-sided binomial test on `8 shared_attractive` versus `1 shared_repellent`. Expected checkpoint: `P = 0.0390625`, rounded to `0.04`.

The reconstructed statistics are integrity checks. The published source analysis remains separately reported so discrepancies cannot be hidden by reimplementation choices.

## Stage 3 — dependence audit

The source unit `unique FVOC × insect-species test` is not equivalent to an independent literature study. Repeated FVOCs, insect species and tests can occur within one publication.

The supplementary workbook must therefore be audited for a stable article/reference identifier. If available, assign every Table-S1 response row to an `independence_cluster` corresponding to the underlying publication.

Report:

```text
number of unique source publications represented
number of response rows per source publication
number of plant genera per source publication
number of consumer roles per source publication
number of FVOCs per source publication
```

No source-test-level P value is interpreted as if there were 220 or 159 independent studies.

## Stage 4 — publication-cluster sensitivity

If a stable source-publication identifier is recoverable, construct a dependence-aware sensitivity without inventing a common biological effect magnitude.

### Detection sensitivity

For each publication × visitor role compute:

```text
detected_fraction = number detected / number tested
```

Retain publication-level paired comparisons only for publications that contain both visitor roles. For unpaired sources, retain the role-specific fraction descriptively.

The primary sensitivity outputs are:

- paired publication count;
- distribution of within-publication `florivore_detected_fraction - pollinator_detected_fraction`;
- median and sign count of paired differences;
- exact sign-test P when the number of non-zero paired publications is sufficient.

No normal approximation is forced for small paired publication counts.

### Behavioural tracking sensitivity

At the publication level, separately summarize the fraction of tests classified:

```text
attractive
repellent
no_response
```

Do not combine attractive and repellent into a signed continuous coefficient because the source tests have heterogeneous assay designs and doses.

## Stage 5 — theory-facing shared-tracking classification

For FVOCs tested on both visitor roles, classify compound-level behaviour within plant-genus context as:

```text
shared_attractive
    attractive to both pollinator and florivore

shared_repellent
    repellent to both

pollinator_attractive_florivore_repellent
    opposite response in the theory-favourable direction

pollinator_repellent_florivore_attractive
    opposite response in the theory-unfavourable direction

role_specific_or_null
    all other combinations, including one role showing no response
```

A compound tested repeatedly within the same publication/consumer context is not counted as multiple independent discoveries merely because multiple assays are present.

The synthesis reports recurrence by plant genus and source publication. Counts across the information-rich source set are **coverage**, not prevalence in nature.

## Gate C pass rule

This Sasidharan module may be called the second quantitative mechanism module only if all of the following are met:

```text
1. article-declared supplementary workbook recovered from an authoritative OA source;
2. Table 2 integer totals reproduced exactly or discrepancy transparently resolved;
3. Table 3 shared-attractive/shared-repellent totals reproduced exactly or discrepancy transparently resolved;
4. source publication/reference identifiers recovered sufficiently to quantify dependence;
5. publication-cluster sensitivity executed where the data support it;
6. all bita outputs retain categorical response structure rather than inventing a cross-assay continuous effect;
7. module kept separate from PR #124 and from primary-study marginal-route ledgers.
```

If criteria 4–5 are impossible because the deposited table lacks stable source identifiers, the module remains a source-reproduction result and does not by itself pass Gate C.

## Prohibited claims

Do not call this module:

- a random sample of flowering plants;
- a prevalence estimate of shared attraction in nature;
- an estimate of `A_to_pollination`, `A_to_antagonism`, `rho`, `iota`, or `W_AD` on a common quantitative scale;
- evidence that every shared-attractive FVOC evolved primarily for pollination;
- 32 or 55 independent studies unless the supplement's source-identifier audit actually supports that count for the relevant analysis.

The valid target claim is narrower: a source-audited deposited synthesis can test whether shared, role-specific, and opposing floral-signal responses recur across multiple plant–insect systems, while explicitly preserving study dependence.