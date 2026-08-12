from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import tarfile
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "empirical" / "mechanism_pattern_synthesis" / "HAAS_DESMARAIS_2026_SUPPLEMENT_RECEIPT_V1.json"
PMCID = "PMC13095882"
ARTICLE_URL = f"https://pmc.ncbi.nlm.nih.gov/articles/{PMCID}/"
OUP_URL = "https://academic.oup.com/aob/article/137/4/879/8287317"
OA_API = f"https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id={PMCID}"
TARGET_FRAGMENT = "mcaf258"
UA = "bita-pattern-expansion/1.0 (+https://github.com/zuizui0223/bita)"


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def oa_package_candidates() -> tuple[list[str], list[dict[str, str]]]:
    attempts: list[dict[str, str]] = []
    urls: list[str] = []
    try:
        xml = fetch(OA_API).decode("utf-8", errors="replace")
        attempts.append({"url": OA_API, "state": "oa_api_success"})
        for href in re.findall(r'href=["\']([^"\']+)["\']', xml, re.I):
            if ".tar.gz" in href:
                # OA API historically returns ftp:// links; HTTPS works against the same host/path.
                if href.startswith("ftp://ftp.ncbi.nlm.nih.gov/"):
                    href = "https://ftp.ncbi.nlm.nih.gov/" + href.split("ftp://ftp.ncbi.nlm.nih.gov/", 1)[1]
                urls.append(href)
    except Exception as exc:
        attempts.append({"url": OA_API, "state": f"oa_api_error:{type(exc).__name__}:{exc}"})
    return urls, attempts


def inspect_xlsx(blob: bytes) -> dict[str, object]:
    import openpyxl  # type: ignore

    wb = openpyxl.load_workbook(io.BytesIO(blob), read_only=True, data_only=True)
    sheets = []
    for ws in wb.worksheets:
        first_rows = []
        for row in ws.iter_rows(min_row=1, max_row=min(ws.max_row, 4), values_only=True):
            first_rows.append([None if v is None else str(v)[:200] for v in row[:25]])
        sheets.append(
            {
                "title": ws.title,
                "max_row": ws.max_row,
                "max_column": ws.max_column,
                "first_rows": first_rows,
            }
        )
    return {"sheets": sheets}


def inspect_csv(blob: bytes) -> dict[str, object]:
    text = blob.decode("utf-8", errors="replace")
    reader = csv.reader(io.StringIO(text))
    rows = []
    for i, row in enumerate(reader):
        if i < 4:
            rows.append(row[:25])
        else:
            break
    line_count = text.count("\n") + (1 if text and not text.endswith("\n") else 0)
    return {"line_count": line_count, "first_rows": rows}


def inspect_blob(name: str, blob: bytes) -> dict[str, object]:
    suffix = Path(name).suffix.lower()
    item: dict[str, object] = {
        "name": name,
        "size": len(blob),
        "sha256": hashlib.sha256(blob).hexdigest(),
    }
    if suffix == ".xlsx":
        item["xlsx"] = inspect_xlsx(blob)
    elif suffix == ".csv":
        item["csv"] = inspect_csv(blob)
    elif suffix in {".r", ".txt", ".md"}:
        text = blob.decode("utf-8", errors="replace")
        item["text_head"] = text[:4000]
    elif suffix == ".zip" and blob[:4] == b"PK\x03\x04":
        nested = []
        with zipfile.ZipFile(io.BytesIO(blob)) as zf:
            for info in zf.infolist():
                if not info.is_dir():
                    nested.append(inspect_blob(f"{name}::{info.filename}", zf.read(info.filename)))
        item["nested_zip_entries"] = nested
    return item


