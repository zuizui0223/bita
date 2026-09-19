# BITA floral-defence selectivity — main figure plan v0

For candidate manuscript manuscript/MANUSCRIPT_FLORAL_DEFENCE_SELECTIVITY_V0.md.

The figure set is designed to make the paper read as a macro-ecology paper, not as an identification-warning paper.

## Figure 1 — Effective-exposure selectivity theory

**Purpose:** establish the mechanism before showing the literature pattern.

### Panel A — two response thresholds

x-axis: focal defence/access intensity x.

Show antagonist response crossing x_H* and pollinator interference crossing x_P*, with the selective window x_H* < x < x_P*.

Three labelled zones:

~~~text
ineffective
selective / guarded
interfering
~~~

### Panel B — what moves the thresholds

Map q_H and q_P to susceptibility, geometry/body size, attack route, timing, cumulative exposure, functional mode, and response stage.

Show separation widening the window and overlap narrowing it.

### Panel C — bypass

Show a flower with legitimate opening, focal barrier, and bypass hole/alternative route.

Prediction: blocked legitimate route does not imply eliminated exploitation.

**Main message:** selectivity depends on relative effective exposure and response thresholds, not on defence label alone.

Source: docs/EFFECTIVE_EXPOSURE_SELECTIVITY_THEORY_V1.md.

---

## Figure 2 — D-side macro landscape and matched-D state map

**Purpose:** show the broad D-side evidence base and then the stricter matched-system layer without pretending heterogeneous outcomes share one effect scale.

### Panel A — route-level D macro landscape

Show:

~~~text
17 unique D-study programs

implementation:
  chemical      9
  physical      7
  reward/access 1

same-study pollinator follow-up:
  10 / 17

pollination-state families:
  context-dependent 4
  null-compatible   3
  improved          1
  interference      1
  unresolved        1
~~~

Add a note:

> legacy D-side count is deduplicated at study-program level; Takeda 2021 entered the historical ledger twice through separate ingestion paths.

### Panel B — system-by-state matrix

Rows = 17 independent matched systems.

Columns:

1. cohort: derivation / systematic expansion / holdout;
2. defence modality;
3. effective-domain state;
4. antagonist efficacy;
5. pollinator state.

Use distinct symbols for preserved/improved, no detected change, impaired, mixed/transition, unresolved, and bypass/null defence.

Architecture code origin must remain visible: historical derivation / source-mechanistic post hoc / prospective blind.

### Panel C — macro state-recovery summary

Annotate:

~~~text
historical derivation: 9 / 9
systematic expansion:  2 / 2
pooled scored:        11 / 11

modality comparator:
historical LOO:        6 / 9
expansion:             1 / 2
~~~

Add a small note:

> Historical alignment probabilities are descriptive because the derivation systems contributed to theory formation.

### Panel D — strict Stage-2 exact table

~~~text
                         compatible   impaired
SEPARATED                     2           0
OVERLAPPED                    0           1
~~~

Annotate Fisher two-sided p = 0.333 and DESCRIPTIVE_EXACT_ONLY.

### Panel E — null-compatible sensitivity

~~~text
SEPARATED compatible-or-null = 6
OVERLAPPED impaired          = 1
Fisher p = 0.143
~~~

Large note: null-compatible is not equivalence-supported preservation.

### Panel F — current confounding

~~~text
Thunia        separated   physical
Caryopteris   separated   physical
Gelsemium     overlapped  chemical
~~~

Therefore domain-versus-modality comparison is not identified.

Data sources:
- empirical/floral_defence_selectivity/results/analysis_ready_matched_systems.csv
- empirical/floral_defence_selectivity/results/stage2_model_gate.json
- empirical/floral_defence_selectivity/results/effective_domain_state_recovery.json
- empirical/floral_defence_selectivity/results/d_side_route_macro_summary.json
- empirical/floral_defence_selectivity/d_side_route_macro_registry.csv

---

