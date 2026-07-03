"""Probe whether the fixed Caruso 2019 meta-analysis exposes an index to primary studies.

Caruso et al. 2019 reports floral-trait selection gradients. Those gradients are
not `d_A` effects and are never imported into Part B. This bounded C3 probe looks
only for public *routes* to a possible primary-study index: publisher data links,
OpenAlex/Unpaywall access locations, and DataCite dataset records explicitly related
to the Caruso DOI. It records URL-level receipts, never article prose, database rows,
primary-study effects, or selection-gradient values.
"""

from __future__ import annotations

import csv
import html
import json
import re
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Iterable
from urllib.error import HTTPError
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen


CARUSO_DOI = "10.1111/evo.13639"
CROSSREF_WORK = "https://api.crossref.org/works/"
UNPAYWALL_WORK = "https://api.unpaywall.org/v2/"
OPENALEX_WORK = "https://api.openalex.org/works/https://doi.org/"
DATACITE_SEARCH = "https://api.datacite.org/dois?query="
PUBLISHER_LANDING = "https://onlinelibrary.wiley.com/doi/full/10.1111/evo.13639"
USER_AGENT = "biotic-interaction-trait-architecture d-a-caruso-index-probe/0.1"
MAX_HTML_BYTES = 2 * 1024 * 1024
DATASET_HOST_MARKERS = ("datadryad.org", "dryad", "zenodo.org", "figshare.com", "osf.io")
URL_PATTERN = re.compile(r"https?://[^\s\"'<>]+", flags=re.I)
PROBE_FIELDS = (
    "source_doi", "probe_source", "http_status", "access_status", "candidate_url",
    "candidate_host", "candidate_kind", "discovery_basis", "related_to_source_doi",
    "notes", "do_not_infer",
)
DO_NOT_INFER = (
    "Discovery receipt only. Do not infer a primary-study list, trait-to-antagonism route, "
    "effect direction, effect size, denominator, uncertainty, or B2 eligibility from a meta-analysis or data-link route."
)


@dataclass(frozen=True)
class IndexProbeReceipt:
    source_doi: str
    probe_source: str
    http_status: str
    access_status: str
    candidate_url: str
    candidate_host: str
    candidate_kind: str
    discovery_basis: str
    related_to_source_doi: str
    notes: str
    do_not_infer: str = DO_NOT_INFER


