# Supplement manifest

This map links the primary submission claim and its supporting context to the files needed to inspect or reproduce them.

## Primary claim: local attraction–defence interaction theory

Primary theory and assumptions:

- `docs/GENERAL_SIGN_CRITERION.md`
- `docs/NOVELTY_POSITIONING.md`
- `theory/README.md`
- `trait_architecture/sign_criterion.py`
- `tests/test_sign_criterion.py`

Implemented baseline corollary and finite-set sensitivity analysis:

- `trait_architecture/model.py`
- `trait_architecture/robustness.py`
- `configs/part_i_robustness_grid.json`
- `scripts/run_part_i_robustness.py`
- `docs/PART_I_ROBUSTNESS_PROTOCOL.md`

Manuscript-facing theory outputs:

- `scripts/build_part_i_manuscript_readout.py`
- `scripts/build_part_i_regime_figure_svg.py`
- `empirical/part_i_robustness/`

Automated guard:

- `.github/workflows/validate-current-theory-meta.yml`
- theory and figure tests under `tests/`

The environmental comparative statics are conditional. `P` and `H` are exogenous reference-regime indices, and the directional effect of changing them depends on the local derivatives of the ecological channel scaling and any regime dependence of direct cross-cost.

The non-negative mechanism-magnitude decomposition is also conditional on an orientation gate. The focal trait labels alone do not guarantee `M_AD <= 0`, `G_AD <= 0`, or `C_AD >= 0`.

The implemented baseline also contains reproductive assurance `R` as an auxiliary background moderator of the pollination-mediated channel. `R` is not a third focal trait in the submission claim, and the manuscript must not present the sensitivity grid as a three-trait theory.

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
- `.github/workflows/validate-current-theory-meta.yml`

All currently active directional records are coded from `crossref_deposited_abstract`. The relevant declared `B_to_pollination × chemical_barrier × pollinator_preference_or_foraging × manipulation` stratum contains three independent primary clusters, all coded negative. A separate `visitation_rate` stratum contains one mixed record and is not pooled into that three-cluster directional fraction.

The current quantitative extraction table contains no eligible effect rows, and the abstract-level registry has not undergone full-text verification and independent duplicate coding or documented adjudication. The literature layer therefore does **not** constitute a second independent submission claim, calibrate effect magnitudes or model parameters, or validate the complete regime map. Its present role is preliminary mechanism context only.

## Boundary between theory and literature context

- `docs/SUBMISSION_SCOPE.md`
- `scripts/validate_current_theory_meta.py`
- `trait_architecture/theory_meta_validation.py`

A negative `D -> pollinator use` route does not by itself identify the focal mutualist mixed curvature `M_AD < 0`; that would require showing how `D` changes the marginal mutualist return to the same focal `A`. Route records from different traits and taxa also do not jointly estimate one system-specific `D` axis, the complete local `A`–`D` mixed partial, its environmental derivative, trait covariance, or an evolutionary endpoint.

## Deliberately absent

Raw third-party observations, the former *Impatiens capensis* case-study pipeline, optimum/covariance analyses, matched-study discovery architecture, network/trait-coverage audits, exploratory candidate scouting, repository-access probes, and superseded manuscript-planning machinery are not part of this supplement.
