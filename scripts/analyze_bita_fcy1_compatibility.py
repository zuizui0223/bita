"""Source-pinned Fcy1 positive-pair compatibility graph (Després et al. 2024).

Input is a *selected positive* pair table after multiple laboratory filters.
Edges do not represent an exhaustive genotype x genotype viability assay.
Repeated colonies and cross identities are not independent evolutionary origins.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "empirical/trait_architecture_history/despres2024_indep_crosses_source.csv"
READOUT = SOURCE.with_name("despres2024_compatibility_readout.json")
SOURCE_BLOB_SHA = "36839a3fd2eb05a521a070d11e60cde1748a682e"


def load_pairs(path: Path = SOURCE) -> list[dict]:
    raw = path.read_bytes()
    git_blob_sha = hashlib.sha1(
        b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw
    ).hexdigest()
    if path.resolve() == SOURCE.resolve() and git_blob_sha != SOURCE_BLOB_SHA:
        raise ValueError("author source Git blob SHA mismatch")
    with path.open(newline="", encoding="utf-8") as stream:
        input_rows = list(csv.DictReader(stream))
    records = []
    for r in input_rows:
        try:
            predicted = r["freq_predicted"]
            records.append({
                "source_index": int(r[""]),
                "allele_1": r["allele_1"],
                "allele_2": r["allele_2"],
                "n_observed": int(r["n_observed"]),
                "n_indep_crosses": int(r["n_indep_crosses"]),
                "freq_predicted_log2": float(predicted) if predicted else None,
            })
        except (TypeError, ValueError, KeyError) as exc:
            raise ValueError("malformed source table row") from exc
    return records


def _graph(rows: list[dict], cutoff: int) -> dict:
    adjacency: dict[str, set[str]] = {}
    included = [r for r in rows if r["n_indep_crosses"] >= cutoff]
    for r in included:
        a, b = r["allele_1"], r["allele_2"]
        adjacency.setdefault(a, set()).add(b)
        adjacency.setdefault(b, set()).add(a)

    visited: set[str] = set()
    component_sizes = []
    for first in sorted(adjacency):
        if first in visited:
            continue
        todo = [first]
        visited.add(first)
        size = 0
        while todo:
            v = todo.pop()
            size += 1
            for u in adjacency[v]:
                if u not in visited:
                    visited.add(u)
                    todo.append(u)
        component_sizes.append(size)
    component_sizes.sort(reverse=True)
    top = sorted(
        ((n, len(neighbors)) for n, neighbors in adjacency.items()),
        key=lambda pair: (-pair[1], pair[0]),
    )[:10]
    return {
        "cutoff_min_distinct_cross_identifiers": cutoff,
        "edges": len(included),
        "vertices": len(adjacency),
        "component_sizes": component_sizes,
        "largest_component_vertices": component_sizes[0] if component_sizes else 0,
        "top_alleles_by_distinct_positive_partners": [
            {"allele": allele, "partners": degree} for allele, degree in top
        ],
        "top5_endpoint_fraction": (
            sum(len(adjacency[n]) for n, _ in top[:5])/(2*len(included))
            if included else None
        ),
    }


def _average_ranks(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=values.__getitem__)
    ranks = [0.0] * len(values)
    i = 0
    while i < len(values):
        j = i+1
        while j < len(values) and values[order[j]] == values[order[i]]:
            j += 1
        avg_rank = (i+1+j)/2
        for k in range(i, j):
            ranks[order[k]] = avg_rank
        i = j
    return ranks


def _descriptive_spearman(x: list[float], y: list[float]) -> float:
    if len(x) != len(y) or len(x) < 3:
        raise ValueError("insufficient common-support pair records")
    a, b = _average_ranks(x), _average_ranks(y)
    ma, mb = sum(a)/len(a), sum(b)/len(b)
    numerator = sum((u-ma)*(v-mb) for u, v in zip(a, b))
    da = sum((u-ma)**2 for u in a)
    db = sum((v-mb)**2 for v in b)
    if da == 0 or db == 0:
        raise ValueError("constant rank vector")
    return numerator / math.sqrt(da*db)


def analyze(rows: list[dict]) -> dict:
    if not rows:
        raise ValueError("empty positive-pair table")
    pairs: set[tuple[str, str]] = set()
    for r in rows:
        a, b = r["allele_1"], r["allele_2"]
        if not a or not b or a == b:
            raise ValueError("invalid or same allele self-loop")
        try:
            n_observed = r["n_observed"]
            n_cross = r["n_indep_crosses"]
            if (type(n_observed) is not int or type(n_cross) is not int
                or n_observed < 1 or n_cross < 1):
                raise ValueError("counts must be positive integers")
            if n_cross > n_observed:
                raise ValueError("independent-cross count exceeds observations")
        except KeyError as exc:
            raise ValueError("missing source count") from exc
        pair = tuple(sorted((a, b)))
        if pair in pairs:
            raise ValueError("duplicate unordered positive-pair key")
        pairs.add(pair)
        pred = r["freq_predicted_log2"]
        if pred is not None and not math.isfinite(pred):
            raise ValueError("nonfinite predicted input abundance")
    if [r["source_index"] for r in rows] != list(range(len(rows))):
        raise ValueError("original source index is not contiguous")
    finite = [r for r in rows if r["freq_predicted_log2"] is not None]
    alleles = {x for a, b in pairs for x in (a, b)}
    total_positives = sum(r["n_observed"] for r in rows)
    total_cross = sum(r["n_indep_crosses"] for r in rows)
    if total_cross > total_positives:
        raise ValueError("cross identifiers cannot exceed selected positive observations")
    return {
        "study_doi": "10.1126/science.ado5719",
        "source_repository": "Landrylab/Despres_et_al_2024",
        "source_path": "validations_analysis/indep_crosses.csv",
        "source_blob_sha": SOURCE_BLOB_SHA,
        "source_data_level": "AUTHOR_PROCESSED_POSITIVE_SELECTED_CROSSING_TABLE",
        "positive_pair_edges": len(rows),
        "positive_unique_alleles": len(alleles),
        "positive_colony_observations": total_positives,
        "positive_distinct_codon_cross_identifiers": total_cross,
        "pairs_with_ge2_source_cross_identifiers": sum(
            r["n_indep_crosses"] >= 2 for r in rows
        ),
        "pairs_with_one_source_cross_identifier": sum(
            r["n_indep_crosses"] == 1 for r in rows
        ),
        "positive_graph_thresholds": {
            f"ge{cut}": _graph(rows, cut) for cut in (1, 2, 3, 5)
        },
        "frequency_finite_n": len(finite),
        "frequency_missing_n": len(rows) - len(finite),
        "descriptive_spearman_frequency_vs_cross_recovery": _descriptive_spearman(
            [r["freq_predicted_log2"] for r in finite],
            [r["n_indep_crosses"] for r in finite]
        ),
        "no_unselected_negative_pair_denominator": True,
        "independent_evolutionary_origins_estimated": False,
        "poolable_study_effects_added": 0,
        "meta_analysis_performed": False,
        "claim_boundary": (
            "Positive selected complementing pairs are not a random sample of "
            "all possible two-allele pairs. 613 distinct codon-by-cross recovery "
            "identifiers are not 613 independent evolutionary origins; 887 is "
            "positive colony observations, not all colonies screened. "
            "The graph is conditional on selection, enrichment and filters. "
            "The repeated-pair subgraph does not estimate an unbiased natural "
            "heteromer benefit, true mutation rate, K(u), fixation, "
            "or an ancestral architecture's evolutionary cause. "
            "Source abundance correlations are descriptive on positive pairs."
        ),
    }


def main() -> None:
    result = analyze(load_pairs())
    READOUT.write_text(json.dumps(result, indent=2, ensure_ascii=False)
                       + "\n", encoding="utf-8")
    print(json.dumps({
        "readout": str(READOUT),
        "positive_pairs": result["positive_pair_edges"],
        "codon_cross_identities": result["positive_distinct_codon_cross_identifiers"],
        "positive_network": result["positive_graph_thresholds"]["ge1"]["component_sizes"],
        "recurrent_ge2_network": result["positive_graph_thresholds"]["ge2"]["component_sizes"],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
