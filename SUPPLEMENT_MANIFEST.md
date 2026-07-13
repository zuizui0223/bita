# Supplement manifest

This map links each submission claim to the files needed to inspect or reproduce it.

## Claim 1: local attraction–defence interaction theory

Primary theory and assumptions:

- `docs/GENERAL_SIGN_CRITERION.md`
- `docs/NOVELTY_POSITIONING.md`
- `theory/README.md`
- `trait_architecture/sign_criterion.py`
- `tests/test_sign_criterion.py`

Implemented baseline corollary and sensitivity analysis:

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

## Claim 2: a flower-specific defence/barrier can reduce pollinator use

Active route-level evidence:

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

The current quantitative extraction table contains no eligible effect rows, so the evidence layer does **not** calibrate effect magnitudes or model parameters. Its present contribution is restricted directional support for mechanism plausibility in declared route strata.

## Boundary between the two claims

- `docs/SUBMISSION_SCOPE.md`
- `scripts/validate_current_theory_meta.py`
- `trait_architecture/theory_meta_validation.py`

Route records from different traits and taxa can establish that a pathway is biologically possible. They do not jointly estimate one system-specific `D` axis, the complete local `A`–`D` mixed partial, its environmental derivative, trait covariance, or an evolutionary endpoint.

## Deliberately absent

Raw third-party observations, the former *Impatiens capensis* case-study pipeline, optimum/covariance analyses, matched-study discovery architecture, network/trait-coverage audits, exploratory candidate scouting, repository-access probes, and superseded manuscript-planning machinery are not part of this supplement.
