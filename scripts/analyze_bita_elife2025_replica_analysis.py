"""Independent replicate-line reanalysis of eLife 97216 original Figure 2/3 cells.

Only the publisher's SHA-pinned Fig2/3 tables are used. Repeated generations
are not independent lines; source-pool cells are not independent populations.
All tests are post-publication and exploratory.
"""
from __future__ import annotations

import csv
import itertools
import json
import math
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "empirical/trait_architecture_history/mihajlovic2025_fig2_fig3_replicates.csv"
RESULT = SOURCE.with_name("mihajlovic2025_replica_reanalysis.json")
SHA = {
    "fig2": "d8ab8a5cd012654e32cd1bac2059bd423ea2731f0e3a00ee39134ce632138bee",
    "fig3": "8c9e9c84b4e2ed49684c580fc26863a871628a9a41125e9ead89f1c788c8bf32",
}
GENS = {"fig2": (1, 2, 3, 4, 5), "fig3": (0, 1, 2, 3, 4, 5)}
ENDPOINTS = {
    "fig2": "fraction_fluorescent_cells",
    "fig3": "log10_fluorescence_normalized_to_ancestral",
}

def read_rows(path: Path = SOURCE) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as stream:
        raw = list(csv.DictReader(stream))
    rows = []
    for item in raw:
        row = dict(item)
        row["source_row"] = int(row["source_row"])
        row["generation"] = int(row["generation"])
        row["value"] = float(row["value"])
        rows.append(row)
    return rows

def exact_perm(single, double) -> dict:
    """Two-sided label permutation of 3+3 independent lines (20 assignments)."""
    if len(single) != 3 or len(double) != 3 or not all(
        math.isfinite(float(x)) for x in [*single, *double]
    ):
        raise ValueError("requires 3 finite independent line summaries per group")
    pooled = tuple(single) + tuple(double)
    observed = mean(double) - mean(single)
    total = sum(pooled)
    extreme = 0
    n = 0
    for chosen in itertools.combinations(range(6), 3):
        s = sum(pooled[j] for j in chosen)
        difference = (2 * s - total) / 3
        extreme += abs(difference) >= abs(observed) - 1e-12
        n += 1
    return {"extreme_permutations": extreme, "permutations": n, "p_two_sided": extreme / n}

def _point(single, double):
    out = {"single_mean": mean(single), "double_mean": mean(double),
           "difference_double_minus_single": mean(double) - mean(single)}
    return {**out, **exact_perm(single, double)}

def _auc(points: list[tuple[int, float]]) -> float:
    ordered = sorted(points)
    if len(ordered) < 2 or len({g for g, _ in ordered}) != len(ordered):
        raise ValueError("at least two distinct ordered generations")
    area = sum(
        (ordered[i][1] + ordered[i+1][1])
        * (ordered[i+1][0] - ordered[i][0]) / 2
        for i in range(len(ordered)-1)
    )
    return area / (ordered[-1][0] - ordered[0][0])

def summarize(rows: list[dict]) -> dict:
    if len(rows) != 66:
        raise ValueError("expected 30 Fig2 and 36 Fig3 source observations")
    seen = set()
    source_rows = set()
    for r in rows:
        fig, group = r["figure"], r["copy_group"]
        rep, generation, value = r["biological_replicate"], r["generation"], r["value"]
        if (fig not in SHA or group not in ("single", "double")
            or rep not in ("X", "Y", "Z") or generation not in GENS[fig]
            or not math.isfinite(value)
            or r["publisher_xlsx_sha256"] != SHA[fig]
            or r["doi"] != "10.7554/eLife.97216.3"
            or r["endpoint"] != ENDPOINTS[fig]
            or r["worksheet"] != ("sheet1" if fig=="fig2" else "sheet2")):
            raise ValueError("source identity, group, generation, or value mismatch")
        if fig == "fig2" and not 0 <= value <= 1:
            raise ValueError("fraction must be a probability")
        key = fig, group, rep, generation
        source_key = fig, r["worksheet"], r["source_row"]
        if key in seen:
            raise ValueError("duplicate biological replicate-generation")
        if source_key in source_rows:
            raise ValueError("duplicate original workbook row")
        seen.add(key)
        source_rows.add(source_key)

    result = {
        "doi": "10.7554/eLife.97216.3",
        "data_level": "ORIGINAL_PUBLISHER_XLSX_EXTRACTED_CELLS_SHA_PINNED",
        "source_sha256": SHA,
        "independent_biological_replicates_per_group": 3,
        "analysis_status": "POST_PUBLICATION_EXPLORATORY",
        "pooled_meta_analysis_performed": False,
        "evolutionary_origin_or_hysteresis_identified": False,
        "claim_boundary": (
            "One experimental source per Figure 2/3 outcome, not 10 or 11 independent "
            "studies. Five/six generations are repeated observations of the same "
            "three replicate lines per copy-number treatment. No two-copy division "
            "of labor, K(u), or evolutionary history identified by these readouts."
        ),
    }
    for figure, label in (
        ("fig2", "fig2_robustness"),
        ("fig3", "fig3_normalized_fluorescence"),
    ):
        data = [r for r in rows if r["figure"] == figure]
        if len(data) != len(GENS[figure]) * 6:
            raise ValueError("wrong within-figure row count")
        steps = []
        trajectories = {"single": [], "double": []}
        for g in GENS[figure]:
            groups = {q: [r["value"] for r in data if r["copy_group"] == q
                          and r["generation"] == g] for q in ("single","double")}
            if any(len(v) != 3 for v in groups.values()):
                raise ValueError("incomplete generation/group")
            steps.append({"generation": g, **_point(groups["single"], groups["double"])})
        for group in ("single", "double"):
            for rep in ("X", "Y", "Z"):
                series = [(r["generation"], r["value"]) for r in data
                          if r["copy_group"] == group and r["biological_replicate"] == rep]
                if tuple(sorted(g for g, _ in series)) != GENS[figure]:
                    raise ValueError("incomplete replicate trajectory")
                trajectories[group].append(_auc(series))
        result[label] = {
            "n_values": len(data),
            "n_replicate_trajectories": 6,
            "endpoint": ENDPOINTS[figure],
            "generations": list(GENS[figure]),
            "per_generation": steps,
            "final_gen": steps[-1],
            "trajectory_auc": {
                **_point(trajectories["single"], trajectories["double"]),
                "single_per_replicate": trajectories["single"],
                "double_per_replicate": trajectories["double"],
                "method": "trapezoid AUC divided by generation span; independent unit is line",
            },
        }
    return result

def main() -> None:
    readout = summarize(read_rows())
    RESULT.write_text(json.dumps(readout, indent=2, ensure_ascii=False, allow_nan=False)
                      + "\n", encoding="utf-8")
    print(json.dumps({
        "source_figures": list(SHA),
        "fig2_final": readout["fig2_robustness"]["final_gen"],
        "fig3_final": readout["fig3_normalized_fluorescence"]["final_gen"],
        "fig2_trajectory": readout["fig2_robustness"]["trajectory_auc"],
        "fig3_trajectory": readout["fig3_normalized_fluorescence"]["trajectory_auc"],
    }, ensure_ascii=False))

if __name__ == "__main__":
    main()
