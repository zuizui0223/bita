"""Bounded XML route screen for the fixed scent/reward d_A eLife lead.

The Schiestl eLife lead is already registered in the d_A scouting table and its
source probe established public XML access. This module reads only an exact XML
receipt, emits headings/figure/table locators for scent-or-nectar and oviposition
terms, and creates no effect estimate. It is a C4 feasibility screen, not evidence
that the source identifies a d_A coefficient.
"""

from __future__ import annotations

import csv
import json
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable
from urllib.request import Request, urlopen


USER_AGENT = "bita d-a-elife-screen/0.1"
MAX_XML_BYTES = 15 * 1024 * 1024
TRAIT_TERMS = ("scent", "fragrance", "volatile", "odor", "odour", "nectar", "reward")
ANTAGONIST_TERMS = ("oviposition", "oviposit", "egg", "larva", "herbivor", "florivor")
INTERVENTION_TERMS = ("selection", "manipulation", "treatment", "experimental", "supplement")
SCREEN_FIELDS = (
    "candidate_id", "doi", "xml_url", "source_access_status", "xml_bytes",
    "matched_trait_terms", "matched_antagonist_terms", "matched_section_titles",
    "trait_intervention_section_titles", "antagonist_outcome_section_titles",
    "referenced_figure_labels", "referenced_table_labels", "route_structure_signal",
    "c4_extraction_status", "screen_note", "do_not_infer",
)
DO_NOT_INFER = (
    "XML locator only. Do not infer a direct d_A effect, effect direction, denominator, "
    "uncertainty, experimental unit, or B2 eligibility until source context is read."
)


@dataclass(frozen=True)
class ELifeScreen:
    candidate_id: str
    doi: str
    xml_url: str
    source_access_status: str
    xml_bytes: str
    matched_trait_terms: str
    matched_antagonist_terms: str
    matched_section_titles: str
    trait_intervention_section_titles: str
    antagonist_outcome_section_titles: str
    referenced_figure_labels: str
    referenced_table_labels: str
    route_structure_signal: str
    c4_extraction_status: str
    screen_note: str
    do_not_infer: str = DO_NOT_INFER


def _text(value: object) -> str:
    return str(value or "").strip()


def _plain(element: ET.Element | None) -> str:
    return "" if element is None else " ".join("".join(element.itertext()).split())


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


def read_xml_receipt(path: str | Path) -> dict[str, str]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = [{key: _text(value) for key, value in row.items()} for row in csv.DictReader(handle)]
    xml_rows = [row for row in rows if row.get("access_status") == "public_xml_prefix_recovered"]
    if not xml_rows:
        raise ValueError("no public XML receipt available for the eLife d_A lead")
    xml_rows.sort(key=lambda row: (row.get("source_label") != "elife_xml", row.get("source_url", "")))
    return xml_rows[0]


def _fetch_xml(url: str) -> tuple[int, bytes]:
    request = Request(url, headers={"Accept": "application/xml,text/xml,*/*", "User-Agent": USER_AGENT})
    with urlopen(request, timeout=60) as response:  # nosec B310: exact public XML URL from a source probe receipt
        return int(getattr(response, "status", response.getcode())), response.read(MAX_XML_BYTES + 1)


def _labels(root: ET.Element, tag: str) -> dict[str, str]:
    labels: dict[str, str] = {}
    for element in root.findall(f".//{tag}"):
        identifier = _text(element.get("id"))
        if identifier:
            labels[identifier] = _plain(element.find("label")) or identifier
    return labels


def _refs(section: ET.Element, figures: dict[str, str], tables: dict[str, str]) -> tuple[list[str], list[str]]:
    f_labels: list[str] = []
    t_labels: list[str] = []
    for ref in section.findall(".//xref"):
        identifier = _text(ref.get("rid"))
        kind = _text(ref.get("ref-type")).casefold()
        if kind == "fig" and identifier:
            f_labels.append(figures.get(identifier, identifier))
        if kind in {"table", "table-wrap"} and identifier:
            t_labels.append(tables.get(identifier, identifier))
    return f_labels, t_labels


