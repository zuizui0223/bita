from __future__ import annotations

import hashlib
import http.cookiejar
import io
import json
import re
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "empirical" / "mechanism_pattern_synthesis" / "CARUSO_2019_DRYAD_RECEIPT_V1.json"
DOI_TEXT = "doi:10.5061/dryad.2v8c5g0"
ENCODED_DOI = urllib.parse.quote(DOI_TEXT, safe="")
DATASET_URL = f"https://datadryad.org/dataset/{ENCODED_DOI}"
API_URL = f"https://datadryad.org/api/v2/datasets/{ENCODED_DOI}"
TARGETS = ("Exp_stud_NOTdup_Dryad.xls", "Exp_stud_dup_Dryad.xlsx")
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36 bita-pattern-expansion/1.0"

COOKIE_JAR = http.cookiejar.CookieJar()
OPENER = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(COOKIE_JAR))


def fetch(url: str, *, referer: str | None = None) -> bytes:
    headers = {
        "User-Agent": UA,
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.8",
    }
    if referer:
        headers["Referer"] = referer
    req = urllib.request.Request(url, headers=headers)
    with OPENER.open(req, timeout=60) as resp:
        return resp.read()


def normalize_url(url: str) -> str:
    return urllib.parse.urljoin("https://datadryad.org", url)


def office_file(blob: bytes) -> bool:
    return blob[:8] == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1" or blob[:4] == b"PK\x03\x04"


def inspect_workbook(blob: bytes, filename: str) -> dict[str, object]:
    import pandas as pd  # type: ignore

    engine = "xlrd" if filename.endswith(".xls") else "openpyxl"
    bio = io.BytesIO(blob)
    xls = pd.ExcelFile(bio, engine=engine)
    sheets = []
    for sheet in xls.sheet_names:
        bio.seek(0)
        df = pd.read_excel(bio, sheet_name=sheet, engine=engine)
        sheets.append(
            {
                "sheet": sheet,
                "rows": int(len(df)),
                "columns": int(len(df.columns)),
                "column_names": [str(c) for c in df.columns[:80]],
                "first_two_rows": df.head(2).fillna("").astype(str).iloc[:, :30].to_dict(orient="records"),
            }
        )
    return {"engine": engine, "sheets": sheets}


def extract_targets_from_zip(blob: bytes, source_url: str) -> tuple[list[dict[str, object]], list[str]]:
    found: list[dict[str, object]] = []
    names: list[str] = []
    with zipfile.ZipFile(io.BytesIO(blob)) as zf:
        names = zf.namelist()
        by_base = {Path(name).name: name for name in names if not name.endswith("/")}
        for filename in TARGETS:
            member = by_base.get(filename)
            if member is None:
                continue
            data = zf.read(member)
            found.append(
                {
                    "filename": filename,
                    "archive_member": member,
                    "download_url": source_url,
                    "size": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "workbook": inspect_workbook(data, filename),
                }
            )
    return found, names


def discover_api_downloads(obj: object) -> list[str]:
    out: list[str] = []
    queue = [obj]
    while queue:
        item = queue.pop()
        if isinstance(item, dict):
            for key, value in item.items():
                if isinstance(value, str):
                    low_key = key.lower()
                    low_val = value.lower()
                    if (
                        "download" in low_key
                        or "file_stream" in low_val
                        or "/download" in low_val
                        or any(target.lower() in urllib.parse.unquote(low_val) for target in TARGETS)
                    ):
                        if value.startswith(("http://", "https://", "/")):
                            out.append(normalize_url(value))
                elif isinstance(value, (dict, list)):
                    queue.append(value)
        elif isinstance(item, list):
            queue.extend(item)
    return out


