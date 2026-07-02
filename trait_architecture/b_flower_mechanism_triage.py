"""Mechanism-aware fixed-corpus triage for B-flower full-text screening.

The floral-trait--animal-response queue is deliberately high recall. This module
never decides study inclusion. It ranks B-flower candidates for reading order
while preserving a census of the sparse B->floral-antagonist route.

Batch 1 contains:

* every B_to_antagonist candidate (census; currently 32); and
* up to 24 additional B_to_pollinator candidates not already in that census,
  ranked by flower-specific barrier/deterrence mechanism and animal-response
  evidence in the fixed abstract.

The output remains a full-text screening packet. Scores are not evidence grades,
effect sizes, or model parameters.
"""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path
from typing import Iterable, Mapping


B_ROUTE_ANTAGONIST = "B_to_antagonist"
B_ROUTE_POLLINATOR = "B_to_pollinator"
B_ROUTES = (B_ROUTE_ANTAGONIST, B_ROUTE_POLLINATOR)
DEFAULT_B_POLLINATOR_TOPUP = 24

MECHANISM_PATTERNS = {
    "nectar_secondary_metabolites": re.compile(
        r"(?:nectar.{0,90}(?:alkaloid|nicotine|caffeine|cardenolide|toxic|toxicity|toxin|secondary metabolite|amino acid|phenolic)|"
        r"(?:alkaloid|nicotine|caffeine|cardenolide|toxic|toxicity|toxin|secondary metabolite|amino acid|phenolic).{0,90}nectar)",
        re.IGNORECASE,
    ),
    "floral_chemical_deterrence": re.compile(
        r"(?:floral|flower|petal|corolla|inflorescence|pollen).{0,100}(?:chemical|volatile|scent|odou?r|deterren\w*|repellen\w*|defen[cs]e|toxic|alkaloid|nicotine|caffeine)|"
        r"(?:deterren\w*|repellen\w*|defen[cs]e|toxic|alkaloid|nicotine|caffeine).{0,100}(?:floral|flower|petal|corolla|inflorescence|pollen)",
        re.IGNORECASE,
    ),
    "physical_access_barrier": re.compile(
        r"(?:floral|flower|inflorescence|petal|corolla|nectar).{0,80}(?:trichome|sticky|slippery|spine|bract|barrier|closure|closing|closed|trap)|"
        r"(?:trichome|sticky|slippery|spine|bract|barrier|closure|closing|closed|trap).{0,80}(?:floral|flower|inflorescence|petal|corolla|nectar)",
        re.IGNORECASE,
    ),
    "direct_defence_or_access_language": re.compile(
        r"\b(?:defen[cs]e|defensive|deterren\w*|repellen\w*|anti[- ]?herbivor\w*|anti[- ]?florivor\w*|"
        r"nectar[- ]?thiev\w*|nectar robb\w*|robbery|cheater|access restriction|avoidance)\b",
        re.IGNORECASE,
    ),
}
OUTCOME_PATTERNS = {
    "floral_antagonist_response": re.compile(
        r"\b(?:florivor\w*|floral damage|herbivor\w*|nectar robb\w*|nectar thiev\w*|predat\w*|"
        r"floral antagonist|attack|flower damage|consumer)\b",
        re.IGNORECASE,
    ),
    "pollinator_response": re.compile(
        r"\b(?:pollinat\w*|visitation|visit\w*|forag\w*|bumblebee|bee|hawkmoth|moth|butterfly|"
        r"flower visitor|nectar removal|pollen removal|pollen deposition)\b",
        re.IGNORECASE,
    ),
}
FALSE_POSITIVE_PATTERNS = {
    "reproductive_isolation_or_compatibility": re.compile(
        r"\b(?:reproductive isolation|post-pollination|pre[- ]?zygotic|hybridization|hybrid zone|"
        r"self[- ]?incompatib\w*|cytotype|speciation|cytological isolation)\b",
        re.IGNORECASE,
    ),
    "molecular_or_biosynthesis_without_response_risk": re.compile(
        r"\b(?:rna[- ]?seq|transcriptom\w*|genomic\w*|gene expression|biosynthesis)\b",
        re.IGNORECASE,
    ),
    "generic_pollination_context_risk": re.compile(
        r"\b(?:pollination ecology|pollination network|pollination syndrome|trait matching)\b",
        re.IGNORECASE,
    ),
}

