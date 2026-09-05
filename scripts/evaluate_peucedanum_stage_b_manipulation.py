from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean


REQUIRED_FIELDS = (
    "unit_id",
    "block_id",
    "q_target",
    "q_realized",
    "total_before",
    "total_retained",
    "perfect_retained",
    "male_retained",
    "classification_checked_n",
    "classification_correct_n",
    "eggs_before_manipulation",
    "removal_load",
    "handling_actions",
    "mechanical_damage_count",
    "male_phase_complete",
    "flower_height",
    "flowering_day",
)

RECEIPT_SCHEMA = "BITA_PEUCEDANUM_STAGE_B_MANIPULATION_VALIDATION_V1"
PLACEHOLDER = "REQUIRED_BEFORE_USE"


def _num(row: dict[str, str], field: str) -> float:
    try:
        value = float(row[field])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"invalid numeric value for {field!r}: {row.get(field)!r}") from exc
    if not math.isfinite(value):
        raise ValueError(f"non-finite numeric value for {field!r}")
    return value


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
        raise ValueError("CSV has no data rows")

    seen: set[str] = set()
    for i, row in enumerate(rows, start=2):
        for field in REQUIRED_FIELDS:
            if row.get(field, "").strip() == "":
                raise ValueError(f"blank required field {field!r} on CSV line {i}")
        unit = row["unit_id"].strip()
        if unit in seen:
            raise ValueError(f"duplicate unit_id {unit!r}")
        seen.add(unit)
        for field in REQUIRED_FIELDS[2:]:
            _num(row, field)

        q_target = _num(row, "q_target")
        q_realized = _num(row, "q_realized")
        total_before = _num(row, "total_before")
        total_retained = _num(row, "total_retained")
        perfect = _num(row, "perfect_retained")
        male = _num(row, "male_retained")
        checked = _num(row, "classification_checked_n")
        correct = _num(row, "classification_correct_n")
        eggs = _num(row, "eggs_before_manipulation")
        removal = _num(row, "removal_load")
        handling = _num(row, "handling_actions")
        damage = _num(row, "mechanical_damage_count")
        male_complete = _num(row, "male_phase_complete")

        if not 0 <= q_target <= 1 or not 0 <= q_realized <= 1:
            raise ValueError("q_target and q_realized must be on [0,1]")
        if total_before <= 0 or total_retained <= 0 or perfect < 0 or male < 0:
            raise ValueError("flower counts must be non-negative and totals must be > 0")
        if total_retained > total_before + 1e-6:
            raise ValueError("total_retained cannot exceed total_before")
        if abs((perfect + male) - total_retained) > max(1e-6, 1e-6 * total_retained):
            raise ValueError("perfect_retained + male_retained must equal total_retained")
        expected_q = perfect / total_retained
        if abs(q_realized - expected_q) > 1e-6:
            raise ValueError("q_realized must equal perfect_retained / total_retained")
        if checked <= 0 or correct < 0 or correct > checked:
            raise ValueError("classification counts must satisfy 0 <= correct <= checked and checked > 0")
        if eggs < 0 or removal < 0 or handling < 0 or damage < 0:
            raise ValueError("egg, removal, handling and damage counts must be non-negative")
        if abs(removal - (total_before - total_retained)) > max(1e-6, 1e-6 * total_before):
            raise ValueError("removal_load must equal total_before - total_retained")
        if handling + 1e-9 < removal:
            raise ValueError("handling_actions cannot be less than removal_load")
        if damage > total_retained + 1e-6:
            raise ValueError("mechanical_damage_count cannot exceed total_retained")
        if male_complete not in (0.0, 1.0):
            raise ValueError("male_phase_complete must be coded 0/1")
    return rows


