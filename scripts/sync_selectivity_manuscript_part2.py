from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"

SECTION_52 = "### 5.2 Identification-gap pattern: direct interaction scarcity and joint cost\n\nThe registered direct \\(A\\times D\\) search reached its stopping rule with one strict total reproductive-outcome cluster: Soper Gorden and Adler's (2018) *Impatiens capensis* study. The reconstructed interaction for chasmogamous fruits per plant per day was \\(-0.0820\\pm0.0548\\) SE, whereas the interaction for seeds per chasmogamous fruit was \\(+0.1040\\pm0.1043\\) SE. Both confidence intervals included zero, so the cleanest total-outcome candidate remained sign-unresolved and reproductive-component dependent in point direction.\n\nA higher-specificity crossed floral-trait program nevertheless shows that channel-level interaction signs can reverse with consumer context. Kessler et al. (2015) independently crossed floral benzylacetone emission with floral nectar production. With \\(D\\) oriented as nectar restriction, source-mean pollination-channel crossed contrasts were \\(-0.790\\) for the native visitor community, \\(-0.432\\) under *Manduca sexta*, and \\(+0.8699\\) under *Hyles lineata*. These values are direct crossed-trait contrasts on a mutualist-mediated outcome, not estimates of total \\(W_{AD}\\), and the published summaries do not identify an interaction standard error or confidence interval. They therefore strengthen the context-dependence Pattern without resolving total curvature.\n\nThe independent direct joint-cost search reached its stopping rule with zero strict eligible estimates of the additional intrinsic cost of simultaneous investment in distinct floral attraction and defence/access axes. The correct empirical state for \\(\\kappa\\) is uncertainty, not zero. After Theorem 1 this gap has sharper meaning: the sign of direct joint-cost curvature is the minimal empirical gate for whether the one-sided selectivity bound applies biologically to a focal trait pair."
SECTION_54 = '### 5.4 Meta-analysis 1: floral larceny opened an average antagonist-pressure gate but not a universal one\n\nThe Leal et al. (2025) deposited-synthesis reanalysis recovered a pooled log response ratio of \\(-0.210\\) for female reproductive success across 48 independent study clusters, \\(-0.483\\) for nectar standing crop across 28 clusters, and \\(-0.291\\) for legitimate visitation across 22 clusters. These correspond to approximately 19%, 38%, and 25% reductions on the response-ratio scale, respectively. Male reproductive success was highly heterogeneous and uninformative.\n\nThe female-fitness direction was repeatable but not universal: 35 of 48 clusters (73%) were negative, while the 95% prediction interval was \\(-1.13,+0.71\\) and significantly positive systems occurred. The female-fitness, reward, and visitation pooled directions survived every leave-one-cluster-out refit, the declared within-cluster correlation choices, and reinstatement of quarantined sign-discrepant source rows. Six declared moderator analyses detected no statistically resolved context dependence and explained only 0-8% of the extreme heterogeneity. The synthesis therefore establishes that the antagonist-pressure gate can be open on average while leaving its realised magnitude and even sign strongly system dependent.\n\nThe apparent reward-depletion sequence is not treated as a demonstrated mechanism. Only five clusters measured nectar standing crop, legitimate visitation, and female fitness together, and only two of those showed all three arrows negative. Among the eleven clusters measuring both nectar and visitation, the within-study association between reward depletion and visitation loss was \\(r=-0.17\\), opposite in sign to the simplest reward-depletion prediction and indistinguishable from zero at that sample size. The three pooled arrows are therefore constituent-path evidence, not an end-to-end within-study mechanism chain.\n\nLarceny exposure also reduced legitimate visitation, demonstrating that the environmental indices \\(H\\) and \\(P\\) need not be empirically separable. This observation does not estimate \\(W_{AD}\\); it shows that exposure can move more than one channel at once and that the location of the selectivity window is itself an empirical ecological state.'
SECTION_61 = '### 6.1 A recurrent switching architecture becomes a one-sided window, not a sign criterion\n\nPart I now gives the recurrent route-separation Pattern a precise mathematical role. Under non-negative joint-cost curvature, antagonist relief must exceed pollinator interference before complementarity is possible. Spatial, temporal, chemical, and attack-mode separation can therefore move a system into a **permissive selectivity window**, but they do not determine the sign of \\(W_{AD}\\) once exposure and joint cost are included.\n\nPart II supplies the corresponding biology. Independent systems include guarded states in which antagonist reduction occurs with little detected pollinator cost, barriers whose efficacy depends on consumer size or attack mode, and cases in which the same visitor changes from legitimate pollinator to robber while its arrival rate stays similar. These recurrent switching architectures are exactly what can alter \\(\\rho\\) relative to \\(\\iota\\). Their recurrence supports the existence of the window, not the false two-sided claim that every in-window system must be complementary.\n\nThe larceny synthesis adds the other half of the story: the exposure gate that loads antagonist relief is non-zero on average but strongly heterogeneous. Thus the window can open, but the current empirical synthesis cannot yet predict where it opens in a new system.'
SECTION_63 = '### 6.3 Direct evidence scarcity identifies two different missing measurements\n\nThe saturated direct-interaction search explains why broad pollinator-herbivore literatures overstate how often the required attraction × defence quantity is actually identified. Ecological-agent factorials, cross-organ defence studies, dual-function traits, main-effect-only models, and unlinked datasets are informative about constituent biology without being total \\(A\\times D\\) curvature estimates. The *Impatiens* total-outcome candidate remains sign-unresolved, while the Kessler floral factorials demonstrate context-dependent channel interactions without decomposing total outcome.\n\nThe direct joint-cost gap is now especially informative. Many studies discuss allocation trade-offs or marginal costs, but the registered search found no strict estimate of the cross-cost of simultaneously producing distinct attraction and defence/access axes. Under the one-sided theorem, this is not merely a missing third term: **a negative direct joint-cost curvature is the only route by which complementarity can escape the selectivity window in the declared family**. The empirical state of \\(\\kappa\\) must therefore remain unidentified, and its sign is a high-leverage target rather than a quantity to set silently to zero.'

