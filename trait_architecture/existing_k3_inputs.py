"""Canonical scientific-content fingerprints for the existing k=3 inputs.

Representation-only variation is removed without altering scientific values:
- Sakhalkar rows are sorted by the exact fields entering the k=3 analysis.
- Aubert/EPHI rows are the repaired plant-species analysis points. Row order
  is discarded while exact mismatch, robbery rate, and contributing pair-site
  count are preserved.
- No float rounding or quantization is applied.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

RECEIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "empirical"
    / "floral_defence_selectivity"
    / "EXISTING_K3_INPUT_FINGERPRINTS_V1.json"
)
READY_STATUS = "CANONICAL_PUBLIC_INPUTS_FROZEN"
MATCH_STATUS = "CANONICAL_EXISTING_K3_INPUTS_MATCH"
MISMATCH_STATUS = "CANONICAL_EXISTING_K3_INPUTS_MISMATCH"
PRODUCTION_INPUT_MODE = "PUBLIC_EXISTING_NETWORKS_FIXED_DOI_REBUILD"


def _stable_json(payload: object) -> bytes:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _stable_json_sha256(payload: object) -> str:
    return hashlib.sha256(_stable_json(payload)).hexdigest()


def _finite_float(value: object, label: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{label} must be numeric, not boolean")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{label} must be finite")
    return number


def canonicalize_sakhalkar(
    rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for row in rows:
        tube = _finite_float(row["tube_length"], "tube_length")
        balance = _finite_float(row["balance"], "balance")
        route_class = str(row.get("route_class", "")).strip()
        if not (-1.0 <= balance <= 1.0):
            raise ValueError("Sakhalkar balance must be within [-1,1]")
        expected_class = (
            "robber_only"
            if balance == 1.0
            else "thief_only"
            if balance == -1.0
            else "mixed"
        )
        if route_class != expected_class:
            raise ValueError("Sakhalkar route_class is inconsistent with balance")
        out.append(
            {
                "tube_length": tube,
                "balance": balance,
                "route_class": route_class,
            }
        )
    return sorted(
        out,
        key=lambda row: (
            float(row["tube_length"]),
            float(row["balance"]),
            str(row["route_class"]),
        ),
    )


def _aubert_scientific_row(row: dict[str, object]) -> dict[str, object]:
    mismatch = _finite_float(row["mismatch"], "mismatch")
    robbery_rate = _finite_float(row["robbery_rate"], "robbery_rate")
    if not 0.0 <= robbery_rate <= 1.0:
        raise ValueError("robbery_rate must be within [0,1]")

    raw_n = row.get("pair_site_n")
    if isinstance(raw_n, bool) or not isinstance(raw_n, int):
        raise ValueError("pair_site_n must be an integer")
    if raw_n <= 0:
        raise ValueError("pair_site_n must be positive")

    return {
        "mismatch": mismatch,
        "robbery_rate": robbery_rate,
        "pair_site_n": raw_n,
    }


def _aubert_row_key(row: dict[str, object]) -> tuple[object, ...]:
    return (
        float(row["mismatch"]),
        float(row["robbery_rate"]),
        int(row["pair_site_n"]),
    )


def canonicalize_aubert(
    rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Canonicalize plant-species Aubert points; row order is representation only."""
    if not rows:
        raise ValueError("Aubert input must contain at least one plant-species point")
    out = [_aubert_scientific_row(row) for row in rows]
    return sorted(out, key=_aubert_row_key)

def canonical_stable_json_sha256(
    network: str,
    rows: list[dict[str, object]],
) -> str:
    if network == "sakhalkar":
        payload = canonicalize_sakhalkar(rows)
    elif network == "aubert_ephi":
        payload = canonicalize_aubert(rows)
    else:
        raise ValueError(f"unknown existing network: {network}")
    return _stable_json_sha256(payload)


def load_canonical_fingerprints(
    path: str | Path = RECEIPT_PATH,
) -> dict[str, object]:
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
        digest = str(entry.get("canonical_stable_json_sha256", "")).strip().lower()
        if len(digest) != 64:
            raise ValueError(f"EXISTING_K3_FINGERPRINT_INVALID:{key}")
        try:
            int(digest, 16)
        except ValueError as exc:
            raise ValueError(f"EXISTING_K3_FINGERPRINT_INVALID:{key}") from exc
        units = entry.get("analysis_units")
        if not isinstance(units, int) or units <= 0:
            raise ValueError(f"EXISTING_K3_ANALYSIS_UNITS_INVALID:{key}")
        if not str(entry.get("source_doi", "")).strip():
            raise ValueError(f"EXISTING_K3_SOURCE_DOI_MISSING:{key}")
    return receipt


def validate_existing_network_payloads(
    sakhalkar_points: list[dict[str, object]],
    aubert_rows: list[dict[str, object]],
    *,
    receipt_path: str | Path = RECEIPT_PATH,
) -> dict[str, object]:
    receipt = load_canonical_fingerprints(receipt_path)
    payloads = {
        "sakhalkar": sakhalkar_points,
        "aubert_ephi": aubert_rows,
    }
    checks: dict[str, object] = {}
    failures: list[str] = []
    for key, payload in payloads.items():
        expected = receipt["networks"][key]
        digest = canonical_stable_json_sha256(key, payload)
        units = len(payload)
        digest_match = digest == expected["canonical_stable_json_sha256"]
        units_match = units == expected["analysis_units"]
        checks[key] = {
            "analysis_units": units,
            "expected_analysis_units": expected["analysis_units"],
            "analysis_units_match": units_match,
            "canonical_stable_json_sha256": digest,
            "expected_canonical_stable_json_sha256": expected[
                "canonical_stable_json_sha256"
            ],
            "canonical_stable_json_match": digest_match,
            "source_doi": expected["source_doi"],
        }
        if not units_match:
            failures.append(f"canonical_analysis_units_mismatch:{key}")
        if not digest_match:
            failures.append(f"canonical_stable_digest_mismatch:{key}")
    return {
        "status": MATCH_STATUS if not failures else MISMATCH_STATUS,
        "checks": checks,
        "failures": failures,
    }
