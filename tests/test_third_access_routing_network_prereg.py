from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "empirical" / "floral_defence_selectivity" / "THIRD_ACCESS_ROUTING_NETWORK_PREREG_V1.md"
REGISTRY = ROOT / "empirical" / "floral_defence_selectivity" / "THIRD_NETWORK_CANDIDATE_REGISTRY_V1.csv"
SEARCH_AUDIT = ROOT / "empirical" / "floral_defence_selectivity" / "THIRD_NETWORK_BOUNDED_SEARCH_V1.md"
PROSPECTIVE_DESIGN = ROOT / "empirical" / "floral_defence_selectivity" / "THIRD_NETWORK_PROSPECTIVE_MAMMAL_DESIGN_V1.md"
PROSPECTIVE_SCHEMA = ROOT / "empirical" / "floral_defence_selectivity" / "THIRD_NETWORK_PROSPECTIVE_SCHEMA_V1.csv"
ROUTE_MANUAL = ROOT / "empirical" / "floral_defence_selectivity" / "THIRD_NETWORK_ROUTE_CODING_MANUAL_V1.md"
PILOT_SPLIT = ROOT / "empirical" / "floral_defence_selectivity" / "THIRD_NETWORK_PILOT_SPLIT_CONTRACT_V1.md"
SEED_RECEIPT = ROOT / "empirical" / "floral_defence_selectivity" / "THIRD_NETWORK_SEED_RECEIPT_V1.json"
FREEZE_TEMPLATE = ROOT / "empirical" / "floral_defence_selectivity" / "THIRD_NETWORK_CONFIRMATORY_FREEZE_RECEIPT_TEMPLATE_V1.json"


def test_third_network_estimand_is_frozen_before_confirmatory_outcome_search() -> None:
    text = PREREG.read_text(encoding="utf-8")
    for token in (
        "FREEZE_STATUS = PRE_OUTCOME_CONFIRMATORY",
        "TARGET_FAUNA = NON_INSECTA_NON_AVES",
        "OUTCOME_DIRECTION_MUST_NOT_BE_USED_FOR_DATASET_SELECTION",
        "visitor species x plant species x site/context stratum",
        "M_ij = log(P_j / V_i)",
        "Y = B / (B + L)",
        "at least **30** inferential units",
        "at least **5 visitor species**",
        "at least **5 plant species**",
        "9,999",
        "DISCOVERY_EXPOSED_NOT_CONFIRMATORY",
        "stop searching for a more favorable dataset",
    ):
        assert token in text


def test_third_network_k3_statistic_is_equal_network_and_nonpooled() -> None:
    text = PREREG.read_text(encoding="utf-8")
    assert "r_J3" in text
    assert "Each network has equal weight." in text
    assert "No raw observations are pooled." in text
    assert "universal causality" in text
    assert "estimated between-network heterogeneity" in text


def test_exposed_candidates_cannot_reenter_confirmatory_lane() -> None:
    text = REGISTRY.read_text(encoding="utf-8")
    assert "Xiao_2022_Mucuna_sempervirens" in text
    assert "DinizAguiar_2023_bat_flower" in text
    assert "Mucuna_macrocarpa_Dryad" in text
    assert text.count("DISCOVERY_EXPOSED_NOT_CONFIRMATORY") >= 5


def test_bounded_search_closes_without_relaxing_third_network_estimand() -> None:
    text = SEARCH_AUDIT.read_text(encoding="utf-8")
    for token in (
        "PUBLIC_THIRD_NETWORK = NOT_AVAILABLE",
        "NO_PUBLIC_DATASET_PASSED_ALL_FROZEN_ELIGIBILITY_GATES",
        "ESTIMAND_RELAXATION = PROHIBITED",
        "EXISTING_CONFIRMATORY_NETWORKS = 2",
        "PUBLIC_SCHEMA_ELIGIBLE_THIRD_NETWORK = 0",
        "JOINT_NETWORK_K = 2",
        "K3_PUBLIC_REANALYSIS = NOT_CURRENTLY_AVAILABLE",
        "newly released public dataset",
        "prospective third-fauna field dataset",
    ):
        assert token in text


