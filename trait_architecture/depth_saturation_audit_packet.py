"""Retrieve Crossref metadata abstracts for the head-versus-tail audit queue.

The resulting packet is for source triage only. It preserves the frozen depth and
screen stratum for every selected query-rank membership and deliberately makes no
claim about trait measurement, effect direction, or meta-analytic eligibility.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Callable, Iterable
from urllib.parse import quote

from trait_architecture.broad_calibration_abstracts import (
    CROSSREF_WORKS_URL,
    _plain_text,
    _request_json,
    _text,
    _year,
)
from trait_architecture.depth_saturation_audit import DEPTH_AUDIT_FIELDS


DEPTH_PACKET_FIELDS = (
    *DEPTH_AUDIT_FIELDS,
    "crossref_lookup_status",
    "crossref_message_type",
    "crossref_title",
    "crossref_published_year",
    "crossref_container_title",
    "crossref_abstract_available",
    "crossref_abstract_text",
    "source_packet_warning",
)
WARNING = (
    "Crossref metadata abstracts support source screening only. They do not alone "
    "establish a measured direct route, effect direction, causal design, or quantitative eligibility."
)


def read_depth_audit_queue(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = [{key: _text(value) for key, value in row.items()} for row in csv.DictReader(handle)]
    if rows and not set(DEPTH_AUDIT_FIELDS).issubset(rows[0]):
        raise ValueError("depth audit queue lacks required fields")
    return rows


def _lookup(doi: str, request_json: Callable[[str], dict[str, Any]] | None) -> dict[str, str]:
    if not doi:
        return {
            "crossref_lookup_status": "not_attempted_missing_doi",
            "crossref_message_type": "",
            "crossref_title": "",
            "crossref_published_year": "",
            "crossref_container_title": "",
            "crossref_abstract_available": "false",
            "crossref_abstract_text": "",
            "source_packet_warning": WARNING + " No DOI was available for Crossref lookup.",
        }
    try:
        payload = _request_json(f"{CROSSREF_WORKS_URL}/{quote(doi, safe='')}", request_json)
        message = payload.get("message")
        if not isinstance(message, dict):
            raise ValueError("Crossref response lacks message object")
        abstract = _plain_text(message.get("abstract"))
        return {
            "crossref_lookup_status": "success",
            "crossref_message_type": _text(message.get("type")),
            "crossref_title": _plain_text(message.get("title")),
            "crossref_published_year": _year(message),
            "crossref_container_title": _plain_text(message.get("container-title")),
            "crossref_abstract_available": str(bool(abstract)).lower(),
            "crossref_abstract_text": abstract,
            "source_packet_warning": WARNING,
        }
    except Exception as error:
        return {
            "crossref_lookup_status": "failed",
            "crossref_message_type": "",
            "crossref_title": "",
            "crossref_published_year": "",
            "crossref_container_title": "",
            "crossref_abstract_available": "false",
            "crossref_abstract_text": "",
            "source_packet_warning": WARNING + f" Lookup failed: {type(error).__name__}: {error}",
        }


def build_depth_audit_abstract_packet(
    audit_rows: Iterable[dict[str, str]], *, request_json: Callable[[str], dict[str, Any]] | None = None,
) -> list[dict[str, str]]:
    """Retrieve each DOI once while retaining the frozen audit rows."""

    cache: dict[str, dict[str, str]] = {}
    packet: list[dict[str, str]] = []
    for raw in audit_rows:
        row = {field: _text(raw.get(field)) for field in DEPTH_AUDIT_FIELDS}
        doi = row["doi"]
        if doi not in cache:
            cache[doi] = _lookup(doi, request_json)
        packet.append({**row, **cache[doi]})
    return packet


def write_depth_audit_abstract_packet(path: str | Path, rows: Iterable[dict[str, str]]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=DEPTH_PACKET_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
