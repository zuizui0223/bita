# Repository structure and source-of-truth policy

This repository is in **paperization mode** for the canonical identification manuscript. Repository changes should improve reproducibility, clarity, or submission readiness without silently promoting historical analyses or the separate one-trait companion question into the active paper.

## 1. Canonical scientific source of truth

These files define the paper-facing scientific state.

### Manuscript

- `manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md` — sole active article text.
- `manuscript/IDENTIFICATION_DESIGN_REFERENCES.md` — focused reference spine.
- `manuscript/identification_figures/` — canonical main-figure sources.
- `manuscript/supplementary/SUPPLEMENT_IDENTIFICATION_DESIGN.md` — active Appendix S1.

`manuscript/MANUSCRIPT_THEORETICAL_ECOLOGY.md`, its earlier tables/figures, and the Leal/Sasidharan modules remain versioned for provenance and reproducibility. They do not define the current submission package.

### Scientific boundaries

- `docs/SUBMISSION_SCOPE.md` — active submission and inference boundary.
- `docs/PARTIAL_IDENTIFICATION_FRONTIER_V1.md` — identified-set and partial-bound derivation.
- `docs/MECHANISM_PATTERN_IDENTIFICATION_BRIDGE.md` — recurrence/identification bridge.
- `docs/HYPOTHESIS_RECOVERY_MAP.md` — audit of the historical one-trait target and its separation from BITA.
- `docs/QUESTION_METHOD_EXPLANATION_MATRIX.md` — which method answers which part of the two-trait question.
- `docs/PUBLICATION_MATERIAL_RECOVERY_LEDGER.md` — editorial state of Main, Appendix, evidence and remaining gates.

No historical readout, exploratory note, or old PR description overrides these files.

## 2. Reproduction-critical implementation

The core theory implementation is under `trait_architecture/`.

Primary paper-facing modules:

- `identification.py` — discrete crossed-intervention estimands and causal gates.
- `partial_identification.py` — identified sets and assumption-indexed bounds.
- `model.py` — declared biological parameterization and parameter constraints.
- `sign_criterion.py` — local sign logic and orientation-facing quantities.
- `robustness.py` — mixed-partial decomposition and response-shape robustness.
- `theory_evidence_interface.py` / `theory_meta_validation.py` — explicit theory-to-evidence boundary checks.

The current identification regressions include `tests/test_identification.py`, `tests/test_identification_four_way.py`, `tests/test_partial_identification.py`, and `tests/test_identification_coverage.py`. Historical theorem and robustness regressions remain active because Appendix S1 preserves those analyses under a lower claim ceiling.

Paper-facing generation and validation scripts under `scripts/` are retained when they reproduce a declared analysis, table, figure, supplement, source receipt, or validation state. Examples include:

- `run_part_i_robustness.py`
- `build_part_i_regime_figure_svg.py`
- `build_mechanism_coverage_audit.py`
- `build_empirical_mechanism_figure_svg.py`
- `build_pattern_expansion_readout.py`
- `run_leal_modern_estimator_sensitivity.py`
- Sasidharan reconstruction/adjudication scripts
- supplementary table/figure builders
- `export_manuscript_figures.sh`

## 3. Empirical evidence layers

`empirical/` contains evidence products at different inferential levels. They are intentionally not interchangeable.

### `empirical/mechanism_pattern_synthesis/`

This is the retained recurrence/provenance layer: route ledgers, source-adjudicated system audits, context/sign-switch records, saturation receipts, direct-design audits, and quantitative-module receipts. Its marginal routes establish recurrence and do not identify channel interactions.

### `empirical/identification_design/`

This is the active empirical identification layer: the 16-system high-information audit, direct interaction anchors, public-data retrofit, and source-package receipts.

`QUESTION_METHOD_EXPLANATION_MATRIX_V1.csv` is the machine-readable claim architecture linking each scientific question to its minimum information, current BITA evidence, claim ceiling and next valid gate.

### External one-trait companion

