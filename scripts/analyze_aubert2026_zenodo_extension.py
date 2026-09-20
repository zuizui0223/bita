"""Independent Aubert-style access-barrier extension using the public EPHI Zenodo mirror.

This is not an exact replication of Aubert et al. 2026, which used three transects
and AVONET bill traits. The extension uses all 18 Ecuador EPHI sites, the mirror's
culmen_length field (mm), site-specific plant tube length (cm), and pair-site
robbery rates. Raw rows and species identifiers are not emitted.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
import random
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from trait_architecture.numerics import spearman as _shared_spearman

BASE = "https://zenodo.org/records/14185547/files"
FILES = {
    "interactions": "Interactions_data_Ecuador.txt",
    "cameras": "Cameras_data_Ecuador.txt",
    "plants": "Plant_traits.txt",
    "birds": "Hummingbird_traits.txt",
}
SEED = 20260919
USER_AGENT = "bita-aubert-zenodo-extension/1.0"


def _download(name: str) -> bytes:
    url = f"{BASE}/{quote(name)}?download=1"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=90) as response:  # nosec B310 fixed Zenodo URL
        return response.read()


def _read(data: bytes) -> list[dict[str, str]]:
    text = data.decode("utf-8-sig", errors="replace")
    try:
        dialect = csv.Sniffer().sniff(text[:8192], delimiters="\t,;")
        delimiter = dialect.delimiter
    except csv.Error:
        delimiter = "\t"
    return [dict(row) for row in csv.DictReader(io.StringIO(text), delimiter=delimiter)]


def _as_float(value: object) -> float | None:
    try:
        x = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def _mean(values: list[float]) -> float:
    return sum(values) / len(values)


def _median(values: list[float]) -> float:
    s = sorted(values)
    n = len(s)
    m = n // 2
    return s[m] if n % 2 else (s[m - 1] + s[m]) / 2


def spearman(x: list[float], y: list[float]) -> float:
    return _shared_spearman(x, y)

def _perm_p_spearman(x: list[float], y: list[float], permutations: int, seed: int) -> tuple[float, float]:
    obs = spearman(x, y)
    rng = random.Random(seed)
    shuffled = list(y)
    extreme = 0
    for _ in range(permutations):
        rng.shuffle(shuffled)
        if abs(spearman(x, shuffled)) >= abs(obs) - 1e-15:
            extreme += 1
    return obs, (extreme + 1) / (permutations + 1)


def _perm_p_mean_diff(values: list[float], barrier: list[bool], permutations: int, seed: int) -> tuple[float, float]:
    a = [v for v, b in zip(values, barrier) if b]
    b = [v for v, flag in zip(values, barrier) if not flag]
    if not a or not b:
        raise ValueError("both barrier groups are required")
    obs = _mean(a) - _mean(b)
    labels = list(barrier)
    rng = random.Random(seed)
    extreme = 0
    for _ in range(permutations):
        rng.shuffle(labels)
        pa = [v for v, flag in zip(values, labels) if flag]
        pb = [v for v, flag in zip(values, labels) if not flag]
        diff = _mean(pa) - _mean(pb)
        if abs(diff) >= abs(obs) - 1e-15:
            extreme += 1
    return obs, (extreme + 1) / (permutations + 1)


def build_pair_site_rows(
    interactions: list[dict[str, str]],
    cameras: list[dict[str, str]],
    plants: list[dict[str, str]],
    birds: list[dict[str, str]],
) -> tuple[list[dict[str, float | str | bool | int]], dict[str, int]]:
    camera_map: dict[str, tuple[str, str]] = {}
    for row in cameras:
        wp = str(row.get("waypoint", "")).strip()
        site = str(row.get("site", "")).strip()
        plant = str(row.get("plant_species", "")).strip()
        if wp and site and plant:
            camera_map.setdefault(wp, (site, plant))

    plant_values: dict[tuple[str, str], list[float]] = defaultdict(list)
    plant_global: dict[str, list[float]] = defaultdict(list)
    for row in plants:
        if str(row.get("Country", "")).strip().lower() not in {"ecuador", ""}:
            continue
        species = str(row.get("plant_species", "")).strip()
        site = str(row.get("site", "")).strip()
        tube = _as_float(row.get("Tubelength"))
        if species and tube is not None and tube > 0:
            plant_global[species].append(tube)
            if site:
                plant_values[(site, species)].append(tube)

    bird_values: dict[str, list[float]] = defaultdict(list)
    for row in birds:
        species = str(row.get("hummingbird_species", "")).strip()
        culmen = _as_float(row.get("culmen_length"))
        if species and culmen is not None and culmen > 0:
            bird_values[species].append(culmen)

    grouped: dict[tuple[str, str, str], dict[str, object]] = {}
    resolved_interactions = 0
    trait_matched_interactions = 0
    group_counts = defaultdict(int)

    for row in interactions:
        status = str(row.get("piercing", "")).strip().lower()
        if status not in {"yes", "no"}:
            continue
        family = str(row.get("hummingbird_family", "")).strip()
        genus = str(row.get("hummingbird_genus", "")).strip()
        if not (family == "Trochilidae" or genus == "Diglossa"):
            continue
        species = str(row.get("hummingbird_species", "")).strip()
        wp = str(row.get("waypoint", "")).strip()
        if not species or wp not in camera_map:
            continue
        site, plant_species = camera_map[wp]
        resolved_interactions += 1
        tube_vals = plant_values.get((site, plant_species)) or plant_global.get(plant_species)
        bill_vals = bird_values.get(species)
        if not tube_vals or not bill_vals:
            continue
        tube_cm = _mean(tube_vals)
        culmen_cm = _mean(bill_vals) / 10.0
        if tube_cm <= 0 or culmen_cm <= 0:
            continue
        trait_matched_interactions += 1
        key = (site, species, plant_species)
        item = grouped.setdefault(key, {
            "site": site,
            "tube_cm": tube_cm,
            "culmen_cm": culmen_cm,
            "robbing": 0,
            "legitimate": 0,
            "bird_group": "flowerpiercer" if genus == "Diglossa" else "hummingbird",
        })
        if status == "yes":
            item["robbing"] = int(item["robbing"]) + 1
        else:
            item["legitimate"] = int(item["legitimate"]) + 1
        group_counts[str(item["bird_group"])] += 1

    rows_out: list[dict[str, float | str | bool | int]] = []
    for item in grouped.values():
        rob = int(item["robbing"])
        leg = int(item["legitimate"])
        total = rob + leg
        if total <= 0:
            continue
        tube = float(item["tube_cm"])
        bill = float(item["culmen_cm"])
        mismatch = math.log(tube / bill)
        rows_out.append({
            "site": str(item["site"]),
            "bird_group": str(item["bird_group"]),
            "n_interactions": total,
            "robbery_rate": rob / total,
            "mismatch_log_t_over_b": mismatch,
            "trait_barrier": mismatch > 0,
        })

    audit = {
        "resolved_target_interactions": resolved_interactions,
        "trait_matched_interactions": trait_matched_interactions,
        "pair_site_rows": len(rows_out),
        "sites": len({str(row["site"]) for row in rows_out}),
        "hummingbird_pair_sites": sum(row["bird_group"] == "hummingbird" for row in rows_out),
        "flowerpiercer_pair_sites": sum(row["bird_group"] == "flowerpiercer" for row in rows_out),
    }
    return rows_out, audit



def _binomial_two_sided_sign_p(positive: int, total: int) -> float | None:
    if total <= 0:
        return None
    k = min(positive, total - positive)
    tail = sum(math.comb(total, i) for i in range(k + 1)) / (2 ** total)
    return min(1.0, 2 * tail)


def _site_difference_summary(
    rows: list[dict[str, float | str | bool | int]],
    *,
    permutations: int,
    seed: int,
) -> dict[str, object]:
    by_site: dict[str, list[dict[str, float | str | bool | int]]] = defaultdict(list)
    for row in rows:
        by_site[str(row["site"])].append(row)

    observed_diffs: dict[str, float] = {}
    eligible_rows: dict[str, list[dict[str, float | str | bool | int]]] = {}
    for site, site_rows in by_site.items():
        barrier_rates = [float(r["robbery_rate"]) for r in site_rows if bool(r["trait_barrier"])]
        accessible_rates = [float(r["robbery_rate"]) for r in site_rows if not bool(r["trait_barrier"])]
        if not barrier_rates or not accessible_rates:
            continue
        observed_diffs[site] = _mean(barrier_rates) - _mean(accessible_rates)
        eligible_rows[site] = site_rows

    if not observed_diffs:
        return {
            "eligible_sites": 0,
            "positive_sites": 0,
            "mean_within_site_difference": None,
            "median_within_site_difference": None,
            "sign_test_p": None,
            "site_stratified_permutation_p": None,
        }

    observed_stat = _mean(list(observed_diffs.values()))
    positive = sum(diff > 0 for diff in observed_diffs.values())
    nonzero = sum(diff != 0 for diff in observed_diffs.values())
    sign_p = _binomial_two_sided_sign_p(positive, nonzero) if nonzero else None

    rng = random.Random(seed)
    extreme = 0
    for _ in range(permutations):
        perm_diffs = []
        for site, site_rows in eligible_rows.items():
            values = [float(r["robbery_rate"]) for r in site_rows]
            labels = [bool(r["trait_barrier"]) for r in site_rows]
            rng.shuffle(labels)
            a = [v for v, flag in zip(values, labels) if flag]
            b = [v for v, flag in zip(values, labels) if not flag]
            perm_diffs.append(_mean(a) - _mean(b))
        stat = _mean(perm_diffs)
        if abs(stat) >= abs(observed_stat) - 1e-15:
            extreme += 1

    return {
        "eligible_sites": len(observed_diffs),
        "positive_sites": positive,
        "mean_within_site_difference": observed_stat,
        "median_within_site_difference": _median(list(observed_diffs.values())),
        "sign_test_p": sign_p,
        "site_stratified_permutation_p": (extreme + 1) / (permutations + 1),
    }


def _min_interaction_sensitivity(
    rows: list[dict[str, float | str | bool | int]],
    *,
    permutations: int,
    seed: int,
) -> dict[str, object]:
    out: dict[str, object] = {}
    for offset, minimum in enumerate((1, 2, 5)):
        subset = [
            row
            for row in rows
            if int(row.get("n_interactions", 1)) >= minimum
        ]
        key = f"min_{minimum}"
        if len(subset) < 6:
            out[key] = {
                "n_pair_sites": len(subset),
                "status": "INSUFFICIENT_ROWS",
            }
            continue

        rates = [float(row["robbery_rate"]) for row in subset]
        mismatch = [float(row["mismatch_log_t_over_b"]) for row in subset]
        barrier = [bool(row["trait_barrier"]) for row in subset]
        if not any(barrier) or all(barrier):
            out[key] = {
                "n_pair_sites": len(subset),
                "status": "ONE_BARRIER_CLASS_ONLY",
            }
            continue

        rho, rho_p = _perm_p_spearman(
            mismatch,
            rates,
            permutations,
            seed + 100 + offset,
        )
        diff, diff_p = _perm_p_mean_diff(
            rates,
            barrier,
            permutations,
            seed + 200 + offset,
        )
        barrier_rates = [v for v, flag in zip(rates, barrier) if flag]
        accessible_rates = [v for v, flag in zip(rates, barrier) if not flag]
        out[key] = {
            "status": "FIT",
            "n_pair_sites": len(subset),
            "barrier_pair_sites": len(barrier_rates),
            "accessible_pair_sites": len(accessible_rates),
            "mean_robbery_rate_barrier": _mean(barrier_rates),
            "mean_robbery_rate_accessible": _mean(accessible_rates),
            "barrier_minus_accessible_mean_rate": diff,
            "barrier_mean_difference_permutation_p": diff_p,
            "mismatch_spearman_rho": rho,
            "mismatch_spearman_permutation_p": rho_p,
        }
    return out

def summarize_pair_sites(rows: list[dict[str, float | str | bool | int]], permutations: int = 9999, seed: int = SEED) -> dict[str, object]:
    if len(rows) < 6:
        raise ValueError("too few trait-matched pair-site rows")
    rates = [float(row["robbery_rate"]) for row in rows]
    mismatch = [float(row["mismatch_log_t_over_b"]) for row in rows]
    barrier = [bool(row["trait_barrier"]) for row in rows]

    rho, rho_p = _perm_p_spearman(mismatch, rates, permutations, seed)
    diff, diff_p = _perm_p_mean_diff(rates, barrier, permutations, seed + 1)

    barrier_rates = [v for v, b in zip(rates, barrier) if b]
    accessible_rates = [v for v, b in zip(rates, barrier) if not b]

    group_summary = {}
    for group in ("hummingbird", "flowerpiercer"):
        sub = [row for row in rows if row["bird_group"] == group]
        if sub:
            group_summary[group] = {
                "pair_site_n": len(sub),
                "mean_robbery_rate": _mean([float(row["robbery_rate"]) for row in sub]),
            }

    site_summary = _site_difference_summary(rows, permutations=permutations, seed=seed + 2)
    min_interaction_sensitivity = _min_interaction_sensitivity(
        rows,
        permutations=permutations,
        seed=seed,
    )

    return {
        "analysis_name": "aubert_zenodo_all_ecuador_access_barrier_extension",
        "pair_site_n": len(rows),
        "barrier_pair_sites": len(barrier_rates),
        "accessible_pair_sites": len(accessible_rates),
        "mean_robbery_rate_barrier": _mean(barrier_rates),
        "mean_robbery_rate_accessible": _mean(accessible_rates),
        "median_robbery_rate_barrier": _median(barrier_rates),
        "median_robbery_rate_accessible": _median(accessible_rates),
        "barrier_minus_accessible_mean_rate": diff,
        "barrier_mean_difference_permutation_p": diff_p,
        "mismatch_spearman_rho": rho,
        "mismatch_spearman_permutation_p": rho_p,
        "bird_group_summary": group_summary,
        "site_difference": site_summary,
        "min_interaction_sensitivity": min_interaction_sensitivity,
        "permutations": permutations,
        "seed": seed,
        "trait_definition": {
            "flower_tube": "site-specific mean Tubelength in cm; species mean fallback",
            "bird_bill": "species mean culmen_length in mm divided by 10 to cm",
            "mismatch": "log(flower_tube_cm / culmen_cm)",
            "barrier": "mismatch > 0 (flower tube longer than bill)",
        },
        "claim_boundary": (
            "Independent all-18-site EPHI Zenodo extension, not an exact replication of "
            "Aubert et al. 2026. Pair-site robbery rates are the inferential units. "
            "Associations do not establish causal floral defence."
        ),
    }


def run(output: str | Path, permutations: int = 9999) -> dict[str, object]:
    tables = {key: _read(_download(name)) for key, name in FILES.items()}
    rows, audit = build_pair_site_rows(
        tables["interactions"], tables["cameras"], tables["plants"], tables["birds"]
    )
    result = summarize_pair_sites(rows, permutations=permutations)
    result["audit"] = audit
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    parser.add_argument("--permutations", type=int, default=9999)
    args = parser.parse_args()
    print(json.dumps(run(args.output, args.permutations), indent=2, sort_keys=True))
