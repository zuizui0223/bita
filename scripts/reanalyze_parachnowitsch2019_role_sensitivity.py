"""Reanalyse the reproduced 2019 paper effects across fixed role-evidence tiers.

The tiers are declared in ``PARACHNOWITSCH2019_ROLE_AUDIT_V1.csv`` and are
primary-source evidence filters, not new biological parameters. The analysis
uses the same DerSimonian-Laird random-effects calculation as the existing
broad reproduction.

Usage:
    python scripts/reanalyze_parachnowitsch2019_role_sensitivity.py \
      empirical/constituent_path_meta/PARACHNOWITSCH2019_STUDY_EFFECTS_V1.csv \
      empirical/constituent_path_meta/PARACHNOWITSCH2019_ROLE_AUDIT_V1.csv \
      OUTPUT_DIR
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

Z_975 = 1.959963984540054
TIER_FIELDS = (
    ("published_all_9", "include_published_all"),
    ("defence_associated_verified_5", "include_defence_associated_verified"),
    (
        "defence_associated_with_provisional_identity_6",
        "include_defence_associated_with_provisional_identity",
    ),
    ("same_system_role_verified_3", "include_same_system_role_verified"),
)


def read_csv(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return [{key: (value or "").strip() for key, value in row.items()} for row in csv.DictReader(handle)]


def _float(value: str, field: str) -> float:
    try:
        number = float(value)
    except ValueError as error:
        raise ValueError(f"{field} must be numeric") from error
    if not math.isfinite(number):
        raise ValueError(f"{field} must be finite")
    return number


def dersimonian_laird(rows: list[dict[str, str]]) -> dict[str, float]:
    if len(rows) < 2:
        raise ValueError("role sensitivity requires at least two paper effects")
    effects = [_float(row["fixed_effect_hedges_g"], "fixed_effect_hedges_g") for row in rows]
    variances = [_float(row["sampling_variance"], "sampling_variance") for row in rows]
    if any(variance <= 0 for variance in variances):
        raise ValueError("sampling variances must be positive")
    weights = [1 / variance for variance in variances]
    fixed_mean = sum(weight * effect for weight, effect in zip(weights, effects)) / sum(weights)
    q_value = sum(
        weight * (effect - fixed_mean) ** 2
        for weight, effect in zip(weights, effects)
    )
    q_df = len(rows) - 1
    c_value = sum(weights) - sum(weight**2 for weight in weights) / sum(weights)
    tau_squared = max(0.0, (q_value - q_df) / c_value) if c_value > 0 else 0.0
    random_weights = [1 / (variance + tau_squared) for variance in variances]
    pooled = sum(
        weight * effect for weight, effect in zip(random_weights, effects)
    ) / sum(random_weights)
    pooled_se = math.sqrt(1 / sum(random_weights))
    ci_low = pooled - Z_975 * pooled_se
    ci_high = pooled + Z_975 * pooled_se
    i_squared = max(0.0, (q_value - q_df) / q_value * 100) if q_value > 0 else 0.0
    return {
        "fixed_effect_mean": fixed_mean,
        "random_effects_mean": pooled,
        "random_effects_standard_error": pooled_se,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "tau_squared_DL": tau_squared,
        "Q": q_value,
        "Q_df": float(q_df),
        "I_squared_percent": i_squared,
    }


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty {path.name}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paper_effects_csv")
    parser.add_argument("role_audit_csv")
    parser.add_argument("output_dir")
    args = parser.parse_args(argv)

    effects = read_csv(args.paper_effects_csv)
    audit = read_csv(args.role_audit_csv)
    effect_by_paper = {row["paper"]: row for row in effects}
    if len(effect_by_paper) != len(effects):
        raise ValueError("paper effect labels must be unique")
    audit_by_paper = {row["workbook_label"]: row for row in audit}
    if set(effect_by_paper) != set(audit_by_paper):
        raise ValueError("paper effects and role audit must contain the same workbook labels")

    summaries: list[dict[str, object]] = []
    membership: list[dict[str, object]] = []
    for tier_name, audit_field in TIER_FIELDS:
        members = [
            effect_by_paper[paper]
            for paper, row in audit_by_paper.items()
            if row[audit_field].lower() == "yes"
        ]
        diagnostics = dersimonian_laird(members)
        ci_excludes_zero = diagnostics["ci_high"] < 0 or diagnostics["ci_low"] > 0
        summaries.append({
            "tier": tier_name,
            "independent_papers": len(members),
            "paper_labels": ";".join(sorted(row["paper"] for row in members)),
            **diagnostics,
            "pooled_direction": (
                "negative" if diagnostics["random_effects_mean"] < 0
                else "positive" if diagnostics["random_effects_mean"] > 0
                else "zero"
            ),
            "ci_excludes_zero": "yes" if ci_excludes_zero else "no",
        })
        for row in sorted(members, key=lambda item: item["paper"]):
            membership.append({
                "tier": tier_name,
                "paper": row["paper"],
                "paper_effect_hedges_g": row["fixed_effect_hedges_g"],
                "sampling_variance": row["sampling_variance"],
                "canonical_strict_b_to_p_status": audit_by_paper[row["paper"]]["canonical_strict_b_to_p_status"],
            })

    destination = Path(args.output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    _write_csv(destination / "parachnowitsch2019_role_sensitivity_summary.csv", summaries)
    _write_csv(destination / "parachnowitsch2019_role_sensitivity_membership.csv", membership)
    report = {
        "article_doi": "10.1093/aob/mcy132",
        "tiers": summaries,
        "interpretation_boundary": (
            "These are sensitivity estimates from the published paper-level summaries. The "
            "stricter tiers improve trait-role provenance but do not repair mixed consumer roles, "
            "mixed response constructs, dose pooling, or treatment-orientation problems within "
            "the source workbook. No tier is a canonical estimate of iota or W_AD."
        ),
    }
    (destination / "parachnowitsch2019_role_sensitivity_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
