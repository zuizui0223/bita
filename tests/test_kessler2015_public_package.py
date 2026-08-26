from __future__ import annotations

import importlib.util
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_kessler2015_public_package.py"
SPEC = importlib.util.spec_from_file_location("kessler_package", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def test_package_audit_distinguishes_machine_files_from_figures(tmp_path: Path) -> None:
    package = tmp_path / "supp.zip"
    with zipfile.ZipFile(package, "w") as archive:
        archive.writestr("figure-supplement.pdf", b"pdf")
        archive.writestr("figure.png", b"png")
        archive.writestr("source-data.csv", "x,y\n1,2\n")
    report = MODULE.audit(package)
    assert report["file_count"] == 3
    assert report["machine_readable_candidate_count"] == 1
    assert report["machine_readable_candidates"][0]["path"] == "source-data.csv"


def test_zero_machine_candidates_is_not_overinterpreted(tmp_path: Path) -> None:
    package = tmp_path / "supp.zip"
    with zipfile.ZipFile(package, "w") as archive:
        archive.writestr("figure-supplement.pdf", b"pdf")
        archive.writestr("figure.tif", b"tif")
    report = MODULE.audit(package)
    assert report["machine_readable_candidate_count"] == 0
    assert "does not prove" in report["interpretation_rule"]
