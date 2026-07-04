"""Bounded C3/C4 probe for the PMID 27325896 seed-predation d_A candidate.

The registered candidate may be an observational floral-exsertion -> seed-predation
study rather than a trait-manipulation experiment. This module resolves its PMID
through NCBI's public id-conversion endpoint and, only when a PMCID is public,
searches XML for *co-located* exsertion and seed-predation terms plus a model context.
It first tries the Europe PMC full-text route and then NCBI EFetch for PMC records.
It stores identifiers and locators only; it never stores article prose, effect
values, signs, sample sizes, or a B2 eligibility decision.
"""

from __future__ import annotations

import csv
import json
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Iterable
from urllib.parse import quote
from urllib.request import Request, urlopen


PMID = "27325896"
NCBI_IDCONV = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?format=json&ids="
EUROPE_PMC_FULLTEXT = "https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
NCBI_PMC_EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id={pmc_numeric}"
USER_AGENT = "bita d-a-seedpred-pmid-probe/0.2"
TRAIT_TERMS = ("exsertion", "floral exsertion", "flower exsertion")
OUTCOME_TERMS = ("seed predat", "seed predator", "seed damage")
MODEL_TERMS = ("regression", "generalized linear", "glm", "glmm", "mixed model", "logistic", "model")
PROBE_FIELDS = (
    "candidate_id", "pmid", "doi", "pmcid", "idconv_status", "source_access_status", "xml_retrieval_route", "xml_bytes",
    "matched_trait_terms", "matched_antagonist_terms", "matched_model_terms", "shared_section_titles",
    "relevant_table_labels", "route_structure_signal", "direct_route_screen_status", "screen_note", "do_not_infer",
)
DO_NOT_INFER = (
    "PMID-resolution and XML term-location screen only. Do not infer a direct effect, direction, effect size, "
    "denominator, experimental unit, uncertainty, taxon, or B2 eligibility."
)


@dataclass(frozen=True)
class SeedPredProbe:
    candidate_id: str
    pmid: str
    doi: str
    pmcid: str
    idconv_status: str
    source_access_status: str
    xml_retrieval_route: str
    xml_bytes: str
    matched_trait_terms: str
    matched_antagonist_terms: str
    matched_model_terms: str
    shared_section_titles: str
    relevant_table_labels: str
    route_structure_signal: str
    direct_route_screen_status: str
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
    output: list[str] = []
    seen: set[str] = set()
    for value in values:
        value = _text(value)
        if value and value not in seen:
            seen.add(value)
            output.append(value)
    return output


def _fetch_json(url: str) -> tuple[int, Any]:
    request = Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    with urlopen(request, timeout=60) as response:  # nosec B310: fixed public NCBI endpoint
        status = int(getattr(response, "status", response.getcode()))
        return status, json.loads(response.read().decode("utf-8"))


def _fetch_xml(url: str) -> tuple[int, bytes]:
    request = Request(url, headers={"Accept": "application/xml,text/xml,*/*", "User-Agent": USER_AGENT})
    with urlopen(request, timeout=60) as response:  # nosec B310: exact resolved public full-text routes
        return int(getattr(response, "status", response.getcode())), response.read(15 * 1024 * 1024 + 1)


def _candidate(scouting_csv: str | Path) -> dict[str, str]:
    with Path(scouting_csv).open(encoding="utf-8", newline="") as handle:
        rows = [{key: _text(value) for key, value in row.items()} for row in csv.DictReader(handle)]
    matches = [row for row in rows if _text(row.get("candidate_id")) == "dA_cand_conflicting_seedpred"]
    if len(matches) != 1:
        raise ValueError("expected exactly one registered seed-predation d_A candidate")
    return matches[0]


def _idconv(payload: Any) -> tuple[str, str]:
    if not isinstance(payload, dict) or not isinstance(payload.get("records"), list) or not payload["records"]:
        return "", ""
    record = payload["records"][0]
    if not isinstance(record, dict):
        return "", ""
    return _text(record.get("doi")), _text(record.get("pmcid")).upper()


def _pmc_numeric(pmcid: str) -> str:
    return pmcid[3:] if pmcid.upper().startswith("PMC") else pmcid


def _failure(base: dict[str, str], *, idconv_status: str, access: str, note: str, xml_route: str = "") -> SeedPredProbe:
    return SeedPredProbe(
        **base,
        idconv_status=idconv_status,
        source_access_status=access,
        xml_retrieval_route=xml_route,
        xml_bytes="",
        matched_trait_terms="",
        matched_antagonist_terms="",
        matched_model_terms="",
        shared_section_titles="",
        relevant_table_labels="",
        route_structure_signal="not_available",
        direct_route_screen_status="not_screened",
        screen_note=note,
    )


def _recover_xml(
    pmcid: str,
    *,
    fetch_xml: Callable[[str], tuple[int, bytes]],
) -> tuple[str, bytes, str]:
    """Return (route, XML bytes, failure notes) after two fixed public routes."""

    routes = (
        ("europe_pmc_fulltext_xml", EUROPE_PMC_FULLTEXT.format(pmcid=quote(pmcid))),
        ("ncbi_pmc_efetch", NCBI_PMC_EFETCH.format(pmc_numeric=quote(_pmc_numeric(pmcid)))),
    )
    failures: list[str] = []
    for name, url in routes:
        try:
            status, payload = fetch_xml(url)
            if status >= 400:
                failures.append(f"{name}:HTTP_{status}")
                continue
            if len(payload) > 15 * 1024 * 1024:
                failures.append(f"{name}:response_exceeds_15MiB_cap")
                continue
            ET.fromstring(payload)
            return name, payload, ""
        except Exception as error:
            failures.append(f"{name}:{type(error).__name__}:{error}")
    return "", b"", "; ".join(failures)


