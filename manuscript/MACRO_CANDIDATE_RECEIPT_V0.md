# BITA macro candidate figure and analysis receipt v0

Candidate branch:

```text
design/bita-floral-defence-selectivity-macro
verified head: d488e3cf31ab4823bc1d79efd120a523c45f801c
```

## 1. Current-head verification

All branch workflows were green at the verified head:

```text
CI                                      SUCCESS   run 35394357483
submission-scope                        SUCCESS   run 35394357354
legacy-ecology-submission-package-guard SUCCESS   run 35394357508
Analyze Sakhalkar 2023 network          SUCCESS   run 35394357398
Audit Sakhalkar 2023 Zenodo             SUCCESS   run 35394357410
Audit Aubert 2026 Dryad                 SUCCESS   run 35394357493
Build BITA macro candidate figures      SUCCESS   run 35394357512
Build Sakhalkar route-switch figure     SUCCESS   run 35394357359
```

The legacy submission-package guard passing confirms that the macro candidate has not silently replaced or corrupted the old canonical BITA package.

## 2. Figures 1–3 artifact

Workflow:

```text
run:      35394357512
artifact: bita-macro-candidate-figures
id:       10566473399
digest:   sha256:5757faa7ccecaa6433822aedbb76045dfecff1b79e7a73eb3d76b033db42fa44
```

Generated files:

```text
FIGURE_1_EFFECTIVE_EXPOSURE_THEORY.svg
FIGURE_2_MATCHED_D_STATE_MAP.svg
FIGURE_3_DEFENCE_STATE_SWITCHES.svg
```

Visual QA completed after regeneration.

### Figure 1

Contains:

- (x_H^*) antagonist threshold;
- (x_P^*) pollinator-interference threshold;
- selective / guarded window;
- susceptibility, geometry, attack-route, timing, cumulative-exposure and response-stage axes;
- explicit bypass prediction.

### Figure 2

Contains:

- all 17 independent matched systems once each;
- cohort;
- modality;
- domain code;
- antagonist state;
- pollinator state;
- strict Stage-2 2×2 table;
- Fisher (p=0.333);
- null-compatible sensitivity (p=0.143);
- explicit domain–modality confounding warning.

### Figure 3

Contains all eight independent defence-side conditionality clusters and the Kessler 2015 bridge.

No repeated endpoint is shown as an independent biological study.

## 3. Figure 4 artifact

Workflow:

```text
run:      35394357359
artifact: sakhalkar2023-route-figure
id:       10567492447
digest:   sha256:89909a746193fb149cfbc18ba43ef0395634a39ab14fc7b1be4979cf41b76a53
```

Generated file:

```text
FIGURE_4_SAKHALKAR_ACCESS_ROUTING.svg
```

The build retrieves the public Zenodo workbook at runtime. Raw visit rows and species identifiers are not committed or emitted in the figure.

Frozen annotations:

```text
n = 57 species
Spearman rho = 0.347
permutation p = 0.0086

robber-only median tube length = 2.089
thief-only median tube length  = 0.677
```

The public-data analysis workflow separately reproduces the frozen aggregate JSON exactly.

## 4. Frozen Sakhalkar aggregate

Current reproducible result:

```text
raw workbook rows:              18,440
rows after source-script filter 14,383
visited plant species:             183
trait-matched plant species:       182
species with robbery:               26
species with thieving:              39
species with cheating + tube:       57

rho = 0.3467862681178467
permutation p = 0.0086
permutations = 9,999
seed = 20260919
```

The current workbook count remains eight below the 14,391 visits stated in the source paper summary. The candidate paper reports the deposited data as observed and does not force equality.

## 5. Current candidate package

Present:

```text
manuscript/MANUSCRIPT_FLORAL_DEFENCE_SELECTIVITY_V0.md
manuscript/CLAIM_FREEZE_MACRO_V0.md
manuscript/FLORAL_DEFENCE_SELECTIVITY_REFERENCES_V0.md
manuscript/FIGURE_PLAN_FLORAL_DEFENCE_SELECTIVITY_V0.md
manuscript/MACRO_MANUSCRIPT_SOURCE_AUDIT_V0.md
docs/EFFECTIVE_EXPOSURE_SELECTIVITY_THEORY_V1.md
empirical/floral_defence_selectivity/ECOLOGICAL_SYNTHESIS_V1.md
empirical/floral_defence_selectivity/STAGE2_MODEL_GATE_V1.md
empirical/floral_defence_selectivity/POST_RULE_VALIDATION_READOUT_V1.md
empirical/floral_defence_selectivity/TARGETED_STAGE2_CELL_AUDIT_V1.md
```

## 6. Scientific state at this receipt

Headline ecological result:

> **Access and exposure structure recurrently organizes floral antagonist–mutualist outcomes and exploitation route across matched systems, within-system state transitions, and a multispecies visitor network.**

Current matched-D inferential ceiling:

```text
strict Stage-2 N = 3
model = DESCRIPTIVE_EXACT_ONLY
domain vs modality = NOT IDENTIFIED
```

The strongest quantitative macro result is the community-scale route-switch association, not the three-study strict matched-D table.

## 7. Legacy preservation

The candidate does not delete or overwrite:

- the 56-route / 25-cluster source-adjudicated evidence architecture;
- the 17-system identification frontier;
- direct A×D anchors;
- Kessler bounds;
- identification-set and partial-identification framework;
- crossed intervention and separability logic;
- larceny and other quantitative modules;
- the old canonical mechanism-identification manuscript.

Promotion to canonical status remains an explicit editorial decision rather than an automatic consequence of this receipt.
