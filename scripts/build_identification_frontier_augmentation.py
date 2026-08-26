from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "empirical" / "identification_design" / "HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V1.csv"
OUT_CSV = ROOT / "empirical" / "identification_design" / "IDENTIFICATION_FRONTIER_AUGMENTATION_V1.csv"
OUT_MD = ROOT / "empirical" / "identification_design" / "IDENTIFICATION_FRONTIER_AUGMENTATION_V1.md"

# These labels do not score study quality.  They externalize which information
# face of the identification problem each screened system currently occupies and
# what biologically meaningful module would move it forward.
DERIVED = {
    "Gorden_Adler_2018_Impatiens_capensis": (
        "randomized_context_anchor",
        "randomize_and_cross_valid_A_and_D_and_replace_intensity_additions_with_selective_G_P_toggles",
        "M0_delta;four_way_separability;independent_kappa_assay",
        "observational_AxD_target_intervals_cross_zero_so_no_sign_resolved_biotic_balance_from_current_data",
    ),
    "Kessler_Gase_Baldwin_2008_Nicotiana": (
        "direct_trait_factorial_anchor",
        "resolve_flower_specific_D_scope_and_add_crossed_selective_G_P_toggles_to_existing_AxD_backbone",
        "M0_delta;four_way_separability;independent_kappa_assay",
        "published_rounded_probability_Delta_AD=+0.19_to_+0.25;conditional_on_same_scale_kappa>=0_biotic_balance_rho_minus_iota>=+0.19;aggregate_constraint_not_confidence_bound",
    ),
    "Irwin_Adler_2006_Gelsemium": (
        "joint_trait_observational",
        "experimentally_cross_attraction_traits_with_nectar_gelsemine_on_common_reproductive_outcome",
        "selective_G_P_toggles;M0_delta;four_way_separability;independent_kappa_assay",
        "no_total_AxD_in_current_audit",
    ),
    "Gross_Sun_Schiestl_2016_Gymnadenia": (
        "single_A_axis",
        "add_distinct_independently_manipulable_flower_associated_D_and_cross_with_scent",
        "common_AxD_outcome;selective_G_P_toggles;M0_delta;four_way_separability;independent_kappa_assay",
        "no_valid_D_axis",
    ),
    "Dalechampia_linked_panel_candidate": (
        "unresolved_candidate",
        "verify_individual_level_A_D_linkage_and_common_outcome_before_any_mechanistic_allocation",
        "crossed_A_D_manipulation;selective_G_P_toggles;M0_delta;four_way_separability;independent_kappa_assay",
        "individual_level_linkage_not_verified",
    ),
    "Strauss_Irwin_2004_Raphanus": (
        "joint_trait_observational",
        "put_petal_colour_and_defence_on_common_within_system_AxD_fitness_factorial",
        "selective_G_P_toggles;M0_delta;four_way_separability;independent_kappa_assay",
        "no_direct_AxD_common_outcome",
    ),
    "Gronquist_2001_Hypericum": (
        "nonseparable_single_trait",
        "choose_distinct_attraction_and_defence_coordinates_before_testing_AxD",
        "crossed_A_D_manipulation;common_outcome;selective_G_P_toggles;M0_delta;four_way_separability;independent_kappa_assay",
        "A_and_D_are_same_trait_axis",
    ),
    "Kessler_2015_Nicotiana": (
        "phenotype_factorial_invalid_D",
        "replace_nectar_reward_axis_with_independently_justified_antagonist_reducing_D_while_retaining_2x2_floral_phenotype",
        "shared_reproductive_AxD;selective_G_P_toggles;M0_delta;four_way_separability;independent_kappa_assay",
        "second_axis_is_reward_not_valid_D",
    ),
    "Santangelo_2019_Trifolium": (
        "cross_organ_trait_defence",
        "use_flower_specific_D_and_manipulate_A_on_same_floral_coordinates",
        "strict_flower_AxD_factorial;selective_P_toggle;M0_delta;four_way_separability;independent_kappa_assay",
        "current_D_is_whole_plant_and_A_is_not_manipulated",
    ),
    "Egan_2021_Fragaria": (
        "consumer_factorial_anchor",
        "cross_independently_manipulable_flower_specific_A_and_D_onto_existing_consumer_factorial_backbone",
        "M0_delta;four_way_separability;independent_kappa_assay",
        "consumer_factorial_exists_but_focal_A_D_are_not_crossed_and_D_is_leaf_specific",
    ),
    "Garcia_2024_Asclepias": (
        "joint_trait_observational",
        "add_experimental_AxD_cross_on_common_outcome_to_flower_specific_latex_system",
        "selective_G_P_toggles;M0_delta;four_way_separability;independent_kappa_assay",
        "current_data_have_main_effects_only",
    ),
    "Knauer_Schiestl_2017_Brassica": (
        "single_A_multiroute",
        "add_distinct_flower_associated_D_axis_and_cross_with_attraction_signals",
        "common_AxD_outcome;selective_G_P_toggles;M0_delta;four_way_separability;independent_kappa_assay",
        "no_distinct_D_axis",
    ),
    "Strauss_1999_Brassica": (
        "cross_organ_consumer_context",
        "replace_whole_plant_D_with_flower_specific_D_and_manipulate_A_within_existing_damage_context",
        "strict_flower_AxD_factorial;selective_P_toggle;M0_delta;four_way_separability;independent_kappa_assay",
        "current_D_is_whole_plant_and_A_is_not_manipulated",
    ),
    "Hanley_2009_Hakea": (
        "comparative_joint_trait_covariance",
        "move_comparative_A_D_covariance_to_within_system_crossed_AxD_manipulation",
        "common_reproductive_outcome;selective_G_P_toggles;M0_delta;four_way_separability;independent_kappa_assay",
        "comparative_covariation_only",
    ),
    "Kessler_2013_Petunia": (
        "component_partitioning_not_crossed",
        "cross_attractive_and_defensive_scent_components_in_same_plants_on_common_outcome",
        "selective_G_P_toggles;M0_delta;four_way_separability;independent_kappa_assay",
        "component_specific_lines_are_not_crossed_A_D",
    ),
    "Sun_Huang_2015_Pedicularis_rex": (
        "selective_D_system_anchor",
        "add_independent_attraction_manipulation_to_selective_D_backbone",
        "full_AxD_trait_factorial;true_selective_G_P_toggles;M0_delta;four_way_separability;independent_kappa_assay",
        "selective_D_exists_but_no_independent_A",
    ),
}