def screen_receipt(receipt: dict[str, str], *, fetch_xml: Callable[[str], tuple[int, bytes]] = _fetch_xml) -> ELifeScreen:
    base = {"candidate_id": receipt.get("candidate_id", ""), "doi": receipt.get("doi", ""), "xml_url": receipt.get("source_url", "")}
    try:
        status, payload = fetch_xml(base["xml_url"])
        if status >= 400:
            raise RuntimeError(f"HTTP {status}")
        if len(payload) > MAX_XML_BYTES:
            raise RuntimeError("XML response exceeds 15 MiB cap")
        root = ET.fromstring(payload)
    except Exception as error:
        return ELifeScreen(**base, source_access_status="xml_access_or_parse_failed", xml_bytes="", matched_trait_terms="", matched_antagonist_terms="", matched_section_titles="", trait_intervention_section_titles="", antagonist_outcome_section_titles="", referenced_figure_labels="", referenced_table_labels="", route_structure_signal="not_available", c4_extraction_status="blocked_before_source_context", screen_note=f"{type(error).__name__}: {error}")

    article = _plain(root)
    trait_hits, antagonist_hits = _matched(article, TRAIT_TERMS), _matched(article, ANTAGONIST_TERMS)
    figures, tables = _labels(root, "fig"), _labels(root, "table-wrap")
    shared, trait_intervention, antagonist_sections, fig_refs, table_refs = [], [], [], [], []
    for section in root.findall(".//sec"):
        title = _plain(section.find("title")) or "untitled_section"
        body = _plain(section)
        title_trait, title_antagonist, title_intervention = _matched(title, TRAIT_TERMS), _matched(title, ANTAGONIST_TERMS), _matched(title, INTERVENTION_TERMS)
        body_trait, body_antagonist = _matched(body, TRAIT_TERMS), _matched(body, ANTAGONIST_TERMS)
        if body_trait and body_antagonist:
            shared.append(title)
            f, t = _refs(section, figures, tables)
            fig_refs.extend(f); table_refs.extend(t)
        if title_trait and title_intervention:
            trait_intervention.append(title)
        if title_antagonist:
            antagonist_sections.append(title)
    shared, trait_intervention, antagonist_sections = _unique(shared), _unique(trait_intervention), _unique(antagonist_sections)
    if shared and trait_hits and antagonist_hits:
        signal = "candidate_scent_reward_to_oviposition_structure_needs_numeric_context_check"
        status = "needs_manual_model_and_effect_context"
        note = "At least one source section contains both scent/reward and oviposition-term families; inspect treatment, model, and outcome denominator before declaring d_A."
    elif trait_hits and antagonist_hits:
        signal = "term_cooccurrence_without_same_section_link"
        status = "needs_manual_route_context"
        note = "Both term families occur in the article but not in a shared section locator."
    else:
        signal = "insufficient_term_structure"
        status = "not_a_C4_target_from_XML_screen"
        note = "The XML screen did not recover both scent/reward and oviposition term families."
    return ELifeScreen(**base, source_access_status="fulltext_xml_recovered", xml_bytes=str(len(payload)), matched_trait_terms=";".join(trait_hits), matched_antagonist_terms=";".join(antagonist_hits), matched_section_titles=";".join(shared), trait_intervention_section_titles=";".join(trait_intervention), antagonist_outcome_section_titles=";".join(antagonist_sections), referenced_figure_labels=";".join(_unique(fig_refs)), referenced_table_labels=";".join(_unique(table_refs)), route_structure_signal=signal, c4_extraction_status=status, screen_note=note)


def write_outputs(out_dir: str | Path, rows: Iterable[ELifeScreen]) -> dict[str, object]:
    rows = list(rows)
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    with (destination / "d_a_elife_xml_screen.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SCREEN_FIELDS)
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)
    report = {
        "screened_source_count": len(rows),
        "fulltext_xml_recovered": sum(row.source_access_status == "fulltext_xml_recovered" for row in rows),
        "candidate_c4_structure": sum(row.route_structure_signal == "candidate_scent_reward_to_oviposition_structure_needs_numeric_context_check" for row in rows),
        "decision_boundary": DO_NOT_INFER,
    }
    (destination / "d_a_elife_xml_screen_report.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report
