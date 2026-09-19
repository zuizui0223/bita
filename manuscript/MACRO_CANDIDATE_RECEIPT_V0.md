# BITA macro candidate figure and analysis receipt v1

Candidate branch:

~~~text
design/bita-floral-defence-selectivity-macro
verified head: 5d078096ddc89d8a038714d9976598e0eddb79f9
~~~

## 1. Current-head verification

All ten active branch workflows were green at the verified head:

~~~text
CI                                      SUCCESS   run 35414996104
submission-scope                        SUCCESS   run 35414996113
legacy-ecology-submission-package-guard SUCCESS   run 35414996083
Analyze effective-domain state recovery SUCCESS   run 35414996115
Analyze Sakhalkar network               SUCCESS   run 35414996110
Analyze Sakhalkar multitrait routing    SUCCESS   run 35414996106
Audit Sakhalkar Zenodo                  SUCCESS   run 35414996094
Audit Aubert Dryad                      SUCCESS   run 35414996102
Build BITA macro candidate figures      SUCCESS   run 35414996240
Build Sakhalkar route-switch figure     SUCCESS   run 35414996120
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
run:      35414996115
artifact: effective-domain-state-recovery
id:       10574983706
digest:   sha256:5274804ade9ea139ee870f70a566f392795167a73497af2b334aede5a879df71
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
run:      35414996106
artifact: sakhalkar2023-trait-routing
id:       10575018663
digest:   sha256:38ea1263d9b44c5194845dc62bba01f33bbe5b4ef991e82e3dd7affffda530be
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
run:      35414996240
artifact: bita-macro-candidate-figures
id:       10575751485
digest:   sha256:309d7fb1e2f08ad34db35cf00fbcf04f5b8c3471c65d09a8ef0989117b04df77
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
run:      35414996120
artifact: sakhalkar2023-route-figure
id:       10575203433
digest:   sha256:35f24e9d1e753582b708239fcfc9892bcfacedf108d5ab175907aaa7b4d6218a
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


## 13. Supplementary A-side signal leakage

Legacy attraction-side route evidence is retained as a supplementary macro result:

~~~text
A -> pollination unique studies: 5
A -> antagonism unique studies:  8
same-study paired A systems:     5

scorable paired states:
    SHARED_TRACKING    3
    ANTAGONIST_BIASED  1
    UNRESOLVED         1
~~~

Among the four scorable historical paired systems, none shows a resolved mutualist-exclusive attraction state.

This is used only as mechanistic context:

> attraction/display signals can leak to antagonists, creating ecological demand for selective filtering.

It is not counted as a fifth main macro layer and is not treated as a prevalence estimate.

Sources:

- `empirical/floral_defence_selectivity/a_side_signal_leakage_registry.csv`
- `empirical/floral_defence_selectivity/A_SIDE_SIGNAL_LEAKAGE_READOUT_V1.md`
- `tests/test_a_side_signal_leakage.py`
