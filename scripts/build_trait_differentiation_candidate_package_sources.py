from __future__ import annotations

from pathlib import Path
import re
import shutil


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md"
REFERENCES = ROOT / "manuscript" / "TRAIT_DIFFERENTIATION_REFERENCES_V1.md"
CAPTIONS = ROOT / "manuscript" / "TRAIT_DIFFERENTIATION_FIGURE_CAPTIONS_V1.md"
FIGDIR = ROOT / "manuscript" / "trait_differentiation_figures"
THEORY = ROOT / "theory" / "TRAIT_DIFFERENTIATION_EXTENSION.md"
ROBUSTNESS = ROOT / "docs" / "TRAIT_DIFFERENTIATION_ROBUSTNESS.md"
ROBUSTNESS_JSON = ROOT / "docs" / "TRAIT_DIFFERENTIATION_ROBUSTNESS_READOUT.json"
EMPIRICAL_BRIDGES = ROOT / "docs" / "TRAIT_DIFFERENTIATION_EMPIRICAL_BRIDGES.md"
IDENTIFICATION_SUPPLEMENT = ROOT / "manuscript" / "supplementary" / "SUPPLEMENT_IDENTIFICATION_DESIGN.md"
HIGH_INFO_COVERAGE = ROOT / "empirical" / "identification_design" / "HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V2.csv"
IMPATIENS_RETROFIT = ROOT / "empirical" / "identification_design" / "IMPATIENS_2018_IDENTIFICATION_RETROFIT_V1.json"
OUT = ROOT / "submission" / "ecology" / "trait_differentiation_candidate" / "generated"
DATA_OUT = OUT / "open_research_data"

TITLE_BREAK = "[[ECOLOGY_SECTION_BREAK_AFTER_TITLE]]"
REF_BREAK = "[[ECOLOGY_SECTION_BREAK_AFTER_REFERENCES]]"
PAGE_BREAK = "[[ECOLOGY_PAGE_BREAK]]"

FIGURES = [
    "FIGURE_1_BALANCE_TO_DIFFERENTIATION.svg",
    "FIGURE_2_ARCHITECTURE_BOUNDARY.svg",
    "FIGURE_3_ROBUSTNESS_AND_REALITY.svg",
    "FIGURE_4_MECHANISM_IDENTIFICATION.svg",
    "FIGURE_5_FRAGMENTED_IDENTIFICATION.svg",
]

# Main is intentionally lean. The reference source file is a reusable pool for the
# integrated paper and supplement, whereas Main carries only sources directly
# invoked in the current prose or directly underlying the worked empirical case.
MAIN_REFERENCE_PREFIXES = (
    "Armbruster WS,",
    "Burress ED,",
    "Conith AJ,",
    "Guillaume F,",
    "Rüffler C,",
    "Sack L,",
    "Egan PA,",
    "Kessler D, Gase K, Baldwin IT (2008)",
    "Soper Gorden NL, Adler LS (2018)",
)


def _reference_text() -> str:
    text = REFERENCES.read_text(encoding="utf-8")
    if "## Reference-use guardrail" in text:
        text = text.split("## Reference-use guardrail", 1)[0]
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    pool = [
        p
        for p in paragraphs
        if not p.startswith("#")
        and not p.startswith("This bibliography merges")
    ]

    selected: list[str] = []
    for prefix in MAIN_REFERENCE_PREFIXES:
        matches = [entry for entry in pool if entry.startswith(prefix)]
        if len(matches) != 1:
            raise RuntimeError(
                f"expected exactly one Main reference beginning {prefix!r}, found {len(matches)}"
            )
        selected.append(matches[0])

    if len(selected) != 9:
        raise RuntimeError(f"expected 9 Main references, found {len(selected)}")
    return "\n\n".join(selected)


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
            raise RuntimeError(f"missing Figure {idx} caption")
        title = re.sub(r"\s+", " ", match.group(1)).strip()
        body = re.sub(r"\s+", " ", match.group(2)).strip()
        captions.append(f"**Figure {idx}. {title}** {body}")
    return captions


def _strip_embedded_reference_draft(text: str) -> str:
    markers = (
        "\n## References added for the Chapter 2 reframe",
        "\n## References\n",
    )
    for marker in markers:
        if marker in text:
            return text.split(marker, 1)[0].rstrip()
    raise RuntimeError("integrated manuscript has no recognizable reference boundary")


def build_main_source() -> str:
    text = MANUSCRIPT.read_text(encoding="utf-8").strip()
    text = text.replace("**Working integrated Chapter 2 draft — not yet the canonical submission source.**\n\n", "", 1)
    text = _strip_embedded_reference_draft(text)

    if "## Abstract" not in text:
        raise RuntimeError("integrated manuscript has no Abstract heading")
    front, body_rest = text.split("## Abstract", 1)
    front = front.rstrip()
    body = "## Abstract" + body_rest

    open_research = (
        "**Open Research statement:** Review-stage theory code, robustness readouts, "
        "source-audited empirical bridge materials, and the retained floral identification "
        "products are maintained in the public project repository. The accepted exact "
        "data/code release will be archived permanently and cited in the final article."
    )

    backmatter = (
        "\n\n## Acknowledgments\n\n[Author-controlled; complete before submission.]"
        "\n\n## Author Contributions\n\n[Author-controlled; complete before submission.]"
        "\n\n## Funding\n\n[Author-controlled; insert funding statement or confirmed no-funding statement.]"
        "\n\n## Conflict of Interest Statement\n\n[Author-controlled; complete before submission.]"
    )

    refs = _reference_text()
    captions = _figure_captions()
    figure_blocks: list[str] = []
    for idx, (caption, filename) in enumerate(zip(captions, FIGURES, strict=True), 1):
        if not (FIGDIR / filename).exists():
            raise RuntimeError(f"missing Chapter 2 Figure {idx}: {filename}")
        page_prefix = "" if idx == 1 else f"{PAGE_BREAK}\n\n"
        figure_blocks.append(
            f"{page_prefix}{caption}\n\n"
            f"![](../../../../manuscript/trait_differentiation_figures/{filename})"
        )

    return (
        front
        + "\n\n**Journal:** Ecology\n\n**Manuscript type:** Concepts & Synthesis\n\n"
        + open_research
        + "\n\n"
        + TITLE_BREAK
        + "\n\n"
        + body.strip()
        + backmatter
        + "\n\n## References\n\n"
        + refs
        + "\n\n"
        + REF_BREAK
        + "\n\n"
        + "\n\n".join(figure_blocks)
        + "\n"
    )


