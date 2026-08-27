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


def _main_body() -> str:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    before_refs = text.split("## References", 1)[0].rstrip()
    if "## Author contributions, funding, acknowledgments and competing interests" in before_refs:
        before_refs = before_refs.split("## Author contributions, funding, acknowledgments and competing interests", 1)[0].rstrip()
    return before_refs


def build_main_source() -> str:
    body = _main_body()
    refs = _focused_reference_text()
    captions = _figure_captions()
    parts = [body, "", "## References", "", refs, "", REF_BREAK]
    for idx, caption in enumerate(captions, start=1):
        if idx > 1:
            parts.extend(["", PAGE_BREAK])
        parts.extend([
            "",
            caption,
            "",
            f"![](../../../manuscript/identification_figures/FIGURE_{idx}_IDENTIFICATION_DESIGN.svg)",
        ])
    return "\n".join(parts).rstrip() + "\n"


def build_supplement_source() -> str:
    text = SUPPLEMENT.read_text(encoding="utf-8").rstrip()
    return "# Appendix S1 — Identification design\n\n" + text + "\n"


def write_sources(out: Path = OUT) -> tuple[Path, Path]:
    out.mkdir(parents=True, exist_ok=True)
    main_path = out / "MANUSCRIPT_IDENTIFICATION_CANDIDATE.md"
    supplement_path = out / "APPENDIX_IDENTIFICATION_CANDIDATE.md"
    main_path.write_text(build_main_source(), encoding="utf-8")
    supplement_path.write_text(build_supplement_source(), encoding="utf-8")
    return main_path, supplement_path


if __name__ == "__main__":
    for path in write_sources():
        print(path)
