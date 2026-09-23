"""Compute canonical fingerprints for the two existing k=3 network inputs.

This is a provenance utility. It rebuilds the exact Sakhalkar and Aubert/EPHI
analysis rows from their frozen public source DOIs, serializes them with the
same stable-content contract used by the confirmatory runner, and emits a
machine-readable fingerprint receipt.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.analyze_joint_access_routing import build_public_inputs
from scripts.audit_sakhalkar2023_zenodo import ARCHIVE_MD5 as SAKHALKAR_ARCHIVE_MD5
from scripts.analyze_aubert2026_zenodo_extension import FILE_MD5 as AUBERT_FILE_MD5
from trait_architecture.existing_k3_inputs import canonical_stable_json_sha256

RECEIPT = "BITA_EXISTING_K3_INPUT_FINGERPRINTS_V1"
SOURCES = {
    "sakhalkar": "10.5281/zenodo.8398202",
    "aubert_ephi": "10.5281/zenodo.14185547",
}


def fingerprint_rows(
    sakhalkar_points: list[dict[str, float | str]],
    aubert_rows: list[dict[str, float | str | bool | int]],
) -> dict[str, object]:
    return {
        "receipt": RECEIPT,
        "networks": {
            "sakhalkar": {
                "analysis_units": len(sakhalkar_points),
                "canonical_stable_json_sha256": canonical_stable_json_sha256(
                    "sakhalkar",
                    sakhalkar_points,
                ),
                "source_doi": SOURCES["sakhalkar"],
            },
            "aubert_ephi": {
                "analysis_units": len(aubert_rows),
                "canonical_stable_json_sha256": canonical_stable_json_sha256(
                    "aubert_ephi",
                    aubert_rows,
                ),
                "source_doi": SOURCES["aubert_ephi"],
            },
        },
        "source_file_integrity": {
            "sakhalkar": {
                "SaileeSakhalkar/cheaters-among-pollinators-ecosphere-v1.0.0.zip": {
                    "md5": SAKHALKAR_ARCHIVE_MD5,
                }
            },
            "aubert_ephi": {
                name: {"md5": digest}
                for name, digest in sorted(AUBERT_FILE_MD5.items())
            },
        },
        "canonicalization": {
            "sakhalkar": "sort exact tube_length/balance/route_class rows",
            "aubert_ephi": (
                "deterministically relabel sites while preserving site partition, "
                "then sort all exact scientific fields"
            ),
            "numeric_quantization": "none",
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
