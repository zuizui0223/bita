from __future__ import annotations

import csv
from pathlib import Path

import pytest

from scripts.build_floral_defence_selectivity_dataset import build_analysis_ready
from trait_architecture.floral_defence_selectivity import load_csv_rows


def _registry(cluster: str = "c1") -> dict[str, str]:
    return {
        "study_cluster_id": cluster,
        "publication_id": f"pub-{cluster}",
        "plant_taxon": "Plant sp.",
        "D_axis_id": "D1",
        "context_id": "ctx",
        "derivation_or_holdout": "derivation",
        "source_provenance_path": "source.md",
    }


def _architecture(cluster: str = "c1") -> dict[str, str]:
    return {
        "study_cluster_id": cluster,
        "D_axis_id": "D1",
        "context_id": "ctx",
        "pre_outcome_domain_code": "SEPARATED",
        "separating_coordinate": "geometry",
        "defence_modality": "physical",
        "antagonist_guild": "antagonist",
        "pollinator_guild": "pollinator",
        "observational_or_experimental": "experimental",
        "architecture_basis_path": "architecture.md",
    }


def _outcome(cluster: str = "c1", pollinator_state: str = "PRESERVED_OR_IMPROVED") -> dict[str, str]:
    direction = "improved" if pollinator_state == "PRESERVED_OR_IMPROVED" else "impaired"
    return {
        "study_cluster_id": cluster,
        "D_axis_id": "D1",
        "context_id": "ctx",
        "antagonist_outcome_type": "damage",
        "antagonist_effect_direction": "suppressed",
        "antagonist_uncertainty_class": "DIRECTION_SUPPORTED",
        "pollinator_outcome_type": "visitation",
        "pollinator_response_stage": "arrival",
        "pollinator_effect_direction": direction,
        "pollinator_uncertainty_class": "DIRECTION_SUPPORTED",
        "pollinator_cost_state": pollinator_state,
        "source_supported_preservation": "true" if pollinator_state == "PRESERVED_OR_IMPROVED" else "false",
        "source_inference": "source-supported",
        "outcome_basis_path": "outcome.md",
    }


def test_load_csv_rows_round_trips_rows(tmp_path: Path) -> None:
    path = tmp_path / "rows.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["a", "b"])
        writer.writeheader()
        writer.writerow({"a": "1", "b": "2"})
    assert load_csv_rows(path) == [{"a": "1", "b": "2"}]


def test_duplicate_registry_key_is_rejected() -> None:
    with pytest.raises(ValueError, match="duplicate registry key"):
        build_analysis_ready([_registry(), _registry()], [_architecture()], [_outcome()])


def test_join_requires_exact_architecture_and_outcome_keys() -> None:
    with pytest.raises(ValueError, match="missing architecture"):
        build_analysis_ready([_registry()], [], [_outcome()])
    with pytest.raises(ValueError, match="missing outcome"):
        build_analysis_ready([_registry()], [_architecture()], [])


def test_audit_counts_independent_clusters_not_effect_rows() -> None:
    registry = [_registry("c1"), _registry("c2")]
    architecture = [_architecture("c1"), _architecture("c2")]
    outcomes = [_outcome("c1", "PRESERVED_OR_IMPROVED"), _outcome("c2", "IMPAIRED")]
    joined, audit = build_analysis_ready(registry, architecture, outcomes)
    assert len(joined) == 2
    assert audit["registry_rows"] == 2
    assert audit["independent_study_clusters"] == 2
    assert audit["stage1_eligible_clusters"] == 2
    assert audit["stage2_strict_eligible_clusters"] == 2
    assert audit["derivation_clusters"] == 2
    assert audit["holdout_clusters"] == 0


def test_join_preserves_both_provenance_paths() -> None:
    joined, _ = build_analysis_ready([_registry()], [_architecture()], [_outcome()])
    row = joined[0]
    assert row["source_provenance_path"] == "source.md"
    assert row["architecture_basis_path"] == "architecture.md"
    assert row["outcome_basis_path"] == "outcome.md"
