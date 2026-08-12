"""Apply current Theoretical Ecology submission-format requirements.

This script changes presentation/metadata structure only. It does not alter Part I
mathematics, the saturated Pattern evidence counts, or any quantitative result.
Author-controlled declarations remain explicit placeholders rather than being
invented.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"
PORTAL = ROOT / "submission" / "AUTHOR_AND_PORTAL_METADATA_TEMPLATE.md"
COVER = ROOT / "submission" / "COVER_LETTER_THEORETICAL_ECOLOGY.md"

ABSTRACT = (
    "Flowers must attract mutualists while remaining exposed to florivores, nectar robbers, pathogens, and other antagonists. "
    "We ask what mechanism determines whether floral attraction and defence are locally complementary or substitutable, and what cross-system patterns recur empirically. "
    "In Part I, we derive a local theory for one attraction trait, one flower-specific antagonist-reducing trait, and one outcome scale. After an explicit orientation gate, the mixed partial is the balance between antagonist relief, pollinator interference, and direct joint-cost curvature, \\(W_{AD}=\\rho-\\iota-\\kappa\\). "
    "The same total curvature can arise from different channel allocations, so total fitness alone does not identify mechanism. Across 2,592 endpoint-normalized sensitivity evaluations, both complementary and substitutable regimes occur. "
    "In Part II, a registered synthesis yields 56 route-level records from 25 independent biological study clusters, including 14 same-system multi-route and 17 context/sign-switch clusters, while seven context-only programs are kept outside route counts. "
    "A random-effects reanalysis of floral larceny shows reductions in female fitness (log response ratio -0.210; 48 clusters), nectar standing crop (-0.483; 28), and legitimate visitation (-0.291; 22), with extreme heterogeneity. "
    "A second 32-study-component synthesis shows shared pollinator and florivore responsiveness to floral volatiles but strong context dependence. Direct \\(A\\times D\\) evidence remains one sign-unresolved cluster, and no strict direct joint-cost estimate was found. "
    "Thus constituent mechanisms recur across systems, but their realised balance is context dependent rather than universally complementary or substitutable."
)

KEYWORDS = "attraction-defence interaction; floral defence; florivory; mechanism; meta-analysis; pollination"


def replace_between(text: str, start: str, end: str, replacement: str) -> str:
    i = text.index(start) + len(start)
    j = text.index(end, i)
    return text[:i] + replacement + text[j:]


def normalize_manuscript(text: str) -> str:
    # Abstract and keywords: journal requires 150–250 words and 4–6 keywords.
    text = replace_between(text, "## Abstract\n\n", "\n\n**Keywords:**", ABSTRACT)
    keyword_start = text.index("**Keywords:**")
    keyword_end = text.index("\n\n## 1. Introduction", keyword_start)
    text = text[:keyword_start] + f"**Keywords:** {KEYWORDS}" + text[keyword_end:]

    # Make missing title-page information explicit without inventing author data.
    title_line_end = text.index("\n", 2)
    title_meta = (
        "\n\n**Authors and affiliations:** [Author-controlled; insert final publication names and affiliations before submission.]\n\n"
        "**Corresponding author:** [Author-controlled; insert name and active e-mail address.]\n\n"
        "**ORCID(s):** [Insert available 16-digit ORCID identifiers after author approval.]"
    )
    if "**Authors and affiliations:**" not in text[: text.index("## Abstract")]:
        text = text[:title_line_end] + title_meta + text[title_line_end:]

    # Required disclosure because LLM use here extends beyond copy editing.
    disclosure_heading = "### 4.3 Computational and AI-assisted workflow transparency"
    if disclosure_heading not in text:
        marker = "## 5. Part II results — meta-analytic patterns across systems"
        disclosure = (
            "### 4.3 Computational and AI-assisted workflow transparency\n\n"
            "During analysis and manuscript development, an OpenAI large language model was used to assist code generation, structured literature triage, and manuscript drafting. AI-generated output was not treated as empirical evidence. Source claims entered the admitted evidence architecture only through source-linked audit records, numerical results were generated or reconstructed from committed code and data products, and manuscript-facing counts and figures were protected by repository regression tests. The authors retain responsibility for the final scientific content and must confirm this disclosure together with the exact submitted version.\n\n"
        )
        text = text.replace(marker, disclosure + marker, 1)

    # Springer caption form: bold "Fig." + bold number, no punctuation after number
    # and no punctuation at the end of the caption.
    caption_map = {
        "**Figure 1. Mechanistic architecture of the local attraction-defence interaction.** Attraction may increase mutualist service and antagonist exposure. A focal flower-specific defence trait is defined by an operational antagonist-reduction role, but the same trait may interfere with legitimate pollinator use. Attraction and defence may also interact through direct joint-cost curvature. After the orientation gate is established, the local mixed partial is \\(W_{AD}=\\rho-\\iota-\\kappa\\), where \\(\\rho\\) is antagonist relief, \\(\\iota\\) is mutualist interference, and \\(\\kappa\\) is direct joint-cost curvature. The diagram does not imply that every route occurs in every system or that the components are identifiable from total fitness alone.":
        "**Fig. 1** Mechanistic architecture of the local attraction-defence interaction. Attraction may increase mutualist service and antagonist exposure. A focal flower-specific defence trait is defined by an operational antagonist-reduction role, but the same trait may interfere with legitimate pollinator use. Attraction and defence may also interact through direct joint-cost curvature. After the orientation gate is established, the local mixed partial is \\(W_{AD}=\\rho-\\iota-\\kappa\\), where \\(\\rho\\) is antagonist relief, \\(\\iota\\) is mutualist interference, and \\(\\kappa\\) is direct joint-cost curvature. The diagram does not imply that every route occurs in every system or that the components are identifiable from total fitness alone",
        "**Figure 2. Conditional sign regimes in the endpoint-normalized implemented corollary.** The declared finite design evaluates focal attraction and defence coordinates, exogenous pollinator-service and antagonist-pressure indices, an auxiliary reproductive-assurance moderator, four biological parameter scenarios, and four endpoint-normalized response-shape variants. Counts and percentages are unweighted occupancies of the declared finite tested set, not estimates of prevalence in nature. Response-shape unanimity is evaluated within fixed biological scenarios, whereas the full tested set deliberately combines scenarios with opposing route strengths.":
        "**Fig. 2** Conditional sign regimes in the endpoint-normalized implemented corollary. The declared finite design evaluates focal attraction and defence coordinates, exogenous pollinator-service and antagonist-pressure indices, an auxiliary reproductive-assurance moderator, four biological parameter scenarios, and four endpoint-normalized response-shape variants. Counts and percentages are unweighted occupancies of the declared finite tested set, not estimates of prevalence in nature. Response-shape unanimity is evaluated within fixed biological scenarios, whereas the full tested set deliberately combines scenarios with opposing route strengths",
        "**Figure 3. Meta-analytic pattern architecture and identification boundary.** Source-adjudicated evidence is organized as four marginal route families, same-system multi-route regimes, context/sign-switch and context-only programs, two reproduced quantitative synthesis modules, three secondary contextual syntheses, the saturated direct \\(A\\times D\\) layer, and the direct joint-cost search. Counts indicate evidence capacity in the screened architecture rather than prevalence. Guarded defence, spatial/temporal filtering, visitor functional-mode switching, and lifecycle-role reversal are recurrent state classes. Marginal, same-system, and secondary contextual evidence terminate at the inference boundary and are not combined into an estimate of \\(W_{AD}\\).":
        "**Fig. 3** Meta-analytic pattern architecture and identification boundary. Source-adjudicated evidence is organized as four marginal route families, same-system multi-route regimes, context/sign-switch and context-only programs, two reproduced quantitative synthesis modules, three secondary contextual syntheses, the saturated direct \\(A\\times D\\) layer, and the direct joint-cost search. Counts indicate evidence capacity in the screened architecture rather than prevalence. Guarded defence, spatial/temporal filtering, visitor functional-mode switching, and lifecycle-role reversal are recurrent state classes. Marginal, same-system, and secondary contextual evidence terminate at the inference boundary and are not combined into an estimate of \\(W_{AD}\\)",
    }
    for old, new in caption_map.items():
        if old in text:
            text = text.replace(old, new, 1)

    # Remove pre-reference declarations and move the required statements after References.
    pre_start = text.index("## Data and code availability\n")
    refs_start = text.index("## References\n", pre_start)
    data_block = text[pre_start: text.index("## Author contributions\n", pre_start)].strip()
    text = text[:pre_start] + text[refs_start:]

    # Append required Statements and Declarations after the complete reference list.
    if "## Statements and Declarations" not in text:
        statements = (
            "\n\n## Statements and Declarations\n\n"
            "### Funding\n\n"
            "[Author confirmation required. State all funding agencies and grant numbers, or explicitly state that no funds, grants, or other support were received.]\n\n"
            "### Competing interests\n\n"
            "[Author confirmation required. Provide the final financial and non-financial competing-interest statement for all authors through both the manuscript and submission interface.]\n\n"
            "### Author contributions\n\n"
            "[Author-controlled. Complete the contribution statement after the final author list and CRediT roles are approved.]\n\n"
            "### Data and code availability\n\n"
            + data_block.replace("## Data and code availability\n\n", "")
        )
        text = text.rstrip() + statements + "\n"
    return text


def normalize_portal(text: str) -> str:
    text = replace_between(text, "### Abstract\n\n", "\n\n### Keywords", ABSTRACT)
    text = replace_between(
        text,
        "### Keywords\n\n",
        "\n\n## Authors",
        "\n".join(f"- {kw.strip()}" for kw in KEYWORDS.split(";")),
    )
    text = text.replace("Provide 4–6 reviewers", "Provide exactly 5 potential reviewers")
    return text


def normalize_cover(text: str) -> str:
    # Replace the long old abstract-like quantitative sentence only if needed? No:
    # cover letter can stay narrative. Add the journal-required 5-reviewer section.
    if "## Potential reviewers" not in text:
        marker = "\nThank you for considering our manuscript.\n"
        reviewers = (
            "\n## Potential reviewers\n\n"
            "*The journal requests five potential reviewers. These must be selected and conflict-checked by the authors before submission; names are intentionally not inferred here.*\n\n"
            "1. [Name — institution — e-mail — expertise — conflict check]\n"
            "2. [Name — institution — e-mail — expertise — conflict check]\n"
            "3. [Name — institution — e-mail — expertise — conflict check]\n"
            "4. [Name — institution — e-mail — expertise — conflict check]\n"
            "5. [Name — institution — e-mail — expertise — conflict check]\n"
        )
        if marker not in text:
            raise RuntimeError("Cover-letter closing anchor not found")
        text = text.replace(marker, reviewers + marker, 1)
    return text


def main() -> None:
    MANUSCRIPT.write_text(normalize_manuscript(MANUSCRIPT.read_text(encoding="utf-8")), encoding="utf-8")
    PORTAL.write_text(normalize_portal(PORTAL.read_text(encoding="utf-8")), encoding="utf-8")
    COVER.write_text(normalize_cover(COVER.read_text(encoding="utf-8")), encoding="utf-8")
    print("applied Theoretical Ecology abstract, keyword, declaration, AI-disclosure, caption, and reviewer-slot requirements")


if __name__ == "__main__":
    main()
