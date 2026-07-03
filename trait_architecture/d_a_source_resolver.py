"""Reproducible source-access resolver for d_A candidate leads (C3 feasibility).

Given the `d_A` candidate scouting table, this resolves each candidate to a DOI
(directly, or via NCBI id-conversion for `pmid:`/PMC leads, or a DOI embedded in a
`url:`), then resolves that DOI against the public Crossref works API and records a
deterministic **access receipt**: whether the DOI resolves, whether a full-text
link is advertised, and whether a linked dataset relation exists. It is the
repository's standard C3 source-feasibility pattern applied to the d_A leads.

Like the other probes in this package, it takes an injectable `fetch_json` so the
logic is deterministic and unit-testable offline; the CLI supplies a real,
rate-limited fetcher. It records access and relation metadata only. It does not
read article text, inspect tables, assign trait roles, or estimate any effect. A
resolved OA link is a route, never evidence.
"""

from __future__ import annotations

import csv
import json
import re
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Iterable
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen


USER_AGENT = "biotic-interaction-trait-architecture d-a-source-resolver/0.1"
CROSSREF_WORKS = "https://api.crossref.org/works/"
NCBI_IDCONV = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?format=json&ids="
_DOI_IN_TEXT = re.compile(r"10\.\d{4,9}/[^\s\"'<>&]+")
_PMCID_IN_TEXT = re.compile(r"PMC\d+", re.IGNORECASE)
RECEIPT_FIELDS = (
    "candidate_id", "source", "doi", "resolution_method", "access_state", "resolved",
    "work_type", "is_referenced_by_count", "license_present", "fulltext_link_count",
    "fulltext_content_types", "data_relation_types", "notes", "do_not_infer",
)
DO_NOT_INFER = (
    "Access and relation metadata only. Do not infer article table content, trait "
    "roles, denominators, linked units, moderator levels, or effect values."
)


@dataclass(frozen=True)
class SourceReceipt:
    candidate_id: str
    source: str
    doi: str
    resolution_method: str
    access_state: str
    resolved: str
    work_type: str
    is_referenced_by_count: str
    license_present: str
    fulltext_link_count: str
    fulltext_content_types: str
    data_relation_types: str
    notes: str
    do_not_infer: str = DO_NOT_INFER


class CrossrefFetcher:
    """Polite, keyless JSON fetcher with a minimum inter-request interval.

    Used for both Crossref and the NCBI id-conversion endpoint. ``mailto`` is added
    to the Crossref polite pool only when the URL has no query string of its own.
    """

    def __init__(self, min_interval_seconds: float = 0.5, mailto: str | None = None):
        if min_interval_seconds < 0:
            raise ValueError("min_interval_seconds must be non-negative")
        self.min_interval_seconds = min_interval_seconds
        self.mailto = mailto
        self._next_allowed = 0.0

    def json(self, url: str) -> tuple[int, Any]:
        wait = self._next_allowed - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        self._next_allowed = time.monotonic() + self.min_interval_seconds
        if self.mailto and "?" not in url:
            url = f"{url}?mailto={quote(self.mailto)}"
        request = Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
        try:
            with urlopen(request, timeout=45) as response:  # nosec B310: fixed public metadata endpoints
                status = int(getattr(response, "status", response.getcode()))
                return status, json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            return int(error.code), None


def _text(value: object) -> str:
    return str(value or "").strip()


def doi_from_source(source: str) -> str:
    """Return a directly declared DOI from a `doi:`-prefixed source, else empty."""

    value = _text(source)
    if value.lower().startswith("doi:"):
        return value[4:].strip()
    return ""


def _idconv_to_doi(identifier: str, fetch_json: Callable[[str], tuple[int, Any]]) -> str:
    """Resolve a PMID or PMCID to a DOI via the NCBI id-conversion API."""

    status, payload = fetch_json(NCBI_IDCONV + quote(identifier))
    if status >= 400 or not isinstance(payload, dict):
        return ""
    records = payload.get("records")
    if isinstance(records, list) and records and isinstance(records[0], dict):
        return _text(records[0].get("doi"))
    return ""


def resolve_source_doi(
    source: str,
    *,
    fetch_json: Callable[[str], tuple[int, Any]],
) -> tuple[str, str, str]:
    """Resolve a candidate `source` field to (doi, resolution_method, note).

    Handles `doi:` (direct), `pmid:` and PMC ids (via NCBI id-conversion), and a
    DOI or PMCID embedded in a `url:`. Returns an empty DOI with a method of
    ``unresolvable`` when no identifier can be recovered, so the receipt records
    honest missingness rather than a guess.
    """

    value = _text(source)
    low = value.lower()
    if low.startswith("doi:"):
        return value[4:].strip(), "declared_doi", ""
    if low.startswith("pmid:"):
        pmid = value.split(":", 1)[1].strip()
        doi = _idconv_to_doi(pmid, fetch_json)
        return (doi, "pmid_idconv", "") if doi else ("", "pmid_idconv_failed", f"NCBI id-conversion returned no DOI for {pmid}")
    # url: (or bare) — try an embedded DOI first, then an embedded PMCID.
    embedded = _DOI_IN_TEXT.search(value)
    if embedded:
        return embedded.group(0).rstrip(".").strip(), "doi_in_url", ""
    pmcid = _PMCID_IN_TEXT.search(value)
    if pmcid:
        doi = _idconv_to_doi(pmcid.group(0).upper(), fetch_json)
        return (doi, "pmcid_idconv", "") if doi else ("", "pmcid_idconv_failed", f"NCBI id-conversion returned no DOI for {pmcid.group(0)}")
    return "", "unresolvable", "No DOI, PMID, or PMCID recoverable from source."


