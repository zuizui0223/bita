# Supplement manifest — canonical Mechanism → Pattern paper

This manifest maps the **current main-line submission package** for the paper:

> **When are floral attraction and defence complementary? A one-sided mechanistic bound and cross-system patterns**

Historical PR and branch chronology remains in Git history. No historical branch overrides the canonical manuscript, claim freeze, current builders, or current submission checklist.

## 1. Canonical paper and one-sided theoretical core

Primary reader-facing sources:

- `manuscript/MANUSCRIPT_THEORETICAL_ECOLOGY.md`
- `manuscript/TABLES_THEORETICAL_ECOLOGY.md`
- `manuscript/CLAIM_FREEZE.md`
- `docs/MECHANISM_PATTERN_STORY_BOUNDARY.md`
- `docs/NOVELTY_POSITIONING.md`
- `docs/SELECTIVITY_WINDOW_BOUND.md`
- `docs/REPOSITORY_STRUCTURE.md`
- `submission/SUBMISSION_CHECKLIST.md`

Theory implementation and declared finite design:

- `trait_architecture/model.py`
- `trait_architecture/sign_criterion.py`
- `trait_architecture/robustness.py`
- `configs/part_i_robustness_grid.json`
- `scripts/run_part_i_robustness.py`
- `docs/PART_I_ROBUSTNESS_PROTOCOL.md`
- `tests/test_selectivity_bound.py`

The signed identity is bookkeeping:

```text
W_AD = rho - iota - kappa
```

The strongest structural claim is one-sided:

```text
W_AD > 0  =>  rho > iota     when kappa >= 0
```

Across the declared 2,592 evaluations, the forward implication has zero counterexamples. The converse is false: window precision is 77.2%, so approximately 23% of in-window evaluations remain substitutable. At `kappa = 0`, the window and sign criterion coincide exactly.

Finite-grid occupancies are declared-design sensitivities, not probabilities or prevalence in nature.

## 2. Mechanism → Pattern protocol and saturation

Primary empirical architecture:

- `docs/MECHANISM_PATTERN_UNIVERSALITY_PROTOCOL_V1.md`
- `empirical/mechanism_pattern_synthesis/COMPLETION_GATE_V1.md`
- `empirical/mechanism_pattern_synthesis/COMPLETION_STATUS_V2.md`
- `empirical/mechanism_pattern_synthesis/SEARCH_REGISTRY_V1.csv`
- `empirical/mechanism_pattern_synthesis/MASTER_LEDGER_SCHEMA_V1.csv`
- canonical `MASTER_LEDGER` / `LEDGER_BATCH_*` files
- `EXPANSION_LEDGER_BATCH_*_V1.csv`
- `EXPANSION_SIGN_SWITCH_BATCH_*_V1.csv`
- `EXPANSION_CONTEXT_PROGRAMS_V1.csv`
- `CROSS_MODULE_PATTERN_MATRIX_V2.csv`
- `PATTERN_MODULE_REGISTRY_V2.csv`
- `PATTERN_EXPANSION_READOUT_V1.md/json`
- `PATTERN_EXPANSION_COMPLETION_GATE_V1.md`
- registered `PRIORITY_RESCREEN_BATCH_*_V1.csv` files

The expansion targeted theory-facing Pattern classes rather than article count. After a lifecycle-stage role-reversal class reset the stopping counter, two subsequent distinct targeted batches produced no new admissible Pattern class; a parallel quantitative search produced no additional synthesis with a distinct theory-facing axis.

The empirical endpoint is **recurrent constituent mechanisms + context-dependent balance inside a moving permissive window**, not a pooled estimate of the mixed partial.

## 3. Saturated route-ledger architecture

Canonical manuscript-facing state:

```text
56 source-adjudicated effect/directional records
25 independent biological study clusters
A -> pollination:       5 clusters
A -> antagonism:        8
D -> antagonism:       18
D -> pollination:      10
same-system:           14 clusters
context/sign switch:   17 clusters
context-only programs:  7, excluded from route-ledger N
```

Route counts overlap and are not additive independent-study totals or prevalence estimates.

## 4. Direct interaction and same-system evidence

Direct `A × D` evidence:

- `empirical/mechanism_pattern_synthesis/DIRECT_AXD_AUDIT_V1.csv`
- `DIRECT_AXD_SEARCH_EXPANSION_READOUT_V1.md`
- `DIRECT_AXD_SATURATION_RECEIPT_V1.md`