def test_postfreeze_registry_contains_schema_failures_not_selected_outcomes() -> None:
    text = REGISTRY.read_text(encoding="utf-8")
    for candidate in (
        "MaguinaConde_2024_bat_trait_matching",
        "Caatinga_bat_flower_network",
        "Pantanal_bat_flower_network",
        "NeoBat_interactions",
        "Yungas_bat_pollination",
        "Cneorum_Podarcis",
        "Grizzled_giant_squirrel_feeding",
        "Flower_eDNA_multitaxon",
    ):
        assert candidate in text
    assert "INELIGIBLE_NO_ROUTE_OUTCOME" in text
    assert "INELIGIBLE_PLANT_RICHNESS" in text
    assert "INELIGIBLE_VISITOR_RICHNESS" in text


def test_prospective_mammal_design_preserves_frozen_estimand() -> None:
    text = PROSPECTIVE_DESIGN.read_text(encoding="utf-8")
    for token in (
        "FAUNA = NON_FLYING_MAMMALIA",
        "PRIMARY_ESTIMAND = UNCHANGED",
        "target realized units     >= 70",
        "pilot events are never included in the confirmatory analysis",
        "M_ij = log(P_j / V_i)",
        "Y = B / (B + L)",
        "Morphology and route tables are joined only after both are checksum-frozen",
        "target kappa >=0.80",
        "INELIGIBLE_CONFIRMATORY_DATASET",
        "If the prospective mammal network passes the sampling gates but r_T is",
    ):
        assert token in text

    schema = PROSPECTIVE_SCHEMA.read_text(encoding="utf-8")
    for column in (
        "route_code",
        "access_depth_mm",
        "rostral_reach_mm",
        "M_log_ratio",
        "B_count",
        "L_count",
        "Y_bypass_prop",
    ):
        assert column in schema


def test_route_coding_and_pilot_split_are_frozen_before_data() -> None:
    manual = ROUTE_MANUAL.read_text(encoding="utf-8")
    split = PILOT_SPLIT.read_text(encoding="utf-8")
    seed = SEED_RECEIPT.read_text(encoding="utf-8")

    for token in (
        "MORPHOLOGY_BLIND = REQUIRED",
        "L = LEGITIMATE",
        "B = BYPASS",
        "A = AMBIGUOUS",
        "N = NON_NECTAR / NOT A FEEDING EVENT",
        "kappa_LBAN >= 0.80",
        "Y = B_count / (B_count + L_count)",
    ):
        assert token in manual

    assert "PILOT_EVENTS_IN_CONFIRMATORY_ANALYSIS = FORBIDDEN" in split
    assert "confirmatory unit builder accepts **CONFIRMATORY only**" in split
    assert '"third_network_permutation_seed": 20260921' in seed
    assert '"pilot_events_allowed_in_confirmatory_analysis": false' in seed


def test_confirmatory_builder_exists_as_only_supported_data_entry() -> None:
    path = ROOT / "scripts" / "build_third_access_routing_units.py"
    text = path.read_text(encoding="utf-8")
    assert "PILOT_OR_NONCONFIRMATORY_EVENT_SUPPLIED" in text
    assert 'roles != {"CONFIRMATORY"}' in text
    assert "M_log_ratio" in text
    assert "Y_bypass_prop" in text



def test_pilot_route_presence_is_not_a_site_selection_gate() -> None:
    design = PROSPECTIVE_DESIGN.read_text(encoding="utf-8")
    split = PILOT_SPLIT.read_text(encoding="utf-8")
    template = FREEZE_TEMPLATE.read_text(encoding="utf-8")

    assert "no site, plant species or mammal species is retained or dropped because B or L" in design
    assert "Observed absence of B or L in pilot footage is **not** a pilot-failure criterion." in split
    assert '"pilot_B_or_L_presence_used_for_selection": false' in template
    assert '"may_extend_based_on_route_outcomes": false' in template
