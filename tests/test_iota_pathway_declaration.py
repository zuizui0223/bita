"""Integrity of the committed constituent-pathway declaration.

These tests guard the pre-registration itself: the declared stratum exists, every
declared moderator analysis points at it, and no effect can be added to the target
stratum without the moderator coding the declared analyses require.
"""

from __future__ import annotations

from pathlib import Path

from trait_architecture.broad_meta_analysis import read_csv_rows, read_strata, validate_effect_rows
from trait_architecture.context_dependence import (
    read_moderator_coding,
    read_moderator_registry,
    run_context_dependence,
)


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "empirical" / "broad_reality_evidence"
IOTA = EVIDENCE / "iota_pathway"
TARGET_STRATUM = "BP_chemical_pollinator_use_lrr_manipulation"


def _strata() -> list[dict[str, str]]:
    return read_strata(EVIDENCE / "broad_meta_analysis_strata.csv")


def _registry() -> list[dict[str, str]]:
    return read_moderator_registry(IOTA / "iota_moderator_registry.csv")


def _coding() -> list[dict[str, str]]:
    return read_moderator_coding(IOTA / "iota_moderator_coding.csv")


def _effects() -> list[dict[str, str]]:
    return validate_effect_rows(read_csv_rows(EVIDENCE / "broad_effect_extractions.csv"))


def test_target_stratum_is_declared_with_the_channel_expectation() -> None:
    stratum = next(row for row in _strata() if row["stratum_id"] == TARGET_STRATUM)

    assert stratum["route"] == "B_to_pollination"
    assert stratum["trait_class"] == "chemical_barrier"
    assert stratum["outcome_class"] == "pollinator_preference_or_foraging"
    assert stratum["design_class"] == "manipulation"
    assert stratum["effect_metric"] == "log_response_ratio"
    assert stratum["expected_effect_direction"] == "negative"
    assert stratum["part_i_parameter"] == "c_D"


def test_every_declared_moderator_analysis_targets_the_declared_stratum() -> None:
    stratum_ids = {row["stratum_id"] for row in _strata()}
    registry = _registry()

    assert registry, "the constituent-pathway registry must declare at least one analysis"
    for row in registry:
        assert row["stratum_id"] in stratum_ids, row["analysis_id"]
        assert row["stratum_id"] == TARGET_STRATUM, row["analysis_id"]

    categorical = [row for row in registry if row["moderator_type"] == "categorical"]
    assert categorical, "at least one categorical context moderator must be declared"
    for row in categorical:
        assert row["reference_level"], row["analysis_id"]


def test_reading_queue_records_provenance_and_carries_no_numbers() -> None:
    rows = read_csv_rows(IOTA / "iota_reading_queue.csv")

    assert rows
    identifiers = [row["candidate_id"] for row in rows]
    assert len(identifiers) == len(set(identifiers))
    for row in rows:
        assert row["identifier_verification_status"], row["candidate_id"]
        assert row["retrieval_status"], row["candidate_id"]
        assert row["why_candidate"], row["candidate_id"]
    # The queue is a retrieval plan. Effect values live only in the extraction table.
    assert not {"effect_value", "standard_error", "effect_metric"} & set(rows[0])


def test_no_target_stratum_effect_may_bypass_the_declared_moderator_coding() -> None:
    stratum = next(row for row in _strata() if row["stratum_id"] == TARGET_STRATUM)
    keys = ("route", "trait_class", "outcome_class", "effect_metric", "design_class")
    matching = [
        row for row in _effects()
        if row.get("analysis_status") == "eligible_for_quantitative_synthesis"
        and all(row.get(key, "") == stratum[key] for key in keys)
    ]
    coded = {(row["effect_id"], row["moderator_name"]) for row in _coding()}
    required = [
        row["moderator_name"] for row in _registry()
        if row["moderator_type"] == "categorical" and row["stratum_id"] == TARGET_STRATUM
    ]

    missing = [
        (row["effect_id"], moderator)
        for row in matching
        for moderator in required
        if (row["effect_id"], moderator) not in coded
    ]
    assert not missing, f"target-stratum effects without declared moderator coding rows: {missing}"


def test_committed_inputs_report_a_withheld_rather_than_an_undeclared_verdict() -> None:
    tables = run_context_dependence(_effects(), _coding(), _strata(), _registry())

    allowed = {
        "not_evaluated",
        "context_dependent_direction_reversal",
        "context_dependent_magnitude_only",
        "no_detected_context_dependence",
        "moderator_changes_route_effect",
        "omnibus_moderator_test_not_estimable",
    }
    verdicts = [row["context_dependence_verdict"] for row in tables["subgroup_tests"]]
    verdicts += [row["context_dependence_verdict"] for row in tables["meta_regression_models"]]

    assert verdicts
    assert set(verdicts) <= allowed
