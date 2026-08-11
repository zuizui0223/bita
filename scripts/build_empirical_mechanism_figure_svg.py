"""Build manuscript Figure 3 from committed mechanism-synthesis evidence states.

The figure is intentionally an evidence-architecture diagram, not a prevalence
plot and not an estimate of the theoretical mixed partial. Counts are derived
from committed study-cluster ledgers; quantitative-module summaries are parsed
from the canonical module registry. The direct A×D and joint-cost states are
checked against their saturation receipts before rendering.
"""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SYNTHESIS = ROOT / "empirical" / "mechanism_pattern_synthesis"
DEFAULT_OUTPUT = ROOT / "manuscript" / "figures" / "FIGURE_3_EMPIRICAL_MECHANISM_ARCHITECTURE.svg"

ROUTES = (
    "A_to_pollination",
    "A_to_antagonism",
    "D_to_antagonism",
    "D_to_pollination",
)


@dataclass(frozen=True)
class FigureStats:
    record_count: int
    independent_clusters: int
    route_counts: dict[str, int]
    same_system_clusters: int
    sign_switch_clusters: int
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
    joint_cost_estimates: int


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _required_match(pattern: str, text: str, label: str) -> re.Match[str]:
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if not match:
        raise ValueError(f"Could not parse {label} from canonical module registry")
    return match


def collect_stats(root: Path = ROOT) -> FigureStats:
    synthesis = root / "empirical" / "mechanism_pattern_synthesis"
    ledger = _read_csv(synthesis / "MASTER_LEDGER_V1.csv")
    if not ledger:
        raise ValueError("MASTER_LEDGER_V1.csv is empty")

    clusters = {row["independence_cluster"] for row in ledger if row.get("independence_cluster")}
    route_counts = {
        route: len(
            {
                row["independence_cluster"]
                for row in ledger
                if row.get("route") == route and row.get("independence_cluster")
            }
        )
        for route in ROUTES
    }
    same_system = {
        row["independence_cluster"]
        for row in ledger
        if row.get("is_same_system_multi_route", "").strip().lower() == "true"
        and row.get("independence_cluster")
    }
    direct = {
        row["independence_cluster"]
        for row in ledger
        if row.get("is_direct_AxD", "").strip().lower() == "true"
        and row.get("independence_cluster")
    }

    switches = _read_csv(synthesis / "SIGN_SWITCH_LEDGER_V1.csv")
    switch_clusters = {row["study_id"] for row in switches if row.get("study_id")}

    modules = {row["module_id"]: row for row in _read_csv(synthesis / "SECONDARY_SYNTHESIS_MODULES_V1.csv")}
    leal = modules["SM001"]["current_result"]
    sasidharan = modules["SM003"]["current_result"]

    female = _required_match(r"female fitness LRR\s*([+-]?\d+\.\d+)\s*\((\d+) clusters\)", leal, "Leal female fitness")
    nectar = _required_match(r"nectar standing crop\s*([+-]?\d+\.\d+)\s*\((\d+)\)", leal, "Leal nectar")
    visitation = _required_match(r"legitimate visitation\s*([+-]?\d+\.\d+)\s*\((\d+)\)", leal, "Leal visitation")

    roles = _required_match(r"florivore\s*`?(\d+/\d+)`?\s*vs pollinator\s*`?(\d+/\d+)`?", sasidharan, "Sasidharan role counts")
    risk = _required_match(r"risk difference\s*`?([+-]?\d+\.\d+)`?", sasidharan, "Sasidharan risk difference")
    loco = _required_match(r"positive direction\s*(?:\*\*)?([0-9]+/[0-9]+)(?:\*\*)?", sasidharan, "Sasidharan LOCO")

    direct_receipt = (synthesis / "DIRECT_AXD_SATURATION_RECEIPT_V1.md").read_text(encoding="utf-8")
    if "strict direct sign resolved: no" not in direct_receipt:
        raise ValueError("Direct A×D saturation receipt no longer records an unresolved sign")

    joint_receipt = (synthesis / "JOINT_COST_SATURATION_RECEIPT_V1.md").read_text(encoding="utf-8")
    joint = _required_match(
        r"strict direct measured A\+D allocation/construction-cost studies:\s*`?(\d+)`?",
        joint_receipt,
        "strict joint-cost count",
    )

    return FigureStats(
        record_count=len(ledger),
        independent_clusters=len(clusters),
        route_counts=route_counts,
        same_system_clusters=len(same_system),
        sign_switch_clusters=len(switch_clusters),
        direct_clusters=len(direct),
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
        joint_cost_estimates=int(joint.group(1)),
    )


