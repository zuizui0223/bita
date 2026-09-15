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

TITLE_CHAR_LIMIT = 120
ABSTRACT_WORD_LIMIT = 350
KEYWORD_MIN = 6
KEYWORD_MAX = 12
CORRESPONDING_AUTHOR_LINE = "**Corresponding author:** [Author-controlled]"
OPEN_RESEARCH_STATEMENT = (
    "**Open Research statement:** Review-stage identification code, source-adjudicated "
    "evidence products, derived analysis receipts, and the reader-facing "
    "mechanism-identification package are maintained in the public project repository. "
    "The accepted exact data/code release will be archived permanently and cited in the "
    "final article."
)

FIGURES = figure_builder.FIGURE_NAMES


def _strip_reference_placeholder(text: str) -> str:
    marker = "\n## References\n"
    if marker not in text:
        raise RuntimeError("canonical BITA manuscript has no References boundary")
    return text.split(marker, 1)[0].rstrip()


def _submission_front(front: str) -> str:
    """Keep journal-facing title/authors while removing repository editorial metadata."""
    front = re.sub(r"\n\*\*Canonical BITA full-paper science source\*\*\s*", "\n", front)
    front = re.sub(r"\n\*\*Target class:\*\*[^\n]*\s*", "\n", front)
    front = re.sub(r"\n{3,}", "\n\n", front).strip()
    if "Canonical BITA" in front or "Target class:" in front:
        raise RuntimeError("internal manuscript metadata survived submission-front sanitization")
    return front


def _title(text: str) -> str:
    first = text.splitlines()[0].strip()
    if not first.startswith("# "):
        raise RuntimeError("canonical BITA manuscript has no H1 title")
    title = first[2:].strip()
    if len(title) > TITLE_CHAR_LIMIT:
        raise RuntimeError(
            f"Ecology title exceeds {TITLE_CHAR_LIMIT} characters: {len(title)}"
        )
    return title


def _abstract_text(body: str) -> str:
    match = re.search(r"(?ms)^## Abstract\s*\n+(.*?)(?=^##\s+1\.)", body)
    if match is None:
        raise RuntimeError("canonical BITA manuscript has no bounded Abstract")
    return match.group(1).strip()


def _word_count(text: str) -> int:
    # A conservative plain-text count for the journal's abstract ceiling. TeX
    # punctuation is ignored; identifiers/numbers still count as tokens.
    cleaned = re.sub(r"\\[A-Za-z]+", " ", text)
    cleaned = re.sub(r"[{}_^$]", " ", cleaned)
    return len(re.findall(r"[A-Za-z0-9]+(?:[-'’][A-Za-z0-9]+)*", cleaned))


def _extract_and_sort_keywords(body: str) -> tuple[str, str, list[str]]:
    pattern = re.compile(r"(?m)^\*\*Keywords:\*\*\s*(.+?)\s*$")
    matches = list(pattern.finditer(body))
    if len(matches) != 1:
        raise RuntimeError(
            f"expected exactly one canonical Keywords line, found {len(matches)}"
        )

    keywords = [item.strip() for item in matches[0].group(1).split(";")]
    if any(not item for item in keywords):
        raise RuntimeError("canonical Keywords line contains an empty keyword")
    if not KEYWORD_MIN <= len(keywords) <= KEYWORD_MAX:
        raise RuntimeError(
            f"Ecology requires {KEYWORD_MIN}-{KEYWORD_MAX} keywords; found {len(keywords)}"
        )
    folded = [item.casefold() for item in keywords]
    if len(set(folded)) != len(folded):
        raise RuntimeError("canonical Keywords line contains duplicates")

    keywords = sorted(keywords, key=str.casefold)
    keyword_line = "**Keywords:** " + "; ".join(keywords)
    body_without = body[: matches[0].start()] + body[matches[0].end() :]
    body_without = re.sub(r"\n{3,}", "\n\n", body_without).strip()
    return body_without, keyword_line, keywords


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
    _title(text)
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

    front, body_tail = text.split("## Abstract", 1)
    front = _submission_front(front.rstrip())
    body = "## Abstract" + body_tail
    body, keyword_line, _ = _extract_and_sort_keywords(body)
    abstract_words = _word_count(_abstract_text(body))
    if abstract_words > ABSTRACT_WORD_LIMIT:
        raise RuntimeError(
            f"Ecology abstract exceeds {ABSTRACT_WORD_LIMIT} words: {abstract_words}"
        )

    refs = _reference_text()
    captions = _figure_captions()

    figure_blocks: list[str] = []
    for idx, (caption, filename) in enumerate(zip(captions, FIGURES, strict=True), 1):
        prefix = "" if idx == 1 else f"{PAGE_BREAK}\n\n"
        figure_blocks.append(
            f"{prefix}{caption}\n\n"
            f"![](../../../../manuscript/mechanism_identification_figures/{filename})"
        )

    title_page = (
        front
        + "\n\n**Journal:** Ecology"
        + "\n\n**Manuscript type:** Concepts & Synthesis"
        + "\n\n"
        + CORRESPONDING_AUTHOR_LINE
        + "\n\n"
        + OPEN_RESEARCH_STATEMENT
        + "\n\n"
        + keyword_line
    )

    out = (
        title_page
        + "\n\n"
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
    if "Canonical BITA full-paper science source" in out or "Target class:" in out:
        raise RuntimeError("internal repository metadata survived into generated Main")
    if out.count("**Keywords:**") != 1:
        raise RuntimeError("generated Main must contain exactly one Keywords line")
    if out.count("**Open Research statement:**") != 1:
        raise RuntimeError("generated Main must contain exactly one Open Research statement")
    return out


def build_appendix_source() -> str:
    text = APPENDIX.read_text(encoding="utf-8").strip()
    start = re.search(r"(?m)^## S1\.", text)
    if start is None:
        raise RuntimeError("active identification Appendix has no S1 boundary")
    text = text[start.start():]
    text = text.replace(
        "These classes motivate the experimental roadmap in Main Fig. 5.",
        "These classes motivate the crossed-intervention roadmap and fragmented-frontier synthesis in Main Figs. 3–4.",
    )
    header = (
        "# Appendix S1 — Identification design, empirical frontier, and provenance\n\n"
        "This Appendix supports the BITA mechanism-identification manuscript. "
        "It provides technical derivations, source-bounded reconstructions, the public-data retrofit, "
        "the identification-coverage audit, and reproducibility pointers for the active inference ladder. "
        "Architecture-value derivations retained elsewhere in the repository are outside the active BITA claim spine.\n\n"
    )
    out = header + text + "\n"
    forbidden = (
        "MANUSCRIPT_IDENTIFICATION_DESIGN.md",
        "earlier theorem-led manuscript",
    )
    for token in forbidden:
        if token in out:
            raise RuntimeError(f"stale Appendix routing survived candidate build: {token}")
    return out


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