The one strict total reproductive-outcome cluster, *Impatiens capensis*, remains sign-unresolved across reproductive components.

Same-system architecture:

- `SAME_SYSTEM_REGIME_PROTOCOL_V1.md`
- `SAME_SYSTEM_REGIME_LEDGER_V1.csv`
- `SAME_SYSTEM_REGIME_READOUT_V1.md`
- later `EXPANSION_LEDGER_BATCH_*_V1.csv` files that add linked routes.

Same-system marginal co-occurrence is never relabelled as direct `A × D` evidence.

## 5. Conditionality and context architecture

Canonical inputs:

- `SIGN_SWITCH_LEDGER_V1.csv`
- `EXPANSION_SIGN_SWITCH_BATCH_*_V1.csv`
- `EXPANSION_CONTEXT_PROGRAMS_V1.csv`
- `CONDITIONALITY_ONTOLOGY_V1.md`
- `CROSS_MODULE_PATTERN_MATRIX_V2.csv`

The saturated state contains 17 independent sign/state-switch clusters plus seven context-only programs. Recurrent states include trait intensity, resource/exposure, consumer identity and functional role, response stage/scale, compound/mechanism identity, guarded defence, spatial/temporal/attack-mode filtering, visitor functional-mode routing, lifecycle-stage role reversal, and population/site or trait-class dependence.

Incompatible response constructs are not forced into a cross-outcome grand moderator coefficient.

## 6. Direct joint-cost evidence state

- `JOINT_COST_SEARCH_PROTOCOL_V1.md`
- `JOINT_COST_AUDIT_V1.csv`
- `JOINT_COST_READOUT_V1.md`
- `JOINT_COST_SATURATION_RECEIPT_V1.md`

Strict simultaneous A+D intrinsic-cost estimates remain zero in the admitted evidence layer. `kappa` is therefore unidentified, not estimated as zero.

Under the one-sided theorem, outside-window complementarity requires negative joint-cost curvature, and an observed violation requires it to be sufficiently negative relative to the relief-interference difference. The sign of joint-cost curvature is therefore the minimal empirical applicability/falsification gate for a focal trait pair.

## 7. Reproduced quantitative synthesis module 1 — Leal et al. 2025 floral larceny

The completed module is included directly in the canonical repository tree and is pinned to immutable provenance.

Admitted manuscript values remain:

```text
female reproductive success  LRR -0.210  48 independent clusters
nectar standing crop          LRR -0.483  28
legitimate visitation         LRR -0.291  22
```

For female fitness, 35/48 clusters are negative and the 95% prediction interval spans approximately `-1.13` to `+0.71`. Declared moderators explain only 0–8% of heterogeneity.

The reward → visitation → female-fitness sequence is retained as constituent-path evidence, not a demonstrated within-study mechanism chain.

## 8. Reproduced quantitative synthesis module 2 — Sasidharan et al. 2023 FVOCs

Canonical adjudication is `PASS_AS_DEPOSITED_REANALYSIS`. The conservative 32-study-component citation topology remains the dependence source of record. Physiological detection is 84/103 for florivore units and 151/220 for pollinator units; the assembled risk difference is `+0.129` and remains positive in 32/32 leave-one-component-out refits.

Only three study components contain both physiological consumer roles and all three paired differences are zero, so the assembled contrast is not treated as a causal within-study role effect.

## 9. Secondary contextual/cross-synthesis modules

These modules broaden Pattern recurrence without being pooled with Leal/Sasidharan. **Secondary-synthesis counts are not added to route-ledger N**.

- Haas-Desmarais et al. 2026: 171 studies / 1,348 study cases; supplement package independently retrieved and hashed; herbivory is not relabelled as focal floral `D`.
- Caruso et al. 2019: 755 directional selection gradients with SE from 36 articles; current raw file-byte access remains an access-layer limitation rather than a biological null.
- Junker & Blüthgen 2010: 18 publications / 425 observations; visitor dependence on floral resources is not equated with pollinator-versus-antagonist identity.

## 10. Robustness and theory–empiricism boundary

Primary boundary records:

- `SYNTHESIS_ROBUSTNESS_AUDIT_V1.md`
- `THEORY_EMPIRICISM_BOUNDARY_AUDIT_V1.md`
- `manuscript/CLAIM_FREEZE.md`

Required boundaries include:

- marginal routes do not estimate `W_AD`;
- same-system evidence does not equal direct total `A × D`;
- context programs are not extra route-ledger N;
- secondary-synthesis counts are not added to route-ledger N;
- screened/deposited fractions are not prevalence;
- finite-grid occupancy is not prevalence;
- one direct interaction is not generalized to a universal sign;
- incompatible outcomes are not averaged into a grand mean;
- absence of a strict joint-cost estimate does not imply `kappa = 0`;
- herbivory treatment does not become focal floral `D` by relabelling.

## 11. Canonical figures, tables, supplement, and callouts

### Final Main figures

The manuscript-facing final numbering is:

1. `FIGURE_1_MECHANISTIC_ARCHITECTURE.svg` — mechanistic architecture and inference boundary.
2. `FIGURE_2_THEORY_REGIME_MAP.svg` — finite theory regime / selectivity-window result.
3. `FIGURE_3_EMPIRICAL_MECHANISM_ARCHITECTURE.svg` — cross-system Pattern architecture.
4. Final **Fig. 4** uses the frozen quantitative evidence / identification-boundary source currently stored as `manuscript/figures/FIGURE_5_QUANTITATIVE_IDENTIFICATION_BOUNDARY.svg`.
5. Final **Fig. 5** uses the 14-cluster same-system route-matrix source currently stored as `manuscript/supplementary/figures/FIGURE_S3_SAME_SYSTEM_ROUTE_MATRIX.svg`.

The historical `FIGURE_4_MECHANISM_PATTERN_OVERVIEW.svg` is not part of the final Main Document because it is reader orientation only and adds no new scientific result.

### Final Appendix S1 figures

- **Figure S1:** `FIGURE_S1_DERIVATIVE_AGREEMENT.svg` — analytic versus finite-difference implementation check.
- **Figure S2:** `FIGURE_S2_SCENARIO_SIGN_MAPS.svg` — detailed scenario × response-shape sign maps.
- **Figure S3:** `FIGURE_S4_QUANTITATIVE_ROBUSTNESS.svg` — quantitative robustness/sensitivity source, renumbered reader-facing as S3 after promotion of the same-system matrix to Main Fig. 5.

Canonical supplementary Tables S1–S6 remain machine-readable products and are represented in the Open Research package rather than uploaded as spreadsheet Supporting Information.

The final manuscript contains explicit callouts for Figures 1–5, Tables 1–4, Appendix S1 Figures S1–S3, and the relevant Open Research products.

Active reproducibility contracts now:

- reproduce the 2,592-evaluation theory state and diff committed Figure 2;
- regenerate Figure 3 from the saturated ledgers;
- regenerate the result-first Fig. 4/5 scientific sources;
- rebuild Appendix S1 Figures S1–S3 and Tables S1–S6 from frozen sources;
- export and validate submission-form EPS files `Fig1.eps` through `Fig5.eps`;
- build and render the Ecology review package and fail if the Main Document exceeds 50 pages.

The current pre-metadata review render is **48 Main pages + 5 Appendix pages**. Final manual visual QA found no clipping, overflow, broken glyphs, or missing figure content.

## 12. Deliberately not promoted

The current submission does not promote:

- route or publication counts to biological prevalence;
- finite-grid regime fractions to natural frequencies;
- cross-organ or whole-inflorescence defence to strict flower-specific `D` without the organ gate;
- herbivory or simulated damage to focal `D`;
- a dual-function single trait to an independently varied A+D design;
- unrelated marginal studies to a constructed mixed partial;
- Caruso to a locally reproduced raw-effect analysis while file bytes remain inaccessible;
- Haas-Desmarais to a local raw-effect reanalysis merely because its supplement package was verified;
- zero joint-cost evidence to `kappa = 0`.

## 13. Release and submission boundary

The **science and machine-controlled review-package engineering are complete** for the present claim set.

External submission is now blocked only by human-controlled metadata and sign-off:

- final author order/publication names;
- affiliations, corresponding author/email, and ORCIDs;
- final CRediT roles, funding, acknowledgments, and competing-interest statement;
- repository/software/data licence statement where applicable;
- all-author approval and no-simultaneous-consideration confirmation;
- reviewer/opposed-reviewer entries only if requested by the live ScholarOne portal.

After those fields are inserted, rebuild the exact review package, rerun all normal validation workflows, confirm the Main Document remains ≤50 pages, visually inspect the complete Main Document and Appendix S1, and confirm the portal fields match the frozen files before submission.

A permanent archive DOI is **not an initial-submission blocker**. At acceptance, freeze the accepted exact data/code version in a permanent versioned archive and insert the archival citation/DOI required for publication.
