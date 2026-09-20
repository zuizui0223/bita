"""BITA-specific reanalysis of Sakhalkar et al. 2023 network data."""

from __future__ import annotations

import io
import json
import math
import random
import statistics
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from trait_architecture.numerics import rankdata as _shared_rankdata, spearman as _shared_spearman
from scripts.audit_sakhalkar2023_zenodo import _download, read_xlsx_sheet_rows

WORKBOOK_BASENAME = "cheaters_visitation_and_trait_data.xlsx"
SEED = 20260919


def _as_float(value: str) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _rankdata(values: list[float]) -> list[float]:
    """Backward-compatible alias to the shared tie-aware implementation."""

    return _shared_rankdata(values)


def _spearman(x: list[float], y: list[float]) -> float:
    return _shared_spearman(x, y)

def _permutation_p(
    x: list[float],
    y: list[float],
    observed: float,
    permutations: int,
    *,
    seed: int,
) -> float | None:
    if permutations <= 0 or not math.isfinite(observed):
        return None
    rng = random.Random(seed)
    shuffled = list(y)
    extreme = 0
    for _ in range(permutations):
        rng.shuffle(shuffled)
        rho = _spearman(x, shuffled)
        if math.isfinite(rho) and abs(rho) >= abs(observed) - 1e-12:
            extreme += 1
    return (extreme + 1) / (permutations + 1)


def _find_workbook(archive_bytes: bytes) -> bytes:
    with zipfile.ZipFile(io.BytesIO(archive_bytes)) as archive:
        matches = [
            item
            for item in archive.infolist()
            if not item.is_dir() and Path(item.filename).name == WORKBOOK_BASENAME
        ]
        if len(matches) != 1:
            raise ValueError(f"expected one {WORKBOOK_BASENAME}, found {len(matches)}")
        return archive.read(matches[0])



def species_route_points(
    raw_visits: list[dict[str, str]],
    traits: list[dict[str, str]],
) -> list[dict[str, float | str]]:
    """Return anonymous species-level tube-length / cheating-mode points.

    Species identifiers are intentionally omitted so downstream figure artifacts
    cannot expose raw species rows. The aggregation rules match analyze_rows().
    """
    visits = [
        row
        for row in raw_visits
        if str(row.get("behavior", "")).strip().lower() != "visiting"
    ]

    frequency: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    visited_species: set[str] = set()
    for row in visits:
        spcode = str(row.get("spcode", "")).strip()
        behavior = str(row.get("behavior", "")).strip().lower()
        value = _as_float(str(row.get("freq_fm_per_species", "")).strip())
        if not spcode:
            continue
        visited_species.add(spcode)
        if behavior and value is not None:
            frequency[spcode][behavior] += value

    tube_length_by_species: dict[str, float] = {}
    for row in traits:
        spcode = str(row.get("spcode", "")).strip()
        tube_length = _as_float(str(row.get("tube_length", "")).strip())
        if spcode and tube_length is not None:
            tube_length_by_species[spcode] = tube_length

    points: list[dict[str, float | str]] = []
    for sp in sorted(visited_species.intersection(tube_length_by_species)):
        rob = frequency[sp].get("robbing", 0.0)
        thief = frequency[sp].get("thieving", 0.0)
        total = rob + thief
        if total <= 0:
            continue
        if rob > 0 and thief == 0:
            route_class = "robber_only"
        elif thief > 0 and rob == 0:
            route_class = "thief_only"
        else:
            route_class = "mixed"
        points.append(
            {
                "tube_length": tube_length_by_species[sp],
                "balance": (rob - thief) / total,
                "route_class": route_class,
            }
        )
    return points

