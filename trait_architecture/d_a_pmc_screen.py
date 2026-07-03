"""Bounded full-text XML screen for registered PMC d_A candidate leads.

The d_A scouting table contains two leads explicitly anchored to PMC records. This
module fetches only those exact PMCID records through Europe PMC's full-text XML
endpoint and emits locator metadata: matched section titles, table labels, and
route-structure signals from declared term families. It does not retain article
XML, copy tables, estimate effects, determine direction, or promote a lead into B2.

The screen answers only a feasibility question: does the accessible source appear
to contain a candidate trait intervention and an antagonist outcome in a structure
that warrants human source coding? It distinguishes that pattern from headings
that instead describe antagonist effects on pollinators (H -> P), which must not be
mistaken for d_A.
"""

from __future__ import annotations

import csv
import json
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Callable, Iterable
from urllib.parse import quote
from urllib.request import Request, urlopen


EUROPE_PMC_FULLTEXT = "https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
USER_AGENT = "bita d-a-pmc-screen/0.2"
PMCID_PATTERN = re.compile(r"PMC\d+", re.IGNORECASE)

TRAIT_TERMS = (
    "staminode", "display", "flower size", "floral size", "corolla", "exsertion",
    "scent", "fragrance", "nectar", "colour", "color", "petal",
)
ANTAGONIST_TERMS = (
    "florivor", "herbivor", "beetle", "seed predat", "oviposition", "nectar rob",
    "pollen thief", "larcen", "damage",
)
INTERVENTION_TERMS = (
    "removal", "manipulation", "treatment", "choice experiment", "feeding choice",
)
POLLINATION_DOWNSTREAM_TERMS = (
    "pollinator", "pollination", "foraging behavior", "visitor", "reproductive fitness",
    "pollen transfer",
)
SCREEN_FIELDS = (
    "candidate_id", "pmcid", "doi", "trait_class", "antagonism_outcome",
    "source_access_status", "xml_bytes", "matched_trait_terms", "matched_antagonist_terms",
    "matched_section_titles", "matched_table_labels", "trait_intervention_section_titles",
    "antagonist_outcome_section_titles", "reverse_route_section_titles",
    "direct_route_screen_status", "route_structure_signal", "screen_note", "do_not_infer",
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
    trait_intervention_section_titles: str
    antagonist_outcome_section_titles: str
    reverse_route_section_titles: str
    direct_route_screen_status: str
    route_structure_signal: str
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


def _failure_screen(base: dict[str, str], *, access_status: str, note: str) -> PMCScreen:
    return PMCScreen(
        **base,
        source_access_status=access_status,
        xml_bytes="",
        matched_trait_terms="",
        matched_antagonist_terms="",
        matched_section_titles="",
        matched_table_labels="",
        trait_intervention_section_titles="",
        antagonist_outcome_section_titles="",
        reverse_route_section_titles="",
        direct_route_screen_status="not_screened",
        route_structure_signal="not_available",
        screen_note=note,
    )


def _route_structure_signal(
    *,
    trait_intervention_sections: list[str],
    antagonist_sections: list[str],
    reverse_sections: list[str],
    trait_hits: list[str],
    antagonist_hits: list[str],
) -> tuple[str, str]:
    """Triage headings without converting textual co-occurrence into a d_A effect."""

    if trait_intervention_sections and antagonist_sections and not reverse_sections:
        return (
            "candidate_A_to_H_experiment_structure_needs_numeric_context_check",
            "Trait-intervention and antagonist-outcome sections are both present; inspect model/table context, denominator, and effect direction before declaring d_A.",
        )
    if reverse_sections and not trait_intervention_sections:
        return (
            "probable_H_to_P_or_downstream_structure",
            "Antagonist and pollination/behavior terms co-occur in section headings without a trait-intervention section; do not code as d_A unless a direct trait-to-antagonist model is located.",
        )
    if trait_intervention_sections and antagonist_sections:
        return (
            "mixed_route_structure_needs_manual_disambiguation",
            "Both candidate d_A and possible downstream-route section structures occur; manually identify whether the same model links trait to antagonist outcome.",
        )
    if trait_hits and antagonist_hits:
        return (
            "term_cooccurrence_without_experiment_link",
            "Both term families occur, but section structure does not establish a trait-intervention to antagonist-outcome test.",
        )
    if trait_hits or antagonist_hits:
        return (
            "one_term_family_present",
            "Only one candidate term family appears in the full-text XML screen.",
        )
    return (
        "no_candidate_term_family_detected",
        "Neither candidate term family appears in the full-text XML screen.",
    )


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
        return _failure_screen(base, access_status="not_pmc_candidate", note="Registered source contains no PMCID.")
    url = EUROPE_PMC_FULLTEXT.format(pmcid=quote(pmcid))
    try:
        status, payload = fetch_xml(url)
        if status >= 400:
            raise RuntimeError(f"HTTP {status}")
        if len(payload) > 15 * 1024 * 1024:
            raise RuntimeError("XML response exceeds 15 MiB cap")
        root = ET.fromstring(payload)
    except Exception as error:
        return _failure_screen(base, access_status="xml_access_or_parse_failed", note=f"{type(error).__name__}: {error}")

    article_text = _plain(root)
    trait_hits = _matched(article_text, TRAIT_TERMS)
    antagonist_hits = _matched(article_text, ANTAGONIST_TERMS)
    doi = _text(root.findtext(".//article-id[@pub-id-type='doi']"))
    section_titles: list[str] = []
    trait_intervention_sections: list[str] = []
    antagonist_sections: list[str] = []
    reverse_sections: list[str] = []
    for section in root.findall(".//sec"):
        title = _plain(section.find("title")) or "untitled_section"
        text = _plain(section)
        section_trait = _matched(text, TRAIT_TERMS)
        section_antagonist = _matched(text, ANTAGONIST_TERMS)
        section_intervention = _matched(text, INTERVENTION_TERMS)
        section_pollination = _matched(text, POLLINATION_DOWNSTREAM_TERMS)
        if section_trait and section_antagonist:
            section_titles.append(title)
        if section_trait and section_intervention:
            trait_intervention_sections.append(title)
        if section_antagonist:
            antagonist_sections.append(title)
        if section_antagonist and section_pollination and not section_trait:
            reverse_sections.append(title)
    table_labels: list[str] = []
    for table in root.findall(".//table-wrap"):
        text = _plain(table)
        if _matched(text, TRAIT_TERMS) and _matched(text, ANTAGONIST_TERMS):
            table_labels.append(_plain(table.find("label")) or "unlabeled_table")

    signal, note = _route_structure_signal(
        trait_intervention_sections=_unique(trait_intervention_sections),
        antagonist_sections=_unique(antagonist_sections),
        reverse_sections=_unique(reverse_sections),
        trait_hits=trait_hits,
        antagonist_hits=antagonist_hits,
    )
    if trait_hits and antagonist_hits:
        route_status = "both_term_families_present_needs_human_route_coding"
    elif trait_hits or antagonist_hits:
        route_status = "one_term_family_present_not_direct_route"
    else:
        route_status = "no_candidate_term_family_detected"
    return PMCScreen(
        **{**base, "doi": doi},
        source_access_status="fulltext_xml_recovered",
        xml_bytes=str(len(payload)),
        matched_trait_terms=";".join(trait_hits),
        matched_antagonist_terms=";".join(antagonist_hits),
        matched_section_titles=";".join(_unique(section_titles)),
        matched_table_labels=";".join(_unique(table_labels)),
        trait_intervention_section_titles=";".join(_unique(trait_intervention_sections)),
        antagonist_outcome_section_titles=";".join(_unique(antagonist_sections)),
        reverse_route_section_titles=";".join(_unique(reverse_sections)),
        direct_route_screen_status=route_status,
        route_structure_signal=signal,
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
        "candidate_A_to_H_experiment_structure": sum(
            row.route_structure_signal == "candidate_A_to_H_experiment_structure_needs_numeric_context_check"
            for row in rows
        ),
        "probable_H_to_P_or_downstream_structure": sum(
            row.route_structure_signal == "probable_H_to_P_or_downstream_structure" for row in rows
        ),
        "decision_boundary": DO_NOT_INFER,
    }
    (destination / "d_a_pmc_fulltext_screen_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
    )
    return report
