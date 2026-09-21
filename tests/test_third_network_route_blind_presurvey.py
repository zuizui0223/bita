from __future__ import annotations

import csv

import pytest

from scripts.evaluate_third_network_route_blind_presurvey import evaluate_rows, run


def _rows(n_mammals: int = 5) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    i = 0
    for p in range(5):
        i += 1
        rows.append(
            {
                "record_id": f"R{i}",
                "site_id": "S1",
                "record_type": "PLANT",
                "plant_species": f"P{p}",
                "mammal_species": "",
                "evidence_method": "flowering presurvey",
                "flowering_available": "YES",
                "camera_operable": "NA",
            }
        )
    for m in range(n_mammals):
        i += 1
        rows.append(
            {
                "record_id": f"R{i}",
                "site_id": "S1",
                "record_type": "MAMMAL",
                "plant_species": "",
                "mammal_species": f"M{m}",
                "evidence_method": "independent non-route mammal survey",
                "flowering_available": "NA",
                "camera_operable": "NA",
            }
        )
    i += 1
    rows.append(
        {
            "record_id": f"R{i}",
            "site_id": "S1",
            "record_type": "CAMERA",
            "plant_species": "",
            "mammal_species": "",
            "evidence_method": "camera setup test",
            "flowering_available": "NA",
            "camera_operable": "YES",
        }
    )
    return rows


def test_route_blind_presurvey_can_promote_schema_eligible_site() -> None:
    result = evaluate_rows(_rows())
    assert result["status"] == "PRESURVEY_ROUTE_BLIND_ELIGIBLE_SITES_PRESENT"
    assert result["eligible_sites"] == ["S1"]
    assert result["route_outcome_fields_present"] is False
    assert result["morphology_fields_present"] is False


def test_route_blind_presurvey_fails_richness_without_relaxation() -> None:
    result = evaluate_rows(_rows(n_mammals=4))
    assert result["status"] == "PRESURVEY_NO_ELIGIBLE_SITE"
    assert result["eligible_sites"] == []
    assert result["site_summary"]["S1"]["mammal_species"] == 4


def test_presurvey_reader_rejects_route_or_morphology_columns(tmp_path) -> None:
    path = tmp_path / "presurvey.csv"
    fields = list(_rows()[0]) + ["route_code"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in _rows():
            writer.writerow({**row, "route_code": ""})

    with pytest.raises(ValueError, match="ROUTE_OR_MORPHOLOGY_FIELD_FORBIDDEN"):
        run(path)


def test_presurvey_rejects_duplicate_record_ids() -> None:
    rows = _rows()
    rows[1]["record_id"] = rows[0]["record_id"]
    with pytest.raises(ValueError, match="record_id must be unique"):
        evaluate_rows(rows)
