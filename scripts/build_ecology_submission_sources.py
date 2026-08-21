from __future__ import annotations

from pathlib import Path
import re
import shutil


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"
TABLES = ROOT / "manuscript" / "TABLES_THEORETICAL_ECOLOGY.md"
SUPPLEMENT = ROOT / "manuscript" / "supplementary" / "SUPPLEMENTARY_MATERIAL.md"
SUPP_TABLE_DIR = ROOT / "manuscript" / "supplementary" / "tables"
OUT = ROOT / "submission" / "ecology" / "generated"
DATA_OUT = OUT / "open_research_data"


PAGEBREAK = "[[ECOLOGY_PAGE_BREAK]]"
TITLE_SECTION_BREAK = "[[ECOLOGY_SECTION_BREAK_AFTER_TITLE]]"
REF_SECTION_BREAK = "[[ECOLOGY_SECTION_BREAK_AFTER_REFERENCES]]"


def _between(text: str, start: str, end: str) -> str:
    return text.split(start, 1)[1].split(end, 1)[0].strip()


def _subsection(text: str, heading: str, next_headings: tuple[str, ...]) -> str:
    marker = f"### {heading}\n\n"
    if marker not in text:
        return ""
    rest = text.split(marker, 1)[1]
    candidates: list[tuple[int, str]] = []
    for nxt in next_headings:
        token = f"\n### {nxt}\n"
        idx = rest.find(token)
        if idx >= 0:
            candidates.append((idx, token))
    if candidates:
        idx, _ = min(candidates)
        rest = rest[:idx]
    return rest.strip()


def _normalize_acknowledgments(text: str, funding: str) -> str:
    chunks = [c.strip() for c in re.split(r"\n\s*\n", text) if c.strip()]
    if funding:
        chunks.insert(1 if chunks else 0, funding)
    return " ".join(chunks)


