from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from statistics import mean

from scripts.plan_peucedanum_stage_b_sampling import minimum_recruitment


SCHEMA = "BITA_PEUCEDANUM_STAGE_B_COMMON_SUPPORT_V1"
REQUIRED_FIELDS = ("unit_id", "perfect_available", "male_available", "total_available")


def _integer(row: dict[str, str], field: str) -> int:
    try:
        raw = float(row[field])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"invalid numeric value for {field!r}: {row.get(field)!r}") from exc
    if not math.isfinite(raw) or raw < 0 or abs(raw - round(raw)) > 1e-9:
        raise ValueError(f"{field} must be a non-negative integer")
    return int(round(raw))


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("CSV has no header")
        missing = [field for field in REQUIRED_FIELDS if field not in reader.fieldnames]
        if missing:
            raise ValueError(f"missing required columns: {', '.join(missing)}")
        rows = list(reader)
    if not rows:
        raise ValueError("presurvey CSV has no data rows")
    seen: set[str] = set()
    for line, row in enumerate(rows, start=2):
        for field in REQUIRED_FIELDS:
            if row.get(field, "").strip() == "":
                raise ValueError(f"blank required field {field!r} on line {line}")
        unit = row["unit_id"]
        if unit in seen:
            raise ValueError(f"duplicate unit_id {unit!r}")
        seen.add(unit)
        perfect = _integer(row, "perfect_available")
        male = _integer(row, "male_available")
        total = _integer(row, "total_available")
        if perfect + male != total:
            raise ValueError("perfect_available + male_available must equal total_available")
    return rows


def _wilson_lower(successes: int, n: int, z: float = 1.96) -> float:
    if n <= 0:
        raise ValueError("Wilson interval requires n > 0")
    p = successes / n
    z2 = z * z
    denom = 1 + z2 / n
    center = p + z2 / (2 * n)
    half = z * math.sqrt((p * (1 - p) + z2 / (4 * n)) / n)
    return max(0.0, (center - half) / denom)


def _integer_q_counts(retained_total: int, q_targets: list[float]) -> list[int]:
    if retained_total < 1:
        raise ValueError("retained_total must be >= 1")
    if len(q_targets) < 3 or sorted(q_targets) != q_targets or len(set(q_targets)) != len(q_targets):
        raise ValueError("q_targets must contain at least three distinct increasing values")
    counts = []
    for q in q_targets:
        if not 0 < q < 1:
            raise ValueError("q targets must be on (0,1)")
        expected = q * retained_total
        if abs(expected - round(expected)) > 1e-9:
            raise ValueError(
                f"q={q} is not exactly realizable with retained_total={retained_total}; "
                "choose q targets corresponding to integer flower counts"
            )
        counts.append(int(round(expected)))
    return counts


def evaluate_design(
    rows: list[dict[str, str]],
    *,
    retained_total: int,
    q_targets: list[float],
    pilot_common_eligible_target: int = 24,
    confirmatory_common_eligible_target: int = 189,
    screening_coverage_probability: float = 0.90,
) -> dict:
    perfect_targets = _integer_q_counts(retained_total, q_targets)
    male_targets = [retained_total - perfect for perfect in perfect_targets]
    min_perfect_required = max(perfect_targets)
    min_male_required = max(male_targets)

    eligible_ids = []
    natural_q_all = []
    natural_q_eligible = []
    for row in rows:
        perfect = _integer(row, "perfect_available")
        male = _integer(row, "male_available")
        total = _integer(row, "total_available")
        natural_q = perfect / total if total > 0 else 0.0
        natural_q_all.append(natural_q)
        eligible = (
            perfect >= min_perfect_required
            and male >= min_male_required
            and total >= retained_total
        )
        if eligible:
            eligible_ids.append(row["unit_id"])
            natural_q_eligible.append(natural_q)

    n = len(rows)
    eligible_n = len(eligible_ids)
    fraction = eligible_n / n
    lower95 = _wilson_lower(eligible_n, n)

    def screening_plan(target: int) -> dict | None:
        if lower95 <= 0:
            return None
        return minimum_recruitment(
            target_retained=target,
            retention_probability=lower95,
            groups=1,
            minimum_joint_probability=screening_coverage_probability,
        )

    return {
        "schema_version": SCHEMA,
        "retained_total": retained_total,
        "q_targets": q_targets,
        "perfect_retained_by_q": {str(q): p for q, p in zip(q_targets, perfect_targets)},
        "male_retained_by_q": {str(q): m for q, m in zip(q_targets, male_targets)},
        "common_support_requirements": {
            "minimum_perfect_available": min_perfect_required,
            "minimum_male_available": min_male_required,
            "minimum_total_available": retained_total,
            "logic": (
                "Only units capable of every registered q target enter q randomization. "
                "This prevents treatment eligibility from being determined by natural sex allocation."
            ),
        },
        "presurvey": {
            "n_screened": n,
            "n_common_eligible": eligible_n,
            "common_eligible_fraction": fraction,
            "common_eligible_fraction_wilson_lower95": lower95,
            "eligible_unit_ids": eligible_ids,
            "mean_natural_q_all": mean(natural_q_all),
            "mean_natural_q_common_eligible": mean(natural_q_eligible) if natural_q_eligible else None,
        },
        "screening_plans_using_wilson_lower95": {
            "pilot_target": {
                "target_common_eligible": pilot_common_eligible_target,
                "plan": screening_plan(pilot_common_eligible_target),
            },
            "confirmatory_target": {
                "target_common_eligible": confirmatory_common_eligible_target,
                "plan": screening_plan(confirmatory_common_eligible_target),
            },
        },
        "q_span": max(q_targets) - min(q_targets),
        "claim_boundary": (
            "Common-support screening protects q randomization within the eligible subset. "
            "It does not make that subset representative of the full population, and the screening-size "
            "calculation is operational coverage, not power for the causal fitness effect."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate common support for Peucedanum Stage-B q manipulation")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--retained-total", type=int, required=True)
    parser.add_argument("--q-targets", required=True, help="comma-separated increasing q values, e.g. 0.2,0.4,0.6")
    parser.add_argument("--pilot-target", type=int, default=24)
    parser.add_argument("--confirmatory-target", type=int, default=189)
    parser.add_argument("--coverage", type=float, default=0.90)
    args = parser.parse_args()
    q_targets = [float(value) for value in args.q_targets.split(",")]
    result = evaluate_design(
        read_rows(args.csv_path),
        retained_total=args.retained_total,
        q_targets=q_targets,
        pilot_common_eligible_target=args.pilot_target,
        confirmatory_common_eligible_target=args.confirmatory_target,
        screening_coverage_probability=args.coverage,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