def _require_config(config: dict) -> dict:
    numeric_keys = (
        "min_q_levels",
        "min_units_per_q_level",
        "target_total_retained_count",
        "max_abs_q_realization_error",
        "min_q_target_separation",
        "min_classification_accuracy_lower95",
        "max_pre_manipulation_egg_positive_fraction",
        "max_mean_pre_manipulation_eggs",
        "max_total_retained_relative_deviation",
        "max_handling_group_relative_range",
        "max_abs_pretreatment_group_smd",
        "max_mechanical_damage_rate",
        "max_mechanical_damage_group_difference",
        "min_male_phase_complete_fraction",
    )
    out = dict(config)
    for key in numeric_keys:
        value = out.get(key)
        if value is None or value == PLACEHOLDER:
            raise ValueError(f"config field {key!r} must be preregistered before Stage-B validation")
        try:
            out[key] = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"config field {key!r} must be numeric") from exc
    for key in ("min_q_levels", "min_units_per_q_level"):
        if out[key] < 1:
            raise ValueError(f"config field {key!r} must be >= 1")
        out[key] = int(out[key])
    if out["target_total_retained_count"] <= 0:
        raise ValueError("target_total_retained_count must be > 0")
    for key in numeric_keys[3:]:
        if out[key] < 0:
            raise ValueError(f"config field {key!r} must be >= 0")
    for key in (
        "min_classification_accuracy_lower95",
        "max_pre_manipulation_egg_positive_fraction",
        "max_mechanical_damage_rate",
        "max_mechanical_damage_group_difference",
        "min_male_phase_complete_fraction",
    ):
        if out[key] > 1:
            raise ValueError(f"config field {key!r} must be <= 1")
    return out


