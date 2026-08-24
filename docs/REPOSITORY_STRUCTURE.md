# Repository structure and source-of-truth policy

This repository has entered **paperization mode**. The scientific conclusion is frozen at the Mechanism → Pattern boundary carried by `main`; repository changes should now improve reproducibility, clarity, or submission readiness without reopening broad discovery by default.

## 1. Canonical scientific source of truth

These files define the paper-facing scientific state.

### Manuscript

- `manuscript/MANUSCRIPT_THEORETICAL_ECOLOGY.md` — canonical article text.
- `manuscript/TABLES_THEORETICAL_ECOLOGY.md` — canonical main tables.
- `manuscript/figures/` — canonical main-figure sources.
- `manuscript/supplementary/` — canonical supplementary text, figures, and tables.

### Scientific boundaries

- `docs/MECHANISM_PATTERN_STORY_BOUNDARY.md` — frozen integrated conclusion.
- `docs/NOVELTY_POSITIONING.md` — what is and is not claimed as novel.
- `docs/SELECTIVITY_WINDOW_BOUND.md` — one-sided theorem, finite verification, and falsification gate.
- `docs/PART_I_ROBUSTNESS_PROTOCOL.md` and `configs/part_i_robustness_grid.json` — declared finite-design contract.

No historical readout, exploratory note, or old PR description overrides these files.

## 2. Reproduction-critical implementation

The core theory implementation is under `trait_architecture/`.

Primary paper-facing modules:

- `model.py` — declared biological parameterization and parameter constraints.
- `sign_criterion.py` — local sign logic and orientation-facing quantities.
- `robustness.py` — mixed-partial decomposition and response-shape robustness.
- `theory_evidence_interface.py` / `theory_meta_validation.py` — explicit theory-to-evidence boundary checks.

The main theorem regression is `tests/test_selectivity_bound.py`. Core CI must continue to discover and run it.

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

This is the primary Part II paper-facing evidence layer: route ledgers, source-adjudicated system audits, context/sign-switch records, saturation receipts, direct-design audits, and quantitative-module receipts.

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

## 8. Frozen scientific endpoint for this paper

The paper supports:

> **a one-sided mechanistic theorem plus a recurrent but context-dependent empirical Pattern**

Under non-negative joint-cost curvature, complementarity cannot occur outside the selectivity window. The window is not sufficient for complementarity. Antagonist exposure can open the relief opportunity on average but is heterogeneous among systems. Direct joint-cost curvature remains unmeasured, and sufficiently negative joint-cost curvature is the unique escape route from the one-sided bound in the declared functional family.

The next empirical work is therefore generated by the paper rather than required to complete it: first test the sign of the joint-cost interaction with a 2 × 2 allocation design; then, separately, use a full `A × D` factorial to estimate total interaction and channel allocation.
