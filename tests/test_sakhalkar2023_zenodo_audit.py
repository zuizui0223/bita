from __future__ import annotations

import hashlib
import io
import zipfile
from http.client import RemoteDisconnected
from urllib.error import HTTPError

import pytest

from scripts import audit_sakhalkar2023_zenodo as audit
from scripts.audit_sakhalkar2023_zenodo import summarize_archive


def _fake_xlsx() -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as book:
        book.writestr(
            "xl/workbook.xml",
            """<?xml version="1.0" encoding="UTF-8"?>
            <workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
              xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
              <sheets><sheet name="visits" sheetId="1" r:id="rId1"/></sheets>
            </workbook>""",
        )
        book.writestr(
            "xl/_rels/workbook.xml.rels",
            """<?xml version="1.0" encoding="UTF-8"?>
            <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
              <Relationship Id="rId1" Type="worksheet" Target="worksheets/sheet1.xml"/>
            </Relationships>""",
        )
        book.writestr(
            "xl/worksheets/sheet1.xml",
            """<?xml version="1.0" encoding="UTF-8"?>
            <worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
              <dimension ref="A1:C3"/>
              <sheetData><row r="1">
                <c r="A1" t="inlineStr"><is><t>plant</t></is></c>
                <c r="B1" t="inlineStr"><is><t>visitor</t></is></c>
                <c r="C1" t="inlineStr"><is><t>role</t></is></c>
              </row></sheetData>
            </worksheet>""",
        )
    return buffer.getvalue()


def _fake_archive() -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("project/input/cheaters.xlsx", _fake_xlsx())
        archive.writestr("project/R/analysis.R", "print('ok')\n")
        archive.writestr("project/README.md", "test")
    return buffer.getvalue()


def test_archive_inventory_reports_safe_file_metadata() -> None:
    report = summarize_archive(_fake_archive())
    assert report["archive_member_count"] == 3
    assert report["member_names"] == [
        "project/R/analysis.R",
        "project/README.md",
        "project/input/cheaters.xlsx",
    ]
    assert report["xlsx_files"] == ["project/input/cheaters.xlsx"]
    assert report["r_files"] == ["project/R/analysis.R"]
    assert report["readme_files"] == ["project/README.md"]
    assert report["total_uncompressed_bytes"] > 0


def test_xlsx_schema_reports_sheet_dimension_and_headers_only() -> None:
    report = summarize_archive(_fake_archive())
    workbook = report["xlsx_workbooks"]["project/input/cheaters.xlsx"]
    assert workbook["sheets"] == [
        {
            "name": "visits",
            "dimension": "A1:C3",
            "headers": ["plant", "visitor", "role"],
        }
    ]


def test_archive_inventory_does_not_emit_data_rows_or_script_contents() -> None:
    report = summarize_archive(_fake_archive())
    encoded = str(report)
    assert "print('ok')" not in encoded
    assert "raw_rows" not in report


def test_download_retries_transient_5xx(monkeypatch) -> None:
    calls = {"n": 0}

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self, _limit):
            return b"abc"

    def fake_urlopen(request, timeout=60):
        calls["n"] += 1
        if calls["n"] < 3:
            raise HTTPError(request.full_url, 504, "Gateway Time-out", {}, None)
        return FakeResponse()

    monkeypatch.setattr(audit, "urlopen", fake_urlopen)
    monkeypatch.setattr(audit.time, "sleep", lambda _seconds: None)
    monkeypatch.setattr(audit, "MAX_BYTES", 10)

    assert audit._download() == b"abc"
    assert calls["n"] == 3


def test_download_retries_remote_disconnected(monkeypatch) -> None:
    calls = {"n": 0}

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self, _limit):
            return b"source-zip"

    def fake_urlopen(_request, timeout=60):
        calls["n"] += 1
        if calls["n"] == 1:
            raise RemoteDisconnected("Remote end closed connection without response")
        return FakeResponse()

    monkeypatch.setattr(audit, "urlopen", fake_urlopen)
    monkeypatch.setattr(audit.time, "sleep", lambda _seconds: None)
    assert audit._download() == b"source-zip"
    assert calls["n"] == 2


