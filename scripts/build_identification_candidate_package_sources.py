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
    if len(entries) != 12:
        raise RuntimeError(f"expected 12 focused bibliography entries, found {len(entries)}")
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
    # real section break before the abstract so line-number formatting can be
    # reused from the established Ecology formatter.
    if "## Abstract" not in pre_refs:
        raise RuntimeError("candidate manuscript has no Abstract heading")
    front, rest = pre_refs.split("## Abstract", 1)
    front = front.rstrip()
    body = "## Abstract" + rest

    refs = _focused_reference_text()
    captions = _figure_captions()

    # This generated Markdown lives four directories below repository root:
    # submission/ecology/identification_candidate/generated/. Keep figure paths
    # relative to the Markdown file so pandoc embeds the actual SVGs rather than
    # silently replacing them with alt text.
    figure_blocks: list[str] = []
    for idx, caption in enumerate(captions, 1):
        figure_blocks.append(
            f"{PAGE_BREAK}\n\n{caption}\n\n"
            f"![](../../../../manuscript/identification_figures/FIGURE_{idx}_IDENTIFICATION_DESIGN.svg)"
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
        + "\n\n## Figure captions and figures\n\n"
        + "\n\n".join(figure_blocks)
        + "\n"
    )


def build_supplement_source() -> str:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    title = manuscript.splitlines()[0].removeprefix("# ").strip()
    author_match = re.search(r"\*\*Authors and affiliations:\*\*.*", manuscript)
    if author_match is None:
        raise RuntimeError("candidate manuscript missing authors field")

    supplement = SUPPLEMENT.read_text(encoding="utf-8").strip()
    old_s1 = "../../../../manuscript/supplementary/figures/FIGURE_S1_DERIVATIVE_AGREEMENT.svg"
    old_s2 = "../../../../manuscript/supplementary/figures/FIGURE_S2_SCENARIO_SIGN_MAPS.svg"

    return (
        "# Appendix S1 — Identification design\n\n"
        + author_match.group(0)
        + f"\n\n**Manuscript title:** {title}\n\n**Journal:** Ecology\n\n"
        + supplement
        + f"\n\n{PAGE_BREAK}\n\n## Supplementary Figure S1 — continuous-limit implementation check\n\n"
        + "The analytic mixed partial and central finite-difference implementation are compared across the original finite sensitivity design. This is a software check, not empirical validation.\n\n"
        + f"![]({old_s1})\n\n"
        + f"{PAGE_BREAK}\n\n## Supplementary Figure S2 — response-shape sensitivity maps\n\n"
        + "Scenario-specific sign maps show the original response-shape sensitivity analysis. Cell occupancy reflects the chosen finite grid and is not ecological prevalence.\n\n"
        + f"![]({old_s2})\n"
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    main_path = OUT / "MANUSCRIPT_IDENTIFICATION_CANDIDATE.md"
    supp_path = OUT / "APPENDIX_IDENTIFICATION_CANDIDATE.md"
    main_path.write_text(build_main_source(), encoding="utf-8")
    supp_path.write_text(build_supplement_source(), encoding="utf-8")
    print(main_path)
    print(supp_path)


if __name__ == "__main__":
    main()
