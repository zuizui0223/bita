"""Compute canonical fingerprints for the two existing k=3 network inputs.

This is a provenance utility. It rebuilds the exact Sakhalkar and Aubert/EPHI
analysis rows from their frozen public source DOIs, serializes them with the
same stable-content contract used by the confirmatory runner, and emits a
machine-readable fingerprint receipt.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from scripts.analyze_joint_access_routing import build_public_inputs

RECEIPT = "BITA_EXISTING_K3_INPUT_FINGERPRINTS_V1"
SOURCES = {
    "sakhalkar": "10.5281/zenodo.8398202",
    "aubert_ephi": "10.5281/zenodo.14185547",
}


def stable_json_bytes(payload: object) -> bytes:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def stable_json_sha256(payload: object) -> str:
    return hashlib.sha256(stable_json_bytes(payload)).hexdigest()


def fingerprint_rows(
    sakhalkar_points: list[dict[str, float | str]],
    aubert_rows: list[dict[str, float | str | bool | int]],
) -> dict[str, object]:
    return {
        "receipt": RECEIPT,
        "networks": {
            "sakhalkar": {
                "analysis_units": len(sakhalkar_points),
                "stable_json_sha256": stable_json_sha256(sakhalkar_points),
                "source_doi": SOURCES["sakhalkar"],
            },
            "aubert_ephi": {
                "analysis_units": len(aubert_rows),
                "stable_json_sha256": stable_json_sha256(aubert_rows),
                "source_doi": SOURCES["aubert_ephi"],
            },
        },
        "serialization": {
            "json_sort_keys": True,
            "json_separators": [",", ":"],
            "ensure_ascii": False,
            "allow_nan": False,
        },
        "claim_boundary": (
            "This receipt identifies the exact existing-network analysis rows used "
            "for future k=3 integration. It is provenance only and does not alter "
            "the current k=2 scientific result."
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
