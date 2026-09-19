# BITA macro candidate figure and analysis receipt v2

Candidate branch:

~~~text
design/bita-floral-defence-selectivity-macro
verified head: d8376ff7ef6bfec4d2f268074c24d67f9be686db
~~~

## 1. Current-head verification

All twelve active branch workflows were green at the verified head:

~~~text
CI                                      SUCCESS   run 35447623295
submission-scope                        SUCCESS   run 35447623314
legacy-ecology-submission-package-guard SUCCESS   run 35447623338
Analyze effective-domain state recovery SUCCESS   run 35447623296
Analyze Sakhalkar network               SUCCESS   run 35447623288
Analyze Sakhalkar multitrait routing    SUCCESS   run 35447623328
Audit Sakhalkar Zenodo                  SUCCESS   run 35447623292
Audit Aubert Dryad                      SUCCESS   run 35447623367
Audit Aubert Zenodo mirror              SUCCESS   run 35447623300
Analyze Aubert Zenodo access barrier    SUCCESS   run 35447623301
Build BITA macro candidate figures      SUCCESS   run 35447623282
Build two-network access-routing figure SUCCESS   run 35447623355
~~~

The legacy submission-package guard passing confirms that the macro candidate has not silently replaced or corrupted the old canonical BITA package.

## 2. Broad D-side route macro corpus

After DOI-level study deduplication:

~~~text
legacy D -> antagonism cluster labels: 18
unique D -> antagonism study programs: 17
same-study D -> pollination follow-up: 10 / 17
~~~

The duplicated study is Takeda 2021 (DOI 10.1093/aob/mcaa168), which entered the historical ledger under two cluster labels.

Implementation breadth:

~~~text
chemical      9
physical      7
reward/access 1

antagonist EFFECTIVE   16
antagonist UNRESOLVED   1
~~~

Pollination-state families among the ten same-study follow-ups:

~~~text
CONTEXT_DEPENDENT  4
NULL_COMPATIBLE    3
IMPROVED           1
INTERFERENCE       1
UNRESOLVED         1
~~~

Pollinator follow-up coverage:

~~~text
chemical  7 / 9
physical  2 / 7
Fisher two-sided p = 0.1262
~~~

This contrast audits study-design coverage and is not an ecological chemical-versus-physical effect test.

## 3. Matched-system effective-domain state recovery

Frozen mapping:

~~~text
SEPARATED    -> NO_INTERFERENCE_OBSERVED
TRANSITIONAL -> MIXED
OVERLAPPED   -> IMPAIRED
~~~

Observed:

~~~text
historical derivation: 9 / 9 aligned
systematic expansion:   2 / 2 aligned
pooled scored:         11 / 11 aligned
~~~

Descriptive fixed-margin alignment probabilities:

~~~text
historical  = 1 / 630  = 0.0015873
pooled      = 1 / 2310 = 0.0004329
~~~

These are not confirmatory p-values because historical systems contributed to theory formation and systematic-expansion coding was not prospectively blinded.

Coarse modality comparator:

~~~text
historical leave-one-out = 6 / 9
systematic expansion      = 1 / 2
~~~

Registered Erica hold-out remains unresolved and unscored.

Latest state-recovery artifact:

~~~text
run:      35447623296
artifact: effective-domain-state-recovery
id:       10586276175
digest:   sha256:4bf79058fc2a12041c4ccd750e1a9c71790d47e90278b7c477d0d253d6ac8348
~~~

## 4. Strict Stage-2 gate

~~~text
                         compatible   impaired
SEPARATED                     2           0
OVERLAPPED                    0           1

Fisher two-sided p = 0.333333
~~~

Null-compatible sensitivity:

~~~text
SEPARATED compatible-or-null = 6
OVERLAPPED impaired          = 1
Fisher two-sided p = 0.142857
~~~

Current decision:

~~~text
DESCRIPTIVE_EXACT_ONLY
domain vs modality = NOT IDENTIFIED in strict n=3
~~~

NO_DETECTED_CHANGE remains distinct from equivalence-supported preservation.

## 5. Defence-side conditionality

Eight independent D-side systems preserve within-system switching across:

- dose / expression;
- cumulative exposure / reward context;
- consumer identity;
- response stage;
- temporal expression.

This layer supports a dynamic selective-window interpretation without pooling heterogeneous outcomes into one universal effect size.

## 6. Network validation A — Sakhalkar 2023

Frozen public-data result:

~~~text
raw workbook rows:               18,440
rows after source-script filter: 14,383
visited plant species:              183
trait-matched plant species:        182
cheating species + tube length:      57

Spearman rho = 0.3467862681
permutation p = 0.0086
~~~

Route-specific medians:

~~~text
robber-only = 2.0892833335
thief-only  = 0.6766
~~~

Source-defined multitrait sensitivity:

~~~text
robber-source predictors:
    tube_length + tube_width + shape
n = 57
full-model R2 = 0.290239
full-model permutation p = 0.2016

tube-length delta R2 = 0.02880
tube-length permutation p = 0.2110
BH q = 0.6330

brightness available = 0 / 57
~~~

Therefore the robust claim is about access geometry and cheating route, not a uniquely identified tube-length effect.

## 7. Network validation B — Aubert / EPHI all-Ecuador extension

This is an independent extension of Aubert et al. 2026, not an exact replication of the published three-transect mixed model.

Public mirror:

~~~text
EPHI Zenodo DOI 10.5281/zenodo.14185547
18 Ecuador sites
~~~

Trait rule:

~~~text
M = log(T / B)