def _fulltext_links(message: dict[str, Any]) -> list[str]:
    links = message.get("link")
    if not isinstance(links, list):
        return []
    return [_text(link.get("content-type")) or "unspecified" for link in links if isinstance(link, dict)]


def _data_relation_types(message: dict[str, Any]) -> list[str]:
    relation = message.get("relation")
    if not isinstance(relation, dict):
        return []
    interesting = ("is-supplemented-by", "references", "is-derived-from", "has-part")
    return sorted(key for key in relation if key in interesting)


def _receipt(candidate_id: str, source: str, doi: str, method: str, access_state: str, resolved: str,
             *, work_type: str = "", refs: str = "", license_present: str = "", link_count: str = "",
             link_types: str = "", data_relations: str = "", notes: str = "") -> SourceReceipt:
    return SourceReceipt(
        candidate_id=candidate_id, source=source, doi=doi, resolution_method=method,
        access_state=access_state, resolved=resolved, work_type=work_type,
        is_referenced_by_count=refs, license_present=license_present,
        fulltext_link_count=link_count, fulltext_content_types=link_types,
        data_relation_types=data_relations, notes=notes,
    )


def resolve_candidate_source(
    row: dict[str, str],
    *,
    fetch_json: Callable[[str], tuple[int, Any]],
) -> SourceReceipt:
    """Resolve one candidate to a DOI and then to a deterministic access receipt."""

    candidate_id = _text(row.get("candidate_id"))
    source = _text(row.get("source"))
    doi, method, note = resolve_source_doi(source, fetch_json=fetch_json)
    if not doi:
        return _receipt(candidate_id, source, "", method, "no_doi_resolved", "false", notes=note)
    try:
        status, payload = fetch_json(CROSSREF_WORKS + quote(doi, safe=""))
    except Exception as error:  # network / parse failure
        return _receipt(candidate_id, source, doi, method, "crossref_unresolved", "false",
                        notes=f"{type(error).__name__}: {error}")
    if status >= 400 or not isinstance(payload, dict) or not isinstance(payload.get("message"), dict):
        return _receipt(candidate_id, source, doi, method, "crossref_unresolved", "false",
                        notes=f"Crossref returned HTTP {status} or no message.")
    message = payload["message"]
    fulltext = _fulltext_links(message)
    data_relations = _data_relation_types(message)
    license_present = "true" if isinstance(message.get("license"), list) and message["license"] else "false"
    if data_relations:
        state = "linked_data_relation_present"
    elif fulltext:
        state = "oa_or_fulltext_link_present"
    else:
        state = "metadata_only"
    return _receipt(
        candidate_id, source, doi, method, state, "true",
        work_type=_text(message.get("type")),
        refs=_text(message.get("is-referenced-by-count")),
        license_present=license_present,
        link_count=str(len(fulltext)),
        link_types=";".join(sorted(set(fulltext))),
        data_relations=";".join(data_relations),
        notes="Resolved via Crossref; access/relation metadata only.",
    )


def resolve_candidates(
    rows: Iterable[dict[str, str]],
    *,
    fetch_json: Callable[[str], tuple[int, Any]],
) -> list[SourceReceipt]:
    return [resolve_candidate_source(row, fetch_json=fetch_json) for row in rows]


def summarise(receipts: Iterable[SourceReceipt]) -> dict[str, object]:
    receipts = list(receipts)
    states: dict[str, int] = {}
    methods: dict[str, int] = {}
    for receipt in receipts:
        states[receipt.access_state] = states.get(receipt.access_state, 0) + 1
        methods[receipt.resolution_method] = methods.get(receipt.resolution_method, 0) + 1
    return {
        "candidate_count": len(receipts),
        "counts_by_access_state": dict(sorted(states.items())),
        "counts_by_resolution_method": dict(sorted(methods.items())),
        "decision_boundary": DO_NOT_INFER,
    }


def read_candidates(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return [{key: _text(value) for key, value in row.items()} for row in csv.DictReader(handle)]


def write_receipts(out_dir: str | Path, receipts: Iterable[SourceReceipt], summary: dict[str, object]) -> None:
    output = Path(out_dir)
    output.mkdir(parents=True, exist_ok=True)
    with (output / "d_a_candidate_source_receipts.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=RECEIPT_FIELDS)
        writer.writeheader()
        for receipt in receipts:
            writer.writerow(asdict(receipt))
    (output / "d_a_candidate_source_report.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8"
    )
