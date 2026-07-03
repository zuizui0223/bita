"""Reproducible source-access resolver for d_A candidate leads (C3 feasibility).

Given the `d_A` candidate scouting table, this resolves each candidate's DOI
against the public Crossref works API and records a deterministic **access
receipt**: whether the DOI resolves, whether a full-text link is advertised, and
whether a linked dataset relation exists. It is the repository's standard C3
source-feasibility pattern applied to the d_A leads.

Like the other probes in this package, it takes an injectable `fetch_json` so the
logic is deterministic and unit-testable offline; the CLI supplies a real,
rate-limited Crossref fetcher. It records access and relation metadata only. It
does not read article text, inspect tables, assign trait roles, or estimate any
effect. A resolved OA link is a route, never evidence.
"""

from __future__ import annotations

import csv
import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Iterable
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen


USER_AGENT = "biotic-interaction-trait-architecture d-a-source-resolver/0.1"
CROSSREF_WORKS = "https://api.crossref.org/works/"
RECEIPT_FIELDS = (
    "candidate_id", "source", "doi", "access_state", "resolved", "work_type",
    "is_referenced_by_count", "license_present", "fulltext_link_count",
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
    """Polite, keyless Crossref JSON fetcher with a minimum inter-request interval."""

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
        if self.mailto:
            url = f"{url}?mailto={quote(self.mailto)}"
        request = Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
        try:
            with urlopen(request, timeout=45) as response:  # nosec B310: fixed public Crossref endpoint
                status = int(getattr(response, "status", response.getcode()))
                return status, json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            return int(error.code), None


def _text(value: object) -> str:
    return str(value or "").strip()


def doi_from_source(source: str) -> str:
    """Extract a DOI from a candidate `source` field, else empty.

    Candidate sources look like `doi:10.x/y`, `pmid:12345`, or `url:host/path`.
    Only `doi:`-prefixed sources are resolvable here; others return empty so the
    receipt records `no_doi_supplied` rather than guessing.
    """

    value = _text(source)
    if value.lower().startswith("doi:"):
        return value[4:].strip()
    return ""


def _fulltext_links(message: dict[str, Any]) -> list[str]:
    links = message.get("link")
    if not isinstance(links, list):
        return []
    types: list[str] = []
    for link in links:
        if isinstance(link, dict):
            content_type = _text(link.get("content-type")) or "unspecified"
            types.append(content_type)
    return types


def _data_relation_types(message: dict[str, Any]) -> list[str]:
    relation = message.get("relation")
    if not isinstance(relation, dict):
        return []
    interesting = ("is-supplemented-by", "references", "is-derived-from", "has-part")
    return sorted(key for key in relation if key in interesting)


def resolve_candidate_source(
    row: dict[str, str],
    *,
    fetch_json: Callable[[str], tuple[int, Any]],
) -> SourceReceipt:
    """Resolve one candidate's DOI to a deterministic access receipt."""

    candidate_id = _text(row.get("candidate_id"))
    source = _text(row.get("source"))
    doi = doi_from_source(source)
    if not doi:
        return SourceReceipt(
            candidate_id=candidate_id, source=source, doi="", access_state="no_doi_supplied",
            resolved="false", work_type="", is_referenced_by_count="", license_present="",
            fulltext_link_count="", fulltext_content_types="", data_relation_types="",
            notes="Source is not a DOI (pmid/url); resolve a DOI before Crossref lookup.",
        )
    try:
        status, payload = fetch_json(CROSSREF_WORKS + quote(doi, safe=""))
    except Exception as error:  # network / parse failure
        return SourceReceipt(
            candidate_id=candidate_id, source=source, doi=doi, access_state="crossref_unresolved",
            resolved="false", work_type="", is_referenced_by_count="", license_present="",
            fulltext_link_count="", fulltext_content_types="", data_relation_types="",
            notes=f"{type(error).__name__}: {error}",
        )
    if status >= 400 or not isinstance(payload, dict) or not isinstance(payload.get("message"), dict):
        return SourceReceipt(
            candidate_id=candidate_id, source=source, doi=doi, access_state="crossref_unresolved",
            resolved="false", work_type="", is_referenced_by_count="", license_present="",
            fulltext_link_count="", fulltext_content_types="", data_relation_types="",
            notes=f"Crossref returned HTTP {status} or no message.",
        )
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
    return SourceReceipt(
        candidate_id=candidate_id, source=source, doi=doi, access_state=state, resolved="true",
        work_type=_text(message.get("type")),
        is_referenced_by_count=_text(message.get("is-referenced-by-count")),
        license_present=license_present,
        fulltext_link_count=str(len(fulltext)),
        fulltext_content_types=";".join(sorted(set(fulltext))),
        data_relation_types=";".join(data_relations),
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
    for receipt in receipts:
        states[receipt.access_state] = states.get(receipt.access_state, 0) + 1
    return {
        "candidate_count": len(receipts),
        "counts_by_access_state": dict(sorted(states.items())),
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
