"""Audit García et al. (2024) JPE appendices without retaining raw rows.

The JPE article exposes Appendix I and Appendix II through stable article-view
endpoints. This script retrieves both on GitHub Actions, records content type and
size, and inspects Appendix II only when it is a structured text/spreadsheet file.
PDF content is not parsed here; the PDF appendix is only classified by format.

The JPE/OJS host intermittently closes Python urllib connections without a response
and has repeatedly produced HTTP/2 PROTOCOL_ERROR failures on GitHub-hosted runners.
Retrieval therefore falls back to curl forced to HTTP/1.1, with redirects/retries
against the same fixed public URLs. This changes transport only; source identity and
scientific adjudication are unchanged. Raw appendix files are held only in memory /
temporary files during the workflow and are never committed.
"""

from __future__ import annotations

import csv
import io
import json
import math
import subprocess
import tempfile
import zipfile
from pathlib import Path
from urllib.request import Request, urlopen

ARTICLE_DOI = "10.26786/1920-7603(2024)758"
ARTICLE_URL = "https://www.pollinationecology.org/index.php/jpe/article/view/758"
APPENDICES = {
    "Appendix_I": "https://www.pollinationecology.org/index.php/jpe/article/view/758/477",
    "Appendix_II": "https://www.pollinationecology.org/index.php/jpe/article/view/758/478",
}
USER_AGENT = "bita-garcia2024-appendix-audit/1.2"
MAX_BYTES = 50 * 1024 * 1024
KEY_TOKENS = (
    "id", "plant", "petal", "latex", "pollin", "fruit", "nectar", "inflores", "flower",
    "height", "damage", "fitness", "male", "female",
)


def _urllib_download(url: str) -> tuple[bytes, dict[str, str], str]:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*", "Referer": ARTICLE_URL})
    with urlopen(req, timeout=45) as response:  # nosec B310: fixed public journal endpoints
        data = response.read(MAX_BYTES + 1)
        headers = {k.lower(): v for k, v in response.headers.items()}
        final_url = response.geturl()
    if len(data) > MAX_BYTES:
        raise ValueError("appendix exceeds configured byte limit")
    return data, headers, final_url


def _curl_download(url: str) -> tuple[bytes, dict[str, str], str]:
    with tempfile.TemporaryDirectory(prefix="garcia-jpe-") as tmp:
        body = Path(tmp) / "body.bin"
        headers_path = Path(tmp) / "headers.txt"
        effective_path = Path(tmp) / "effective.txt"
        command = [
            "curl", "--fail", "--location", "--silent", "--show-error",
            # The JPE/OJS endpoint repeatedly resets HTTP/2 streams on hosted
            # runners. Force HTTP/1.1 and close each connection; this is a
            # transport-only workaround against the same article-declared URLs.
            "--http1.1", "--no-keepalive",
            "--retry", "8", "--retry-all-errors", "--retry-delay", "2",
            "--connect-timeout", "30", "--max-time", "300",
            "--user-agent", USER_AGENT,
            "--header", f"Referer: {ARTICLE_URL}",
            "--header", "Accept: */*",
            "--header", "Connection: close",
            "--dump-header", str(headers_path),
            "--output", str(body),
            "--write-out", "%{url_effective}",
            url,
        ]
        completed = subprocess.run(command, capture_output=True, text=True)
        effective_path.write_text(completed.stdout or url, encoding="utf-8")
        if completed.returncode != 0:
            raise RuntimeError(f"curl failed ({completed.returncode}): {completed.stderr[-600:]}")
        data = body.read_bytes()
        if len(data) > MAX_BYTES:
            raise ValueError("appendix exceeds configured byte limit")
        # Multiple redirect header blocks may be present. Keep the final non-empty
        # values for the small set of headers used by the audit.
        headers: dict[str, str] = {}
        for line in headers_path.read_text(encoding="latin-1", errors="replace").splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            headers[key.strip().lower()] = value.strip()
        return data, headers, effective_path.read_text(encoding="utf-8").strip() or url


def _download(url: str) -> tuple[bytes, dict[str, str], str]:
    try:
        return _urllib_download(url)
    except Exception as urllib_error:
        try:
            return _curl_download(url)
        except Exception as curl_error:
            raise RuntimeError(
                f"JPE appendix retrieval failed via urllib ({type(urllib_error).__name__}: {urllib_error}) "
                f"and curl ({type(curl_error).__name__}: {curl_error})"
            ) from curl_error


def _kind(data: bytes, content_type: str, final_url: str) -> str:
    lower_type = content_type.lower()
    lower_url = final_url.lower()
    if data.startswith(b"%PDF") or "pdf" in lower_type:
        return "pdf"
    if data.startswith(b"PK\x03\x04"):
        if "spreadsheet" in lower_type or lower_url.endswith((".xlsx", ".xlsm")):
            return "xlsx"
        return "zip_or_office"
    stripped = data[:200].lstrip()
    if stripped.startswith((b"{", b"[")) or "json" in lower_type:
        return "json"
    if "csv" in lower_type or lower_url.endswith(".csv"):
        return "csv"
    if "text" in lower_type or "html" in lower_type:
        return "text_or_html"
    return "binary_unknown"


