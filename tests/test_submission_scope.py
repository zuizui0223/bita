from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


RETIRED_PATHS = [
    "trait_architecture/dalechampia_linked_panel.py",
    "trait_architecture/dalechampia_package_documentation.py",
    "trait_architecture/gymnadenia_a_to_antagonism.py",
    "trait_architecture/gymnadenia_row_linkage.py",
    "trait_architecture/fixed_candidate_universe.py",
    "scripts/harvest_openalex_matched_flower_seeds.py",
    "scripts/run_research_pipeline.py",
    "empirical/matched_flower_regime/MATCHED_STUDY_PROTOCOL.md",
    "docs/MANUSCRIPT_RESULTS_V1.md",
    "docs/CURRENT_REVIEW_AND_CLEANUP_PLAN_V1.md",
]


REQUIRED_ACTIVE_PATHS = [
    "docs/MANUSCRIPT_RESULTS_V2.md",
    "docs/IMPATIENS_RESULTS_LOCK_V1.md",
    "docs/SUBMISSION_SCOPE.md",
    "scripts/build_part_i_manuscript_readout.py",
    "scripts/build_part_i_regime_figure_svg.py",
]


def test_retired_exploratory_paths_do_not_return():
    for relative in RETIRED_PATHS:
        assert not (ROOT / relative).exists(), relative


def test_current_submission_spine_is_present():
    for relative in REQUIRED_ACTIVE_PATHS:
        assert (ROOT / relative).exists(), relative
