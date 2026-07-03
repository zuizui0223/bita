from __future__ import annotations

import csv
import json

from trait_architecture.d_a_caruso_dryad_manifest import (
    CARUSO_SOURCE_DOI,
    DRYAD_DATASET_DOI,
    probe_dryad_manifest,
    summarise,
    write_outputs,
)


def _responder(url: str):
    if "api.datacite.org" in url:
        return 200, {"data": {"attributes": {"relatedIdentifiers": [{"relatedIdentifier": CARUSO_SOURCE_DOI}]}}}
    if "datadryad.org/api/v2/datasets/" in url:
        # The real API returns an encoded DOI route and a relative versions link.
        return 200, {"_links": {"stash:versions": {"href": "/api/v2/datasets/doi%3A10.5061%2Fdryad.2v8c5g0/versions"}}}
    if url.endswith("/versions"):
        # Versions can arrive as a collection; the file relation belongs to the
        # current embedded version entry rather than the collection itself.
        return 200, {
            "_embedded": {
                "stash:versions": [
                    {"_links": {"stash:files": {"href": "/api/v2/versions/1/files"}}}
                ]
            }
        }
    if url.endswith("/versions/1/files"):
        return 200, {
            "_embedded": {
                "stash:files": [
                    {
                        "id": "f1",
                        "path": "primary_study_metadata.csv",
                        "mimeType": "text/csv",
                        "size": 1200,
                        "_links": {"stash:download": {"href": "/file/f1/download"}},
                    },
                    {"id": "f2", "path": "effect_sizes.rds", "mimeType": "application/octet-stream", "size": 999},
                ]
            }
        }
    raise AssertionError(url)


def test_manifest_identifies_filename_candidate_without_reading_contents() -> None:
    rows = probe_dryad_manifest(fetch_json=_responder)
    entries = [row for row in rows if row.access_status == "file_manifest_entry"]
    assert len(entries) == 2
    assert any(row.access_status == "version_metadata_recovered" for row in rows)
    assert entries[0].filename == "primary_study_metadata.csv"
    assert entries[0].file_url == "https://datadryad.org/file/f1/download"
    assert entries[0].primary_study_index_candidate == "true"
    assert entries[1].primary_study_index_candidate == "false"
    report = summarise(rows)
    assert report["dataset_doi"] == DRYAD_DATASET_DOI
    assert report["primary_study_index_file_candidate_count"] == 1
    assert report["next_action"] == "inspect_capped_candidate_file_schema"


def test_missing_file_link_stops_before_file_download() -> None:
    def responder(url: str):
        if "api.datacite.org" in url:
            return 200, {"data": {"attributes": {"relatedIdentifiers": []}}}
        return 200, {"_links": {}}
    rows = probe_dryad_manifest(fetch_json=responder)
    assert any(row.access_status == "file_manifest_link_not_found" for row in rows)
    assert summarise(rows)["next_action"] == "stop_before_file_download_no_bibliographic_index_filename_candidate"


def test_write_outputs_contains_no_primary_study_rows(tmp_path) -> None:
    rows = probe_dryad_manifest(fetch_json=_responder)
    report = write_outputs(tmp_path, rows)
    written = list(csv.DictReader((tmp_path / "d_a_caruso_dryad_manifest.csv").open(encoding="utf-8")))
    saved = json.loads((tmp_path / "d_a_caruso_dryad_manifest_report.json").read_text(encoding="utf-8"))
    assert report["manifest_file_count"] == 2
    assert saved["primary_study_index_file_candidate_count"] == 1
    assert all("effect_value" not in row and "primary_study_doi" not in row for row in written)
