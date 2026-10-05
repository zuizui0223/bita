"""Reserve a Zenodo DOI for the access-routing Letter without publishing.

Uses Zenodo's legacy deposit API because creating an empty deposition returns a
stable prereserved DOI before full metadata and files are supplied. The access
token is read only from ZENODO_ACCESS_TOKEN and is never written to disk.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
API_URL = "https://zenodo.org/api/deposit/depositions"
DOI_RE = re.compile(r"^10\.5281/zenodo\.\d+$", re.IGNORECASE)
RESERVED_RECEIPT = ROOT / "submission" / "access_routing_archive" / "RESERVED_DOI_RECEIPT.json"
DRAFT_RECEIPT = ROOT / "submission" / "access_routing_archive" / "ZENODO_DRAFT_RECEIPT.json"


def _request_json(url: str, token: str) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=b"{}",
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "bita-access-routing-archive/1",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = response.read().decode("utf-8")
            if response.status != 201:
                raise RuntimeError(f"ZENODO_CREATE_UNEXPECTED_STATUS:{response.status}")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"ZENODO_CREATE_HTTP_ERROR:{exc.code}:{body[:500]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"ZENODO_CREATE_NETWORK_ERROR:{exc.reason}") from exc

    parsed = json.loads(payload)
    if not isinstance(parsed, dict):
        raise RuntimeError("ZENODO_CREATE_RESPONSE_NOT_OBJECT")
    return parsed


def extract_reserved_doi(deposition: dict[str, Any]) -> str:
    metadata = deposition.get("metadata")
    if not isinstance(metadata, dict):
        raise RuntimeError("ZENODO_CREATE_RESPONSE_MISSING_METADATA")
    prereserve = metadata.get("prereserve_doi")
    if not isinstance(prereserve, dict):
        raise RuntimeError("ZENODO_CREATE_RESPONSE_MISSING_PRERESERVE_DOI")
    doi = str(prereserve.get("doi", "")).strip()
    if DOI_RE.fullmatch(doi) is None:
        raise RuntimeError(f"ZENODO_RESERVED_DOI_INVALID:{doi}")
    return doi


def build_draft_receipt(deposition: dict[str, Any], doi: str) -> dict[str, Any]:
    dep_id = deposition.get("id")
    if not isinstance(dep_id, int):
        raise RuntimeError("ZENODO_CREATE_RESPONSE_MISSING_DEPOSITION_ID")
    links = deposition.get("links") if isinstance(deposition.get("links"), dict) else {}
    return {
        "receipt": "BITA_ACCESS_ROUTING_ZENODO_DRAFT_V1",
        "status": "ZENODO_DRAFT_CREATED_DOI_RESERVED_NOT_PUBLISHED",
        "deposition_id": dep_id,
        "reserved_doi": doi,
        "draft_url": links.get("html"),
        "api_self": links.get("self"),
        "submitted": bool(deposition.get("submitted", False)),
        "publication_performed": False,
    }


def _apply_reserved_doi(doi: str) -> None:
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "apply_reserved_archive_doi.py"),
            "--doi",
            doi,
        ],
        cwd=ROOT,
        check=True,
    )


def main() -> int:
    if RESERVED_RECEIPT.is_file():
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "apply_reserved_archive_doi.py"),
                "--check-only",
            ],
            cwd=ROOT,
            check=True,
        )
        existing = json.loads(RESERVED_RECEIPT.read_text(encoding="utf-8"))
        print(json.dumps({
            "status": "ALREADY_RESERVED",
            "doi": existing.get("doi"),
            "created_new_draft": False,
        }, indent=2, sort_keys=True))
        return 0

    token = os.environ.get("ZENODO_ACCESS_TOKEN", "").strip()
    if not token:
        raise SystemExit(
            "ZENODO_ACCESS_TOKEN_MISSING: add a Zenodo personal access token with "
            "deposit:write scope as a GitHub Actions repository secret."
        )

    deposition = _request_json(API_URL, token)
    doi = extract_reserved_doi(deposition)
    receipt = build_draft_receipt(deposition, doi)

    # Freeze the DOI into all submission surfaces before any archive is built.
    _apply_reserved_doi(doi)

    DRAFT_RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    DRAFT_RECEIPT.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "status": receipt["status"],
        "doi": doi,
        "deposition_id": receipt["deposition_id"],
        "draft_url": receipt["draft_url"],
        "created_new_draft": True,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
