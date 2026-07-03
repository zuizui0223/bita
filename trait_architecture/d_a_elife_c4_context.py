"""Bounded C4 context assessment for the fixed Schiestl eLife d_A source.

The public XML and two primary figures establish that this source is readable, but
C4 must still answer whether one exact comparison supplies treatment/control,
outcome unit, experimental unit, replication, uncertainty, and a recoverable
numerical effect. This module records only structured *presence/absence* signals
and section/figure locators. It never stores article prose, digitizes a figure, or
computes an effect size.
"""

from __future__ import annotations

import csv
import json
import re
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable

from .d_a_elife_screen import _fetch_xml, _plain, _text, read_xml_receipt


OVIPOSITION_TITLE = "oviposition trials"
CONTROL_TERMS = ("control", "empty vector", "wild type", "untransformed")
OUTCOME_TERMS = ("egg", "oviposition", "plant", "day")
UNIT_TERMS = ("plant", "flower", "individual", "day")
REPLICATION_TERMS = ("replicate", "replication", "sample size", "n =", "n=")
UNCERTAINTY_TERMS = ("standard error", "s.e.", "se", "confidence interval", "error bar")
MODEL_TERMS = ("generalized linear", "linear model", "anova", "glm", "glmm", "model")
NUMERIC_TABLE_TERMS = ("table", "supplementary file")
CONTEXT_FIELDS = (
    "candidate_id", "doi", "xml_url", "source_access_status", "xml_bytes",
    "oviposition_section_locator", "figure_2_locator", "control_context_signal",
    "outcome_context_signal", "experimental_unit_context_signal", "replication_context_signal",
    "uncertainty_context_signal", "model_context_signal", "numeric_table_context_signal",
    "c4_readout_status", "c4_decision", "do_not_infer",
)
DO_NOT_INFER = (
    "Structured context signals and locators only. Do not infer a treatment mapping, effect direction, "
    "numeric contrast, uncertainty value, or B2 eligibility unless the same source context explicitly "
    "supplies the required fields."
)


@dataclass(frozen=True)
class C4Context:
    candidate_id: str
    doi: str
    xml_url: str
    source_access_status: str
    xml_bytes: str
    oviposition_section_locator: str
    figure_2_locator: str
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


def _matching_sections(root: ET.Element) -> list[ET.Element]:
    sections: list[ET.Element] = []
    for section in root.findall(".//sec"):
        title = _plain(section.find("title")).casefold()
        if OVIPOSITION_TITLE in title:
            sections.append(section)
    return sections


def _figure_locator(root: ET.Element) -> str:
    for figure in root.findall(".//fig"):
        label = _plain(figure.find("label"))
        if label == "Figure 2.":
            return label
    return ""


def _numeric_table_signal(root: ET.Element, section_text: str) -> bool:
    # A source may contain a table, but this deliberately requires a table/supplement
    # locator in the same Oviposition section before it is considered a candidate
    # numerical source. A plotted bar alone never satisfies the B2 numeric gate.
    if not _has_any(section_text, NUMERIC_TABLE_TERMS):
        return False
    return bool(root.findall(".//table-wrap"))


def assess_receipt(
    receipt: dict[str, str],
    *,
    fetch_xml: Callable[[str], tuple[int, bytes]] = _fetch_xml,
) -> C4Context:
    base = {
        "candidate_id": _text(receipt.get("candidate_id")),
        "doi": _text(receipt.get("doi")),
        "xml_url": _text(receipt.get("source_url")),
    }
    try:
        status, payload = fetch_xml(base["xml_url"])
        if status >= 400:
            raise RuntimeError(f"HTTP {status}")
        root = ET.fromstring(payload)
    except Exception:
        return C4Context(
            **base,
            source_access_status="xml_access_or_parse_failed",
            xml_bytes="",
            oviposition_section_locator="",
            figure_2_locator="",
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

    sections = _matching_sections(root)
    section_text = " ".join(_plain(section) for section in sections)
    figure_2 = _figure_locator(root)
    control = _has_any(section_text, CONTROL_TERMS)
    outcome = _has_any(section_text, OUTCOME_TERMS)
    unit = _has_any(section_text, UNIT_TERMS)
    replication = _has_any(section_text, REPLICATION_TERMS) or bool(re.search(r"\bn\s*[=:]\s*\d+", section_text, flags=re.I))
    uncertainty = _has_any(section_text, UNCERTAINTY_TERMS)
    model = _has_any(section_text, MODEL_TERMS)
    numeric_table = _numeric_table_signal(root, section_text)

    # The source needs an explicitly recoverable numeric comparison with uncertainty
    # before it can reach B2. The context audit does not turn a plotted mean/error
    # bar into a number; absent table/supplement context remains non-numeric.
    if sections and figure_2 and control and outcome and unit and replication and uncertainty and numeric_table:
        readout = "context_fields_present_needs_manual_numeric_verification"
        decision = "manual_numeric_extraction_required_before_B2"
    elif sections and figure_2 and outcome:
        readout = "route_context_located_numeric_effect_not_recovered"
        decision = "retain_as_directional_or_C4_evidence_not_B2"
    else:
        readout = "incomplete_context"
        decision = "retain_as_C4_target"

    return C4Context(
        **base,
        source_access_status="fulltext_xml_recovered",
        xml_bytes=str(len(payload)),
        oviposition_section_locator="Oviposition trials" if sections else "",
        figure_2_locator=figure_2,
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


def write_outputs(out_dir: str | Path, rows: Iterable[C4Context]) -> dict[str, object]:
    rows = list(rows)
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    with (destination / "d_a_elife_c4_context.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CONTEXT_FIELDS)
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)
    report = {
        "assessed_source_count": len(rows),
        "numeric_context_candidates": sum(
            row.c4_decision == "manual_numeric_extraction_required_before_B2" for row in rows
        ),
        "non_B2_contexts": sum(
            row.c4_decision == "retain_as_directional_or_C4_evidence_not_B2" for row in rows
        ),
        "decision_boundary": DO_NOT_INFER,
    }
    (destination / "d_a_elife_c4_context_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
    )
    return report


def assess_probe_csv(
    probe_csv: str | Path,
    out_dir: str | Path,
    *,
    fetch_xml: Callable[[str], tuple[int, bytes]] = _fetch_xml,
) -> dict[str, object]:
    rows = [assess_receipt(read_xml_receipt(probe_csv), fetch_xml=fetch_xml)]
    return write_outputs(out_dir, rows)
