# Figure export receipt v1 — manuscript Figures 1–3

## Decision

The current manuscript figure set has passed a reproducible vector-export check suitable for the final Springer/*Theoretical Ecology* packaging workflow.

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

The exporter uses Inkscape CLI to create EPS vector files from the committed SVG sources and converts text to paths to avoid font substitution. It validates that each output is non-empty and contains a PostScript header and BoundingBox.

## Latest validated export

The latest export includes the strengthened Figure 1 with the explicit signed identity, orientation gate, oriented balance, and inference boundary.

```text
source head:       51d75c8c8f02525430d7e369c1d9eeeb86964e99
workflow:          Export manuscript figures
workflow run:      31542777226
run number:        3
conclusion:        success
artifact:          manuscript-figures-eps
artifact id:       9121336188
artifact sha256:   ec4752ee35b32448f75935a2866e55527cefcc1e99051e651c1030dc17c6cbf5
artifact size:     774152 bytes
```

At the same source head, all 14 pull-request workflows completed successfully, including core CI, submission-scope, mechanism/same-system audits, the source-specific audit workflows, and this EPS export.

## Figure-specific reproducibility state

### Figure 1

The committed SVG directly displays:

```text
signed identity
-> explicit orientation gate
-> W_AD = rho - iota - kappa
-> local sign inequality
-> inference boundary
```

`tests/test_figure1_inference_boundary.py` protects those required elements.

### Figure 2

The canonical SVG is tied to `endpoint_normalized_grid_v2` and protected against `empirical/part_i_robustness/endpoint_normalized_grid_v2_report.json` by `tests/test_committed_figure2.py`. Provenance is recorded in `manuscript/figures/README.md`.

### Figure 3

The SVG is rebuilt from the canonical five-ledger coverage universe, sign-switch ledger, quantitative-module registry, and direct/joint-cost saturation receipts. `tests/test_build_empirical_mechanism_figure_svg.py` requires byte-identical regeneration.

## Interpretation guardrails

The export step changes presentation format only. It does not change any scientific quantity.

- Figure 2 percentages remain unweighted finite-grid occupancies, not empirical probabilities or prevalence estimates.
- Figure 3 route/module counts remain evidence architecture, not estimates of `W_AD` or prevalence in nature.
- Figure 1's oriented `rho`, `iota`, `kappa` interpretation is valid only after the displayed orientation gate.

## Final-release rule

The Actions artifact is a validation receipt, not a permanent archive. Before portal submission:

1. run the same export workflow from the exact final submission commit;
2. retain or archive the resulting EPS files with the submitted manuscript package;
3. record the final commit SHA, workflow run, artifact digest, and archival DOI/release identifier;
4. do not reuse this transient Actions artifact as the archival submission object if the manuscript or figures change.

## Current state

```text
SVG manuscript sources:          complete
reproducible EPS exporter:       complete
strengthened Figure 1 export:    validated
Figure 2 canonical export:       validated
Figure 3 reproducible export:    validated
current export workflow:         green
final-release export rerun:      still required after all final metadata/formatting edits
```
