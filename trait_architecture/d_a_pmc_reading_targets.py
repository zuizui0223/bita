"""Build bounded C4 reading targets for viable PMC d_A leads.

This consumes the route-structure screen and re-fetches only candidates marked as a
possible trait-intervention -> antagonist-outcome experiment. It records exact
section titles, figure/table labels referenced from those sections, and broad model
method terms. It never stores article XML/prose, extracts an effect, or declares a
candidate eligible for B2.
"""

from __future__ import annotations

import csv
import json
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable
from urllib.parse import quote
from urllib.request import Request, urlopen

from .d_a_pmc_screen import EUROPE_PMC_FULLTEXT, USER_AGENT, _text


VIABLE_SIGNAL = "candidate_A_to_H_experiment_structure_needs_numeric_context_check"
MODEL_TERMS = ("generalized linear", "glmm", "glm", "mixed model", "binomial", "logistic")
TARGET_FIELDS = (
    "candidate_id", "pmcid", "doi", "empirical_track", "trait_class", "antagonism_outcome",
    "source_access_status", "target_trait_intervention_sections", "target_antagonist_outcome_sections",
    "referenced_figure_labels", "referenced_table_labels", "model_method_terms",
    "c4_extraction_status", "c4_action", "do_not_infer",
)
DO_NOT_INFER = (
    "C4 reading-target locator only. Do not infer treatment/control values, effect direction, "
    "denominator, variance, experimental unit, or B2 eligibility until the cited source context is read."
)


@dataclass(frozen=True)
class PMCReadingTarget:
    candidate_id: str
    pmcid: str
    doi: str
    empirical_track: str
    trait_class: str
    antagonism_outcome: str
    source_access_status: str
    target_trait_intervention_sections: str
    target_antagonist_outcome_sections: str
    referenced_figure_labels: str
    referenced_table_labels: str
    model_method_terms: str
    c4_extraction_status: str
    c4_action: str
    do_not_infer: str = DO_NOT_INFER


def _fetch_xml(url: str) -> tuple[int, bytes]:
    request = Request(url, headers={"Accept": "application/xml,text/xml,*/*", "User-Agent": USER_AGENT})
    with urlopen(request, timeout=60) as response:  # nosec B310: exact PMCID endpoint preselected by source screen
        return int(getattr(response, "status", response.getcode())), response.read(15 * 1024 * 1024 + 1)


def _plain(element: ET.Element | None) -> str:
    return "" if element is None else " ".join("".join(element.itertext()).split())


def _split(value: str) -> list[str]:
    return [item.strip() for item in _text(value).split(";") if item.strip()]


def _track(trait_class: str) -> str:
    folded = trait_class.casefold()
    if any(term in folded for term in ("display", "staminode", "flower_size", "visual", "colour", "color")):
        return "visual_display"
    if any(term in folded for term in ("scent", "nectar", "reward", "fragrance")):
        return "scent_reward"
    return "unresolved_trait_track"


