# Figure and table plan — Mechanism → Pattern submission

The visual package must make the manuscript’s two-part scientific architecture obvious without relying on section headings alone.

```text
Part I — Mechanism: Figures 1–2, Tables 1–2
Part II — Pattern:   Figure 3, Tables 3–4
```

## Part I — Mechanism

### Figure 1. Mechanistic architecture, orientation gate, and inference boundary

**Purpose:** show the mathematical/mechanistic logic before any cross-study evidence is introduced.

Required visual chain:

```text
W_AD = M_AD - G_AD - C_AD
→ ORIENTATION GATE
→ W_AD = rho - iota - kappa
→ complementarity/substitutability inequality
→ INFERENCE BOUNDARY
```

The figure must also retain the biological channels connecting attraction `A` and defence `D` to mutualist contribution, antagonist loss, and direct joint cost.

**Boundary:** `W_AD > 0` is local complementarity of marginal effects; it does not imply positive first derivatives and does not identify mechanism from total `W` alone.

### Figure 2. Mechanistic sign regimes in the implemented corollary

Use `scripts/build_part_i_regime_figure_svg.py` and the canonical `endpoint_normalized_grid_v2` source.

**Purpose:** show that the same mechanism equation yields complementary or substitutable regimes as biological channel strengths change.

Required language:

- 2,592 declared evaluations;
- endpoint-normalized response-shape variants;
- contrasting biological scenarios;
- `R` only as an auxiliary moderator;
- 51.8% / 48.2% only as **unweighted finite-grid occupancy**;
- never probability or prevalence.

### Table 1. Mechanistic definitions and inference boundaries

Use canonical Table 1. It belongs to Part I and defines the variables, orientation gate, and what each quantity does not imply.

### Table 2. Mechanistic finite-sensitivity design and sign regimes

Use only canonical `endpoint_normalized_grid_v2` values. It belongs to Part I and is a robustness/sensitivity table, not an empirical pattern table.

## Part II — Pattern

### Figure 3. Meta-analytic pattern architecture and identification boundary

**Purpose:** answer the Part I mechanism with cross-study patterns while preventing the reader from mistaking heterogeneous marginal evidence for an estimate of `W_AD`.

The committed figure must contain four distinct elements.

**A — Cross-study pattern scaffold**

```text
A -> pollination       4 independent clusters
A -> antagonism        5
D -> antagonism       10
D -> pollination       7
38 effect/directional records
14 independent biological study clusters
```

This scaffold maps recurrence onto Part I mechanisms. It is **not a grand meta-analysis**, and overlapping route counts are not additive study totals.

**B — Recurrence and conditionality**

```text
same-system multi-route clusters: 10
context/sign-switch clusters:     11
```

Five theory-facing context classes:

1. trait intensity / expression;
2. resource / exposure;
3. consumer identity / functional role;
4. response definition / decision stage / reproductive scale;
5. compound identity / mechanism partition.

**C — Quantitative cross-study patterns**

- **Meta-analysis 1 — Leal et al. 2025:** female fitness LRR −0.210 (48 clusters), nectar −0.483 (28), visitation −0.291 (22); extreme heterogeneity retained.
- **Meta-analytic synthesis 2 — Sasidharan et al. 2023:** florivore 84/103 vs pollinator 151/220 physiological detections, assembled risk difference +0.129, LOCO positive 32/32; only three paired both-role components and all paired differences 0.

The two quantitative modules must remain visually separate because they do not share an effect-size scale.

**D — Identification bottlenecks**

```text
direct A x D:       1 strict cluster, sign unresolved
direct joint cost:  0 strict estimates, kappa unidentified
```

An explicit **IDENTIFICATION BOUNDARY** must separate the recurrent/meta-analytic pattern evidence from direct identification of `W_AD`.

### Table 3. Cross-study pattern scaffold

Report the four route-family cluster counts, same-system recurrence, conditionality, direct `A x D` state, and direct joint-cost state. Explicitly state that this is a theory-to-pattern scaffold rather than a pooled grand effect.

### Table 4. Quantitative meta-analytic patterns

For Leal and Sasidharan report:

- dependence unit and data scale;
- canonical quantitative pattern;
- influence/heterogeneity/source-discrepancy diagnostics;
- admitted cross-system inference;
- prohibited inference regarding `rho`, `iota`, `kappa`, or `W_AD`.

## Supplementary figures and tables

### Figure S1
Analytic versus finite-difference derivative agreement for each endpoint-normalized response-shape variant.

### Figure S2
Scenario-specific mechanistic sign maps separated by response-shape variant.

### Figure S3
Study-level same-system pattern ledger as a categorical matrix.

### Figure S4
Quantitative robustness panels: Leal leave-one-cluster-out/sensitivity summaries and Sasidharan leave-one-study-component-out range. Keep metrics visually separate. **These robustness panels remain supplementary rather than being added to main Figure 3.**

### Table S1
Complete parameter definitions, values, units or scaling, and biological interpretation.

### Table S2
All 162 local cases and the four-scenario × four-shape classifications.

### Table S3
Master source-adjudicated mechanism/pattern ledger with dependence and verification fields.

### Table S4
Sign-switch/context ledger with the five-class ontology.

### Table S5
Direct `A x D` and joint-cost search decisions/exclusion classes documenting saturation.

## Production rules

1. Mechanism figures/tables must precede Pattern figures/tables in narrative role.
2. Generate numerical figures only from committed scripts and canonical inputs.
3. Record the exact commit SHA used for final exports.
4. Export vector EPS for submission and retain SVG as the reproducible source.
5. Never display finite-grid occupancies as probabilities/prevalence.
6. Never convert route/sign-switch/deposit counts into prevalence.
7. Never visually sum marginal evidence into `W_AD`.
8. Display `kappa` as **unidentified**, not zero.
9. Keep Leal and Sasidharan in separate visual encodings.
10. The one-sentence visual conclusion of Part II is: **recurrent mechanism plus context-dependent balance**.
