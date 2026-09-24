"""Rebuild and fingerprint the exact existing networks entering future k=3."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.analyze_joint_access_routing import build_public_inputs
from trait_architecture.existing_k3_inputs import canonical_stable_json_sha256

RECEIPT = "BITA_EXISTING_K3_INPUT_FINGERPRINT_CANDIDATE_V2"
SOURCES = {
    "sakhalkar": "10.5281/zenodo.8398202",
    "aubert_ephi": "10.5281/zenodo.14185547",
}


def fingerprint_rows(
    sakhalkar_points: list[dict[str, object]],
    aubert_rows: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "receipt": RECEIPT,
        "status": "CANDIDATE_REBUILT_FROM_FIXED_PUBLIC_SOURCES",
        "networks": {
            "sakhalkar": {
                "analysis_units": len(sakhalkar_points),
                "canonical_stable_json_sha256": canonical_stable_json_sha256(
                    "sakhalkar", sakhalkar_points
                ),
                "source_doi": SOURCES["sakhalkar"],
            },
            "aubert_ephi": {
                "analysis_units": len(aubert_rows),
                "canonical_stable_json_sha256": canonical_stable_json_sha256(
                    "aubert_ephi", aubert_rows
                ),
                "source_doi": SOURCES["aubert_ephi"],
            },
        },
        "canonicalization": {
            "sakhalkar": "sort exact k3 scientific fields; zero tube length retained",
            "aubert_ephi": (
                "discard arbitrary site labels; sort sites by the complete multiset "
                "of exact scientific rows; preserve site partition"
            ),
            "numeric_quantization": "none",
        },
        "claim_boundary": (
            "Candidate provenance receipt only. Commit the digest as canonical only "
            "after independent workflow rebuild and regression checks pass."
        ),
    }


def run(output: str | Path | None = None) -> dict[str, object]:
    sakhalkar_points, aubert_rows = build_public_inputs()
    result = fingerprint_rows(sakhalkar_points, aubert_rows)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if output is not None:
        path = Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload, encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()
    print(json.dumps(run(args.output), indent=2, sort_keys=True))
