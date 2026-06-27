"""Audit a standardised plant--animal interaction table before analysis.

The audit is intentionally source-agnostic: Web of Life, Mangal, GloBI,
local field networks, and published supplements must be normalised into the
same contract before traits or model predictions are evaluated.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

REQUIRED_INTERACTION_COLUMNS = {"network_id", "interaction_type", "plant_taxon", "animal_taxon"}
REQUIRED_NETWORK_COLUMNS = {"network_id", "region"}


@dataclass(frozen=True)
class CoverageReport:
    interaction_rows: int
    networks: int
    regions: int
    interaction_types: tuple[str, ...]
    unique_plants: int
    unique_animals: int
    weighted_rows: int
    cited_rows: int
    period_rows: int
    plant_trait_match_rate: float
    trait_ready_networks: int
    status: str
    warnings: tuple[str, ...]


def _normalise(value: str | None) -> str:
    return (value or "").strip()


def _read_csv(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return [{key: _normalise(value) for key, value in row.items()} for row in csv.DictReader(handle)]


def _assert_columns(rows: list[dict[str, str]], required: set[str], label: str) -> None:
    if not rows:
        raise ValueError(f"{label} is empty")
    missing = sorted(required - set(rows[0]))
    if missing:
        raise ValueError(f"{label} is missing required columns: {', '.join(missing)}")


def audit_network_coverage(
    interactions: Iterable[dict[str, str]],
    network_metadata: Iterable[dict[str, str]],
    trait_taxa: Iterable[str],
) -> CoverageReport:
    interactions = [{key: _normalise(value) for key, value in row.items()} for row in interactions]
    metadata = [{key: _normalise(value) for key, value in row.items()} for row in network_metadata]
    _assert_columns(interactions, REQUIRED_INTERACTION_COLUMNS, "interaction table")
    _assert_columns(metadata, REQUIRED_NETWORK_COLUMNS, "network metadata")

    metadata_by_network = {row["network_id"]: row for row in metadata if row["network_id"]}
    valid = [row for row in interactions if row["network_id"] and row["plant_taxon"] and row["animal_taxon"]]
    plants = {row["plant_taxon"] for row in valid}
    trait_set = {_normalise(taxon) for taxon in trait_taxa if _normalise(taxon)}
    matched_plants = plants & trait_set
    per_network_plants: dict[str, set[str]] = defaultdict(set)
    for row in valid:
        per_network_plants[row["network_id"]].add(row["plant_taxon"])

    regions = {metadata_by_network[row["network_id"]].get("region", "") for row in valid if row["network_id"] in metadata_by_network}
    regions.discard("")
    interaction_types = tuple(sorted({row["interaction_type"] for row in valid if row["interaction_type"]}))
    weighted_rows = sum(bool(row.get("weight", "")) for row in valid)
    cited_rows = sum(bool(row.get("citation_id", "") or row.get("source_dataset_id", "")) for row in valid)
    period_rows = sum(bool(row.get("sampling_period", "")) for row in valid)
    trait_ready_networks = sum(bool(taxa & trait_set) for taxa in per_network_plants.values())
    rate = len(matched_plants) / len(plants) if plants else 0.0

    warnings: list[str] = []
    if len(metadata_by_network) < len({row["network_id"] for row in valid}):
        warnings.append("Some interaction rows lack matching network metadata.")
    if len(interaction_types) != 1:
        warnings.append("Multiple interaction types are present; analyse them as separate layers unless a harmonisation rule is declared.")
    if weighted_rows == 0:
        warnings.append("No interaction weights are present; interaction intensity cannot be tested from this table.")
    if cited_rows < len(valid):
        warnings.append("Some rows lack dataset/citation provenance.")
    if rate < 0.60:
        warnings.append("Plant trait coverage is below the 60% backbone threshold.")
    if len(per_network_plants) < 30:
        warnings.append("Fewer than 30 networks: retain as a pilot, not a broad backbone.")

    if len(per_network_plants) >= 30 and rate >= 0.60 and len(regions) >= 3:
        status = "backbone_candidate"
    elif len(per_network_plants) >= 10 and rate >= 0.40:
        status = "pilot_candidate"
    else:
        status = "insufficient"

    return CoverageReport(
        interaction_rows=len(valid),
        networks=len(per_network_plants),
        regions=len(regions),
        interaction_types=interaction_types,
        unique_plants=len(plants),
        unique_animals=len({row["animal_taxon"] for row in valid}),
        weighted_rows=weighted_rows,
        cited_rows=cited_rows,
        period_rows=period_rows,
        plant_trait_match_rate=rate,
        trait_ready_networks=trait_ready_networks,
        status=status,
        warnings=tuple(warnings),
    )


def audit_files(interaction_csv: str | Path, metadata_csv: str | Path, trait_taxa_csv: str | Path) -> CoverageReport:
    interactions = _read_csv(interaction_csv)
    metadata = _read_csv(metadata_csv)
    trait_rows = _read_csv(trait_taxa_csv)
    if not trait_rows or "plant_taxon" not in trait_rows[0]:
        raise ValueError("trait taxa table must contain plant_taxon")
    return audit_network_coverage(interactions, metadata, [row["plant_taxon"] for row in trait_rows])


def report_to_dict(report: CoverageReport) -> dict[str, object]:
    return {
        "interaction_rows": report.interaction_rows,
        "networks": report.networks,
        "regions": report.regions,
        "interaction_types": list(report.interaction_types),
        "unique_plants": report.unique_plants,
        "unique_animals": report.unique_animals,
        "weighted_rows": report.weighted_rows,
        "cited_rows": report.cited_rows,
        "period_rows": report.period_rows,
        "plant_trait_match_rate": report.plant_trait_match_rate,
        "trait_ready_networks": report.trait_ready_networks,
        "status": report.status,
        "warnings": list(report.warnings),
    }
