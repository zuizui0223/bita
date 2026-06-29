"""Validation for the literature-first functional-trait evidence matrix."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REQUIRED_COLUMNS = frozenset(
    {
        "trait_id",
        "trait_label",
        "organ",
        "functional_module",
        "trait_modality",
        "candidate_consumer_layer",
        "mechanism_claim",
        "evidence_grade",
        "global_availability",
        "provisional_role",
        "v1_decision",
        "source_seed_ids",
        "notes",
    }
)

ALLOWED_EVIDENCE_GRADES = frozenset({"A", "B", "C", "U"})
ALLOWED_DECISIONS = frozenset(
    {
        "retain_pending_coverage",
        "hold_for_coverage_audit",
        "hold_for_case_study",
        "hold_for_clade_specific_analysis",
        "exclude_from_v1_defence",
        "exclude_from_v1",
    }
)
PRIMARY_ROLES = frozenset({"primary floral attraction candidate", "primary leaf quality candidate"})
LOW_COVERAGE = frozenset({"low", "very_low"})


@dataclass(frozen=True)
class FunctionalTraitMatrixReport:
    """Audit result for a functional-trait evidence matrix."""

    n_rows: int
    module_counts: dict[str, int]
    errors: tuple[str, ...]

    @property
    def is_valid(self) -> bool:
        return not self.errors


def audit_functional_trait_matrix(rows: Iterable[dict[str, str]]) -> FunctionalTraitMatrixReport:
    """Validate decision rules before traits are used in model fitting.

    The audit does not prove that a trait has the claimed biological function.
    It prevents obvious protocol violations, such as labelling an unresolved
    visual pattern as a primary defence trait or promoting a very-low-coverage
    trait directly into the first global analysis.
    """

    rows_tuple = tuple(rows)
    errors: list[str] = []
    seen_ids: set[str] = set()
    module_counts: dict[str, int] = {}

    for index, row in enumerate(rows_tuple, start=1):
        missing = REQUIRED_COLUMNS.difference(row)
        if missing:
            errors.append(f"row {index}: missing columns {sorted(missing)}")
            continue

        trait_id = row["trait_id"].strip()
        if not trait_id:
            errors.append(f"row {index}: trait_id is blank")
        elif trait_id in seen_ids:
            errors.append(f"row {index}: duplicate trait_id {trait_id!r}")
        else:
            seen_ids.add(trait_id)

        grade = row["evidence_grade"].strip()
        decision = row["v1_decision"].strip()
        availability = row["global_availability"].strip()
        role = row["provisional_role"].strip()
        module = row["functional_module"].strip()

        if grade not in ALLOWED_EVIDENCE_GRADES:
            errors.append(f"row {index}: unsupported evidence_grade {grade!r}")
        if decision not in ALLOWED_DECISIONS:
            errors.append(f"row {index}: unsupported v1_decision {decision!r}")
        if not module:
            errors.append(f"row {index}: functional_module is blank")
        else:
            module_counts[module] = module_counts.get(module, 0) + 1

        if role in PRIMARY_ROLES:
            if grade not in {"A", "B"}:
                errors.append(f"row {index}: primary role requires grade A or B")
            if availability in LOW_COVERAGE:
                errors.append(f"row {index}: primary role cannot have low or very_low availability")
            if decision != "retain_pending_coverage":
                errors.append(f"row {index}: primary role must remain pending coverage audit")

        if grade == "U" and decision not in {"exclude_from_v1", "exclude_from_v1_defence"}:
            errors.append(f"row {index}: unresolved function must be excluded from v1")

        if not row["source_seed_ids"].strip() and grade != "U":
            errors.append(f"row {index}: resolved evidence grade requires a literature seed")

    if not rows_tuple:
        errors.append("matrix has no rows")

    return FunctionalTraitMatrixReport(
        n_rows=len(rows_tuple),
        module_counts=module_counts,
        errors=tuple(errors),
    )


def audit_functional_trait_matrix_file(path: str | Path) -> FunctionalTraitMatrixReport:
    """Read and audit a CSV matrix at ``path``."""

    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return audit_functional_trait_matrix(reader)
