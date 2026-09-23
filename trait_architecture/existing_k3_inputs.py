"""Canonical fingerprints for the two existing networks entering k=3."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

RECEIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "empirical"
    / "floral_defence_selectivity"
    / "EXISTING_K3_INPUT_FINGERPRINTS_V1.json"
)
READY_STATUS = "CANONICAL_PUBLIC_INPUTS_FROZEN"
PLACEHOLDER = "REQUIRED_BEFORE_MERGE"


def stable_json_sha256(payload: object) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load_canonical_fingerprints(path: str | Path = RECEIPT_PATH) -> dict[str, object]:
    receipt = json.loads(Path(path).read_text(encoding="utf-8"))
    if receipt.get("receipt") != "BITA_EXISTING_K3_INPUT_FINGERPRINTS_V1":
        raise ValueError("WRONG_EXISTING_K3_FINGERPRINT_RECEIPT")
    if receipt.get("status") != READY_STATUS:
        raise ValueError("EXISTING_K3_FINGERPRINTS_NOT_FROZEN")

    networks = receipt.get("networks")
    if not isinstance(networks, dict):
        raise ValueError("EXISTING_K3_FINGERPRINT_NETWORKS_MISSING")

    for key in ("sakhalkar", "aubert_ephi"):
        entry = networks.get(key)
        if not isinstance(entry, dict):
            raise ValueError(f"EXISTING_K3_FINGERPRINT_ENTRY_MISSING:{key}")
        digest = str(entry.get("stable_json_sha256", "")).strip().lower()
        if digest == PLACEHOLDER or len(digest) != 64:
            raise ValueError(f"EXISTING_K3_FINGERPRINT_INVALID:{key}")
        try:
            int(digest, 16)
        except ValueError as exc:
            raise ValueError(f"EXISTING_K3_FINGERPRINT_INVALID:{key}") from exc
        units = entry.get("analysis_units")
        if not isinstance(units, int) or units <= 0:
            raise ValueError(f"EXISTING_K3_ANALYSIS_UNITS_INVALID:{key}")
        doi = str(entry.get("source_doi", "")).strip()
        if not doi:
            raise ValueError(f"EXISTING_K3_SOURCE_DOI_MISSING:{key}")
    return receipt


def validate_existing_network_payloads(
    sakhalkar_points: list[dict[str, object]],
    aubert_rows: list[dict[str, object]],
    *,
    receipt_path: str | Path = RECEIPT_PATH,
) -> dict[str, object]:
    receipt = load_canonical_fingerprints(receipt_path)
    checks: dict[str, object] = {}
    failures: list[str] = []

    payloads = {
        "sakhalkar": sakhalkar_points,
        "aubert_ephi": aubert_rows,
    }

    for key, payload in payloads.items():
        expected = receipt["networks"][key]
        digest = stable_json_sha256(payload)
        units = len(payload)
        digest_match = digest == expected["stable_json_sha256"]
        units_match = units == expected["analysis_units"]
        checks[key] = {
            "analysis_units": units,
            "expected_analysis_units": expected["analysis_units"],
            "analysis_units_match": units_match,
            "stable_json_sha256": digest,
            "expected_stable_json_sha256": expected["stable_json_sha256"],
            "stable_json_match": digest_match,
            "source_doi": expected["source_doi"],
        }
        if not units_match:
            failures.append(f"canonical_analysis_units_mismatch:{key}")
        if not digest_match:
            failures.append(f"canonical_stable_digest_mismatch:{key}")

    return {
        "status": "CANONICAL_EXISTING_K3_INPUTS_MATCH" if not failures else "CANONICAL_EXISTING_K3_INPUTS_MISMATCH",
        "checks": checks,
        "failures": failures,
    }
