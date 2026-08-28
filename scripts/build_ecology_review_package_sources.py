from __future__ import annotations

from pathlib import Path
import re
import shutil

import build_ecology_submission_sources as legacy
import build_identification_candidate_package_sources as candidate


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "submission" / "ecology" / "generated"
DATA_OUT = OUT / "open_research_data"

TITLE_BREAK = candidate.TITLE_BREAK
REF_BREAK = candidate.REF_BREAK
PAGE_BREAK = candidate.PAGE_BREAK


def _title_page_open_research() -> str:
    return (
        "**Open Research statement:** Review-stage analysis code, identification estimands, "
        "source-audit products, the *Impatiens* public-data retrofit, and machine-readable "
        "identification-coverage products are available in the public project repository. "
        "The exact accepted data/code version will be deposited in a permanent versioned "
        "archive and cited in the final article at the acceptance stage."
    )


def build_main_submission_source() -> str:
    """Promote the validated identification-design candidate to Ecology Main source.

    The historical theorem-led manuscript remains in the repository, but it is no
    longer the source used by the canonical Ecology review-package builder.
    """
    text = candidate.build_main_source()

    # The candidate package is generated one directory deeper than the canonical
    # Ecology package. Rebase embedded figure paths for submission/ecology/generated/.
    text = text.replace("../../../../manuscript/", "../../../manuscript/")

    if TITLE_BREAK not in text:
        raise RuntimeError("candidate source is missing the title-page section break")
    text = text.replace(
        TITLE_BREAK,
        _title_page_open_research() + "\n\n" + TITLE_BREAK,
        1,
    )

    # Move review-stage availability to the title page and keep the backmatter in
    # the journal-facing order. Human-controlled statements remain explicit
    # placeholders and are not inferred here. The canonical scientific source
    # already contains the Section 5.4 AI-use disclosure, so do not duplicate it
    # in the backmatter during packaging.
    pattern = re.compile(
        r"\n\n## Open Research statement\n\n.+?"
        r"\n\n## Author contributions, funding, acknowledgments and competing interests\n\n"
        r"\[Author-controlled; complete before submission\.\]",
        flags=re.S,
    )
    replacement = (
        "\n\n## Acknowledgments\n\n[Author-controlled; complete before submission.]"
        + "\n\n## Author Contributions\n\n[Author-controlled; complete before submission.]"
        + "\n\n## Funding\n\n[Author-controlled; insert funding statement or confirmed no-funding statement.]"
        + "\n\n## Conflict of Interest Statement\n\n[Author-controlled; complete before submission.]"
    )
    text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError("could not normalize identification-manuscript backmatter")

    return text


def build_appendix_source() -> str:
    text = candidate.build_supplement_source()
    return text.replace("../../../../manuscript/", "../../../manuscript/")


def build_open_research_manifest() -> str:
    """Retain legacy machine-readable products and add identification-era outputs."""
    legacy.OUT = OUT
    legacy.DATA_OUT = DATA_OUT
    manifest = legacy.build_open_research_manifest().rstrip()

    DATA_OUT.mkdir(parents=True, exist_ok=True)
    additions = [
        (
            ROOT / "empirical" / "identification_design" / "HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V1.csv",
            DATA_OUT / "high_information_identification_coverage.csv",
            "Sixteen-system high-information identification-coverage matrix; screened-set coverage, not literature prevalence.",
        ),
        (
            ROOT / "empirical" / "identification_design" / "IMPATIENS_2018_IDENTIFICATION_RETROFIT_V1.json",
            DATA_OUT / "impatiens_identification_retrofit.json",
            "Aggregate model coefficients, HC3 intervals, cell counts, and identification boundaries for the public-data retrofit; no individual records.",
        ),
        (
            ROOT / "empirical" / "identification_design" / "QUESTION_METHOD_EXPLANATION_MATRIX_V1.csv",
            DATA_OUT / "question_method_explanation_matrix.csv",
            "Question-by-method explanatory reach, current evidence state, claim ceiling, and next valid identification gate.",
        ),
    ]
    for src, dst, _ in additions:
        if not src.exists():
            raise RuntimeError(f"missing identification-era Open Research source: {src}")
        shutil.copyfile(src, dst)

    lines = [
        manifest,
        "",
        "## Identification-design additions",
        "",
        "| Deposition file | Canonical repository source | Contents |",
        "|---|---|---|",
    ]
    for src, dst, description in additions:
        lines.append(f"| `{dst.name}` | `{src.relative_to(ROOT)}` | {description} |")
    lines += [
        "",
        "The historical mechanism/Pattern products are retained for provenance and supplementary sensitivity work; the canonical Main argument now uses the identification-design manuscript and its coverage audit.",
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