QUEUE_REQUIRED = {
    "candidate_id", "doi", "title", "publication_year", "work_type", "container_title", "publisher",
    "source_queries", "route_families", "source_bucket", "route_memberships", "screening_priority",
    "cue_experimental", "cue_choice", "cue_association", "cue_effect_statistics",
    "crossref_abstract_text",
}
TRIAGE_FIELDS = (
    "candidate_id", "doi", "title", "publication_year", "work_type", "container_title", "publisher",
    "route_memberships", "source_bucket", "screening_priority", "mechanism_tags", "outcome_tags",
    "false_positive_risk_tags", "mechanism_score", "design_signal_score", "outcome_score", "risk_penalty",
    "priority_score", "selection_lane", "selection_reason", "source_queries", "route_families",
    "cue_experimental", "cue_choice", "cue_association", "cue_effect_statistics", "crossref_abstract_text",
    "triage_warning",
)
SCREENING_FIELDS = TRIAGE_FIELDS + (
    "full_text_access", "full_text_b_flower_plausible", "full_text_b_mechanism", "full_text_animal_response",
    "full_text_design", "full_text_effect_recoverable", "full_text_include", "full_text_exclusion_reason",
    "source_locator", "screened_by", "screening_note",
)
SUMMARY_FIELDS = (
    "metric", "value", "interpretation_boundary",
)


class BFlowerTriageError(ValueError):
    """Raised when the fixed candidate queue lacks the triage contract."""


def _text(value: object) -> str:
    return str(value or "").strip()


def _truth(value: object) -> bool:
    return _text(value).lower() in {"true", "yes", "1", "y"}


def read_queue(path: str | Path) -> list[dict[str, str]]:
    location = Path(path)
    with location.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = QUEUE_REQUIRED.difference(reader.fieldnames or [])
        if missing:
            raise BFlowerTriageError(f"{location} missing required columns: {', '.join(sorted(missing))}")
        rows = [{key: _text(value) for key, value in row.items()} for row in reader]
    identifiers = [row["candidate_id"] for row in rows]
    if len(identifiers) != len(set(identifiers)):
        raise BFlowerTriageError("candidate queue requires unique candidate_id values")
    return rows


def _tags(text: str, patterns: Mapping[str, re.Pattern[str]]) -> list[str]:
    return [name for name, pattern in patterns.items() if pattern.search(text)]


def _route_set(row: Mapping[str, str]) -> set[str]:
    return set(filter(None, _text(row.get("route_memberships")).split(";")))


def _score(row: Mapping[str, str], mechanisms: list[str], outcomes: list[str], risks: list[str]) -> tuple[int, int, int, int, list[str]]:
    mechanism_score = 0
    if "nectar_secondary_metabolites" in mechanisms:
        mechanism_score += 5
    if "floral_chemical_deterrence" in mechanisms:
        mechanism_score += 4
    if "physical_access_barrier" in mechanisms:
        mechanism_score += 4
    if "direct_defence_or_access_language" in mechanisms:
        mechanism_score += 3

    outcome_score = 2 * len(outcomes)
    design_score = 0
    if _text(row.get("source_bucket")) == "empirical_nonreview":
        design_score += 2
    if _truth(row.get("cue_experimental")):
        design_score += 2
    if _truth(row.get("cue_choice")):
        design_score += 2
    if _truth(row.get("cue_association")):
        design_score += 1
    if _truth(row.get("cue_effect_statistics")):
        design_score += 2

    risk_penalty = 3 * len(risks)
    reasons = []
    if mechanisms:
        reasons.append("mechanism=" + ";".join(mechanisms))
    if outcomes:
        reasons.append("outcomes=" + ";".join(outcomes))
    if design_score:
        reasons.append("design_or_statistic_signal")
    if risks:
        reasons.append("manual_false_positive_check=" + ";".join(risks))
    return mechanism_score, design_score, outcome_score, risk_penalty, reasons


