from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

from scripts.load_frozen_access_routing_archive import (
    AUBERT_EPHI_DOI,
    CANONICAL_AUBERT_CSV_SHA256,
    CANONICAL_MANIFEST_SHA256,
    CANONICAL_SAKHALKAR_CSV_SHA256,
    EXPECTED_ARCHIVE_SCHEMA,
    MODE,
    SAKHALKAR_DOI,
    load_frozen_existing_networks,
    observed_k2_effects,
)


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _archive(tmp_path: Path):
    root = tmp_path / "archive"
    root.mkdir()

    sakh_rows = [
        {
            "analysis_unit": f"plant_{i:03d}",
            "route_balance": float(i - 2),
            "tube_length": float(i + 1),
            "tube_width": "",
            "brightness": "",
            "shape": "shape",
        }
        for i in range(1, 6)
    ]
    aubert_rows = []
    index = 0
    for site_i, site in enumerate(("site_01", "site_02"), start=1):
        for i in range(6):
            index += 1
            mismatch = float(i - 2.5)
            aubert_rows.append(
                {
                    "analysis_unit": f"pair_site_{index:04d}",
                    "site_id": site,
                    "bird_group": "hummingbird",
                    "n_interactions": 3,
                    "robbery_rate": (i + site_i) / 10.0,
                    "mismatch_log_t_over_b": mismatch,
                    "trait_barrier": "true" if mismatch > 0 else "false",
                }
            )

    _write_csv(
        root / "sakhalkar_species_analysis.csv",
        ["analysis_unit", "route_balance", "tube_length", "tube_width", "brightness", "shape"],
        sakh_rows,
    )
    _write_csv(
        root / "aubert_ephi_pair_site_analysis.csv",
        [
            "analysis_unit",
            "site_id",
            "bird_group",
            "n_interactions",
            "robbery_rate",
            "mismatch_log_t_over_b",
            "trait_barrier",
        ],
        aubert_rows,
    )

    manifest = {
        "archive_schema": EXPECTED_ARCHIVE_SCHEMA,
        "source_data": {
            "sakhalkar_2023_zenodo_doi": SAKHALKAR_DOI,
            "aubert_ephi_zenodo_mirror_doi": AUBERT_EPHI_DOI,
        },
        "analysis_tables": {
            "sakhalkar_species_analysis.csv": len(sakh_rows),
            "aubert_ephi_pair_site_analysis.csv": len(aubert_rows),
        },
        "identifier_policy": "test",
    }
    (root / "archive_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    sakh_points = [
        {"tube_length": float(row["tube_length"]), "balance": float(row["route_balance"])}
        for row in sakh_rows
    ]
    normalized_aubert = [
        {
            "site": str(row["site_id"]),
            "bird_group": str(row["bird_group"]),
            "n_interactions": int(row["n_interactions"]),
            "robbery_rate": float(row["robbery_rate"]),
            "mismatch_log_t_over_b": float(row["mismatch_log_t_over_b"]),
            "trait_barrier": str(row["trait_barrier"]) == "true",
        }
        for row in aubert_rows
    ]
    observed = observed_k2_effects(
        sakh_points,
        normalized_aubert,
        expected_sakhalkar_units=5,
        expected_aubert_units=12,
        expected_aubert_sites=2,
    )
    frozen = {
        "network_count": 2,
        "network_direction_concordance": "2_of_2_positive",
        "network_effects": {
            "sakhalkar": {
                "n_units": 5,
                "rho": observed["sakhalkar_rho"],
            },
            "aubert_ephi": {
                "n_units": 12,
                "site_count": 2,
                "rho": observed["aubert_site_adjusted_rho"],
                "rho_global_descriptive": observed["aubert_global_rho"],
            },
        },
        "joint_equal_network_fisher_z_rho": observed[
            "joint_equal_network_fisher_z_rho"
        ],
    }
    frozen_path = tmp_path / "frozen.json"
    frozen_path.write_text(
        json.dumps(frozen, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return root, frozen_path, observed


def test_frozen_existing_network_archive_loads_without_network_access(tmp_path) -> None:
    root, frozen, expected = _archive(tmp_path)
    sakh, aubert, receipt = load_frozen_existing_networks(
        root,
        frozen,
        expected_sakhalkar_units=5,
        expected_aubert_units=12,
        expected_aubert_sites=2,
        enforce_canonical_hashes=False,
    )
    assert len(sakh) == 5
    assert len(aubert) == 12
    assert receipt["status"] == "FROZEN_EXISTING_NETWORKS_VALIDATED"
    assert receipt["input_mode"] == MODE
    assert receipt["frozen_k2_validation"] == "PASS"
    assert receipt["observed_k2_effects"] == expected
    assert receipt["source_dois"]["sakhalkar"] == SAKHALKAR_DOI
    assert receipt["source_dois"]["aubert_ephi"] == AUBERT_EPHI_DOI
    for entry in receipt["files"].values():
        assert len(entry["sha256"]) == 64


def test_changed_archive_value_fails_frozen_k2_validation(tmp_path) -> None:
    root, frozen, _expected = _archive(tmp_path)
    path = root / "sakhalkar_species_analysis.csv"
    rows = list(csv.DictReader(path.open(encoding="utf-8", newline="")))
    rows[0]["route_balance"] = "999"
    _write_csv(
        path,
        ["analysis_unit", "route_balance", "tube_length", "tube_width", "brightness", "shape"],
        rows,
    )

    with pytest.raises(ValueError, match="FROZEN_K2_MISMATCH"):
        load_frozen_existing_networks(
            root,
            frozen,
            expected_sakhalkar_units=5,
            expected_aubert_units=12,
            expected_aubert_sites=2,
            enforce_canonical_hashes=False,
        )


def test_wrong_archive_unit_count_fails_before_k3(tmp_path) -> None:
    root, frozen, _expected = _archive(tmp_path)
    path = root / "aubert_ephi_pair_site_analysis.csv"
    rows = list(csv.DictReader(path.open(encoding="utf-8", newline="")))[:-1]
    _write_csv(
        path,
        [
            "analysis_unit",
            "site_id",
            "bird_group",
            "n_interactions",
            "robbery_rate",
            "mismatch_log_t_over_b",
            "trait_barrier",
        ],
        rows,
    )

    with pytest.raises(ValueError, match="FROZEN_AUBERT_UNIT_COUNT_MISMATCH"):
        load_frozen_existing_networks(
            root,
            frozen,
            expected_sakhalkar_units=5,
            expected_aubert_units=12,
            expected_aubert_sites=2,
            enforce_canonical_hashes=False,
        )


def test_wrong_source_doi_fails_archive_gate(tmp_path) -> None:
    root, frozen, _expected = _archive(tmp_path)
    path = root / "archive_manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest["source_data"]["sakhalkar_2023_zenodo_doi"] = "10.0000/wrong"
    path.write_text(json.dumps(manifest), encoding="utf-8")

    with pytest.raises(ValueError, match="SAKHALKAR_DOI_MISMATCH"):
        load_frozen_existing_networks(
            root,
            frozen,
            expected_sakhalkar_units=5,
            expected_aubert_units=12,
            expected_aubert_sites=2,
            enforce_canonical_hashes=False,
        )


def test_wrong_frozen_joint_effect_fails_archive_gate(tmp_path) -> None:
    root, frozen, _expected = _archive(tmp_path)
    payload = json.loads(frozen.read_text(encoding="utf-8"))
    payload["joint_equal_network_fisher_z_rho"] += 0.1
    frozen.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="joint_equal_network_fisher_z_rho"):
        load_frozen_existing_networks(
            root,
            frozen,
            expected_sakhalkar_units=5,
            expected_aubert_units=12,
            expected_aubert_sites=2,
            enforce_canonical_hashes=False,
        )



def test_production_default_rejects_noncanonical_archive_bytes(tmp_path) -> None:
    root, frozen, _expected = _archive(tmp_path)
    with pytest.raises(ValueError, match="FROZEN_EXISTING_NETWORK_CANONICAL_HASH_MISMATCH"):
        load_frozen_existing_networks(
            root,
            frozen,
            expected_sakhalkar_units=5,
            expected_aubert_units=12,
            expected_aubert_sites=2,
        )



def test_canonical_archive_hash_constants_match_frozen_provenance_receipt() -> None:
    path = (
        ROOT
        / "empirical"
        / "floral_defence_selectivity"
        / "EXISTING_NETWORK_ARCHIVE_FREEZE_RECEIPT_V1.json"
    )
    receipt = json.loads(path.read_text(encoding="utf-8"))
    archive = receipt["analysis_archive"]

    assert receipt["status"] == "FROZEN_FOR_FUTURE_K3"
    assert receipt["production_input_mode"] == MODE
    assert archive["archive_schema"] == EXPECTED_ARCHIVE_SCHEMA
    assert (
        archive["sakhalkar_species_analysis.csv"]["sha256"]
        == CANONICAL_SAKHALKAR_CSV_SHA256
    )
    assert (
        archive["aubert_ephi_pair_site_analysis.csv"]["sha256"]
        == CANONICAL_AUBERT_CSV_SHA256
    )
    assert archive["archive_manifest.json"]["sha256"] == CANONICAL_MANIFEST_SHA256
    assert receipt["source_dois"]["sakhalkar"] == SAKHALKAR_DOI
    assert receipt["source_dois"]["aubert_ephi"] == AUBERT_EPHI_DOI
