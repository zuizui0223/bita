from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "empirical" / "identification_design" / "HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V1.csv"
OUT = ROOT / "empirical" / "identification_design" / "HYPERCUBE_FACE_COVERAGE_V1.csv"

FIELDS = [
    "study_id", "source", "A_coordinate", "D_coordinate", "G_intervention",
    "P_intervention", "face_label", "strict_target_status", "key_missing_for_ADGP",
]

FACE_SPEC = {
    "Kessler_Gase_Baldwin_2008_Nicotiana": {
        "face_label": "A_x_D_trait_face",
        "strict_target_status": "near_trait_face_not_strict_full",
        "key_missing_for_ADGP": "D_flower_specificity;G_toggle;P_toggle;M0;separability;kappa",
    },
    "Theis_Adler_2012_Cucurbita": {
        "face_label": "A_x_G_x_Psupp_face",
        "strict_target_status": "bridge_not_target_P_or_D",
        "key_missing_for_ADGP": "distinct_D;selective_P_access;M0;separability;kappa",
    },
    "Santangelo_2019_Trifolium": {
        "face_label": "D_x_G_x_Psupp_plus_observed_A_face",
        "strict_target_status": "cross_organ_D_and_nonaccess_P",
        "key_missing_for_ADGP": "manipulated_flower_specific_A_D;selective_P_access;M0;separability;kappa",
    },
    "Egan_2021_Fragaria": {
        "face_label": "G_x_P_consumer_face_plus_observed_A_D",
        "strict_target_status": "traits_not_crossed_and_D_not_floral",
        "key_missing_for_ADGP": "crossed_flower_specific_A_D;selective_P_access;M0;separability;kappa",
    },
    "Gorden_Adler_2018_Impatiens_capensis": {
        "face_label": "observed_A_D_x_randomized_context_face",
        "strict_target_status": "context_modification_not_selective_toggles",
        "key_missing_for_ADGP": "randomized_A_D;selective_G_P_access;M0;separability;kappa",
    },
    "Sun_Huang_2015_Pedicularis_rex": {
        "face_label": "selective_D_mechanism_face",
        "strict_target_status": "D_anchor_not_crossed_design",
        "key_missing_for_ADGP": "independent_A;separate_selective_G_P_toggles;M0;separability;kappa",
    },
}

# Output language is deliberately faithful to the source audit statuses.  Hand
# pollination is kept distinct from a pollinator-access toggle.
DISPLAY = {
    "Kessler_Gase_Baldwin_2008_Nicotiana": ("manipulated_floral_BA", "manipulated_nicotine_candidate_systemic_scope", "no", "no"),
    "Theis_Adler_2012_Cucurbita": ("manipulated_1_4_dimethoxybenzene_fragrance", "absent", "repeated_manual_beetle_removal", "supplemental_hand_pollination"),
    "Santangelo_2019_Trifolium": ("observed_floral_display_traits", "inherited_whole_plant_HCN", "herbivore_suppression", "hand_pollination"),
    "Egan_2021_Fragaria": ("observed_attraction_related_traits", "observed_leaf_defence_metabolites", "herbivory_presence_absence", "open_vs_hand_pollination"),
    "Gorden_Adler_2018_Impatiens_capensis": ("observed_flower_redness", "observed_floral_tannins", "randomized_robbing_and_florivory_intensity_additions", "randomized_pollination_intensity_addition"),
    "Sun_Huang_2015_Pedicularis_rex": ("absent", "manipulated_water_holding_bract", "D_changes_seed_predation_not_separate_G_toggle", "pollinator_response_measured"),
}


def build_rows(source_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    by_id = {row["study_id"]: row for row in source_rows}
    missing = sorted(set(FACE_SPEC) - set(by_id))
    if missing:
        raise ValueError(f"missing hypercube anchors from source audit: {missing}")
    out = []
    for sid in FACE_SPEC:
        source = by_id[sid]
        a, d, g, p = DISPLAY[sid]
        # Guard against silent drift in the underlying audit.
        if sid == "Theis_Adler_2012_Cucurbita":
            assert source["D_status"] == "absent"
            assert "manual_beetle_removal" in source["G_toggle_status"]
            assert "supplemental_hand_pollination" in source["P_toggle_status"]
            assert "not_access_toggle" in source["P_toggle_status"]
        if sid == "Santangelo_2019_Trifolium":
            assert source["D_status"] == "whole_plant_HCN_defence"
            assert source["G_toggle_status"] == "herbivory_manipulated"
            assert "pollination_context" in source["P_toggle_status"]
        spec = FACE_SPEC[sid]
        out.append({
            "study_id": sid,
            "source": source["source"],
            "A_coordinate": a,
            "D_coordinate": d,
            "G_intervention": g,
            "P_intervention": p,
            **spec,
        })
    return out


def main() -> None:
    with SOURCE.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    out = build_rows(rows)
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(out)


if __name__ == "__main__":
    main()
