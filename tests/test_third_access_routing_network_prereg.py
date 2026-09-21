from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "empirical" / "floral_defence_selectivity" / "THIRD_ACCESS_ROUTING_NETWORK_PREREG_V1.md"
REGISTRY = ROOT / "empirical" / "floral_defence_selectivity" / "THIRD_NETWORK_CANDIDATE_REGISTRY_V1.csv"


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