def probe_candidate(
    candidate: dict[str, str],
    *,
    fetch_json: Callable[[str], tuple[int, Any]] = _fetch_json,
    fetch_xml: Callable[[str], tuple[int, bytes]] = _fetch_xml,
) -> SeedPredProbe:
    base = {"candidate_id": _text(candidate.get("candidate_id")), "pmid": PMID, "doi": "", "pmcid": ""}
    try:
        status, payload = fetch_json(NCBI_IDCONV + quote(PMID))
    except Exception as error:
        return _failure(base, idconv_status="request_failed", access="idconv_unavailable", note=f"{type(error).__name__}: {error}")
    if status >= 400:
        return _failure(base, idconv_status=f"http_{status}", access="idconv_unavailable", note="NCBI id-conversion returned an HTTP error.")
    doi, pmcid = _idconv(payload)
    base = {**base, "doi": doi, "pmcid": pmcid}
    if not pmcid:
        return _failure(base, idconv_status="resolved_no_pmcid", access="no_pmc_fulltext_route", note="PMID resolved without a PMCID; retain as an unverified candidate pending a lawful full-text route.")

    xml_route, xml, failure_note = _recover_xml(pmcid, fetch_xml=fetch_xml)
    if not xml_route:
        return _failure(base, idconv_status="resolved_pmcid", access="xml_access_or_parse_failed", xml_route="public_xml_routes_exhausted", note=failure_note)
    root = ET.fromstring(xml)

    article = _plain(root)
    trait_hits = _matched(article, TRAIT_TERMS)
    outcome_hits = _matched(article, OUTCOME_TERMS)
    model_hits = _matched(article, MODEL_TERMS)
    shared_sections: list[str] = []
    model_sections: list[str] = []
    for section in root.findall(".//sec"):
        title = _plain(section.find("title")) or "untitled_section"
        body = _plain(section)
        if _matched(body, TRAIT_TERMS) and _matched(body, OUTCOME_TERMS):
            shared_sections.append(title)
            if _matched(body, MODEL_TERMS):
                model_sections.append(title)
    table_labels = [
        _plain(table.find("label")) or "unlabeled_table"
        for table in root.findall(".//table-wrap")
        if _matched(_plain(table), TRAIT_TERMS) and _matched(_plain(table), OUTCOME_TERMS)
    ]

    if shared_sections and (model_sections or table_labels):
        signal = "candidate_observational_trait_to_seed_predation_model_needs_numeric_context_check"
        note = "Exsertion and seed-predation terms co-locate in at least one section with model context or a relevant table; inspect the exact model, denominator, and uncertainty before any d_A coding."
    elif trait_hits and outcome_hits:
        signal = "term_cooccurrence_without_model_context"
        note = "Trait and seed-predation terms occur in the XML, but no co-located model/table context was found."
    elif trait_hits or outcome_hits:
        signal = "one_term_family_present"
        note = "Only one candidate term family appears in the public XML."
    else:
        signal = "no_candidate_term_family_detected"
        note = "Neither floral-exsertion nor seed-predation terms appear in the public XML screen."
    status_label = "both_term_families_present_needs_human_route_coding" if trait_hits and outcome_hits else ("one_term_family_present_not_direct_route" if trait_hits or outcome_hits else "no_candidate_term_family_detected")
    return SeedPredProbe(
        **base,
        idconv_status="resolved_pmcid",
        source_access_status="fulltext_xml_recovered",
        xml_retrieval_route=xml_route,
        xml_bytes=str(len(xml)),
        matched_trait_terms=";".join(trait_hits),
        matched_antagonist_terms=";".join(outcome_hits),
        matched_model_terms=";".join(model_hits),
        shared_section_titles=";".join(_unique(shared_sections)),
        relevant_table_labels=";".join(_unique(table_labels)),
        route_structure_signal=signal,
        direct_route_screen_status=status_label,
        screen_note=note,
    )


def write_outputs(out_dir: str | Path, rows: Iterable[SeedPredProbe]) -> dict[str, object]:
    rows = list(rows)
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    with (destination / "d_a_seedpred_pmid_probe.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=PROBE_FIELDS)
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)
    report = {
        "candidate_count": len(rows),
        "pmcid_resolved": sum(bool(row.pmcid) for row in rows),
        "fulltext_xml_recovered": sum(row.source_access_status == "fulltext_xml_recovered" for row in rows),
        "candidate_observational_direct_route": sum(row.route_structure_signal == "candidate_observational_trait_to_seed_predation_model_needs_numeric_context_check" for row in rows),
        "decision_boundary": DO_NOT_INFER,
    }
    (destination / "d_a_seedpred_pmid_probe_report.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def probe_scouting_file(
    scouting_csv: str | Path,
    out_dir: str | Path,
    *,
    fetch_json: Callable[[str], tuple[int, Any]] = _fetch_json,
    fetch_xml: Callable[[str], tuple[int, bytes]] = _fetch_xml,
) -> dict[str, object]:
    return write_outputs(out_dir, [probe_candidate(_candidate(scouting_csv), fetch_json=fetch_json, fetch_xml=fetch_xml)])
