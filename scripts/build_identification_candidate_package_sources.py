from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_IDENTIFICATION_DESIGN.md"
REFERENCES = ROOT / "manuscript" / "IDENTIFICATION_DESIGN_REFERENCES.md"
CAPTIONS = ROOT / "manuscript" / "IDENTIFICATION_DESIGN_FIGURE_CAPTIONS.md"
SUPPLEMENT = ROOT / "manuscript" / "supplementary" / "SUPPLEMENT_IDENTIFICATION_DESIGN.md"
OUT = ROOT / "submission" / "ecology" / "identification_candidate" / "generated"

TITLE_BREAK = "[[ECOLOGY_SECTION_BREAK_AFTER_TITLE]]"
REF_BREAK = "[[ECOLOGY_SECTION_BREAK_AFTER_REFERENCES]]"
PAGE_BREAK = "[[ECOLOGY_PAGE_BREAK]]"


def _focused_reference_text() -> str:
    text = REFERENCES.read_text(encoding="utf-8")
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    entries = [
        p for p in paragraphs
        if not p.startswith("# ")
        and not p.startswith("This bibliography")
    ]
    if len(entries) != 13:
        raise RuntimeError(f"expected 13 focused bibliography entries, found {len(entries)}")
    return "\n\n".join(entries)


def _figure_captions() -> list[str]:
    text = CAPTIONS.read_text(encoding="utf-8")
    captions: list[str] = []
    for idx in range(1, 6):
        match = re.search(
            rf"\*\*Figure {idx}\.\s*(.+?)\*\*\s*(.+?)(?=\n\n\*\*Figure |\Z)",
            text,
            flags=re.S,
        )
        if match is None:
            raise RuntimeError(f"missing Figure {idx} caption")
        title = re.sub(r"\s+", " ", match.group(1)).strip()
        body = re.sub(r"\s+", " ", match.group(2)).strip()
        captions.append(f"**Figure {idx}. {title}** {body}")
    return captions


def build_main_source() -> str:
    text = MANUSCRIPT.read_text(encoding="utf-8").strip()
    if "## References" not in text:
        raise RuntimeError("candidate manuscript has no References heading")

    pre_refs = text.split("## References", 1)[0].rstrip()
    # Keep title-page metadata and abstract in the candidate text, but insert a
    # marker after the title block for a section break in the Word build.
    title_end = pre_refs.find("\n\n## Abstract")
    if title_end < 0:
        raise RuntimeError("candidate manuscript has no Abstract heading")
    pre_refs = pre_refs[:title_end] + f"\n\n{TITLE_BREAK}" + pre_refs[title_end:]
    refs = _focused_reference_text()
    figures = _figure_captions()
    figure_block = "\n\n".join(
        f"{caption}\n\n![](../../../manuscript/identification_figures/FIGURE_{idx}_IDENTIFICATION_DESIGN.svg)"
        for idx, caption in enumerate(figures, 1)
    )
    return (
        pre_refs
        + "\n\n## References\n\n"
        + refs
        + f"\n\n{REF_BREAK}\n\n"
        + "## Figures\n\n"
        + figure_block
        + "\n"
    )


def build_supplement_source() -> str:
    text = SUPPLEMENT.read_text(encoding="utf-8").strip()
    return text + "\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "MANUSCRIPT_IDENTIFICATION_CANDIDATE.md").write_text(build_main_source(), encoding="utf-8")
    (OUT / "APPENDIX_IDENTIFICATION_CANDIDATE.md").write_text(build_supplement_source(), encoding="utf-8")


if __name__ == "__main__":
    main()
