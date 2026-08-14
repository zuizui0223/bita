# Synthesis-level robustness audit and Gate G adjudication v1

## Decision

**Gate G — synthesis-level bias and robustness: PASS for the two quantitative modules admitted under Gate C.**

The audit is module-specific because the two modules have different data-generating structures. Diagnostics are used only when they are meaningful for the metric and dependence structure; the project does not force funnel tests or a common heterogeneity statistic onto categorical deposited-synthesis data.

## Module 1 — Leal et al. 2025 floral-larceny deposit

Canonical source implementation is pinned to PR #124 (`claude/attraction-defense-conditional-olom0x`, head `ed33b25593c0d90ad6657753f6f5501d9efc7b82`) and `empirical/broad_reality_evidence/larceny_gate/LARCENY_GATE_READOUT_V1.md` on that line.

### Independence

- deposited rows are reduced to one aggregated effect per independent study cluster within each stratum;
- primary within-cluster dependence assumption is conservative (`rho_w = 1.0`);
- primary strata contain 48 female-fitness, 28 nectar-standing-crop, and 22 legitimate-visitation clusters; the male-fitness stratum has 11 clusters and is explicitly uninformative.

### Heterogeneity

The admitted pooled effects retain very high between-study heterogeneity:

```text
female fitness        I2 = 99.5%
nectar standing crop  I2 = 99.3%
legitimate visitation I2 = 97.5%
```

The large heterogeneity is part of the result, not suppressed by reporting only the pooled mean. Six preregistered moderator analyses explain only 0–8% of it and are reported as underpowered non-detections rather than evidence of homogeneity.

### Influence and declared sensitivity

- leave-one-cluster-out refits retain the pooled direction in 100% of refits across the reported analyses;
- changing the within-cluster correlation from `1.0` to `0.5` or `0.0` preserves sign, magnitude, and interval exclusion for the three informative arrows;
- including the three quarantined sign-discrepant deposit rows likewise preserves the three informative conclusions;
- the source deposit was recomputed from its group means: 260/267 rows reproduce as log response ratios, four require variance recomputation, and three sign-discrepant rows are quarantined rather than silently resolved.

### Modern random-effects estimator sensitivity

Because the canonical DerSimonian–Laird analyses have extreme heterogeneity, the same one-effect-per-independent-cluster inputs were additionally checked with REML heterogeneity estimation plus modified Hartung–Knapp inference. This is a **sensitivity analysis only**: the preregistered DerSimonian–Laird estimates remain the canonical manuscript point estimates.

Canonical and sensitivity results:

```text
female reproductive success
  canonical DL pooled = -0.2105
  REML pooled         = -0.2048
  modified HK 95% CI  = [-0.3318, -0.0777]

nectar standing crop
  canonical DL pooled = -0.4834
  REML pooled         = -0.4894
  modified HK 95% CI  = [-0.7948, -0.1840]

legitimate visitation
  canonical DL pooled = -0.2907
  REML pooled         = -0.2879
  modified HK 95% CI  = [-0.5756, -0.0002]
```

All three intervals remain below zero, so the direction is not an artefact of the canonical DerSimonian–Laird estimator. However, the legitimate-visitation upper limit is only about `-0.00018`; this outcome is therefore recorded as **borderline estimator robustness**, not as a strong exclusion of zero. Female reproductive success and nectar standing crop remain clearly negative under the more conservative inferential convention.

The deterministic readout is:

- `empirical/mechanism_pattern_synthesis/LEAL_2025_MODERN_ESTIMATOR_SENSITIVITY_V1.md`
- `empirical/mechanism_pattern_synthesis/LEAL_2025_MODERN_ESTIMATOR_SENSITIVITY_V1.json`
- `scripts/run_leal_modern_estimator_sensitivity.py`
- `.github/workflows/leal-modern-estimator-sensitivity.yml`

Method references encoded in the readout are Röver, Knapp & Friede (2015; DOI `10.1186/s12874-015-0091-1`) for the modified Knapp–Hartung procedure and Partlett & Riley (2017; DOI `10.1002/sim.7140`) for REML/Hartung–Knapp coverage behavior.

### Small-study / publication-bias diagnostics

Egger-type asymmetry is reported where there are enough study clusters:

