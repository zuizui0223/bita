from __future__ import annotations

import csv
import io
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "empirical" / "floral_defence_selectivity" / "CASE2026_POSTPUBLICATION_SOURCE_RECEIPT_V1.json"

from scripts.analyze_case2026_hawaii_replication import (
    CASE_MEMBER,
    aggregate_case_by_plant,
    normalize_case_units,
    read_case_rows,
    replication_gate,
    summarize_case,
    verify_case_source_bytes,
)


def _fixture_zip(path: Path) -> Path:
    fields = [
        "plant_species",
        "bird_species",
        "N",
        "pollen_contact",
        "nectar_robbing",
        "source",
        "culmen",
        "flower_length",
        "bill_minus_flower",
    ]
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fields)
    writer.writeheader()
    for i in range(30):
        plant_i = i % 6
        bird_i = i % 5
        culmen = 20.0 + bird_i
        flower = 18.0 + plant_i * 3.0
        mismatch = flower - culmen
        robbery = max(0.0, min(1.0, 0.2 + 0.05 * mismatch))
        writer.writerow(
            {
                "plant_species": f"P{plant_i}",
                "bird_species": f"B{bird_i}",
                "N": 10,
                "pollen_contact": 1.0 - robbery,
                "nectar_robbing": robbery,
                "source": f"S{i // 10}",
                "culmen": culmen,
                "flower_length": flower,
                "bill_minus_flower": culmen - flower,
            }
        )
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(CASE_MEMBER, buffer.getvalue())
    return path


def test_case_fixture_passes_replication_gate_without_becoming_confirmatory(tmp_path: Path) -> None:
    rows = read_case_rows(_fixture_zip(tmp_path / "case.zip"))
    units, audit = normalize_case_units(rows)
    points = aggregate_case_by_plant(units)
    gate = replication_gate(units, points)

    assert audit["normalized_source_bird_plant_units"] == 30
    assert audit["bird_species"] == 5
    assert audit["plant_species"] == 6
    assert gate["passes_postpublication_replication_gate"] is True
    assert gate["confirmatory_third_fauna_gate"] is False


def test_case_access_constraint_sign_matches_bita_definition(tmp_path: Path) -> None:
    rows = read_case_rows(_fixture_zip(tmp_path / "case.zip"))
    units, _ = normalize_case_units(rows)
    first = units[0]
    assert first["access_constraint_flower_minus_bill_mm"] == (
        18.0 - 20.0
    )


def test_case_summary_is_positive_but_labeled_postpublication(tmp_path: Path) -> None:
    rows = read_case_rows(_fixture_zip(tmp_path / "case.zip"))
    units, _ = normalize_case_units(rows)
    result = summarize_case(units, permutations=199, seed=123)

    assert result["analysis_status"] == "POST_PUBLICATION_REPLICATION"
    assert result["rho"] is not None
    assert float(result["rho"]) > 0
    assert "not an outcome-blind" in str(result["claim_boundary"]).lower()


def test_wrong_case_bytes_fail_exact_source_identity(tmp_path: Path) -> None:
    path = _fixture_zip(tmp_path / "not-the-dryad-source.zip")
    import pytest
    with pytest.raises(ValueError, match="do not match frozen Dryad identity"):
        verify_case_source_bytes(path)


def test_case_source_receipt_keeps_standardized_k3_closed_without_source_bytes() -> None:
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert receipt["status"] == "SOURCE_BYTES_NOT_AVAILABLE_IN_AUTOMATION"
    assert receipt["source_file"] == "Case_FE_2026_Analysis_2.csv"
    assert receipt["source_size_bytes"] == 1462
    assert receipt["source_sha256"] == "ac132a82cc70abc34765b76add6c2280603108b2c958578b816cf211d3deb691"
    assert receipt["public_schema_breadth"] == {"plant_species": 11, "bird_species": 7}
    assert receipt["published_direction"]["concordant_with_bita"] is True
    assert receipt["standardized_reanalysis"]["exact_source_bytes_verified"] is False
    assert receipt["standardized_reanalysis"]["case_rho"] is None
    assert receipt["standardized_reanalysis"]["joint_k3_rho"] is None
    assert receipt["claim_boundary"]["current_standardized_network_k"] == 2
