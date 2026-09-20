"""Reproduce Letter statistics from the DOI-archive analysis tables only."""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

from scripts.analyze_aubert2026_zenodo_extension import summarize_pair_sites
from scripts.analyze_joint_access_routing import summarize_joint
from scripts.analyze_sakhalkar2023_network import _permutation_p, _spearman
from scripts.analyze_sakhalkar2023_trait_routing import fit_source_model_set

SAKHALKAR_SEED = 20260919
JOINT_SEED = 20260920


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _optional_float(value: str) -> float | None:
    text = str(value).strip()
    if text == "":
        return None
    number = float(text)
    if not math.isfinite(number):
        raise ValueError(f"non-finite archive value: {value!r}")
    return number


def load_sakhalkar(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in _read_csv(path):
        rows.append({
            "route_balance": float(row["route_balance"]),
            "tube_length": _optional_float(row["tube_length"]),
            "tube_width": _optional_float(row["tube_width"]),
            "brightness": _optional_float(row["brightness"]),
            "shape": row["shape"],
        })
    return rows


def load_aubert(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in _read_csv(path):
        rows.append({
            "site": row["site_id"],
            "bird_group": row["bird_group"],
            "n_interactions": int(row["n_interactions"]),
            "robbery_rate": float(row["robbery_rate"]),
            "mismatch_log_t_over_b": float(row["mismatch_log_t_over_b"]),
            "trait_barrier": row["trait_barrier"].strip().lower() == "true",
        })
    return rows


def reproduce(input_dir: Path, *, permutations: int = 9999) -> dict[str, object]:
    sakh_rows = load_sakhalkar(input_dir / "sakhalkar_species_analysis.csv")
    aubert_rows = load_aubert(input_dir / "aubert_ephi_pair_site_analysis.csv")

    sx = [float(row["tube_length"]) for row in sakh_rows if row["tube_length"] is not None]
    sy = [float(row["route_balance"]) for row in sakh_rows if row["tube_length"] is not None]
    s_rho = _spearman(sx, sy)
    s_p = _permutation_p(
        sx,
        sy,
        s_rho,
        permutations,
        seed=SAKHALKAR_SEED,
    )

    sakh_points = [
        {
            "tube_length": float(row["tube_length"]),
            "balance": float(row["route_balance"]),
        }
        for row in sakh_rows
        if row["tube_length"] is not None
    ]

    return {
        "archive_schema": "BITA_ACCESS_ROUTING_LETTER_ARCHIVE_REPRODUCTION_V1",
        "sakhalkar": {
            "n_species": len(sakh_points),
            "spearman_rho": s_rho,
            "permutation_p_two_sided": s_p,
            "multitrait": fit_source_model_set(
                sakh_rows,
                permutations=permutations,
                seed=SAKHALKAR_SEED,
            ),
        },
        "aubert_ephi": summarize_pair_sites(
            aubert_rows,
            permutations=permutations,
            seed=SAKHALKAR_SEED,
        ),
        "joint": summarize_joint(
            sakh_points,
            aubert_rows,
            permutations=permutations,
            seed=JOINT_SEED,
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--permutations", type=int, default=9999)
    args = parser.parse_args()

    result = reproduce(args.input_dir, permutations=args.permutations)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
