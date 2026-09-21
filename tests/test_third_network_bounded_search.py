from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "empirical" / "floral_defence_selectivity" / "THIRD_NETWORK_BOUNDED_SEARCH_AUDIT_V1.md"
REGISTRY = ROOT / "empirical" / "floral_defence_selectivity" / "THIRD_NETWORK_CANDIDATE_REGISTRY_V1.csv"


def test_bounded_search_does_not_relax_k3_estimand() -> None:
    text = AUDIT.read_text(encoding="utf-8")
    assert "PUBLIC_THIRD_NETWORK = NOT_AVAILABLE" in text
    assert "CURRENT_JOINT_NETWORK_K = 2" in text
    assert "M = log(plant legitimate-route depth / visitor reach)" in text
    assert "Y = bypass / (bypass + legitimate)" in text
    assert "The estimand was not relaxed." in text


def test_closest_bat_candidate_fails_only_the_required_route_lane() -> None:
    text = AUDIT.read_text(encoding="utf-8")
    assert "10.7291/D1QX26" in text
    assert "frozen access mismatch: constructible" in text
    assert "frozen route outcome: absent" in text
    assert "cannot produce" in text


def test_registry_records_postfreeze_bat_network_near_misses() -> None:
    text = REGISTRY.read_text(encoding="utf-8")
    for token in (
        "Bat_flower_trait_matching_Dryad",
        "Caatinga_bat_flower_network_Dryad",
        "Pantanal_bat_flower_network_Dryad",
        "Neotropical_bat_plant_niche_overlap_Dryad",
        "Central_Mexico_bat_flower_network_Dryad",
    ):
        assert token in text
    assert text.count("INELIGIBLE_ROUTE_OUTCOME") >= 4
