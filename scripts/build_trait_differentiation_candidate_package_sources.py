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

CANDIDATE_ABSTRACT = """Multifunctional traits can face conflicting functional optima. One solution is compromise on a shared trait axis; another is differentiation across partly independent axes. General specialization theory establishes that trade-offs can favour division of labour, but it does not by itself connect an observed ecological compromise to the mechanism of a resulting multi-trait phenotype. We formulate that bridge as an architecture comparison. If a differentiated architecture contains the shared phenotype on its diagonal, its optimized fitness before any extra fixed architecture cost cannot be lower than the best shared compromise. If residual coupling enters as a non-negative penalty, stronger coupling cannot increase the fitness recoverable by differentiation. In a quadratic baseline, the shared-axis conflict load is \(L_S^*\), residual coupling leaves a decoupling fraction \(s\) of the function-specific separation, and the same fraction of conflict loss is recoverable. Thus \(\Delta_{arch}=sL_S^*-K\), where \(K\) is the additional architecture cost. Differentiation is favoured when the recovered compromise loss exceeds \(K\). A registered 300-condition convex power-loss design finds strict positive recovery in all 300 nonzero-conflict evaluations and increasing recovery with optimum separation in 60/60 declared series; coupling monotonicity in 60/60 series verifies the structural result numerically. Cichlid oral and pharyngeal jaws illustrate partial differentiation with residual integration, whereas *Dalechampia* illustrates historical redeployment and addition of functional structures. We then use floral attraction and defence as a worked case showing that, once multiple trait axes exist, their total fitness interaction still does not identify the ecological pathway producing the apparent release. Across 56 route records from 25 independent biological study clusters and a 17-system high-information audit, the constituent pathways recur but the required identification dimensions remain fragmented across experiments. The framework therefore links shared-trait balance, incomplete differentiation and causal mechanism identification without equating structural separation with evolutionary independence or historical trait splitting."""

GENERAL_PROPOSITIONS = r"""### 2.1 General architecture propositions

Before choosing a response shape, write the best loss on the shared axis as

\[
L_S^*=\min_z\{\ell_1(z)+\ell_2(z)\}.
\]

Let the differentiated architecture have pre-fixed-cost loss

\[
L_{D,0}(x,y;\lambda)
=\ell_1(x)+\ell_2(y)+\lambda c(x,y),
\]

with \(\lambda\ge0\), \(c(x,y)\ge0\), and \(c(z,z)=0\). The last condition means that the two-axis architecture contains every shared phenotype on its diagonal before the extra fixed architecture cost is charged. Define

\[
L_{D,0}^*(\lambda)=\min_{x,y}L_{D,0}(x,y;\lambda),
\qquad
R(\lambda)=L_S^*-L_{D,0}^*(\lambda).
\]

**Proposition 1 — nested-architecture weak dominance.** Because the differentiated optimizer can always choose \(x=y=z^*\),

\[
L_{D,0}^*(\lambda)\le L_S^*,
\qquad
R(\lambda)\ge0.
\]

This feasible-set statement does not require quadratic, convex or smooth loss functions. It is deliberately weak: \(R=0\) is possible when the added axes cannot exploit a beneficial off-diagonal state. If \(K\ge0\) is the additional fixed architecture cost, then

\[
\boxed{\Delta_{arch}=R-K},
\qquad
\boxed{\Delta_{arch}>0\iff K<R}.
\]

Thus adding a trait axis is not automatically advantageous after its costs are paid. The relevant quantity is the loss that the enlarged architecture can actually recover from the original compromise.

**Proposition 2 — residual-coupling monotonicity.** If coupling enters as the non-negative scaled penalty \(\lambda c(x,y)\), then for \(\lambda_2>\lambda_1\) every fixed \((x,y)\) state is at least as costly under \(\lambda_2\). Hence

\[
L_{D,0}^*(\lambda_2)\ge L_{D,0}^*(\lambda_1)
\]

and therefore

\[
\boxed{R(\lambda_2)\le R(\lambda_1)}.
\]

Stronger residual coupling cannot increase recoverable compromise loss within this declared architecture. What remains shape dependent is whether recovery is strictly positive when functional optima differ and how rapidly recovery grows as those optima separate. The quadratic model gives a closed-form answer to those stricter questions, and the nonquadratic analysis tests them over a declared convex family.
"""

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


def _replace_abstract(text: str) -> str:
    prefix, tail = text.split("## Abstract\n\n", 1)
    _, after = tail.split("\n\n**Keywords:**", 1)
    return prefix + "## Abstract\n\n" + CANDIDATE_ABSTRACT + "\n\n**Keywords:**" + after


def _promote_general_propositions(text: str) -> str:
    section = "## 2. From shared-trait compromise to differentiated architecture\n\n"
    if section not in text:
        raise RuntimeError("cannot locate Chapter 2 architecture section")

    # Renumber the quadratic subsections after inserting the general propositions.
    replacements = (
        ("### 2.4 Comparative statics", "### 2.5 Comparative statics"),
        ("### 2.3 Decoupling fraction and the amount of compromise that can be recovered", "### 2.4 Decoupling fraction and the amount of compromise that can be recovered"),
        ("### 2.2 Differentiated architecture with residual cross-talk", "### 2.3 Differentiated architecture with residual cross-talk"),
        ("### 2.1 Shared-axis architecture", "### 2.2 Shared-axis architecture"),
    )
    for old, new in replacements:
        if old not in text:
            raise RuntimeError(f"cannot locate subsection for candidate promotion: {old}")
        text = text.replace(old, new, 1)

    text = text.replace(section, section + GENERAL_PROPOSITIONS + "\n\n", 1)

    robustness_heading = "## 3. Robustness beyond quadratic response shapes\n\n"
    framing = (
        "The weak-dominance and coupling-monotonicity results above do not depend on "
        "quadratic response shapes. The finite robustness analysis therefore asks the "
        "stricter shape-dependent questions: whether recovery is strictly positive for "
        "nonzero conflict and whether larger separation between function-specific optima "
        "continues to increase the recoverable loss across a declared nonlinear family.\n\n"
    )
    if robustness_heading not in text:
        raise RuntimeError("cannot locate nonquadratic robustness section")
    return text.replace(robustness_heading, robustness_heading + framing, 1)


def build_main_source() -> str:
    text = MANUSCRIPT.read_text(encoding="utf-8").strip()
    text = text.replace("**Working integrated Chapter 2 draft — not yet the canonical submission source.**\n\n", "", 1)
    text = _strip_embedded_reference_draft(text)
    text = _replace_abstract(text)
    text = _promote_general_propositions(text)

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
