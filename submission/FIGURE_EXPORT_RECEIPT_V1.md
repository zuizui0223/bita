# Figure export receipt v4 — submission-ready Mechanism → Pattern Figures 1–3

## Decision

The saturated 25-system main-figure set has passed reproducible vector export in the current *Theoretical Ecology* submission form at the same checkpoint that also carries the modernized supplementary robustness figure.

Canonical scientific source figures remain:

```text
manuscript/figures/FIGURE_1_MECHANISTIC_ARCHITECTURE.svg
manuscript/figures/FIGURE_2_THEORY_REGIME_MAP.svg
manuscript/figures/FIGURE_3_EMPIRICAL_MECHANISM_ARCHITECTURE.svg
```

Submission export implementation:

```text
scripts/prepare_submission_svg.py
scripts/export_manuscript_figures.sh
.github/workflows/export-manuscript-figures.yml
```

The canonical SVGs are retained as the reproducible scientific sources. For submission export only, `prepare_submission_svg.py` deterministically removes exactly one visible outer figure-title text element from each illustration while retaining panel labels, equations, annotations, and accessibility metadata. The exporter then creates vector EPS files with Inkscape, converts text to paths to prevent font substitution, and verifies the PostScript header and BoundingBox.

## Current submission-form export validation

```text
source head:       fe274a91349931c08b8d820f99dc7b3ab5d8f725
workflow:          Export manuscript figures
workflow run:      31666278452
run number:        96
conclusion:        success
artifact:          manuscript-figures-eps
artifact id:       9168041835
artifact sha256:   f4fb42b7421958a5a5251f24f03c666de2735b28bbded739286e65e9705090fd
artifact size:     759365 bytes
submission files:  Fig1.eps, Fig2.eps, Fig3.eps
```

Artifact metadata records the same source head. At that source head, core CI, submission-scope, and the main EPS workflow all completed successfully. The supplementary package workflow also completed successfully and the committed Fig. S4 displays the registered REML + modified Hartung–Knapp sensitivity while retaining the canonical DerSimonian–Laird estimates.

## Submission preprocessing contract

The submission EPS files differ from the canonical SVG sources only in presentation required for journal upload:

1. exactly one visible outer figure-title line is removed from each figure;
2. the manuscript retains the corresponding `**Fig. 1**`, `**Fig. 2**`, and `**Fig. 3**` captions outside the illustration;
3. panel headings and scientific annotations are retained;
4. vector geometry is retained;
5. text is converted to paths only during EPS export;
6. filenames are `Fig1.eps`, `Fig2.eps`, and `Fig3.eps`.

`tests/test_theoretical_ecology_house_style.py` executes the SVG preprocessor on all three canonical figures and verifies that each visible outer title is removed while internal scientific content remains.

## Figure-specific scientific reproducibility

### Fig. 1 — Mechanism

The canonical source remains protected for:

```text
signed identity
-> explicit orientation gate
-> W_AD = rho - iota - kappa
-> local sign inequality
-> inference boundary
```

No Part I scientific content was changed by submission preprocessing.

### Fig. 2 — Mechanistic sign regimes

The canonical SVG remains tied to `endpoint_normalized_grid_v2` and protected against `empirical/part_i_robustness/endpoint_normalized_grid_v2_report.json`. Percentages are finite-grid occupancies, not prevalence estimates.

### Fig. 3 — Saturated Pattern architecture

The expanded builder reads the frozen five-ledger canonical universe plus all admitted expansion ledgers, canonical and expansion sign-switch ledgers, seven context-only programs, the quantitative/secondary module registries, and direct/joint-cost saturation receipts.

The scientific source displays:

```text
56 route records / 25 independent systems
A -> pollination 5
A -> antagonism 8
D -> antagonism 18
D -> pollination 10
same-system 14
context/sign-switch 17
context-only programs 7
2 reproduced quantitative modules
3 secondary contextual syntheses
direct A x D: 1 strict sign-unresolved cluster
direct joint cost: 0 strict estimates; kappa unidentified
```

The committed scientific SVG is byte-reproducible before the journal-specific title-strip export step.

### Fig. S4 — quantitative robustness companion

The supplementary robustness figure is generated from the canonical module summaries and then deterministically augmented from `LEAL_2025_MODERN_ESTIMATOR_SENSITIVITY_V1.json`. The added inset preserves the canonical DerSimonian–Laird estimates and separately displays REML + modified Hartung–Knapp sensitivity for the same independent-cluster inputs. The legitimate-visitation interval is explicitly flagged borderline to zero rather than strengthened into a more confident claim.

## Interpretation guardrails

The export and supplementary presentation changes do not alter scientific quantities.

- Fig. 2 percentages remain unweighted finite-grid occupancies, not empirical probabilities or prevalence estimates.
- Fig. 3 route/context/module counts remain evidence architecture, not prevalence or estimates of `W_AD`.
- Context-only programs and secondary-synthesis study counts are not added to route-ledger N.
- Fig. 1's oriented `rho`, `iota`, `kappa` interpretation is valid only after the orientation gate.
- Fig. S4's REML/mHK inset is a robustness sensitivity, not a replacement of the canonical meta-analysis.
- `kappa` remains unidentified, not zero.

## Final-release rule

This Actions artifact is a validation receipt, not the permanent archive. Before actual portal submission:

1. freeze the exact author-approved manuscript after author/licence/declaration fields are supplied;
2. rerun the export if any canonical figure or figure-caption requirement changes;
3. retain the resulting `Fig1.eps`–`Fig3.eps` with the submitted package;
4. render the reader-facing supplement only after author/release metadata are frozen;
5. record the final release/tag and archival DOI;
6. do not treat a transient Actions artifact as the permanent repository archive.

## Current state

```text
canonical SVG scientific sources:      complete
expanded Fig. 3:                       reproducible
supplementary Fig. S4 modern sensitivity: synchronized / tested
journal caption convention:            implemented
visible outer title stripping:         validated
submission filenames Fig1-Fig3.eps:   validated
submission-form EPS export:            GREEN
submission EPS source head:            fe274a91349931c08b8d820f99dc7b3ab5d8f725
artifact digest recorded:              yes
core CI / submission-scope at source:  GREEN
Part I scientific figure content:      unchanged
final author-approved release:         pending author metadata/licence
archival DOI:                          pending final release
```
