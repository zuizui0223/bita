from __future__ import annotations

import csv
import io
import zipfile
from pathlib import Path

from scripts.analyze_case2026_hawaii_replication import (
    CASE_MEMBER,
    aggregate_case_by_plant,
    normalize_case_units,
    read_case_rows,
    replication_gate,
    summarize_case,
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
