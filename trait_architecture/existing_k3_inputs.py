"""Canonical fingerprints for the two existing networks entering k=3.

The fingerprint deliberately removes representation-only degrees of freedom:
- Sakhalkar rows are sorted by their scientific fields;
- Aubert/EPHI site labels are deterministically relabelled while preserving the
  exact site partition, then rows are sorted by all scientific fields.

No numerical value used by the k=3 calculation is rounded or quantized.
"""
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
MATCH_STATUS = "CANONICAL_EXISTING_K3_INPUTS_MATCH"
MISMATCH_STATUS = "CANONICAL_EXISTING_K3_INPUTS_MISMATCH"
PRODUCTION_INPUT_MODE = "PUBLIC_EXISTING_NETWORKS_FIXED_DOI_REBUILD"


def _stable_json_sha256(payload: object) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _finite_float(value: object, label: str) -> float:
    number = float(value)
    if number != number or number in {float("inf"), float("-inf")}:
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
        if route_class not in {"robber_only", "thief_only", "mixed"}:
            raise ValueError("invalid Sakhalkar route_class")
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


def canonicalize_aubert(
    rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    sites = sorted({str(row["site"]).strip() for row in rows})
    if not sites or any(not site for site in sites):
        raise ValueError("Aubert site labels must be nonblank")
    site_map = {
        site: f"site_{index:02d}"
        for index, site in enumerate(sites, start=1)
    }

    out: list[dict[str, object]] = []
    for row in rows:
        site = str(row["site"]).strip()
        bird_group = str(row["bird_group"]).strip()
        n_interactions = int(row["n_interactions"])
        robbery_rate = _finite_float(row["robbery_rate"], "robbery_rate")
        mismatch = _finite_float(
            row["mismatch_log_t_over_b"],
            "mismatch_log_t_over_b",
        )
        barrier = bool(row["trait_barrier"])
        if n_interactions <= 0:
            raise ValueError("n_interactions must be positive")
        if not bird_group:
            raise ValueError("bird_group must be nonblank")
        out.append(
            {
                "site": site_map[site],
                "bird_group": bird_group,
                "n_interactions": n_interactions,
                "robbery_rate": robbery_rate,
                "mismatch_log_t_over_b": mismatch,
                "trait_barrier": barrier,
            }
        )

    return sorted(
        out,
        key=lambda row: (
            str(row["site"]),
            str(row["bird_group"]),
            int(row["n_interactions"]),
            float(row["robbery_rate"]),
            float(row["mismatch_log_t_over_b"]),
            bool(row["trait_barrier"]),
        ),
    )


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
