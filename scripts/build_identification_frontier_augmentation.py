from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "empirical" / "identification_design" / "HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V2.csv"
OUT_CSV = ROOT / "empirical" / "identification_design" / "IDENTIFICATION_FRONTIER_AUGMENTATION_V1.csv"
OUT_MD = ROOT / "empirical" / "identification_design" / "IDENTIFICATION_FRONTIER_AUGMENTATION_V1.md"

DERIVED = {
    "Gorden_Adler_2018_Impatiens_capensis": ("randomized_context_anchor", "randomize_and_cross_valid_A_and_D_and_replace_intensity_additions_with_selective_G_P_toggles", "M0_delta;four_way_separability;independent_kappa_assay", "observational_AxD_target_intervals_cross_zero_so_no_sign_resolved_biotic_balance_from_current_data"),
    "Kessler_Gase_Baldwin_2008_Nicotiana": ("direct_trait_factorial_anchor", "resolve_flower_specific_D_scope_and_add_crossed_selective_G_P_toggles_to_existing_AxD_backbone", "M0_delta;four_way_separability;independent_kappa_assay", "published_rounded_probability_Delta_AD=+0.19_to_+0.25;conditional_on_same_scale_kappa>=0_biotic_balance_rho_minus_iota>=+0.19;aggregate_constraint_not_confidence_bound"),
    "Irwin_Adler_2006_Gelsemium": ("joint_trait_observational", "experimentally_cross_attraction_traits_with_nectar_gelsemine_on_common_reproductive_outcome", "selective_G_P_toggles;M0_delta;four_way_separability;independent_kappa_assay", "no_total_AxD_in_current_audit"),
    "Gross_Sun_Schiestl_2016_Gymnadenia": ("single_A_axis", "add_distinct_independently_manipulable_flower_associated_D_and_cross_with_scent", "common_AxD_outcome;selective_G_P_toggles;M0_delta;four_way_separability;independent_kappa_assay", "no_valid_D_axis"),
    "Dalechampia_linked_panel_candidate": ("unresolved_candidate", "verify_individual_level_A_D_linkage_and_common_outcome_before_any_mechanistic_allocation", "crossed_A_D_manipulation;selective_G_P_toggles;M0_delta;four_way_separability;independent_kappa_assay", "individual_level_linkage_not_verified"),
    "Strauss_Irwin_2004_Raphanus": ("joint_trait_observational", "put_petal_colour_and_defence_on_common_within_system_AxD_fitness_factorial", "selective_G_P_toggles;M0_delta;four_way_separability;independent_kappa_assay", "no_direct_AxD_common_outcome"),
    "Gronquist_2001_Hypericum": ("nonseparable_single_trait", "choose_distinct_attraction_and_defence_coordinates_before_testing_AxD", "crossed_A_D_manipulation;common_outcome;selective_G_P_toggles;M0_delta;four_way_separability;independent_kappa_assay", "A_and_D_are_same_trait_axis"),
    "Kessler_2015_Nicotiana": ("phenotype_factorial_invalid_D", "replace_nectar_reward_axis_with_independently_justified_antagonist_reducing_D_while_retaining_2x2_floral_phenotype", "shared_reproductive_AxD;selective_G_P_toggles;M0_delta;four_way_separability;independent_kappa_assay", "second_axis_is_reward_not_valid_D"),
    "Santangelo_2019_Trifolium": ("cross_organ_trait_defence", "use_flower_specific_D_and_manipulate_A_on_same_floral_coordinates", "strict_flower_AxD_factorial;selective_P_toggle;M0_delta;four_way_separability;independent_kappa_assay", "current_D_is_whole_plant_and_A_is_not_manipulated"),
    "Egan_2021_Fragaria": ("consumer_factorial_anchor", "cross_independently_manipulable_flower_specific_A_and_D_onto_existing_consumer_factorial_backbone", "M0_delta;four_way_separability;independent_kappa_assay", "consumer_factorial_exists_but_focal_A_D_are_not_crossed_and_D_is_leaf_specific"),
    "Garcia_2024_Asclepias": ("joint_trait_observational", "add_experimental_AxD_cross_on_common_outcome_to_flower_specific_latex_system", "selective_G_P_toggles;M0_delta;four_way_separability;independent_kappa_assay", "current_data_have_main_effects_only"),
    "Knauer_Schiestl_2017_Brassica": ("single_A_multiroute", "add_distinct_flower_associated_D_axis_and_cross_with_attraction_signals", "common_AxD_outcome;selective_G_P_toggles;M0_delta;four_way_separability;independent_kappa_assay", "no_distinct_D_axis"),
    "Strauss_1999_Brassica": ("cross_organ_consumer_context", "replace_whole_plant_D_with_flower_specific_D_and_manipulate_A_within_existing_damage_context", "strict_flower_AxD_factorial;selective_P_toggle;M0_delta;four_way_separability;independent_kappa_assay", "current_D_is_whole_plant_and_A_is_not_manipulated"),
    "Hanley_2009_Hakea": ("comparative_joint_trait_covariance", "move_comparative_A_D_covariance_to_within_system_crossed_AxD_manipulation", "common_reproductive_outcome;selective_G_P_toggles;M0_delta;four_way_separability;independent_kappa_assay", "comparative_covariation_only"),
    "Kessler_2013_Petunia": ("component_partitioning_not_crossed", "cross_attractive_and_defensive_scent_components_in_same_plants_on_common_outcome", "selective_G_P_toggles;M0_delta;four_way_separability;independent_kappa_assay", "component_specific_lines_are_not_crossed_A_D"),
    "Sun_Huang_2015_Pedicularis_rex": ("selective_D_system_anchor", "add_independent_attraction_manipulation_to_selective_D_backbone", "full_AxD_trait_factorial;true_selective_G_P_toggles;M0_delta;four_way_separability;independent_kappa_assay", "selective_D_exists_but_no_independent_A"),
    "Theis_Adler_2012_Cucurbita": ("A_G_pollination_bridge_anchor", "add_distinct_flower_associated_D_and_replace_or_complement_hand_pollination_with_selective_P_access_toggle", "full_AxD_trait_factorial;M0_delta;four_way_separability;independent_kappa_assay", "A_is_manipulated_and_crossed_with_beetle_removal_and_hand_pollination_but_D_is_absent_and_P_is_not_access_toggle"),
}

