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
