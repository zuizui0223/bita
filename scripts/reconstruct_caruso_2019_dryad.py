from __future__ import annotations

import hashlib
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "empirical" / "mechanism_pattern_synthesis" / "CARUSO_2019_DRYAD_RECEIPT_V1.json"
DATASET_URL = "https://datadryad.org/dataset/doi%3A10.5061%2Fdryad.2v8c5g0"
TARGETS = ("Exp_stud_NOTdup_Dryad.xls", "Exp_stud_dup_Dryad.xlsx")
UA = "bita-pattern-expansion/1.0 (+https://github.com/zuizui0223/bita)"


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def discover_links(html: str, filename: str) -> list[str]:
    links = []
    for m in re.finditer(r'href=["\']([^"\']+)["\']', html, re.I):
        href = m.group(1).replace("&amp;", "&")
        if filename.lower() in urllib.parse.unquote(href).lower() or "file_stream" in href:
            links.append(urllib.parse.urljoin(DATASET_URL, href))
    return links


def dryad_api_links(filename: str) -> list[str]:
    links = []
    encoded = urllib.parse.quote("doi:10.5061/dryad.2v8c5g0", safe="")
    endpoints = [
        f"https://datadryad.org/api/v2/datasets/{encoded}",
        f"https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.2v8c5g0",
    ]
    for endpoint in endpoints:
        try:
            obj = json.loads(fetch(endpoint).decode("utf-8"))
        except Exception:
            continue
        queue = [obj]
        seen = set()
        while queue:
            x = queue.pop()
            if isinstance(x, dict):
                for k, v in x.items():
                    if isinstance(v, str):
                        if filename.lower() in urllib.parse.unquote(v).lower() or (k.lower() in {"href", "url", "downloadurl"} and "download" in v.lower()):
                            links.append(v)
                        if v.startswith("http") and "api/v2" in v and v not in seen:
                            seen.add(v)
                            try:
                                queue.append(json.loads(fetch(v).decode("utf-8")))
                            except Exception:
                                pass
                    elif isinstance(v, (dict, list)):
                        queue.append(v)
            elif isinstance(x, list):
                queue.extend(x)
    return links


def download_target(html: str, filename: str) -> tuple[bytes, str, list[dict[str, str]]]:
    candidates = discover_links(html, filename) + dryad_api_links(filename)
    # Also try common Dryad file endpoint using an encoded file name if supported.
    encoded_doi = urllib.parse.quote("doi:10.5061/dryad.2v8c5g0", safe="")
    candidates.append(f"https://datadryad.org/api/v2/datasets/{encoded_doi}/files/{urllib.parse.quote(filename)}")
    unique = []
    seen = set()
    for url in candidates:
        if url not in seen:
            seen.add(url)
            unique.append(url)
    attempts = []
    for url in unique:
        try:
            blob = fetch(url)
            # Office files can be OLE (xls) or ZIP (xlsx); reject JSON/HTML wrappers.
            good = blob[:8] == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1" or blob[:4] == b"PK\x03\x04"
            if good:
                attempts.append({"url": url, "state": "success"})
                return blob, url, attempts
            # Some API endpoints return JSON metadata with a download link.
            try:
                obj = json.loads(blob.decode("utf-8"))
            except Exception:
                obj = None
            if isinstance(obj, dict):
                text = json.dumps(obj)
                urls = re.findall(r'https?://[^"\\]+', text)
                for u in urls:
                    if "download" in u.lower() or "file_stream" in u.lower():
                        try:
                            data = fetch(u)
                            good2 = data[:8] == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1" or data[:4] == b"PK\x03\x04"
                            if good2:
                                attempts.append({"url": u, "state": "success_via_metadata"})
                                return data, u, attempts
                        except Exception:
                            pass
            attempts.append({"url": url, "state": f"not_office_file:{blob[:30]!r}"})
        except Exception as exc:
            attempts.append({"url": url, "state": f"error:{type(exc).__name__}:{exc}"})
    raise RuntimeError(f"Could not download {filename}: " + json.dumps(attempts, indent=2))


def inspect_workbook(blob: bytes, filename: str) -> dict[str, object]:
    import pandas as pd  # type: ignore

    engine = "xlrd" if filename.endswith(".xls") else "openpyxl"
    xls = pd.ExcelFile(blob, engine=engine)
    sheets = []
    for sheet in xls.sheet_names:
        df = pd.read_excel(blob, sheet_name=sheet, engine=engine)
        sheets.append(
            {
                "sheet": sheet,
                "rows": int(len(df)),
                "columns": int(len(df.columns)),
                "column_names": [str(c) for c in df.columns[:50]],
                "first_two_rows": df.head(2).fillna("").astype(str).iloc[:, :30].to_dict(orient="records"),
            }
        )
    return {"engine": engine, "sheets": sheets}


def main() -> None:
    html = fetch(DATASET_URL).decode("utf-8", errors="ignore")
    files = []
    for filename in TARGETS:
        blob, url, attempts = download_target(html, filename)
        files.append(
            {
                "filename": filename,
                "download_url": url,
                "size": len(blob),
                "sha256": hashlib.sha256(blob).hexdigest(),
                "attempts": attempts,
                "workbook": inspect_workbook(blob, filename),
            }
        )

    nondup = next(f for f in files if f["filename"] == "Exp_stud_NOTdup_Dryad.xls")
    sheet_rows = [s["rows"] for s in nondup["workbook"]["sheets"]]
    if 755 not in sheet_rows:
        raise RuntimeError(f"Published 755-record analysis sheet not reproduced; sheet rows={sheet_rows}")

    payload = {
        "status": "DRYAD_WORKBOOKS_RETRIEVED_AND_755_RECORD_SHEET_REPRODUCED",
        "dataset_doi": "10.5061/dryad.2v8c5g0",
        "article_doi": "10.1111/evo.13639",
        "files": files,
        "boundary": [
            "selection gradients are downstream selection-context evidence, not W_AD",
            "other-biotic treatment is not automatically antagonist pressure H",
            "records from this database are not added to source-level route-ledger cluster counts without overlap adjudication",
        ],
    }
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "files": [(f["filename"], f["sha256"]) for f in files]}, indent=2))


if __name__ == "__main__":
    main()