def _minus(value: str) -> str:
    return value.replace("-", "−")


def build_svg(stats: FigureStats) -> str:
    routes = stats.route_counts
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1100" viewBox="0 0 1600 1100">
<defs>
<style>
  .title {{ font: 700 34px "DejaVu Sans", Arial, sans-serif; }}
  .subtitle {{ font: 700 25px "DejaVu Sans", Arial, sans-serif; }}
  .body {{ font: 21px "DejaVu Sans", Arial, sans-serif; }}
  .small {{ font: 18px "DejaVu Sans", Arial, sans-serif; }}
  .tiny {{ font: 16px "DejaVu Sans", Arial, sans-serif; }}
  .box {{ fill: #ffffff; stroke: #222222; stroke-width: 2.5; }}
  .soft {{ fill: #f5f5f5; stroke: #333333; stroke-width: 2; }}
  .direct {{ fill: #e8e8e8; stroke: #111111; stroke-width: 3; }}
  .line {{ stroke: #222222; stroke-width: 2.5; fill: none; }}
  .dash {{ stroke: #222222; stroke-width: 3; stroke-dasharray: 12 10; fill: none; }}
</style>
<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
<path d="M 0 0 L 10 5 L 0 10 z" fill="#222222"/>
</marker>
</defs>
<rect x="0" y="0" width="1600" height="1100" fill="#ffffff"/>
<text x="800" y="48" text-anchor="middle" class="title">Empirical mechanism-pattern architecture and identification boundary</text>
<text x="800" y="82" text-anchor="middle" class="body">Constituent mechanisms recur and switch with context; marginal evidence is not an estimate of W_AD</text>

<rect x="490" y="105" width="620" height="92" rx="16" class="direct"/>
<text x="800" y="143" text-anchor="middle" class="subtitle">Fixed local theory</text>
<text x="800" y="179" text-anchor="middle" class="subtitle">W_AD = ρ − ι − κ</text>

<rect x="60" y="235" width="860" height="300" rx="16" class="box"/>
<text x="490" y="270" text-anchor="middle" class="subtitle">Source-adjudicated mechanism evidence</text>
<text x="490" y="300" text-anchor="middle" class="small">{stats.record_count} effect/directional records · {stats.independent_clusters} independent biological study clusters</text>

<rect x="90" y="330" width="380" height="78" rx="14" class="soft"/>
<text x="280" y="361" text-anchor="middle" class="body">A → pollination</text>
<text x="280" y="391" text-anchor="middle" class="small">{routes['A_to_pollination']} independent clusters</text>
<rect x="510" y="330" width="380" height="78" rx="14" class="soft"/>
<text x="700" y="361" text-anchor="middle" class="body">A → antagonism</text>
<text x="700" y="391" text-anchor="middle" class="small">{routes['A_to_antagonism']} independent clusters</text>
<rect x="90" y="430" width="380" height="78" rx="14" class="soft"/>
<text x="280" y="461" text-anchor="middle" class="body">D → antagonism</text>
<text x="280" y="491" text-anchor="middle" class="small">{routes['D_to_antagonism']} independent clusters</text>
<rect x="510" y="430" width="380" height="78" rx="14" class="soft"/>
<text x="700" y="461" text-anchor="middle" class="body">D → pollination</text>
<text x="700" y="491" text-anchor="middle" class="small">{routes['D_to_pollination']} independent clusters</text>

<rect x="950" y="235" width="590" height="300" rx="16" class="box"/>
<text x="1245" y="270" text-anchor="middle" class="subtitle">Linked architecture and conditionality</text>
<text x="985" y="315" class="body">Same-system multi-route: <tspan font-weight="700">{stats.same_system_clusters} clusters</tspan></text>
<text x="985" y="353" class="body">Context/sign switch: <tspan font-weight="700">{stats.sign_switch_clusters} clusters</tspan></text>
<text x="985" y="397" class="small">Five theory-facing context classes</text>
<text x="1005" y="426" class="tiny">1  trait intensity / expression</text>
<text x="1005" y="449" class="tiny">2  resource / exposure</text>
<text x="1005" y="472" class="tiny">3  consumer identity / role</text>
<text x="1005" y="495" class="tiny">4  response definition / stage / scale</text>
<text x="1005" y="518" class="tiny">5  compound identity / mechanism partition</text>

<rect x="60" y="575" width="690" height="185" rx="16" class="box"/>
<text x="405" y="610" text-anchor="middle" class="subtitle">Quantitative module 1 · floral larceny</text>
<text x="95" y="648" class="body">Female fitness: LRR {_minus(stats.leal_female_lrr)} · {stats.leal_female_k} clusters</text>
<text x="95" y="682" class="body">Nectar standing crop: LRR {_minus(stats.leal_nectar_lrr)} · {stats.leal_nectar_k}</text>
<text x="95" y="716" class="body">Legitimate visitation: LRR {_minus(stats.leal_visitation_lrr)} · {stats.leal_visitation_k}</text>
<text x="95" y="744" class="tiny">Realised antagonist-pressure costs; high heterogeneity retained</text>

<rect x="790" y="575" width="750" height="185" rx="16" class="box"/>
<text x="1165" y="610" text-anchor="middle" class="subtitle">Quantitative module 2 · floral volatiles</text>
<text x="825" y="648" class="body">Physiological detection: florivore {stats.sasidharan_florivore} · pollinator {stats.sasidharan_pollinator}</text>
<text x="825" y="682" class="body">Assembled risk difference {stats.sasidharan_risk_difference} · LOCO positive {stats.sasidharan_loco}</text>
<text x="825" y="716" class="body">Paired both-role components: 3 · all paired differences = 0</text>
<text x="825" y="744" class="tiny">Repeated behavioral units switch attraction ↔ no response across studies</text>

<line x1="60" y1="812" x2="1540" y2="812" class="dash"/>
<rect x="520" y="785" width="560" height="62" fill="#ffffff"/>
<text x="800" y="817" text-anchor="middle" class="subtitle">IDENTIFICATION BOUNDARY</text>
<text x="800" y="842" text-anchor="middle" class="small">Evidence above supports mechanism recurrence / conditionality, not W_AD</text>

<rect x="155" y="885" width="560" height="110" rx="14" class="direct"/>
<text x="435" y="920" text-anchor="middle" class="subtitle">Direct A × D layer</text>
<text x="435" y="954" text-anchor="middle" class="body">{stats.direct_clusters} strict cluster · sign unresolved</text>
<text x="435" y="982" text-anchor="middle" class="tiny">Two reproductive-component CIs include zero</text>

<rect x="885" y="885" width="560" height="110" rx="14" class="direct"/>
<text x="1165" y="920" text-anchor="middle" class="subtitle">Direct joint-cost layer</text>
<text x="1165" y="954" text-anchor="middle" class="body">{stats.joint_cost_estimates} strict estimates · κ unidentified</text>
<text x="1165" y="982" text-anchor="middle" class="tiny">Zero eligible estimates ≠ κ = 0</text>

<text x="800" y="1045" text-anchor="middle" class="small">Only linked direct designs can identify the cross-trait interaction; marginal evidence cannot be algebraically combined into it.</text>

<path d="M 620 197 C 500 215, 430 215, 430 235" class="line" marker-end="url(#arrow)"/>
<path d="M 980 197 C 1100 215, 1190 215, 1190 235" class="line" marker-end="url(#arrow)"/>
</svg>\n'''


def write_svg(output_path: Path = DEFAULT_OUTPUT, root: Path = ROOT) -> Path:
    stats = collect_stats(root)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_svg(stats), encoding="utf-8")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", nargs="?", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    path = write_svg(args.output)
    print(path)


if __name__ == "__main__":
    main()