def retrieve_from_oa_package() -> tuple[bytes, str, str, list[dict[str, str]], list[dict[str, object]]]:
    candidates, attempts = oa_package_candidates()
    for url in candidates:
        try:
            package = fetch(url)
            if package[:2] != b"\x1f\x8b":
                attempts.append({"url": url, "state": f"not_gzip_prefix:{package[:20]!r}"})
                continue
            entries: list[dict[str, object]] = []
            supplement_blobs: list[tuple[str, bytes]] = []
            with tarfile.open(fileobj=io.BytesIO(package), mode="r:gz") as tf:
                for member in tf.getmembers():
                    if not member.isfile():
                        continue
                    fh = tf.extractfile(member)
                    if fh is None:
                        continue
                    blob = fh.read()
                    lower = member.name.lower()
                    # Record only likely supplementary/data/code files in detail to keep receipt compact.
                    if any(lower.endswith(ext) for ext in (".zip", ".xlsx", ".xls", ".csv", ".r", ".txt", ".pdf")):
                        entries.append(inspect_blob(member.name, blob))
                    if TARGET_FRAGMENT in lower and ("supp" in lower or lower.endswith((".zip", ".xlsx", ".xls", ".csv", ".r"))):
                        supplement_blobs.append((member.name, blob))
            if not supplement_blobs:
                # The package itself is still a valid reproducibility object; require at least one likely supplement/data entry.
                supplement_blobs = [(str(e["name"]), b"") for e in entries if "supp" in str(e["name"]).lower()]
            if not entries:
                attempts.append({"url": url, "state": "oa_package_opened_but_no_data_like_entries"})
                continue
            attempts.append({"url": url, "state": "oa_package_success"})
            return package, url, "pmc_oa_tar_gz", attempts, entries
        except Exception as exc:
            attempts.append({"url": url, "state": f"oa_package_error:{type(exc).__name__}:{exc}"})
    raise RuntimeError("PMC OA package retrieval did not yield inspectable supplementary/data entries: " + json.dumps(attempts, indent=2))


def fallback_direct_zip() -> tuple[bytes, str, str, list[dict[str, str]], list[dict[str, object]]]:
    attempts: list[dict[str, str]] = []
    candidates: list[str] = []
    for page in (ARTICLE_URL, OUP_URL):
        try:
            html = fetch(page).decode("utf-8", errors="ignore")
        except Exception as exc:
            attempts.append({"url": page, "state": f"page_error:{type(exc).__name__}:{exc}"})
            continue
        for m in re.finditer(r'href=["\']([^"\']+)["\']', html, re.I):
            href = m.group(1).replace("&amp;", "&")
            decoded = urllib.parse.unquote(href).lower()
            if TARGET_FRAGMENT in decoded and ("supp" in decoded or ".zip" in decoded):
                candidates.append(urllib.parse.urljoin(page, href))
    seen: set[str] = set()
    for url in candidates:
        if url in seen:
            continue
        seen.add(url)
        try:
            blob = fetch(url)
            if blob[:4] != b"PK\x03\x04":
                attempts.append({"url": url, "state": f"not_zip_prefix:{blob[:20]!r}"})
                continue
            entries = []
            with zipfile.ZipFile(io.BytesIO(blob)) as zf:
                for info in zf.infolist():
                    if not info.is_dir():
                        entries.append(inspect_blob(info.filename, zf.read(info.filename)))
            attempts.append({"url": url, "state": "direct_zip_success"})
            return blob, url, "direct_zip", attempts, entries
        except Exception as exc:
            attempts.append({"url": url, "state": f"error:{type(exc).__name__}:{exc}"})
    raise RuntimeError("No direct supplement ZIP succeeded: " + json.dumps(attempts, indent=2))


def main() -> None:
    all_attempts: list[dict[str, str]] = []
    try:
        package, source_url, package_type, attempts, entries = retrieve_from_oa_package()
        all_attempts.extend(attempts)
    except Exception as oa_exc:
        all_attempts.append({"url": OA_API, "state": f"oa_route_failed:{type(oa_exc).__name__}:{oa_exc}"})
        package, source_url, package_type, attempts, entries = fallback_direct_zip()
        all_attempts.extend(attempts)

    package_sha = hashlib.sha256(package).hexdigest()
    names = [str(e["name"]) for e in entries]
    if not any("supp" in name.lower() or name.lower().endswith((".xlsx", ".xls", ".csv", ".r", ".zip")) for name in names):
        raise RuntimeError(f"Package retrieved but no recognizable supplement/data/code entry found: {names}")

    payload = {
        "status": "SUPPLEMENT_OR_OA_PACKAGE_RETRIEVED_AND_INSPECTED",
        "article_doi": "10.1093/aob/mcaf258",
        "pmcid": PMCID,
        "retrieval_url": source_url,
        "package_type": package_type,
        "package_size": len(package),
        "package_sha256": package_sha,
        "attempts": all_attempts,
        "entries": entries,
        "boundary": [
            "this receipt verifies deposited supplementary/OA package structure, not the published meta-analysis estimates by itself",
            "herbivory treatment is not the focal floral defence trait D",
            "no effect from this module is rho, iota, kappa, or W_AD",
        ],
    }
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "package_sha256": package_sha, "entries": names}, indent=2))


if __name__ == "__main__":
    main()
