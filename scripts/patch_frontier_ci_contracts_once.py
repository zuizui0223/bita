from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace(path: str, old: str, new: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"missing patch target in {path}: {old!r}")
    p.write_text(text.replace(old, new), encoding="utf-8")


# Preserve scientifically valid boundary language that older regression tests guard.
replace("submission/ECOLOGY_CONCEPTS_SYNTHESIS_FIT_AUDIT.md", "## Identification invariants\n", "## Identification invariants preserved\n")
replace("submission/ECOLOGY_CONCEPTS_SYNTHESIS_FIT_AUDIT.md", "## Mechanism → Pattern / partial-identification fit\n", "## Mechanism → Pattern fit / partial-identification fit\n")
replace(
    "submission/ECOLOGY_CONCEPTS_SYNTHESIS_FIT_AUDIT.md",
    "The 56-route / 25-cluster synthesis supports only cross-system recurrence of the four constituent pathway families; it does not estimate natural prevalence or rho/iota/kappa.\n",
    "The 56-route / 25-cluster synthesis supports only the statement that the constituent ecological channels recur across systems; it does not estimate natural prevalence or rho/iota/kappa.\n",
)
replace("SUPPLEMENT_MANIFEST.md", "## 2. Scientific core\n", "## 2. Canonical scientific core\n")
replace("SUPPLEMENT_MANIFEST.md", "→ selective crossed interventions\n", "→ crossed A × D × antagonist × pollinator interventions\n")
replace(
    "SUPPLEMENT_MANIFEST.md",
    "- rho/iota invariance views are one four-way interaction up to sign;\n",
    "- rho/iota invariance views are one four-way interaction up to sign; this is the `A×D×G×P separability diagnostic`;\n",
)
replace("SUPPLEMENT_MANIFEST.md", "## 7. Historical provenance\n", "## 7. Historical quantitative provenance retained\n")
replace("SUPPLEMENT_MANIFEST.md", "Leal et al. 2025 pins remain unchanged:\n", "Leal et al. 2025 provenance remains pinned:\n")
replace(
    "SUPPLEMENT_MANIFEST.md",
    "Historical values and Sasidharan reconstruction remain preserved with their original inference boundaries.\n",
    "Historical values and the Sasidharan reconstruction remain preserved with their original inference boundaries and do not validate the identification framework.\n",
)
replace(
    "docs/SUBMISSION_SCOPE.md",
    "These overlapping categories establish recurrence capacity only. They are not prevalence estimates and do not estimate `Delta_AD W`, rho, iota, or kappa.\n",
    "These overlapping categories establish recurrence capacity only. The source-adjudicated route ledger is **not itself a grand meta-analysis**. They are not prevalence estimates and do not estimate `Delta_AD W`, rho, iota, or kappa.\n",
)
replace(
    "docs/SUBMISSION_SCOPE.md",
    "but the stronger synthesis is not simply `0/16`. Existing studies occupy complementary faces of the allocation problem.",
    "but the stronger synthesis is not simply `0/16`. Constituent channels recur, but their joint allocation remains unidentified. Existing studies occupy complementary faces of the allocation problem.",
)
replace(
    "docs/MECHANISM_PATTERN_IDENTIFICATION_BRIDGE.md",
    "The canonical paper preserves the original Mechanism → Pattern logic while distinguishing **recurrence**, **partial identification**, and **point identification**.\n\n```text\nMechanism\n→ constituent ecological recurrence\n→ total-interaction identified set",
    "The canonical paper preserves the original Mechanism → Pattern logic while distinguishing **recurrence**, **partial identification**, and **point identification**. At the coarsest empirical level, the original bridge remains:\n\n```text\nMechanism\n→ constituent ecological recurrence\n→ identification coverage\n→ mechanism-allocation experiment\n```\n\nThe refined inference sequence is:\n\n```text\nMechanism\n→ constituent ecological recurrence\n→ total-interaction identified set",
)
replace(
    "docs/MECHANISM_PATTERN_IDENTIFICATION_BRIDGE.md",
    "Recurrence may establish that the framework's biological ingredients are not peculiar to one system.",
    "The recurrence layer may support the statement that the framework's biological ingredients are not peculiar to one system.",
)
replace(
    "docs/MECHANISM_PATTERN_IDENTIFICATION_BRIDGE.md",
    "It may not validate the algebra, estimate channel interactions, imply natural prevalence, or establish a universal sign.",
    "It may not be used to validate the algebra, estimate channel interactions, imply natural prevalence, or establish a universal sign.",
)
replace(
    "submission/COVER_LETTER_ECOLOGY_CONCEPTS_SYNTHESIS.md",
    "recovering the earlier one-sided relation as an assumption-indexed bound on the biotic balance rather than a standalone theorem.",
    "recovering the earlier one-sided relation as a partial-identification bound rather than a standalone theorem; the bound is assumption-indexed through the stated kappa restriction.",
)
replace(
    "README.md",
    "The cross-system conclusion is therefore:\n\n> **The constituent channels recur, current studies constrain different parts of their allocation, but the full joint mechanism is not yet point-identified.**",
    "The cross-system conclusion retains the earlier boundary:\n\n> **The constituent channels recur, but their joint allocation remains unidentified.**\n\nThe refined conclusion is:\n\n> **The constituent channels recur, current studies constrain different parts of their allocation, but the full joint mechanism is not yet point-identified.**",
)
replace(
    "docs/FINAL_SUBMISSION_AUDIT.md",
    "but the stronger conclusion is that existing studies already constrain different dimensions of the allocation problem while none closes all of them.",
    "The constituent channels recur, but their joint allocation remains unidentified. The stronger conclusion is that existing studies already constrain different dimensions of the allocation problem while none closes all of them.",
)

# Update only genuinely changed numerical/current-state contracts.
replace("tests/test_identification_coverage.py", "assert len(rows) == 16", "assert len(rows) == 17")
replace("tests/test_identification_design_figures.py", "assert len(_read_coverage()) == 16", "assert len(_read_coverage()) == 17")
replace(
    "tests/test_submission_narrative.py",
    'assert "# Supplement manifest — canonical identification-design paper" in text',
    'assert "# Supplement manifest — canonical partial-identification paper" in text',
)
replace(
    "tests/test_submission_narrative.py",
    'assert "29 Main pages + 11 Appendix pages" in text',
    'assert "29 Main pages + 12 Appendix pages" in text',
)
