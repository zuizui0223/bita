"""Validate author-controlled metadata for the Ecology Letters access-routing Letter."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PATH = ROOT / "submission" / "ECOLOGY_LETTERS_LETTER_AUTHOR_METADATA_V1.json"
SCHEMA = "BITA_ECOLOGY_LETTERS_LETTER_AUTHOR_METADATA_V1"
ORCID_RE = re.compile(r"^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$")


def _text(value: object) -> str:
    return str(value or "").strip()


def validate(data: dict[str, object]) -> dict[str, object]:
    missing: list[str] = []
    invalid: list[str] = []

    if data.get("schema") != SCHEMA:
        invalid.append("schema")

    authors = data.get("authors")
    if not isinstance(authors, list) or not authors:
        missing.append("authors")
        authors = []

    affiliations = data.get("affiliations")
    if not isinstance(affiliations, dict) or not affiliations:
        missing.append("affiliations")
        affiliations = {}

    corresponding = 0
    for index, author in enumerate(authors, start=1):
        prefix = f"authors[{index}]"
        if not isinstance(author, dict):
            invalid.append(prefix)
            continue
        if not _text(author.get("name")):
            missing.append(f"{prefix}.name")
        ids = author.get("affiliation_ids")
        if not isinstance(ids, list) or not ids:
            missing.append(f"{prefix}.affiliation_ids")
        else:
            for aid in ids:
                if _text(aid) not in affiliations:
                    invalid.append(f"{prefix}.unknown_affiliation:{aid}")
        if not _text(author.get("email")):
            missing.append(f"{prefix}.email")
        orcid = _text(author.get("orcid"))
        if orcid and ORCID_RE.fullmatch(orcid) is None:
            invalid.append(f"{prefix}.orcid")
        if author.get("corresponding") is True:
            corresponding += 1

    if authors and corresponding != 1:
        invalid.append("exactly_one_corresponding_author")

    for aid, affiliation in affiliations.items():
        if not _text(aid) or not _text(affiliation):
            invalid.append(f"affiliations.{aid}")

    correspondence = data.get("correspondence")
    if not isinstance(correspondence, dict):
        missing.append("correspondence")
        correspondence = {}
    for key in ("postal_address", "telephone", "email"):
        if not _text(correspondence.get(key)):
            missing.append(f"correspondence.{key}")

    for key in (
        "authorship_statement",
        "funding_statement",
        "acknowledgments",
        "conflict_of_interest_statement",
        "ai_assisted_workflow_disclosure",
        "author_relative_novelty_statement",
        "archive_license",
    ):
        if not _text(data.get(key)):
            missing.append(key)

    for key in (
        "all_authors_approved_submitted_version",
        "not_under_consideration_elsewhere",
    ):
        if data.get(key) is not True:
            missing.append(key)

    status = "AUTHOR_METADATA_COMPLETE" if not missing and not invalid else "AUTHOR_METADATA_INCOMPLETE"
    return {
        "schema": SCHEMA,
        "status": status,
        "missing": sorted(set(missing)),
        "invalid": sorted(set(invalid)),
        "ready_for_submission_metadata_application": status == "AUTHOR_METADATA_COMPLETE",
    }


def run(path: Path, *, require_complete: bool = False) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("AUTHOR_METADATA_ROOT_MUST_BE_OBJECT")
    result = validate(data)
    if require_complete and result["status"] != "AUTHOR_METADATA_COMPLETE":
        problems = result["missing"] + result["invalid"]
        raise ValueError("AUTHOR_METADATA_INCOMPLETE:" + ",".join(problems))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=Path, default=DEFAULT_PATH)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run(args.path, require_complete=args.require_complete), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
