# BITA macro candidate figure and analysis receipt v1

Candidate branch:

~~~text
design/bita-floral-defence-selectivity-macro
verified head: e5fe26eb4ccf8424ffd82eb9baf1b74334da6286
~~~

## 1. Current-head verification

All ten active branch workflows were green at the verified head:

~~~text
CI                                      SUCCESS   run 35414655045
submission-scope                        SUCCESS   run 35414655051
legacy-ecology-submission-package-guard SUCCESS   run 35414655046
Analyze effective-domain state recovery SUCCESS   run 35414654983
Analyze Sakhalkar network               SUCCESS   run 35414655043
Analyze Sakhalkar multitrait routing    SUCCESS   run 35414655015
Audit Sakhalkar Zenodo                  SUCCESS   run 35414655038
Audit Aubert Dryad                      SUCCESS   run 35414655114
Build BITA macro candidate figures      SUCCESS   run 35414655018
Build Sakhalkar route-switch figure     SUCCESS   run 35414655153
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

Frozen fixed mapping:

~~~text
SEPARATED    -> NO_INTERFERENCE_OBSERVED
TRANSITIONAL -> MIXED
OVERLAPPED   -> IMPAIRED
~~~

Historical derivation:

~~~text
scorable systems = 9
domain-state recovery = 9 / 9
descriptive fixed-margin perfect-allocation probability = 1 / 630 = 0.0015873
~~~

Systematic expansion:

~~~text
scorable systems = 2
domain-state recovery = 2 / 2
~~~

Pooled historical + systematic expansion:

~~~text
scorable systems = 11
domain-state recovery = 11 / 11
descriptive fixed-margin perfect-allocation probability = 1 / 2310 = 0.0004329
~~~

The historical and pooled exact allocation values are descriptive alignment probabilities, not confirmatory p-values, because historical systems contributed to theory formation and systematic-expansion coding is not prospectively blinded.

Coarse modality comparator:

~~~text
historical leave-one-out = 6 / 9
systematic expansion using derivation rule = 1 / 2
~~~

Registered Erica hold-out remains DIRECTION_ONLY / UNRESOLVED and is not scored.

State-recovery workflow artifact:

~~~text
run:      35414654983
artifact: effective-domain-state-recovery
id:       10574788327
digest:   sha256:2fd0d6a46273c79f04d12caf7a4baefc26442361d6099dc904680b5bf22c1bba
~~~

## 4. Strict Stage-2 gate

Direction-supported strict subset:

~~~text
                         compatible   impaired
SEPARATED                     2           0
OVERLAPPED                    0           1

Fisher two-sided p = 0.333333
~~~

Null-compatible sensitivity:

~~~text
                         compatible-or-null   impaired
SEPARATED                           6              0
OVERLAPPED                          0              1

Fisher two-sided p = 0.142857
~~~

Current decision:

~~~text
DESCRIPTIVE_EXACT_ONLY
domain vs modality = NOT IDENTIFIED in strict n=3
~~~

NO_DETECTED_CHANGE remains distinct from equivalence-supported preservation.

## 5. Defence-side conditionality

Eight independent D-side study clusters preserve within-system state switching across:

- dose / expression;
- cumulative exposure / reward context;
- consumer identity;
- response stage;
- temporal expression.

This layer supports a dynamic selective-window interpretation without pooling heterogeneous outcomes into one effect size or universal threshold ratio.

## 6. Sakhalkar community-scale route association

Frozen public-data result:

~~~text
raw workbook rows:               18,440
rows after source-script filter: 14,383
visited plant species:              183
trait-matched plant species:        182
species with robbery:                26
species with thieving:               39
cheating species + tube length:      57

Spearman rho = 0.3467862681178467
permutation p = 0.0086
permutations = 9,999
seed = 20260919

robber-only median tube length = 2.0892833335
thief-only median tube length  = 0.6766
~~~

The deposited workbook remains eight rows below the 14,391 visits stated in the paper summary; the candidate reports the deposited data as observed.

The public-data reanalysis is verified exactly against the frozen aggregate JSON in CI.

## 7. Sakhalkar source-defined multitrait sensitivity

Predictor sets were frozen from the source paper:

~~~text
robber model: tube_length + tube_width + shape
thief model:  tube_length + brightness + shape
union model:  tube_length + tube_width + brightness + shape
~~~

Coverage among the 57 cheating species:

~~~text
tube_length 57 / 57
tube_width  57 / 57
shape       57 / 57
brightness   0 / 57
~~~

Robber-source sensitivity:

~~~text
n = 57
full-model R2 = 0.290239
full-model permutation p = 0.2016

tube-length delta R2 = 0.02880
tube-length permutation p = 0.2110
BH q = 0.6330
~~~

Therefore the main network result is an association between access geometry and cheating route; tube length is not identified as a unique partial driver after adjustment for correlated morphology.

Multitrait workflow artifact:

~~~text
run:      35414655015
artifact: sakhalkar2023-trait-routing
id:       10575417686
digest:   sha256:d02c0d9ae01b4c62360b132147e32274a3fe7da02ba68b7d2bae885d6a4e3e96
~~~

## 8. Physical-defence pollinator-follow-up gap

The broad D-side corpus contains seven physical-defence study programs but only two same-study D-to-pollination follow-ups.

A targeted re-audit of Takeda 2021, Pedicularis 2015, Chrysothemis 2007, Menyanthes 2018 and Bejaria 2022 admitted no new strict physical-D system.

The high-value missing experiment remains a physical access/geometry manipulation that measures the same focal D against antagonist use, legitimate pollinator response, bypass behaviour and reproduction.

Source:

`empirical/floral_defence_selectivity/PHYSICAL_D_POLLINATOR_GAP_AUDIT_V1.md`

## 9. Figures 1–3 artifact

Workflow:

~~~text
run:      35414655018
artifact: bita-macro-candidate-figures
id:       10574798322
digest:   sha256:a6c0ca0b5734c9e69d8383ea50ac483d81a8fbd92228dc29eb7ab1440fe1c816
~~~

Generated:

~~~text
FIGURE_1_EFFECTIVE_EXPOSURE_THEORY.svg
FIGURE_2_MATCHED_D_STATE_MAP.svg
FIGURE_3_DEFENCE_STATE_SWITCHES.svg
~~~

Figure 2 now displays both:

1. the 17-program broad D-route macro landscape;
2. the stricter matched-system state-recovery / exact-gate evidence.

Visual QA completed.

## 10. Figure 4 artifact

Workflow:

~~~text
run:      35414655153
artifact: sakhalkar2023-route-figure
id:       10575531276
digest:   sha256:18c7866b900329a5ddc12e77b718cecef28eb045a5525d75a9d2bce9711b060c
~~~

Figure 4 uses anonymous species-level points and emits no raw visit rows or species identifiers.

It presents the significant univariate route association together with the explicit multitrait claim boundary.

## 11. Current empirical architecture

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
    57 cheating-exposed species
    rho = 0.347, permutation p = 0.0086
    multitrait sensitivity prevents unique tube-length claim
~~~

Headline ecological result:

> **Access and exposure structure recurrently organizes floral antagonist–mutualist outcomes and exploitation route across route-level, matched-system, within-system and community-scale evidence.**

## 12. Legacy preservation

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