def build_b_triage(
    candidate_queue: Iterable[Mapping[str, str]], *, b_pollinator_topup: int = DEFAULT_B_POLLINATOR_TOPUP,
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    """Rank all B-route candidates and select the first full-text batch.

    B->antagonist is always censused. B->pollinator gets an additional
    mechanism-aware top-up selected after the antagonist census is retained.
    The score only ranks reading order and does not determine eventual inclusion.
    """
    if b_pollinator_topup < 1:
        raise BFlowerTriageError("b_pollinator_topup must be positive")
    rows = []
    for source in candidate_queue:
        routes = _route_set(source)
        if not routes.intersection(B_ROUTES):
            continue
        content = (_text(source.get("title")) + " " + _text(source.get("crossref_abstract_text"))).lower()
        mechanisms = _tags(content, MECHANISM_PATTERNS)
        outcomes = _tags(content, OUTCOME_PATTERNS)
        risks = _tags(content, FALSE_POSITIVE_PATTERNS)
        mechanism_score, design_score, outcome_score, risk_penalty, reasons = _score(source, mechanisms, outcomes, risks)
        priority_score = mechanism_score + design_score + outcome_score - risk_penalty
        row = {
            "candidate_id": _text(source.get("candidate_id")), "doi": _text(source.get("doi")),
            "title": _text(source.get("title")), "publication_year": _text(source.get("publication_year")),
            "work_type": _text(source.get("work_type")), "container_title": _text(source.get("container_title")),
            "publisher": _text(source.get("publisher")), "route_memberships": ";".join(sorted(routes)),
            "source_bucket": _text(source.get("source_bucket")), "screening_priority": _text(source.get("screening_priority")),
            "mechanism_tags": ";".join(mechanisms), "outcome_tags": ";".join(outcomes),
            "false_positive_risk_tags": ";".join(risks), "mechanism_score": str(mechanism_score),
            "design_signal_score": str(design_score), "outcome_score": str(outcome_score), "risk_penalty": str(risk_penalty),
            "priority_score": str(priority_score), "selection_lane": "not_batch_1", "selection_reason": ";".join(reasons),
            "source_queries": _text(source.get("source_queries")), "route_families": _text(source.get("route_families")),
            "cue_experimental": _text(source.get("cue_experimental")), "cue_choice": _text(source.get("cue_choice")),
            "cue_association": _text(source.get("cue_association")), "cue_effect_statistics": _text(source.get("cue_effect_statistics")),
            "crossref_abstract_text": _text(source.get("crossref_abstract_text")),
            "triage_warning": "Mechanism-aware abstract score ranks full-text reading order only; it is not a biological evidence grade or inclusion decision.",
        }
        rows.append(row)

    by_id = {row["candidate_id"]: row for row in rows}
    antagonist_census = sorted(
        [row for row in rows if B_ROUTE_ANTAGONIST in set(row["route_memberships"].split(";"))],
        key=lambda row: (-int(row["priority_score"]), row["candidate_id"]),
    )
    selected = {row["candidate_id"] for row in antagonist_census}
    for row in antagonist_census:
        row["selection_lane"] = "B_to_antagonist_census"
        row["selection_reason"] = (row["selection_reason"] + ";" if row["selection_reason"] else "") + "all B_to_antagonist candidates are censused"

    pollinator_pool = [
        row for row in rows
        if B_ROUTE_POLLINATOR in set(row["route_memberships"].split(";")) and row["candidate_id"] not in selected
    ]
    pollinator_topup = sorted(
        pollinator_pool,
        key=lambda row: (-int(row["priority_score"]), row["candidate_id"]),
    )[:b_pollinator_topup]
    for row in pollinator_topup:
        row["selection_lane"] = "B_to_pollinator_mechanism_topup"
        row["selection_reason"] = (row["selection_reason"] + ";" if row["selection_reason"] else "") + "top-ranked non-census B_to_pollinator candidate"
        selected.add(row["candidate_id"])

    triage = sorted(rows, key=lambda row: (row["selection_lane"] == "not_batch_1", -int(row["priority_score"]), row["candidate_id"]))
    batch = [row for row in triage if row["candidate_id"] in selected]
    screening = [{
        **row,
        "full_text_access": "unreviewed", "full_text_b_flower_plausible": "", "full_text_b_mechanism": "",
        "full_text_animal_response": "", "full_text_design": "", "full_text_effect_recoverable": "",
        "full_text_include": "pending_full_text", "full_text_exclusion_reason": "", "source_locator": "",
        "screened_by": "", "screening_note": "",
    } for row in batch]
    return triage, batch, screening


def summarize_b_triage(triage: Iterable[Mapping[str, str]], batch: Iterable[Mapping[str, str]]) -> list[dict[str, str]]:
    triage, batch = list(triage), list(batch)
    lane_counts = Counter(row["selection_lane"] for row in triage)
    mechanism_counts = Counter(tag for row in triage for tag in filter(None, row["mechanism_tags"].split(";")))
    return [
        {
            "metric": "B_route_candidates", "value": str(len(triage)),
            "interpretation_boundary": "Fixed-corpus B-route abstract candidates; not full-text included studies.",
        },
        {
            "metric": "B_batch_1_unique_candidates", "value": str(len(batch)),
            "interpretation_boundary": "Batch 1 reading packet: B_to_antagonist census plus B_to_pollinator mechanism-aware top-up.",
        },
        {
            "metric": "B_to_antagonist_census", "value": str(lane_counts.get("B_to_antagonist_census", 0)),
            "interpretation_boundary": "All sparse B_to_antagonist abstract candidates are sent to full-text screening.",
        },
        {
            "metric": "B_to_pollinator_mechanism_topup", "value": str(lane_counts.get("B_to_pollinator_mechanism_topup", 0)),
            "interpretation_boundary": "Top-ranked B_to_pollinator candidates outside the B_to_antagonist census; rank is only reading order.",
        },
        *[
            {
                "metric": "mechanism_tag_" + tag, "value": str(count),
                "interpretation_boundary": "Abstract cue frequency in B-route candidates; not validated trait prevalence.",
            }
            for tag, count in sorted(mechanism_counts.items())
        ],
    ]


def _write_csv(path: Path, fields: Iterable[str], rows: Iterable[Mapping[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields))
        writer.writeheader()
        writer.writerows(rows)


def write_b_triage_packet(
    out_dir: str | Path,
    triage: list[dict[str, str]],
    batch: list[dict[str, str]],
    screening: list[dict[str, str]],
) -> None:
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    _write_csv(destination / "b_flower_mechanism_triage_all.csv", TRIAGE_FIELDS, triage)
    _write_csv(destination / "b_flower_full_text_batch_1.csv", TRIAGE_FIELDS, batch)
    _write_csv(destination / "b_flower_full_text_batch_1_screening_sheet.csv", SCREENING_FIELDS, screening)
    _write_csv(destination / "b_flower_mechanism_triage_summary.csv", SUMMARY_FIELDS, summarize_b_triage(triage, batch))
    (destination / "README.md").write_text(
        "# B-flower mechanism-aware screening packet\n\n"
        "Batch 1 censors no evidence: all B_to_antagonist candidates are included, and B_to_pollinator candidates are ranked for reading order using flower-specific mechanism and animal-response cues. "
        "Confirm every field from the full text before calling a record included or extracting an effect size.\n",
        encoding="utf-8",
    )