The historical one-trait shared-cue question, its coverage audit and its paper framework belong to [SCH](https://github.com/zuizui0223/sch). BITA retains source-adjudicated marginal routes only because they are constituent evidence for its two-trait decomposition.

### `empirical/broad_reality_evidence/`

This contains source recovery, screening, extraction, and provenance products developed before and during the final synthesis. It is retained because some canonical results are pinned to immutable historical commits and because the audit trail matters for reproducibility. It is **provenance**, not a competing manuscript source of truth.

### Other empirical directories

Other empirical directories may contain supporting or earlier calibration products. They can remain when tests, admitted evidence, or reproducibility depend on them, but they should not be cited as current scientific conclusions unless promoted through the canonical manuscript-facing evidence architecture.

## 4. What is deliberately removed from the main working path

One-off files whose only role was to mutate already-frozen manuscript prose or labels are not part of the scientific reproduction path. The paperization cleanup therefore removes completed manuscript-promotion/restructure/relabel scripts and their dedicated workflows.

Unrelated scratch analysis from another research programme is also removed from the repository root.

Git history remains the archive for those implementation steps. We do not preserve dead machinery merely because it once produced a manuscript revision.

## 5. Workflow policy

Keep a workflow active when it validates at least one of the following:

1. core theory or regression tests;
2. a canonical manuscript/supplement asset;
3. an admitted empirical reconstruction or source receipt;
4. a submission-facing reproducibility contract.

Do not keep a workflow active solely because it once rewrote prose, relabelled a frozen figure, or promoted an already-admitted Pattern batch.

Network-dependent source-audit workflows are provenance/validation tools, not the default research loop. Broad searching is not reopened unless a specific manuscript claim, reviewer request, or provenance gate requires it.

The two secondary-synthesis receipt reconstructions are exposed through one
read-only, manually dispatched workflow:
`.github/workflows/audit-secondary-synthesis-receipts.yml`. It uploads newly
generated receipts for inspection and never commits to a historical analysis
branch.

## 6. Graph-integrity policy

Repository organization follows a paper-spine dependency graph rather than file
type alone:

```text
canonical manuscript / tables / figures
    <- deterministic builders
    <- admitted theory or empirical inputs
    <- source receipts and declared provenance
    <- regression tests and read-only workflows
```

A file remains on the active graph when it is reachable from a canonical paper
asset or when the Supplement Manifest explicitly licenses it as provenance for an
admitted empirical module. A script that imports a retired local module, a
workflow that calls a missing script, or a workflow that writes to a retired
research branch is dead machinery rather than reproducibility infrastructure.

`tests/test_repository_graph_integrity.py` enforces those executable edges.
`tests/test_submission_scope.py` separately prevents retired scientific
architectures from returning.

## 7. Paperization change policy

From this point forward, proposed changes should be classified before implementation:

- **Editorial:** wording, flow, title/abstract, figure readability, references, submission metadata. Allowed if scientific claims and numbers are unchanged.
- **Reproducibility:** tests, deterministic builders, provenance receipts, source-of-truth documentation. Allowed if they preserve the frozen inference boundary.
- **Scientific correction:** change to an estimate, theorem, admitted evidence state, or inference boundary. Requires an explicit reason and revalidation of all downstream manuscript claims.
- **New discovery:** new broad search, new Pattern class, new model family, or new empirical programme. Out of scope for the current paper unless the frozen conclusion is actually falsified.

## 8. Current scientific endpoint for this paper

The canonical paper supports:

> **interaction detection → identified set → assumption-indexed partial identification → selective mechanism identification**

The four marginal channel families recur across independent systems, but the 16 screened high-information studies occupy fragmented faces of the identification frontier. No screened study point-identifies the full channel allocation or supplies an independent joint-cost assay. The historical one-sided result is retained as a partial-identification bound under an explicit non-negative joint-cost restriction, not as a standalone universal theorem.

The separate one-trait shared-cue question is not a missing section of this paper. It has its own estimand and coverage gate in SCH, while the source-adjudicated BITA routes remain preserved under their existing claim ceilings.
