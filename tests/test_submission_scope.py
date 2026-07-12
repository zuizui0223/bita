from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


RETIRED_PATHS = [
    ".github/workflows/run-impatiens-empirical-core.yml",
    "configs/impatiens_capensis_four_path_models.json",
    "configs/impatiens_response_scale_models.json",
    "configs/impatiens_randomized_fitness_models.json",
    "docs/EMPIRICAL_PIVOT_IMPATIENS_V1.md",
    "docs/IMPATIENS_RESULTS_LOCK_V1.md",
    "docs/IMPATIENS_MODEL_ADEQUACY_SENSITIVITY_V1.md",
    "docs/MANUSCRIPT_SKELETON_V1.md",
    "docs/MANUSCRIPT_RESULTS_V2.md",
    "docs/MANUSCRIPT_RESULTS_TABLES_V1.md",
    "scripts/run_impatiens_four_path_models.py",
    "scripts/run_impatiens_response_scale_models.py",
    "scripts/run_impatiens_randomized_fitness_models.py",
    "trait_architecture/impatiens_models.py",
    "trait_architecture/impatiens_response_scale_models.py",
    "trait_architecture/impatiens_factorial_fitness_models.py",
    "empirical/four_path_effects/title_validated_dataset_targets.csv",
    "trait_architecture/dalechampia_linked_panel.py",
    "trait_architecture/gymnadenia_a_to_antagonism.py",
    "trait_architecture/fixed_candidate_universe.py",
    "scripts/harvest_openalex_matched_flower_seeds.py",
    "scripts/run_research_pipeline.py",
]


REQUIRED_ACTIVE_PATHS = [
    "README.md",
    "SUPPLEMENT_MANIFEST.md",
    "docs/SUBMISSION_SCOPE.md",
    "configs/part_i_robustness_grid.json",
    "trait_architecture/model.py",
    "trait_architecture/robustness.py",
    "scripts/run_part_i_robustness.py",
    "scripts/build_part_i_manuscript_readout.py",
    "scripts/build_part_i_regime_figure_svg.py",
    "empirical/broad_reality_evidence/part_b_arrow_effects.csv",
    "scripts/validate_part_b_integrity.py",
]


def test_retired_exploratory_paths_do_not_return():
    for relative in RETIRED_PATHS:
        assert not (ROOT / relative).exists(), relative


def test_current_submission_spine_is_present():
    for relative in REQUIRED_ACTIVE_PATHS:
        assert (ROOT / relative).exists(), relative
