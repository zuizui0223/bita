"""Bounded full-text XML screen for the registered PMC d_A candidate leads.

The d_A scouting table contains two leads explicitly anchored to PMC records. This
module fetches only those exact PMCID records through Europe PMC's full-text XML
endpoint and emits locator metadata: matched section titles, table labels, and the
presence of declared trait/outcome term families. It does not retain article XML,
copy tables, estimate effects, determine direction, or promote a lead into B2.

The screen answers only a feasibility question: does the accessible source appear
to contain both a candidate attraction/display term and a candidate antagonist
outcome term that warrant human source coding?
"""

from __future__ import annotations

import csv
import json
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Callable, Iterable
from urllib.parse import quote
from urllib.request import Request, urlopen


EUROPE_PMC_FULLTEXT = "https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
USER_AGENT = "bita d-a-pmc-screen/0.1"
PMCID_PATTERN = re.compile(r"PMC\d+", re.IGNORECASE)

TRAIT_TERMS = (
    "staminode", "display", "flower size", "floral size", "corolla", "exsertion",
    "scent", "fragrance", "nectar", "colour", "color", "petal",
)
ANTAGONIST_TERMS = (
    "florivor", "herbivor", "beetle", "seed predat", "oviposition", "nectar rob",
    "pollen thief", "larcen", "damage",
)
SCREEN_FIELDS = (
    "candidate_id", "pmcid", "doi", "trait_class", "antagonism_outcome",
    "source_access_status", "xml_bytes", "matched_trait_terms", "matched_antagonist_terms",
    "matched_section_titles", "matched_table_labels", "direct_route_screen_status",
    "screen_note", "do_not_infer",
)
DO_NOT_INFER = (
    "Full-text XML term-location screen only. Do not infer a measured direct route, "
    "effect direction, effect size, denominator, causal design, or B2 eligibility."
)


@dataclass(frozen=True)
class PMCScreen:
    candidate_id: str
    pmcid: str
    doi: str
    trait_class: str
    antagonism_outcome: str
    source_access_status: str
    xml_bytes: str
    matched_trait_terms: str
    matched_antagonist_terms: str
    matched_section_titles: str
    matched_table_labels: str
    direct_route_screen_status: str
    screen_note: str
    do_not_infer: str = DO_NOT_INFER


def _text(value: object) -> str:
    return str(value or "").strip()


def _pmcid(source: str) -> str:
    match = PMCID_PATTERN.search(_text(source))
    return match.group(0).upper() if match else ""


