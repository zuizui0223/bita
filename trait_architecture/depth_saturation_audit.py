"""Build a route-balanced head-versus-tail source-coding audit queue.

This audit follows the rank-binned depth diagnostic.  It asks whether the same
metadata screen finds direct-route studies near the beginning and near the end of
each existing Crossref query.  It never changes the query registry, inclusion
rules, or effect estimands.

The queue deliberately uses query-rank memberships rather than corpus-wide unique
records.  Within a route, a candidate already seen in the head stratum is excluded
from the tail stratum so the comparison does not reread the same study as both a
head and a tail result.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Iterable


PRIORITY = "priority_for_shallow_source_coding"
BIOLOGICAL_NONPRIORITY = "biological_context_needs_route_screen"
SCREEN_GROUPS = {
    PRIORITY: "priority",
    BIOLOGICAL_NONPRIORITY: "biological_nonpriority",
}
DEPTH_STRATA = ("head", "tail")
DEPTH_AUDIT_FIELDS = (
    "audit_group",
    "depth_stratum",
    "screen_group",
    "route_family_audit",
    "audit_rank",
    "query_id",
    "query_rank",
    "candidate_id",
    "doi",
    "title",
    "publication_year",
    "container_title",
    "landing_page_url",
    "source_queries",
    "route_families",
    "metadata_A_signal",
    "metadata_B_signal",
    "metadata_P_signal",
    "metadata_H_signal",
    "metadata_W_signal",
    "metadata_biology_context_term_count",
    "shallow_screen_status",
    "shallow_screen_reason",
    "depth_audit_warning",
)

BOUNDARY = (
    "This is a deterministic metadata-to-source-coding queue for testing retrieval "
    "depth. It does not establish direct-route measurement, effect direction, effect "
    "size, causal design, quantitative eligibility, or corpus-wide prevalence."
)


def _text(value: object) -> str:
    return str(value or "").strip()


def _rank(value: object) -> int:
    try:
        rank = int(_text(value))
    except ValueError as error:
        raise ValueError(f"query_rank must be a positive integer, got {value!r}") from error
    if rank < 1:
        raise ValueError(f"query_rank must be a positive integer, got {value!r}")
    return rank


def _stable_rank(seed: str, candidate_id: str, route: str, stratum: str, group: str) -> str:
    return hashlib.sha256(
        f"{seed}|{candidate_id}|{route}|{stratum}|{group}".encode("utf-8")
    ).hexdigest()


def _stratum(rank: int, *, head_rank_max: int, tail_rank_min: int, tail_rank_max: int) -> str:
    if 1 <= rank <= head_rank_max:
        return "head"
    if tail_rank_min <= rank <= tail_rank_max:
        return "tail"
    return ""


def _representative(existing: dict[str, str] | None, incoming: dict[str, str]) -> dict[str, str]:
    """Keep the lowest-rank membership for one route/stratum/group/candidate cell."""

    if existing is None:
        return incoming
    existing_key = (_rank(existing["query_rank"]), _text(existing.get("query_id")))
    incoming_key = (_rank(incoming["query_rank"]), _text(incoming.get("query_id")))
    return incoming if incoming_key < existing_key else existing


def read_rank_memberships(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = [{key: _text(value) for key, value in row.items()} for row in csv.DictReader(handle)]
    required = {
        "query_id", "route_family", "query_rank", "candidate_id", "shallow_screen_status",
        "doi", "title", "publication_year", "container_title", "landing_page_url",
    }
    if rows and not required.issubset(rows[0]):
        raise ValueError("rank-membership file lacks required retrieval and screen columns")
    return rows


def build_depth_audit_sample(
    rows: Iterable[dict[str, str]],
    *,
    head_rank_max: int = 200,
    tail_rank_min: int = 1601,
    tail_rank_max: int = 2000,
    per_route_stratum_group: int = 15,
    seed: str = "depth-saturation-audit-v1",
) -> tuple[list[dict[str, str]], dict[str, object]]:
    """Select a route-balanced head/tail audit sample from rank memberships.

    Both screen groups are sampled separately in both rank strata.  Candidate
    duplicates within a route/stratum/group retain their lowest-ranked query
    membership.  Any candidate present in the head stratum of a route is removed
    from that route's tail cells, preserving non-overlapping comparison samples.
    """

    if head_rank_max < 1:
        raise ValueError("head_rank_max must be positive")
    if tail_rank_min <= head_rank_max or tail_rank_max < tail_rank_min:
        raise ValueError("tail ranks must begin after the head stratum and be ordered")
    if per_route_stratum_group < 1:
        raise ValueError("per_route_stratum_group must be positive")

    rows = list(rows)
    routes = sorted({_text(row.get("route_family")) for row in rows if _text(row.get("route_family"))})
    cells: dict[tuple[str, str, str], dict[str, dict[str, str]]] = defaultdict(dict)
    head_seen: dict[str, set[str]] = defaultdict(set)
    pre_tail_overlap: dict[str, set[str]] = defaultdict(set)

    # First pass determines all candidates seen in each route's head band.
    for row in rows:
        route = _text(row.get("route_family"))
        candidate_id = _text(row.get("candidate_id"))
        status = _text(row.get("shallow_screen_status"))
        if not route or not candidate_id or status not in SCREEN_GROUPS:
            continue
        rank = _rank(row.get("query_rank"))
        if _stratum(
            rank,
            head_rank_max=head_rank_max,
            tail_rank_min=tail_rank_min,
            tail_rank_max=tail_rank_max,
        ) == "head":
            head_seen[route].add(candidate_id)

    # Second pass creates the four route × stratum × screen-group cells.
    for row in rows:
        route = _text(row.get("route_family"))
        candidate_id = _text(row.get("candidate_id"))
        status = _text(row.get("shallow_screen_status"))
        if not route or not candidate_id or status not in SCREEN_GROUPS:
            continue
        rank = _rank(row.get("query_rank"))
        stratum = _stratum(
            rank,
            head_rank_max=head_rank_max,
            tail_rank_min=tail_rank_min,
            tail_rank_max=tail_rank_max,
        )
        if not stratum:
            continue
        if stratum == "tail" and candidate_id in head_seen[route]:
            pre_tail_overlap[route].add(candidate_id)
            continue
        group = SCREEN_GROUPS[status]
        cell = (route, stratum, group)
        cells[cell][candidate_id] = _representative(cells[cell].get(candidate_id), row)

    output: list[dict[str, str]] = []
    availability: dict[str, dict[str, dict[str, int]]] = {
        route: {stratum: {group: 0 for group in SCREEN_GROUPS.values()} for stratum in DEPTH_STRATA}
        for route in routes
    }
    for route in routes:
        for stratum in DEPTH_STRATA:
            for group in SCREEN_GROUPS.values():
                cell = (route, stratum, group)
                candidates = list(cells[cell].values())
                candidates.sort(
                    key=lambda row: _stable_rank(seed, row["candidate_id"], route, stratum, group)
                )
                availability[route][stratum][group] = len(candidates)
                for audit_rank, row in enumerate(candidates[:per_route_stratum_group], start=1):
                    audit_group = f"{stratum}_{group}"
                    output.append({
                        "audit_group": audit_group,
                        "depth_stratum": stratum,
                        "screen_group": group,
                        "route_family_audit": route,
                        "audit_rank": str(audit_rank),
                        "query_id": _text(row.get("query_id")),
                        "query_rank": _text(row.get("query_rank")),
                        "candidate_id": _text(row.get("candidate_id")),
                        "doi": _text(row.get("doi")),
                        "title": _text(row.get("title")),
                        "publication_year": _text(row.get("publication_year")),
                        "container_title": _text(row.get("container_title")),
                        "landing_page_url": _text(row.get("landing_page_url")),
                        "source_queries": _text(row.get("source_queries")),
                        "route_families": _text(row.get("route_families")),
                        "metadata_A_signal": _text(row.get("metadata_A_signal")),
                        "metadata_B_signal": _text(row.get("metadata_B_signal")),
                        "metadata_P_signal": _text(row.get("metadata_P_signal")),
                        "metadata_H_signal": _text(row.get("metadata_H_signal")),
                        "metadata_W_signal": _text(row.get("metadata_W_signal")),
                        "metadata_biology_context_term_count": _text(row.get("metadata_biology_context_term_count")),
                        "shallow_screen_status": _text(row.get("shallow_screen_status")),
                        "shallow_screen_reason": _text(row.get("shallow_screen_reason")),
                        "depth_audit_warning": BOUNDARY,
                    })

    summary = {
        "seed": seed,
        "head_rank_max": head_rank_max,
        "tail_rank_min": tail_rank_min,
        "tail_rank_max": tail_rank_max,
        "per_route_stratum_group_requested": per_route_stratum_group,
        "route_families": routes,
        "availability_after_within_cell_deduplication": availability,
        "tail_candidates_excluded_due_to_head_overlap_by_route": {
            route: len(candidates) for route, candidates in sorted(pre_tail_overlap.items())
        },
        "sampled_row_count": len(output),
        "interpretation_boundary": BOUNDARY,
    }
    return output, summary


def write_depth_audit_outputs(
    membership_csv: str | Path,
    out_dir: str | Path,
    *,
    head_rank_max: int = 200,
    tail_rank_min: int = 1601,
    tail_rank_max: int = 2000,
    per_route_stratum_group: int = 15,
) -> dict[str, object]:
    rows = read_rank_memberships(membership_csv)
    sample, summary = build_depth_audit_sample(
        rows,
        head_rank_max=head_rank_max,
        tail_rank_min=tail_rank_min,
        tail_rank_max=tail_rank_max,
        per_route_stratum_group=per_route_stratum_group,
    )
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    with (destination / "depth_saturation_audit_queue.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=DEPTH_AUDIT_FIELDS)
        writer.writeheader()
        writer.writerows(sample)
    (destination / "depth_saturation_audit_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8"
    )
    return summary
