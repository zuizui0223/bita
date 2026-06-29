from trait_architecture.trait_coverage_audit import audit_trait_coverage


def _manifest() -> list[dict[str, str]]:
    return [
        {
            "plant_taxon_as_reported": f"Plantus species{i}",
            "network_names": f"network_{i:02d}",
        }
        for i in range(40)
    ]


def _matrix() -> list[dict[str, str]]:
    return [
        {
            "trait_id": "sla",
            "functional_module": "Q_leaf",
            "evidence_grade": "B",
            "global_availability": "high",
            "provisional_role": "primary leaf quality candidate",
            "v1_decision": "retain_pending_coverage",
        },
        {
            "trait_id": "leaf_toughness",
            "functional_module": "B_leaf",
            "evidence_grade": "A",
            "global_availability": "low_medium",
            "provisional_role": "conditional leaf resistance candidate",
            "v1_decision": "hold_for_coverage_audit",
        },
    ]


def _receipt_row(plant: str, trait_id: str, *, imputed: str = "false", match: str = "exact") -> dict[str, str]:
    return {
        "plant_taxon": plant,
        "trait_id": trait_id,
        "trait_value": "12.5",
        "trait_unit": "m2 kg-1",
        "trait_source": "synthetic test receipt",
        "trait_observation_level": "species",
        "imputation_flag": imputed,
        "taxon_match_status": match,
    }


def test_primary_trait_requires_direct_plant_and_network_coverage() -> None:
    manifest = _manifest()
    receipt = [
        _receipt_row(row["plant_taxon_as_reported"], "sla")
        for row in manifest[:30]
    ]
    receipt.extend(
        _receipt_row(row["plant_taxon_as_reported"], "sla", imputed="true")
        for row in manifest[30:35]
    )

    report = audit_trait_coverage(manifest, _matrix(), receipt)
    sla = next(summary for summary in report.summaries if summary.trait_id == "sla")

    assert sla.direct_plants == 30
    assert sla.imputed_only_plants == 5
    assert sla.direct_coverage == 0.75
    assert sla.imputed_or_direct_coverage == 0.875
    assert sla.trait_ready_networks == 30
    assert sla.status == "ready_for_primary_analysis"


def test_conditional_trait_stays_conditional_after_passing_coverage() -> None:
    manifest = _manifest()
    receipt = [
        _receipt_row(row["plant_taxon_as_reported"], "leaf_toughness")
        for row in manifest[:35]
    ]

    report = audit_trait_coverage(manifest, _matrix(), receipt)
    toughness = next(summary for summary in report.summaries if summary.trait_id == "leaf_toughness")

    assert toughness.direct_coverage == 0.875
    assert toughness.status == "conditional_trait_requires_design_decision"


def test_unmatched_and_non_direct_records_do_not_count_as_direct_coverage() -> None:
    manifest = _manifest()
    receipt = [
        _receipt_row(row["plant_taxon_as_reported"], "sla", match="unmatched")
        for row in manifest[:30]
    ]
    receipt.append(_receipt_row("Not in manifest", "sla"))
    receipt.append(
        {
            **_receipt_row(manifest[30]["plant_taxon_as_reported"], "sla"),
            "trait_observation_level": "genus",
        }
    )

    report = audit_trait_coverage(manifest, _matrix(), receipt)
    sla = next(summary for summary in report.summaries if summary.trait_id == "sla")

    assert sla.direct_plants == 0
    assert sla.status == "insufficient_direct_coverage"
    assert report.invalid_receipt_rows == 32


def test_manifest_without_network_names_does_not_promote_a_trait() -> None:
    manifest = [{"plant_taxon": f"Plantus species{i}"} for i in range(40)]
    receipt = [_receipt_row(row["plant_taxon"], "sla") for row in manifest]

    report = audit_trait_coverage(manifest, _matrix(), receipt)
    sla = next(summary for summary in report.summaries if summary.trait_id == "sla")

    assert sla.direct_coverage == 1.0
    assert sla.trait_ready_networks == 0
    assert sla.status == "insufficient_direct_coverage"
    assert "Manifest has no network_names" in report.warnings[0]