T = flower tube length
B = bird bill / culmen length
TRAIT_BARRIER = T > B
~~~

Analysis grain:

~~~text
bird species × plant species × site
~~~

Coverage:

~~~text
resolved target interactions: 21,114
trait-matched interactions:   20,572
pair-site units:               1,378
sites:                            18

hummingbird pair-sites:        1,377
flowerpiercer pair-sites:          1
~~~

The current extension is therefore effectively a hummingbird result.

Binary barrier result:

~~~text
barrier pair-sites:    888
accessible pair-sites: 490

mean robbery rate:
    barrier     = 0.30698
    accessible  = 0.08139
    difference  = +0.22560

pair-site permutation p = 0.0001
~~~

Continuous mismatch result:

~~~text
Spearman rho[log(T/B), robbery rate] = 0.41826
permutation p = 0.0001
~~~

Within-site recurrence:

~~~text
eligible sites: 17
barrier > accessible robbery: 15 / 17

mean within-site difference:   +0.14399
median within-site difference: +0.13132

two-sided sign-test p = 0.00235
site-stratified permutation p = 0.0001
~~~

Supported interpretation:

> when flower tubes exceed legitimate visitor access morphology, nectar robbing becomes more common.

Boundary:

- observational association, not causal floral defence;
- all-18-site EPHI extension, not exact Aubert three-site replication;
- no flowerpiercer moderator claim from the mirror;
- no common pooled effect scale with Sakhalkar.

Frozen result source:

`empirical/floral_defence_selectivity/results/aubert2026_zenodo_extension.json`

Original generating run recorded in the frozen result:

~~~text
workflow run: 35447201668
artifact digest: sha256:d9f8962c4f934bd5ed3786b61223fce837be3fdcf7084c37f6ad8d5fa559efb1
~~~

Latest exact-reproduction workflow artifact:

~~~text
run:      35447623301
artifact: aubert2026-zenodo-extension
id:       10585521200
digest:   sha256:6f3872aa4db283de140e1b31046ac31aa1036cb93d807ff5ccb0c877e01ef4a3
~~~

Zenodo mirror audit artifact:

~~~text
run:      35447623300
artifact: aubert2026-zenodo-mirror-audit
id:       10586051215
digest:   sha256:1926151e8602de27cf234d01422f7e4e3d0d1b593e47ec9450b7afdafb1a0978
~~~

## 8. Cross-network result

The two public network analyses recover the same routing direction in different faunas and with different response definitions:

~~~text
Sakhalkar — Afrotropical insect visitors
    longer flowers
    -> relatively more robbing than thieving

Aubert / EPHI — Ecuadorian bird–flower interactions
    tube > bill barrier
    -> higher robbery rate

    increasing log(T/B)
    -> higher robbery rate
~~~

This recurrence is stronger evidence for a general access-routing principle than either network alone.

It does not imply:

- a common numerical effect size;
- a shared microscopic mechanism;
- causality from observational network data.

## 9. Physical-defence pollinator-follow-up gap

The broad D-side corpus contains seven physical-defence study programs but only two same-study D-to-pollination follow-ups.

A targeted re-audit admitted no new strict physical-D system.

The highest-value missing experiment remains a physical access/geometry manipulation measuring the same focal D against antagonist use, legitimate pollinator response, bypass behaviour and reproduction.

## 10. Supplementary A-side signal leakage

Legacy paired-A evidence is retained as a supplementary result:

~~~text
same-study paired A systems: 5
scorable states:             4

SHARED_TRACKING:    3
ANTAGONIST_BIASED:  1
UNRESOLVED:         1
~~~

This supports recurrent signal leakage as contextual motivation for selective filtering.

It is not a fifth main evidence layer and is not a prevalence estimate.

## 11. Figure artifacts

Figures 1–3 are reproducibly generated from the candidate theory / matched-system / conditionality sources.

Figure 4 now contains both independent network analyses.

Latest two-network Figure 4 artifact:

~~~text
run:      35447623355
artifact: two-network-access-routing-figure
id:       10586161127
digest:   sha256:48bd3945d9af3c428feae7c78816ceb82ff254cda87e279cb8f1bf3dd603d85a
~~~

Figure 4 explicitly labels the different inferential units and retains the observational / non-equivalence claim boundaries.

## 12. Current empirical architecture

~~~text
Layer 1 — broad route-level D macro corpus
    17 unique D programs
    implementation breadth + pollination-state heterogeneity
    physical pollinator-follow-up gap identified

Layer 2 — matched-D effective-domain state recovery
    11 / 11 scorable historical + expansion systems aligned
    strict direct Stage-2 n = 3 remains descriptive only

Layer 3 — within-D conditionality
    8 independent state-switch systems

Layer 4 — community-scale routing
    Network A: Sakhalkar, 57 plant species
    Network B: Aubert/EPHI, 1,378 bird × plant × site units
    same qualitative access-routing direction across faunas
~~~

Headline ecological result:

> **Access and exposure structure recurrently organizes floral antagonist–mutualist outcomes and exploitation route across route-level, matched-system, within-system and two independent community-scale network analyses.**

## 13. Legacy preservation

The candidate does not delete or overwrite:

- 56 directional route records / 25 historical cluster labels;
- the 17-system high-information identification frontier;
- direct and near-direct A×D results;
- Kessler interaction bounds and partial identification;
- Kessler 2015 consumer-context sign switching;
- identified-set / crossed-intervention / separability logic;
- larceny and other quantitative modules;
- the old canonical mechanism-identification manuscript.

Promotion to canonical status remains an explicit editorial decision.
