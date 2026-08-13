from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"

ABSTRACT = "Flowers must attract mutualists while remaining exposed to florivores, nectar robbers, pathogens, and other antagonists. We ask what mechanism determines whether floral attraction and defence are locally complementary or substitutable, and what cross-system patterns recur empirically. In Part I, after an explicit orientation gate, the mixed partial is the balance between antagonist relief, pollinator interference, and direct joint-cost curvature, \\(W_{AD}=\\rho-\\iota-\\kappa\\); this identity is bookkeeping, and total fitness alone does not identify its channel allocation. A stronger one-sided result follows: under non-negative joint-cost curvature, complementarity can occur only inside a selectivity window where antagonist relief exceeds pollinator interference. Across 2,592 endpoint-normalized evaluations and four response-shape variants there are no counterexamples, whereas about 23% of in-window evaluations remain substitutable. In Part II, a registered synthesis yields 56 route-level records from 25 independent biological study clusters. Floral larceny reduces female fitness on average (log response ratio -0.210; 48 clusters), but only 35/48 clusters are negative and the 95% prediction interval spans -1.13 to +0.71; declared moderators explain only 0-8% of heterogeneity. Thus antagonist exposure can open the theoretical window but does not locate it reliably across systems. The constituent mechanisms and switching architecture recur, while direct \\(A\\times D\\) evidence remains sparse and direct joint-cost curvature unmeasured. The integrated result is therefore a one-sided mechanistic bound plus a context-dependent empirical Pattern, with the sign of joint-cost curvature as the minimal missing test of the bound's biological applicability."
SECTION_15 = '### 1.5 Two-part contribution: mechanism and pattern\n\nThe paper is deliberately organized as two linked but inferentially distinct parts.\n\n**Part I — Mechanism.** We derive the local attraction-defence balance, make its orientation and non-identifiability assumptions explicit, and then ask whether any stronger statement survives response-shape variation. The answer is one-sided: under non-negative joint-cost curvature, complementarity is restricted to a selectivity window where antagonist relief exceeds pollinator interference. The window is necessary but not sufficient. This part asks **why the sign changes, where complementarity is permitted, and what can break that bound**.\n\n**Part II — Pattern.** We then use those mechanism classes to organize cross-study evidence. Quantitative meta-analysis is used where compatible effect scales exist; otherwise source-adjudicated study clusters map recurrence, same-system co-occurrence, conditionality, and identification gaps without manufacturing a common effect size. This part asks **which theory-predicted pathways recur, whether the exposure gate is open in nature, and why the window moves among systems**.\n\nThe key synthesis is therefore Mechanism \\(\\rightarrow\\) Pattern, not theory \\(\\rightarrow\\) validation. Cross-system recurrence shows that the constituent processes and switching architecture are biologically real; it does not estimate the prevalence or total sign of \\(W_{AD}\\).'
SECTION_27 = '### 2.7 Selectivity window and one-sided bound\n\nFor the deployed oriented family, define the **selectivity window** as the region in which antagonist relief exceeds pollinator interference before the direct joint-cost term is charged.\n\n**Theorem 1 (one-sided selectivity bound).** If the three deployed terms are non-negative, then\n\n\\[\nW_{AD}>0 \\;\\Longrightarrow\\; \\rho>\\iota.\n\\]\n\nEquivalently, complementarity does not occur outside the selectivity window.\n\nThe proof is immediate from \\(W_{AD}=\\rho-\\iota-\\kappa\\): if \\(W_{AD}>0\\) and \\(\\kappa\\ge0\\), then \\(\\rho-\\iota=W_{AD}+\\kappa>0\\). The proof uses only the non-negative relief-minus-interference-minus-cost structure, preserved by all four declared endpoint-normalized response-shape variants. When \\(\\kappa=0\\), the implication runs both ways and the window becomes the exact sign criterion.\n\nThe converse is not generally true when \\(\\kappa>0\\). Outside the window, complementarity would require \\(\\kappa<\\rho-\\iota\\le0\\). Thus a **negative joint-cost curvature is necessary for the bound to fail, and sufficient when negative enough**. Because the implemented parameterization constrains direct joint cost to be non-negative, this is a structural result of the declared family rather than an empirical statement about joint-cost curvature in nature.'
SECTION_34 = '### 3.4 Verification of the one-sided selectivity bound\n\nThe theorem itself is algebraic; the declared grid verifies that the implementation obeys its premises across the full finite design. Among 2,592 evaluations, all 1,342 complementary evaluations occurred inside the selectivity window, giving **zero false negatives** for the bound. The converse was loose: 397 in-window evaluations were substitutable, so the share of in-window points that were genuinely complementary was 77.2%; approximately 23% of the window therefore failed as a sufficient criterion.\n\nWhen direct joint cost was forced to zero, the window and the sign criterion coincided exactly across the same declared design. These fractions are unweighted finite-grid occupancies, not estimates of natural prevalence. Their role is to distinguish an exact structural implication from the false two-sided rule that the finite design itself rejects.'

def replace_section(text, start_heading, next_heading, replacement):
    start = text.index(start_heading + "\n")
    end = text.index(next_heading + "\n", start)
    return text[:start] + replacement.rstrip() + "\n\n" + text[end:]

def replace_between(text, start_anchor, end_anchor, replacement):
    start = text.index(start_anchor) + len(start_anchor)
    end = text.index(end_anchor, start)
    return text[:start] + replacement + text[end:]

def sync(text):
    text = replace_between(text, "## Abstract\n\n", "\n\n**Keywords:**", ABSTRACT)
    text = replace_section(text, "### 1.5 Two-part contribution: mechanism and pattern", "### 1.6 Paper organization", SECTION_15)
    if "### 2.7 Selectivity window and one-sided bound" not in text:
        anchor = "## 3. Part I results — mechanistic sign regimes"
        if anchor not in text:
            raise RuntimeError("Part I results anchor missing")
        text = text.replace(anchor, SECTION_27 + "\n\n" + anchor, 1)
    if "### 3.4 Verification of the one-sided selectivity bound" not in text:
        anchor = "## 4. Part II — Meta-analysis and cross-study pattern synthesis"
        if anchor not in text:
            raise RuntimeError("Part II anchor missing")
        text = text.replace(anchor, SECTION_34 + "\n\n" + anchor, 1)
    return text

def main():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    MANUSCRIPT.write_text(sync(text), encoding="utf-8")
    print("synchronized manuscript Part I theorem story")

if __name__ == "__main__":
    main()