EXTRA_FIELDS = ["frontier_face", "next_major_augmentation", "remaining_gates_after_next_step", "conditional_partial_id_note"]


def augment_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    ids = {row["study_id"] for row in rows}
    if ids != set(DERIVED):
        missing = sorted(ids - set(DERIVED))
        stale = sorted(set(DERIVED) - ids)
        raise ValueError(f"frontier mapping mismatch: missing={missing}, stale={stale}")
    out = []
    for row in rows:
        face, next_step, remaining, partial = DERIVED[row["study_id"]]
        enriched = dict(row)
        enriched.update(frontier_face=face, next_major_augmentation=next_step, remaining_gates_after_next_step=remaining, conditional_partial_id_note=partial)
        out.append(enriched)
    return out


def build_readout(rows: list[dict[str, str]]) -> str:
    faces = Counter(row["frontier_face"] for row in rows)
    n = len(rows)
    m0 = sum(row["M0_delta_status"] != "not_identified" for row in rows)
    kappa = sum(row["independent_kappa_status"] != "no" for row in rows)
    full = sum("full" in row["highest_recoverable_layer"] and "identification" in row["highest_recoverable_layer"] for row in rows)
    anchor_specs = [
        ("Kessler_Gase_Baldwin_2008_Nicotiana", "Kessler et al. 2008", "direct A×D-like trait factorial"),
        ("Egan_2021_Fragaria", "Egan et al. 2021", "consumer factorial"),
        ("Gorden_Adler_2018_Impatiens_capensis", "Soper Gorden & Adler 2018", "observational A×D + randomized context modification"),
        ("Sun_Huang_2015_Pedicularis_rex", "Sun & Huang 2015", "selective flower-associated D manipulation"),
        ("Theis_Adler_2012_Cucurbita", "Theis & Adler 2012", "manipulated A × beetle-removal × pollination-supplementation bridge"),
    ]
    by_id = {r["study_id"]: r for r in rows}
    lines = [
        "# Identification frontier and minimum augmentation — v1", "", "## Screened-set result", "",
        f"The current audit contains **{n} high-information systems**. The strongest information modules are fragmented across different studies rather than accumulated in one design:", "",
        f"- direct A×D-like trait-factorial anchor: **{faces['direct_trait_factorial_anchor']}/{n}** (Kessler et al. 2008; systemic-D scope caveat);",
        f"- consumer-factorial anchor: **{faces['consumer_factorial_anchor']}/{n}** (Egan et al. 2021);",
        f"- randomized-context anchor around an observational A×D term: **{faces['randomized_context_anchor']}/{n}** (Soper Gorden & Adler 2018);",
        f"- selective-D system anchor: **{faces['selective_D_system_anchor']}/{n}** (Sun & Huang 2015);",
        f"- manipulated A × antagonist-removal × pollination-supplementation bridge: **{faces['A_G_pollination_bridge_anchor']}/{n}** (Theis & Adler 2012);",
        f"- characterized `m0_delta`: **{m0}/{n}**;",
        f"- independent joint-cost assay: **{kappa}/{n}**;",
        f"- full channel-allocation closure: **{full}/{n}**.", "",
        "The five strongest frontier faces above are represented by **five different studies**. This is the empirical design-fragmentation pattern: sophisticated pieces of the target architecture already exist, including a three-factor attraction–consumer bridge, but they are distributed across systems.", "",
        "Theis & Adler (2012) is especially informative because fragrance enhancement, repeated beetle removal, and supplemental hand pollination were crossed on female flowers. Hand pollination is not a pollinator-access toggle, so this remains a bridge rather than channel identification.", "",
        "## Minimum-augmentation interpretation", "", "No scalar distance is assigned. The relevant next step depends on the information face already occupied:", "",
        "| anchor | current strength | minimum major augmentation | still required afterward |", "|---|---|---|---|",
    ]
    for sid, label, strength in anchor_specs:
        row = by_id[sid]
        lines.append(f"| {label} | {strength} | `{row['next_major_augmentation']}` | `{row['remaining_gates_after_next_step']}` |")
    lines += [
        "", "## Hierarchical bottleneck", "",
        "The target design is not missing wholesale. Theis & Adler (2012) already crosses a manipulated attraction signal with an antagonist-removal treatment and a pollination-supplementation treatment; Kessler et al. (2008) supplies the strongest A×D-like trait factorial; Egan et al. (2021) supplies the strongest consumer-factorial backbone; and Sun & Huang (2015) supplies a selective-D mechanism. The bottleneck is their **intersection on valid A/D coordinates with selective consumer access and baseline/cost closure**.", "",
        "`m0_delta` and independent `kappa` assays remain absent across the screened set, but they are downstream gates: many studies stop earlier because a distinct A/D factorial or target-style consumer access contrast is missing.", "",
        "## Conditional partial-identification recovery from Kessler et al. 2008", "",
        "The published rounded probability-scale interaction is `Delta_AD = +0.19 to +0.25`. Conditional on the explicit same-scale restriction `kappa_delta >= 0`,", "", "```text", "rho_delta - iota_delta >= +0.19", "```", "",
        "within those published aggregate constraints. This is **not a confidence bound** because source-level factorial uncertainty is unrecovered. It is an assumption-indexed aggregate-constraint bound. A hidden synergistic joint channel would need magnitude at least 0.19 on that probability scale before the positive biotic balance could be erased at the lower end of the published range.", "",
        "## Scientific consequence", "",
        "> **Constituent channels recur, and multiple near-complete experimental modules already exist, but the modules occupy different studies. Mechanism allocation is blocked by design fragmentation rather than by absence of relevant biology.**", "",
        "> **Reuse the strongest existing backbone and add the missing module that most shrinks the identified set.**", "",
        "For Theis & Adler (2012), this means adding a distinct D coordinate and a true pollinator-access/baseline treatment to an existing A×G×pollination-supplementation backbone. For Kessler (2008), it means selective consumer interventions; for Egan (2021), valid crossed floral A/D coordinates; for Pedicularis, an independent attraction manipulation.", "",
        "## Boundary", "",
        f"These counts describe the current **{n}-system high-information screen**, not literature prevalence. The augmentation labels are design recommendations derived from recorded blockers; they are not claims that the proposed additions are technically easy, uniquely optimal, or already validated. No study-specific `rho_delta`, `iota_delta`, or `kappa_delta` point values are inferred.",
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
