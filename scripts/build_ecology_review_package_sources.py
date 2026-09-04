from __future__ import annotations

from pathlib import Path

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
    text = candidate.build_appendix_source()
    return text.replace("../../../../manuscript/", "../../../manuscript/")


def build_open_research_manifest() -> str:
    """Build the canonical Open Research export from the same candidate graph."""

    old_out, old_data = candidate.OUT, candidate.DATA_OUT
    try:
        candidate.OUT = OUT
        candidate.DATA_OUT = DATA_OUT
        return candidate.build_open_research_manifest()
    finally:
        candidate.OUT = old_out
        candidate.DATA_OUT = old_data


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
