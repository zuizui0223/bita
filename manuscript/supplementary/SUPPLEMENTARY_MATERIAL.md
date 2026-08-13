# Supplementary material — Mechanism → Pattern paper

This reader-facing supplement belongs to the saturated 25-system candidate on PR #129. It preserves the same inference boundary as the main manuscript: finite-grid occupancy is not empirical prevalence; marginal or same-system route evidence is not a direct estimate of `W_AD`; zero strict joint-cost estimates means `kappa` is unidentified, not zero.

## Supplementary Figures

**Fig. S1** Analytic versus finite-difference implementation check for the local mixed partial. All 2,592 declared endpoint-normalized sensitivity evaluations are plotted by response-shape variant. The numerical check uses a central finite difference with step `1e-5`; the figure reports the maximum absolute analytic-versus-numerical discrepancy for each response shape. This is a software/numerical verification, not empirical validation of the model.

**Fig. S2** Scenario-specific mechanistic sign maps separated by endpoint-normalized response-shape variant. Each cell gives the unweighted fraction of complementary evaluations across the declared `A × D × R` coordinates for a fixed biological scenario, response shape, pollinator-service index `P`, and antagonist-pressure index `H`. Fractions describe occupancy of the finite declared grid, not prevalence in nature.

**Fig. S3** Same-system route architecture across the saturated evidence universe. Rows are the 14 independent biological clusters with at least two linked marginal route families, or an explicit same-system linkage retained by the evidence audit. Filled cells indicate categorical route presence only; they are not effect sizes and do not constitute direct `A × D` evidence.

**Fig. S4** Module-specific quantitative robustness. Panel A reports the three informative Leal et al. (2025) pooled log-response-ratio patterns together with retained extreme heterogeneity and the declared leave-one-cluster-out direction stability. Panel B reports the Sasidharan et al. (2023) assembled physiological-detection contrast and the minimum, median, and maximum leave-one-study-component-out contrasts. The two panels retain different metrics and dependence structures and are not pooled into one effect.

Canonical SVG targets:

```text
manuscript/supplementary/figures/FIGURE_S1_DERIVATIVE_AGREEMENT.svg
manuscript/supplementary/figures/FIGURE_S2_SCENARIO_SIGN_MAPS.svg
manuscript/supplementary/figures/FIGURE_S3_SAME_SYSTEM_ROUTE_MATRIX.svg
manuscript/supplementary/figures/FIGURE_S4_QUANTITATIVE_ROBUSTNESS.svg
```

## Supplementary Tables

The following numbering is frozen for the submission package. Machine-readable CSV views must preserve the authoritative source identifiers rather than replace the underlying ledgers.

**Table S1. Complete parameter definitions, finite-grid coordinates, biological scenarios, response-shape parameters, scaling, and numerical tolerance.** Authoritative sources: `configs/part_i_robustness_grid.json`, `trait_architecture/model.py`, and `trait_architecture/robustness.py`.

**Table S2. All 162 local phenotype × ecological-context cases and their classifications across the deliberately heterogeneous full tested set.** Generated directly by `scripts/run_part_i_robustness.py` as `part_i_full_tested_set_summary.csv`; the associated 2,592 evaluation rows remain available as the reproducibility source.

**Table S3. Full source-adjudicated mechanism/Pattern route ledger.** Concatenates the five canonical ledger files plus the six admitted expansion ledgers with a `source_file` provenance field. Required package state: 56 route records across 25 independent biological clusters. Route counts overlap.

**Table S4. Conditionality and context architecture.** Combines the canonical and expansion sign-switch ledgers with the seven context-only programs while retaining `record_type` and `source_file`. Required package state: 17 independent sign/context-switch clusters plus 7 context-only programs; context-only programs are excluded from route-ledger N.

**Table S5. Direct-identification audits.** Presents the direct `A × D` audit and direct joint-cost audit as two labeled audit families without forcing their different eligibility schemas into an effect-size meta-analysis. The admitted state remains one strict sign-unresolved direct `A × D` cluster and zero strict direct joint-cost estimates.

**Table S6. Pattern-expansion screening and registered stopping batches.** Preserves batch/source/decision/reason fields from the priority-rescreen sequence. Batch 7 introduced a new lifecycle-stage role-reversal class and reset the stopping counter; Batches 8 and 9 yielded no new admissible Pattern class, satisfying the registered stopping rule.

## Quantitative-module source boundary

Leal et al. (2025) is pinned to immutable repository commit `ed33b25593c0d90ad6657753f6f5501d9efc7b82`. Sasidharan et al. (2023) uses the current-branch 32-study-component reconstruction. Haas-Desmarais et al. (2026), Caruso et al. (2019), and Junker & Blüthgen (2010) remain secondary contextual/cross-synthesis modules rather than co-equal locally reproduced meta-analyses.

## Final-render rule

The SVG and CSV sources can be generated and regression-tested before author metadata are supplied. The final reader-facing supplementary PDF should be rendered only after the manuscript wording, author-controlled declarations, repository licence, release commit, and final numbering are frozen. The final PDF must cite the exact release commit and archive DOI used for submission.
