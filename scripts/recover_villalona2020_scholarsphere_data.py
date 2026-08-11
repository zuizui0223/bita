"""Recover the public raw-data deposit for Villalona et al. 2020.

Article DOI: 10.1007/s00442-020-04701-0
Data DOI:    10.26207/pgeq-he51

The primary article declares this ScholarSphere deposit in its Data
availability statement. This utility resolves the data DOI, preserves the
landing page and machine-readable metadata it can reach, downloads every
non-HTML data file exposed by the deposit, and writes an auditable receipt.
It does not select contrasts or calculate effects.

Usage:
    python scripts/recover_villalona2020_scholarsphere_data.py OUTPUT_DIR
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import mimetypes
import re
import subprocess
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

ARTICLE_DOI = "10.1007/s00442-020-04701-0"
DATA_DOI = "10.26207/pgeq-he51"
DOI_URL = f"https://doi.org/{DATA_DOI}"
ARTICLE_URL = f"https://doi.org/{ARTICLE_DOI}"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/131 Safari/537.36"
DATA_SUFFIXES = {
    ".csv", ".tsv", ".txt", ".json", ".zip", ".xlsx", ".xls", ".r",
    ".rdata", ".rds", ".sav", ".jmp", ".dat", ".xml", ".yaml", ".yml",
}


def _request(url: str, *, accept: str = "*/*", referer: str | None = None) -> tuple[bytes, str, str]:
    headers = {"User-Agent": USER_AGENT, "Accept": accept}
    if referer:
        headers["Referer"] = referer
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read(), response.geturl(), response.headers.get("Content-Type", "")


def _curl(url: str, *, accept: str = "*/*", referer: str | None = None) -> tuple[bytes, str, str]:
    command = [
        "curl", "--fail", "--location", "--silent", "--show-error",
        "--max-time", "180", "--user-agent", USER_AGENT,
        "--header", f"Accept: {accept}",
        "--write-out", "\n__FINAL_URL__:%{url_effective}\n__CONTENT_TYPE__:%{content_type}",
    ]
    if referer:
        command += ["--referer", referer]
    command.append(url)
    completed = subprocess.run(command, check=True, capture_output=True)
    marker = b"\n__FINAL_URL__:"
    if marker not in completed.stdout:
        raise RuntimeError("curl response did not include final URL marker")
    payload, metadata = completed.stdout.rsplit(marker, 1)
    lines = metadata.decode("utf-8", errors="replace").splitlines()
    final_url = lines[0].strip()
    content_type = ""
    for line in lines[1:]:
        if line.startswith("__CONTENT_TYPE__:"):
            content_type = line.split(":", 1)[1].strip()
    return payload, final_url, content_type


def _fetch(url: str, *, accept: str = "*/*", referer: str | None = None) -> tuple[bytes, str, str, str]:
    errors: list[str] = []
    for method_name, method in (("urllib", _request), ("curl", _curl)):
        try:
            payload, final_url, content_type = method(url, accept=accept, referer=referer)
            return payload, final_url, content_type, method_name
        except Exception as error:  # pragma: no cover - network dependent
            errors.append(f"{method_name}: {error!r}")
    raise RuntimeError("; ".join(errors))


def _decoded_text(payload: bytes) -> str:
    return html.unescape(payload.decode("utf-8", errors="replace"))


def _normalise_embedded_text(text: str) -> str:
    return (
        text.replace("\\/", "/")
        .replace("\\u002F", "/")
        .replace("\\u002f", "/")
        .replace("&amp;", "&")
    )


def _all_strings(value: object) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from _all_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from _all_strings(item)


def _candidate_links(base_url: str, payload: bytes, content_type: str) -> list[str]:
    candidates: list[str] = []
    text = _normalise_embedded_text(_decoded_text(payload))

    for pattern in (
        r"(?:href|src|data-download-url|data-url|contentUrl)\s*=\s*[\"']([^\"']+)[\"']",
        r"https?://[^\s\"'<>]+",
    ):
        for match in re.findall(pattern, text, flags=re.IGNORECASE):
            candidates.append(urllib.parse.urljoin(base_url, match.rstrip(").,;")))

    if "json" in content_type.lower() or text.lstrip().startswith(("{", "[")):
        try:
            document = json.loads(text)
        except json.JSONDecodeError:
            document = None
        if document is not None:
            for value in _all_strings(document):
                value = _normalise_embedded_text(value)
                if value.startswith(("http://", "https://", "/")):
                    candidates.append(urllib.parse.urljoin(base_url, value))

    selected: list[str] = []
    for candidate in candidates:
        parsed = urllib.parse.urlsplit(candidate)
        suffix = Path(urllib.parse.unquote(parsed.path)).suffix.lower()
        lowered = candidate.lower()
        if (
            suffix in DATA_SUFFIXES
            or "/download" in lowered
            or "/files/" in lowered
            or "contenturl" in lowered
            or "file=" in lowered
        ):
            selected.append(candidate)
    return list(dict.fromkeys(selected))


def _looks_like_html(payload: bytes, content_type: str) -> bool:
    preview = payload[:500].lstrip().lower()
    return (
        "text/html" in content_type.lower()
        or preview.startswith((b"<!doctype html", b"<html", b"<head", b"<body"))
    )


def _safe_name(url: str, index: int, content_type: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    name = Path(urllib.parse.unquote(parsed.path)).name
    if not name or "." not in name:
        extension = mimetypes.guess_extension(content_type.split(";", 1)[0].strip()) or ".bin"
        name = f"file_{index:02d}{extension}"
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._")
    return name or f"file_{index:02d}.bin"


def _metadata_endpoints(landing_url: str) -> list[str]:
    parsed = urllib.parse.urlsplit(landing_url)
    path = parsed.path.rstrip("/")
    endpoints = [
        landing_url + ("&format=json" if "?" in landing_url else "?format=json"),
        urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, path + ".json", "", "")),
    ]
    match = re.search(r"/resources/([0-9a-fA-F-]{16,})", path)
    if match:
        identifier = match.group(1)
        endpoints.extend(
            [
                f"{parsed.scheme}://{parsed.netloc}/api/resources/{identifier}",
                f"{parsed.scheme}://{parsed.netloc}/api/public/resources/{identifier}",
                f"{parsed.scheme}://{parsed.netloc}/api/v1/resources/{identifier}",
            ]
        )
    return list(dict.fromkeys(endpoints))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir")
    args = parser.parse_args(argv)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    files_dir = output_dir / "files"
    files_dir.mkdir(parents=True, exist_ok=True)

    attempts: list[dict[str, object]] = []
    payload, landing_url, landing_type, landing_method = _fetch(
        DOI_URL,
        accept="text/html,application/xhtml+xml,application/json,*/*",
        referer=ARTICLE_URL,
    )
    (output_dir / "landing_page.html").write_bytes(payload)
    attempts.append(
        {
            "url": DOI_URL,
            "method": landing_method,
            "status": "landing_recovered",
            "final_url": landing_url,
            "content_type": landing_type,
            "bytes": len(payload),
        }
    )

    page_payloads: list[tuple[str, bytes, str]] = [(landing_url, payload, landing_type)]
    for endpoint in _metadata_endpoints(landing_url):
        try:
            metadata_payload, metadata_url, metadata_type, method = _fetch(
                endpoint,
                accept="application/json,text/html,*/*",
                referer=landing_url,
            )
        except Exception as error:  # pragma: no cover - network dependent
            attempts.append({"url": endpoint, "status": "metadata_failed", "error": repr(error)})
            continue
        suffix = "json" if "json" in metadata_type.lower() else "html"
        metadata_path = output_dir / f"metadata_{len(page_payloads):02d}.{suffix}"
        metadata_path.write_bytes(metadata_payload)
        page_payloads.append((metadata_url, metadata_payload, metadata_type))
        attempts.append(
            {
                "url": endpoint,
                "method": method,
                "status": "metadata_recovered",
                "final_url": metadata_url,
                "content_type": metadata_type,
                "bytes": len(metadata_payload),
            }
        )

    links: list[str] = []
    for page_url, page_payload, page_type in page_payloads:
        links.extend(_candidate_links(page_url, page_payload, page_type))
    links = list(dict.fromkeys(links))
    (output_dir / "candidate_links.json").write_text(
        json.dumps(links, indent=2) + "\n", encoding="utf-8"
    )

    recovered: list[dict[str, object]] = []
    used_names: set[str] = set()
    for index, link in enumerate(links, start=1):
        try:
            file_payload, final_url, content_type, method = _fetch(
                link,
                accept="text/csv,text/plain,application/zip,application/json,application/octet-stream,*/*",
                referer=landing_url,
            )
        except Exception as error:  # pragma: no cover - network dependent
            attempts.append({"url": link, "status": "file_failed", "error": repr(error)})
            continue
        if not file_payload or _looks_like_html(file_payload, content_type):
            attempts.append(
                {
                    "url": link,
                    "status": "not_data_file",
                    "final_url": final_url,
                    "content_type": content_type,
                    "bytes": len(file_payload),
                }
            )
            continue
        name = _safe_name(final_url, index, content_type)
        original = name
        counter = 2
        while name in used_names:
            stem = Path(original).stem
            suffix = Path(original).suffix
            name = f"{stem}_{counter}{suffix}"
            counter += 1
        used_names.add(name)
        path = files_dir / name
        path.write_bytes(file_payload)
        record = {
            "filename": name,
            "source_url": link,
            "final_url": final_url,
            "method": method,
            "content_type": content_type,
            "bytes": len(file_payload),
            "sha256": hashlib.sha256(file_payload).hexdigest(),
        }
        recovered.append(record)
        attempts.append({**record, "status": "data_file_recovered"})

    receipt = {
        "article_doi": ARTICLE_DOI,
        "data_doi": DATA_DOI,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "landing_url": landing_url,
        "landing_sha256": hashlib.sha256(payload).hexdigest(),
        "candidate_link_count": len(links),
        "recovered_file_count": len(recovered),
        "files": recovered,
        "attempts": attempts,
        "status": "source_data_recovered" if recovered else "landing_recovered_but_no_data_files",
        "interpretation_boundary": (
            "Files are preserved without selecting observations, contrasts, outcomes, or doses. "
            "Any analysis must still identify the experimental unit, repeated-measures structure, "
            "treatment orientation, outcome lane, and study dependence from the primary article."
        ),
    }
    (output_dir / "source_receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