def retrieve() -> tuple[list[dict[str, object]], list[dict[str, str]]]:
    attempts: list[dict[str, str]] = []

    # Prime cookies and independently verify the human-facing dataset page.
    html = fetch(DATASET_URL).decode("utf-8", errors="ignore")
    if not all(target in html for target in TARGETS):
        raise RuntimeError("Dryad dataset page did not expose both expected filenames")
    attempts.append({"url": DATASET_URL, "state": "dataset_page_verified"})

    candidates = [
        f"https://datadryad.org/api/v2/datasets/{ENCODED_DOI}/download",
        f"https://datadryad.org/api/v2/datasets/{ENCODED_DOI}/download?download=1",
    ]

    try:
        api_obj = json.loads(fetch(API_URL, referer=DATASET_URL).decode("utf-8"))
        attempts.append({"url": API_URL, "state": "dataset_api_verified"})
        candidates.extend(discover_api_downloads(api_obj))
    except Exception as exc:
        attempts.append({"url": API_URL, "state": f"dataset_api_error:{type(exc).__name__}:{exc}"})

    # Human-facing links remain useful fallbacks. Capture only real href values.
    for m in re.finditer(r'href=["\']([^"\']+)["\']', html, re.I):
        href = m.group(1).replace("&amp;", "&")
        decoded = urllib.parse.unquote(href)
        if "file_stream" in href or any(target in decoded for target in TARGETS):
            candidates.append(urllib.parse.urljoin(DATASET_URL, href))

    unique: list[str] = []
    seen: set[str] = set()
    for url in candidates:
        url = normalize_url(url)
        if url not in seen:
            seen.add(url)
            unique.append(url)

    individual: dict[str, dict[str, object]] = {}
    for url in unique:
        try:
            blob = fetch(url, referer=DATASET_URL)
        except Exception as exc:
            attempts.append({"url": url, "state": f"error:{type(exc).__name__}:{exc}"})
            continue

        if blob[:4] == b"PK\x03\x04":
            # This can be the full-dataset archive OR the xlsx target itself.
            try:
                found, names = extract_targets_from_zip(blob, url)
            except Exception:
                found, names = [], []
            if found:
                attempts.append({"url": url, "state": f"full_dataset_zip_success:{len(found)}_targets"})
                for item in found:
                    individual[str(item["filename"])] = item
            else:
                # If the URL identifies the xlsx file, inspect it directly.
                if "Exp_stud_dup_Dryad.xlsx" in urllib.parse.unquote(url):
                    filename = "Exp_stud_dup_Dryad.xlsx"
                    individual[filename] = {
                        "filename": filename,
                        "download_url": url,
                        "size": len(blob),
                        "sha256": hashlib.sha256(blob).hexdigest(),
                        "workbook": inspect_workbook(blob, filename),
                    }
                    attempts.append({"url": url, "state": "xlsx_success"})
                else:
                    attempts.append({"url": url, "state": f"zip_without_targets:{names[:10]}"})
        elif blob[:8] == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1":
            filename = "Exp_stud_NOTdup_Dryad.xls"
            individual[filename] = {
                "filename": filename,
                "download_url": url,
                "size": len(blob),
                "sha256": hashlib.sha256(blob).hexdigest(),
                "workbook": inspect_workbook(blob, filename),
            }
            attempts.append({"url": url, "state": "xls_success"})
        else:
            attempts.append({"url": url, "state": f"not_dataset_or_office_file:{blob[:30]!r}"})

        if all(target in individual for target in TARGETS):
            break

    if not all(target in individual for target in TARGETS):
        raise RuntimeError(
            "Could not retrieve both Dryad workbooks; retrieved="
            + json.dumps(sorted(individual))
            + " attempts="
            + json.dumps(attempts, indent=2)
        )
    return [individual[target] for target in TARGETS], attempts


def main() -> None:
    files, attempts = retrieve()

    nondup = next(f for f in files if f["filename"] == "Exp_stud_NOTdup_Dryad.xls")
    sheet_rows = [s["rows"] for s in nondup["workbook"]["sheets"]]
    if 755 not in sheet_rows:
        raise RuntimeError(f"Published 755-record analysis sheet not reproduced; sheet rows={sheet_rows}")

    payload = {
        "status": "DRYAD_WORKBOOKS_RETRIEVED_AND_755_RECORD_SHEET_REPRODUCED",
        "dataset_doi": "10.5061/dryad.2v8c5g0",
        "article_doi": "10.1111/evo.13639",
        "attempts": attempts,
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
