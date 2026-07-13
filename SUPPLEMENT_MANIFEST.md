# Supplement manifest

This map links each submission claim to the files needed to inspect or reproduce it.

## Claim 1: regime-scaled attraction–defence interaction

Primary theory:

- `docs/GENERAL_SIGN_CRITERION.md`
- `docs/NOVELTY_POSITIONING.md`
- `trait_architecture/sign_criterion.py`
- `tests/test_sign_criterion.py`

Implemented corollary and sensitivity analysis:

- `trait_architecture/model.py`
- `trait_architecture/robustness.py`
- `configs/part_i_robustness_grid.json`
- `scripts/run_part_i_robustness.py`

Manuscript-facing outputs:

- `scripts/build_part_i_manuscript_readout.py`
- `scripts/build_part_i_regime_figure_svg.py`
- `docs/PART_I_ROBUSTNESS_PROTOCOL.md`
- `empirical/part_i_robustness/`

Automated guard:

- `.github/workflows/validate-current-theory-meta.yml`
- theory and figure tests under `tests/`

The primary directional prediction is conditional: with locally comparable positive relief and interference rates, increasing antagonist pressure raises `W_AD`, while increasing mutualist service lowers `W_AD` when defence interferes with attraction-mediated mutualist return.

## Claim 2: a defence/access -> pollination cost occurs in at least some systems

Registered evidence and outputs:

- `empirical/broad_reality_evidence/broad_route_records.csv`
- `empirical/broad_reality_evidence/broad_effect_extractions.csv`
- `empirical/broad_reality_evidence/broad_meta_analysis_strata.csv`
- `empirical/broad_reality_evidence/part_b_arrow_effects.csv`
- `empirical/broad_reality_evidence/PART_B_RESULTS_READOUT_v1.md`

Validation:

- `scripts/run_broad_meta_analysis.py`
- `scripts/validate_part_b_integrity.py`
- `.github/workflows/part-b-integrity.yml`

## Boundary between the two claims

- `scripts/validate_current_theory_meta.py`
- `scripts/audit_current_regime_discrimination.py`
- `trait_architecture/theory_meta_validation.py`
- `trait_architecture/regime_discrimination_audit.py`
- `docs/SUBMISSION_SCOPE.md`

The literature records support the plausibility of one ingredient of mutualist interference. They do not estimate the complete local curvature, the regime-scaled comparative statics, or the prevalence of complementarity versus substitutability in nature.

## Deliberately absent

Raw third-party observations, the former *Impatiens capensis* case-study pipeline, exploratory candidate discovery, repository-access probes, and superseded manuscript drafts are not part of this supplement.
