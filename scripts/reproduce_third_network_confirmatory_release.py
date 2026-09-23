"""Offline replay of a packaged third-network confirmatory release.

The release must contain:
- confirmatory_bundle/
- frozen_inputs/

No public-data download is performed. The exact Sakhalkar and Aubert/EPHI rows
are loaded from the confirmatory bundle.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import tempfile
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.analyze_joint_access_routing_k3 import summarize_joint_k3
from scripts.analyze_third_access_routing_network import (
    load_analysis_units,
    summarize_third_network,
)
from scripts.build_third_access_routing_units import run as build_units
from scripts.verify_third_network_confirmatory_bundle import (
    VERIFIED_STATUS,
    verify,
)
from trait_architecture.serialization import canonicalize_generated_floats

RECEIPT = "BITA_THIRD_NETWORK_RELEASE_REPRODUCTION_V1"


def _load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _finite_close(a: object, b: object, *, tol: float = 1e-15) -> bool:
    try:
        left = float(a)
        right = float(b)
    except (TypeError, ValueError):
        return False
    return (
        math.isfinite(left)
        and math.isfinite(right)
        and math.isclose(left, right, rel_tol=0.0, abs_tol=tol)
    )


def reproduce(release_dir: str | Path) -> dict[str, object]:
    root = Path(release_dir)
    bundle = root / "confirmatory_bundle"
    source = root / "frozen_inputs"

    canonical_path = root / "protocol" / "EXISTING_K3_INPUT_FINGERPRINTS_V1.json"
    verification = verify(
        bundle,
        source_dir=source,
        canonical_fingerprint_path=(
            canonical_path if canonical_path.is_file() else None
        ),
    )
    if verification["status"] != VERIFIED_STATUS:
        raise ValueError(
            "PACKAGED_CONFIRMATORY_BUNDLE_INVALID: "
            + ",".join(str(x) for x in verification.get("failures", []))
        )

    manifest = _load(bundle / "input_freeze_manifest.json")
    if not isinstance(manifest, dict):
        raise ValueError("PACKAGED_INPUT_FREEZE_MANIFEST_INVALID")

    files = manifest.get("files", {})
    if not isinstance(files, dict):
        raise ValueError("PACKAGED_INPUT_FREEZE_FILES_MISSING")

    def source_path(key: str) -> Path:
        entry = files.get(key, {})
        if not isinstance(entry, dict):
            raise ValueError(f"PACKAGED_SOURCE_ENTRY_MISSING:{key}")
        filename = str(entry.get("filename", "")).strip()
        if not filename:
            raise ValueError(f"PACKAGED_SOURCE_FILENAME_MISSING:{key}")
        return source / filename

    original_third = _load(bundle / "third_network_result.json")
    original_joint = _load(bundle / "joint_access_routing_k3_result.json")
    if not isinstance(original_third, dict) or not isinstance(original_joint, dict):
        raise ValueError("PACKAGED_RESULT_JSON_INVALID")

    third_effect = original_third.get("effect", {})
    if not isinstance(third_effect, dict):
        raise ValueError("PACKAGED_THIRD_EFFECT_MISSING")

    third_permutations = int(third_effect["permutations"])
    third_seed = int(third_effect["seed"])
    joint_permutations = int(original_joint["permutations"])
    joint_seed = int(original_joint["seed"])

    with tempfile.TemporaryDirectory(prefix="bita-third-replay-") as tmp:
        tmp_root = Path(tmp)
        units_csv = tmp_root / "analysis_units.csv"
        audit_json = tmp_root / "unit_build_audit.json"

        build_units(
            source_path("events"),
            source_path("plant_traits"),
            source_path("mammal_traits"),
            bundle / "input_freeze_manifest.json",
            units_csv,
            audit_json,
        )

        third_rows = load_analysis_units(units_csv)
        replay_third = canonicalize_generated_floats(
            summarize_third_network(
                third_rows,
                permutations=third_permutations,
                seed=third_seed,
            )
        )

        sakhalkar = _load(bundle / "existing_network_sakhalkar_input.json")
        aubert = _load(bundle / "existing_network_aubert_ephi_input.json")
        if not isinstance(sakhalkar, list) or not isinstance(aubert, list):
            raise ValueError("PACKAGED_EXISTING_NETWORK_INPUT_INVALID")

        replay_joint = canonicalize_generated_floats(
            summarize_joint_k3(
                sakhalkar,
                aubert,
                third_rows,
                permutations=joint_permutations,
                seed=joint_seed,
            )
        )

    original_third_effect = original_third.get("effect", {})
    third_matches = {
        "rho": _finite_close(
            replay_third["effect"]["rho_site_adjusted_rank"],
            original_third_effect.get("rho_site_adjusted_rank"),
        ),
        "p": _finite_close(
            replay_third["effect"]["permutation_p_two_sided"],
            original_third_effect.get("permutation_p_two_sided"),
        ),
        "gate": replay_third.get("gate") == original_third.get("gate"),
    }

    joint_matches = {
        "network_count": replay_joint.get("network_count") == original_joint.get("network_count"),
        "network_effects": replay_joint.get("network_effects") == original_joint.get("network_effects"),
        "rho": _finite_close(
            replay_joint["joint_equal_network_fisher_z_rho"],
            original_joint.get("joint_equal_network_fisher_z_rho"),
        ),
        "p": _finite_close(
            replay_joint["joint_permutation_p_two_sided"],
            original_joint.get("joint_permutation_p_two_sided"),
        ),
        "direction": replay_joint.get("network_direction_concordance")
        == original_joint.get("network_direction_concordance"),
    }

    all_match = all(third_matches.values()) and all(joint_matches.values())
    return {
        "receipt": RECEIPT,
        "status": "REPRODUCTION_MATCH" if all_match else "REPRODUCTION_MISMATCH",
        "bundle_verification_status": verification["status"],
        "source_recheck_mode": verification["source_recheck_mode"],
        "canonical_existing_inputs_status": verification[
            "canonical_existing_inputs_status"
        ],
        "third_network_matches": third_matches,
        "joint_k3_matches": joint_matches,
        "third_network_recomputed": replay_third,
        "joint_k3_recomputed": replay_joint,
        "claim_boundary": (
            "This replay verifies scientific-output reproducibility from the packaged "
            "frozen inputs and exact existing-network rows. It does not alter claims."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("release_dir")
    parser.add_argument("--output")
    args = parser.parse_args()

    result = reproduce(args.release_dir)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")

    if result["status"] != "REPRODUCTION_MATCH":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
