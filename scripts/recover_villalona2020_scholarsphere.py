"""Recover the public ScholarSphere data package for Villalona et al. 2020.

The primary article states that study data are available at
https://doi.org/10.26207/pgeq-he51. This utility resolves that DOI, preserves the
landing page and DataCite metadata, follows ScholarSphere's download handoff,
and retrieves every validated non-HTML file it can reach.

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
import http.cookiejar
import json
import mimetypes
import re
import subprocess
import urllib.parse
import urllib.request
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

DATA_DOI = "10.26207/pgeq-he51"
DOI_URL = f"https://doi.org/{DATA_DOI}"
DATACITE_URL = f"https://api.datacite.org/dois/{DATA_DOI}"
ARTICLE_URL = "https://doi.org/10.1007/s00442-020-04701-0"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/131 Safari/537.36"
FILE_SUFFIXES = {
    ".csv", ".tsv", ".txt", ".xlsx", ".xls", ".zip", ".rds", ".rda",
    ".json", ".sav", ".dta", ".docx", ".r", ".xml", ".dat", ".jmp",
}
MAX_CANDIDATES = 100

_COOKIE_JAR = http.cookiejar.CookieJar()
_OPENER = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(_COOKIE_JAR))


def _request(
    url: str,
    *,
    accept: str = "text/html,*/*",
    referer: str | None = None,
) -> tuple[bytes, str, dict[str, str]]:
    headers = {"User-Agent": USER_AGENT, "Accept": accept}
    if referer:
        headers["Referer"] = referer
    request = urllib.request.Request(url, headers=headers)
    with _OPENER.open(request, timeout=120) as response:
        payload = response.read()
        response_headers = {key.lower(): value for key, value in response.headers.items()}
        return payload, response.geturl(), response_headers


def _curl(
    url: str,
    *,
    accept: str = "text/html,*/*",
    referer: str | None = None,
) -> tuple[bytes, str, dict[str, str]]:
    marker = "__BITA_FINAL_URL__"
    command = [
        "curl", "--fail", "--location", "--silent", "--show-error",
        "--max-time", "180", "--user-agent", USER_AGENT,
        "--header", f"Accept: {accept}",
        "--write-out", f"\n{marker}%{{url_effective}}\t%{{content_type}}",
    ]
    if referer:
        command += ["--referer", referer]
    command.append(url)
    completed = subprocess.run(command, check=True, capture_output=True)
    output = completed.stdout
    split = output.rsplit(f"\n{marker}".encode(), 1)
    if len(split) != 2:
        raise RuntimeError("curl response did not contain final-url marker")
    payload, trailer = split
    final_url, _, content_type = trailer.decode("utf-8", errors="replace").partition("\t")
    return payload, final_url.strip(), {"content-type": content_type.strip()}


def _retrieve(
    url: str,
    *,
    accept: str = "text/html,*/*",
    referer: str | None = None,
) -> tuple[bytes, str, dict[str, str], list[dict[str, object]]]:
    attempts: list[dict[str, object]] = []
    for method_name, method in (("urllib", _request), ("curl", _curl)):
        try:
            payload, final_url, headers = method(url, accept=accept, referer=referer)
        except Exception as error:  # pragma: no cover - network dependent
            attempts.append(
                {"url": url, "method": method_name, "status": "failed", "error": repr(error)}
            )
            continue
        attempts.append(
            {
                "url": url,
                "method": method_name,
                "status": "retrieved",
                "final_url": final_url,
                "content_type": headers.get("content-type", ""),
                "content_disposition": headers.get("content-disposition", ""),
                "bytes": len(payload),
            }
        )
        return payload, final_url, headers, attempts
    raise RuntimeError(json.dumps({"message": f"could not retrieve {url}", "attempts": attempts}, indent=2))


def _looks_like_html(payload: bytes, content_type: str = "") -> bool:
    if "html" in content_type.lower():
        return True
    preview = payload[:1000].lstrip().lower()
    return preview.startswith((b"<!doctype html", b"<html", b"<head", b"<body"))


def _normalise_embedded_url(value: str) -> str:
    return html.unescape(value).replace("\\/", "/").replace("\\u002F", "/").replace("\\u002f", "/")


def _candidate_links(base_url: str, payload: bytes, *, broad: bool = False) -> list[str]:
    text = _normalise_embedded_url(payload.decode("utf-8", errors="replace"))
    raw_links: list[str] = []
    patterns = (
        r"(?:href|src|action|data-download-url|data-url|contentUrl)\s*=\s*[\"']([^\"']+)[\"']",
        r"(?:url|location(?:\.href)?)\s*[:=]\s*[\"']([^\"']+)[\"']",
        r"https?://[^\s\"'<>]+",
    )
    for pattern in patterns:
        raw_links.extend(re.findall(pattern, text, flags=re.IGNORECASE))
    for content in re.findall(r"<meta[^>]+http-equiv=[\"']?refresh[\"']?[^>]+content=[\"']([^\"']+)[\"']", text, flags=re.IGNORECASE):
        match = re.search(r"url\s*=\s*(.+)$", content, flags=re.IGNORECASE)
        if match:
            raw_links.append(match.group(1).strip(" '\""))

    candidates: list[str] = []
    for raw in raw_links:
        raw = _normalise_embedded_url(raw).rstrip(").,;")
        absolute = urllib.parse.urljoin(base_url, raw)
        parsed = urllib.parse.urlsplit(absolute)
        suffix = Path(urllib.parse.unquote(parsed.path)).suffix.lower()
        lowered_path = parsed.path.lower()
        lowered_query = parsed.query.lower()
        selected = (
            suffix in FILE_SUFFIXES
            or "/download" in lowered_path
            or "/downloads/" in lowered_path
            or "/files/" in lowered_path
            or "/file_sets/" in lowered_path
            or "/rails/active_storage/" in lowered_path
            or "download=" in lowered_query
            or "filename=" in lowered_query
            or "download_token=" in lowered_query
        )
        if broad or selected:
            if parsed.scheme in {"http", "https"}:
                candidates.append(absolute)
    return list(dict.fromkeys(candidates))


def _download_variants(url: str) -> list[str]:
    variants = [url]
    parsed = urllib.parse.urlsplit(url)
    query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    existing = {key for key, _ in query}
    for key, value in (("download", "1"), ("raw", "1"), ("attachment", "1")):
        if key not in existing:
            variants.append(
                urllib.parse.urlunsplit(
                    (parsed.scheme, parsed.netloc, parsed.path, urllib.parse.urlencode(query + [(key, value)]), parsed.fragment)
                )
            )
    match = re.search(r"/resources/[^/]+/downloads/(\d+)", parsed.path)
    if match:
        file_id = match.group(1)
        variants.extend(
            [
                f"{parsed.scheme}://{parsed.netloc}/downloads/{file_id}",
                f"{parsed.scheme}://{parsed.netloc}/downloads/{file_id}?download=1",
            ]
        )
    return list(dict.fromkeys(variants))


def _name_from_disposition(disposition: str) -> str:
    match = re.search(r"filename\*?=(?:UTF-8''|[\"']?)([^\"';]+)", disposition, flags=re.IGNORECASE)
    return urllib.parse.unquote(match.group(1)) if match else ""


def _safe_name(url: str, index: int, headers: dict[str, str]) -> str:
    name = _name_from_disposition(headers.get("content-disposition", ""))
    parsed = urllib.parse.urlsplit(url)
    if not name:
        name = Path(urllib.parse.unquote(parsed.path)).name
    if not name or "." not in name:
        query = urllib.parse.parse_qs(parsed.query)
        for key in ("filename", "file", "download"):
            if query.get(key):
                name = Path(query[key][0]).name
                break
    if not name or "." not in name:
        mime = headers.get("content-type", "").split(";", 1)[0].strip()
        extension = mimetypes.guess_extension(mime) or ".bin"
        name = f"repository_file_{index:02d}{extension}"
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._")
    return cleaned or f"repository_file_{index:02d}.bin"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir")
    args = parser.parse_args(argv)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    files_dir = output_dir / "files"
    previews_dir = output_dir / "html_previews"
    files_dir.mkdir(parents=True, exist_ok=True)
    previews_dir.mkdir(parents=True, exist_ok=True)

    attempts: list[dict[str, object]] = []
    landing, landing_url, landing_headers, current_attempts = _retrieve(
        DOI_URL, accept="text/html,application/xhtml+xml,application/json,*/*", referer=ARTICLE_URL
    )
    attempts.extend(current_attempts)
    (output_dir / "landing_page.html").write_bytes(landing)

    metadata_payload = b""
    metadata_url = DATACITE_URL
    try:
        metadata_payload, metadata_url, _, current_attempts = _retrieve(
            DATACITE_URL,
            accept="application/vnd.api+json,application/json,*/*",
            referer=landing_url,
        )
        attempts.extend(current_attempts)
        (output_dir / "datacite_metadata.json").write_bytes(metadata_payload)
    except Exception as error:  # pragma: no cover - network dependent
        attempts.append({"url": DATACITE_URL, "status": "metadata_failed", "error": repr(error)})

    initial = _candidate_links(landing_url, landing)
    if metadata_payload:
        initial.extend(_candidate_links(metadata_url, metadata_payload))
    queue: deque[tuple[str, str]] = deque((url, landing_url) for url in dict.fromkeys(initial))
    queued = {url for url, _ in queue}
    visited: set[str] = set()
    recovered: list[dict[str, object]] = []
    rejected: list[dict[str, object]] = []
    used_names: set[str] = set()
    preview_index = 0

    while queue and len(visited) < MAX_CANDIDATES:
        candidate, referer = queue.popleft()
        if candidate in visited:
            continue
        visited.add(candidate)
        success = False
        for variant in _download_variants(candidate):
            if variant != candidate and variant in visited:
                continue
            if variant != candidate:
                visited.add(variant)
            try:
                payload, final_url, headers, current_attempts = _retrieve(
                    variant,
                    accept="application/octet-stream,application/zip,text/csv,text/plain,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,*/*",
                    referer=referer,
                )
                attempts.extend(current_attempts)
            except Exception as error:  # pragma: no cover - network dependent
                rejected.append({"url": variant, "status": "download_failed", "error": repr(error)})
                continue
            content_type = headers.get("content-type", "")
            if payload and not _looks_like_html(payload, content_type):
                name = _safe_name(final_url, len(recovered) + 1, headers)
                original = name
                counter = 2
                while name in used_names:
                    stem = Path(original).stem
                    suffix = Path(original).suffix
                    name = f"{stem}_{counter}{suffix}"
                    counter += 1
                used_names.add(name)
                path = files_dir / name
                path.write_bytes(payload)
                recovered.append(
                    {
                        "candidate_url": candidate,
                        "retrieved_variant": variant,
                        "source_url": final_url,
                        "filename": name,
                        "content_type": content_type,
                        "bytes": len(payload),
                        "sha256": hashlib.sha256(payload).hexdigest(),
                    }
                )
                success = True
                break

            preview_index += 1
            preview_path = previews_dir / f"preview_{preview_index:02d}.html"
            preview_path.write_bytes(payload)
            nested = _candidate_links(final_url, payload, broad=True)
            for nested_url in nested:
                if nested_url not in queued and nested_url not in visited:
                    queue.append((nested_url, final_url))
                    queued.add(nested_url)
            rejected.append(
                {
                    "url": variant,
                    "final_url": final_url,
                    "status": "html_or_empty",
                    "content_type": content_type,
                    "bytes": len(payload),
                    "saved_preview": str(preview_path.relative_to(output_dir)),
                    "nested_candidate_count": len(nested),
                }
            )
        if success:
            continue

    receipt = {
        "article_doi": "10.1007/s00442-020-04701-0",
        "data_doi": DATA_DOI,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "landing_final_url": landing_url,
        "landing_content_type": landing_headers.get("content-type", ""),
        "landing_sha256": hashlib.sha256(landing).hexdigest(),
        "initial_candidate_count": len(initial),
        "visited_candidate_count": len(visited),
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
