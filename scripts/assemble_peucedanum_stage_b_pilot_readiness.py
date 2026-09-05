from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

from scripts.evaluate_peucedanum_stage_b_manipulation import (
    analyze as validate_manipulation,
    read_rows as read_validation_rows,
)


COMMON_SUPPORT_SCHEMA = "BITA_PEUCEDANUM_STAGE_B_COMMON_SUPPORT_V1"
PILOT_SCHEMA = "BITA_PEUCEDANUM_STAGE_B_TECHNICAL_PILOT_V1"
PLACEHOLDER = "REQUIRED_BEFORE_USE"
ATTEMPT_FIELDS = (
    "unit_id",
    "q_target",
    "common_support_eligible",
    "manipulation_attempted",
    "manipulation_qualified",
    "failure_reason",
)


def _flag(value: str, field: str) -> int:
    if value.strip() not in {"0", "1"}:
        raise ValueError(f"{field} must be coded 0/1")
    return int(value.strip())


def _num(value: str, field: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"invalid numeric value for {field!r}: {value!r}") from exc
    if not math.isfinite(result):
        raise ValueError(f"non-finite numeric value for {field!r}")
    return result


def _wilson_lower(successes: int, trials: int, z: float = 1.96) -> float:
    if trials <= 0:
        raise ValueError("Wilson interval requires trials > 0")
    p = successes / trials
    z2 = z * z
    denom = 1 + z2 / trials
    center = p + z2 / (2 * trials)
    half = z * math.sqrt((p * (1 - p) + z2 / (4 * trials)) / trials)
    return max(0.0, (center - half) / denom)


def read_attempt_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("attempt ledger has no header")
        missing = [field for field in ATTEMPT_FIELDS if field not in reader.fieldnames]
        if missing:
            raise ValueError(f"attempt ledger missing columns: {', '.join(missing)}")
        rows = list(reader)
    if not rows:
        raise ValueError("attempt ledger has no data rows")

    seen: set[str] = set()
    for line, row in enumerate(rows, start=2):
        for field in ATTEMPT_FIELDS[:-1]:
            if row.get(field, "").strip() == "":
                raise ValueError(f"blank required field {field!r} on line {line}")
        unit = row["unit_id"].strip()
        if unit in seen:
            raise ValueError(f"duplicate unit_id {unit!r}")
        seen.add(unit)
        q = _num(row["q_target"], "q_target")
        if not 0 < q < 1:
            raise ValueError("q_target must be on (0,1)")
        eligible = _flag(row["common_support_eligible"], "common_support_eligible")
        attempted = _flag(row["manipulation_attempted"], "manipulation_attempted")
        qualified = _flag(row["manipulation_qualified"], "manipulation_qualified")
        if attempted and not eligible:
            raise ValueError("non-common-support unit cannot be manipulation_attempted=1")
        if qualified and not attempted:
            raise ValueError("manipulation_qualified=1 requires manipulation_attempted=1")
        reason = row.get("failure_reason", "").strip()
        if qualified and reason not in {"", "OK", "PASS"}:
            raise ValueError("qualified units must not carry a failure reason")
        if attempted and not qualified and reason == "":
            raise ValueError("failed manipulation attempts must record failure_reason")
    return rows


def _require_pilot_config(config: dict) -> dict:
    keys = (
        "min_attempted_per_q_level",
        "min_qualified_per_q_level",
        "min_overall_qualification_fraction",
        "min_qualification_fraction_per_q_level",
        "max_qualification_fraction_difference_across_q",
    )
    out = dict(config)
    for key in keys:
        value = out.get(key)
        if value is None or value == PLACEHOLDER:
            raise ValueError(f"pilot config field {key!r} must be preregistered")
        try:
            out[key] = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"pilot config field {key!r} must be numeric") from exc
    for key in ("min_attempted_per_q_level", "min_qualified_per_q_level"):
        if out[key] < 1 or abs(out[key] - round(out[key])) > 1e-9:
            raise ValueError(f"pilot config field {key!r} must be a positive integer")
        out[key] = int(round(out[key]))
    for key in keys[2:]:
        if not 0 <= out[key] <= 1:
            raise ValueError(f"pilot config field {key!r} must be on [0,1]")
    return out


