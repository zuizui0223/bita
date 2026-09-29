"""Sensitivity audit for Aubert/EPHI piercing missingness and species dependence.

This audit leaves the frozen complete-case analysis untouched and adds two checks:

1. Rebuild pair-site robbery rates after treating explicitly missing piercing codes
   ("NA", "N/A", or blank) as legitimate interactions ("no"), as suggested by
   the source metadata. Distinct non-missing states such as "maybe", "thief",
   and "not_interacting" remain excluded.
2. Re-test the barrier contrast with one paired difference per plant species
   (and, separately, per bird species). A label-swap/sign-flip permutation acts
   on whole species-level differences rather than pair-site rows, so repeated
   sites for the same species cannot create pseudo-replicated significance.

Source species identifiers are used only in memory to define clusters and are
not emitted in the aggregate JSON output.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.analyze_aubert2026_zenodo_extension import (
    FILES,
    SEED,
    _as_float,
    _download,
    _mean,
    _median,
    _perm_p_spearman,
    _read,
    summarize_pair_sites,
)

MISSING_CODES = {"", "na", "n/a"}


def _piercing_value(value: object, *, missing_as_no: bool) -> bool | None:
    """Return True=robbing, False=legitimate, None=exclude."""
    if value is None:
        status = ""
    else:
        status = str(value).strip().lower()
    if status == "yes":
        return True
    if status == "no":
        return False
    if missing_as_no and status in MISSING_CODES:
        return False
    return None


def build_pair_site_rows_policy(
    interactions: list[dict[str, str]],
    cameras: list[dict[str, str]],
    plants: list[dict[str, str]],
    birds: list[dict[str, str]],
    *,
    missing_as_no: bool,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    """Build pair-site rows while retaining species keys only for clustering."""
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
    raw_status_counts: Counter[str] = Counter()
    target_taxon_rows = 0
    included_status_rows = 0
    resolved_interactions = 0
    trait_matched_interactions = 0

    for row in interactions:
        family = str(row.get("hummingbird_family", "")).strip()
        genus = str(row.get("hummingbird_genus", "")).strip()
        if not (family == "Trochilidae" or genus == "Diglossa"):
            continue

        target_taxon_rows += 1
        raw = row.get("piercing", "")
        status_name = "" if raw is None else str(raw).strip().lower()
        raw_status_counts[status_name or "<blank>"] += 1
        robbed = _piercing_value(raw, missing_as_no=missing_as_no)
        if robbed is None:
            continue
        included_status_rows += 1

        bird_species = str(row.get("hummingbird_species", "")).strip()
        wp = str(row.get("waypoint", "")).strip()
        if not bird_species or wp not in camera_map:
            continue
        site, plant_species = camera_map[wp]
        resolved_interactions += 1

        tube_vals = plant_values.get((site, plant_species)) or plant_global.get(plant_species)
        bill_vals = bird_values.get(bird_species)
        if not tube_vals or not bill_vals:
            continue
        tube_cm = _mean(tube_vals)
        culmen_cm = _mean(bill_vals) / 10.0
        if tube_cm <= 0 or culmen_cm <= 0:
            continue

        trait_matched_interactions += 1
        mismatch = math.log(tube_cm / culmen_cm)
        key = (site, bird_species, plant_species)
        item = grouped.setdefault(
            key,
            {
                "site": site,
                "bird_species": bird_species,
                "plant_species": plant_species,
                "bird_group": "flowerpiercer" if genus == "Diglossa" else "hummingbird",
                "mismatch_log_t_over_b": mismatch,
                "trait_barrier": mismatch > 0,
                "robbing": 0,
                "legitimate": 0,
            },
        )
        if robbed:
            item["robbing"] = int(item["robbing"]) + 1
        else:
            item["legitimate"] = int(item["legitimate"]) + 1

    rows_out: list[dict[str, object]] = []
    for item in grouped.values():
        rob = int(item["robbing"])
        leg = int(item["legitimate"])
        total = rob + leg
        if total <= 0:
            continue
        rows_out.append(
            {
                "site": str(item["site"]),
                "bird_species": str(item["bird_species"]),
                "plant_species": str(item["plant_species"]),
                "bird_group": str(item["bird_group"]),
                "n_interactions": total,
                "robbery_count": rob,
                "legitimate_count": leg,
                "robbery_rate": rob / total,
                "mismatch_log_t_over_b": float(item["mismatch_log_t_over_b"]),
                "trait_barrier": bool(item["trait_barrier"]),
            }
        )

    audit: dict[str, object] = {
        "missing_as_no": missing_as_no,
        "target_taxon_rows_before_piercing_filter": target_taxon_rows,
        "included_by_piercing_policy": included_status_rows,
        "resolved_target_interactions": resolved_interactions,
        "trait_matched_interactions": trait_matched_interactions,
        "pair_site_rows": len(rows_out),
        "sites": len({str(row["site"]) for row in rows_out}),
        "plant_species_clusters": len({str(row["plant_species"]) for row in rows_out}),
        "bird_species_clusters": len({str(row["bird_species"]) for row in rows_out}),
        "raw_piercing_status_counts": dict(sorted(raw_status_counts.items())),
    }
    return rows_out, audit


def _binomial_two_sided_sign_p(positive: int, total: int) -> float | None:
    if total <= 0:
        return None
    k = min(positive, total - positive)
    tail = sum(math.comb(total, i) for i in range(k + 1)) / (2 ** total)
    return min(1.0, 2 * tail)


def cluster_label_swap_summary(
    rows: list[dict[str, object]],
    *,
    cluster_key: str,
    permutations: int,
    seed: int,
) -> dict[str, object]:
    """One paired barrier-minus-accessible difference per species cluster.

    Under the null, swapping the two condition labels for a whole cluster flips
    that cluster's difference. The permutation therefore acts on species-level
    units, not on the repeated pair-site rows inside a species.
    """
    by_cluster: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_cluster[str(row[cluster_key])].append(row)

    differences: list[float] = []
    for cluster_rows in by_cluster.values():
        barrier = [
            float(row["robbery_rate"])
            for row in cluster_rows
            if bool(row["trait_barrier"])
        ]
        accessible = [
            float(row["robbery_rate"])
            for row in cluster_rows
            if not bool(row["trait_barrier"])
        ]
        if barrier and accessible:
            differences.append(_mean(barrier) - _mean(accessible))

    if not differences:
        return {
            "cluster_key": cluster_key,
            "eligible_clusters": 0,
            "positive_clusters": 0,
            "mean_cluster_difference": None,
            "median_cluster_difference": None,
            "sign_test_p": None,
            "cluster_label_swap_permutation_p": None,
        }

    observed = _mean(differences)
    nonzero = [value for value in differences if value != 0]
    positive = sum(value > 0 for value in nonzero)
    sign_p = _binomial_two_sided_sign_p(positive, len(nonzero))

    rng = random.Random(seed)
    extreme = 0
    for _ in range(permutations):
        permuted = [
            value if rng.getrandbits(1) else -value
            for value in differences
        ]
        statistic = _mean(permuted)
        if abs(statistic) >= abs(observed) - 1e-15:
            extreme += 1

    return {
        "cluster_key": cluster_key,
        "eligible_clusters": len(differences),
        "nonzero_clusters": len(nonzero),
        "positive_clusters": positive,
        "mean_cluster_difference": observed,
        "median_cluster_difference": _median(differences),
        "sign_test_p": sign_p,
        "cluster_label_swap_permutation_p": (extreme + 1) / (permutations + 1),
        "permutations": permutations,
    }



def cluster_aggregated_rho_summary(
    rows: list[dict[str, object]],
    *,
    cluster_key: str,
    permutations: int,
    seed: int,
) -> dict[str, object]:
    """Aggregate repeated pair-sites once per species before rank inference."""
    by_cluster: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_cluster[str(row[cluster_key])].append(row)

    points: list[tuple[float, float]] = []
    for cluster_rows in by_cluster.values():
        mismatch = _mean([float(row["mismatch_log_t_over_b"]) for row in cluster_rows])
        robbery = _mean([float(row["robbery_rate"]) for row in cluster_rows])
        points.append((mismatch, robbery))

    if len(points) < 3:
        return {
            "cluster_key": cluster_key,
            "n_clusters": len(points),
            "rho": None,
            "permutation_p_two_sided": None,
        }

    x = [point[0] for point in points]
    y = [point[1] for point in points]
    rho, p = _perm_p_spearman(x, y, permutations, seed)
    return {
        "cluster_key": cluster_key,
        "n_clusters": len(points),
        "rho": rho,
        "permutation_p_two_sided": p,
        "permutations": permutations,
        "aggregation": "unweighted mean across pair-site units within species",
    }



def _rankdata_local(values: list[float]) -> list[float]:
    """Average ranks with 1-based ranking; local helper avoids extra dependencies."""
    indexed = sorted(enumerate(values), key=lambda item: item[1])
    out = [0.0] * len(values)
    i = 0
    while i < len(indexed):
        j = i + 1
        while j < len(indexed) and indexed[j][1] == indexed[i][1]:
            j += 1
        rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            out[indexed[k][0]] = rank
        i = j
    return out


def _pearson_local(x: list[float], y: list[float]) -> float:
    if len(x) != len(y) or len(x) < 2:
        return float("nan")
    mx = _mean(x)
    my = _mean(y)
    dx = [value - mx for value in x]
    dy = [value - my for value in y]
    den_x = math.sqrt(sum(value * value for value in dx))
    den_y = math.sqrt(sum(value * value for value in dy))
    if den_x == 0 or den_y == 0:
        return float("nan")
    return sum(a * b for a, b in zip(dx, dy)) / (den_x * den_y)


def bird_within_species_continuous_summary(
    rows: list[dict[str, object]],
    *,
    permutations: int,
    seed: int,
) -> dict[str, object]:
    """Continuous within-bird route-switching check at bird x plant grain.

    Pair-site rows are first averaged across sites for each bird x plant dyad.
    Within each bird species, mismatch and robbery are ranked and centered.
    The pooled statistic is the Pearson correlation of these centered within-bird
    ranks. Its null shuffles robbery ranks only within each bird species.

    We also report one Spearman rho per bird species where both variables vary.
    Those bird-specific rhos are a descriptive species-balanced complement; the
    sign test does not treat pair-site rows as independent replicates.
    """
    by_dyad: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        key = (str(row["bird_species"]), str(row["plant_species"]))
        by_dyad[key].append(row)

    by_bird: dict[str, list[tuple[float, float]]] = defaultdict(list)
    for (bird, _plant), dyad_rows in by_dyad.items():
        mismatch = _mean(
            [float(row["mismatch_log_t_over_b"]) for row in dyad_rows]
        )
        robbery = _mean([float(row["robbery_rate"]) for row in dyad_rows])
        by_bird[bird].append((mismatch, robbery))

    groups: list[dict[str, object]] = []
    bird_rhos: list[float] = []
    mismatch_spans: list[float] = []
    for points in by_bird.values():
        if len(points) < 3:
            continue
        x = [point[0] for point in points]
        y = [point[1] for point in points]
        mismatch_spans.append(max(x) - min(x))
        if len(set(x)) < 2 or len(set(y)) < 2:
            continue
        xr = _rankdata_local(x)
        yr = _rankdata_local(y)
        xmean = _mean(xr)
        ymean = _mean(yr)
        xc = [value - xmean for value in xr]
        yc = [value - ymean for value in yr]
        rho = _pearson_local(xr, yr)
        if math.isfinite(rho):
            bird_rhos.append(rho)
        groups.append(
            {
                "x_centered": xc,
                "y_centered": yc,
            }
        )

    pooled_x: list[float] = []
    pooled_y: list[float] = []
    for group in groups:
        pooled_x.extend(group["x_centered"])
        pooled_y.extend(group["y_centered"])

    observed = _pearson_local(pooled_x, pooled_y)
    if not math.isfinite(observed):
        pooled_p = None
    else:
        rng = random.Random(seed)
        extreme = 0
        for _ in range(permutations):
            permuted_y: list[float] = []
            for group in groups:
                local = list(group["y_centered"])
                rng.shuffle(local)
                permuted_y.extend(local)
            permuted = _pearson_local(pooled_x, permuted_y)
            if math.isfinite(permuted) and abs(permuted) >= abs(observed) - 1e-15:
                extreme += 1
        pooled_p = (extreme + 1) / (permutations + 1)

    nonzero_rhos = [rho for rho in bird_rhos if rho != 0]
    positive_rhos = sum(rho > 0 for rho in nonzero_rhos)
    sign_p = _binomial_two_sided_sign_p(positive_rhos, len(nonzero_rhos))

    return {
        "aggregation": (
            "bird x plant dyads averaged across sites; ranks computed and centered "
            "within bird species before pooling"
        ),
        "bird_species_total": len(by_bird),
        "bird_species_with_at_least_3_plant_dyads": sum(
            len(points) >= 3 for points in by_bird.values()
        ),
        "eligible_bird_species_continuous": len(groups),
        "bird_plant_dyads_in_pooled_test": len(pooled_x),
        "pooled_within_bird_rank_rho": observed if math.isfinite(observed) else None,
        "within_bird_permutation_p_two_sided": pooled_p,
        "bird_specific_rho_count": len(bird_rhos),
        "bird_specific_positive_rho_count": positive_rhos,
        "bird_specific_median_rho": _median(bird_rhos) if bird_rhos else None,
        "bird_specific_sign_test_p": sign_p,
        "median_within_bird_mismatch_span": (
            _median(mismatch_spans) if mismatch_spans else None
        ),
        "permutations": permutations,
        "claim_boundary": (
            "This is a within-bird behavioral sensitivity, not a crossed "
            "bird-and-plant random-effects model. Bird x plant dyads are averaged "
            "across sites before inference."
        ),
    }


def summarize_policy(
    rows: list[dict[str, object]],
    *,
    audit: dict[str, object],
    permutations: int,
    seed: int,
) -> dict[str, object]:
    native = summarize_pair_sites(rows, permutations=permutations, seed=seed)
    return {
        "audit": audit,
        "native_pair_site_summary": native,
        "plant_species_cluster_check": cluster_label_swap_summary(
            rows,
            cluster_key="plant_species",
            permutations=permutations,
            seed=seed + 300,
        ),
        "plant_species_rho_check": cluster_aggregated_rho_summary(
            rows,
            cluster_key="plant_species",
            permutations=permutations,
            seed=seed + 350,
        ),
        "bird_species_cluster_check": cluster_label_swap_summary(
            rows,
            cluster_key="bird_species",
            permutations=permutations,
            seed=seed + 400,
        ),
        "bird_species_rho_check": cluster_aggregated_rho_summary(
            rows,
            cluster_key="bird_species",
            permutations=permutations,
            seed=seed + 450,
        ),
        "bird_within_species_continuous_check": bird_within_species_continuous_summary(
            rows,
            permutations=permutations,
            seed=seed + 500,
        ),
    }


def _comparison(complete: dict[str, object], missing: dict[str, object]) -> dict[str, object]:
    a = complete["native_pair_site_summary"]
    b = missing["native_pair_site_summary"]
    assert isinstance(a, dict) and isinstance(b, dict)
    keys = [
        "pair_site_n",
        "mean_robbery_rate_barrier",
        "mean_robbery_rate_accessible",
        "barrier_minus_accessible_mean_rate",
        "mismatch_spearman_rho",
    ]
    out: dict[str, object] = {}
    for key in keys:
        av = a[key]
        bv = b[key]
        out[key] = {
            "complete_case": av,
            "missing_as_no": bv,
            "change": (float(bv) - float(av)) if av is not None and bv is not None else None,
        }
    out["direction_preserved"] = (
        float(a["barrier_minus_accessible_mean_rate"]) > 0
        and float(b["barrier_minus_accessible_mean_rate"]) > 0
        and float(a["mismatch_spearman_rho"]) > 0
        and float(b["mismatch_spearman_rho"]) > 0
    )
    return out


def run(output: str | Path, *, permutations: int = 9999) -> dict[str, object]:
    tables = {key: _read(_download(name)) for key, name in FILES.items()}

    complete_rows, complete_audit = build_pair_site_rows_policy(
        tables["interactions"],
        tables["cameras"],
        tables["plants"],
        tables["birds"],
        missing_as_no=False,
    )
    missing_rows, missing_audit = build_pair_site_rows_policy(
        tables["interactions"],
        tables["cameras"],
        tables["plants"],
        tables["birds"],
        missing_as_no=True,
    )

    complete = summarize_policy(
        complete_rows,
        audit=complete_audit,
        permutations=permutations,
        seed=SEED,
    )
    missing = summarize_policy(
        missing_rows,
        audit=missing_audit,
        permutations=permutations,
        seed=SEED + 1000,
    )

    result = {
        "analysis_name": "aubert_ephi_missingness_and_species_dependence_sensitivity",
        "source_metadata_rule": (
            "EPHI metadata states that piercing=NA means not specified and is most probably 'no' "
            "because some observers filled the field only when a bird was piercing."
        ),
        "status_policy": {
            "complete_case": "include only piercing=yes/no",
            "missing_as_no": (
                "include piercing=yes/no and recode explicit missing codes NA/N/A/blank as no; "
                "retain exclusion of maybe, thief, not_interacting, and other non-binary states"
            ),
        },
        "complete_case": complete,
        "missing_as_no": missing,
        "comparison": _comparison(complete, missing),
        "claim_boundary": (
            "The species-cluster checks are sensitivity analyses that make plant or bird species "
            "the unit of label swapping. They address repeated pair-site observations but are not "
            "a crossed-random-effects model and do not establish causality."
        ),
        "guardrail": "Aggregate output only; source species identifiers are not emitted.",
        "permutations": permutations,
    }

    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    parser.add_argument("--permutations", type=int, default=9999)
    args = parser.parse_args()
    print(json.dumps(run(args.output, permutations=args.permutations), indent=2, sort_keys=True))
