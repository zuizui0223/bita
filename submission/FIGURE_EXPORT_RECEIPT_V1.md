# Figure export receipt v2 — saturated Mechanism → Pattern Figures 1–3

## Decision

The saturated 25-system manuscript figure set has passed reproducible vector export from the exact figure-content checkpoint used for the expanded Figure 3.

Canonical source figures:

```text
manuscript/figures/FIGURE_1_MECHANISTIC_ARCHITECTURE.svg
manuscript/figures/FIGURE_2_THEORY_REGIME_MAP.svg
manuscript/figures/FIGURE_3_EMPIRICAL_MECHANISM_ARCHITECTURE.svg
```

Export implementation:

```text
scripts/export_manuscript_figures.sh
.github/workflows/export-manuscript-figures.yml
```

The exporter uses Inkscape CLI to create EPS vector files from the committed SVG sources, converts text to paths to avoid font substitution, and validates non-empty PostScript outputs with a header and BoundingBox.

## Saturated candidate export

Figure-content/source head:

```text
source head:       8d0df837535efaf2d31a9909e9dac5cbbf492ea1
workflow:          Export manuscript figures
workflow run:      31566025924
run number:        48
conclusion:        success
artifact:          manuscript-figures-eps
artifact id:       9129476142
artifact sha256:   014cc4f7d17541fb91d3637201013ccc391d7858a4d26779214294829e7cd27f
artifact size:     800986 bytes
```

The artifact metadata records the same source head and is not expired at the time of this receipt.

At the same source head:

```text
CI Python 3.10:    success
CI Python 3.11:    success
CI Python 3.12:    success
submission-scope:  success
EPS export:        success
```

This source head already contains the saturated manuscript, Tables 3–4, 20-entry bibliography, and expanded Figure 3. Later commits that edit only this receipt/checklist/PR metadata do not change the figure bytes and therefore do not invalidate this figure-content export receipt; they still require ordinary repository CI if they become the final package head.

## Figure-specific reproducibility state

### Figure 1 — Mechanism

The committed SVG displays:

```text
signed identity
-> explicit orientation gate
-> W_AD = rho - iota - kappa
-> local sign inequality
-> inference boundary
```

`tests/test_figure1_inference_boundary.py` protects those elements.

### Figure 2 — Mechanistic sign regimes

The canonical SVG remains tied to `endpoint_normalized_grid_v2` and protected against `empirical/part_i_robustness/endpoint_normalized_grid_v2_report.json` by `tests/test_committed_figure2.py`. The expansion did not change Part I.

### Figure 3 — Saturated Pattern architecture

The expanded builder reads the frozen five-ledger canonical evidence universe plus all admitted expansion ledgers, canonical and expansion sign-switch ledgers, seven context-only programs, the quantitative/secondary module registries, and direct/joint-cost saturation receipts.

The committed SVG is byte-reproducible and displays:

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

`tests/test_build_empirical_mechanism_figure_svg.py` requires byte-identical regeneration and the identification-boundary labels.

## Interpretation guardrails

The export changes presentation format only.

- Figure 2 percentages remain unweighted finite-grid occupancies, not empirical probabilities or prevalence estimates.
- Figure 3 route/context/module counts remain evidence architecture, not prevalence or estimates of `W_AD`.
- Context-only programs and secondary-synthesis study counts are not added to route-ledger N.
- Figure 1's oriented `rho`, `iota`, `kappa` interpretation is valid only after the displayed orientation gate.
- `kappa` is displayed as unidentified, not zero.

## Final-release rule

The Actions artifact is a validation receipt, not a permanent archive. Before actual portal submission:

1. create/freeze the exact author-approved submission release after author/licence metadata are supplied;
2. run the export workflow from that release commit if any manuscript figure changes after this receipt;
3. retain/archive the resulting EPS files with the submitted package;
4. record the release/tag and archival DOI;
5. do not treat a transient Actions artifact as the permanent archive.

## Current state

```text
SVG manuscript sources:              complete
expanded Figure 3:                   reproducible
saturated EPS export:                validated
figure-content head:                 8d0df837535efaf2d31a9909e9dac5cbbf492ea1
artifact digest recorded:            yes
Part I figure content:               unchanged
final author-approved release:       pending author metadata/licence
archival DOI:                        pending final release
```
