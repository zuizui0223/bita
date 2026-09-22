"""Load and validate the frozen two-network Letter analysis archive for k=3.

The real third-network production analysis must not rebuild the existing insect
and bird networks from live public downloads. Instead it consumes the exact
analysis-ready tables already exported for the Ecology Letters Letter and checks
their observed network effects against the committed frozen k=2 receipt.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.analyze_joint_access_routing import (
    _center_within_group,
    _pearson,
    _rankdata,
    combine_rhos_equal_network,
)
from scripts.reproduce_access_routing_archive import load_aubert, load_sakhalkar

MODE = "FROZEN_LETTER_ANALYSIS_ARCHIVE_V1"
EXPECTED_ARCHIVE_SCHEMA = "BITA_ACCESS_ROUTING_LETTER_ARCHIVE_V1"
EXPECTED_SAKHALKAR_UNITS = 57
EXPECTED_AUBERT_UNITS = 1378
EXPECTED_AUBERT_SITES = 18
SAKHALKAR_DOI = "10.5281/zenodo.8398202"
AUBERT_EPHI_DOI = "10.5281/zenodo.14185547"


def _sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _finite_float(value: object, label: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc
    if not math.isfinite(number):
        raise ValueError(f"{label} must be finite")
    return number


def _assert_close(actual: float, expected: object, label: str) -> None:
    target = _finite_float(expected, label)
    if not math.isclose(actual, target, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError(
            f"FROZEN_K2_MISMATCH:{label}: actual={actual!r} expected={target!r}"
        )


def observed_k2_effects(
    sakhalkar_points: list[dict[str, float | str]],
    aubert_rows: list[dict[str, float | str | bool | int]],
) -> dict[str, object]:
    if len(sakhalkar_points) != EXPECTED_SAKHALKAR_UNITS:
        raise ValueError(
            f"FROZEN_SAKHALKAR_UNIT_COUNT_MISMATCH:{len(sakhalkar_points)}"
        )
    if len(aubert_rows) != EXPECTED_AUBERT_UNITS:
        raise ValueError(
            f"FROZEN_AUBERT_UNIT_COUNT_MISMATCH:{len(aubert_rows)}"
        )

    sx = [float(row["tube_length"]) for row in sakhalkar_points]
    sy = [float(row["balance"]) for row in sakhalkar_points]
    ax = [float(row["mismatch_log_t_over_b"]) for row in aubert_rows]
    ay = [float(row["robbery_rate"]) for row in aubert_rows]
    sites = [str(row["site"]) for row in aubert_rows]

    if len(set(sites)) != EXPECTED_AUBERT_SITES:
        raise ValueError(
            f"FROZEN_AUBERT_SITE_COUNT_MISMATCH:{len(set(sites))}"
        )

    sx_rank = _rankdata(sx)
    sy_rank = _rankdata(sy)
    ax_rank = _rankdata(ax)
    ay_rank = _rankdata(ay)

    r_s = _pearson(sx_rank, sy_rank)
    ax_centered = _center_within_group(ax_rank, sites)
    ay_centered = _center_within_group(ay_rank, sites)
    r_a = _pearson(ax_centered, ay_centered)
    r_a_global = _pearson(ax_rank, ay_rank)

    if not all(math.isfinite(value) for value in (r_s, r_a, r_a_global)):
        raise ValueError("frozen existing-network effect is not finite")

    r_j2 = combine_rhos_equal_network([r_s, r_a])
    return {
        "sakhalkar_rho": r_s,
        "aubert_site_adjusted_rho": r_a,
        "aubert_global_rho": r_a_global,
        "joint_equal_network_fisher_z_rho": r_j2,
        "sakhalkar_units": len(sakhalkar_points),
        "aubert_units": len(aubert_rows),
        "aubert_sites": len(set(sites)),
    }


def validate_against_frozen_result(
    observed: dict[str, object],
    frozen: dict[str, object],
) -> None:
    if int(frozen.get("network_count", -1)) != 2:
        raise ValueError("FROZEN_K2_RESULT_NETWORK_COUNT_NOT_TWO")

    effects = frozen.get("network_effects", {})
    if not isinstance(effects, dict):
        raise ValueError("FROZEN_K2_RESULT_EFFECTS_MISSING")
    sakh = effects.get("sakhalkar", {})
    aubert = effects.get("aubert_ephi", {})
    if not isinstance(sakh, dict) or not isinstance(aubert, dict):
        raise ValueError("FROZEN_K2_RESULT_EFFECTS_MISSING")

    if int(sakh.get("n_units", -1)) != int(observed["sakhalkar_units"]):
        raise ValueError("FROZEN_K2_MISMATCH:sakhalkar_n_units")
    if int(aubert.get("n_units", -1)) != int(observed["aubert_units"]):
        raise ValueError("FROZEN_K2_MISMATCH:aubert_n_units")
    if int(aubert.get("site_count", -1)) != int(observed["aubert_sites"]):
        raise ValueError("FROZEN_K2_MISMATCH:aubert_site_count")

    _assert_close(
        float(observed["sakhalkar_rho"]),
        sakh.get("rho"),
        "sakhalkar_rho",
    )
    _assert_close(
        float(observed["aubert_site_adjusted_rho"]),
        aubert.get("rho"),
        "aubert_site_adjusted_rho",
    )
    _assert_close(
        float(observed["aubert_global_rho"]),
        aubert.get("rho_global_descriptive"),
        "aubert_global_rho",
    )
    _assert_close(
        float(observed["joint_equal_network_fisher_z_rho"]),
        frozen.get("joint_equal_network_fisher_z_rho"),
        "joint_equal_network_fisher_z_rho",
    )

    if frozen.get("network_direction_concordance") != "2_of_2_positive":
        raise ValueError("FROZEN_K2_DIRECTION_RECEIPT_CHANGED")


def load_frozen_existing_networks(
    archive_dir: str | Path,
    frozen_result_json: str | Path,
) -> tuple[
    list[dict[str, float | str]],
    list[dict[str, float | str | bool | int]],
    dict[str, object],
]:
    root = Path(archive_dir)
    sakh_path = root / "sakhalkar_species_analysis.csv"
    aubert_path = root / "aubert_ephi_pair_site_analysis.csv"
    manifest_path = root / "archive_manifest.json"
    frozen_path = Path(frozen_result_json)

    for path, label in (
        (sakh_path, "sakhalkar analysis table"),
        (aubert_path, "aubert analysis table"),
        (manifest_path, "archive manifest"),
        (frozen_path, "frozen k2 result"),
    ):
        if not path.is_file():
            raise ValueError(f"FROZEN_EXISTING_NETWORK_INPUT_MISSING:{label}:{path}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("archive_schema") != EXPECTED_ARCHIVE_SCHEMA:
        raise ValueError("FROZEN_EXISTING_NETWORK_ARCHIVE_SCHEMA_MISMATCH")

    tables = manifest.get("analysis_tables", {})
    if not isinstance(tables, dict):
        raise ValueError("FROZEN_EXISTING_NETWORK_ARCHIVE_TABLE_RECEIPT_MISSING")
    if int(tables.get(sakh_path.name, -1)) != EXPECTED_SAKHALKAR_UNITS:
        raise ValueError("FROZEN_EXISTING_NETWORK_MANIFEST_SAKHALKAR_COUNT_MISMATCH")
    if int(tables.get(aubert_path.name, -1)) != EXPECTED_AUBERT_UNITS:
        raise ValueError("FROZEN_EXISTING_NETWORK_MANIFEST_AUBERT_COUNT_MISMATCH")

    source_data = manifest.get("source_data", {})
    if not isinstance(source_data, dict):
        raise ValueError("FROZEN_EXISTING_NETWORK_SOURCE_RECEIPT_MISSING")
    if source_data.get("sakhalkar_2023_zenodo_doi") != SAKHALKAR_DOI:
        raise ValueError("FROZEN_EXISTING_NETWORK_SAKHALKAR_DOI_MISMATCH")
    if source_data.get("aubert_ephi_zenodo_mirror_doi") != AUBERT_EPHI_DOI:
        raise ValueError("FROZEN_EXISTING_NETWORK_AUBERT_DOI_MISMATCH")

    sakh_rows = load_sakhalkar(sakh_path)
    aubert_loaded = load_aubert(aubert_path)

    sakhalkar_points: list[dict[str, float | str]] = []
    for row in sakh_rows:
        tube = row.get("tube_length")
        if tube is None:
            continue
        sakhalkar_points.append(
            {
                "tube_length": float(tube),
                "balance": float(row["route_balance"]),
            }
        )

    aubert_rows: list[dict[str, float | str | bool | int]] = [
        {
            "site": str(row["site"]),
            "bird_group": str(row["bird_group"]),
            "n_interactions": int(row["n_interactions"]),
            "robbery_rate": float(row["robbery_rate"]),
            "mismatch_log_t_over_b": float(row["mismatch_log_t_over_b"]),
            "trait_barrier": bool(row["trait_barrier"]),
        }
        for row in aubert_loaded
    ]

    observed = observed_k2_effects(sakhalkar_points, aubert_rows)
    frozen = json.loads(frozen_path.read_text(encoding="utf-8"))
    validate_against_frozen_result(observed, frozen)

    receipt = {
        "receipt": "BITA_FROZEN_EXISTING_NETWORK_ARCHIVE_V1",
        "status": "FROZEN_EXISTING_NETWORKS_VALIDATED",
        "input_mode": MODE,
        "archive_schema": EXPECTED_ARCHIVE_SCHEMA,
        "source_dois": {
            "sakhalkar": SAKHALKAR_DOI,
            "aubert_ephi": AUBERT_EPHI_DOI,
        },
        "files": {
            "sakhalkar_species_analysis.csv": {
                "sha256": _sha256(sakh_path),
                "rows": len(sakhalkar_points),
            },
            "aubert_ephi_pair_site_analysis.csv": {
                "sha256": _sha256(aubert_path),
                "rows": len(aubert_rows),
            },
            "archive_manifest.json": {
                "sha256": _sha256(manifest_path),
            },
            "frozen_k2_result.json": {
                "filename": frozen_path.name,
                "sha256": _sha256(frozen_path),
            },
        },
        "observed_k2_effects": observed,
        "frozen_k2_validation": "PASS",
        "claim_boundary": (
            "The two pre-existing networks are loaded from the exact Letter analysis-ready "
            "archive and checked against the committed frozen k=2 effect receipt. No public "
            "dataset is redownloaded or reselected during the real k=3 run."
        ),
    }
    return sakhalkar_points, aubert_rows, receipt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive_dir")
    parser.add_argument("frozen_result_json")
    parser.add_argument("--output")
    args = parser.parse_args()

    _sakh, _aubert, receipt = load_frozen_existing_networks(
        args.archive_dir,
        args.frozen_result_json,
    )
    payload = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