```text
female fitness:        asymmetry detected, p = 1.6e-9
legitimate visitation: asymmetry detected, p = 0.021
nectar standing crop:  no detected asymmetry, p = 0.98
```

The readout explicitly limits interpretation because log response ratios couple effect magnitude and sampling variance, making Egger regression prone to metric-induced asymmetry. Opposite asymmetry directions across strata and no asymmetry for the reward stratum are retained as part of that limitation. No publication-bias correction is used to manufacture a preferred adjusted effect.

### Scope limitation

This is a secondary analysis of a deposited synthesis, not a new systematic search. It inherits the source authors' search, screening, and extraction universe and is restricted biologically to floral nectar larceny. It provides an antagonist-pressure gate module, not an estimate of the attraction–defence mixed partial. The REML/modified-Hartung–Knapp check strengthens estimator robustness only; it does not reduce the biological heterogeneity or make the source search independent of Leal et al.

## Module 2 — Sasidharan et al. 2023 FVOC deposited synthesis

Canonical current-branch source is `SASIDHARAN_2023_REPRO_READOUT_V1.md` with machine adjudication `PASS_AS_DEPOSITED_REANALYSIS`.

### Independence

- 36 raw reference strings are conservatively reconciled to exactly **32 study components** using exact citation stems plus explicit shared DOI links;
- fuzzy bibliographic similarity is diagnostic only and never merges studies;
- the older 34-cluster DOI-first reconstruction is explicitly noncanonical.

### Influence

For the current-deposit physiological-detection contrast (florivore minus pollinator risk difference `+0.1292`):

```text
leave-one-study-component-out runs: 32
minimum difference:                  +0.0873
median difference:                   +0.1274
maximum difference:                  +0.2065
positive direction:                  32 / 32
```

An equal-weight study-role sensitivity retains the same assembled direction.

### Composition / heterogeneity limitation

Only three recovered study components contain physiological-detection data for both functional roles, and all three paired differences are zero. The assembled `+12.9` percentage-point pattern is therefore explicitly **not** interpreted as a within-study causal role effect.

Behavioral data provide a separate heterogeneity signal: six repeated `FVOC x insect x role` units disagree across source studies, all switching between attraction and no response. These disagreements are retained rather than deduplicated away.

### Source-version robustness

The current PMC deposit and printed article differ in bounded ways:

- current deposit has one additional detected florivore physiological unit relative to the printed table;
- behavioral pollinator totals cannot be exactly reconstructed from current S1;
- shared-attraction counts differ among printed genus cells, printed total, and current deposit.

The module therefore reports current-deposit quantities and explicit discrepancy bounds instead of choosing rows to force agreement.

### Why no funnel test is run

A conventional small-study/funnel diagnostic is **not appropriate** for this module. The source is a categorical ledger of physiological detection and behavioral state across heterogeneous assays, and the project does not construct one homogeneous study-level effect plus standard error merely to enable Egger testing. Omitting such a test is a metric-appropriate decision, not an unreported diagnostic.

## Non-module layers

The direct `A x D` layer contains one strict study cluster and is therefore not eligible for publication-bias diagnostics or pooled heterogeneity estimation. The same-system and sign-switch layers are recurrence/conditionality maps; source verification and dependence are reported, but their counts are not treated as effect sizes.

## Gate G status

```text
Module 1 Leal 2025:
  independence audit                PASS
  influence audit                   PASS
  heterogeneity                     REPORTED
  small-study diagnostic            REPORTED_WITH_METRIC_LIMITATION
  declared sensitivity              PASS
  REML + modified Hartung-Knapp     PASS_WITH_BORDERLINE_VISITATION

Module 2 Sasidharan 2023:
  independence audit                PASS
  influence audit                   PASS
  heterogeneity/context             RETAINED
  source discrepancy                EXPLICIT
  small-study diagnostic            NOT_APPROPRIATE_FOR_METRIC

Gate G:                              PASS
```

## Repository packaging note

The Leal implementation remains deliberately pinned to immutable PR #124 commit `ed33b25593c0d90ad6657753f6f5501d9efc7b82` rather than duplicated and silently reimplemented on PR #129. The supplement manifest records that immutable dependency, and the modern-estimator sensitivity reads the cluster-level contributing effects directly from the pinned commit. This resolves the consolidation requirement without changing the canonical numerical analysis.