def analyze_rows(
    raw_visits: list[dict[str, str]],
    traits: list[dict[str, str]],
    *,
    permutations: int = 9999,
    seed: int = SEED,
) -> dict[str, object]:
    """Aggregate visit rows to plant species before testing cheating-mode routing."""
    visits = [
        row
        for row in raw_visits
        if str(row.get("behavior", "")).strip().lower() != "visiting"
    ]
    behavior_counts = Counter(
        str(row.get("behavior", "")).strip().lower()
        for row in visits
        if str(row.get("behavior", "")).strip()
    )

    frequency: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    visited_species: set[str] = set()
    for row in visits:
        spcode = str(row.get("spcode", "")).strip()
        behavior = str(row.get("behavior", "")).strip().lower()
        value = _as_float(str(row.get("freq_fm_per_species", "")).strip())
        if not spcode:
            continue
        visited_species.add(spcode)
        if behavior and value is not None:
            frequency[spcode][behavior] += value

    tube_length_by_species: dict[str, float] = {}
    for row in traits:
        spcode = str(row.get("spcode", "")).strip()
        tube_length = _as_float(str(row.get("tube_length", "")).strip())
        if spcode and tube_length is not None:
            tube_length_by_species[spcode] = tube_length

    trait_matched = sorted(visited_species.intersection(tube_length_by_species))
    species_with_robbing = {
        sp for sp in visited_species if frequency[sp].get("robbing", 0.0) > 0
    }
    species_with_thieving = {
        sp for sp in visited_species if frequency[sp].get("thieving", 0.0) > 0
    }

    cheated_species = [
        sp
        for sp in trait_matched
        if frequency[sp].get("robbing", 0.0)
        + frequency[sp].get("thieving", 0.0)
        > 0
    ]
    tube_length = [tube_length_by_species[sp] for sp in cheated_species]
    route_balance: list[float] = []
    for sp in cheated_species:
        rob = frequency[sp].get("robbing", 0.0)
        thief = frequency[sp].get("thieving", 0.0)
        route_balance.append((rob - thief) / (rob + thief))

    rho = _spearman(tube_length, route_balance)
    p_value = _permutation_p(
        tube_length,
        route_balance,
        rho,
        permutations,
        seed=seed,
    )

    robber_only = [
        tube_length_by_species[sp]
        for sp in trait_matched
        if frequency[sp].get("robbing", 0.0) > 0
        and frequency[sp].get("thieving", 0.0) == 0
    ]
    thief_only = [
        tube_length_by_species[sp]
        for sp in trait_matched
        if frequency[sp].get("thieving", 0.0) > 0
        and frequency[sp].get("robbing", 0.0) == 0
    ]

    return {
        "raw_cheater_rows": len(raw_visits),
        "analysis_visit_rows": len(visits),
        "behavior_counts": dict(sorted(behavior_counts.items())),
        "visited_species": len(visited_species),
        "trait_matched_species": len(trait_matched),
        "species_with_robbing": len(species_with_robbing),
        "species_with_thieving": len(species_with_thieving),
        "species_with_any_cheating_and_tube_length": len(cheated_species),
        "tube_length_cheating_mode_balance": {
            "definition": (
                "(robbing_frequency-thieving_frequency)/"
                "(robbing_frequency+thieving_frequency)"
            ),
            "n_species": len(cheated_species),
            "spearman_rho": None if not math.isfinite(rho) else rho,
            "permutation_p_two_sided": p_value,
            "permutations": permutations,
            "seed": seed,
        },
        "median_tube_length_robber_only": (
            statistics.median(robber_only) if robber_only else None
        ),
        "median_tube_length_thief_only": (
            statistics.median(thief_only) if thief_only else None
        ),
        "guardrail": (
            "Species-level aggregate reanalysis. No raw visit or species rows are emitted."
        ),
    }


def analyze_workbook(
    workbook_bytes: bytes,
    *,
    permutations: int = 9999,
    seed: int = SEED,
) -> dict[str, object]:
    raw_visits = read_xlsx_sheet_rows(workbook_bytes, "cheater_data")
    traits = read_xlsx_sheet_rows(workbook_bytes, "plant_traits")
    return analyze_rows(
        raw_visits,
        traits,
        permutations=permutations,
        seed=seed,
    )


def run(output_path: str | Path, *, permutations: int = 9999) -> dict[str, object]:
    workbook = _find_workbook(_download())
    result = analyze_workbook(workbook, permutations=permutations)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    parser.add_argument("--permutations", type=int, default=9999)
    args = parser.parse_args()
    result = run(args.output, permutations=args.permutations)
    print(json.dumps(result, indent=2, sort_keys=True))
