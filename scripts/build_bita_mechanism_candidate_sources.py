from __future__ import annotations

from pathlib import Path
import re
import shutil

try:  # importable from tests and executable from scripts/
    from scripts import build_mechanism_identification_figures_svg as figure_builder
except ImportError:  # pragma: no cover
    import build_mechanism_identification_figures_svg as figure_builder


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md"
REFERENCES = ROOT / "manuscript" / "IDENTIFICATION_DESIGN_REFERENCES.md"
CAPTIONS = ROOT / "manuscript" / "TRAIT_DIFFERENTIATION_FIGURE_CAPTIONS_V1.md"
FIGDIR = ROOT / "manuscript" / "mechanism_identification_figures"
APPENDIX = ROOT / "manuscript" / "supplementary" / "SUPPLEMENT_IDENTIFICATION_DESIGN.md"
HIGH_INFO = ROOT / "empirical" / "identification_design" / "HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V2.csv"
IMPATIENS = ROOT / "empirical" / "identification_design" / "IMPATIENS_2018_IDENTIFICATION_RETROFIT_V1.json"
PATTERN_READOUT = ROOT / "empirical" / "mechanism_pattern_synthesis" / "PATTERN_EXPANSION_READOUT_V1.json"
OUT = ROOT / "submission" / "ecology" / "mechanism_identification_candidate" / "generated"
DATA_OUT = OUT / "open_research_data"

TITLE_BREAK = "[[ECOLOGY_SECTION_BREAK_AFTER_TITLE]]"
REF_BREAK = "[[ECOLOGY_SECTION_BREAK_AFTER_REFERENCES]]"
PAGE_BREAK = "[[ECOLOGY_PAGE_BREAK]]"

FIGURES = figure_builder.FIGURE_NAMES


def _strip_reference_placeholder(text: str) -> str:
    marker = "\n## References\n"
    if marker not in text:
        raise RuntimeError("canonical BITA manuscript has no References boundary")
    return text.split(marker, 1)[0].rstrip()


def _reference_text() -> str:
    text = REFERENCES.read_text(encoding="utf-8").strip()
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    entries = [
        p for p in paragraphs
        if not p.startswith("#")
        and not p.startswith("This bibliography")
    ]
    if len(entries) < 10:
        raise RuntimeError(f"focused BITA bibliography unexpectedly small: {len(entries)}")
    return "\n\n".join(entries)


def _figure_captions() -> list[str]:
    text = CAPTIONS.read_text(encoding="utf-8")
    captions: list[str] = []
    for idx in range(1, 6):
        match = re.search(
            rf"## Figure {idx}\.\s*(.+?)\n\n(.+?)(?=\n\n## Figure |\Z)",
            text,
            flags=re.S,
        )
        if match is None:
            raise RuntimeError(f"missing active Figure {idx} caption")
        title = re.sub(r"\s+", " ", match.group(1)).strip()
        body = re.sub(r"\s+", " ", match.group(2)).strip()
        captions.append(f"**Figure {idx}. {title}** {body}")
    return captions


def _ensure_figures() -> None:
    paths = figure_builder.build(FIGDIR)
    if len(paths) != 5:
        raise RuntimeError(f"expected five BITA Main figures, got {len(paths)}")
    missing = [name for name in FIGURES if not (FIGDIR / name).exists()]
    if missing:
        raise RuntimeError(f"missing generated BITA Main figures: {missing}")


def build_main_source() -> str:
    _ensure_figures()
    text = _strip_reference_placeholder(MANUSCRIPT.read_text(encoding="utf-8").strip())
    if "Trait interaction is not ecological mechanism" not in text:
        raise RuntimeError("canonical BITA title has drifted")
    forbidden = (
        "When does a trait trade-off resolve by differentiation rather than compromise?",
        "300 nonzero-conflict evaluations",
        "Delta_arch = sL_S* - K",
    )
    for token in forbidden:
        if token in text:
            raise RuntimeError(f"stale architecture-paper token in active BITA Main: {token}")

    front, body = text.split("## Abstract", 1)
    front = front.rstrip()
    body = "## Abstract" + body
    refs = _reference_text()
    captions = _figure_captions()

    figure_blocks: list[str] = []
    for idx, (caption, filename) in enumerate(zip(captions, FIGURES, strict=True), 1):
        prefix = "" if idx == 1 else f"{PAGE_BREAK}\n\n"
        figure_blocks.append(
            f"{prefix}{caption}\n\n"
            f"![](../../../../manuscript/mechanism_identification_figures/{filename})"
        )

    return (
        front
        + "\n\n**Journal:** Ecology\n\n**Manuscript type:** Concepts & Synthesis\n\n"
        + TITLE_BREAK
        + "\n\n"
        + body.strip()
        + "\n\n## References\n\n"
        + refs
        + "\n\n"
        + REF_BREAK
        + "\n\n"
        + "\n\n".join(figure_blocks)
        + "\n"
    )


def build_appendix_source() -> str:
    text = APPENDIX.read_text(encoding="utf-8").strip()
    header = (
        "# Appendix S1 — Identification design, empirical frontier, and provenance\n\n"
        "This Appendix supports the active BITA mechanism-identification paper. "
        "Architecture-value derivations retained elsewhere in the repository are not part of the active Main claim spine.\n\n"
    )
    return header + text + "\n"


def build_open_research_manifest() -> str:
    DATA_OUT.mkdir(parents=True, exist_ok=True)
    files = [
        (HIGH_INFO, DATA_OUT / "high_information_identification_coverage_v2.csv", "17-system high-information identification frontier."),
        (IMPATIENS, DATA_OUT / "impatiens_2018_identification_retrofit_v1.json", "Public-data identification retrofit summary."),
        (PATTERN_READOUT, DATA_OUT / "pattern_expansion_readout_v1.json", "Source-adjudicated 56-route / 25-cluster recurrence readout."),
    ]
    lines = [
        "# BITA mechanism-identification Open Research manifest",
        "",
        "| Deposition file | Canonical source | Role |",
        "|---|---|---|",
    ]
    for src, dst, role in files:
        if not src.exists():
            raise RuntimeError(f"missing Open Research source: {src}")
        shutil.copyfile(src, dst)
        lines.append(f"| `{dst.name}` | `{src.relative_to(ROOT)}` | {role} |")
    lines += [
        "",
        "These products document evidence capacity and identification status. Route counts are overlapping recurrence diagnostics, not prevalence estimates.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "MANUSCRIPT_ECOLOGY_SUBMISSION.md").write_text(build_main_source(), encoding="utf-8")
    (OUT / "APPENDIX_S1.md").write_text(build_appendix_source(), encoding="utf-8")
    (OUT / "OPEN_RESEARCH_DATA_MANIFEST.md").write_text(build_open_research_manifest(), encoding="utf-8")
    print(OUT / "MANUSCRIPT_ECOLOGY_SUBMISSION.md")
    print(OUT / "APPENDIX_S1.md")
    print(OUT / "OPEN_RESEARCH_DATA_MANIFEST.md")


if __name__ == "__main__":
    main()