## Figure 3 — Selective windows open and close within systems

**Purpose:** recover the strongest inherited BITA biological result rather than relegating it to provenance.

### Panel A — ordered exposure systems

Four horizontal transition tracks:

- Polemonium;
- Asclepias colony exposure;
- Asclepias syriaca dose;
- Aconitum.

Generic state sequence:

~~~text
low exposure        intermediate             high exposure
ineffective/null →  guarded/selective  →     pollinator interference
~~~

Only place systems into states supported by their source audits.

### Panel B — other conditionality axes

Group remaining defence-side systems by consumer identity, response stage, reward context, and temporal expression.

### Panel C — Kessler 2015 bridge

Show the same nectar-restriction axis with high pollination cost in Manduca but no detected single-axis cost in Hyles.

Keep the legacy source-mean A×D sign reversal as a small annotation, not the dominant panel.

**Main message:** selectivity is dynamic; the same trait can change ecological state without changing defence category.

Data sources:
- empirical/floral_defence_selectivity/d_side_conditionality_registry.csv
- empirical/floral_defence_selectivity/D_SIDE_CONDITIONALITY_READOUT_V1.md
- empirical/floral_defence_selectivity/KESSLER_2015_LEGACY_RESULT_BRIDGE_V1.md

---

## Figure 4 — Community-scale route switching in Sakhalkar 2023

**Purpose:** provide the macro-ecological quantitative result.

### Panel A — species-level tube length vs cheating-mode balance

x-axis = tube length.

y-axis:

\[
B=(R-T)/(R+T)
\]

where +1 = robbing-only and -1 = thieving-only.

Plot one point per plant species, n = 57. Overlay only a simple monotonic trend or rank summary; do not imply linear causality.

Annotate:

~~~text
Spearman rho = 0.347
permutation p = 0.0086
n = 57 species
~~~

### Panel B — route-specific descriptive distributions

Compare tube length for robber-only and thief-only species.

Annotate medians:

~~~text
robber-only  2.0893
thief-only   0.6766
~~~

Do not present the approximate threefold ratio as an inferential test.

### Panel C — ecological routing interpretation

~~~text
short / accessible
    -> legitimate opening usable
    -> thieving relatively favoured

long / constrained
    -> opening mismatch
    -> bypass/robbing relatively favoured
~~~

**Main message:** access geometry is associated with exploitation route; the univariate tube-length signal should not be presented as a uniquely identified partial effect.

Data/source:
- Zenodo DOI 10.5281/zenodo.8398202
- scripts/analyze_sakhalkar2023_network.py
- empirical/floral_defence_selectivity/results/sakhalkar2023_network_result.json

The plotting workflow may download the public workbook at build time, but raw species rows must not be committed. Add the source-defined multitrait sensitivity note: full-model permutation p = 0.202 and tube-length block p = 0.211; brightness is unavailable in the deposited trait table, so thief-source and union models are not estimable.

---

## Supplementary figures retained from legacy BITA

Move identification-focused graphics out of the new Main rather than deleting them:

- identified-set geometry;
- A×D×antagonist×pollinator intervention ladder;
- four-way separability diagnostic;
- 56-route / 25-cluster evidence architecture;
- 17-system identification frontier;
- Kessler 2008 aggregate partial-identification bounds.

These remain scientifically useful but no longer define the paper's visual first impression.

## Figure production order

1. Figure 4 — quantitative public-data result and least ambiguous.
2. Figure 2 — deterministic from committed matched-system tables.
3. Figure 3 — conditionality audit requires careful state labeling.
4. Figure 1 — final theory graphic after notation is frozen.

## Figure completion gate

- every plotted system must trace to a provenance path;
- repeated outcomes from one study must not appear as independent systems;
- null-compatible states must be graphically distinct from preservation;
- cohort/origin must remain visible in Figure 2;
- Figure 4 must use plant species as the inferential unit;
- no panel may imply a domain-versus-modality comparison that the strict data cannot identify.
