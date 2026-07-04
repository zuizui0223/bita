"""Bounded abstract screen for the fixed Phlox d_A candidate.

Ruane, Rotzin & Congleton 2014 (DOI 10.1093/aob/mcu007) is a `d_A` candidate only
if an accessible abstract/full-text route establishes floral display as a predictor
of florivory. This module checks a narrower alternative: whether fruit set is the
regression response while display size and florivorous beetle density are parallel
predictors. It first tries the publisher abstract and falls back to PubMed's public
abstract XML when the publisher blocks automated access. It writes structural
presence/absence signals only, never article prose, numerical results, or effect
rows.
"""

from __future__ import annotations

import csv
import html
import json
import re
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Iterable
from urllib.parse import quote
from urllib.request import Request, urlopen

PHLOX_DOI = "10.1093/aob/mcu007"
PUBLISHER_URL = "https://academic.oup.com/aob/article/113/5/887/160290"
PUBMED_ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&term="
PUBMED_EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id="
USER_AGENT = "bita d-a-phlox-abstract-screen/0.2"
MAX_HTML_BYTES = 2 * 1024 * 1024
MAX_XML_BYTES = 2 * 1024 * 1024
RESPONSE_TERMS = ("fruit set", "percentage fruit set")
DISPLAY_TERMS = ("floral display size", "display size")
FLORIVORY_TERMS = ("florivorous beetle density", "florivory", "florivorous beetle")
REGRESSION_TERMS = ("multiple linear regressions", "regression")
FIELDS = (
    "candidate_id", "doi", "pubmed_id", "abstract_access_status", "abstract_retrieval_route", "abstract_bytes",
    "response_terms", "display_predictor_terms", "florivory_predictor_terms",
    "regression_terms", "direct_display_to_florivory_model_signal", "route_assignment",
    "screen_note", "do_not_infer",
)
DO_NOT_INFER = (
    "Abstract structure screen only. Do not infer a direct display-to-florivory effect, effect direction, "
    "effect size, denominator, experimental unit, uncertainty, or B2 eligibility."
)


@dataclass(frozen=True)
class PhloxAbstractScreen:
    candidate_id: str
    doi: str
    pubmed_id: str
    abstract_access_status: str
    abstract_retrieval_route: str
    abstract_bytes: str
    response_terms: str
    display_predictor_terms: str
    florivory_predictor_terms: str
    regression_terms: str
    direct_display_to_florivory_model_signal: str
    route_assignment: str
    screen_note: str
    do_not_infer: str = DO_NOT_INFER


def _text(value: object) -> str:
    return str(value or "").strip()


def _matched(text: str, terms: Iterable[str]) -> list[str]:
    folded = text.casefold()
    return [term for term in terms if term in folded]


def _plain_html(page: str) -> str:
    decoded = html.unescape(page)
    without_scripts = re.sub(r"<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>", " ", decoded, flags=re.I | re.S)
    return " ".join(re.sub(r"<[^>]+>", " ", without_scripts).split())


def _fetch_html(url: str) -> tuple[int, str]:
    request = Request(url, headers={"Accept": "text/html,application/xhtml+xml", "User-Agent": USER_AGENT})
    with urlopen(request, timeout=60) as response:  # nosec B310: fixed publisher abstract route
        status = int(getattr(response, "status", response.getcode()))
        payload = response.read(MAX_HTML_BYTES + 1)
    if len(payload) > MAX_HTML_BYTES:
        raise ValueError("publisher abstract response exceeds 2 MiB cap")
    return status, payload.decode("utf-8", errors="replace")


def _fetch_json(url: str) -> tuple[int, Any]:
    request = Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    with urlopen(request, timeout=60) as response:  # nosec B310: fixed public PubMed DOI lookup
        status = int(getattr(response, "status", response.getcode()))
        return status, json.loads(response.read().decode("utf-8"))


def _fetch_xml(url: str) -> tuple[int, bytes]:
    request = Request(url, headers={"Accept": "application/xml,text/xml,*/*", "User-Agent": USER_AGENT})
    with urlopen(request, timeout=60) as response:  # nosec B310: exact public PubMed abstract route
        status = int(getattr(response, "status", response.getcode()))
        payload = response.read(MAX_XML_BYTES + 1)
    if len(payload) > MAX_XML_BYTES:
        raise ValueError("PubMed XML response exceeds 2 MiB cap")
    return status, payload


def _candidate(scouting_csv: str | Path) -> dict[str, str]:
    with Path(scouting_csv).open(encoding="utf-8", newline="") as handle:
        rows = [{key: _text(value) for key, value in row.items()} for row in csv.DictReader(handle)]
    matches = [row for row in rows if _text(row.get("candidate_id")) == "dA_cand_phlox_hirsuta"]
    if len(matches) != 1:
        raise ValueError("expected exactly one registered Phlox d_A candidate")
    return matches[0]


def _pubmed_id(payload: Any) -> str:
    if not isinstance(payload, dict):
        return ""
    result = payload.get("esearchresult")
    identifiers = result.get("idlist") if isinstance(result, dict) else []
    return _text(identifiers[0]) if isinstance(identifiers, list) and identifiers else ""