def read_screen(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = [{key: _text(value) for key, value in row.items()} for row in csv.DictReader(handle)]
    required = {
        "candidate_id", "pmcid", "doi", "trait_class", "antagonism_outcome",
        "trait_intervention_section_titles", "antagonist_outcome_section_titles", "route_structure_signal",
    }
    if rows and not required.issubset(rows[0]):
        raise ValueError("d_A PMC screen lacks required fields")
    return [row for row in rows if row["route_structure_signal"] == VIABLE_SIGNAL]


def _labels(root: ET.Element, tag: str) -> dict[str, str]:
    output: dict[str, str] = {}
    for element in root.findall(f".//{tag}"):
        identifier = _text(element.get("id"))
        if identifier:
            output[identifier] = _plain(element.find("label")) or identifier
    return output


def _references(section: ET.Element, *, figures: dict[str, str], tables: dict[str, str]) -> tuple[list[str], list[str]]:
    figure_labels: list[str] = []
    table_labels: list[str] = []
    for xref in section.findall(".//xref"):
        identifier = _text(xref.get("rid"))
        kind = _text(xref.get("ref-type")).casefold()
        if kind == "fig" and identifier:
            figure_labels.append(figures.get(identifier, identifier))
        if kind in {"table", "table-wrap"} and identifier:
            table_labels.append(tables.get(identifier, identifier))
    return figure_labels, table_labels


def _unique(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        value = _text(value)
        if value and value not in seen:
            seen.add(value)
            output.append(value)
    return output


def build_target(row: dict[str, str], *, fetch_xml: Callable[[str], tuple[int, bytes]] = _fetch_xml) -> PMCReadingTarget:
    base = {
        "candidate_id": row["candidate_id"],
        "pmcid": row["pmcid"],
        "doi": row["doi"],
        "empirical_track": _track(row["trait_class"]),
        "trait_class": row["trait_class"],
        "antagonism_outcome": row["antagonism_outcome"],
    }
    trait_sections = _split(row["trait_intervention_section_titles"])
    antagonist_sections = _split(row["antagonist_outcome_section_titles"])
    try:
        status, payload = fetch_xml(EUROPE_PMC_FULLTEXT.format(pmcid=quote(row["pmcid"])))
        if status >= 400:
            raise RuntimeError(f"HTTP {status}")
        root = ET.fromstring(payload)
    except Exception as error:
        return PMCReadingTarget(
            **base,
            source_access_status="xml_access_or_parse_failed",
            target_trait_intervention_sections=";".join(trait_sections),
            target_antagonist_outcome_sections=";".join(antagonist_sections),
            referenced_figure_labels="",
            referenced_table_labels="",
            model_method_terms="",
            c4_extraction_status="blocked_before_source_context",
            c4_action=f"Resolve XML/source access before C4 reading: {type(error).__name__}: {error}",
        )

    figures = _labels(root, "fig")
    tables = _labels(root, "table-wrap")
    figures_found: list[str] = []
    tables_found: list[str] = []
    model_text: list[str] = []
    target_titles = set(trait_sections + antagonist_sections)
    for section in root.findall(".//sec"):
        title = _plain(section.find("title")) or "untitled_section"
        if title not in target_titles:
            continue
        figure_labels, table_labels = _references(section, figures=figures, tables=tables)
        figures_found.extend(figure_labels)
        tables_found.extend(table_labels)
        section_text = _plain(section).casefold()
        model_text.extend(term for term in MODEL_TERMS if term in section_text)

    return PMCReadingTarget(
        **base,
        source_access_status="fulltext_xml_recovered",
        target_trait_intervention_sections=";".join(trait_sections),
        target_antagonist_outcome_sections=";".join(antagonist_sections),
        referenced_figure_labels=";".join(_unique(figures_found)),
        referenced_table_labels=";".join(_unique(tables_found)),
        model_method_terms=";".join(_unique(model_text)),
        c4_extraction_status="needs_manual_model_and_effect_context",
        c4_action=(
            "Read the listed intervention and antagonist sections together; recover treatment/control, "
            "antagonist outcome denominator, model coefficient or raw contrast, uncertainty, and cited figure/table context."
        ),
    )


def build_targets(rows: Iterable[dict[str, str]], *, fetch_xml: Callable[[str], tuple[int, bytes]] = _fetch_xml) -> list[PMCReadingTarget]:
    return [build_target(row, fetch_xml=fetch_xml) for row in rows]


def write_outputs(out_dir: str | Path, rows: Iterable[PMCReadingTarget]) -> dict[str, object]:
    rows = list(rows)
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    with (destination / "d_a_pmc_c4_reading_targets.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=TARGET_FIELDS)
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)
    report = {
        "target_count": len(rows),
        "fulltext_xml_recovered": sum(row.source_access_status == "fulltext_xml_recovered" for row in rows),
        "visual_display_targets": sum(row.empirical_track == "visual_display" for row in rows),
        "scent_reward_targets": sum(row.empirical_track == "scent_reward" for row in rows),
        "decision_boundary": DO_NOT_INFER,
    }
    (destination / "d_a_pmc_c4_reading_targets_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
    )
    return report
