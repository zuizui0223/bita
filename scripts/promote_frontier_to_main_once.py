from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace(path: str, old: str, new: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"missing patch target in {path}: {old[:120]!r}")
    p.write_text(text.replace(old, new), encoding="utf-8")


def replace_section(path: str, start: str, end: str, replacement: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    if text.count(start) != 1 or text.count(end) != 1:
        raise RuntimeError(f"non-unique section markers in {path}: {start!r}, {end!r}")
    a = text.index(start)
    b = text.index(end, a)
    p.write_text(text[:a] + replacement.rstrip() + "\n\n" + text[b:], encoding="utf-8")


MAN = "manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md"

sec42 = r'''### 4.2 Identification-coverage audit

We reclassified a high-information set of published floral systems according to the experimental information required above. The screen was designed to expose distinct design classes, not to estimate their prevalence in the literature. For each study we asked whether \(A\) and \(D\) were distinct and biologically justified, whether they were manipulated or observed, whether a shared \(A\times D\) outcome was available, whether antagonist and pollinator interventions were crossed with the trait states, whether the pollinator-absent baseline could be characterized, and whether a joint-cost assay existed.

Seventeen high-information systems are retained. None reaches the full sequence from trait interaction to channel allocation and independent joint-cost measurement, but `0/17` hides a more informative structure. The studies occupy complementary lower-dimensional faces of the target \(A\times D\times G\times P\) design. Kessler et al. (2008) supplies the strongest direct \(A\times D\)-like trait face; Theis and Adler (2012) crosses manipulated attraction with beetle removal and supplemental hand pollination; Santangelo et al. (2019) crosses defence, herbivore suppression and hand pollination; Egan et al. (2021) supplies a strong consumer factorial with measured traits; and *Pedicularis rex* supplies a selective defence mechanism. These treatments are not equivalent to the strict target axes, but together they show that substantial pieces of the design already exist.

The empirical pattern is therefore **design fragmentation** rather than absence of relevant biology or experimental competence. The practical question for each near miss becomes which additional intervention or measurement would most reduce its remaining identified set.'''
replace_section(MAN, "### 4.2 Identification-coverage audit", "### 4.3 A trait-factorial anchor: Kessler et al. 2008", sec42)

sec46 = r'''### 4.6 Complementary experimental faces

Theis and Adler (2012) provides an unusually informative bridge. Floral fragrance was experimentally enhanced, beetles were repeatedly removed from a crossed subset, and supplemental hand pollination was applied within the fragrance-by-beetle combinations. This creates an \(A\times G\times P_{\mathrm{supp}}\) reproductive backbone. It is not the target pollinator-access contrast—hand pollination supplements rather than removes pollinator service—and the experiment lacks an independent defence axis. Its importance is structural: three of the four target dimensions can already be crossed in a field experiment.

Other studies cover different faces. Kessler et al. (2015) crossed floral scent and nectar production, but nectar is a reward rather than an independently justified antagonist-reducing defence trait. In *Pedicularis rex*, Sun and Huang (2015) manipulated a water-holding bract barrier that strongly affected seed predation without a detected effect on legitimate pollinator or nectar-robber visitation, providing a practical selective-access defence system without an attraction manipulation. Santangelo et al. (2019) similarly demonstrates a defence-by-herbivore-suppression-by-hand-pollination backbone, although defence is whole-plant HCN rather than a strict floral \(D\).

Across the 17 screened systems, no system closes these complementary faces into one valid \(A\times D\times G\times P\) experiment, characterizes \(m_{0,\Delta}\), and supplies an independent attraction-by-defence joint-cost assay.'''
replace_section(MAN, "### 4.6 Other informative near misses", "## 5. Designing an identifiable experiment", sec46)

replace(
    MAN,
    "The strongest conclusion from the reanalysis and coverage audit is narrower and more useful than the claim that attraction–defence biology is understudied. The retained route synthesis shows that the four constituent marginal pathways recur across 25 independent biological clusters, including same-system and context-switching architectures. Ecologists also manipulate floral traits, pollination and antagonists in sophisticated experiments. Kessler et al. (2008) shows that a direct attraction-by-defence-like trait factorial can be built in the field, whereas Egan et al. (2021) shows that pollination and herbivory can be crossed to estimate context-dependent selection. What remains rare in the screened evidence is the intersection of these recurrent biological channels and these experimental design components on the same trait coordinates and outcome scale.\n",
    "The strongest conclusion from the reanalysis and coverage audit is narrower and more useful than the claim that attraction–defence biology is understudied. The retained route synthesis shows that the four constituent marginal pathways recur across 25 independent biological clusters, including same-system and context-switching architectures. The 17-system design audit then shows that sophisticated experimental faces of the target architecture also recur: Kessler et al. (2008) supplies an A×D-like trait face, Theis and Adler (2012) an A×G×pollination-supplementation bridge, Santangelo et al. (2019) a defence×consumer×pollination-supplementation bridge, and Egan et al. (2021) a consumer-factorial backbone. What remains missing is closure of these faces on the same biologically valid trait coordinates and outcome scale.\n",
)
replace(
    MAN,
    "The current empirical audit is likewise a high-information design audit rather than a systematic estimate of how often each design class occurs in the literature. The 16 systems were selected because they are close to the identification target or expose informative failure modes. A future systematic review could quantify design prevalence, but such a count is not needed to demonstrate the logical distinction among total interaction, consumer-context modification and channel identification.\n",
    "The current empirical audit is likewise a high-information design audit rather than a systematic estimate of how often each design class occurs in the literature. The 17 systems were selected because they are close to the identification target or expose informative failure modes. The resulting face counts therefore describe evidence capacity, not design prevalence.\n",
)
replace(
    MAN,
    "The four constituent ecological pathway families recur across independent systems, while high-information studies already occupy complementary parts of this identification frontier. A direct trait factorial, a consumer factorial, a selective floral defence manipulation and a linked public-data panel each exist, but largely in different studies. The empirical gap is therefore not absence of relevant biology but fragmentation of the information needed to allocate a joint interaction. This also makes the next experiment study-specific: add the measurement or intervention that most reduces the remaining identified set rather than simply collecting another marginal association.\n",
    "The four constituent ecological pathway families recur across independent systems, while high-information studies already occupy complementary faces of the identification frontier. A direct A×D-like trait factorial, A×G×pollination-supplementation and defence×consumer×pollination-supplementation bridges, a consumer factorial, a selective floral defence manipulation and a linked public-data panel all exist, but in different systems. The empirical gap is therefore design fragmentation: the next experiment can reuse a strong existing backbone and add the missing module that most reduces its identified set.\n",
)
replace(
    MAN,
    "Core sources cited in this draft include Adler (2008), Catford et al. (2022), Egan et al. (2021), Kessler and Halitschke (2009), Kessler et al. (2008, 2015), Lucas-Barbosa (2016), McCall and Irwin (2006), Soper Gorden and Adler (2018), Strauss and Whittall (2006), and Sun and Huang (2015).",
    "Core sources cited in this draft include Adler (2008), Catford et al. (2022), Egan et al. (2021), Kessler and Halitschke (2009), Kessler et al. (2008, 2015), Lucas-Barbosa (2016), McCall and Irwin (2006), Soper Gorden and Adler (2018), Strauss and Whittall (2006), Sun and Huang (2015), and Theis and Adler (2012).",
)

SUPP = "manuscript/supplementary/SUPPLEMENT_IDENTIFICATION_DESIGN.md"
replace(
    SUPP,
    "The current matrix contains 16 systems. Fixed conclusions are:\n\n```text\nclosest full A×D-like trait factorial:      Kessler et al. 2008\nclosest crossed G×P-like consumer factorial: Egan et al. 2021\nindependent kappa assay:                    0\nfull rho/iota/kappa identification:         0\n```\n\nThe main empirical pattern is not absence of sophisticated experiments, but separation of the required components across different studies.\n",
    "The current matrix contains 17 systems. Fixed conclusions are:\n\n```text\nclosest full A×D-like trait factorial:       Kessler et al. 2008\nA×G×pollination-supplementation bridge:      Theis & Adler 2012\nD×G×pollination-supplementation bridge:      Santangelo et al. 2019\nclosest crossed G×P-like consumer factorial: Egan et al. 2021\nindependent kappa assay:                     0\nfull rho/iota/kappa identification:          0\n```\n\nThe main empirical pattern is design fragmentation: complementary lower-dimensional faces of the target A×D×G×P architecture occur in different systems. Supplemental hand pollination is not treated as a pollinator-access toggle, and whole-plant defence is not relabelled as flower-specific D.\n\nDerived frontier products:\n\n```text\nempirical/identification_design/IDENTIFICATION_FRONTIER_AUGMENTATION_V1.csv\nempirical/identification_design/IDENTIFICATION_FRONTIER_AUGMENTATION_V1.md\nempirical/identification_design/HYPERCUBE_FACE_COVERAGE_V1.csv\nempirical/identification_design/HYPERCUBE_FACE_COVERAGE_V1.md\nempirical/identification_design/THEIS_ADLER_2012_IDENTIFICATION_REAUDIT_V1.md\n```\n",
)

CAP = "manuscript/IDENTIFICATION_DESIGN_FIGURE_CAPTIONS.md"
old_cap = "**Figure 4. Constituent ecological channels recur, but mechanism allocation remains unidentified.** The retained mechanism-route synthesis contains 56 route records across 25 independent biological clusters and covers all four marginal pathway families; these overlapping counts demonstrate recurrence rather than channel-interaction identification or natural prevalence. Kessler et al. (2008) is the closest trait-factorial anchor, whereas Egan et al. (2021) supplies the complementary consumer-factorial structure. The lower panel shows the *Impatiens capensis* retrofit: the observational `A×D` term and its randomized robbing, florivory, and pollination modifiers are estimable, but all eight target 95% intervals cross zero. Across 16 screened high-information systems, independent joint-cost assays and full channel identification are absent; the studies instead occupy complementary faces of a fragmented identification frontier."
new_cap = "**Figure 4. Constituent channels and complementary experimental faces recur, but mechanism allocation remains unidentified.** The retained route synthesis contains 56 records across 25 independent biological clusters and covers all four marginal pathway families; these overlapping counts demonstrate recurrence rather than prevalence or channel identification. The upper panel shows complementary experimental faces: Kessler et al. (2008) supplies an A×D-like trait factorial, Egan et al. (2021) a consumer-factorial backbone with measured traits, and Theis and Adler (2012) an A×G×pollination-supplementation bridge. Supplemental hand pollination is not a pollinator-access toggle. The lower panel shows the *Impatiens capensis* retrofit, where all eight target 95% intervals cross zero. Across 17 screened high-information systems, independent joint-cost assays and full channel identification remain absent; the stronger result is design fragmentation across the target A×D×G×P hypercube."
replace(CAP, old_cap, new_cap)

# Replace the complete Fig. 4 builder while preserving the lower Impatiens forest plot.
FIG = ROOT / "scripts/build_identification_design_figures_svg.py"
text = FIG.read_text(encoding="utf-8")
start = text.index("def fig4() -> str:")
end = text.index("\ndef fig5() -> str:", start)
new_fig4 = r'''def fig4() -> str:
    rows=_read_coverage(); targets=_impatiens_targets(); pattern=_pattern_counts()
    b=['<text x="650" y="42" text-anchor="middle" class="title">Experimental faces recur, but mechanism allocation remains unidentified</text>']
    b.append(_box(35,85,390,220,"A×D face — Kessler 2008",["benzylacetone × nicotine", "direct reproductive A×D-like interaction", "published Δ ≈ +0.19 to +0.25", "missing: selective G/P toggles", "systemic-D caveat"],"dark"))
    b.append(_box(455,85,390,220,"G×P face — Egan 2021",["herbivory × pollination environment", "attraction/defence traits measured", "strong consumer-factorial backbone", "missing: manipulated floral A×D", "defence partly leaf-derived"],"dark"))
    b.append(_box(875,85,390,220,"A×G×Pₛ — Theis 2012",["fragrance × beetle removal", "× supplemental hand pollination", "three-factor reproductive bridge", "missing: distinct D axis", "P supplementation ≠ access toggle"],"dark"))
    b.append('<text x="650" y="345" text-anchor="middle" class="sub">The missing object is closure of these faces in one valid A×D×G×P experiment</text>')
    b.append(f'<text x="650" y="378" text-anchor="middle" class="tiny">Mechanism Pattern: {pattern["records"]} routes / {pattern["clusters"]} clusters | A→P {pattern["a_poll"]} | A→G {pattern["a_ant"]} | D→G {pattern["d_ant"]} | D→P {pattern["d_poll"]} | same-system {pattern["same"]} | switches {pattern["switch"]}</text>')
    b.append(f'<text x="650" y="405" text-anchor="middle" class="small">Route recurrence ≠ channel identification | {len(rows)}-system frontier: independent κ assay 0; full identification 0</text>')
    b.append('<text x="60" y="430" class="sub">Impatiens public-data retrofit: observational A×D and randomized-agent modifiers</text>')
    x0=600; w=600
    for tick in [-1.5,-1.0,-0.5,0,0.5,1.0]:
        x=_xscale(tick,x0=x0,width=w)
        b.append(f'<line x1="{x}" y1="455" x2="{x}" y2="830" class="dash"/><text x="{x}" y="850" text-anchor="middle" class="tiny">{tick:+.1f}</text>')
    label_map={"A_z:D_z":"A×D","A_z:D_z:Robbing_c":"A×D×Robbing","A_z:D_z:Florivory_c":"A×D×Florivory","A_z:D_z:Pollination_c":"A×D×Pollination"}
    order=["A_z:D_z","A_z:D_z:Robbing_c","A_z:D_z:Florivory_c","A_z:D_z:Pollination_c"]
    targets=sorted(targets,key=lambda r:(str(r["analysis"]), order.index(str(r["term"]))))
    y=485; last_analysis=None
    for r in targets:
        analysis=str(r["analysis"])
        if analysis!=last_analysis:
            short="CH fruits/day" if "fruit" in analysis.lower() and "seed" not in analysis.lower() else "seeds/CH fruit"
            b.append(f'<text x="70" y="{y}" class="small">{escape(short)}</text>'); y+=25; last_analysis=analysis
        lo=_xscale(float(r["lo"]),x0=x0,width=w); hi=_xscale(float(r["hi"]),x0=x0,width=w); est=_xscale(float(r["estimate"]),x0=x0,width=w)
        b.append(f'<text x="230" y="{y+5}" class="tiny">{escape(label_map.get(str(r["term"]),str(r["term"])))}</text>')
        b.append(f'<line x1="{lo}" y1="{y}" x2="{hi}" y2="{y}" class="line"/><circle cx="{est}" cy="{y}" r="5" fill="#222"/>')
        y+=38
    b.append('<text x="900" y="885" text-anchor="middle" class="small">All eight target intervals cross zero; context modification is estimable but unresolved.</text>')
    return _svg(1300,920,"".join(b))
'''
FIG.write_text(text[:start] + new_fig4.rstrip() + text[end:], encoding="utf-8")

# Live docs: promote 17-system / hypercube terminology without changing page claims yet.
for rel in [
    "README.md",
    "SUPPLEMENT_MANIFEST.md",
    "docs/FINAL_SUBMISSION_AUDIT.md",
    "docs/SUBMISSION_SCOPE.md",
    "submission/COVER_LETTER_ECOLOGY_CONCEPTS_SYNTHESIS.md",
    "submission/ECOLOGY_CONCEPTS_SYNTHESIS_FIT_AUDIT.md",
    "submission/ECOLOGY_UPLOAD_PACKAGE_PLAN.md",
    "submission/MANUSCRIPT_AUDIT_V2.md",
    "submission/SUBMISSION_CHECKLIST.md",
    "submission/TARGET_JOURNAL_STRATEGY.md",
]:
    p = ROOT / rel
    t = p.read_text(encoding="utf-8")
    t = t.replace("16-system", "17-system").replace("16 systems", "17 systems").replace("16 screened", "17 screened")
    p.write_text(t, encoding="utf-8")
