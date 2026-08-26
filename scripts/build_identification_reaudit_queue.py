"""Build a source re-audit queue under the discrete identification design.

The existing direct-AxD audit was built for a different question and does not
encode selective antagonist/pollinator toggles, Delta_AD M0, or an independent
joint-cost assay. This script therefore does not infer absence of those features.
It marks them as requiring source re-audit and prioritizes candidates by the
amount of already-established A/D interaction structure.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path


ANCHOR_CLASS = {
    "Gorden_Adler_2018_Impatiens_capensis": "TOTAL_INTERACTION_OBSERVATIONAL",
    "Kessler_et_al_2015_Nicotiana": "FACTORIAL_PHENOTYPE_INVALID_D",
    "Santangelo_Thompson_Johnson_2019_Trifolium": "CROSS_ORGAN_FACTORIAL_NEAR_MISS",
    "Garcia_Dow_Vezina_Parachnowitsch_2024_Asclepias": "JOINT_TRAIT_NO_AXD_TERM",
    "Irwin_Adler_2006_Gelsemium": "JOINT_TRAIT_NO_AXD_TERM",
}


def priority(row: dict[str, str]) -> tuple[int, str]:
    study = row["study_id"]
    anchor = ANCHOR_CLASS.get(study)
    if anchor == "TOTAL_INTERACTION_OBSERVATIONAL":
        return 1, anchor
    if anchor in {"FACTORIAL_PHENOTYPE_INVALID_D", "CROSS_ORGAN_FACTORIAL_NEAR_MISS"}:
        return 2, anchor
    if anchor == "JOINT_TRAIT_NO_AXD_TERM":
        return 3, anchor
    return 4, "STRUCTURAL_EXCLUSION_OR_COMPONENT_ONLY"


def build_rows(input_csv: Path) -> list[dict[str, str]]:
    with input_csv.open(newline="", encoding="utf-8") as handle:
        source = list(csv.DictReader(handle))
    rows = []
    for row in source:
        rank, design_class = priority(row)
        rows.append(
            {
                "audit_id": row["audit_id"],
                "study_id": row["study_id"],
                "plant_taxon": row["plant_taxon"],
                "existing_tier": row["tier_decision"],
                "existing_direct_status": row["direct_AxD_term_status"],
                "identification_design_class": design_class,
                "reaudit_priority": str(rank),
                "selective_antagonist_toggle": "REQUIRES_SOURCE_REAUDIT",
                "selective_pollinator_toggle": "REQUIRES_SOURCE_REAUDIT",
                "m0_delta": "REQUIRES_SOURCE_REAUDIT",
                "independent_kappa_assay": "REQUIRES_SOURCE_REAUDIT",
                "interpretation": (
                    "Old direct-AxD audit does not encode the new intervention/baseline/cost identification fields; "
                    "do not infer absence from this queue."
                ),
            }
        )
    rows.sort(key=lambda r: (int(r["reaudit_priority"]), r["study_id"]))
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_csv", type=Path)
    args = parser.parse_args(argv)
    rows = build_rows(args.input_csv)
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {args.output_csv}: {len(rows)} candidates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
