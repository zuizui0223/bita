from __future__ import annotations

import io
import zipfile

import pytest

from scripts.audit_bita_peucedanum2025_huscap import (
    ARCHIVE, DOI, RESULT_SCHEMA, audit, inspect_zip,
)


def makezip(files):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zf:
        for name, contents in files.items():
            zf.writestr(name, contents)
    return buffer.getvalue()


def test_verified_schema_readout_does_not_claim_fitness_result():
    blob = makezip({
        "Data2025.csv": "population,perfect,male,predation\nP1,8,30,0.4\nP2,20,5,0.1\n",
        "README.txt": "Research data notes\n",
        "analysis.R": "print('synthetic')",
    })
    result = audit(fetcher=lambda: blob)
    assert result["receipt_schema"] == RESULT_SCHEMA
    assert result["doi"] == DOI == "10.14943/hu95572"
    assert result["status"] == "SOURCE_ZIP_VERIFIED_SCHEMA_LISTED"
    assert result["entries_n"] == 3
    assert result["supported_readable_tables"] == 2
    assert not result["raw_data_redistributed"]
    assert not result["statistical_result_computed"]
    assert result["zip_sha256"]


def test_wrong_html_page_fails_closed():
    result = audit(fetcher=lambda: b"<html>cloudflare challenge</html>")
    assert result["status"] == "SOURCE_NOT_VERIFIED"
    assert not result["statistical_result_computed"]
    assert "zip_sha256" not in result


def test_no_untrusted_path_extraction():
    with pytest.raises(ValueError, match="UNSAFE"):
        inspect_zip(makezip({"../bad.csv": "a\n1\n"}))


def test_empty_and_truncated_files_rejected():
    with pytest.raises(ValueError):
        inspect_zip(makezip({}))
    with pytest.raises((ValueError, zipfile.BadZipFile)):
        inspect_zip(b"PKbrokenzip")


def test_paper_source_is_2025_huscap_not_older_dryad():
    assert "/95572/" in ARCHIVE
    assert "2025" in audit(fetcher=lambda: b"html")["source_paper"]
    assert "dryad" not in ARCHIVE.lower()
