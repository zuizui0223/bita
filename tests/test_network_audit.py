from trait_architecture.network_audit import audit_network_coverage, report_to_dict


def make_rows(networks=30, regions=3, matched=True, weighted=True):
    interactions = []
    metadata = []
    traits = []
    for index in range(networks):
        network_id = f"n{index}"
        plant = f"Plantus {index}"
        interactions.append(
            {
                "network_id": network_id,
                "interaction_type": "pollination",
                "plant_taxon": plant,
                "animal_taxon": f"Animalus {index}",
                "weight": "1" if weighted else "",
                "citation_id": "doi:example",
                "sampling_period": "2025",
            }
        )
        metadata.append({"network_id": network_id, "region": f"region{index % regions}"})
        if matched:
            traits.append(plant)
    return interactions, metadata, traits


def test_backbone_candidate_requires_networks_regions_and_trait_coverage():
    interactions, metadata, traits = make_rows()
    report = audit_network_coverage(interactions, metadata, traits)
    assert report.status == "backbone_candidate"
    assert report.networks == 30
    assert report.plant_trait_match_rate == 1.0
    assert report.weighted_rows == 30


def test_presence_only_networks_warn_but_can_remain_pilot():
    interactions, metadata, traits = make_rows(networks=10, regions=3, weighted=False)
    report = audit_network_coverage(interactions, metadata, traits)
    assert report.status == "pilot_candidate"
    assert any("No interaction weights" in warning for warning in report.warnings)


def test_low_trait_coverage_is_not_backbone_candidate():
    interactions, metadata, _ = make_rows()
    report = audit_network_coverage(interactions, metadata, ["Plantus 0"])
    assert report.status == "insufficient"
    assert report.plant_trait_match_rate < 0.60


def test_multiple_interaction_types_are_flagged_not_silently_pooled():
    interactions, metadata, traits = make_rows(networks=10)
    interactions[0]["interaction_type"] = "herbivory"
    report = audit_network_coverage(interactions, metadata, traits)
    assert len(report.interaction_types) == 2
    assert any("Multiple interaction types" in warning for warning in report.warnings)
    assert report_to_dict(report)["interaction_types"] == ["herbivory", "pollination"]
