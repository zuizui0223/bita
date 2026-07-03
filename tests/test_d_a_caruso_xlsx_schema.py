from __future__ import annotations

import csv
import io
import json
import zipfile

from trait_architecture.d_a_caruso_xlsx_schema import inspect_manifest, read_manifest, write_outputs


NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG = "http://schemas.openxmlformats.org/package/2006/relationships"


def _xlsx_bytes(headers: list[str]) -> bytes:
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w") as archive:
        archive.writestr(
            "xl/workbook.xml",
            f'<workbook xmlns="{NS}" xmlns:r="{REL}"><sheets><sheet name="Study metadata" sheetId="1" r:id="rId1"/></sheets></workbook>',
        )
        archive.writestr(
            "xl/_rels/workbook.xml.rels",
            f'<Relationships xmlns="{PKG}"><Relationship Id="rId1" Target="worksheets/sheet1.xml"/></Relationships>',
        )
        cells = "".join(f'<c r="A{i + 1}" t="s"><v>{i}</v></c>' for i in range(len(headers)))
        # Cell positions are irrelevant for the schema test; the first row is the
        # header source and no data row is included in the fixture.
        archive.writestr(
            "xl/worksheets/sheet1.xml",
            f'<worksheet xmlns="{NS}"><dimension ref="A1:E12"/><sheetData><row r="1">{cells}</row></sheetData></worksheet>',
        )
        strings = "".join(f"<si><t>{header}</t></si>" for header in headers)
        archive.writestr("xl/sharedStrings.xml", f'<sst xmlns="{NS}">{strings}</sst>')
    return output.getvalue()


def _write_manifest(path, rows):
    fields = ["access_status", "filename", "file_url", "primary_study_index_candidate"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def test_exp_stud_xlsx_is_selected_and_emits_headers_only(tmp_path) -> None:
    manifest = tmp_path / "manifest.csv"
    _write_manifest(manifest, [{
        "access_status": "file_manifest_entry",
        "filename": "Exp_stud_dup_Dryad.xlsx",
        "file_url": "https://datadryad.org/api/v2/files/21863/download",
        "primary_study_index_candidate": "false",
    }])
    rows = inspect_manifest(manifest, download=lambda _url: _xlsx_bytes(["Study_ID", "DOI", "Trait", "Herbivore_damage", "Selection_gradient"]))
    assert len(rows) == 1
    assert rows[0].sheet_name == "Study metadata"
    assert rows[0].worksheet_dimension == "A1:E12"
    assert rows[0].bibliographic_identifier_columns == "Study_ID;DOI"
    assert "Trait" in rows[0].route_context_columns
    assert "Selection_gradient" in rows[0].selection_metric_columns
    assert rows[0].schema_decision == "bibliographic_index_columns_present_needs_identifier_extraction"


def test_only_xls_manifest_entry_is_not_downloaded(tmp_path) -> None:
    manifest = tmp_path / "manifest.csv"
    _write_manifest(manifest, [{
        "access_status": "file_manifest_entry",
        "filename": "Exp_stud_NOTdup_Dryad.xls",
        "file_url": "https://datadryad.org/api/v2/files/21862/download",
        "primary_study_index_candidate": "false",
    }])
    assert read_manifest(manifest) == []
    assert inspect_manifest(manifest, download=lambda _url: (_ for _ in ()).throw(AssertionError("must not download xls"))) == []


def test_write_outputs_has_no_data_rows_or_identifiers(tmp_path) -> None:
    manifest = tmp_path / "manifest.csv"
    _write_manifest(manifest, [{
        "access_status": "file_manifest_entry",
        "filename": "Exp_stud_dup_Dryad.xlsx",
        "file_url": "https://datadryad.org/api/v2/files/21863/download",
        "primary_study_index_candidate": "false",
    }])
    rows = inspect_manifest(manifest, download=lambda _url: _xlsx_bytes(["Study_ID", "DOI"]))
    report = write_outputs(tmp_path / "out", rows)
    saved = json.loads((tmp_path / "out" / "d_a_caruso_xlsx_schema_report.json").read_text(encoding="utf-8"))
    written = list(csv.DictReader((tmp_path / "out" / "d_a_caruso_xlsx_schema.csv").open(encoding="utf-8")))
    assert report["sheets_with_bibliographic_identifier_columns"] == 1
    assert saved["next_action"] == "extract_bibliographic_identifiers_only"
    assert "effect_value" not in written[0]
    assert "example_doi" not in written[0]