def _replace_supplement_callouts(text: str) -> str:
    replacements = {
        "analytic-versus-finite-difference checks and scenario-specific maps are provided in Supplementary Figs. S1–S2 and Tables S1–S2.":
            "analytic-versus-finite-difference checks and scenario-specific maps are provided in Appendix S1: Figures S1–S2; complete parameter and finite-grid records are provided as machine-readable Open Research data products.",
        "full route, conditionality, direct-identification, and stopping-rule records are provided in Tables S3–S6, with same-system and module-robustness displays in Supplementary Figs. S3–S4.":
            "full route, conditionality, direct-identification, and stopping-rule records are provided as machine-readable Open Research data products, with same-system and module-robustness displays in Appendix S1: Figures S3–S4.",
        "Supplementary Fig. S1": "Appendix S1: Figure S1",
        "Supplementary Fig. S2": "Appendix S1: Figure S2",
        "Supplementary Fig. S3": "Appendix S1: Figure S3",
        "Supplementary Fig. S4": "Appendix S1: Figure S4",
        "Supplementary Figs. S1–S2": "Appendix S1: Figures S1–S2",
        "Supplementary Fig. S3": "Appendix S1: Figure S3",
        "Supplementary Figs. S1–S3": "Appendix S1: Figures S1–S3",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def _extract_reference_blocks(refs: str, surnames: tuple[str, ...]) -> str:
    blocks = [b.strip() for b in refs.split("\n\n") if b.strip()]
    selected = [b for b in blocks if any(b.startswith(name) for name in surnames)]
    return "\n\n".join(selected)


def _table_submission_text() -> str:
    text = TABLES.read_text(encoding="utf-8")
    text = text.split("## Table 1.", 1)[1]
    text = "## Table 1." + text
    # REF_SECTION_BREAK already starts Table 1 on a new page. Only Tables 2–4
    # need explicit page breaks; adding one before Table 1 creates a blank page.
    text = re.sub(
        r"(?m)^## Table ([2-4])\.",
        lambda m: f"{PAGEBREAK}\n\n## Table {m.group(1)}.",
        text,
    )
    return text.strip()


def build_main_submission_source() -> str:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    title = text.splitlines()[0].removeprefix("# ").strip()
    front = text.split("## Abstract", 1)[0]

    authors = re.search(r"\*\*Authors and affiliations:\*\*.*", front)
    corresponding = re.search(r"\*\*Corresponding author:\*\*.*", front)
    orcids = re.search(r"\*\*ORCID\(s\):\*\*.*", front)
    open_research = re.search(r"\*\*Open Research statement:\*\*.*", front)
    for name, match in {
        "authors": authors,
        "corresponding": corresponding,
        "ORCID": orcids,
        "Open Research": open_research,
    }.items():
        if match is None:
            raise RuntimeError(f"missing canonical title-page field: {name}")

    abstract = _between(text, "## Abstract\n\n", "\n\n**Keywords:**")
    kw_match = re.search(r"\*\*Keywords:\*\*\s*(.+)", text)
    if kw_match is None:
        raise RuntimeError("missing canonical keyword line")
    keywords = kw_match.group(1).strip()

    body = _between(text, "## 1. Introduction", "## Figure captions")
    body = "## 1. Introduction\n\n" + body
    body = _replace_supplement_callouts(body)

    figure_captions = _between(text, "## Figure captions", "## Table captions")
    references = _between(text, "## References", "## Acknowledgments")
    acknowledgments = _between(text, "## Acknowledgments", "## Statements and Declarations")
    declarations = text.split("## Statements and Declarations", 1)[1]
    funding = _subsection(
        declarations,
        "Funding",
        ("Competing interests", "Author contributions", "Data and code availability"),
    )
    conflict = _subsection(
        declarations,
        "Competing interests",
        ("Author contributions", "Data and code availability"),
    )
    contributions = _subsection(
        declarations,
        "Author contributions",
        ("Data and code availability",),
    )
    data_code = _subsection(declarations, "Data and code availability", tuple())

    ack = _normalize_acknowledgments(acknowledgments, funding)
    open_research_text = open_research.group(0)
    if data_code:
        open_research_text += (
            " Review-stage code and data-access details: "
            + re.sub(r"\s+", " ", data_code).strip()
        )

    tables = _table_submission_text()

    figure_pages = []
    figure_paths = {
        1: "../../../manuscript/figures/FIGURE_1_MECHANISTIC_ARCHITECTURE.svg",
        2: "../../../manuscript/figures/FIGURE_2_THEORY_REGIME_MAP.svg",
        3: "../../../manuscript/figures/FIGURE_3_EMPIRICAL_MECHANISM_ARCHITECTURE.svg",
        4: "../../../manuscript/figures/FIGURE_5_QUANTITATIVE_IDENTIFICATION_BOUNDARY.svg",
        5: "../../../manuscript/supplementary/figures/FIGURE_S3_SAME_SYSTEM_ROUTE_MATRIX.svg",
    }
    for idx in range(1, 6):
        figure_pages.append(
            f"{PAGEBREAK}\n\n**Figure {idx}**\n\n"
            f"![]({figure_paths[idx]})"
        )

    parts = [
        f"# {title}",
        "**Journal:** Ecology",
        "**Manuscript type:** Concepts & Synthesis",
        authors.group(0),
        corresponding.group(0),
        orcids.group(0),
        open_research_text,
        f"**Key words/phrases:** {keywords}",
        TITLE_SECTION_BREAK,
        "## Abstract\n\n" + abstract,
        body,
        "## Acknowledgments\n\n" + ack,
        "## Author Contributions\n\n" + (contributions or "[Author-controlled; complete before submission.]"),
        "## Conflict of Interest Statement\n\n" + (conflict or "[Author confirmation required before submission.]"),
        "## References\n\n" + references,
        REF_SECTION_BREAK,
        tables,
        f"{PAGEBREAK}\n\n## Figure captions\n\n" + figure_captions,
        "\n\n".join(figure_pages),
    ]
    return "\n\n".join(p.strip() for p in parts if p.strip()) + "\n"


def build_appendix_source() -> str:
    canonical = MANUSCRIPT.read_text(encoding="utf-8")
    supplement = SUPPLEMENT.read_text(encoding="utf-8")
    title = canonical.splitlines()[0].removeprefix("# ").strip()
    front = canonical.split("## Abstract", 1)[0]
    authors = re.search(r"\*\*Authors and affiliations:\*\*.*", front)
    if authors is None:
        raise RuntimeError("missing canonical authors field")

    refs = _between(canonical, "## References", "## Acknowledgments")
    appendix_refs = _extract_reference_blocks(
        refs,
        (
            "Caruso ",
            "Haas-Desmarais ",
            "Junker ",
            "Leal ",
            "Sasidharan ",
        ),
    )

    captions = []
    for idx in range(1, 4):
        pat = re.compile(
            rf"\*\*Fig\. S{idx}\*\*\s*(.+?)(?=\n\n\*\*Fig\. S|\n\nCanonical SVG targets:)",
            re.S,
        )
        match = pat.search(supplement)
        if match is None:
            raise RuntimeError(f"missing Fig. S{idx} caption")
        captions.append(re.sub(r"\s+", " ", match.group(1)).strip())

    figure_blocks = []
    names = {
        1: "FIGURE_S1_DERIVATIVE_AGREEMENT.svg",
        2: "FIGURE_S2_SCENARIO_SIGN_MAPS.svg",
        3: "FIGURE_S4_QUANTITATIVE_ROBUSTNESS.svg",
    }
    for idx in range(1, 4):
        figure_blocks.append(
            f"{PAGEBREAK}\n\n### Figure S{idx}\n\n{captions[idx - 1]}\n\n"
            f"![](../../../manuscript/supplementary/figures/{names[idx]})"
        )
    figures_joined = "\n\n".join(figure_blocks)

    return (
        "# Appendix S1\n\n"
        + authors.group(0)
        + "\n\n**Manuscript title:** "
        + title
        + "\n\n**Journal:** Ecology\n\n"
        + "## Section S1: Scope and inference boundary\n\n"
        + "This appendix contains reader-facing supporting figures for the Mechanism → Pattern paper. "
        + "It preserves the same inference boundary as the Main Document: finite-grid occupancy is not empirical prevalence; "
        + "marginal or same-system route evidence is not a direct estimate of \\(W_{AD}\\); and zero strict joint-cost estimates means \\(\\kappa\\) is unidentified, not zero.\n\n"
        + "The complete parameter grid, local-case records, route ledger, conditionality records, direct-identification audits, and registered stopping batches are machine-readable data products rather than Appendix tables. "
        + "Under ESA's Open Research policy these spreadsheet-format records belong in the external data/code repository, not in the Supporting Information file list. "
        + "Their descriptive mapping is provided in the Open Research data manifest generated with this submission package.\n\n"
        + "## Section S2: Supporting figures\n\n"
        + figures_joined
        + "\n\n"
        + PAGEBREAK
        + "\n\n## References\n\n"
        + appendix_refs
        + "\n"
    )


def build_open_research_manifest() -> str:
    mapping = [
        ("model_parameters_and_scaling.csv", "TABLE_S1_PARAMETERS_AND_SCALING.csv", "Complete parameter definitions, finite-grid coordinates, response-shape parameters, scaling, and numerical tolerance."),
        ("finite_grid_local_cases.csv", "TABLE_S2_LOCAL_CASES.csv", "All 162 local phenotype × ecological-context cases and classifications across the declared tested set."),
        ("mechanism_pattern_route_ledger.csv", "TABLE_S3_MECHANISM_PATTERN_LEDGER.csv", "Full source-adjudicated mechanism/Pattern route ledger: 56 route records across 25 independent biological clusters."),
        ("conditionality_context_records.csv", "TABLE_S4_CONDITIONALITY_AND_CONTEXT.csv", "Conditionality/sign-switch records and seven context-only programs with record type and provenance."),
        ("direct_identification_audits.csv", "TABLE_S5_DIRECT_IDENTIFICATION_AUDITS.csv", "Direct A×D and direct joint-cost audit families, preserving distinct eligibility schemas."),
        ("pattern_expansion_screening.csv", "TABLE_S6_PATTERN_EXPANSION_SCREENING.csv", "Priority-rescreen sequence and registered Pattern-expansion stopping batches."),
    ]
    DATA_OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for public_name, source_name, description in mapping:
        src = SUPP_TABLE_DIR / source_name
        if not src.exists():
            raise RuntimeError(f"missing supplementary data source: {src}")
        shutil.copyfile(src, DATA_OUT / public_name)
        rows.append((public_name, source_name, description))

    lines = [
        "# Open Research data manifest — Ecology submission package",
        "",
        "These machine-readable files are derived from the canonical supplementary-table builders but are deliberately renamed for external repository deposition. ESA's Open Research policy requires spreadsheet-format data and large tables to be supplied through an external repository rather than the Supporting Information file list.",
        "",
        "| Deposition file | Canonical repository source | Contents |",
        "|---|---|---|",
    ]
    for public_name, source_name, description in rows:
        lines.append(
            f"| `{public_name}` | `manuscript/supplementary/tables/{source_name}` | {description} |"
        )
    lines += [
        "",
        "The exact immutable archival DOI is an acceptance-stage field. During peer review, the public GitHub repository may provide access to novel code; the final accepted version should be archived in a permanent versioned repository such as Zenodo or an equivalent service and cited in the final paper.",
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