def _numeric_summary(rows: list[dict[str, object]], headers: list[str]) -> dict[str, dict[str, object]]:
    out: dict[str, dict[str, object]] = {}
    for header in headers:
        values: list[float] = []
        for row in rows:
            value = row.get(header)
            if value is None or str(value).strip() == "":
                continue
            try:
                x = float(value)
            except (TypeError, ValueError):
                continue
            if math.isfinite(x):
                values.append(x)
        if values:
            out[header] = {"n_numeric": len(values), "min": min(values), "max": max(values)}
    return out


def _audit_csv(data: bytes) -> dict[str, object]:
    text = data.decode("utf-8-sig", errors="replace")
    sample = text[:4096]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",\t;")
        delimiter = dialect.delimiter
    except csv.Error:
        delimiter = ","
    reader = csv.DictReader(io.StringIO(text), delimiter=delimiter)
    rows = [dict(row) for row in reader]
    headers = list(reader.fieldnames or [])
    return {
        "format": "csv_like",
        "delimiter": "tab" if delimiter == "\t" else delimiter,
        "n_rows": len(rows),
        "headers": headers,
        "candidate_columns": [h for h in headers if any(token in h.lower() for token in KEY_TOKENS)],
        "nonempty_counts": {h: sum(1 for row in rows if str(row.get(h, "") or "").strip()) for h in headers},
        "numeric_ranges": _numeric_summary(rows, headers),
    }


def _audit_xlsx(data: bytes) -> dict[str, object]:
    import openpyxl  # type: ignore

    workbook = openpyxl.load_workbook(io.BytesIO(data), read_only=True, data_only=True)
    sheets: list[dict[str, object]] = []
    for ws in workbook.worksheets:
        iterator = ws.iter_rows(values_only=True)
        try:
            first = next(iterator)
        except StopIteration:
            sheets.append({"sheet": ws.title, "n_rows": 0, "headers": []})
            continue
        headers = [str(value).strip() if value is not None else "" for value in first]
        while headers and headers[-1] == "":
            headers.pop()
        rows: list[dict[str, object]] = []
        for values in iterator:
            mapped = {headers[i]: values[i] if i < len(values) else None for i in range(len(headers)) if headers[i]}
            if any(value is not None and str(value).strip() != "" for value in mapped.values()):
                rows.append(mapped)
        clean_headers = [h for h in headers if h]
        sheets.append({
            "sheet": ws.title,
            "n_rows": len(rows),
            "headers": clean_headers,
            "candidate_columns": [h for h in clean_headers if any(token in h.lower() for token in KEY_TOKENS)],
            "nonempty_counts": {h: sum(1 for row in rows if row.get(h) is not None and str(row.get(h)).strip()) for h in clean_headers},
            "numeric_ranges": _numeric_summary(rows, clean_headers),
        })
    return {"format": "xlsx", "sheet_count": len(sheets), "sheets": sheets}


def _audit_appendix(label: str, url: str) -> dict[str, object]:
    data, headers, final_url = _download(url)
    content_type = headers.get("content-type", "")
    disposition = headers.get("content-disposition", "")
    kind = _kind(data, content_type, final_url)
    result: dict[str, object] = {
        "label": label,
        "requested_url": url,
        "final_url": final_url,
        "content_type": content_type,
        "content_disposition": disposition,
        "size_bytes": len(data),
        "detected_kind": kind,
    }
    if label == "Appendix_II":
        if kind == "xlsx":
            result["structured_audit"] = _audit_xlsx(data)
        elif kind in {"csv", "text_or_html"}:
            prefix = data[:4096].decode("utf-8-sig", errors="replace")
            if "," in prefix or "\t" in prefix:
                result["structured_audit"] = _audit_csv(data)
            else:
                result["structured_audit"] = {"format": kind, "table_not_detected": True}
        elif kind == "zip_or_office":
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                names = set(archive.namelist())
            if "xl/workbook.xml" in names:
                result["detected_kind"] = "xlsx"
                result["structured_audit"] = _audit_xlsx(data)
            else:
                result["structured_audit"] = {"format": "zip", "member_count": len(names), "member_names": sorted(names)}
    return result


def run(output_path: str | Path) -> dict[str, object]:
    audits = [_audit_appendix(label, url) for label, url in APPENDICES.items()]
    report = {
        "article_doi": ARTICLE_DOI,
        "audits": audits,
        "guardrails": [
            "No observation-level rows are written to the report.",
            "Appendix I PDF content is not parsed by this workflow; only file metadata are recorded.",
            "No A x D model is fitted until the source model/variable definitions are independently fixed.",
            "curl fallback changes transport only; the fixed article-declared appendix URLs are unchanged.",
        ],
    }
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    args = parser.parse_args()
    result = run(args.output)
    print(json.dumps({
        "appendices": [
            {"label": item["label"], "kind": item["detected_kind"], "size_bytes": item["size_bytes"]}
            for item in result["audits"]
        ]
    }, indent=2))