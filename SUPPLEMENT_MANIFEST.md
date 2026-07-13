# Supplement manifest

This map links the one primary submission claim and its preliminary supporting context to the files needed to inspect or reproduce them.

## Primary claim: local attraction–defence interaction theory

Primary theory and assumptions:

- `docs/GENERAL_SIGN_CRITERION.md`
- `docs/NOVELTY_POSITIONING.md`
- `theory/README.md`
- `trait_architecture/sign_criterion.py`
- `tests/test_sign_criterion.py`

Implemented corollary and finite-set sensitivity analysis:

- `trait_architecture/model.py`
- `trait_architecture/robustness.py`
- `configs/part_i_robustness_grid.json`
- `scripts/run_part_i_robustness.py`
- `docs/PART_I_ROBUSTNESS_PROTOCOL.md`
- `tests/test_robustness.py`
- `tests/test_run_part_i_robustness.py`
- `tests/test_committed_part_i_results_current.py`

Canonical V2 outputs and manuscript-facing builders:

- `empirical/part_i_robustness/endpoint_normalized_grid_v2_report.json`
- `empirical/part_i_robustness/PART_I_SENSITIVITY_READOUT_V2.md`
- `scripts/build_part_i_manuscript_readout.py`
- `scripts/build_part_i_regime_figure_svg.py`
- `tests/test_build_part_i_manuscript_readout.py`
- `tests/test_build_part_i_regime_figure_svg.py`

Interpretive boundary:

- `P` and `H` are exogenous reference-regime indices.
- Environmental directional predictions depend on derivatives of all channel contributions, not on `P` or `H` alone.
- The non-negative relief/interference decomposition requires an explicit local orientation gate.
- Reproductive assurance `R` is an auxiliary background moderator in the implemented corollary, not a third focal trait.
- Reported percentages are unweighted occupancies of the declared finite grid, not empirical probabilities or prevalence estimates.
- `tested_set_unanimous` and `mixed_or_sensitive` are the only categorical finite-set agreement labels; `modal_sign_agreement` is continuous and no arbitrary majority threshold defines a third class.

## Preliminary literature context: collateral pollinator-cost route

Active route-level context:

- `empirical/broad_reality_evidence/broad_route_records.csv`
- `empirical/broad_reality_evidence/broad_effect_extractions.csv`
- `empirical/broad_reality_evidence/broad_meta_analysis_strata.csv`
- `empirical/broad_reality_evidence/LITERATURE_EVIDENCE_READOUT.md`

Reproduction and validation:

- `scripts/run_broad_meta_analysis.py`
- `scripts/validate_current_theory_meta.py`
- `trait_architecture/broad_meta_analysis.py`
- `trait_architecture/theory_meta_validation.py`
- `tests/test_theory_meta_validation.py`
- `.github/workflows/validate-current-theory-meta.yml`

All currently active directional records are coded from `crossref_deposited_abstract`. The relevant declared `B_to_pollination × chemical_barrier × pollinator_preference_or_foraging × manipulation` stratum contains three independent primary clusters, all coded negative. A separate `visitation_rate` stratum contains one mixed record and is not pooled into that three-cluster directional fraction.

The current quantitative extraction table contains no eligible effect rows, and the abstract-level registry has not undergone full-text verification and independent duplicate coding or documented adjudication. The literature layer is therefore **preliminary mechanism context only**. It is not a second independent submission claim, does not calibrate model parameters, and does not validate the regime map.

## Boundary between theory and literature context

- `README.md`
- `docs/SUBMISSION_SCOPE.md`
- `docs/FINAL_SUBMISSION_AUDIT.md`
- `scripts/validate_current_theory_meta.py`
- `trait_architecture/theory_meta_validation.py`
- `tests/test_submission_scope.py`
- `tests/test_submission_narrative_contract.py`

A negative `D -> pollinator use` route does not by itself identify the focal mutualist mixed curvature `M_AD < 0`; that would require showing how `D` changes the marginal mutualist return to the same focal `A`. Route records from different traits and taxa also do not jointly estimate one system-specific `D` axis, the complete local `A`–`D` mixed partial, its environmental derivative, trait covariance, or an evolutionary endpoint.

## Deliberately absent

Raw third-party observations, the former *Impatiens capensis* case-study pipeline, optimum/covariance analyses, matched-study discovery architecture, network/trait-coverage audits, regime-discrimination audits based on abstract-level direction records, exploratory candidate scouting, repository-access probes, broad candidate-harvesting machinery, and superseded manuscript-planning files are not part of this supplement. Git history is the archive for those earlier branches.
