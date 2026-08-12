from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EMP = ROOT / "empirical" / "mechanism_pattern_synthesis"

CANONICAL = [
    EMP / "MASTER_LEDGER_V1.csv",
    EMP / "LEDGER_BATCH_2_V1.csv",
    EMP / "LEDGER_BATCH_3_V1.csv",
    EMP / "LEDGER_BATCH_4_V1.csv",
    EMP / "LEDGER_BATCH_5_V1.csv",
]
EXPANSION = sorted(EMP.glob("EXPANSION_LEDGER_BATCH_*_V1.csv"))
CANONICAL_SWITCH = EMP / "SIGN_SWITCH_LEDGER_V1.csv"
EXPANSION_SWITCH = sorted(EMP.glob("EXPANSION_SIGN_SWITCH_BATCH_*_V1.csv"))
OUT_JSON = EMP / "PATTERN_EXPANSION_READOUT_V1.json"
OUT_MD = EMP / "PATTERN_EXPANSION_READOUT_V1.md"

ROUTES = ("A_to_pollination", "A_to_antagonism", "D_to_antagonism", "D_to_pollination")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def summarize(rows: list[dict[str, str]]) -> dict[str, object]:
    route_clusters: dict[str, set[str]] = defaultdict(set)
    routes_by_cluster: dict[str, set[str]] = defaultdict(set)
    all_clusters: set[str] = set()
    explicit_same_system: set[str] = set()
    records: set[str] = set()

    for row in rows:
        rid = row["record_id"]
        if rid in records:
            raise ValueError(f"duplicate record_id: {rid}")
        records.add(rid)
        cluster = row["independence_cluster"]
        all_clusters.add(cluster)
        route = row["route"]
        if route in ROUTES:
            route_clusters[route].add(cluster)
            routes_by_cluster[cluster].add(route)
        if row["is_same_system_multi_route"].strip().lower() == "true":
            explicit_same_system.add(cluster)

    inferred_same_system = {
        cluster for cluster, routes in routes_by_cluster.items() if len(routes) >= 2
    }
    same_system = explicit_same_system | inferred_same_system

    return {
        "records": len(records),
        "independent_clusters": len(all_clusters),
        "route_clusters": {route: len(route_clusters[route]) for route in ROUTES},
        "same_system_clusters": len(same_system),
    }


def switch_cluster_count(paths: list[Path]) -> int:
    studies: set[str] = set()
    for path in paths:
        for row in read_rows(path):
            studies.add(row["study_id"])
    return len(studies)


