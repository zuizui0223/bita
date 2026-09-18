from __future__ import annotations

import io
import zipfile

from scripts.audit_sakhalkar2023_zenodo import summarize_archive


def _fake_archive() -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("project/data/visits.csv", "plant,visitor,role\nA,X,legitimate\n")
        archive.writestr("project/data/traits.csv", "plant,tube_length\nA,2.3\n")
        archive.writestr("project/R/analysis.R", "print('ok')\n")
        archive.writestr("project/README.md", "test")
    return buffer.getvalue()


def test_archive_inventory_reports_safe_file_metadata() -> None:
    report = summarize_archive(_fake_archive())
    assert report["archive_member_count"] == 4
    assert report["member_names"] == [
        "project/R/analysis.R",
        "project/README.md",
        "project/data/traits.csv",
        "project/data/visits.csv",
    ]
    assert report["csv_files"] == ["project/data/traits.csv", "project/data/visits.csv"]
    assert report["r_files"] == ["project/R/analysis.R"]
    assert report["readme_files"] == ["project/README.md"]
    assert report["total_uncompressed_bytes"] > 0


def test_archive_inventory_does_not_emit_file_contents() -> None:
    report = summarize_archive(_fake_archive())
    encoded = str(report)
    assert "legitimate" not in encoded
    assert "tube_length" not in encoded
    assert "print('ok')" not in encoded
