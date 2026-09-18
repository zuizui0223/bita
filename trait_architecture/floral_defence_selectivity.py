from __future__ import annotations

from collections.abc import Iterable

DOMAIN_CODES = frozenset({"SEPARATED", "OVERLAPPED", "BYPASS_TOLERANCE", "TRANSITIONAL", "UNCLEAR"})
COHORTS = frozenset({"derivation", "holdout"})
UNCERTAINTY_CLASSES = frozenset(
    {
        "DIRECTION_SUPPORTED",
        "NULL_COMPATIBLE",
        "EQUIVALENCE_SUPPORTED",
        "DIRECTION_ONLY",
        "UNRESOLVED",
    }
)
POLLINATOR_STATES = frozenset(
    {
        "PRESERVED_OR_IMPROVED",
        "IMPAIRED",
        "NO_DETECTED_CHANGE",
        "MIXED",
        "UNRESOLVED",
    }
)

REGISTRY_REQUIRED = frozenset(
    {
        "study_cluster_id",
        "publication_id",
        "plant_taxon",
        "D_axis_id",
        "context_id",
        "derivation_or_holdout",
        "source_provenance_path",
    }
)
ARCHITECTURE_REQUIRED = frozenset(
    {
        "study_cluster_id",
        "D_axis_id",
        "context_id",
        "pre_outcome_domain_code",
        "separating_coordinate",
        "defence_modality",
        "antagonist_guild",
        "pollinator_guild",
        "observational_or_experimental",
        "architecture_basis_path",
    }
)
OUTCOME_REQUIRED = frozenset(
    {
        "study_cluster_id",
        "D_axis_id",
        "context_id",
        "antagonist_outcome_type",
        "antagonist_effect_direction",
        "antagonist_uncertainty_class",
        "pollinator_outcome_type",
        "pollinator_response_stage",
        "pollinator_effect_direction",
        "pollinator_uncertainty_class",
        "pollinator_cost_state",
        "source_supported_preservation",
        "source_inference",
        "outcome_basis_path",
    }
)


def _missing_required(
    row: dict[str, str], required: frozenset[str], label: str, index: int
) -> list[str]:
    errors: list[str] = []
    for field in sorted(required):
        if not str(row.get(field, "")).strip():
            errors.append(f"{label} row {index}: missing required field {field}")
    return errors


def validate_registry(rows: Iterable[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    for index, row in enumerate(rows, start=1):
        errors.extend(_missing_required(row, REGISTRY_REQUIRED, "registry", index))
        cohort = str(row.get("derivation_or_holdout", "")).strip()
        if cohort and cohort not in COHORTS:
            errors.append(f"registry row {index}: invalid derivation_or_holdout={cohort!r}")
    return errors


def validate_architecture_codes(rows: Iterable[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    for index, row in enumerate(rows, start=1):
        errors.extend(_missing_required(row, ARCHITECTURE_REQUIRED, "architecture", index))
        code = str(row.get("pre_outcome_domain_code", "")).strip()
        if code and code not in DOMAIN_CODES:
            errors.append(f"architecture row {index}: invalid pre_outcome_domain_code={code!r}")
    return errors


def validate_outcome_codes(rows: Iterable[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    for index, row in enumerate(rows, start=1):
        errors.extend(_missing_required(row, OUTCOME_REQUIRED, "outcome", index))
        for field in ("antagonist_uncertainty_class", "pollinator_uncertainty_class"):
            value = str(row.get(field, "")).strip()
            if value and value not in UNCERTAINTY_CLASSES:
                errors.append(f"outcome row {index}: invalid {field}={value!r}")
        state = str(row.get("pollinator_cost_state", "")).strip()
        if state and state not in POLLINATOR_STATES:
            errors.append(f"outcome row {index}: invalid pollinator_cost_state={state!r}")
        preservation = str(row.get("source_supported_preservation", "")).strip().lower() == "true"
        pollinator_uncertainty = str(row.get("pollinator_uncertainty_class", "")).strip()
        if (
            state == "PRESERVED_OR_IMPROVED"
            and pollinator_uncertainty == "NULL_COMPATIBLE"
            and not preservation
        ):
            errors.append(
                f"outcome row {index}: PRESERVED_OR_IMPROVED is not licensed by "
                "NULL_COMPATIBLE without source-supported preservation"
            )
    return errors