def test_download_remote_disconnected_exhaustion_is_fail_closed(monkeypatch) -> None:
    calls = {"n": 0}

    def fake_urlopen(_request, timeout=60):
        calls["n"] += 1
        raise RemoteDisconnected("Remote end closed connection without response")

    monkeypatch.setattr(audit, "urlopen", fake_urlopen)
    monkeypatch.setattr(audit.time, "sleep", lambda _seconds: None)

    with pytest.raises(RuntimeError, match="after Zenodo retries"):
        audit._download()
    assert calls["n"] == 5  # Four Zenodo attempts plus one pinned GitHub attempt


def _author_snapshot(workbook: bytes) -> bytes:
    archive = io.BytesIO()
    with zipfile.ZipFile(archive, "w") as z:
        z.writestr(
            "cheaters-among-pollinators-ecosphere/input/cheaters_visitation_and_trait_data.xlsx",
            workbook,
        )
        z.writestr("cheaters-among-pollinators-ecosphere/README.md", "author archive")
        z.writestr("cheaters-among-pollinators-ecosphere/scripts/cheaters_analysis.R", "pass")
    return archive.getvalue()


def _source_response(payload: bytes):
    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self, _limit):
            return payload

    return FakeResponse()


def test_zenodo_504_uses_only_blob_verified_tagged_author_snapshot(monkeypatch, capsys) -> None:
    workbook = _fake_xlsx()
    blob = hashlib.sha1(f"blob {len(workbook)}\0".encode("ascii") + workbook).hexdigest()
    upstream = _author_snapshot(workbook)
    monkeypatch.setattr(audit, "UPSTREAM_WORKBOOK_BLOB_SHA1", blob)
    monkeypatch.setattr(audit, "UPSTREAM_WORKBOOK_SIZE", len(workbook))
    monkeypatch.setattr(audit.time, "sleep", lambda _seconds: None)
    requests = []

    def fake_urlopen(request, timeout=60):
        requests.append(request.full_url)
        if "zenodo.org" in request.full_url:
            raise HTTPError(request.full_url, 504, "Gateway Time-out", {}, None)
        assert request.full_url == audit.UPSTREAM_SNAPSHOT_URL
        return _source_response(upstream)

    monkeypatch.setattr(audit, "urlopen", fake_urlopen)
    assert audit._download() == upstream
    assert len(requests) == 5
    assert all("zenodo.org" in u for u in requests[:4])
    assert requests[-1] == audit.UPSTREAM_SNAPSHOT_URL
    stderr = capsys.readouterr().err
    assert blob in stderr
    assert "ZENODO_TRANSIENT_FAILURE" in stderr
    assert "SOURCE_PROVENANCE" in stderr
    # Provenance is printed for the release audit but no raw rows are emitted.


def test_github_snapshot_rejects_changed_primary_workbook(monkeypatch) -> None:
    workbook = _fake_xlsx()
    upstream = _author_snapshot(workbook)
    monkeypatch.setattr(audit, "UPSTREAM_WORKBOOK_SIZE", len(workbook))
    monkeypatch.setattr(audit, "urlopen", lambda *_args, **_kwargs: _source_response(upstream))
    with pytest.raises(ValueError, match="git blob SHA-1 mismatch"):
        audit._pinned_author_github_snapshot()


def test_github_snapshot_rejects_missing_workbook(monkeypatch) -> None:
    payload = io.BytesIO()
    with zipfile.ZipFile(payload, "w") as z:
        z.writestr("README.md", "no workbook")
    monkeypatch.setattr(audit, "urlopen", lambda *_args, **_kwargs: _source_response(payload.getvalue()))
    with pytest.raises(ValueError, match="exactly one"):
        audit._pinned_author_github_snapshot()


def test_zenodo_404_does_not_switch_sources(monkeypatch) -> None:
    requests = []

    def fake_urlopen(request, timeout=60):
        requests.append(request.full_url)
        raise HTTPError(request.full_url, 404, "Not Found", {}, None)

    monkeypatch.setattr(audit, "urlopen", fake_urlopen)
    with pytest.raises(RuntimeError, match="Non-retryable Zenodo source response: HTTP 404"):
        audit._download()
    assert len(requests) == 1
    assert requests[0] == audit.DOWNLOAD_URL
