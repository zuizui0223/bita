"""Validate the single machine-readable author/submission metadata input.

Schema validation is safe to run in CI while the template is incomplete.
Use --require-complete only for the final author-approved submission input.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "submission" / "AUTHOR_METADATA_INPUT_TEMPLATE.json"

AUTHOR_KEYS = {
    "publication_name",
    "affiliations",
    "present_address",
    "orcid",
    "email",
    "corresponding",
    "credit_roles",
}
TOP_KEYS = {
    "authors",
    "corresponding_author",
    "funding",
    "acknowledgments",
    "competing_interests",
    "repository_licence_statement",
    "submission_confirmations",
    "reviewers",
    "opposed_reviewers",
}
CONFIRMATION_KEYS = {
    "all_authors_approve_exact_version",
    "all_authors_agree_to_ecology_submission",
    "not_under_consideration_elsewhere",
}


def load(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("metadata root must be a JSON object")
    return data


def schema_errors(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = TOP_KEYS - data.keys()
    if missing:
        errors.append("missing top-level keys: " + ", ".join(sorted(missing)))

    authors = data.get("authors")
    if not isinstance(authors, list) or not authors:
        errors.append("authors must be a non-empty list")
    else:
        for i, author in enumerate(authors):
            if not isinstance(author, dict):
                errors.append(f"authors[{i}] must be an object")
                continue
            absent = AUTHOR_KEYS - author.keys()
            if absent:
                errors.append(f"authors[{i}] missing keys: " + ", ".join(sorted(absent)))
            if "affiliations" in author and not isinstance(author["affiliations"], list):
                errors.append(f"authors[{i}].affiliations must be a list")
            if "credit_roles" in author and not isinstance(author["credit_roles"], list):
                errors.append(f"authors[{i}].credit_roles must be a list")
            if "corresponding" in author and not isinstance(author["corresponding"], bool):
                errors.append(f"authors[{i}].corresponding must be boolean")

    confirmations = data.get("submission_confirmations")
    if not isinstance(confirmations, dict):
        errors.append("submission_confirmations must be an object")
    else:
        absent = CONFIRMATION_KEYS - confirmations.keys()
        if absent:
            errors.append("submission_confirmations missing keys: " + ", ".join(sorted(absent)))
        for key in CONFIRMATION_KEYS & confirmations.keys():
            if confirmations[key] not in (True, False, None):
                errors.append(f"submission_confirmations.{key} must be true, false, or null")

    for key in ("reviewers", "opposed_reviewers"):
        if key in data and not isinstance(data[key], list):
            errors.append(f"{key} must be a list")
    return errors


def _blank(value: Any) -> bool:
    return value is None or value == "" or value == []


def completeness_errors(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    authors = data.get("authors", [])
    corresponding_indices: list[int] = []
    for i, author in enumerate(authors):
        for field in ("publication_name", "affiliations", "email", "credit_roles"):
            if _blank(author.get(field)):
                errors.append(f"authors[{i}].{field} is incomplete")
        if author.get("corresponding") is True:
            corresponding_indices.append(i)

    if len(corresponding_indices) != 1:
        errors.append("exactly one author must have corresponding=true")

    ca = data.get("corresponding_author", {})
    for field in ("publication_name", "email"):
        if _blank(ca.get(field)):
            errors.append(f"corresponding_author.{field} is incomplete")

    funding = data.get("funding", {})
    if _blank(funding.get("statement")):
        errors.append("funding.statement is incomplete; use an explicit no-funding statement when applicable")

    ci = data.get("competing_interests", {})
    if _blank(ci.get("statement")):
        errors.append("competing_interests.statement is incomplete")

    if _blank(data.get("repository_licence_statement")):
        errors.append("repository_licence_statement is incomplete")

    confirmations = data.get("submission_confirmations", {})
    for key in CONFIRMATION_KEYS:
        if confirmations.get(key) is not True:
            errors.append(f"submission_confirmations.{key} must be explicitly true")

    if len(corresponding_indices) == 1:
        author = authors[corresponding_indices[0]]
        if ca.get("publication_name") != author.get("publication_name"):
            errors.append("corresponding_author.publication_name does not match the corresponding author entry")
        if ca.get("email") != author.get("email"):
            errors.append("corresponding_author.email does not match the corresponding author entry")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()

    data = load(args.path)
    errors = schema_errors(data)
    if args.require_complete and not errors:
        errors.extend(completeness_errors(data))

    if errors:
        print("Metadata validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    mode = "complete" if args.require_complete else "schema"
    print(f"Metadata {mode} validation passed: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