EXTRA_FIELDS = [
    "frontier_face",
    "next_major_augmentation",
    "remaining_gates_after_next_step",
    "conditional_partial_id_note",
]


def augment_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    ids = {row["study_id"] for row in rows}
    if ids != set(DERIVED):
        missing = sorted(ids - set(DERIVED))
        stale = sorted(set(DERIVED) - ids)
        raise ValueError(f"frontier mapping mismatch: missing={missing}, stale={stale}")
    out: list[dict[str, str]] = []
    for row in rows:
        face, next_step, remaining, partial = DERIVED[row["study_id"]]
        enriched = dict(row)
        enriched.update(
            frontier_face=face,
            next_major_augmentation=next_step,
            remaining_gates_after_next_step=remaining,
            conditional_partial_id_note=partial,
        )
        out.append(enriched)
    return out


def build_readout(rows: list[dict[str, str]]) -> str:
    faces = Counter(row["frontier_face"] for row in rows)
    direct = faces["direct_trait_factorial_anchor"]
    consumer = faces["consumer_factorial_anchor"]
    context = faces["randomized_context_anchor"]
    selective_d = faces["selective_D_system_anchor"]
    m0 = sum(row["M0_delta_status"] != "not_identified" for row in rows)
    kappa = sum(row["independent_kappa_status"] != "no" for row in rows)
    full = sum("full" in row["highest_recoverable_layer"] and "identification" in row["highest_recoverable_layer"] for row in rows)

    lines = [
        "# Identification frontier and minimum augmentation — v1",
        "",
        "## Screened-set result",
        "",
        f"The current audit contains **{len(rows)} high-information systems**. The strongest information modules are fragmented across different studies rather than accumulated in one design:",
        "",
        f"- direct A×D-like trait-factorial anchor: **{direct}/{len(rows)}** (Kessler et al. 2008; systemic-D scope caveat);",
        f"- consumer-factorial anchor: **{consumer}/{len(rows)}** (Egan et al. 2021);",
        f"- randomized-context anchor around an observational A×D term: **{context}/{len(rows)}** (Soper Gorden & Adler 2018);",
        f"- selective-D system anchor: **{selective_d}/{len(rows)}** (Sun & Huang 2015);",
        f"- characterized `m0_delta`: **{m0}/{len(rows)}**;",
        f"- independent joint-cost assay: **{kappa}/{len(rows)}**;",
        f"- full channel-allocation closure: **{full}/{len(rows)}**.",
        "",
        "The first four anchor classes are represented by four different studies. This is the empirical **design-fragmentation pattern**: the literature already contains much of the necessary biology and several sophisticated experimental modules, but those modules are distributed across systems.",
        "",
        "## Minimum-augmentation interpretation",
        "",
        "No scalar distance is assigned. The relevant next step depends on the information face already occupied:",
        "",
        "| anchor | current strength | minimum major augmentation | still required afterward |",
        "|---|---|---|---|",
    ]
    anchor_ids = [
        "Kessler_Gase_Baldwin_2008_Nicotiana",
        "Egan_2021_Fragaria",
        "Gorden_Adler_2018_Impatiens_capensis",
        "Sun_Huang_2015_Pedicularis_rex",
    ]
    by_id = {r["study_id"]: r for r in rows}
    labels = {
        anchor_ids[0]: "Kessler et al. 2008",
        anchor_ids[1]: "Egan et al. 2021",
        anchor_ids[2]: "Soper Gorden & Adler 2018",
        anchor_ids[3]: "Sun & Huang 2015",
    }
    strengths = {
        anchor_ids[0]: "direct A×D-like trait factorial",
        anchor_ids[1]: "consumer factorial",
        anchor_ids[2]: "observational A×D + randomized context modification",
        anchor_ids[3]: "selective flower-associated D manipulation",
    }
    for sid in anchor_ids:
        row = by_id[sid]
        lines.append(
            f"| {labels[sid]} | {strengths[sid]} | `{row['next_major_augmentation']}` | `{row['remaining_gates_after_next_step']}` |"
        )

    lines += [
        "",
        "## Conditional partial-identification recovery from Kessler et al. 2008",
        "",
        "The published rounded probability-scale interaction is `Delta_AD = +0.19 to +0.25`. Therefore, conditional on the explicit same-scale restriction `kappa_delta >= 0`,",
        "",
        "```text",
        "rho_delta - iota_delta >= +0.19",
        "```",
        "",
        "within those published aggregate constraints. This is **not a confidence bound** because source-level factorial uncertainty is unrecovered. It is an assumption-indexed aggregate-constraint bound. Equivalently, a hidden synergistic joint channel would need magnitude at least 0.19 on that probability scale before the sign of the biotic balance could be erased at the lower end of the published interaction range.",
        "",
        "## Scientific consequence",
        "",
        "The empirical gap is more specific than `no full experiment exists`. The current screened evidence contains distinct near-complete modules, but the modules are orthogonal across studies. The practical synthesis is therefore:",
        "",
        "> **Reuse the strongest existing backbone and add the missing module that most shrinks the identified set.**",
        "",
        "For a trait-factorial backbone this means selective consumer interventions; for a consumer-factorial backbone it means biologically valid crossed floral A/D coordinates; for a selective-D backbone it means an independent attraction manipulation. `m0_delta`, separability and independent joint-cost evidence remain downstream gates rather than reasons to discard those existing backbones.",
        "",
        "## Boundary",
        "",
        "These counts describe the current 16-system high-information screen, not literature prevalence. The augmentation labels are design recommendations derived from the recorded blockers; they are not claims that the added experiment is technically easy or uniquely optimal.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    with SOURCE.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    enriched = augment_rows(rows)
    fieldnames = list(rows[0]) + EXTRA_FIELDS
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(enriched)
    OUT_MD.write_text(build_readout(enriched), encoding="utf-8")


if __name__ == "__main__":
    main()
