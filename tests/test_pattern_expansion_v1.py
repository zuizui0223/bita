import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EMP = ROOT / "empirical" / "mechanism_pattern_synthesis"


def rows(name: str):
    with (EMP / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def all_expansion_rows():
    out = []
    for path in sorted(EMP.glob("EXPANSION_LEDGER_BATCH_*_V1.csv")):
        with path.open(newline="", encoding="utf-8") as fh:
            out.extend(csv.DictReader(fh))
    return out


def all_switch_rows():
    out = []
    for path in sorted(EMP.glob("EXPANSION_SIGN_SWITCH_BATCH_*_V1.csv")):
        with path.open(newline="", encoding="utf-8") as fh:
            out.extend(csv.DictReader(fh))
    return out


def test_expansion_ledger_has_eleven_new_independent_systems_and_no_direct_axd():
    data = all_expansion_rows()
    assert len(data) == 18
    assert {r["independence_cluster"] for r in data} == {
        "Sun_Huang_2015_Pedicularis_rex",
        "Perez_Barrales_2013_Dalechampia_scandens",
        "McCall_2013_Raphanus_sativus",
        "Chauta_2022_Bejaria_resinosa",
        "Stephenson_1982_Catalpa_speciosa",
        "McCarren_2021_Erica",
        "Takeda_2021_slippery_perianths",
        "Tagawa_2018_Menyanthes_trifoliata",
        "Wu_Gao_2024_Thunia_alba",
        "Carlson_Harms_2007_Chrysothemis",
        "Page_2014_Silene_signals",
    }
    assert all(r["is_direct_AxD"].lower() == "false" for r in data)


def test_pedicularis_is_one_cluster_with_guarded_and_attack_mode_states():
    data = [r for r in all_expansion_rows() if r["independence_cluster"] == "Sun_Huang_2015_Pedicularis_rex"]
    assert len(data) == 3
    assert {r["route"] for r in data} == {"D_to_pollination", "D_to_antagonism"}
    assert all(r["is_same_system_multi_route"].lower() == "true" for r in data)


def test_dalechampia_is_visual_shared_tracking_not_defence():
    data = [r for r in all_expansion_rows() if r["independence_cluster"] == "Perez_Barrales_2013_Dalechampia_scandens"]
    assert len(data) == 2
    assert {r["route"] for r in data} == {"A_to_pollination", "A_to_antagonism"}
    assert all(r["trait_D_class"] == "" for r in data)


def test_raphanus_adds_visual_a_to_antagonism_only():
    data = [r for r in all_expansion_rows() if r["independence_cluster"] == "McCall_2013_Raphanus_sativus"]
    assert len(data) == 1
    row = data[0]
    assert row["route"] == "A_to_antagonism"
    assert row["trait_A_class"] == "petal_color_white_vs_pink"
    assert row["trait_D_class"] == ""


def test_bejaria_adds_one_flower_specific_d_cluster_without_fake_pollinator_route():
    data = [r for r in all_expansion_rows() if r["independence_cluster"] == "Chauta_2022_Bejaria_resinosa"]
    assert len(data) == 2
    assert {r["route"] for r in data} == {"D_to_antagonism"}
    assert all(r["trait_D_class"] == "petal_sepal_stickiness" for r in data)
    assert all(r["is_same_system_multi_route"].lower() == "false" for r in data)


def test_catalpa_is_same_system_chemical_guarded_state():
    data = [r for r in all_expansion_rows() if r["independence_cluster"] == "Stephenson_1982_Catalpa_speciosa"]
    assert len(data) == 2
    assert {r["route"] for r in data} == {"D_to_antagonism", "D_to_pollination"}
    assert all(r["trait_D_class"] == "floral_nectar_iridoid_glycosides" for r in data)
    assert all(r["is_same_system_multi_route"].lower() == "true" for r in data)
    poll = next(r for r in data if r["route"] == "D_to_pollination")
    assert "no_detected_reduction" in poll["effect_orientation"]


def test_erica_adds_one_experimental_surface_defence_cluster():
    data = [r for r in all_expansion_rows() if r["independence_cluster"] == "McCarren_2021_Erica"]
    assert len(data) == 1
    row = data[0]
    assert row["route"] == "D_to_antagonism"
    assert row["trait_D_class"] == "corolla_surface_stickiness"
    assert row["study_design"].startswith("within_species_experimental")


def test_slippery_perianths_count_two_species_as_one_study_cluster():
    data = [r for r in all_expansion_rows() if r["independence_cluster"] == "Takeda_2021_slippery_perianths"]
    assert len(data) == 2
    assert {r["plant_taxon"] for r in data} == {"Codonopsis lanceolata", "Fritillaria koidzumiana"}
    assert {r["route"] for r in data} == {"D_to_antagonism"}
    assert all(r["trait_D_class"] == "epicuticular_wax_slippery_perianth" for r in data)
    assert sum(r["is_primary_effect"].lower() == "true" for r in data) == 1
    assert all(r["is_direct_AxD"].lower() == "false" for r in data)


def test_menyanthes_is_clean_flower_specific_hair_barrier():
    data = [r for r in all_expansion_rows() if r["independence_cluster"] == "Tagawa_2018_Menyanthes_trifoliata"]
    assert len(data) == 1
    row = data[0]
    assert row["route"] == "D_to_antagonism"
    assert row["trait_D_class"] == "dense_petal_hairs"
    assert "hair_trimming" in row["study_design"]
    assert row["is_same_system_multi_route"].lower() == "false"


def test_thunia_routes_same_bombus_between_legitimate_and_robbing_modes():
    data = [r for r in all_expansion_rows() if r["independence_cluster"] == "Wu_Gao_2024_Thunia_alba"]
    assert len(data) == 2
    assert {r["route"] for r in data} == {"D_to_antagonism", "D_to_pollination"}
    assert all(r["trait_D_class"] == "large_spur_enclosing_floral_bract" for r in data)
    assert all(r["is_same_system_multi_route"].lower() == "true" for r in data)
    poll = next(r for r in data if r["route"] == "D_to_pollination")
    assert "without_higher_visit_frequency" in poll["effect_orientation"]


def test_chrysothemis_is_independent_water_calyx_d_to_antagonism():
    data = [r for r in all_expansion_rows() if r["independence_cluster"] == "Carlson_Harms_2007_Chrysothemis"]
    assert len(data) == 1
    row = data[0]
    assert row["route"] == "D_to_antagonism"
    assert row["trait_D_class"] == "liquid_filled_water_calyx"
    assert row["source_effect_metric"] == "reported_odds_ratio"
    assert row["effect_value"] == "2.18"


def test_silene_f2_adds_multidimensional_a_to_antagonism_only():
    data = [r for r in all_expansion_rows() if r["independence_cluster"] == "Page_2014_Silene_signals"]
    assert len(data) == 1
    row = data[0]
    assert row["route"] == "A_to_antagonism"
    assert row["trait_A_class"] == "flower_color_and_floral_scent"
    assert row["trait_D_class"] == ""
    assert row["is_same_system_multi_route"].lower() == "false"


def test_expansion_switch_rows_have_six_unique_new_context_clusters():
    data = all_switch_rows()
    assert len(data) == 10
    assert {r["study_id"] for r in data} == {
        "Sun_Huang_2015_Pedicularis_rex",
        "Chauta_et_al_2022_Bejaria_resinosa",
        "Stephenson_1982_Catalpa_speciosa",
        "Saabna_et_al_2025_Anemone_coronaria",
        "Wu_Gao_2024_Thunia_alba",
        "Dudash_et_al_2020_Silene_stellata",
    }
    thunia = next(r for r in data if r["study_id"] == "Wu_Gao_2024_Thunia_alba")
    assert thunia["contrast_axis"] == "defence_state_and_consumer_function"
    silene = next(r for r in data if r["study_id"] == "Dudash_et_al_2020_Silene_stellata")
    assert silene["contrast_axis"] == "consumer_lifecycle_stage_and_fitness_pathway"


def test_context_programs_are_explicitly_excluded_from_route_n():
    data = rows("EXPANSION_CONTEXT_PROGRAMS_V1.csv")
    assert len(data) == 7
    assert {r["program_id"] for r in data} == {"CTX001", "CTX002", "CTX003", "CTX004", "CTX005", "CTX006", "CTX007"}
    assert all(r["route_ledger_counted"].lower() == "false" for r in data)
    anemone = next(r for r in data if r["program_id"] == "CTX004")
    assert "mutualist and antagonist roles" in anemone["admitted_inference"]
    slippery = next(r for r in data if r["program_id"] == "CTX005")
    assert "pollinator-handling pathway" in slippery["admitted_inference"]
    aquilegia = next(r for r in data if r["program_id"] == "CTX006")
    assert "inflorescence_stalk_trichomes_equals_flower_specific_D" in aquilegia["forbidden_inference"]
    lifecycle = next(r for r in data if r["program_id"] == "CTX007")
    assert "reverse ecological role across its lifecycle" in lifecycle["admitted_inference"]


def test_module_registry_keeps_distinct_inference_boundaries():
    data = rows("PATTERN_MODULE_REGISTRY_V2.csv")
    modules = {r["module_id"]: r for r in data}
    assert set(modules) == {"PM01", "PM02", "PM03", "PM04", "PM05"}
    assert modules["PM01"]["status"] == "ADMITTED_REPRODUCED"
    assert modules["PM02"]["status"] == "ADMITTED_REPRODUCED"
    assert modules["PM03"]["status"] == "ADMITTED_PUBLISHED_META_SUPPLEMENT_PACKAGE_VERIFIED"
    assert "herbivory_equals_D" in modules["PM03"]["forbidden_inference"]
    assert modules["PM04"]["status"] == "ADMIT_AS_SECONDARY_SELECTION_CONTEXT_ACCESS_LIMITED"
    assert "selection_gradient_equals_W_AD" in modules["PM04"]["forbidden_inference"]
    assert "obligate_equals_pollinator" in modules["PM05"]["forbidden_inference"]


def test_cross_module_matrix_preserves_direct_gaps_and_new_classes():
    data = rows("CROSS_MODULE_PATTERN_MATRIX_V2.csv")
    classes = {r["pattern_class"]: r for r in data}
    for required in (
        "guarded_defence_state",
        "spatial_or_temporal_filtering",
        "pollinator_functional_mode_routing",
        "lifecycle_stage_role_reversal",
        "direct_AxD_identification_gap",
        "direct_joint_cost_gap",
    ):
        assert required in classes
    assert "Silene_stellata" in classes["lifecycle_stage_role_reversal"]["source_level_expansion"]
    assert "one_Impatiens_sign_unresolved" in classes["direct_AxD_identification_gap"]["source_level_expansion"]
    assert "no_strict_estimate" in classes["direct_joint_cost_gap"]["source_level_expansion"]
