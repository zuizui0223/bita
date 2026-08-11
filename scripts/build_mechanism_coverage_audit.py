"""Build a reproducible coverage audit from committed mechanism ledgers.

This script counts independence clusters, not effect rows. It writes aggregate
coverage only and never interprets record counts as biological prevalence.
"""

from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from pathlib import Path

INPUTS = (
    "empirical/mechanism_pattern_synthesis/MASTER_LEDGER_V1.csv",
    "empirical/mechanism_pattern_synthesis/LEDGER_BATCH_2_V1.csv",
    "empirical/mechanism_pattern_synthesis/LEDGER_BATCH_3_V1.csv",
    "empirical/mechanism_pattern_synthesis/LEDGER_BATCH_4_V1.csv",
    "empirical/mechanism_pattern_synthesis/LEDGER_BATCH_5_V1.csv",
)
ROUTES = (
    "A_to_pollination",
    "A_to_antagonism",
    "D_to_antagonism",
    "D_to_pollination",
    "direct_AxD",
)
MARGINAL_ROUTES = set(ROUTES[:4])
FLAG_TOKENS = ("discrepancy", "unresolved", "pending", "blocked", "sensitivity")


def _text(value: object) -> str:
    return str(value or "").strip()


def _bool(value: object) -> bool:
    return _text(value).lower() == "true"


def _finite(value: object) -> bool:
    try:
        return math.isfinite(float(_text(value)))
    except (TypeError, ValueError):
        return False


def _read(path: str) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return [{key: _text(value) for key, value in row.items()} for row in csv.DictReader(handle)]


def _validate(rows: list[dict[str, str]]) -> dict[str, object]:
    ids = [_text(row.get("record_id")) for row in rows]
    duplicates = sorted({rid for rid in ids if rid and ids.count(rid) > 1})
    missing_ids = sum(not rid for rid in ids)
    missing_clusters = sum(not _text(row.get("independence_cluster")) for row in rows)
    unknown_routes = sorted({
        _text(row.get("route")) for row in rows
        if _text(row.get("route")) and _text(row.get("route")) not in ROUTES
    })
    if duplicates or missing_ids or missing_clusters or unknown_routes:
        raise ValueError(json.dumps({
            "duplicate_record_ids": duplicates,
            "missing_record_ids": missing_ids,
            "missing_independence_clusters": missing_clusters,
            "unknown_routes": unknown_routes,
        }, sort_keys=True))
    return {
        "record_count": len(rows),
        "unique_record_ids": len(set(ids)),
        "unique_clusters": len({_text(row["independence_cluster"]) for row in rows}),
    }


def _quality_flag(row: dict[str, str]) -> bool:
    text = " ".join((row.get("source_verification_state", ""), row.get("notes", ""))).lower()
    return any(token in text for token in FLAG_TOKENS)


def _route_state(rows: list[dict[str, str]], route: str) -> dict[str, object]:
    route_rows = [row for row in rows if row.get("route") == route]
    clusters = sorted({row["independence_cluster"] for row in route_rows})
    quantitative = sorted({
        row["independence_cluster"] for row in route_rows
        if _finite(row.get("effect_value")) and _finite(row.get("standard_error"))
    })
    primary_quantitative = sorted({
        row["independence_cluster"] for row in route_rows
        if _finite(row.get("effect_value")) and _finite(row.get("standard_error"))
        and _bool(row.get("is_primary_effect")) and not _quality_flag(row)
    })
    primary_any = sorted({
        row["independence_cluster"] for row in route_rows if _bool(row.get("is_primary_effect"))
    })
    flagged = sorted({row["independence_cluster"] for row in route_rows if _quality_flag(row)})
    tiers: dict[str, set[str]] = defaultdict(set)
    for row in route_rows:
        tiers[row.get("evidence_tier", "")].add(row["independence_cluster"])
    return {
        "record_count": len(route_rows),
        "cluster_count": len(clusters),
        "clusters": clusters,
        "primary_record_cluster_count": len(primary_any),
        "quantitative_cluster_count": len(quantitative),
        "quantitative_clusters": quantitative,
        "primary_quantitative_cluster_count": len(primary_quantitative),
        "primary_quantitative_clusters": primary_quantitative,
        "quality_flagged_cluster_count": len(flagged),
        "quality_flagged_clusters": flagged,
        "clusters_by_evidence_tier": {tier: len(value) for tier, value in sorted(tiers.items()) if tier},
    }


def _same_system(rows: list[dict[str, str]]) -> dict[str, object]:
    routes_by_cluster: dict[str, set[str]] = defaultdict(set)
    explicit: set[str] = set()
    for row in rows:
        cluster = row["independence_cluster"]
        route = row.get("route", "")
        if route in MARGINAL_ROUTES:
            routes_by_cluster[cluster].add(route)
        if _bool(row.get("is_same_system_multi_route")):
            explicit.add(cluster)
    inferred = {cluster for cluster, routes in routes_by_cluster.items() if len(routes) >= 2}
    combined = sorted(explicit | inferred)
    return {
        "cluster_count": len(combined),
        "clusters": combined,
        "explicit_cluster_count": len(explicit),
        "two_or_more_marginal_routes_cluster_count": len(inferred),
        "marginal_route_sets": {
            cluster: sorted(routes_by_cluster[cluster]) for cluster in combined if routes_by_cluster.get(cluster)
        },
    }