def _pubmed_abstract(xml: bytes) -> str:
    root = ET.fromstring(xml)
    return " ".join(" ".join("".join(node.itertext()).split()) for node in root.findall(".//Abstract/AbstractText")).strip()


def _assign(candidate_id: str, *, source_text: str, access: str, route: str, source_bytes: int, pubmed_id: str, retrieval_note: str = "") -> PhloxAbstractScreen:
    response = _matched(source_text, RESPONSE_TERMS)
    display = _matched(source_text, DISPLAY_TERMS)
    florivory = _matched(source_text, FLORIVORY_TERMS)
    regression = _matched(source_text, REGRESSION_TERMS)
    if response and display and florivory and regression:
        signal = "parallel_predictors_of_fruit_set_not_direct_d_A"
        assignment = "candidate_screened_context_only"
        note = "Accessible abstract identifies fruit set as the regression response and lists floral display size and florivorous beetle density among assessed factors; no display-to-florivory response model is established."
    elif display and florivory:
        signal = "display_and_florivory_terms_without_model_structure"
        assignment = "retain_unverified_candidate"
        note = "Accessible abstract contains display and florivory terms but does not expose the response-model structure needed to rule in or rule out d_A."
    else:
        signal = "insufficient_abstract_terms"
        assignment = "retain_unverified_candidate"
        note = "Accessible abstract did not expose both display and florivory terms."
    if retrieval_note:
        note = f"{note} {retrieval_note}"
    return PhloxAbstractScreen(candidate_id, PHLOX_DOI, pubmed_id, access, route, str(source_bytes), ";".join(response), ";".join(display), ";".join(florivory), ";".join(regression), signal, assignment, note)


def _pubmed_fallback(candidate_id: str, *, publisher_note: str, fetch_json: Callable[[str], tuple[int, Any]], fetch_xml: Callable[[str], tuple[int, bytes]]) -> PhloxAbstractScreen:
    try:
        status, payload = fetch_json(PUBMED_ESEARCH + quote(f"{PHLOX_DOI}[doi]", safe=""))
        pubmed_id = _pubmed_id(payload) if status < 400 else ""
        if not pubmed_id:
            raise RuntimeError(f"PubMed DOI lookup failed or returned no PMID (HTTP {status})")
        status, xml = fetch_xml(PUBMED_EFETCH + quote(pubmed_id))
        if status >= 400:
            raise RuntimeError(f"PubMed abstract fetch HTTP {status}")
        abstract = _pubmed_abstract(xml)
        if not abstract:
            raise RuntimeError("PubMed XML contains no abstract text")
    except Exception as error:
        return PhloxAbstractScreen(candidate_id, PHLOX_DOI, "", "abstract_routes_exhausted", "", "", "", "", "", "", "not_screened", "retain_unverified_candidate", f"{publisher_note}; PubMed fallback failed: {type(error).__name__}: {error}")
    return _assign(candidate_id, source_text=abstract, access="pubmed_abstract_recovered", route="pubmed_esearch_then_efetch", source_bytes=len(xml), pubmed_id=pubmed_id, retrieval_note=publisher_note)


def screen_candidate(candidate: dict[str, str], *, fetch_html: Callable[[str], tuple[int, str]] = _fetch_html, fetch_json: Callable[[str], tuple[int, Any]] = _fetch_json, fetch_xml: Callable[[str], tuple[int, bytes]] = _fetch_xml) -> PhloxAbstractScreen:
    candidate_id = _text(candidate.get("candidate_id"))
    try:
        status, page = fetch_html(PUBLISHER_URL)
        if status >= 400 or not page:
            raise RuntimeError(f"publisher HTTP {status}")
        return _assign(candidate_id, source_text=_plain_html(page), access="publisher_abstract_recovered", route="publisher_abstract_html", source_bytes=len(page.encode("utf-8")), pubmed_id="")
    except Exception as error:
        return _pubmed_fallback(candidate_id, publisher_note=f"Publisher abstract unavailable: {type(error).__name__}: {error}", fetch_json=fetch_json, fetch_xml=fetch_xml)


def write_outputs(out_dir: str | Path, rows: Iterable[PhloxAbstractScreen]) -> dict[str, object]:
    rows = list(rows)
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    with (destination / "d_a_phlox_abstract_screen.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)
    report = {"candidate_count": len(rows), "abstract_recovered": sum(row.abstract_access_status in {"publisher_abstract_recovered", "pubmed_abstract_recovered"} for row in rows), "parallel_fruit_set_predictor_structure": sum(row.direct_display_to_florivory_model_signal == "parallel_predictors_of_fruit_set_not_direct_d_A" for row in rows), "decision_boundary": DO_NOT_INFER}
    (destination / "d_a_phlox_abstract_screen_report.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def screen_scouting_file(scouting_csv: str | Path, out_dir: str | Path, *, fetch_html: Callable[[str], tuple[int, str]] = _fetch_html, fetch_json: Callable[[str], tuple[int, Any]] = _fetch_json, fetch_xml: Callable[[str], tuple[int, bytes]] = _fetch_xml) -> dict[str, object]:
    return write_outputs(out_dir, [screen_candidate(_candidate(scouting_csv), fetch_html=fetch_html, fetch_json=fetch_json, fetch_xml=fetch_xml)])
