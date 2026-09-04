from __future__ import annotations

from pathlib import Path
import shutil

import build_ecology_submission_sources as legacy
import build_trait_differentiation_candidate_package_sources as candidate


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "submission" / "ecology" / "generated"
DATA_OUT = OUT / "open_research_data"

TITLE_BREAK = candidate.TITLE_BREAK
REF_BREAK = candidate.REF_BREAK
PAGE_BREAK = candidate.PAGE_BREAK


def _remove_redundant_figure_breaks(text: str) -> str:
    """Avoid renderer-only blank pages before the final two tall figures."""

    for idx in (4, 5):
        text = text.replace(
            f"{PAGE_BREAK}\n\n**Figure {idx}.",
            f"**Figure {idx}.",
            1,
        )
    return text


def build_main_submission_source() -> str:
    """Build the canonical Ecology Main from the validated Chapter 2 source."""

    text = _remove_redundant_figure_breaks(candidate.build_main_source())
    return text.replace("../../../../manuscript/", "../../../manuscript/")


def build_appendix_source() -> str:
    """Build the canonical Appendix from the same Chapter 2 source graph."""

    text = candidate.build_appendix_source()
    return text.replace("../../../../manuscript/", "../../../manuscript/")


def build_open_research_manifest() -> str:
    """Retain historical machine-readable products and add active Chapter 2 outputs."""

    old_legacy_out, old_legacy_data = legacy.OUT, legacy.DATA_OUT
    try:
        legacy.OUT = OUT
        legacy.DATA_OUT = DATA_OUT
        manifest = legacy.build_open_research_manifest().rstrip()
    finally:
        legacy.OUT = old_legacy_out
        legacy.DATA_OUT = old_legacy_data

    DATA_OUT.mkdir(parents=True, exist_ok=True)
    additions = [
        (
            candidate.ROBUSTNESS_JSON,
            DATA_OUT / "trait_differentiation_robustness_readout.json",
            "Registered finite-family trait-differentiation robustness readout.",
        ),
        (
            candidate.HIGH_INFO_COVERAGE,
            DATA_OUT / "high_information_identification_coverage.csv",
            "Authoritative V2 high-information identification-coverage matrix; screened-set coverage, not literature prevalence.",
        ),
        (
            candidate.IMPATIENS_RETROFIT,
            DATA_OUT / "impatiens_identification_retrofit.json",
            "Aggregate public-data retrofit used in the floral mechanism-identification worked case; no individual records.",
        ),
        (
            ROOT / "empirical" / "identification_design" / "QUESTION_METHOD_EXPLANATION_MATRIX_V1.csv",
            DATA_OUT / "question_method_explanation_matrix.csv",
            "Question-by-method explanatory reach, current evidence state, claim ceiling, and next valid identification gate.",
        ),
        (
            ROOT / "empirical" / "identification_design" / "DEFENCE_ESCAPE_ROUTE_HYPOTHESIS_RECOVERY_V1.csv",
            DATA_OUT / "defence_escape_route_hypothesis_recovery.csv",
            "Hypothesis-by-hypothesis recovery of defence as an escape route, including positive ecological results, unevaluable complete-system terms, and next valid gates.",
        ),
    ]
    for src, dst, _ in additions:
        if not src.exists():
            raise RuntimeError(f"missing Chapter 2 Open Research source: {src}")
        shutil.copyfile(src, dst)

    lines = [
        manifest,
        "",
        "## Chapter 2 additions",
        "",
        "| Deposition file | Canonical repository source | Contents |",
        "|---|---|---|",
    ]
    for src, dst, description in additions:
        lines.append(f"| `{dst.name}` | `{src.relative_to(ROOT)}` | {description} |")
    lines += [
        "",
        "The six historical mechanism/Pattern machine-readable products are retained for provenance and supplementary sensitivity work. The active Chapter 2 adds the trait-differentiation robustness readout and the authoritative floral identification products without treating either route counts or finite-grid occupancy as natural prevalence.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "MANUSCRIPT_ECOLOGY_SUBMISSION.md").write_text(
        build_main_submission_source(), encoding="utf-8"
    )
    (OUT / "APPENDIX_S1.md").write_text(build_appendix_source(), encoding="utf-8")
    (OUT / "OPEN_RESEARCH_DATA_MANIFEST.md").write_text(
        build_open_research_manifest(), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
