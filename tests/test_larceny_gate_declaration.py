"""Integrity tests for the committed antagonist-relief-gate analysis.

These guard the properties that make the result readable as declared rather
than as fitted: every committed effect is oriented and independent, every
moderator level is coded with a basis, the strata are declared before the rows
exist, and the committed readout matches the committed numbers.
"""

from pathlib import Path

import pytest

from trait_architecture.broad_meta_analysis import (
    DIRECT_ROUTES,
    ORIENTATION,
    ROUTE_EXPECTED_SIGN,
    ROUTE_TRAIT_ROLE,
    read_csv_rows,
    read_strata,
    validate_effect_rows,
)
from trait_architecture.context_dependence import (
    read_moderator_coding,
    read_moderator_registry,
    run_context_dependence,
)


ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "empirical" / "broad_reality_evidence" / "larceny_gate"
STRATA_PATH = ROOT / "empirical" / "broad_reality_evidence" / "broad_meta_analysis_strata.csv"

LARCENY_STRATA = {
    "HF_larceny_female_lrr_comparative",
    "HP_larceny_visitation_lrr_comparative",
    "HR_larceny_nectar_lrr_comparative",
    "HF_larceny_male_lrr_comparative",
}


@pytest.fixture(scope="module")
def effect_rows() -> list[dict[str, str]]:
    return read_csv_rows(GATE / "larceny_effect_rows.csv")


@pytest.fixture(scope="module")
def strata() -> list[dict[str, str]]:
    return read_strata(STRATA_PATH)


def test_antagonist_routes_are_declared_with_role_and_expected_sign() -> None:
    for route in ("H_to_fitness", "H_to_pollination", "H_to_reward"):
        assert route in DIRECT_ROUTES
        assert ROUTE_TRAIT_ROLE[route] == "H"
        assert ROUTE_EXPECTED_SIGN[route] == "negative"


def test_every_larceny_stratum_is_declared(strata: list[dict[str, str]]) -> None:
    declared = {row["stratum_id"] for row in strata}
    assert LARCENY_STRATA <= declared


def test_committed_effect_rows_validate(effect_rows: list[dict[str, str]]) -> None:
    validate_effect_rows(effect_rows)
    assert effect_rows


def test_every_effect_is_oriented_and_traceable(effect_rows: list[dict[str, str]]) -> None:
    for row in effect_rows:
        assert row["effect_orientation"] == ORIENTATION
        assert row["trait_role"] == "H"
        assert row["source_basis"] == "deposited_effect_size_table_of_published_synthesis"
        # Pinned commit, source rows, and the synthesis DOI must all be present.
        assert "@04663ff895b300fc957c4a32f661e5f73ca95217" in row["source_locator"]
        assert "rows[sample]=" in row["source_locator"]
        assert "10.1002/ecy.70036" in row["source_locator"]


def test_no_primary_study_doi_is_invented(effect_rows: list[dict[str, str]]) -> None:
    """The synthesis DOI must never be recorded as a primary study's DOI."""

    for row in effect_rows:
        assert row["doi"] == ""


def test_one_effect_per_cluster_per_stratum(effect_rows: list[dict[str, str]]) -> None:
    seen: set[tuple[str, str, str]] = set()
    for row in effect_rows:
        key = (row["study_cluster_id"], row["route"], row["outcome_class"])
        assert key not in seen, key
        seen.add(key)


def test_every_effect_has_a_coding_row_for_every_declared_moderator(
    effect_rows: list[dict[str, str]],
) -> None:
    coding = read_moderator_coding(GATE / "larceny_moderator_coding.csv")
    registry = read_moderator_registry(GATE / "larceny_moderator_registry.csv")
    moderators = {row["moderator_name"] for row in registry}
    coded = {(row["effect_id"], row["moderator_name"]) for row in coding}
    for row in effect_rows:
        for moderator in moderators:
            assert (row["effect_id"], moderator) in coded, (row["effect_id"], moderator)


def test_every_coding_row_states_its_basis() -> None:
    for row in read_moderator_coding(GATE / "larceny_moderator_coding.csv"):
        assert row["coding_basis"], row["effect_id"]
        if row["coding_status"] == "coded":
            assert row["moderator_value"]
        else:
            # An uncodable cluster must say why, not fall back to a level.
            assert row["moderator_value"] == ""


def test_registry_thresholds_match_the_committed_power_analysis() -> None:
    registry = read_moderator_registry(GATE / "larceny_moderator_registry.csv")
    for row in registry:
        per_level = int(float(row["min_clusters_per_level"]))
        total = int(float(row["min_clusters_total"]))
        # Confirmatory analyses at 5/10, exploratory at 3/6; nothing looser.
        assert (per_level, total) in {(5, 10), (3, 6)}, row["analysis_id"]


def test_declared_analyses_execute_and_return_calibrated_verdicts(
    effect_rows: list[dict[str, str]],
    strata: list[dict[str, str]],
) -> None:
    tables = run_context_dependence(
        effect_rows,
        read_moderator_coding(GATE / "larceny_moderator_coding.csv"),
        strata,
        read_moderator_registry(GATE / "larceny_moderator_registry.csv"),
    )
    models = tables["meta_regression_models"]
    assert len(models) == 6
    assert all(row["analysis_status"] == "random_effects_meta_regression" for row in models)

    permitted = {
        "no_detected_context_dependence",
        "context_dependent_magnitude_only",
        "context_dependent_direction_reversal",
        "moderator_changes_route_effect",
        "omnibus_moderator_test_not_estimable",
    }
    assert {row["context_dependence_verdict"] for row in models} <= permitted

    for row in tables["subgroup_tests"]:
        assert row["inferential_role"] == "descriptive_only_not_used_for_inference"


def test_readout_reports_the_committed_pooled_values() -> None:
    readout = (GATE / "LARCENY_GATE_READOUT_V1.md").read_text(encoding="utf-8")
    # Headline estimate, its interval, and its cluster count.
    for token in ("−0.210", "−0.351", "−0.070", "48", "0.0034"):
        assert token in readout, token
    # The boundaries that must travel with the number.
    assert "not an independent literature search" in readout.lower()
    assert "asymmetry detected" in readout.lower()
    assert "not detected at the declared design" in readout.lower()


def test_protocol_precedes_results_and_discloses_prior_knowledge() -> None:
    protocol = (GATE / "LARCENY_GATE_PROTOCOL_V1.md").read_text(encoding="utf-8")
    assert "before any pooled estimate" in protocol
    # The declared hypothesis must remain in the direction the source contradicts.
    assert "the direction the source publication contradicts" in protocol
    assert "B2" in protocol
