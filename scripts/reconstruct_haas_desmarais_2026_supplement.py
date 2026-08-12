from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "empirical" / "mechanism_pattern_synthesis" / "HAAS_DESMARAIS_2026_SUPPLEMENT_RECEIPT_V1.json"
PMCID = "PMC13095882"
ARTICLE_URL = f"https://pmc.ncbi.nlm.nih.gov/articles/{PMCID}/"
OUP_URL = "https://academic.oup.com/aob/article/137/4/879/8287317"
TARGET_NAME = "mcaf258_supplementary_data.zip"
UA = "bita-pattern-expansion/1.0 (+https://github.com/zuizui0223/bita)"


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=45) as resp:
        return resp.read()


def find_download_candidates() -> list[str]:
    candidates = [
        f"https://pmc.ncbi.nlm.nih.gov/articles/{PMCID}/bin/{TARGET_NAME}",
        f"https://pmc.ncbi.nlm.nih.gov/articles/{PMCID}/bin/{TARGET_NAME}?download=1",
        f"https://pmc.ncbi.nlm.nih.gov/articles/instance/13095882/bin/{TARGET_NAME}",
    ]

    for page in (ARTICLE_URL, OUP_URL):
        try:
            html = fetch(page).decode("utf-8", errors="ignore")
        except Exception:
            continue
        # Capture absolute or relative hrefs that name the supplement zip.
        for m in re.finditer(r'href=["\']([^"\']*mcaf258_supplementary_data\.zip[^"\']*)["\']', html, re.I):
            candidates.append(urllib.parse.urljoin(page, m.group(1).replace("&amp;", "&")))

    # Stable de-duplication.
    seen: set[str] = set()
    out: list[str] = []
    for url in candidates:
        if url not in seen:
            seen.add(url)
            out.append(url)
    return out


def download_zip() -> tuple[bytes, str, list[dict[str, str]]]:
    attempts: list[dict[str, str]] = []
    for url in find_download_candidates():
        try:
            data = fetch(url)
            if data[:4] == b"PK\x03\x04":
                attempts.append({"url": url, "state": "success"})
                return data, url, attempts
            attempts.append({"url": url, "state": f"not_zip_prefix:{data[:20]!r}"})
        except Exception as exc:
            attempts.append({"url": url, "state": f"error:{type(exc).__name__}:{exc}"})
    raise RuntimeError("No supplement ZIP candidate succeeded: " + json.dumps(attempts, indent=2))


def inspect_xlsx(blob: bytes) -> dict[str, object]:
    try:
        import openpyxl  # type: ignore
    except Exception as exc:
        return {"inspection_error": f"openpyxl_unavailable:{exc}"}
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


def main() -> None:
    data, source_url, attempts = download_zip()
    package_sha = hashlib.sha256(data).hexdigest()
    entries = []
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            blob = zf.read(info.filename)
            suffix = Path(info.filename).suffix.lower()
            item: dict[str, object] = {
                "name": info.filename,
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
            entries.append(item)

    payload = {
        "status": "SUPPLEMENT_PACKAGE_RETRIEVED_AND_INSPECTED",
        "article_doi": "10.1093/aob/mcaf258",
        "pmcid": PMCID,
        "retrieval_url": source_url,
        "zip_size": len(data),
        "zip_sha256": package_sha,
        "attempts": attempts,
        "entries": entries,
        "boundary": [
            "this receipt verifies deposited supplementary package structure, not the published meta-analysis estimates by itself",
            "herbivory treatment is not the focal floral defence trait D",
            "no effect from this module is rho, iota, kappa, or W_AD",
        ],
    }
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "zip_sha256": package_sha, "entries": [e["name"] for e in entries]}, indent=2))


if __name__ == "__main__":
    main()
