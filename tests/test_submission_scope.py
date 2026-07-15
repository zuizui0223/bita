from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


RETIRED_PATHS = [
    # Former empirical case study.
    ".github/workflows/run-impatiens-empirical-core.yml",
    "configs/impatiens_capensis_four_path_models.json",
    "configs/impatiens_response_scale_models.json",
    "configs/impatiens_randomized_fitness_models.json",
    "trait_architecture/impatiens_models.py",
    "trait_architecture/impatiens_response_scale_models.py",
    "trait_architecture/impatiens_factorial_fitness_models.py",
    # Optimum/covariance branch.
    "trait_architecture/regime_map.py",
    "trait_architecture/stability.py",
    "tests/test_regime_map.py",
    "tests/test_stability.py",
    "examples/regime_map.py",
    # Superseded duplicate and matched-study architectures.
    "trait_architecture/ad_interaction_condition.py",
    "tests/test_ad_interaction_condition.py",
    "trait_architecture/matched_regime_registry.py",
    "tests/test_matched_regime_registry.py",
    # Retired global network / trait coverage route.
    "trait_architecture/network_audit.py",
    "tests/test_network_audit.py",
    "examples/audit_network_backbone.py",
    "scripts/probe_wol_orientation.py",
    "scripts/prepare_try_wol_request.py",
    "trait_architecture/trait_coverage_audit.py",
    "tests/test_trait_coverage_audit.py",
    "examples/audit_trait_receipt_coverage.py",
    # Retired four-path registry and synthesis layer.
    "trait_architecture/four_path_effects.py",
    "trait_architecture/effect_synthesis.py",
    "scripts/synthesise_four_path_effects.py",
    "examples/audit_four_path_effects.py",
    "tests/test_four_path_effects.py",
    "tests/test_effect_synthesis.py",
    "tests/test_gymnadenia_effect_registration.py",
    "configs/four_path_parameter_envelope_contracts.json",
    "empirical/four_path_effects/FOUR_PATH_EFFECT_PROTOCOL.md",
    # Retired layered Part B machinery and legacy effect anchors.
    "empirical/broad_reality_evidence/part_b_arrow_effects.csv",
    "empirical/broad_reality_evidence/PART_B_RESULTS_READOUT_v1.md",
    "scripts/run_part_b_support.py",
    "scripts/validate_part_b_integrity.py",
    "trait_architecture/part_b_pipeline.py",
    "trait_architecture/part_b_support.py",
    "trait_architecture/part_b_moderator.py",
    "trait_architecture/part_b_arrow_evidence.py",
    ".github/workflows/part-b-pipeline.yml",
    ".github/workflows/part-b-integrity.yml",
    "configs/part_b_break_even_scenarios.json",
    "configs/part_b_moderator_hypotheses.json",
    "configs/part_b_arrow_literature_seeds.json",
    "docs/PART_B_MECHANISM_META_STRATEGY_v1.md",
    "docs/PART_B_C0_CURRENT_READOUT_V1.md",
    # Retired attempt to use abstract-level direction records to discriminate regimes.
    "scripts/audit_current_regime_discrimination.py",
    "trait_architecture/regime_discrimination_audit.py",
    "tests/test_regime_discrimination_audit.py",
    "empirical/part_i_robustness/CURRENT_EVIDENCE_REGIME_DISCRIMINATION_PROTOCOL.md",
    # Superseded Part I V1 artifacts.
    "docs/PART_I_MANUSCRIPT_READOUT_V1.md",
    "empirical/part_i_robustness/INITIAL_GRID_READOUT.md",
    "empirical/part_i_robustness/initial_grid_report.json",
]


REQUIRED_ACTIVE_PATHS = [
    "README.md",
    "SUPPLEMENT_MANIFEST.md",
    "docs/SUBMISSION_SCOPE.md",
    "docs/GENERAL_SIGN_CRITERION.md",
    "docs/NOVELTY_POSITIONING.md",
    "docs/BACKGROUND_NOVELTY_GAP_REVIEW.md",
    "docs/PART_I_ROBUSTNESS_PROTOCOL.md",
    "theory/README.md",
    "configs/part_i_robustness_grid.json",
    "trait_architecture/model.py",
    "trait_architecture/sign_criterion.py",
    "trait_architecture/robustness.py",
    "scripts/run_part_i_robustness.py",
    "scripts/build_part_i_manuscript_readout.py",
    "scripts/build_part_i_regime_figure_svg.py",
    "empirical/part_i_robustness/endpoint_normalized_grid_v2_report.json",
    "empirical/part_i_robustness/PART_I_SENSITIVITY_READOUT_V2.md",
    "empirical/broad_reality_evidence/broad_route_records.csv",
    "empirical/broad_reality_evidence/broad_effect_extractions.csv",
    "empirical/broad_reality_evidence/broad_meta_analysis_strata.csv",
    "empirical/broad_reality_evidence/LITERATURE_EVIDENCE_READOUT.md",
    "scripts/run_broad_meta_analysis.py",
    "scripts/validate_current_theory_meta.py",
]


def test_retired_exploratory_paths_do_not_return() -> None:
    for relative in RETIRED_PATHS:
        assert not (ROOT / relative).exists(), relative


def test_current_submission_spine_is_present() -> None:
    for relative in REQUIRED_ACTIVE_PATHS:
        assert (ROOT / relative).exists(), relative