def main() -> None:
    if not EXPANSION:
        raise ValueError("No expansion ledgers found")
    canonical_rows = [row for path in CANONICAL for row in read_rows(path)]
    expansion_rows = [row for path in EXPANSION for row in read_rows(path)]
    combined_rows = canonical_rows + expansion_rows

    for row in expansion_rows:
        if row["is_direct_AxD"].strip().lower() == "true":
            raise ValueError(f"expansion record {row['record_id']} illegally marked direct A x D")
        if row["route"] not in ROUTES:
            raise ValueError(f"unexpected expansion route: {row['route']}")

    canonical = summarize(canonical_rows)
    expansion = summarize(expansion_rows)
    combined = summarize(combined_rows)
    context_switch_clusters = switch_cluster_count([CANONICAL_SWITCH, *EXPANSION_SWITCH])

    expected_canonical = {
        "records": 38,
        "independent_clusters": 14,
        "route_clusters": {
            "A_to_pollination": 4,
            "A_to_antagonism": 5,
            "D_to_antagonism": 10,
            "D_to_pollination": 7,
        },
        "same_system_clusters": 10,
    }
    if canonical != expected_canonical:
        raise ValueError(f"canonical evidence universe drifted: {canonical!r}")

    expected_expansion = {
        "records": 18,
        "independent_clusters": 11,
        "route_clusters": {
            "A_to_pollination": 1,
            "A_to_antagonism": 3,
            "D_to_antagonism": 8,
            "D_to_pollination": 3,
        },
        "same_system_clusters": 4,
    }
    if expansion != expected_expansion:
        raise ValueError(f"expansion counts unexpected: {expansion!r}")

    expected_combined = {
        "records": 56,
        "independent_clusters": 25,
        "route_clusters": {
            "A_to_pollination": 5,
            "A_to_antagonism": 8,
            "D_to_antagonism": 18,
            "D_to_pollination": 10,
        },
        "same_system_clusters": 14,
    }
    if combined != expected_combined:
        raise ValueError(f"provisional expansion counts unexpected: {combined!r}")
    if context_switch_clusters != 17:
        raise ValueError(f"expected 17 unique context-switch clusters, got {context_switch_clusters}")

    payload = {
        "status": "PROVISIONAL_EXPANSION_BRANCH_NOT_CANONICAL",
        "canonical": canonical,
        "expansion": expansion,
        "expansion_ledger_files": [p.name for p in EXPANSION],
        "combined_provisional": combined,
        "context_switch_clusters_provisional": context_switch_clusters,
        "context_programs_excluded_from_route_N": 7,
        "interpretation_boundary": [
            "counts are evidence-capacity / independent-system recurrence diagnostics",
            "counts are not prevalence estimates",
            "route counts overlap across study clusters and must not be summed",
            "environmental-context-only studies/programs and published meta-analysis module study counts are excluded from route-ledger N",
            "direct A x D and direct joint-cost canonical gaps are unchanged",
        ],
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    rc = combined["route_clusters"]
    lines = [
        "# Pattern expansion readout v1",
        "",
        "**Status: PROVISIONAL EXPANSION BRANCH — NOT CANONICAL MANUSCRIPT COUNTS.**",
        "",
        "This readout combines the frozen five-ledger canonical universe with six source-adjudicated expansion ledgers.",
        "",
        "```text",
        f"route-ledger records:             {combined['records']}  (canonical {canonical['records']})",
        f"independent biological clusters: {combined['independent_clusters']}  (canonical {canonical['independent_clusters']})",
        f"A -> pollination clusters:        {rc['A_to_pollination']}  (canonical 4)",
        f"A -> antagonism clusters:         {rc['A_to_antagonism']}  (canonical 5)",
        f"D -> antagonism clusters:         {rc['D_to_antagonism']}  (canonical 10)",
        f"D -> pollination clusters:        {rc['D_to_pollination']}  (canonical 7)",
        f"same-system multi-route clusters: {combined['same_system_clusters']}  (canonical 10)",
        f"context/sign-switch clusters:      {context_switch_clusters}  (canonical 11)",
        "```",
        "",
        "The expansion currently adds eleven independent route-ledger systems:",
        "",
        "- *Pedicularis rex*: water-filled floral barrier; seed-predator protection, pollinator null, nectar-robber null.",
        "- *Dalechampia scandens*: visual bract attraction axis tracked by both pollinators and seed predators.",
        "- *Raphanus sativus*: petal-colour attraction axis associated with recurrent florivore damage/preference.",
        "- *Bejaria resinosa*: flower-restricted stickiness directly reduces field florivory with consumer/population dependence.",
        "- *Catalpa speciosa*: floral nectar iridoids deter potential nectar thieves with no detected tested-pollinator consumption cost.",
        "- *Erica* spp.: experimentally added corolla stickiness reduces nectar robbing.",
        "- *Codonopsis lanceolata* / *Fritillaria koidzumiana*: slippery wax-covered perianths experimentally prevent nectar-thieving ant entry; counted as one study cluster.",
        "- *Menyanthes trifoliata*: trimmed petal hairs increase nectar-thieving ant entry success and shorten access time.",
        "- *Thunia alba*: a spur-enclosing bract suppresses robbery and routes the same *Bombus* visitor toward legitimate pollination without increasing arrival frequency.",
        "- *Chrysothemis friedrichsthaliana*: a water-filled calyx reduces pre-anthesis microlepidopteran infestation; independent liquid-barrier origin.",
        "- *Silene latifolia × S. dioica* F2: recombinant floral colour/scent dimensions independently predict *Hadena* primary seed predation.",
        "",
        "Seven environmental/reproductive-module/trait-class context programs and the additional published quantitative syntheses are intentionally excluded from the 25 route-ledger clusters.",
        "",
        "## Boundary",
        "",
        "These counts describe source-adjudicated recurrence capacity in the screened architecture. They are not natural prevalence, and overlapping route counts are not additive independent-study totals. The direct `A x D` and direct joint-cost evidence gaps are unchanged.",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
