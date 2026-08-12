import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EMP = ROOT / "empirical" / "mechanism_pattern_synthesis"


def rows(name: str):
    with (EMP / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def test_expansion_ledger_has_two_new_independent_systems_and_no_direct_axd():
    data = rows("EXPANSION_LEDGER_BATCH_1_V1.csv")
    assert len(data) == 5
    assert {r["independence_cluster"] for r in data} == {
        "Sun_Huang_2015_Pedicularis_rex",
        "Perez_Barrales_2013_Dalechampia_scandens",
    }
    assert all(r["is_direct_AxD"].lower() == "false" for r in data)
    assert {r["route"] for r in data} <= {
        "A_to_pollination",
        "A_to_antagonism",
        "D_to_antagonism",
        "D_to_pollination",
    }


def test_pedicularis_is_one_cluster_with_guarded_and_attack_mode_states():
    data = [r for r in rows("EXPANSION_LEDGER_BATCH_1_V1.csv") if r["independence_cluster"] == "Sun_Huang_2015_Pedicularis_rex"]
    assert len(data) == 3
    assert {r["route"] for r in data} == {"D_to_pollination", "D_to_antagonism"}
    assert sum(r["route"] == "D_to_antagonism" for r in data) == 2
    assert all(r["is_same_system_multi_route"].lower() == "true" for r in data)


def test_dalechampia_is_visual_shared_tracking_not_defence():
    data = [r for r in rows("EXPANSION_LEDGER_BATCH_1_V1.csv") if r["independence_cluster"] == "Perez_Barrales_2013_Dalechampia_scandens"]
    assert len(data) == 2
    assert {r["route"] for r in data} == {"A_to_pollination", "A_to_antagonism"}
    assert all(r["trait_D_class"] == "" for r in data)
    assert all(r["trait_A_class"] == "showy_involucral_bract_area" for r in data)


def test_expansion_switch_rows_count_pedicularis_once():
    data = rows("EXPANSION_SIGN_SWITCH_BATCH_1_V1.csv")
    assert len(data) == 2
    assert {r["study_id"] for r in data} == {"Sun_Huang_2015_Pedicularis_rex"}
    assert {r["contrast_axis"] for r in data} == {
        "antagonist_identity_or_attack_mode",
        "consumer_function",
    }


def test_module_registry_keeps_distinct_inference_boundaries():
    data = rows("PATTERN_MODULE_REGISTRY_V2.csv")
    modules = {r["module_id"]: r for r in data}
    assert set(modules) == {"PM01", "PM02", "PM03", "PM04", "PM05"}
    assert modules["PM01"]["status"] == "ADMITTED_REPRODUCED"
    assert modules["PM02"]["status"] == "ADMITTED_REPRODUCED"
    assert "PENDING_SUPPLEMENT_REPRODUCTION" in modules["PM03"]["status"]
    assert "herbivory_equals_D" in modules["PM03"]["forbidden_inference"]
    assert "selection_gradient_equals_W_AD" in modules["PM04"]["forbidden_inference"]
    assert "obligate_equals_pollinator" in modules["PM05"]["forbidden_inference"]


def test_cross_module_matrix_preserves_direct_identification_gaps():
    data = rows("CROSS_MODULE_PATTERN_MATRIX_V2.csv")
    classes = {r["pattern_class"]: r for r in data}
    assert "direct_AxD_identification_gap" in classes
    assert "direct_joint_cost_gap" in classes
    assert "one_Impatiens_sign_unresolved" in classes["direct_AxD_identification_gap"]["source_level_expansion"]
    assert "no_strict_estimate" in classes["direct_joint_cost_gap"]["source_level_expansion"]