class PublicMetadataClient:
    """Small, injectable HTTP client for fixed public metadata routes."""

    def __init__(self, *, mailto: str = "", min_interval_seconds: float = 0.25):
        self.mailto = mailto.strip()
        self.min_interval_seconds = min_interval_seconds
        self._next_allowed = 0.0

    def _request(self, url: str, accept: str) -> tuple[int, bytes]:
        wait = self._next_allowed - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        self._next_allowed = time.monotonic() + self.min_interval_seconds
        request = Request(url, headers={"Accept": accept, "User-Agent": USER_AGENT})
        try:
            with urlopen(request, timeout=60) as response:  # nosec B310: fixed public metadata/landing endpoints
                return int(getattr(response, "status", response.getcode())), response.read(MAX_HTML_BYTES + 1)
        except HTTPError as error:
            return int(error.code), b""

    def json(self, url: str) -> tuple[int, Any]:
        status, payload = self._request(url, "application/json")
        if status >= 400 or not payload:
            return status, None
        try:
            return status, json.loads(payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return status, None

    def html(self, url: str) -> tuple[int, str]:
        status, payload = self._request(url, "text/html,application/xhtml+xml")
        if len(payload) > MAX_HTML_BYTES:
            return status, ""
        return status, payload.decode("utf-8", errors="replace")


def _text(value: object) -> str:
    return str(value or "").strip()


def _host(url: str) -> str:
    return urlparse(url).netloc.casefold()


def _dataset_like(url: str) -> bool:
    folded = url.casefold()
    return any(marker in folded for marker in DATASET_HOST_MARKERS)


def _receipt(
    probe_source: str,
    status: int | str,
    access_status: str,
    *,
    candidate_url: str = "",
    candidate_kind: str = "",
    discovery_basis: str = "",
    related: str = "",
    notes: str = "",
) -> IndexProbeReceipt:
    return IndexProbeReceipt(
        source_doi=CARUSO_DOI,
        probe_source=probe_source,
        http_status=str(status),
        access_status=access_status,
        candidate_url=candidate_url,
        candidate_host=_host(candidate_url) if candidate_url else "",
        candidate_kind=candidate_kind,
        discovery_basis=discovery_basis,
        related_to_source_doi=related,
        notes=notes,
    )


def _crossref_urls(payload: Any) -> list[str]:
    if not isinstance(payload, dict) or not isinstance(payload.get("message"), dict):
        return []
    message = payload["message"]
    urls: list[str] = []
    resource = message.get("resource")
    if isinstance(resource, dict):
        urls.append(_text(resource.get("primary")))
    links = message.get("link")
    if isinstance(links, list):
        urls.extend(_text(item.get("URL")) for item in links if isinstance(item, dict))
    return _unique_urls(urls)


def _unpaywall_urls(payload: Any) -> list[str]:
    if not isinstance(payload, dict):
        return []
    urls: list[str] = []
    locations = list(payload.get("oa_locations") or [])
    best = payload.get("best_oa_location")
    if isinstance(best, dict):
        locations.append(best)
    for location in locations:
        if isinstance(location, dict):
            urls.extend((_text(location.get("url")), _text(location.get("url_for_pdf"))))
    return _unique_urls(urls)


def _openalex_urls(payload: Any) -> list[str]:
    if not isinstance(payload, dict):
        return []
    locations = list(payload.get("locations") or [])
    best = payload.get("best_oa_location")
    if isinstance(best, dict):
        locations.append(best)
    urls: list[str] = []
    for location in locations:
        if isinstance(location, dict):
            urls.extend((_text(location.get("landing_page_url")), _text(location.get("pdf_url"))))
    return _unique_urls(urls)


def _unique_urls(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        value = _text(value).rstrip(".,;)")
        if value and value not in seen:
            seen.add(value)
            output.append(value)
    return output


def _datacite_related_dataset_urls(payload: Any) -> list[str]:
    """Return only Dataset records that explicitly name the Caruso DOI as related."""

    if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
        return []
    urls: list[str] = []
    for item in payload["data"]:
        if not isinstance(item, dict) or not isinstance(item.get("attributes"), dict):
            continue
        attrs = item["attributes"]
        types = attrs.get("types") if isinstance(attrs.get("types"), dict) else {}
        if _text(types.get("resourceTypeGeneral")).casefold() != "dataset":
            continue
        relations = attrs.get("relatedIdentifiers")
        if not isinstance(relations, list):
            continue
        related = any(
            isinstance(relation, dict)
            and _text(relation.get("relatedIdentifier")).casefold().replace("https://doi.org/", "") == CARUSO_DOI
            for relation in relations
        )
        if related:
            doi = _text(attrs.get("doi"))
            if doi:
                urls.append(f"https://doi.org/{doi}")
    return _unique_urls(urls)


def _publisher_dataset_urls(page: str) -> list[str]:
    """Find dataset-host URLs in a publisher landing page without retaining its prose."""

    decoded = html.unescape(page)
    return _unique_urls(url for url in URL_PATTERN.findall(decoded) if _dataset_like(url))


def probe_caruso_index(
    *,
    fetch_json: Callable[[str], tuple[int, Any]],
    fetch_html: Callable[[str], tuple[int, str]],
    unpaywall_email: str,
) -> list[IndexProbeReceipt]:
    """Run bounded, URL-level discovery across four public metadata routes."""

    receipts: list[IndexProbeReceipt] = []
    endpoints = (
        ("crossref", CROSSREF_WORK + quote(CARUSO_DOI, safe="")),
        ("unpaywall", UNPAYWALL_WORK + quote(CARUSO_DOI, safe="") + "?email=" + quote(unpaywall_email, safe="@")),
        ("openalex", OPENALEX_WORK + quote(CARUSO_DOI, safe="")),
        ("datacite", DATACITE_SEARCH + quote(CARUSO_DOI, safe="")),
    )
    responses: dict[str, tuple[int, Any]] = {}
    for name, url in endpoints:
        try:
            status, payload = fetch_json(url)
        except Exception as error:
            receipts.append(_receipt(name, "", "request_failed", notes=f"{type(error).__name__}: {error}"))
            continue
        responses[name] = (status, payload)
        if status >= 400 or payload is None:
            receipts.append(_receipt(name, status, "metadata_unavailable"))
        else:
            receipts.append(_receipt(name, status, "metadata_recovered"))

    for source, extractor in (
        ("crossref", _crossref_urls),
        ("unpaywall", _unpaywall_urls),
        ("openalex", _openalex_urls),
    ):
        status, payload = responses.get(source, (0, None))
        for url in extractor(payload):
            receipts.append(_receipt(
                source, status, "article_access_route",
                candidate_url=url,
                candidate_kind="dataset_link_candidate" if _dataset_like(url) else "article_access_route",
                discovery_basis=f"{source}_metadata_location",
                related="not_asserted",
            ))

    status, datacite_payload = responses.get("datacite", (0, None))
    for url in _datacite_related_dataset_urls(datacite_payload):
        receipts.append(_receipt(
            "datacite", status, "dataset_candidate_related_to_source_doi",
            candidate_url=url,
            candidate_kind="dataset_landing",
            discovery_basis="datacite_related_identifier",
            related="explicit_related_identifier",
        ))

    try:
        status, page = fetch_html(PUBLISHER_LANDING)
    except Exception as error:
        receipts.append(_receipt("publisher_landing", "", "request_failed", notes=f"{type(error).__name__}: {error}"))
    else:
        if status >= 400 or not page:
            receipts.append(_receipt("publisher_landing", status, "landing_unavailable"))
        else:
            receipts.append(_receipt("publisher_landing", status, "landing_recovered"))
            for url in _publisher_dataset_urls(page):
                receipts.append(_receipt(
                    "publisher_landing", status, "dataset_link_candidate",
                    candidate_url=url,
                    candidate_kind="dataset_landing",
                    discovery_basis="publisher_dataset_host_link",
                    related="not_asserted",
                ))
    return receipts


def summarise(receipts: Iterable[IndexProbeReceipt]) -> dict[str, object]:
    rows = list(receipts)
    candidates = [
        row for row in rows
        if row.access_status in {"dataset_candidate_related_to_source_doi", "dataset_link_candidate"}
    ]
    explicit = [row for row in candidates if row.related_to_source_doi == "explicit_related_identifier"]
    return {
        "source_doi": CARUSO_DOI,
        "probe_receipt_count": len(rows),
        "dataset_candidate_count": len({row.candidate_url for row in candidates if row.candidate_url}),
        "explicitly_related_dataset_count": len({row.candidate_url for row in explicit if row.candidate_url}),
        "next_action": (
            "resolve_dataset_metadata_and_primary_study_index"
            if candidates else "retain_caruso_as_system_seed_only_no_public_index_route_recovered"
        ),
        "decision_boundary": DO_NOT_INFER,
    }


def write_outputs(out_dir: str | Path, receipts: Iterable[IndexProbeReceipt]) -> dict[str, object]:
    rows = list(receipts)
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    with (destination / "d_a_caruso_index_probe.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=PROBE_FIELDS)
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)
    report = summarise(rows)
    (destination / "d_a_caruso_index_probe_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
    )
    return report
