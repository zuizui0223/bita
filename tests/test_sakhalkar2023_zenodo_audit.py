from __future__ import annotations

import io
import zipfile
from urllib.error import HTTPError

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
