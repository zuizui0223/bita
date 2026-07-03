"""Bounded C4 context assessment for viable PMC d_A reading targets.

The PMC route screen identifies exact intervention and antagonist sections. This
module checks whether their shared XML context exposes the fields required before a
numerical effect could be manually recovered. It writes only structured signals and
locators; article prose, figure digitization, and effect-size calculation remain
out of scope.
"""

from __future__ import annotations

import csv
import json
import re
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable
from urllib.parse import quote

from .d_a_pmc_reading_targets import _fetch_xml, _plain, _split, _text, read_screen
from .d_a_pmc_screen import EUROPE_PMC_FULLTEXT


CONTROL_TERMS = ("control", "intact", "unmanipulated", "without removal", "sham")
OUTCOME_TERMS = ("florivory", "florivor", "beetle", "damage", "herbivory")
UNIT_TERMS = ("flower", "plant", "inflorescence", "head")
REPLICATION_TERMS = ("replicate", "replication", "sample size", "n =", "n=")
UNCERTAINTY_TERMS = ("standard error", "s.e.", "se", "confidence interval", "error bar")
MODEL_TERMS = ("generalized linear", "glmm", "glm", "mixed model", "binomial", "logistic", "anova", "model")
CONTEXT_FIELDS = (
    "candidate_id", "pmcid", "doi", "empirical_track", "source_access_status", "xml_bytes",
    "intervention_section_locators", "antagonist_section_locators", "referenced_figure_labels",
    "referenced_table_labels", "control_context_signal", "outcome_context_signal",
    "experimental_unit_context_signal", "replication_context_signal", "uncertainty_context_signal",
    "model_context_signal", "numeric_table_context_signal", "c4_readout_status", "c4_decision",
    "do_not_infer",
)
DO_NOT_INFER = (
    "Structured context signals and locators only. Do not infer treatment mapping, effect direction, "
    "numeric contrast, uncertainty value, or B2 eligibility unless the same source context explicitly "
    "supplies the required fields."
)


@dataclass(frozen=True)
class PMCC4Context:
    candidate_id: str
    pmcid: str
    doi: str
    empirical_track: str
    source_access_status: str
    xml_bytes: str
    intervention_section_locators: str
    antagonist_section_locators: str
    referenced_figure_labels: str
    referenced_table_labels: str
    control_context_signal: str
    outcome_context_signal: str
    experimental_unit_context_signal: str
    replication_context_signal: str
    uncertainty_context_signal: str
    model_context_signal: str
    numeric_table_context_signal: str
    c4_readout_status: str
    c4_decision: str
    do_not_infer: str = DO_NOT_INFER


def _has_any(text: str, terms: Iterable[str]) -> bool:
    folded = text.casefold()
    return any(term in folded for term in terms)


def _labels(root: ET.Element, tag: str) -> dict[str, str]:
    output: dict[str, str] = {}
    for element in root.findall(f".//{tag}"):
        identifier = _text(element.get("id"))
        if identifier:
            output[identifier] = _plain(element.find("label")) or identifier
    return output


