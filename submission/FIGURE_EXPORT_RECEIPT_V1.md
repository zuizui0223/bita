# Figure export receipt v3 — submission-ready Mechanism → Pattern Figures 1–3

## Decision

The saturated 25-system figure set has passed reproducible vector export in the current *Theoretical Ecology* submission form.

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

The canonical SVGs are retained as the reproducible scientific sources. For submission export only, `prepare_submission_svg.py` deterministically removes exactly one visible outer figure-title text element from each illustration, while retaining panel labels, equations, annotations, and accessibility metadata. The exporter then creates vector EPS files with Inkscape, converts text to paths to prevent font substitution, and verifies the PostScript header and BoundingBox.

## Final submission-form export validation

```text
source head:       417ee8ce97269f07207d824f8950cbc275c9115a
workflow:          Export manuscript figures
workflow run:      31567045329
run number:        66
conclusion:        success
artifact:          manuscript-figures-eps
artifact id:       9129851593
artifact sha256:   ac255025840465dce4fd22e645e823ea80a09af7cbcc8770aeec7be27c35722f
artifact size:     759365 bytes
submission files:  Fig1.eps, Fig2.eps, Fig3.eps
```

Artifact metadata records the same source head and the artifact was not expired when this receipt was written.

At the same source head, the dedicated Pattern/house-style workflow also passes the expansion contract, readout regeneration, Figure 3 byte-reproducibility, journal-format tests, and manuscript-facing regression tests.

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

## Interpretation guardrails

The export changes presentation format only.

- Fig. 2 percentages remain unweighted finite-grid occupancies, not empirical probabilities or prevalence estimates.
- Fig. 3 route/context/module counts remain evidence architecture, not prevalence or estimates of `W_AD`.
- Context-only programs and secondary-synthesis study counts are not added to route-ledger N.
- Fig. 1's oriented `rho`, `iota`, `kappa` interpretation is valid only after the orientation gate.
- `kappa` remains unidentified, not zero.

## Final-release rule

This Actions artifact is a validation receipt, not the permanent archive. Before actual portal submission:

1. freeze the exact author-approved manuscript after author/licence/declaration fields are supplied;
2. rerun the export if any canonical figure or figure caption requirement changes;
3. retain the resulting `Fig1.eps`–`Fig3.eps` with the submitted package;
4. record the final release/tag and archival DOI;
5. do not treat a transient Actions artifact as the permanent repository archive.

## Current state

```text
canonical SVG scientific sources:      complete
expanded Fig. 3:                       reproducible
journal caption convention:            implemented
visible outer title stripping:         validated
submission filenames Fig1-Fig3.eps:   validated
submission-form EPS export:            GREEN
submission EPS source head:            417ee8ce97269f07207d824f8950cbc275c9115a
artifact digest recorded:              yes
Part I scientific figure content:      unchanged
final author-approved release:         pending author metadata/licence
archival DOI:                          pending final release
```
