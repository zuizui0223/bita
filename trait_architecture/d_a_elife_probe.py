"""Public-source feasibility probe for the registered scent/reward d_A eLife lead.

The target is fixed by the d_A scouting registry: Schiestl et al. 2015,
``10.7554/eLife.07641``. The probe records only URL reachability and content type
for DOI-exact Crossref links plus standard eLife article representations. It does
not retain article content, decide whether a route is direct, or extract an effect.
"""

from __future__ import annotations

import csv
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Iterable
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

from .d_a_source_resolver import CROSSREF_WORKS, CrossrefFetcher


TARGET_ID = "dA_cand_schiestl2015"
TARGET_DOI = "10.7554/eLife.07641"
MAX_PREFIX_BYTES = 8192
USER_AGENT = "bita d-a-elife-probe/0.1"
PROBE_FIELDS = (
    "candidate_id", "doi", "source_label", "source_url", "access_status", "http_status",
    "content_type", "prefix_signature", "do_not_infer",
)
DO_NOT_INFER = (
    "Access probe only. Do not infer XML/HTML article content, trait manipulation, antagonist outcome, "
    "effect direction, denominator, or B2 eligibility."
)


@dataclass(frozen=True)
class ELifeProbeReceipt:
    candidate_id: str
    doi: str
    source_label: str
    source_url: str
    access_status: str
    http_status: str
    content_type: str
    prefix_signature: str
    do_not_infer: str = DO_NOT_INFER


def _text(value: object) -> str:
    return str(value or "").strip()


def _article_id(doi: str) -> str:
    match = re.search(r"elife\.(\d+)$", doi, flags=re.I)
    return match.group(1) if match else ""


def read_target(path: str | Path) -> dict[str, str]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = [{key: _text(value) for key, value in row.items()} for row in csv.DictReader(handle)]
    matches = [row for row in rows if row.get("candidate_id") == TARGET_ID]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one {TARGET_ID} row")
    return matches[0]


def _crossref_links(doi: str, fetch_json: Callable[[str], tuple[int, Any]]) -> list[str]:
    status, payload = fetch_json(CROSSREF_WORKS + quote(doi, safe=""))
    if status >= 400 or not isinstance(payload, dict):
        return []
    message = payload.get("message")
    if not isinstance(message, dict) or not isinstance(message.get("link"), list):
        return []
    urls: list[str] = []
    for link in message["link"]:
        if not isinstance(link, dict):
            continue
        url = _text(link.get("URL"))
        if url and url not in urls:
            urls.append(url)
    return urls


def candidate_urls(doi: str, fetch_json: Callable[[str], tuple[int, Any]]) -> list[tuple[str, str]]:
    article_id = _article_id(doi)
    urls: list[tuple[str, str]] = [("crossref_link", url) for url in _crossref_links(doi, fetch_json)]
    if article_id:
        urls.extend([
            ("elife_html", f"https://elifesciences.org/articles/{article_id}"),
            ("elife_xml", f"https://elifesciences.org/articles/{article_id}.xml"),
            ("elife_pdf", f"https://elifesciences.org/articles/{article_id}.pdf"),
        ])
    seen: set[str] = set()
    return [(label, url) for label, url in urls if not (url in seen or seen.add(url))]


def _prefix(url: str) -> tuple[int, str, bytes]:
    request = Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/xml,application/pdf,text/html,*/*",
        "Range": f"bytes=0-{MAX_PREFIX_BYTES - 1}",
    })
    with urlopen(request, timeout=60) as response:  # nosec B310: DOI-exact Crossref/eLife route
        status = int(getattr(response, "status", response.getcode()))
        content_type = _text(response.headers.get("Content-Type")).lower()
        return status, content_type, response.read(MAX_PREFIX_BYTES)


def _status(content_type: str, prefix: bytes) -> str:
    stripped = prefix.lstrip().lower()
    if prefix.startswith(b"%PDF") or "application/pdf" in content_type:
        return "public_pdf_prefix_recovered"
    if stripped.startswith(b"<?xml") or stripped.startswith(b"<article") or "xml" in content_type:
        return "public_xml_prefix_recovered"
    if stripped.startswith((b"<!doctype html", b"<html", b"<head")) or "html" in content_type:
        return "public_html_prefix_recovered"
    return "non_article_content_returned"


def probe_target(
    target: dict[str, str],
    *,
    fetch_json: Callable[[str], tuple[int, Any]],
    fetch_prefix: Callable[[str], tuple[int, str, bytes]] = _prefix,
) -> list[ELifeProbeReceipt]:
    doi = target.get("source", "").replace("doi:", "", 1).strip() or TARGET_DOI
    receipts: list[ELifeProbeReceipt] = []
    for label, url in candidate_urls(doi, fetch_json):
        try:
            status, content_type, prefix = fetch_prefix(url)
            receipts.append(ELifeProbeReceipt(
                candidate_id=target["candidate_id"], doi=doi, source_label=label, source_url=url,
                access_status=_status(content_type, prefix), http_status=str(status),
                content_type=content_type, prefix_signature=prefix[:16].decode("latin1", errors="replace"),
            ))
        except HTTPError as error:
            receipts.append(ELifeProbeReceipt(
                candidate_id=target["candidate_id"], doi=doi, source_label=label, source_url=url,
                access_status="access_denied_or_http_error", http_status=str(error.code), content_type="", prefix_signature="",
            ))
        except Exception:
            receipts.append(ELifeProbeReceipt(
                candidate_id=target["candidate_id"], doi=doi, source_label=label, source_url=url,
                access_status="access_failed", http_status="", content_type="", prefix_signature="",
            ))
    return receipts


def write_outputs(out_dir: str | Path, receipts: Iterable[ELifeProbeReceipt]) -> dict[str, object]:
    receipts = list(receipts)
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    with (destination / "d_a_elife_source_probe.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=PROBE_FIELDS)
        writer.writeheader()
        writer.writerows(asdict(row) for row in receipts)
    report = {
        "url_count": len(receipts),
        "xml_prefix_recovered": sum(row.access_status == "public_xml_prefix_recovered" for row in receipts),
        "pdf_prefix_recovered": sum(row.access_status == "public_pdf_prefix_recovered" for row in receipts),
        "html_prefix_recovered": sum(row.access_status == "public_html_prefix_recovered" for row in receipts),
        "decision_boundary": DO_NOT_INFER,
    }
    (destination / "d_a_elife_source_probe_report.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def run(target_csv: str | Path, out_dir: str | Path, *, mailto: str | None = None) -> dict[str, object]:
    fetcher = CrossrefFetcher(mailto=mailto)
    receipts = probe_target(read_target(target_csv), fetch_json=fetcher.json)
    return write_outputs(out_dir, receipts)
