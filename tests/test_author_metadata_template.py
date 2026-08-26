from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "submission" / "AUTHOR_METADATA_INPUT_TEMPLATE.json"
SCRIPT = ROOT / "scripts" / "validate_author_metadata.py"

spec = importlib.util.spec_from_file_location("metadata_validator", SCRIPT)
assert spec and spec.loader
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def test_author_metadata_template_is_schema_valid_but_intentionally_incomplete() -> None:
    data = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    assert validator.schema_errors(data) == []
    errors = validator.completeness_errors(data)
    assert errors
    assert any("exactly one author" in error for error in errors)
    assert any("repository_licence_statement" in error for error in errors)
    assert any("not_under_consideration_elsewhere" in error for error in errors)


def test_complete_minimal_metadata_passes() -> None:
    data = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    data["authors"] = [
        {
            "publication_name": "Example Author",
            "affiliations": ["Example University"],
            "present_address": "",
            "orcid": "N/A",
            "email": "author@example.org",
            "corresponding": True,
            "credit_roles": ["Conceptualization", "Writing – original draft"],
        }
    ]
    data["corresponding_author"] = {
        "publication_name": "Example Author",
        "email": "author@example.org",
    }
    data["funding"]["statement"] = "No external funding."
    data["competing_interests"]["statement"] = "The author declares no competing interests."
    data["repository_licence_statement"] = "Repository licence confirmed by the author."
    for key in validator.CONFIRMATION_KEYS:
        data["submission_confirmations"][key] = True

    assert validator.schema_errors(data) == []
    assert validator.completeness_errors(data) == []
