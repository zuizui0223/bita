from dataclasses import dataclass, field

from scripts.bulk_scout_openalex_public_sources import build_row


@dataclass
class CandidateFixture:
    candidate_id: str = "openalex:W1"
    title: str = "Example floral trait paper"
    doi: str = "https://doi.org/10.1111/example"
    publication_year: str = "2024"
    seed_routes: set[str] = field(default_factory=lambda: {"floral_damage_traits"})
    metadata_match_score: int = 4
    metadata_attraction_signal: bool = True
    metadata_barrier_signal: bool = False
    metadata_pollination_signal: bool = True
    metadata_antagonist_signal: bool = True
    metadata_recoverability_signal: bool = True
    is_open_access: bool = True
    open_access_url: str = "https://example.org/paper.pdf"


def test_public_pdf_and_two_channel_metadata_get_high_manual_priority() -> None:
    row = build_row(
        CandidateFixture(),
        {"receipt_count": 3, "counts_by_status": {"public_fulltext_candidate": 1, "metadata_recovered": 1}},
    )

    assert row.public_pdf_candidate_count == 1
    assert row.broad_screen_priority == "manual_screen_high"
    assert row.source_availability_score > 100
    assert "denominators" in row.next_action


def test_repository_manifest_without_two_channel_metadata_stays_medium() -> None:
    candidate = CandidateFixture(metadata_antagonist_signal=False)
    row = build_row(
        candidate,
        {"receipt_count": 2, "counts_by_status": {"linked_repository_manifest": 1, "metadata_recovered": 1}},
    )

    assert row.linked_repository_manifest_count == 1
    assert row.broad_screen_priority == "manual_screen_medium"
    assert "missing channel" in row.next_action


def test_metadata_only_candidate_is_held_back() -> None:
    row = build_row(
        CandidateFixture(is_open_access=False, open_access_url=""),
        {"receipt_count": 4, "counts_by_status": {"metadata_recovered": 1, "not_found": 3}},
    )

    assert row.broad_screen_priority == "hold_metadata_only"
    assert "Do not manually read" in row.next_action
