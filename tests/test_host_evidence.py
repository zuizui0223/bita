from trait_architecture.host_evidence import (
    build_query_rows,
    deduplicate_metadata,
    primary_host_universe,
    validate_host_evidence_record,
)


def primary_row(**updates: str) -> dict[str, str]:
    row = {
        "record_id": "r1",
        "bee_name_reported": "Megachile example",
        "bee_name_accepted": "Megachile example",
        "plant_name_reported": "Rosa multiflora",
        "plant_name_accepted": "Rosa multiflora",
        "interaction_type": "leaf_cutting_direct",
        "evidence_grade": "A",
        "record_basis": "nest observation",
        "country": "Japan",
        "source_type": "article",
        "source_id": "src_1",
        "source_locator": "p. 2",
        "taxon_reconciliation_status": "accepted",
        "include_in_primary_host_universe": "TRUE",
    }
    row.update(updates)
    return row


def test_query_builder_makes_bilingual_queries() -> None:
    output = build_query_rows(({"bee_name_accepted": "Megachile example", "bee_name_japanese": "例ハキリバチ"},))
    assert len(output) == 11
    assert {row["language"] for row in output} == {"en", "ja"}
    assert len({row["query_id"] for row in output}) == len(output)


def test_deduplication_prefers_record_with_doi_and_abstract() -> None:
    raw = (
        {"provider": "crossref", "provider_record_id": "a", "title": "Leaf cutting by Megachile", "publication_year": "2020", "first_author": "A", "doi": "", "abstract": ""},
        {"provider": "openalex", "provider_record_id": "b", "title": "Leaf cutting by Megachile", "publication_year": "2020", "first_author": "A", "doi": "10.1/example", "abstract": "useful abstract"},
    )
    kept, discarded = deduplicate_metadata(raw)
    assert len(kept) == 1
    assert kept[0]["doi"] == "10.1/example"
    assert len(discarded) == 1
    assert discarded[0]["discarded_provider_record_id"] == "a"


def test_primary_record_validates() -> None:
    errors, warnings = validate_host_evidence_record(primary_row())
    assert errors == []
    assert warnings == []


def test_floral_visit_cannot_be_primary() -> None:
    errors, _ = validate_host_evidence_record(primary_row(interaction_type="floral_visit_only"))
    assert any("does not meet" in error for error in errors)


def test_host_universe_aggregates_valid_primary_records() -> None:
    rows = (
        primary_row(),
        primary_row(record_id="r2", source_id="src_2", bee_name_accepted="Megachile second", evidence_grade="B"),
        primary_row(record_id="r3", plant_name_accepted="Acer palmatum", include_in_primary_host_universe="FALSE"),
    )
    output = primary_host_universe(rows)
    assert len(output) == 1
    assert output[0]["plant_name_accepted"] == "Rosa multiflora"
    assert output[0]["number_of_direct_records"] == "2"
    assert output[0]["number_of_bee_species"] == "2"
    assert output[0]["evidence_grade_best"] == "A"
