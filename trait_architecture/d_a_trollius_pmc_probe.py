"""Locate public PMC XML for the fixed Trollius d_A candidate and screen route structure.

The Trollius candidate is registered as a possible display/antagonism context, not
as a verified d_A effect. This C3/C4 probe resolves its fixed DOI through Europe
PMC, then reuses the repository's heading-based PMC screen only if a PMCID and
full-text XML are public. It records accession and screen locators, never article
prose, numerical effects, or a d_A inclusion decision.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Iterable
from urllib.parse import quote
from urllib.request import Request, urlopen

from .d_a_pmc_screen import PMCScreen, screen_candidate


TROLLIUS_DOI = "10.1371/journal.pone.0118299"
EUROPE_PMC_SEARCH = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?format=json&query="
USER_AGENT = "bita d-a-trollius-pmc-probe/0.1"
PROBE_FIELDS = (
    "candidate_id", "doi", "pmcid", "pmid", "source_access_status", "search_status",
    "route_structure_signal", "direct_route_screen_status", "matched_trait_terms",
    "matched_antagonist_terms", "matched_section_titles", "matched_table_labels",
    "screen_note", "do_not_infer",
)
DO_NOT_INFER = (
    "DOI-to-PMC and heading-locator screen only. Do not infer a direct d_A route, effect direction, "
    "effect size, denominator, experimental unit, uncertainty, or B2 eligibility."
)


@dataclass(frozen=True)
class TrolliusProbe:
    candidate_id: str
    doi: str
    pmcid: str
    pmid: str
    source_access_status: str
    search_status: str
    route_structure_signal: str
    direct_route_screen_status: str
    matched_trait_terms: str
    matched_antagonist_terms: str
    matched_section_titles: str
    matched_table_labels: str
    screen_note: str
    do_not_infer: str = DO_NOT_INFER


def _text(value: object) -> str:
    return str(value or "").strip()


def _fetch_json(url: str) -> tuple[int, Any]:
    request = Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    with urlopen(request, timeout=60) as response:  # nosec B310: fixed public Europe PMC search
        status = int(getattr(response, "status", response.getcode()))
        return status, json.loads(response.read().decode("utf-8"))


def _candidate_row(path: str | Path) -> dict[str, str]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = [{key: _text(value) for key, value in row.items()} for row in csv.DictReader(handle)]
    match = [row for row in rows if _text(row.get("candidate_id")) == "dA_cand_trollius"]
    if len(match) != 1:
        raise ValueError("expected exactly one registered Trollius d_A candidate")
    return match[0]


def _pmc_result(payload: Any) -> dict[str, str]:
    if not isinstance(payload, dict):
        return {}
    result_list = payload.get("resultList")
    entries = result_list.get("result") if isinstance(result_list, dict) else []
    if not isinstance(entries, list):
        return {}
    exact = [entry for entry in entries if isinstance(entry, dict) and _text(entry.get("doi")).casefold() == TROLLIUS_DOI]
    entry = exact[0] if exact else next((item for item in entries if isinstance(item, dict)), {})
    return {
        "pmcid": _text(entry.get("pmcid")),
        "pmid": _text(entry.get("pmid")),
    } if isinstance(entry, dict) else {}


def probe_trollius(
    candidate: dict[str, str],
    *,
    fetch_json: Callable[[str], tuple[int, Any]] = _fetch_json,
    fetch_xml: Callable[[str], tuple[int, bytes]] | None = None,
) -> TrolliusProbe:
    base = {"candidate_id": _text(candidate.get("candidate_id")), "doi": TROLLIUS_DOI}
    try:
        status, payload = fetch_json(EUROPE_PMC_SEARCH + quote(f"DOI:{TROLLIUS_DOI}", safe=""))
    except Exception as error:
        return TrolliusProbe(**base, pmcid="", pmid="", source_access_status="pmc_search_failed", search_status="request_failed", route_structure_signal="not_available", direct_route_screen_status="not_screened", matched_trait_terms="", matched_antagonist_terms="", matched_section_titles="", matched_table_labels="", screen_note=f"{type(error).__name__}: {error}")
    if status >= 400:
        return TrolliusProbe(**base, pmcid="", pmid="", source_access_status="pmc_search_failed", search_status=f"http_{status}", route_structure_signal="not_available", direct_route_screen_status="not_screened", matched_trait_terms="", matched_antagonist_terms="", matched_section_titles="", matched_table_labels="", screen_note="Europe PMC DOI search returned an HTTP error.")
    identifiers = _pmc_result(payload)
    pmcid = identifiers.get("pmcid", "")
    if not pmcid:
        return TrolliusProbe(**base, pmcid="", pmid=identifiers.get("pmid", ""), source_access_status="no_pmc_fulltext_route", search_status="search_recovered_no_pmcid", route_structure_signal="not_available", direct_route_screen_status="not_screened", matched_trait_terms="", matched_antagonist_terms="", matched_section_titles="", matched_table_labels="", screen_note="Europe PMC DOI record did not expose a PMCID; retain as a candidate, not a d_A effect.")

    screen_row = {
        **candidate,
        "source": f"pmcid:{pmcid}",
    }
    screen: PMCScreen = screen_candidate(screen_row, fetch_xml=fetch_xml) if fetch_xml else screen_candidate(screen_row)
    return TrolliusProbe(
        **base,
        pmcid=pmcid,
        pmid=identifiers.get("pmid", ""),
        source_access_status=screen.source_access_status,
        search_status="search_recovered_pmcid",
        route_structure_signal=screen.route_structure_signal,
        direct_route_screen_status=screen.direct_route_screen_status,
        matched_trait_terms=screen.matched_trait_terms,
        matched_antagonist_terms=screen.matched_antagonist_terms,
        matched_section_titles=screen.matched_section_titles,
        matched_table_labels=screen.matched_table_labels,
        screen_note=screen.screen_note,
    )


def write_outputs(out_dir: str | Path, rows: Iterable[TrolliusProbe]) -> dict[str, object]:
    rows = list(rows)
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    with (destination / "d_a_trollius_pmc_probe.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=PROBE_FIELDS)
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)
    report = {
        "candidate_count": len(rows),
        "pmc_fulltext_recovered": sum(row.source_access_status == "fulltext_xml_recovered" for row in rows),
        "candidate_direct_route_structure": sum(row.route_structure_signal == "candidate_A_to_H_experiment_structure_needs_numeric_context_check" for row in rows),
        "no_antagonism_term_family": sum(row.route_structure_signal == "one_term_family_present" and not row.matched_antagonist_terms for row in rows),
        "decision_boundary": DO_NOT_INFER,
    }
    (destination / "d_a_trollius_pmc_probe_report.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def probe_scouting_file(
    scouting_csv: str | Path,
    out_dir: str | Path,
    *,
    fetch_json: Callable[[str], tuple[int, Any]] = _fetch_json,
    fetch_xml: Callable[[str], tuple[int, bytes]] | None = None,
) -> dict[str, object]:
    return write_outputs(out_dir, [probe_trollius(_candidate_row(scouting_csv), fetch_json=fetch_json, fetch_xml=fetch_xml)])
