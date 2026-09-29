"""Post-publication independent-network replication using Case et al. (2026).

This lane is deliberately NOT confirmatory: the Case paper and Dryad metadata
already disclose the direction of the bill-flower / nectar-robbing relationship.
The analysis therefore asks a narrower question: does this independently sampled
Hawaiian bird-flower network satisfy the pre-existing data-quality gates needed to
contribute a third network-level rank association on the same access-routing scale?

No gate is relaxed to admit this dataset. The original third-fauna preregistration
still excludes Aves; this module reports a separate POST_PUBLICATION_REPLICATION
status and may only be used to describe k=3 independent-network recurrence, not a
three-fauna confirmatory test.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import random
import tempfile
import urllib.request
import zipfile
from collections import defaultdict
from pathlib import Path
import sys
import subprocess

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.analyze_joint_access_routing import combine_rhos_equal_network
from scripts.analyze_joint_access_routing_species_robust import (
    build_existing_network_species_inputs,
)
from scripts.analyze_sakhalkar2023_network import _pearson, _rankdata

CASE_DOI = "10.5061/dryad.sj3tx96kr"
DRYAD_BASE = "https://datadryad.org"
CASE_DATASET_API_URL = (
    DRYAD_BASE
    + "/api/v2/datasets/doi%3A10.5061%2Fdryad.sj3tx96kr"
)
CASE_MEMBER = "Case_FE_2026_Analysis_2.csv"
SEED = 20260929

MIN_UNITS = 30
MIN_VISITOR_SPECIES = 5
MIN_PLANT_SPECIES = 5


def _mean(values: list[float]) -> float:
    if not values:
        raise ValueError("mean requires data")
    return sum(values) / len(values)


def _as_float(value: object) -> float | None:
    try:
        out = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    return out if math.isfinite(out) else None


def _url_json(url: str) -> dict[str, object]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "BITA-public-replication/1.0",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return json.loads(response.read().decode("utf-8"))


def _absolute_dryad_url(href: str) -> str:
    if href.startswith("http://") or href.startswith("https://"):
        return href
    return DRYAD_BASE + href


def discover_case_public_file_url() -> tuple[str, dict[str, object]]:
    """Resolve the public Case CSV via Dryad metadata plus file_stream."""
    dataset = _url_json(CASE_DATASET_API_URL)
    links = dataset.get("_links", {})
    if not isinstance(links, dict):
        raise ValueError("Dryad dataset metadata lacks _links")
    version_link = links.get("stash:version", {})
    if not isinstance(version_link, dict) or not version_link.get("href"):
        raise ValueError("Dryad dataset metadata lacks stash:version href")
    version = _url_json(_absolute_dryad_url(str(version_link["href"])))
    version_links = version.get("_links", {})
    files_href = None
    if isinstance(version_links, dict):
        files_link = version_links.get("stash:files", {})
        if isinstance(files_link, dict):
            files_href = files_link.get("href")
    if not files_href:
        version_id = version.get("id")
        if version_id is None:
            raise ValueError("Dryad version metadata lacks files link and id")
        files_href = f"/api/v2/versions/{version_id}/files"

    files_payload = _url_json(_absolute_dryad_url(str(files_href)))
    embedded = files_payload.get("_embedded", {})
    entries = embedded.get("stash:files", []) if isinstance(embedded, dict) else []
    matches = [
        entry
        for entry in entries
        if isinstance(entry, dict) and str(entry.get("path", "")) == CASE_MEMBER
    ]
    if len(matches) != 1:
        raise ValueError(
            f"expected exactly one public {CASE_MEMBER}, found {len(matches)}"
        )
    entry = matches[0]
    entry_links = entry.get("_links", {})
    self_href = None
    if isinstance(entry_links, dict):
        self_link = entry_links.get("self", {})
        if isinstance(self_link, dict):
            self_href = self_link.get("href")
    if not self_href:
        raise ValueError("Dryad file metadata lacks self href")

    import re
    match = re.search(r"/api/v2/files/(\d+)$", str(self_href))
    if match is None:
        raise ValueError(f"cannot recover Dryad file id from {self_href}")
    file_id = match.group(1)
    return (
        f"{DRYAD_BASE}/stash/downloads/file_stream/{file_id}",
        {
            "dryad_version_id": version.get("id"),
            "dryad_file_id": int(file_id),
            "dryad_file_size": entry.get("size"),
            "dryad_digest": entry.get("digest"),
            "dryad_digest_type": entry.get("digestType"),
        },
    )


def download_case_file(path: str | Path) -> tuple[Path, dict[str, object]]:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    url, provenance = discover_case_public_file_url()
    completed = subprocess.run(
        [
            "curl",
            "--fail",
            "--location",
            "--silent",
            "--show-error",
            "--retry",
            "3",
            "--retry-all-errors",
            "--user-agent",
            "Mozilla/5.0 (compatible; BITA-public-replication/1.0)",
            "--referer",
            "https://datadryad.org/",
            "--output",
            str(target),
            url,
        ],
        check=False,
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "Dryad public file_stream download failed: "
            + (completed.stderr.strip() or f"curl exit {completed.returncode}")
        )
    if not target.is_file() or target.stat().st_size == 0:
        raise ValueError("downloaded Case CSV is empty")
    probe = target.read_bytes()[:256]
    provenance["downloaded_size_bytes"] = target.stat().st_size
    provenance["downloaded_prefix_repr"] = repr(probe)
    provenance["public_file_stream_url"] = url
    return target, provenance


def read_case_rows(source: str | Path) -> list[dict[str, str]]:
    path = Path(source)
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as zf:
            members = [name for name in zf.namelist() if name.endswith(CASE_MEMBER)]
            if len(members) != 1:
                raise ValueError(
                    f"expected exactly one {CASE_MEMBER}, found {len(members)}"
                )
            text = zf.read(members[0]).decode("utf-8-sig")
    else:
        text = path.read_text(encoding="utf-8-sig")
    return list(csv.DictReader(io.StringIO(text)))


def normalize_case_units(
    rows: list[dict[str, str]],
) -> tuple[list[dict[str, object]], dict[str, object]]:
    required = {
        "plant_species",
        "bird_species",
        "N",
        "nectar_robbing",
        "source",
        "culmen",
        "flower_length",
        "bill_minus_flower",
    }
    if not rows:
        raise ValueError("Case interaction table is empty")
    observed_columns = list(rows[0].keys())
    missing = required - set(rows[0])
    if missing:
        raise ValueError(
            "Case table missing required columns: "
            f"{sorted(missing)}; observed_columns={observed_columns!r}"
        )

    grouped: dict[tuple[str, str, str], list[dict[str, float]]] = defaultdict(list)
    invalid_rows = 0
    mismatch_disagreement_rows = 0

    for row in rows:
        plant = str(row["plant_species"]).strip()
        bird = str(row["bird_species"]).strip()
        source = str(row["source"]).strip()
        n = _as_float(row["N"])
        robbery = _as_float(row["nectar_robbing"])
        culmen = _as_float(row["culmen"])
        flower = _as_float(row["flower_length"])
        reported = _as_float(row["bill_minus_flower"])

        if (
            not plant
            or not bird
            or not source
            or n is None
            or n <= 0
            or robbery is None
            or not 0 <= robbery <= 1
            or culmen is None
            or culmen <= 0
            or flower is None
            or flower <= 0
            or reported is None
        ):
            invalid_rows += 1
            continue

        access_constraint = flower - culmen
        if not math.isclose(
            reported,
            culmen - flower,
            rel_tol=0.0,
            abs_tol=1e-6,
        ):
            mismatch_disagreement_rows += 1
            continue

        grouped[(source, bird, plant)].append(
            {
                "N": n,
                "robbery": robbery,
                "access_constraint": access_constraint,
            }
        )

    units: list[dict[str, object]] = []
    for (source, bird, plant), values in grouped.items():
        total_n = sum(item["N"] for item in values)
        robbery_count = sum(item["N"] * item["robbery"] for item in values)
        access_constraint = _mean(
            [item["access_constraint"] for item in values]
        )
        units.append(
            {
                "source": source,
                "bird_species": bird,
                "plant_species": plant,
                "n_interactions": total_n,
                "robbery_count": robbery_count,
                "legitimate_count": total_n - robbery_count,
                "robbery_rate": robbery_count / total_n,
                "access_constraint_flower_minus_bill_mm": access_constraint,
            }
        )

    audit = {
        "raw_rows": len(rows),
        "normalized_source_bird_plant_units": len(units),
        "duplicate_rows_collapsed": max(0, len(rows) - invalid_rows - mismatch_disagreement_rows - len(units)),
        "invalid_rows_excluded": invalid_rows,
        "bill_minus_flower_consistency_failures": mismatch_disagreement_rows,
        "bird_species": len({str(row["bird_species"]) for row in units}),
        "plant_species": len({str(row["plant_species"]) for row in units}),
        "sources": len({str(row["source"]) for row in units}),
        "total_interactions_N": sum(float(row["n_interactions"]) for row in units),
        "bypass_interactions_reconstructed": sum(float(row["robbery_count"]) for row in units),
        "legitimate_interactions_reconstructed": sum(float(row["legitimate_count"]) for row in units),
    }
    return units, audit


def aggregate_case_by_plant(
    units: list[dict[str, object]],
) -> list[dict[str, float]]:
    by_plant: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in units:
        by_plant[str(row["plant_species"])].append(row)

    points: list[dict[str, float]] = []
    for plant_rows in by_plant.values():
        points.append(
            {
                "access_constraint": _mean(
                    [
                        float(row["access_constraint_flower_minus_bill_mm"])
                        for row in plant_rows
                    ]
                ),
                "robbery_rate": _mean(
                    [float(row["robbery_rate"]) for row in plant_rows]
                ),
                "source_bird_plant_unit_n": float(len(plant_rows)),
            }
        )
    return points


def replication_gate(
    units: list[dict[str, object]],
    plant_points: list[dict[str, float]],
) -> dict[str, object]:
    birds = {str(row["bird_species"]) for row in units}
    plants = {str(row["plant_species"]) for row in units}
    mismatch = [
        float(row["access_constraint_flower_minus_bill_mm"]) for row in units
    ]
    total_bypass = sum(float(row["robbery_count"]) for row in units)
    total_legitimate = sum(float(row["legitimate_count"]) for row in units)
    checks = {
        "units_ge_30": len(units) >= MIN_UNITS,
        "visitor_species_ge_5": len(birds) >= MIN_VISITOR_SPECIES,
        "plant_species_ge_5": len(plants) >= MIN_PLANT_SPECIES,
        "nonzero_access_constraint_variation": len(set(mismatch)) >= 2,
        "contains_bypass_interactions": total_bypass > 0,
        "contains_legitimate_interactions": total_legitimate > 0,
        "plant_grain_points_ge_5": len(plant_points) >= MIN_PLANT_SPECIES,
    }
    return {
        "checks": checks,
        "passes_postpublication_replication_gate": all(checks.values()),
        "confirmatory_third_fauna_gate": False,
        "confirmatory_third_fauna_failure_reasons": [
            "visitor fauna is Aves, excluded by the frozen non-Insecta/non-Aves preregistration",
            "the published paper/Dryad metadata already disclose the relevant outcome direction",
        ],
    }


def _permutation_spearman(
    x: list[float],
    y: list[float],
    *,
    permutations: int,
    seed: int,
) -> tuple[float, float]:
    xr = _rankdata(x)
    yr = _rankdata(y)
    observed = _pearson(xr, yr)
    if not math.isfinite(observed):
        raise ValueError("Case network correlation is not finite")
    rng = random.Random(seed)
    shuffled = list(yr)
    extreme = 0
    for _ in range(permutations):
        rng.shuffle(shuffled)
        rho = _pearson(xr, shuffled)
        if abs(rho) >= abs(observed) - 1e-15:
            extreme += 1
    return observed, (extreme + 1) / (permutations + 1)


def summarize_case(
    units: list[dict[str, object]],
    *,
    permutations: int,
    seed: int,
) -> dict[str, object]:
    points = aggregate_case_by_plant(units)
    gate = replication_gate(units, points)
    result: dict[str, object] = {
        "analysis_status": "POST_PUBLICATION_REPLICATION",
        "source_doi": CASE_DOI,
        "source_file": CASE_MEMBER,
        "access_constraint_definition": "flower_length_mm - culmen_mm; larger means legitimate floral access is more constrained",
        "outcome_definition": "nectar_robbing proportion reported by Case et al. per source x bird x plant row",
        "primary_inferential_grain": "plant_species",
        "aggregation": "unweighted mean access constraint and robbery rate across normalized source x bird x plant units within plant species",
        "gate": gate,
        "n_plant_species_points": len(points),
        "claim_boundary": (
            "The Case paper publicly reports the direction of the trait-matching/nectar-robbing relationship. "
            "This analysis is therefore an independent post-publication network replication, not an outcome-blind "
            "confirmatory third-fauna test."
        ),
    }
    if gate["passes_postpublication_replication_gate"]:
        x = [point["access_constraint"] for point in points]
        y = [point["robbery_rate"] for point in points]
        rho, p = _permutation_spearman(
            x,
            y,
            permutations=permutations,
            seed=seed,
        )
        result["rho"] = rho
        result["permutation_p_two_sided"] = p
        result["permutations"] = permutations
    else:
        result["rho"] = None
        result["permutation_p_two_sided"] = None
    return result


def summarize_k3(
    case_points: list[dict[str, float]],
    *,
    permutations: int,
    seed: int,
) -> dict[str, object]:
    sakhalkar_points, aubert_points = build_existing_network_species_inputs()

    sx = [float(row["tube_length"]) for row in sakhalkar_points]
    sy = [float(row["balance"]) for row in sakhalkar_points]
    ax = [float(row["mismatch"]) for row in aubert_points]
    ay = [float(row["robbery_rate"]) for row in aubert_points]
    cx = [float(row["access_constraint"]) for row in case_points]
    cy = [float(row["robbery_rate"]) for row in case_points]

    sxr, syr = _rankdata(sx), _rankdata(sy)
    axr, ayr = _rankdata(ax), _rankdata(ay)
    cxr, cyr = _rankdata(cx), _rankdata(cy)

    observed = [
        _pearson(sxr, syr),
        _pearson(axr, ayr),
        _pearson(cxr, cyr),
    ]
    if not all(math.isfinite(value) for value in observed):
        raise ValueError("all three network correlations must be finite")
    joint = combine_rhos_equal_network(observed)

    rng_s = random.Random(seed)
    rng_a = random.Random(seed + 1)
    rng_c = random.Random(seed + 2)
    ps_y, pa_y, pc_y = list(syr), list(ayr), list(cyr)
    extreme = 0
    same_direction = 0
    for _ in range(permutations):
        rng_s.shuffle(ps_y)
        rng_a.shuffle(pa_y)
        rng_c.shuffle(pc_y)
        permuted = [
            _pearson(sxr, ps_y),
            _pearson(axr, pa_y),
            _pearson(cxr, pc_y),
        ]
        pj = combine_rhos_equal_network(permuted)
        if abs(pj) >= abs(joint) - 1e-15:
            extreme += 1
        if all(value > 0 for value in permuted):
            same_direction += 1

    return {
        "analysis_name": "joint_equal_network_access_routing_postpublication_k3",
        "analysis_status": "POST_PUBLICATION_REPLICATION_NOT_CONFIRMATORY_THIRD_FAUNA",
        "network_count": 3,
        "network_effects": {
            "sakhalkar_insects": {
                "n_units": len(sakhalkar_points),
                "unit": "plant_species",
                "rho": observed[0],
            },
            "aubert_ephi_birds": {
                "n_units": len(aubert_points),
                "unit": "plant_species",
                "rho": observed[1],
            },
            "case_hawaii_birds": {
                "n_units": len(case_points),
                "unit": "plant_species",
                "rho": observed[2],
            },
        },
        "joint_equal_network_fisher_z_rho": joint,
        "joint_permutation_p_two_sided": (extreme + 1) / (permutations + 1),
        "null_probability_all_three_positive": (same_direction + 1) / (permutations + 1),
        "network_direction_concordance": (
            f"{sum(value > 0 for value in observed)}_of_3_positive"
        ),
        "permutations": permutations,
        "seed": seed,
        "claim_boundary": (
            "This raises the number of independently sampled networks with a harmonized plant-species rank effect "
            "to three only as a post-publication replication synthesis. It does not satisfy the frozen third-fauna "
            "confirmatory gate because Case et al. is another bird network and its outcome direction was already public."
        ),
    }


def run(
    output: str | Path,
    *,
    case_zip: str | Path | None = None,
    permutations: int = 9999,
    seed: int = SEED,
    compute_k3: bool = True,
) -> dict[str, object]:
    source_provenance: dict[str, object] = {}
    if case_zip is None:
        with tempfile.TemporaryDirectory() as tmp:
            case_file, source_provenance = download_case_file(
                Path(tmp) / CASE_MEMBER
            )
            rows = read_case_rows(case_file)
    else:
        rows = read_case_rows(case_zip)

    units, audit = normalize_case_units(rows)
    plant_points = aggregate_case_by_plant(units)
    case_summary = summarize_case(
        units,
        permutations=permutations,
        seed=seed,
    )

    result: dict[str, object] = {
        "analysis_name": "case2026_hawaii_postpublication_access_routing_replication",
        "source": {
            "doi": CASE_DOI,
            "dataset_api_url": CASE_DATASET_API_URL,
            "file": CASE_MEMBER,
            "direction_exposed_before_analysis": True,
            **source_provenance,
        },
        "audit": audit,
        "case_network": case_summary,
        "guardrail": (
            "No outcome-blind confirmatory claim is licensed. The pre-existing non-Insecta/non-Aves third-fauna "
            "preregistration is unchanged."
        ),
    }

    gate = case_summary["gate"]
    assert isinstance(gate, dict)
    if compute_k3 and gate["passes_postpublication_replication_gate"]:
        result["postpublication_k3"] = summarize_k3(
            plant_points,
            permutations=permutations,
            seed=seed + 100,
        )
    else:
        result["postpublication_k3"] = None

    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    parser.add_argument("--case-zip")
    parser.add_argument("--permutations", type=int, default=9999)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--no-k3", action="store_true")
    args = parser.parse_args()
    result = run(
        args.output,
        case_zip=args.case_zip,
        permutations=args.permutations,
        seed=args.seed,
        compute_k3=not args.no_k3,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
