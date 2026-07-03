"""Summarize direct-route coding for the retrieval-depth audit.

This consumes the frozen head/tail packet after human source coding. It compares
direct-route yield between rank strata *within the same metadata screen group*.
The result diagnoses retrieval-depth usefulness; it is not an effect synthesis or
a literature-stopping rule.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

from trait_architecture.priority_leak_audit_adjudication import check_sheet


GROUPS = ("priority", "biological_nonpriority")
SUMMARY_FIELDS = (
    "route_family_audit",
    "audit_group",
    "depth_stratum",
    "screen_group",
    "sampled_rows",
    "route_screenable_rows",
    "direct_route_present_rows",
    "direct_route_absent_rows",
    "unassessed_rows",
    "completion_fraction",
    "direct_route_yield",
)
COMPARISON_FIELDS = (
    "route_family_audit",
    "screen_group",
    "head_screenable_rows",
    "head_direct_route_present_rows",
    "head_direct_route_yield",
    "tail_screenable_rows",
    "tail_direct_route_present_rows",
    "tail_direct_route_yield",
    "tail_minus_head_yield",
    "comparison_status",
)
BOUNDARY = (
    "This head-versus-tail source-screening audit does not establish effect direction, "
    "effect size, causal design, quantitative eligibility, corpus-wide prevalence, or "
    "a stopping rule for the literature search."
)


def _text(value: object) -> str:
    return str(value or "").strip()


def _group_parts(audit_group: str) -> tuple[str, str]:
    value = _text(audit_group)
    for stratum in ("head", "tail"):
        prefix = f"{stratum}_"
        if value.startswith(prefix):
            group = value[len(prefix):]
            if group in GROUPS:
                return stratum, group
    raise ValueError(f"invalid depth audit_group: {audit_group!r}")


def _decimal(numerator: int, denominator: int) -> str:
    return "" if not denominator else f"{numerator / denominator:.6f}"


def summarize_depth_audit(rows: Iterable[dict[str, str]]) -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, object]]:
    rows = list(rows)
    check_sheet(rows)
    counts: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    for row in rows:
        stratum, group = _group_parts(row["audit_group"])
        route = _text(row.get("route_family_audit"))
        key = (route, row["audit_group"])
        counts[key]["sampled_rows"] += 1
        counts[key][row["route_screen_status"]] += 1

    summary: list[dict[str, str]] = []
    for (route, audit_group), count in sorted(counts.items()):
        stratum, group = _group_parts(audit_group)
        screenable = count["direct_route_present"] + count["direct_route_absent"]
        present = count["direct_route_present"]
        summary.append({
            "route_family_audit": route,
            "audit_group": audit_group,
            "depth_stratum": stratum,
            "screen_group": group,
            "sampled_rows": str(count["sampled_rows"]),
            "route_screenable_rows": str(screenable),
            "direct_route_present_rows": str(present),
            "direct_route_absent_rows": str(count["direct_route_absent"]),
            "unassessed_rows": str(count["unassessed"]),
            "completion_fraction": _decimal(screenable, count["sampled_rows"]),
            "direct_route_yield": _decimal(present, screenable),
        })

    lookup = {(row["route_family_audit"], row["depth_stratum"], row["screen_group"]): row for row in summary}
    comparisons: list[dict[str, str]] = []
    routes = sorted({route for route, _ in counts})
    for route in routes:
        for group in GROUPS:
            head = lookup.get((route, "head", group))
            tail = lookup.get((route, "tail", group))
            head_n = int(head["route_screenable_rows"]) if head else 0
            tail_n = int(tail["route_screenable_rows"]) if tail else 0
            head_present = int(head["direct_route_present_rows"]) if head else 0
            tail_present = int(tail["direct_route_present_rows"]) if tail else 0
            head_yield = head_present / head_n if head_n else None
            tail_yield = tail_present / tail_n if tail_n else None
            comparisons.append({
                "route_family_audit": route,
                "screen_group": group,
                "head_screenable_rows": str(head_n),
                "head_direct_route_present_rows": str(head_present),
                "head_direct_route_yield": "" if head_yield is None else f"{head_yield:.6f}",
                "tail_screenable_rows": str(tail_n),
                "tail_direct_route_present_rows": str(tail_present),
                "tail_direct_route_yield": "" if tail_yield is None else f"{tail_yield:.6f}",
                "tail_minus_head_yield": "" if head_yield is None or tail_yield is None else f"{tail_yield - head_yield:.6f}",
                "comparison_status": "comparable_screened_strata" if head_n and tail_n else "insufficient_screened_rows",
            })

    diagnostics = {
        "sampled_row_count": len(rows),
        "overall_route_screen_status_counts": dict(sorted(Counter(row["route_screen_status"] for row in rows).items())),
        "interpretation_boundary": BOUNDARY,
    }
    return summary, comparisons, diagnostics


def write_depth_audit_summary(
    out_dir: str | Path,
    summary: Iterable[dict[str, str]],
    comparisons: Iterable[dict[str, str]],
    diagnostics: dict[str, object],
) -> None:
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    for filename, fields, rows in (
        ("depth_saturation_audit_yield_by_route_group.csv", SUMMARY_FIELDS, summary),
        ("depth_saturation_audit_head_tail_comparisons.csv", COMPARISON_FIELDS, comparisons),
    ):
        with (destination / filename).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
    (destination / "depth_saturation_audit_coding_diagnostics.json").write_text(
        json.dumps(diagnostics, indent=2, sort_keys=True), encoding="utf-8"
    )
