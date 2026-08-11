# Figure and table plan for integrated Theoretical Ecology submission

## Main-text figures

### Figure 1. Mechanistic architecture and inference boundary

**Purpose:** make the ecological problem, orientation gate, sign criterion, and identification boundary understandable before the detailed algebra.

The figure should show:

1. one declared attraction trait `A` affecting mutualist service and antagonist exposure;
2. one declared flower-specific antagonist-reducing defence/access trait `D` reducing antagonist damage while potentially interfering with legitimate pollinator use;
3. a direct joint-cost channel;
4. the oriented local balance

```text
W_AD = rho - iota - kappa
```

5. an explicit boundary indicating that total `W_AD` does not identify the three channel curvatures without channel-specific measurements or interventions.

**Caption boundary:** `W_AD > 0` is local complementarity of marginal effects; it does not imply that both first derivatives are positive. The orientation gate must precede the non-negative `rho`, `iota`, `kappa` interpretation.

### Figure 2. Conditional sign regimes in the implemented corollary

Use the existing generated SVG from `scripts/build_part_i_regime_figure_svg.py` as the numerical source. Do not redraw values manually.

**Purpose:** demonstrate that opposite sign-dominant regimes arise under contrasting channel strengths while response-shape agreement can remain high within a fixed biological scenario.

Required labels/caption language:

- 2,592 declared evaluations;
- endpoint-normalized response-shape variants;
- contrasting biological scenarios;
- `R` shown only as an auxiliary moderator;
- 51.8% / 48.2% described only as **unweighted finite-grid occupancy**;
- no probability, posterior probability, or prevalence language.

### Figure 3. Empirical mechanism-pattern architecture and identification boundary

**Purpose:** make the empirical half answer the theory rather than look like a list of case studies.

Recommended layout:

**Panel A — evidence architecture**

Four marginal route families around the same theoretical diagram:

```text
A -> pollination       4 independent clusters
A -> antagonism        5
D -> antagonism       10
D -> pollination       7
```

Show overlap/dependence explicitly: the route counts are not additive independent-study totals. Total source-adjudicated architecture = 38 effect/directional records across 14 independent biological study clusters.

**Panel B — same-system and conditionality layer**

```text
same-system multi-route clusters: 10
context/sign-switch clusters:     11
```

Represent the five conditionality classes rather than plotting a fake pooled moderator coefficient:

1. trait intensity / expression;
2. resource / exposure;
3. consumer identity / functional role;
4. response definition / decision stage / reproductive scale;
5. compound identity / mechanism partition.

**Panel C — identification bottlenecks**

```text
direct A x D:       1 strict cluster, sign unresolved
direct joint cost:  0 strict estimates, kappa unidentified
```

The visual should terminate the marginal/same-system arrows at an inference boundary before `W_AD` so readers cannot interpret route counts as parameter estimates.

**Panel D — two quantitative modules**

Compact summaries only:

- Leal et al. 2025: female fitness LRR −0.210 (48 clusters), nectar −0.483 (28), visitation −0.291 (22); high heterogeneity retained.
- Sasidharan et al. 2023: florivore 84/103 vs pollinator 151/220 physiological detections, assembled risk difference +0.129, LOCO positive 32/32; only three paired both-role components, all difference 0.

The two modules should be labelled **constituent-mechanism evidence, not `W_AD` estimates**.

## Main-text tables

### Table 1. Definitions and inference boundaries

Use canonical `manuscript/TABLES_THEORETICAL_ECOLOGY.md` Table 1 without introducing alternate symbols.

### Table 2. Canonical finite sensitivity design and results

Use only values generated from the canonical `endpoint_normalized_grid_v2` readout.

### Table 3. Source-adjudicated mechanism-pattern evidence architecture

Report:

- four route-family cluster counts;
- same-system and conditionality states;
- direct `A x D` evidence state;
- direct joint-cost evidence state;
- inference boundary for each layer.

Do not sum overlapping route counts into an apparent total study count. Do not describe any fraction as prevalence.

### Table 4. Quantitative synthesis modules and admitted inference

For each module report:

- data structure / dependence unit;
- canonical quantitative result;
- influence / heterogeneity / source-discrepancy boundary;
- admitted role in the paper;
- prohibited interpretation.

The canonical table is already drafted in `manuscript/TABLES_THEORETICAL_ECOLOGY.md`.

## Supplementary figures and tables

### Figure S1
Analytic versus finite-difference derivative agreement for each endpoint-normalized response-shape variant.

### Figure S2
Scenario-specific sign maps separated by response-shape variant.

### Figure S3
Study-level same-system regime ledger, preferably as a categorical matrix rather than a frequency plot.

### Figure S4
Quantitative-module robustness panels: Leal leave-one-cluster-out / sensitivity summaries and Sasidharan leave-one-study-component-out range. Keep the two metrics visually separate.

### Table S1
Complete parameter definitions, values, units or dimensionless scaling, and biological interpretation.

### Table S2
All 162 local cases and the four-scenario × four-shape classification summaries.

### Table S3
Master source-adjudicated mechanism ledger with study dependence and source-verification fields.

### Table S4
Sign-switch/context ledger with the five-class theory-facing ontology.

### Table S5
Direct `A x D` and joint-cost search decisions / exclusion classes, documenting saturation rather than presenting zero yield as absence proof.

## Production rules

1. Generate numerical figures only from committed scripts and canonical inputs.
2. Record the exact commit SHA used for final exports.
3. Export vector PDF or EPS for submission and retain SVG as the reproducible source where applicable.
4. Use consistent symbols with the manuscript: `rho`, `iota`, and `kappa`.
5. Never display 51.8% and 48.2% without “unweighted finite-grid occupancy” in the same panel or caption.
6. Keep `R` visually subordinate and label it as an auxiliary moderator.
7. Never convert route counts, same-system counts, sign-switch counts, or deposited-test fractions into prevalence language.
8. Never visually sum marginal evidence into `W_AD`; show an inference boundary.
9. Display `kappa` as **unidentified**, not as zero.
10. Keep Leal and Sasidharan quantitative metrics in separate visual encodings; they do not share a common effect-size scale.