def replace_section(text, start_heading, next_heading, replacement):
    start = text.index(start_heading + "\n")
    end = text.index(next_heading + "\n", start)
    return text[:start] + replacement.rstrip() + "\n\n" + text[end:]

def replace_any(text, start_headings, next_heading, replacement):
    for heading in start_headings:
        if heading + "\n" in text:
            return replace_section(text, heading, next_heading, replacement)
    raise RuntimeError(f"None of section anchors found: {start_headings}")

def sync(text):
    text = replace_section(text, "### 5.2 Identification-gap pattern: direct interaction scarcity and joint cost", "### 5.3 Conditionality pattern: mechanism channels open, close, and change role", SECTION_52)
    text = replace_any(
        text,
        (
            "### 5.4 Meta-analysis 1: floral larceny imposed recurrent costs with extreme heterogeneity",
            "### 5.4 Meta-analysis 1: floral larceny opened an average antagonist-pressure gate but not a universal one",
        ),
        "### 5.5 Meta-analytic synthesis 2: floral volatile responses were shared but composition-dependent",
        SECTION_54,
    )
    text = replace_any(
        text,
        (
            "### 6.1 A conditional sign boundary is biologically necessary, not merely mathematically possible",
            "### 6.1 A recurrent switching architecture becomes a one-sided window, not a sign criterion",
        ),
        "### 6.2 Constituent-path evidence is not validation of the mixed partial",
        SECTION_61,
    )
    text = replace_any(
        text,
        (
            "### 6.3 Direct evidence scarcity is itself informative",
            "### 6.3 Direct evidence scarcity identifies two different missing measurements",
        ),
        "### 6.4 Relation to correlational selection and fitness-landscape inference",
        SECTION_63,
    )
    return text

def main():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    MANUSCRIPT.write_text(sync(text), encoding="utf-8")
    print("synchronized manuscript empirical bridge story")

if __name__ == "__main__":
    main()
