"""Recover the public ScholarSphere data package for Villalona et al. 2020.

The primary article states that study data are available at
https://doi.org/10.26207/pgeq-he51. This utility resolves that DOI, preserves the
landing-page and DataCite metadata, discovers repository file links, and
retrieves every non-HTML file it can validate.

This is source recovery only. Downloaded tables are not promoted into the
strict-B effect layer until trial, species, dose, time, experimental unit,
outcome, and dependence are audited.

Usage:
    python scripts/recover_villalona2020_scholarsphere.py OUTPUT_DIR
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DATA_DOI = "10.26207/pgeq-he51"
DOI_URL = f"https://doi.org/{DATA_DOI}"
DATACITE_URL = f"https://api.datacite.org/dois/{DATA_DOI}"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/131 Safari/537.36"
FILE_SUFFIXES = (
    ".csv", ".tsv", ".txt", ".xlsx", ".xls", ".zip", ".rds", ".rda",
    ".json", ".sav", ".dta", ".docx",
)


def _request(url: str, *, accept: str = "text/html,*/*") -> tuple[bytes, str, str]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": accept},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        payload = response.read()
        final_url = response.geturl()
        content_type = response.headers.get("Content-Type", "")
    return payload, final_url, content_type


def _curl(url: str, *, accept: str = "text/html,*/*") -> tuple[bytes, str, str]:
    marker = "__BITA_FINAL_URL__"
    command = [
        "curl", "--fail", "--location", "--silent", "--show-error",
        "--max-time", "180", "--user-agent", USER_AGENT,
        "--header", f"Accept: {accept}",
        "--write-out", f"\n{marker}%{{url_effective}}\t%{{content_type}}",
        url,
    ]
    completed = subprocess.run(command, check=True, capture_output=True)
    output = completed.stdout
    split = output.rsplit(f"\n{marker}".encode(), 1)
    if len(split) != 2:
        raise RuntimeError("curl response did not contain final-url marker")
    payload, trailer = split
    final_url, _, content_type = trailer.decode("utf-8", errors="replace").partition("\t")
    return payload, final_url.strip(), content_type.strip()


def _retrieve(url: str, *, accept: str = "text/html,*/*") -> tuple[bytes, str, str, list[dict[str, object]]]:
    attempts: list[dict[str, object]] = []
    for method_name, method in (("urllib", _request), ("curl", _curl)):
        try:
            payload, final_url, content_type = method(url, accept=accept)
        except Exception as error:  # pragma: no cover - network dependent
            attempts.append({"url": url, "method": method_name, "status": "failed", "error": repr(error)})
            continue
        attempts.append(
            {
                "url": url,
                "method": method_name,
                "status": "retrieved",
                "final_url": final_url,
                "content_type": content_type,
                "bytes": len(payload),
            }
        )
        return payload, final_url, content_type, attempts
    raise RuntimeError(json.dumps({"message": f"could not retrieve {url}", "attempts": attempts}, indent=2))


def _looks_like_html(payload: bytes, content_type: str = "") -> bool:
    if "html" in content_type.lower():
        return True
    preview = payload[:1000].lstrip().lower()
    return preview.startswith((b"<!doctype html", b"<html", b"<?xml"))


def _candidate_links(base_url: str, payload: bytes) -> list[str]:
    text = html.unescape(payload.decode("utf-8", errors="replace"))
    hrefs = re.findall(r"(?:href|src)=[\"']([^\"']+)[\"']", text, flags=re.IGNORECASE)
    # Also catch URLs embedded in JSON-LD, React state, or escaped script data.
    hrefs.extend(re.findall(r"https?:\\?/\\?/[^\"'<>\\s]+", text))
    candidates: list[str] = []
    for raw in hrefs:
        raw = raw.replace("\\/", "/")
        absolute = urllib.parse.urljoin(base_url, raw)
        lowered = urllib.parse.urlsplit(absolute).path.lower()
        query = urllib.parse.urlsplit(absolute).query.lower()
        if (
            lowered.endswith(FILE_SUFFIXES)
            or "/download" in lowered
            or "/downloads/" in lowered
            or "/files/" in lowered
            or "/file_sets/" in lowered
            or "download=" in query
            or "filename=" in query
        ):
            candidates.append(absolute)
    return list(dict.fromkeys(candidates))


def _safe_name(url: str, index: int) -> str:
    parsed = urllib.parse.urlsplit(url)
    name = Path(urllib.parse.unquote(parsed.path)).name
    if not name or "." not in name:
        query = urllib.parse.parse_qs(parsed.query)
        for key in ("filename", "file", "download"):
            if query.get(key):
                name = Path(query[key][0]).name
                break
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("_")
    return cleaned or f"repository_file_{index:02d}.bin"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir")
    args = parser.parse_args(argv)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    files_dir = output_dir / "files"
    files_dir.mkdir(parents=True, exist_ok=True)

    attempts: list[dict[str, object]] = []
    landing, final_url, landing_type, current_attempts = _retrieve(DOI_URL)
    attempts.extend(current_attempts)
    (output_dir / "landing_page.html").write_bytes(landing)

    metadata_payload = b""
    metadata_final_url = DATACITE_URL
    metadata_type = ""
    try:
        metadata_payload, metadata_final_url, metadata_type, current_attempts = _retrieve(
            DATACITE_URL, accept="application/vnd.api+json,application/json,*/*"
        )
        attempts.extend(current_attempts)
        (output_dir / "datacite_metadata.json").write_bytes(metadata_payload)
    except Exception as error:  # pragma: no cover - network dependent
        attempts.append({"url": DATACITE_URL, "status": "metadata_failed", "error": repr(error)})

    candidates = _candidate_links(final_url, landing)
    # DataCite metadata can carry the repository URL or direct content URLs.
    if metadata_payload:
        candidates.extend(_candidate_links(metadata_final_url, metadata_payload))
    candidates = list(dict.fromkeys(candidates))

    recovered: list[dict[str, object]] = []
    rejected: list[dict[str, object]] = []
    for index, candidate in enumerate(candidates, start=1):
        try:
            payload, candidate_final, content_type, current_attempts = _retrieve(
                candidate, accept="text/csv,text/plain,application/octet-stream,application/zip,*/*"
            )
            attempts.extend(current_attempts)
        except Exception as error:  # pragma: no cover - network dependent
            rejected.append({"url": candidate, "status": "download_failed", "error": repr(error)})
            continue
        if not payload or _looks_like_html(payload, content_type):
            rejected.append(
                {
                    "url": candidate,
                    "final_url": candidate_final,
                    "status": "html_or_empty",
                    "content_type": content_type,
                    "bytes": len(payload),
                }
            )
            continue
        filename = _safe_name(candidate_final, index)
        path = files_dir / filename
        if path.exists():
            path = files_dir / f"{index:02d}_{filename}"
        path.write_bytes(payload)
        recovered.append(
            {
                "candidate_url": candidate,
                "source_url": candidate_final,
                "filename": path.name,
                "content_type": content_type,
                "bytes": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
            }
        )

    receipt = {
        "article_doi": "10.1007/s00442-020-04701-0",
        "data_doi": DATA_DOI,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "landing_final_url": final_url,
        "landing_content_type": landing_type,
        "landing_sha256": hashlib.sha256(landing).hexdigest(),
        "candidate_link_count": len(candidates),
        "candidate_links": candidates,
        "recovered_file_count": len(recovered),
        "recovered_files": recovered,
        "rejected_candidates": rejected,
        "attempts": attempts,
        "interpretation_boundary": (
            "Repository files are preserved without selecting effects. Data must still be "
            "mapped to Villalona trial, bee species, dose, time, experimental unit, outcome "
            "lane, B-role provenance, and study dependence before quantitative use."
        ),
    }
    (output_dir / "source_receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))
    # A source audit is useful even if the landing page exposes no directly downloadable file.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