def _clean_supporting_doc(path: Path) -> str:
    text = path.read_text(encoding="utf-8").strip()
    # Demote a source-document H1 so the assembled Appendix has one top-level title.
    if text.startswith("# "):
        text = "## " + text[2:]
    return text


def _demote_all_headings(text: str) -> str:
    """Nest a retained standalone document inside the assembled Appendix."""
    return re.sub(r"^(#{1,5})(\s+)", lambda m: "#" + m.group(1) + m.group(2), text, flags=re.M)


def build_appendix_source() -> str:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    title = manuscript.splitlines()[0].removeprefix("# ").strip()
    author_match = re.search(r"\*\*Authors and affiliations:\*\*.*", manuscript)
    if author_match is None:
        raise RuntimeError("integrated manuscript missing authors field")

    theory = _clean_supporting_doc(THEORY)
    robustness = _clean_supporting_doc(ROBUSTNESS)
    bridges = _clean_supporting_doc(EMPIRICAL_BRIDGES)
    identification = _demote_all_headings(
        IDENTIFICATION_SUPPLEMENT.read_text(encoding="utf-8").strip()
    )
    old_s1 = "../../../../manuscript/supplementary/figures/FIGURE_S1_DERIVATIVE_AGREEMENT.svg"
    old_s2 = "../../../../manuscript/supplementary/figures/FIGURE_S2_SCENARIO_SIGN_MAPS.svg"

    return (
        "# Appendix S1 — Trait differentiation and mechanism identification\n\n"
        + author_match.group(0)
        + f"\n\n**Manuscript title:** {title}\n\n**Journal:** Ecology\n\n"
        + "## S1. Shared-versus-differentiated architecture derivation\n\n"
        + theory
        + f"\n\n{PAGE_BREAK}\n\n## S2. Nonquadratic robustness design and readout\n\n"
        + robustness
        + f"\n\n{PAGE_BREAK}\n\n## S3. Cross-system architecture-state anchors\n\n"
        + bridges
        + f"\n\n{PAGE_BREAK}\n\n## S4. Retained floral mechanism-identification supplement\n\n"
        + identification
        + f"\n\n{PAGE_BREAK}\n\n## Supplementary Figure S1 — continuous-limit implementation check\n\n"
        + "The analytic mixed partial and central finite-difference implementation are compared across the historical finite sensitivity design retained for the floral worked case. This is a software check, not empirical validation.\n\n"
        + f"![]({old_s1})\n\n"
        + f"{PAGE_BREAK}\n\n## Supplementary Figure S2 — response-shape sensitivity maps for the floral worked case\n\n"
        + "Scenario-specific sign maps preserve the historical response-shape sensitivity analysis. Cell occupancy reflects the chosen finite grid and is not ecological prevalence.\n\n"
        + f"![]({old_s2})\n"
    )


def build_open_research_manifest() -> str:
    DATA_OUT.mkdir(parents=True, exist_ok=True)
    additions = [
        (
            ROBUSTNESS_JSON,
            DATA_OUT / "trait_differentiation_robustness_readout.json",
            "Registered finite-family trait-differentiation robustness readout.",
        ),
        (
            HIGH_INFO_COVERAGE,
            DATA_OUT / "high_information_identification_coverage.csv",
            "Authoritative V2 high-information floral identification-coverage matrix; screened-set coverage, not prevalence.",
        ),
        (
            IMPATIENS_RETROFIT,
            DATA_OUT / "impatiens_identification_retrofit.json",
            "Aggregate public-data retrofit used in the floral mechanism-identification worked case.",
        ),
    ]
    lines = [
        "# Open Research data manifest — trait-differentiation Chapter 2 candidate",
        "",
        "| Deposition file | Canonical repository source | Contents |",
        "|---|---|---|",
    ]
    for src, dst, description in additions:
        if not src.exists():
            raise RuntimeError(f"missing Open Research source: {src}")
        shutil.copyfile(src, dst)
        lines.append(f"| `{dst.name}` | `{src.relative_to(ROOT)}` | {description} |")
    lines += [
        "",
        "The broader 56-route/25-cluster corpus and source receipts remain in the repository as provenance for the floral worked case and are not prevalence estimates.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "MANUSCRIPT_TRAIT_DIFFERENTIATION_CANDIDATE.md").write_text(
        build_main_source(), encoding="utf-8"
    )
    (OUT / "APPENDIX_S1_TRAIT_DIFFERENTIATION.md").write_text(
        build_appendix_source(), encoding="utf-8"
    )
    (OUT / "OPEN_RESEARCH_DATA_MANIFEST.md").write_text(
        build_open_research_manifest(), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
