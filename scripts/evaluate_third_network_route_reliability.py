"""Evaluate blinded route-coding reliability for the prospective third network.

The independently double-coded subset is selected deterministically from
route-blind event identifiers using the preregistered seed.  This prevents
choosing easy or favorable events after primary route codes are known.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

SEED = 20260922
MIN_DOUBLE_FRACTION = 0.20
TARGET_KAPPA = 0.80
CODES = ("L", "B", "A", "N")
ELIGIBLE_ID_CONFIDENCE = {"HIGH", "MEDIUM"}


def _bool_text(value: object, label: str) -> bool:
    text = str(value).strip().lower()
    if text == "true":
        return True
    if text == "false":
        return False
    raise ValueError(f"{label} must be true/false")


def _eligible_for_reliability(row: dict[str, str]) -> bool:
    return (
        str(row.get("dataset_role", "")).strip().upper() == "CONFIRMATORY"
        and str(row.get("clip_quality", "")).strip().upper() == "PASS"
        and str(row.get("visitor_id_confidence", "")).strip().upper()
        in ELIGIBLE_ID_CONFIDENCE
    )


def expected_double_code_ids(
    rows: list[dict[str, str]],
    *,
    seed: int = SEED,
    minimum_fraction: float = MIN_DOUBLE_FRACTION,
) -> set[str]:
    if not 0 < minimum_fraction <= 1:
        raise ValueError("minimum_fraction must be in (0,1]")

    eligible_ids: list[str] = []
    seen: set[str] = set()
    for row in rows:
        if not _eligible_for_reliability(row):
            continue
        event_id = str(row.get("event_id", "")).strip()
        if not event_id:
            raise ValueError("reliability-eligible event_id must not be blank")
        if event_id in seen:
            raise ValueError("event_id must be unique")
        seen.add(event_id)
        eligible_ids.append(event_id)

    if not eligible_ids:
        raise ValueError("no reliability-eligible confirmatory events")

    n_select = max(1, math.ceil(minimum_fraction * len(eligible_ids)))
    ranked = sorted(
        eligible_ids,
        key=lambda event_id: (
            hashlib.sha256(f"{seed}:{event_id}".encode("utf-8")).hexdigest(),
            event_id,
        ),
    )
    return set(ranked[:n_select])


def _cohen_kappa(primary: list[str], secondary: list[str]) -> tuple[float, float]:
    if len(primary) != len(secondary) or not primary:
        raise ValueError("paired codes must be non-empty and equal length")

    n = len(primary)
    agreement = sum(a == b for a, b in zip(primary, secondary)) / n
    p1 = {code: primary.count(code) / n for code in CODES}
    p2 = {code: secondary.count(code) / n for code in CODES}
    expected = sum(p1[code] * p2[code] for code in CODES)

    if math.isclose(expected, 1.0, rel_tol=0.0, abs_tol=1e-15):
        raise ValueError("ROUTE_RELIABILITY_KAPPA_NOT_ESTIMABLE")

    kappa = (agreement - expected) / (1.0 - expected)
    return agreement, kappa


def evaluate_rows(
    rows: list[dict[str, str]],
    *,
    seed: int = SEED,
    minimum_fraction: float = MIN_DOUBLE_FRACTION,
    target_kappa: float = TARGET_KAPPA,
) -> dict[str, object]:
    required = {
        "event_id",
        "dataset_role",
        "route_code",
        "visitor_id_confidence",
        "clip_quality",
        "coder_id",
        "double_coded",
        "second_route_code",
    }
    if not rows:
        raise ValueError("event table is empty")
    missing = required.difference(rows[0])
    if missing:
        raise ValueError(f"route reliability missing required columns: {sorted(missing)}")

    expected = expected_double_code_ids(
        rows,
        seed=seed,
        minimum_fraction=minimum_fraction,
    )
    eligible = [row for row in rows if _eligible_for_reliability(row)]
    actual = {
        str(row["event_id"]).strip()
        for row in eligible
        if _bool_text(row["double_coded"], "double_coded")
    }

    if actual != expected:
        missing_ids = sorted(expected - actual)
        extra_ids = sorted(actual - expected)
        raise ValueError(
            "DOUBLE_CODE_SUBSET_MISMATCH:"
            f" missing={missing_ids[:5]} extra={extra_ids[:5]}"
        )

    primary: list[str] = []
    secondary: list[str] = []
    coder_ids: set[str] = set()

    for row in eligible:
        event_id = str(row["event_id"]).strip()
        p = str(row["route_code"]).strip().upper()
        if p not in CODES:
            raise ValueError(f"invalid primary route code: {p!r}")
        if event_id not in expected:
            continue

        s = str(row["second_route_code"]).strip().upper()
        if s not in CODES:
            raise ValueError(
                f"double-coded event {event_id} requires second_route_code in L/B/A/N"
            )
        coder = str(row["coder_id"]).strip()
        if not coder:
            raise ValueError("coder_id must not be blank")
        coder_ids.add(coder)
        primary.append(p)
        secondary.append(s)

    raw_agreement, kappa = _cohen_kappa(primary, secondary)
    fraction = len(expected) / len(eligible)
    status = (
        "ROUTE_RELIABILITY_PASS"
        if kappa >= target_kappa
        else "ROUTE_RELIABILITY_RECODE_REQUIRED"
    )

    return {
        "receipt": "BITA_THIRD_NETWORK_ROUTE_RELIABILITY_V1",
        "status": status,
        "seed": seed,
        "eligible_confirmatory_events": len(eligible),
        "double_coded_events": len(expected),
        "double_code_fraction": fraction,
        "minimum_double_code_fraction": minimum_fraction,
        "raw_agreement_LBAN": raw_agreement,
        "kappa_LBAN": kappa,
        "target_kappa_LBAN": target_kappa,
        "primary_coder_ids": sorted(coder_ids),
        "subset_selection": (
            "lowest SHA256(seed:event_id) scores among PASS HIGH/MEDIUM confirmatory events"
        ),
        "claim_boundary": (
            "Reliability is evaluated before route/morphology integration. "
            "Passing reliability does not imply a positive access-routing effect."
        ),
    }


def run(
    events_csv: str | Path,
    output_json: str | Path | None = None,
) -> dict[str, object]:
    with Path(events_csv).open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    result = evaluate_rows(rows)
    if output_json is not None:
        path = Path(output_json)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("events_csv")
    parser.add_argument("--output")
    args = parser.parse_args()
    print(json.dumps(run(args.events_csv, args.output), indent=2, sort_keys=True))