def _sample_sd(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    center = mean(values)
    return math.sqrt(sum((value - center) ** 2 for value in values) / (len(values) - 1))


def _pairwise_smd(a: list[float], b: list[float]) -> float:
    s_a, s_b = _sample_sd(a), _sample_sd(b)
    pooled = math.sqrt((s_a * s_a + s_b * s_b) / 2.0)
    difference = mean(a) - mean(b)
    if pooled <= 1e-15:
        return 0.0 if abs(difference) <= 1e-15 else math.inf
    return abs(difference) / pooled


def _wilson_lower(successes: float, trials: float, z: float = 1.96) -> float:
    if trials <= 0:
        raise ValueError("Wilson interval requires trials > 0")
    p = successes / trials
    denom = 1.0 + z * z / trials
    center = p + z * z / (2.0 * trials)
    radius = z * math.sqrt(p * (1.0 - p) / trials + z * z / (4.0 * trials * trials))
    return max(0.0, (center - radius) / denom)


def analyze(rows: list[dict[str, str]], config: dict) -> dict:
    config = _require_config(config)
    groups: dict[float, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[_num(row, "q_target")].append(row)
    q_levels = sorted(groups)
    counts = {str(level): len(groups[level]) for level in q_levels}

    coverage_gate = (
        len(q_levels) >= config["min_q_levels"]
        and all(len(group) >= config["min_units_per_q_level"] for group in groups.values())
    )
    separation = min((b - a for a, b in zip(q_levels, q_levels[1:])), default=0.0)

    realization_errors = [abs(_num(row, "q_realized") - _num(row, "q_target")) for row in rows]
    realized_means = {level: mean(_num(row, "q_realized") for row in groups[level]) for level in q_levels}
    monotonic_realized = all(realized_means[a] < realized_means[b] for a, b in zip(q_levels, q_levels[1:]))
    q_gate = (
        max(realization_errors) <= config["max_abs_q_realization_error"]
        and separation >= config["min_q_target_separation"]
        and monotonic_realized
    )

    checked = sum(_num(row, "classification_checked_n") for row in rows)
    correct = sum(_num(row, "classification_correct_n") for row in rows)
    classification_accuracy = correct / checked
    classification_lower = _wilson_lower(correct, checked)
    classification_gate = classification_lower >= config["min_classification_accuracy_lower95"]

    eggs = [_num(row, "eggs_before_manipulation") for row in rows]
    egg_positive_fraction = sum(value > 0 for value in eggs) / len(eggs)
    mean_eggs = mean(eggs)
    egg_gate = (
        egg_positive_fraction <= config["max_pre_manipulation_egg_positive_fraction"]
        and mean_eggs <= config["max_mean_pre_manipulation_eggs"]
    )

    target_total = config["target_total_retained_count"]
    retained_relative_errors = [abs(_num(row, "total_retained") - target_total) / target_total for row in rows]
    fixed_total_gate = max(retained_relative_errors) <= config["max_total_retained_relative_deviation"]

    handling_means = {level: mean(_num(row, "handling_actions") for row in groups[level]) for level in q_levels}
    grand_handling = mean(_num(row, "handling_actions") for row in rows)
    handling_range = max(handling_means.values()) - min(handling_means.values())
    if abs(grand_handling) <= 1e-15:
        handling_relative_range = 0.0 if handling_range <= 1e-15 else math.inf
    else:
        handling_relative_range = handling_range / abs(grand_handling)
    handling_gate = handling_relative_range <= config["max_handling_group_relative_range"]

    pretreatment_fields = ("total_before", "flower_height", "flowering_day")
    pairwise_smd: dict[str, float] = {}
    max_smd = 0.0
    for field in pretreatment_fields:
        field_max = 0.0
        for i, level_a in enumerate(q_levels):
            for level_b in q_levels[i + 1 :]:
                value = _pairwise_smd(
                    [_num(row, field) for row in groups[level_a]],
                    [_num(row, field) for row in groups[level_b]],
                )
                field_max = max(field_max, value)
        pairwise_smd[field] = field_max
        max_smd = max(max_smd, field_max)
    pretreatment_gate = max_smd <= config["max_abs_pretreatment_group_smd"]

    damage_rates = [_num(row, "mechanical_damage_count") / _num(row, "total_retained") for row in rows]
    overall_damage = mean(damage_rates)
    damage_group_means = {
        level: mean(_num(row, "mechanical_damage_count") / _num(row, "total_retained") for row in groups[level])
        for level in q_levels
    }
    damage_group_difference = max(damage_group_means.values()) - min(damage_group_means.values())
    damage_gate = (
        overall_damage <= config["max_mechanical_damage_rate"]
        and damage_group_difference <= config["max_mechanical_damage_group_difference"]
    )

    male_complete_by_group = {
        level: mean(_num(row, "male_phase_complete") for row in groups[level])
        for level in q_levels
    }
    male_phase_gate = min(male_complete_by_group.values()) >= config["min_male_phase_complete_fraction"]

    gates = {
        "q_level_coverage": coverage_gate,
        "q_realization_and_separation": q_gate,
        "sex_classification_accuracy": classification_gate,
        "negligible_pre_manipulation_oviposition": egg_gate,
        "fixed_total_retained_display": fixed_total_gate,
        "handling_load_balance": handling_gate,
        "pretreatment_covariate_balance": pretreatment_gate,
        "mechanical_damage_control": damage_gate,
        "male_phase_completed_before_manipulation": male_phase_gate,
    }
    supported = all(gates.values())

    return {
        "receipt_schema_version": RECEIPT_SCHEMA,
        "analysis": "peucedanum_post_male_phase_sex_composition_manipulation_validation",
        "n_units": len(rows),
        "n_q_levels": len(q_levels),
        "q_levels": q_levels,
        "n_by_q_level": counts,
        "q_realization": {
            "max_abs_error": max(realization_errors),
            "minimum_target_separation": separation,
            "realized_group_means": {str(level): realized_means[level] for level in q_levels},
            "monotonic_realized_means": monotonic_realized,
        },
        "classification": {
            "checked_n": checked,
            "correct_n": correct,
            "accuracy": classification_accuracy,
            "wilson_lower_95": classification_lower,
        },
        "pre_manipulation_oviposition": {
            "positive_fraction": egg_positive_fraction,
            "mean_eggs": mean_eggs,
        },
        "fixed_total": {
            "target_total_retained_count": target_total,
            "max_relative_deviation": max(retained_relative_errors),
        },
        "handling": {
            "mean_by_q_level": {str(level): handling_means[level] for level in q_levels},
            "relative_range_across_q_levels": handling_relative_range,
        },
        "pretreatment_balance": {
            "max_pairwise_abs_smd_by_field": pairwise_smd,
            "max_abs_smd": max_smd,
        },
        "mechanical_damage": {
            "overall_rate": overall_damage,
            "mean_rate_by_q_level": {str(level): damage_group_means[level] for level in q_levels},
            "max_group_difference": damage_group_difference,
        },
        "male_phase_completion": {
            "fraction_by_q_level": {str(level): male_complete_by_group[level] for level in q_levels},
            "minimum_group_fraction": min(male_complete_by_group.values()),
        },
        "gates": gates,
        "status": (
            "PEUCEDANUM_STAGE_B_SEX_COMPOSITION_MANIPULATION_VALIDATED"
            if supported
            else "PEUCEDANUM_STAGE_B_MANIPULATION_NOT_VALIDATED"
        ),
        "claim_ceiling": (
            "manipulation_validity_only; enables_future_randomized_q_by_G_fitness_test; "
            "does_not_itself_estimate_q_fitness_effect; not_complete_modularity; not_historical_origin_of_andromonoecy"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Peucedanum Stage-B post-male-phase sex-composition manipulation")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("config_path", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rows = read_rows(args.csv_path)
    config = json.loads(args.config_path.read_text(encoding="utf-8"))
    result = analyze(rows, config)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