def assemble(
    common_support_receipt: dict,
    attempt_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    validation_config: dict,
    pilot_config: dict,
) -> dict:
    if common_support_receipt.get("schema_version") != COMMON_SUPPORT_SCHEMA:
        raise ValueError("common-support receipt has wrong schema")
    pilot_config = _require_pilot_config(pilot_config)

    eligible_ids = set(common_support_receipt["presurvey"]["eligible_unit_ids"])
    registered_q = [float(value) for value in common_support_receipt["q_targets"]]
    attempted = [row for row in attempt_rows if _flag(row["manipulation_attempted"], "manipulation_attempted")]
    if not attempted:
        raise ValueError("pilot has no attempted manipulations")

    attempted_ids = {row["unit_id"] for row in attempted}
    if not attempted_ids <= eligible_ids:
        missing = sorted(attempted_ids - eligible_ids)
        raise ValueError(f"pilot attempted units outside common support: {missing[:5]}")

    attempt_q = sorted({_num(row["q_target"], "q_target") for row in attempted})
    if len(attempt_q) != len(registered_q) or any(abs(a - b) > 1e-9 for a, b in zip(attempt_q, registered_q)):
        raise ValueError("pilot q levels must exactly match the registered common-support q targets")

    qualified_attempts = [row for row in attempted if _flag(row["manipulation_qualified"], "manipulation_qualified")]
    qualified_ids = {row["unit_id"] for row in qualified_attempts}
    validation_ids = {row["unit_id"] for row in validation_rows}
    if validation_ids != qualified_ids:
        raise ValueError("validation CSV must contain exactly the manipulation-qualified pilot units")

    validation_receipt = validate_manipulation(validation_rows, validation_config)

    by_q: dict[float, list[dict[str, str]]] = defaultdict(list)
    for row in attempted:
        by_q[_num(row["q_target"], "q_target")].append(row)
    attempted_by_q = {q: len(group) for q, group in by_q.items()}
    qualified_by_q = {
        q: sum(_flag(row["manipulation_qualified"], "manipulation_qualified") for row in group)
        for q, group in by_q.items()
    }
    fraction_by_q = {q: qualified_by_q[q] / attempted_by_q[q] for q in by_q}
    total_attempted = len(attempted)
    total_qualified = len(qualified_attempts)
    overall_fraction = total_qualified / total_attempted
    lower95 = _wilson_lower(total_qualified, total_attempted)
    per_q_min = min(fraction_by_q.values())
    per_q_range = max(fraction_by_q.values()) - min(fraction_by_q.values())

    gates = {
        "attempted_units_all_in_common_support": attempted_ids <= eligible_ids,
        "q_targets_match_common_support_design": True,
        "minimum_attempts_per_q": min(attempted_by_q.values()) >= pilot_config["min_attempted_per_q_level"],
        "minimum_qualified_per_q": min(qualified_by_q.values()) >= pilot_config["min_qualified_per_q_level"],
        "overall_qualification_rate": overall_fraction >= pilot_config["min_overall_qualification_fraction"],
        "qualification_rate_per_q": per_q_min >= pilot_config["min_qualification_fraction_per_q_level"],
        "qualification_rate_not_strongly_q_dependent": per_q_range <= pilot_config["max_qualification_fraction_difference_across_q"],
        "qualified_subset_passes_manipulation_validation": (
            validation_receipt["status"] == "PEUCEDANUM_STAGE_B_SEX_COMPOSITION_MANIPULATION_VALIDATED"
        ),
    }
    supported = all(gates.values())

    return {
        "receipt_schema_version": PILOT_SCHEMA,
        "status": "PEUCEDANUM_STAGE_B_TECHNICAL_PILOT_PASSED" if supported else "PEUCEDANUM_STAGE_B_TECHNICAL_PILOT_NOT_PASSED",
        "common_support_design": {
            "retained_total": common_support_receipt["retained_total"],
            "q_targets": registered_q,
            "presurvey_common_eligible_fraction": common_support_receipt["presurvey"]["common_eligible_fraction"],
            "presurvey_common_eligible_fraction_wilson_lower95": common_support_receipt["presurvey"]["common_eligible_fraction_wilson_lower95"],
        },
        "pilot_attempts": {
            "attempted_total": total_attempted,
            "qualified_total": total_qualified,
            "attempted_by_q": {str(q): attempted_by_q[q] for q in sorted(by_q)},
            "qualified_by_q": {str(q): qualified_by_q[q] for q in sorted(by_q)},
            "qualification_fraction_by_q": {str(q): fraction_by_q[q] for q in sorted(by_q)},
            "overall_qualification_fraction": overall_fraction,
            "overall_qualification_fraction_wilson_lower95": lower95,
            "observed_pre_g_qualification_failure_fraction": 1.0 - overall_fraction,
            "conservative_planning_failure_fraction_from_wilson_lower95": 1.0 - lower95,
            "max_qualification_fraction_difference_across_q": per_q_range,
        },
        "manipulation_validation_receipt": validation_receipt,
        "gates": gates,
        "next_use": (
            "If positive, use the common-support eligibility estimate and the pilot qualification-rate estimate "
            "to update the Stage-B operational recruitment planner before freezing the confirmatory design."
        ),
        "claim_ceiling": (
            "technical manipulation feasibility only; not a q fitness effect; not antagonist-dependent selection; "
            "not causal partial differentiation; not historical origin of andromonoecy"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Assemble Peucedanum Stage-B technical pilot readiness")
    parser.add_argument("common_support_json", type=Path)
    parser.add_argument("attempt_ledger_csv", type=Path)
    parser.add_argument("validation_csv", type=Path)
    parser.add_argument("validation_config_json", type=Path)
    parser.add_argument("pilot_config_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    common_support = json.loads(args.common_support_json.read_text(encoding="utf-8"))
    attempts = read_attempt_rows(args.attempt_ledger_csv)
    validation_rows = read_validation_rows(args.validation_csv)
    validation_config = json.loads(args.validation_config_json.read_text(encoding="utf-8"))
    pilot_config = json.loads(args.pilot_config_json.read_text(encoding="utf-8"))
    receipt = assemble(common_support, attempts, validation_rows, validation_config, pilot_config)
    payload = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