def _sign_switch(path: str) -> dict[str, object]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    clusters = sorted({_text(row.get("study_id")) for row in rows if _text(row.get("study_id"))})
    axes: dict[str, int] = defaultdict(int)
    for row in rows:
        axes[_text(row.get("contrast_axis"))] += 1
    return {
        "record_count": len(rows),
        "study_cluster_count": len(clusters),
        "clusters": clusters,
        "records_by_contrast_axis": dict(sorted(axes.items())),
    }


def _render(report: dict[str, object]) -> str:
    lines = [
        "# Mechanism-pattern coverage audit v1",
        "",
        "## Boundary",
        "",
        "This is an audit of the currently committed **source-adjudicated ledger**, not an estimate of mechanism prevalence in nature or a replacement for route-specific meta-analysis.",
        "",
        f"- source-adjudicated effect/directional records: **{report['validation']['record_count']}**",
        f"- independent biological study clusters in those ledgers: **{report['validation']['unique_clusters']}**",
        f"- same-system multi-route clusters: **{report['same_system_multi_route']['cluster_count']}**",
        f"- registered context/sign-switch records: **{report['sign_switch']['record_count']}** from **{report['sign_switch']['study_cluster_count']}** study clusters",
        "",
        "## Route coverage",
        "",
        "| Route | clusters | quantitative clusters | clean primary quantitative | quality-flagged clusters |",
        "|---|---:|---:|---:|---:|",
    ]
    for route in ROUTES:
        state = report["routes"][route]
        lines.append(
            f"| `{route}` | {state['cluster_count']} | {state['quantitative_cluster_count']} | "
            f"{state['primary_quantitative_cluster_count']} | {state['quality_flagged_cluster_count']} |"
        )
    lines += [
        "",
        "`quantitative` means a finite effect plus finite SE is present. `clean primary quantitative` further requires `is_primary_effect=true` and no explicit discrepancy/unresolved/pending/blocked/sensitivity flag.",
        "",
        "## Same-system mechanism architecture",
        "",
    ]
    same = report["same_system_multi_route"]
    for cluster in same["clusters"]:
        routes = same["marginal_route_sets"].get(cluster, [])
        lines.append(f"- `{cluster}`: {', '.join(routes) if routes else 'explicit same-system flag'}")
    lines += [
        "",
        "## Completion-gate implications",
        "",
        "### Gate B — four marginal mechanism families",
        "",
    ]
    all_covered = all(report["routes"][route]["cluster_count"] > 0 for route in MARGINAL_ROUTES)
    lines.append(f"Current ledger status: **{'covered' if all_covered else 'not yet covered'}**. All four routes have at least one source-adjudicated cluster." if all_covered else "At least one marginal route remains absent from the source-adjudicated ledger.")
    lines += [
        "",
        "This does not mean every route has a defensible pooled meta-analysis. Quantitative and directional states remain separated above.",
        "",
        "### Gate C — quantitative modules",
        "",
        "The ledger contains multiple quantitative clusters, but cluster count alone does not pass Gate C. PR #124 remains one independent antagonist-pressure meta-analysis module; a second route-level module still requires biologically compatible multi-study effects rather than a collection of incomparable coefficients.",
        "",
        "### Gate D — context dependence",
        "",
        f"The sign/threshold ledger now contains **{report['sign_switch']['record_count']}** registered within-study conditionality records. This gate is advancing, but formal moderator synthesis is still pending where sample size permits.",
        "",
        "### Gate E — same-system multi-route",
        "",
        f"There are **{same['cluster_count']}** source-adjudicated same-system clusters under the explicit/inferred rule. Gate E has empirical material, but the final guarded-attraction versus pollinator-interference summary is still pending.",
        "",
        "### Gates A, F, G",
        "",
        "Not passed by this audit. Direct A×D search saturation, strict joint-cost search saturation, and module-level bias/robustness analyses remain separate required tasks.",
        "",
        "## Claim guardrail",
        "",
        "No count in this file is a prevalence estimate. No marginal-route record is combined into `W_AD`, and same-system co-occurrence is not re-labelled as direct `A x D` evidence.",
        "",
    ]
    return "\n".join(lines)


def run(output_json: str | Path, output_md: str | Path) -> dict[str, object]:
    rows: list[dict[str, str]] = []
    counts_by_file: dict[str, int] = {}
    for path in INPUTS:
        batch = _read(path)
        counts_by_file[path] = len(batch)
        rows.extend(batch)
    validation = _validate(rows)
    report = {
        "input_files": list(INPUTS),
        "record_counts_by_file": counts_by_file,
        "validation": validation,
        "routes": {route: _route_state(rows, route) for route in ROUTES},
        "same_system_multi_route": _same_system(rows),
        "sign_switch": _sign_switch("empirical/mechanism_pattern_synthesis/SIGN_SWITCH_LEDGER_V1.csv"),
        "warning": "Coverage counts are evidence-architecture diagnostics only; they are not biological prevalence estimates or pooled effects.",
    }
    Path(output_json).parent.mkdir(parents=True, exist_ok=True)
    Path(output_json).write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    Path(output_md).write_text(_render(report), encoding="utf-8")
    return report


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("output_json")
    parser.add_argument("output_md")
    args = parser.parse_args()
    report = run(args.output_json, args.output_md)
    print(json.dumps({
        "records": report["validation"]["record_count"],
        "clusters": report["validation"]["unique_clusters"],
        "same_system": report["same_system_multi_route"]["cluster_count"],
    }, indent=2))
