"""Build manuscript Figure 3 from the saturated mechanism-pattern evidence state.

The figure is an evidence-architecture diagram, not a prevalence plot and not an
estimate of the theoretical mixed partial. It reads the frozen canonical ledgers
plus all admitted expansion ledgers, while preserving the direct A×D and joint-
cost identification boundary.
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SYNTHESIS = ROOT / "empirical" / "mechanism_pattern_synthesis"
DEFAULT_OUTPUT = ROOT / "manuscript" / "figures" / "FIGURE_3_EMPIRICAL_MECHANISM_ARCHITECTURE.svg"

BASE_LEDGER_NAMES = (
    "MASTER_LEDGER_V1.csv",
    "LEDGER_BATCH_2_V1.csv",
    "LEDGER_BATCH_3_V1.csv",
    "LEDGER_BATCH_4_V1.csv",
    "LEDGER_BATCH_5_V1.csv",
)
MARGINAL_ROUTES = (
    "A_to_pollination",
    "A_to_antagonism",
    "D_to_antagonism",
    "D_to_pollination",
)
DIRECT_ROUTE = "direct_AxD"


@dataclass(frozen=True)
class FigureStats:
    record_count: int
    independent_clusters: int
    route_counts: dict[str, int]
    same_system_clusters: int
    sign_switch_clusters: int
    context_programs: int
    direct_clusters: int
    leal_female_lrr: str
    leal_female_k: int
    leal_nectar_lrr: str
    leal_nectar_k: int
    leal_visitation_lrr: str
    leal_visitation_k: int
    sasidharan_florivore: str
    sasidharan_pollinator: str
    sasidharan_risk_difference: str
    sasidharan_loco: str
    secondary_context_modules: int
    joint_cost_estimates: int


def _text(value: object) -> str:
    return str(value or "").strip()


def _bool(value: object) -> bool:
    return _text(value).lower() == "true"


def _read_csv(path: Path, *, strict_overflow: bool = False) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = []
        for row in csv.DictReader(handle):
            # Frozen canonical ledgers contain a known legacy notes-field overflow
            # in at least one row. The canonical audit historically ignores that
            # trailing notes fragment, and changing the source ledger here would
            # alter a frozen evidence object. Newly added expansion ledgers are
            # held to the stricter no-overflow contract.
            if strict_overflow and None in row:
                raise ValueError(
                    f"CSV column overflow in {path.name}: "
                    f"{row.get('record_id') or row.get('study_id')}: {row[None]}"
                )
            rows.append({key: _text(value) for key, value in row.items() if key is not None})
        return rows


def _ledger_paths(synthesis: Path) -> list[tuple[Path, bool]]:
    paths = [(synthesis / name, False) for name in BASE_LEDGER_NAMES]
    paths.extend((path, True) for path in sorted(synthesis.glob("EXPANSION_LEDGER_BATCH_*_V1.csv")))
    return paths


def _coverage_rows(synthesis: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path, strict in _ledger_paths(synthesis):
        rows.extend(_read_csv(path, strict_overflow=strict))

    ids = [row.get("record_id", "") for row in rows]
    duplicates = sorted({rid for rid in ids if rid and ids.count(rid) > 1})
    missing_ids = sum(not rid for rid in ids)
    missing_clusters = sum(not row.get("independence_cluster", "") for row in rows)
    known_routes = set(MARGINAL_ROUTES) | {DIRECT_ROUTE}
    unknown_routes = sorted({row.get("route", "") for row in rows if row.get("route", "") not in known_routes})
    bad_direct = [row.get("record_id", "") for row in rows if row.get("record_id", "").startswith("MPX") and _bool(row.get("is_direct_AxD"))]
    if duplicates or missing_ids or missing_clusters or unknown_routes or bad_direct:
        raise ValueError(
            "Coverage-ledger validation failed: "
            f"duplicates={duplicates}, missing_ids={missing_ids}, missing_clusters={missing_clusters}, "
            f"unknown_routes={unknown_routes}, illegal_expansion_direct={bad_direct}"
        )
    return rows


def _same_system_count(rows: list[dict[str, str]]) -> int:
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
    return len(explicit | inferred)


def _required_match(pattern: str, text: str, label: str) -> re.Match[str]:
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if not match:
        raise ValueError(f"Could not parse {label}")
    return match


def collect_stats(root: Path = ROOT) -> FigureStats:
    synthesis = root / "empirical" / "mechanism_pattern_synthesis"
    ledger = _coverage_rows(synthesis)
    clusters = {row["independence_cluster"] for row in ledger}
    route_counts = {
        route: len({row["independence_cluster"] for row in ledger if row.get("route") == route})
        for route in MARGINAL_ROUTES
    }
    direct_clusters = len({row["independence_cluster"] for row in ledger if row.get("route") == DIRECT_ROUTE})

    switch_paths = [synthesis / "SIGN_SWITCH_LEDGER_V1.csv"]
    switch_paths.extend(sorted(synthesis.glob("EXPANSION_SIGN_SWITCH_BATCH_*_V1.csv")))
    switches = [row for path in switch_paths for row in _read_csv(path)]
    switch_clusters = {row["study_id"] for row in switches if row.get("study_id")}

    context_path = synthesis / "EXPANSION_CONTEXT_PROGRAMS_V1.csv"
    context_programs = len(_read_csv(context_path)) if context_path.exists() else 0

    modules = {row["module_id"]: row for row in _read_csv(synthesis / "SECONDARY_SYNTHESIS_MODULES_V1.csv")}
    leal = modules["SM001"]["current_result"]
    sasidharan = modules["SM003"]["current_result"]

    female = _required_match(r"female fitness LRR\s*([+-]?\d+\.\d+)\s*\((\d+) clusters\)", leal, "Leal female fitness")
    nectar = _required_match(r"nectar standing crop\s*([+-]?\d+\.\d+)\s*\((\d+)\)", leal, "Leal nectar")
    visitation = _required_match(r"legitimate visitation\s*([+-]?\d+\.\d+)\s*\((\d+)\)", leal, "Leal visitation")
    roles = _required_match(r"florivore\s*`?(\d+/\d+)`?\s*vs pollinator\s*`?(\d+/\d+)`?", sasidharan, "Sasidharan role counts")
    risk = _required_match(r"risk difference\s*`?([+-]?\d+\.\d+)`?", sasidharan, "Sasidharan risk difference")
    loco = _required_match(r"leave-one-study-component-out.*?positive(?: direction)?\s*(?:\*\*)?([0-9]+/[0-9]+)(?:\*\*)?", sasidharan, "Sasidharan LOCO")

    direct_receipt = (synthesis / "DIRECT_AXD_SATURATION_RECEIPT_V1.md").read_text(encoding="utf-8")
    if "strict direct sign resolved: no" not in direct_receipt or direct_clusters != 1:
        raise ValueError("Direct A×D state drifted from one sign-unresolved cluster")

    joint_receipt = (synthesis / "JOINT_COST_SATURATION_RECEIPT_V1.md").read_text(encoding="utf-8")
    joint = _required_match(r"strict direct measured A\+D allocation/construction-cost studies:\s*`?(\d+)`?", joint_receipt, "strict joint-cost count")

    pattern_registry = synthesis / "PATTERN_MODULE_REGISTRY_V2.csv"
    secondary_context_modules = 0
    if pattern_registry.exists():
        registry = _read_csv(pattern_registry)
        secondary_context_modules = sum(row.get("module_id") in {"PM03", "PM04", "PM05"} for row in registry)

    return FigureStats(
        record_count=len(ledger),
        independent_clusters=len(clusters),
        route_counts=route_counts,
        same_system_clusters=_same_system_count(ledger),
        sign_switch_clusters=len(switch_clusters),
        context_programs=context_programs,
        direct_clusters=direct_clusters,
        leal_female_lrr=female.group(1),
        leal_female_k=int(female.group(2)),
        leal_nectar_lrr=nectar.group(1),
        leal_nectar_k=int(nectar.group(2)),
        leal_visitation_lrr=visitation.group(1),
        leal_visitation_k=int(visitation.group(2)),
        sasidharan_florivore=roles.group(1),
        sasidharan_pollinator=roles.group(2),
        sasidharan_risk_difference=risk.group(1),
        sasidharan_loco=loco.group(1),
        secondary_context_modules=secondary_context_modules,
        joint_cost_estimates=int(joint.group(1)),
    )


def _minus(value: str) -> str:
    return value.replace("-", "−")


def build_svg(stats: FigureStats) -> str:
    r = stats.route_counts
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1120" viewBox="0 0 1600 1120">
<defs><style>
.title{{font:700 34px DejaVu Sans,Arial,sans-serif}} .subtitle{{font:700 24px DejaVu Sans,Arial,sans-serif}}
.body{{font:20px DejaVu Sans,Arial,sans-serif}} .small{{font:17px DejaVu Sans,Arial,sans-serif}} .tiny{{font:15px DejaVu Sans,Arial,sans-serif}}
.box{{fill:#fff;stroke:#222;stroke-width:2.5}} .soft{{fill:#f5f5f5;stroke:#333;stroke-width:2}} .direct{{fill:#e9e9e9;stroke:#111;stroke-width:3}}
.dash{{stroke:#222;stroke-width:3;stroke-dasharray:12 10;fill:none}}
</style></defs>
<rect width="1600" height="1120" fill="#fff"/>
<text x="800" y="48" text-anchor="middle" class="title">Meta-analytic pattern architecture and identification boundary</text>
<text x="800" y="80" text-anchor="middle" class="body">Recurrent mechanisms + context-dependent balance; route evidence is not W_AD</text>

<rect x="510" y="105" width="580" height="88" rx="16" class="direct"/>
<text x="800" y="140" text-anchor="middle" class="subtitle">Fixed local theory</text><text x="800" y="174" text-anchor="middle" class="subtitle">W_AD = ρ − ι − κ</text>

<rect x="55" y="225" width="875" height="310" rx="16" class="box"/>
<text x="493" y="260" text-anchor="middle" class="subtitle">Source-adjudicated Pattern scaffold</text>
<text x="493" y="292" text-anchor="middle" class="small">{stats.record_count} effect/directional records · {stats.independent_clusters} independent biological study clusters</text>
<rect x="88" y="325" width="390" height="78" rx="14" class="soft"/><text x="283" y="357" text-anchor="middle" class="body">A → pollination</text><text x="283" y="387" text-anchor="middle" class="small">{r['A_to_pollination']} independent clusters</text>
<rect x="510" y="325" width="390" height="78" rx="14" class="soft"/><text x="705" y="357" text-anchor="middle" class="body">A → antagonism</text><text x="705" y="387" text-anchor="middle" class="small">{r['A_to_antagonism']} independent clusters</text>
<rect x="88" y="430" width="390" height="78" rx="14" class="soft"/><text x="283" y="462" text-anchor="middle" class="body">D → antagonism</text><text x="283" y="492" text-anchor="middle" class="small">{r['D_to_antagonism']} independent clusters</text>
<rect x="510" y="430" width="390" height="78" rx="14" class="soft"/><text x="705" y="462" text-anchor="middle" class="body">D → pollination</text><text x="705" y="492" text-anchor="middle" class="small">{r['D_to_pollination']} independent clusters</text>

<rect x="960" y="225" width="585" height="310" rx="16" class="box"/>
<text x="1252" y="260" text-anchor="middle" class="subtitle">Recurrence and conditionality</text>
<text x="995" y="305" class="body">Same-system multi-route: <tspan font-weight="700">{stats.same_system_clusters} clusters</tspan></text>
<text x="995" y="340" class="body">Context/sign switch: <tspan font-weight="700">{stats.sign_switch_clusters} clusters</tspan></text>
<text x="995" y="375" class="body">Context-only programs: <tspan font-weight="700">{stats.context_programs}</tspan></text>
<text x="995" y="415" class="small">Recurring state transitions</text>
<text x="1015" y="444" class="tiny">• guarded defence: antagonist relief without universal pollinator cost</text>
<text x="1015" y="468" class="tiny">• spatial / temporal / attack-mode filtering</text>
<text x="1015" y="492" class="tiny">• visitor functional-mode and lifecycle-role switching</text>
<text x="1015" y="516" class="tiny">• response-stage, resource, population and trait-class dependence</text>

<rect x="55" y="570" width="700" height="190" rx="16" class="box"/>
<text x="405" y="605" text-anchor="middle" class="subtitle">Reproduced meta-analysis · floral larceny</text>
<text x="90" y="645" class="body">Female fitness: LRR {_minus(stats.leal_female_lrr)} · {stats.leal_female_k} clusters</text>
<text x="90" y="679" class="body">Nectar standing crop: LRR {_minus(stats.leal_nectar_lrr)} · {stats.leal_nectar_k}</text>
<text x="90" y="713" class="body">Legitimate visitation: LRR {_minus(stats.leal_visitation_lrr)} · {stats.leal_visitation_k}</text>
<text x="90" y="742" class="tiny">Direction robust; extreme heterogeneity retained</text>

<rect x="790" y="570" width="755" height="190" rx="16" class="box"/>
<text x="1168" y="605" text-anchor="middle" class="subtitle">Reproduced synthesis · floral volatiles</text>
<text x="825" y="645" class="body">Physiological detection: florivore {stats.sasidharan_florivore} · pollinator {stats.sasidharan_pollinator}</text>
<text x="825" y="679" class="body">Risk difference {stats.sasidharan_risk_difference} · LOCO positive {stats.sasidharan_loco}</text>
<text x="825" y="713" class="body">Paired both-role components: 3 · paired differences = 0</text>
<text x="825" y="742" class="tiny">Composition and context dependence remain explicit</text>

<rect x="250" y="785" width="1100" height="62" rx="12" class="soft"/>
<text x="800" y="813" text-anchor="middle" class="body">Secondary contextual syntheses ({stats.secondary_context_modules}): Haas-Desmarais 2026 · Caruso 2019 · Junker &amp; Blüthgen 2010</text>
<text x="800" y="837" text-anchor="middle" class="tiny">Published/deposit-verified context modules; not pooled with the two reproduced quantitative modules</text>

<line x1="55" y1="890" x2="1545" y2="890" class="dash"/>
<rect x="515" y="860" width="570" height="62" fill="#fff"/><text x="800" y="898" text-anchor="middle" class="subtitle">IDENTIFICATION BOUNDARY</text>

<rect x="85" y="940" width="680" height="125" rx="16" class="direct"/>
<text x="425" y="975" text-anchor="middle" class="subtitle">Direct A × D</text>
<text x="425" y="1009" text-anchor="middle" class="body">{stats.direct_clusters} strict cluster · sign unresolved</text>
<text x="425" y="1040" text-anchor="middle" class="small">Marginal + same-system evidence ≠ direct mixed partial</text>

<rect x="835" y="940" width="680" height="125" rx="16" class="direct"/>
<text x="1175" y="975" text-anchor="middle" class="subtitle">Direct joint cost κ</text>
<text x="1175" y="1009" text-anchor="middle" class="body">{stats.joint_cost_estimates} strict estimates · κ unidentified</text>
<text x="1175" y="1040" text-anchor="middle" class="small">Zero eligible estimates ≠ κ = 0</text>

<text x="800" y="1100" text-anchor="middle" class="small">Counts describe evidence capacity in the screened architecture, not prevalence in nature; none of the upper layers is W_AD.</text>
</svg>'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", nargs="?", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()
    stats = collect_stats(ROOT)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_svg(stats), encoding="utf-8")
    print(
        f"wrote {output}: records={stats.record_count}, clusters={stats.independent_clusters}, "
        f"same_system={stats.same_system_clusters}, switches={stats.sign_switch_clusters}, context_programs={stats.context_programs}"
    )


if __name__ == "__main__":
    main()