def _unique(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        value = _text(value)
        if value and value not in seen:
            seen.add(value)
            output.append(value)
    return output


def _references(section: ET.Element, figures: dict[str, str], tables: dict[str, str]) -> tuple[list[str], list[str]]:
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


def assess_row(
    row: dict[str, str],
    *,
    fetch_xml: Callable[[str], tuple[int, bytes]] = _fetch_xml,
) -> PMCC4Context:
    intervention_titles = _split(row["trait_intervention_section_titles"])
    antagonist_titles = _split(row["antagonist_outcome_section_titles"])
    base = {
        "candidate_id": row["candidate_id"],
        "pmcid": row["pmcid"],
        "doi": row["doi"],
        "empirical_track": "visual_display",
        "intervention_section_locators": ";".join(intervention_titles),
        "antagonist_section_locators": ";".join(antagonist_titles),
    }
    try:
        status, payload = fetch_xml(EUROPE_PMC_FULLTEXT.format(pmcid=quote(row["pmcid"])))
        if status >= 400:
            raise RuntimeError(f"HTTP {status}")
        root = ET.fromstring(payload)
    except Exception:
        return PMCC4Context(
            **base,
            source_access_status="xml_access_or_parse_failed",
            xml_bytes="",
            referenced_figure_labels="",
            referenced_table_labels="",
            control_context_signal="not_available",
            outcome_context_signal="not_available",
            experimental_unit_context_signal="not_available",
            replication_context_signal="not_available",
            uncertainty_context_signal="not_available",
            model_context_signal="not_available",
            numeric_table_context_signal="not_available",
            c4_readout_status="blocked_before_context",
            c4_decision="retain_as_C4_target",
        )

    figures, tables = _labels(root, "fig"), _labels(root, "table-wrap")
    target_titles = set(intervention_titles + antagonist_titles)
    sections = [
        section for section in root.findall(".//sec")
        if (_plain(section.find("title")) or "untitled_section") in target_titles
    ]
    context = " ".join(_plain(section) for section in sections)
    figure_labels, table_labels = [], []
    for section in sections:
        f, t = _references(section, figures, tables)
        figure_labels.extend(f)
        table_labels.extend(t)
    control = _has_any(context, CONTROL_TERMS)
    outcome = _has_any(context, OUTCOME_TERMS)
    unit = _has_any(context, UNIT_TERMS)
    replication = _has_any(context, REPLICATION_TERMS) or bool(re.search(r"\bn\s*[=:]\s*\d+", context, flags=re.I))
    uncertainty = _has_any(context, UNCERTAINTY_TERMS)
    model = _has_any(context, MODEL_TERMS)
    # Only a table referenced from the relevant source context may open a numerical
    # extraction attempt. A Figure reference never satisfies this gate.
    numeric_table = bool(table_labels)

    if sections and control and outcome and unit and replication and uncertainty and numeric_table:
        readout = "context_fields_present_needs_manual_numeric_verification"
        decision = "manual_numeric_extraction_required_before_B2"
    elif sections and outcome:
        readout = "route_context_located_numeric_effect_not_recovered"
        decision = "retain_as_directional_or_C4_evidence_not_B2"
    else:
        readout = "incomplete_context"
        decision = "retain_as_C4_target"

    return PMCC4Context(
        **base,
        source_access_status="fulltext_xml_recovered",
        xml_bytes=str(len(payload)),
        referenced_figure_labels=";".join(_unique(figure_labels)),
        referenced_table_labels=";".join(_unique(table_labels)),
        control_context_signal="located" if control else "not_located",
        outcome_context_signal="located" if outcome else "not_located",
        experimental_unit_context_signal="located" if unit else "not_located",
        replication_context_signal="located" if replication else "not_located",
        uncertainty_context_signal="located" if uncertainty else "not_located",
        model_context_signal="located" if model else "not_located",
        numeric_table_context_signal="located" if numeric_table else "not_located",
        c4_readout_status=readout,
        c4_decision=decision,
    )


def write_outputs(out_dir: str | Path, rows: Iterable[PMCC4Context]) -> dict[str, object]:
    rows = list(rows)
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    with (destination / "d_a_pmc_c4_context.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CONTEXT_FIELDS)
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)
    report = {
        "assessed_source_count": len(rows),
        "numeric_context_candidates": sum(row.c4_decision == "manual_numeric_extraction_required_before_B2" for row in rows),
        "non_B2_contexts": sum(row.c4_decision == "retain_as_directional_or_C4_evidence_not_B2" for row in rows),
        "decision_boundary": DO_NOT_INFER,
    }
    (destination / "d_a_pmc_c4_context_report.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def assess_screen_csv(
    screen_csv: str | Path,
    out_dir: str | Path,
    *,
    fetch_xml: Callable[[str], tuple[int, bytes]] = _fetch_xml,
) -> dict[str, object]:
    return write_outputs(out_dir, [assess_row(row, fetch_xml=fetch_xml) for row in read_screen(screen_csv)])
