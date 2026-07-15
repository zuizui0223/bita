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
    "empirical/matched_flower_regime",
    # Retired global network / trait coverage route.
    "trait_architecture/network_audit.py",
    "tests/test_network_audit.py",
    "examples/audit_network_backbone.py",
    "scripts/probe_wol_orientation.py",
    "scripts/prepare_try_wol_request.py",
    "trait_architecture/trait_coverage_audit.py",
    "tests/test_trait_coverage_audit.py",
    "examples/audit_trait_receipt_coverage.py",
    # Retired four-path, functional-trait, and leaf-resource branches.
    "trait_architecture/four_path_effects.py",
    "trait_architecture/effect_synthesis.py",
    "scripts/synthesise_four_path_effects.py",
    "examples/audit_four_path_effects.py",
    "tests/test_four_path_effects.py",
    "tests/test_effect_synthesis.py",
    "tests/test_gymnadenia_effect_registration.py",
    "configs/four_path_parameter_envelope_contracts.json",
    "empirical/four_path_effects",
    "empirical/functional_traits",
    "empirical/megachile_leaf_resource",
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
    # Retired discovery, source-resolution, and meta-intake infrastructure.
    "empirical/broad_reality_evidence/precision_expansions",
    "empirical/broad_reality_evidence/meta_analysis_intake",
    "trait_architecture/b_flower_mechanism_triage.py",
    "trait_architecture/b_to_p_precision_batch.py",
    "trait_architecture/broad_abstract_evidence_map.py",
    "trait_architecture/broad_abstract_label_audit.py",
    "trait_architecture/broad_abstract_corpus.py",
    "trait_architecture/broad_source_screening.py",
    "trait_architecture/castilleja_access_probe.py",
    "trait_architecture/declared_figshare_image_manifest.py",
    "trait_architecture/declared_figshare_receipts.py",
    "trait_architecture/declared_figshare_xlsx_headers.py",
    "trait_architecture/floral_trait_animal_response_meta.py",
    "trait_architecture/functional_trait_matrix.py",
    "trait_architecture/hierarchical_evidence_synthesis.py",
    "trait_architecture/high_information_access_probe.py",
    "trait_architecture/meta_analysis_intake.py",
    "trait_architecture/parameter_envelopes.py",
    "trait_architecture/public_article_source_scout.py",
    "trait_architecture/public_dataset_link_validation.py",
    "trait_architecture/public_repository_resolver.py",
    "scripts/build_b_flower_mechanism_triage.py",
    "scripts/build_b_to_p_precision_batch.py",
    "scripts/build_broad_abstract_theory_map.py",
    "scripts/build_broad_abstract_label_audit.py",
    "scripts/summarize_broad_abstract_label_audit.py",
    "scripts/build_broad_calibration_batch.py",
    "scripts/build_broad_calibration_abstract_packet.py",
    "scripts/build_broad_source_screening_matrix.py",
    "scripts/build_meta_analysis_intake.py",
    "scripts/resolve_public_repository_receipts.py",
    "scripts/resolve_declared_figshare_receipts.py",
    "scripts/audit_declared_figshare_image_manifests.py",
    "scripts/audit_declared_figshare_xlsx_headers.py",
    ".github/workflows/build-floral-trait-animal-response-meta.yml",
    ".github/workflows/build-broad-abstract-label-audit.yml",
    ".github/workflows/resolve-b-to-p-batch-2-source-receipts.yml",
    ".github/workflows/resolve-b-to-p-precision-source-receipts.yml",
    "docs/theory_to_network_prediction_contract.md",
    "docs/public_data_first_feasibility.md",
    "docs/PARAMETER_ENVELOPE_BRIDGE_PROTOCOL.md",
    "docs/part_i_to_big_data_decision_table.md",
    "empirical/broad_reality_evidence/BROAD_CODING_BATCH_PROTOCOL.md",
    "empirical/broad_reality_evidence/BROAD_REGISTERED_DIRECTION_EVIDENCE_v1.md",
    "empirical/broad_reality_evidence/FLORAL_TRAIT_ANIMAL_RESPONSE_META_PROTOCOL_v1.md",
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
    "docs/INTRODUCTION_BLUEPRINT.md",
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
