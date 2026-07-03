from __future__ import annotations

import csv
import json

from trait_architecture.d_a_caruso_index_readout import classify_index_route, write_readout


def _manifest() -> list[dict[str, str]]:
    return [{
        "access_status": "file_manifest_entry",
        "filename": "Exp_stud_dup_Dryad.xlsx",
        "primary_study_index_candidate": "false",
    }]


def test_http_401_before_schema_is_an_access_block_not_missing_columns() -> None:
    report = classify_index_route(_manifest(), [{
        "download_status": "download_or_parse_failed",
        "schema_decision": "retain_as_manifest_candidate:download_http_401",
    }])
    assert report["route_verdict"] == "public_xlsx_access_blocked_before_schema"
    assert report["next_action"] == "retain_caruso_as_system_seed_only_public_xlsx_download_unauthorized"
    assert report["schema_access_blocked_count"] == 1
    assert report["bibliographic_identifier_schema_count"] == 0


def test_recovered_bibliographic_schema_opens_identifier_only_stage() -> None:
    report = classify_index_route(_manifest(), [{
        "download_status": "schema_recovered",
        "schema_decision": "bibliographic_index_columns_present_needs_identifier_extraction",
    }])
    assert report["route_verdict"] == "schema_recovered_with_bibliographic_identifier_columns"
    assert report["next_action"] == "extract_bibliographic_identifiers_only"


def test_write_readout_keeps_only_route_summary(tmp_path) -> None:
    manifest = tmp_path / "manifest.csv"
    schema = tmp_path / "schema.csv"
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["access_status", "filename", "primary_study_index_candidate"])
        writer.writeheader(); writer.writerows(_manifest())
    with schema.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["download_status", "schema_decision"])
        writer.writeheader(); writer.writerow({"download_status": "download_or_parse_failed", "schema_decision": "retain_as_manifest_candidate:download_http_401"})
    report = write_readout(tmp_path / "out", manifest_csv=manifest, schema_csv=schema)
    saved = json.loads((tmp_path / "out" / "d_a_caruso_index_route_readout.json").read_text(encoding="utf-8"))
    assert report["schema_access_blocked_count"] == 1
    assert saved["next_action"] == "retain_caruso_as_system_seed_only_public_xlsx_download_unauthorized"
    assert "effect_value" not in saved