def read_candidates(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = [{key: _text(value) for key, value in row.items()} for row in csv.DictReader(handle)]
    required = {"candidate_id", "source", "trait_class", "antagonism_outcome"}
    if rows and not required.issubset(rows[0]):
        raise ValueError("d_A scouting file lacks required columns")
    return [row for row in rows if _pmcid(row.get("source", ""))]


def _fetch_xml(url: str) -> tuple[int, bytes]:
    request = Request(url, headers={"Accept": "application/xml,text/xml,*/*", "User-Agent": USER_AGENT})
    with urlopen(request, timeout=60) as response:  # nosec B310: exact Europe PMC PMCID endpoint from registered source
        status = int(getattr(response, "status", response.getcode()))
        return status, response.read(15 * 1024 * 1024 + 1)


def _plain(element: ET.Element | None) -> str:
    if element is None:
        return ""
    return " ".join("".join(element.itertext()).split())


def _matched(text: str, terms: Iterable[str]) -> list[str]:
    folded = text.casefold()
    return [term for term in terms if term in folded]


def _unique(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        value = _text(value)
        if value and value not in seen:
            seen.add(value)
            output.append(value)
    return output


def screen_candidate(
    row: dict[str, str],
    *,
    fetch_xml: Callable[[str], tuple[int, bytes]] = _fetch_xml,
) -> PMCScreen:
    pmcid = _pmcid(row.get("source", ""))
    base = {
        "candidate_id": _text(row.get("candidate_id")),
        "pmcid": pmcid,
        "doi": "",
        "trait_class": _text(row.get("trait_class")),
        "antagonism_outcome": _text(row.get("antagonism_outcome")),
    }
    if not pmcid:
        return PMCScreen(**base, source_access_status="not_pmc_candidate", xml_bytes="", matched_trait_terms="", matched_antagonist_terms="", matched_section_titles="", matched_table_labels="", direct_route_screen_status="not_screened", screen_note="Registered source contains no PMCID.")
    url = EUROPE_PMC_FULLTEXT.format(pmcid=quote(pmcid))
    try:
        status, payload = fetch_xml(url)
        if status >= 400:
            raise RuntimeError(f"HTTP {status}")
        if len(payload) > 15 * 1024 * 1024:
            raise RuntimeError("XML response exceeds 15 MiB cap")
        root = ET.fromstring(payload)
    except Exception as error:
        return PMCScreen(**base, source_access_status="xml_access_or_parse_failed", xml_bytes="", matched_trait_terms="", matched_antagonist_terms="", matched_section_titles="", matched_table_labels="", direct_route_screen_status="not_screened", screen_note=f"{type(error).__name__}: {error}")

    article_text = _plain(root)
    trait_hits = _matched(article_text, TRAIT_TERMS)
    antagonist_hits = _matched(article_text, ANTAGONIST_TERMS)
    doi = _text(root.findtext(".//article-id[@pub-id-type='doi']"))
    section_titles: list[str] = []
    for section in root.findall(".//sec"):
        title = _plain(section.find("title"))
        text = _plain(section)
        if _matched(text, trait_hits) and _matched(text, antagonist_hits):
            section_titles.append(title or "untitled_section")
    table_labels: list[str] = []
    for table in root.findall(".//table-wrap"):
        text = _plain(table)
        if _matched(text, trait_hits) and _matched(text, antagonist_hits):
            table_labels.append(_plain(table.find("label")) or "unlabeled_table")
    if trait_hits and antagonist_hits:
        status = "both_term_families_present_needs_human_route_coding"
        note = "Source contains both candidate term families; inspect model/table context before declaring a direct d_A route."
    elif trait_hits or antagonist_hits:
        status = "one_term_family_present_not_direct_route"
        note = "Only one candidate term family appeared in the full-text XML screen."
    else:
        status = "no_candidate_term_family_detected"
        note = "Neither candidate term family appeared in the full-text XML screen."
    return PMCScreen(
        **base,
        doi=doi,
        source_access_status="fulltext_xml_recovered",
        xml_bytes=str(len(payload)),
        matched_trait_terms=";".join(trait_hits),
        matched_antagonist_terms=";".join(antagonist_hits),
        matched_section_titles=";".join(_unique(section_titles)),
        matched_table_labels=";".join(_unique(table_labels)),
        direct_route_screen_status=status,
        screen_note=note,
    )


def screen_candidates(
    rows: Iterable[dict[str, str]],
    *,
    fetch_xml: Callable[[str], tuple[int, bytes]] = _fetch_xml,
) -> list[PMCScreen]:
    return [screen_candidate(row, fetch_xml=fetch_xml) for row in rows]


def write_outputs(out_dir: str | Path, rows: Iterable[PMCScreen]) -> dict[str, object]:
    rows = list(rows)
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    with (destination / "d_a_pmc_fulltext_screen.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SCREEN_FIELDS)
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)
    report = {
        "pmc_candidate_count": len(rows),
        "fulltext_xml_recovered": sum(row.source_access_status == "fulltext_xml_recovered" for row in rows),
        "both_term_families_present": sum(row.direct_route_screen_status == "both_term_families_present_needs_human_route_coding" for row in rows),
        "decision_boundary": DO_NOT_INFER,
    }
    (destination / "d_a_pmc_fulltext_screen_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
    )
    return report
