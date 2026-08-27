from pathlib import Path

P = Path('manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md')
text = P.read_text(encoding='utf-8')

repls = [
(
"We reclassified a high-information set of published floral systems according to the experimental information required above. The screen was designed to expose distinct design classes, not to estimate their prevalence in the literature. For each study we asked whether \\(A\\) and \\(D\\) were distinct and biologically justified, whether they were manipulated or observed, whether a shared \\(A\\times D\\) outcome was available, whether antagonist and pollinator interventions were crossed with the trait states, whether the pollinator-absent baseline could be characterized, and whether a joint-cost assay existed.",
"We reclassified high-information floral systems by the information required for identification rather than by study quality or literature prevalence: valid A/D coordinates, a shared \\(A\\times D\\) outcome, consumer interventions, pollinator-absent baseline characterization, and independent joint-cost evidence."
),
(
"Seventeen high-information systems are retained. None reaches the full sequence from trait interaction to channel allocation and independent joint-cost measurement, but `0/17` hides a more informative structure. The studies occupy complementary lower-dimensional faces of the target \\(A\\times D\\times G\\times P\\) design. Kessler et al. (2008) supplies the strongest direct \\(A\\times D\\)-like trait face; Theis and Adler (2012) crosses manipulated attraction with beetle removal and supplemental hand pollination; Santangelo et al. (2019) crosses defence, herbivore suppression and hand pollination; Egan et al. (2021) supplies a strong consumer factorial with measured traits; and *Pedicularis rex* supplies a selective defence mechanism. These treatments are not equivalent to the strict target axes, but together they show that substantial pieces of the design already exist.",
"Seventeen high-information systems are retained. None closes the full allocation design, but `0/17` hides complementary lower-dimensional faces of the target \\(A\\times D\\times G\\times P\\) architecture: Kessler et al. (2008) supplies an \\(A\\times D\\)-like trait face, Theis and Adler (2012) an attraction×beetle-removal×hand-pollination bridge, Santangelo et al. (2019) a defence×herbivore-suppression×hand-pollination bridge, Egan et al. (2021) a consumer factorial, and *Pedicularis rex* a selective-defence mechanism. These treatments are not equivalent to the strict target axes."
),
(
"Theis and Adler (2012) provides an unusually informative bridge. Floral fragrance was experimentally enhanced, beetles were repeatedly removed from a crossed subset, and supplemental hand pollination was applied within the fragrance-by-beetle combinations. This creates an \\(A\\times G\\times P_{\\mathrm{supp}}\\) reproductive backbone. It is not the target pollinator-access contrast—hand pollination supplements rather than removes pollinator service—and the experiment lacks an independent defence axis. Its importance is structural: three of the four target dimensions can already be crossed in a field experiment.",
"Theis and Adler (2012) crossed enhanced floral fragrance, beetle removal and supplemental hand pollination, creating an \\(A\\times G\\times P_{\\mathrm{supp}}\\) reproductive backbone. Hand pollination supplements rather than removes pollinator service, and no independent defence axis was crossed, so this is a structural bridge rather than the target P contrast."
),
(
"Other studies cover different faces. Kessler et al. (2015) crossed floral scent and nectar production, but nectar is a reward rather than an independently justified antagonist-reducing defence trait. In *Pedicularis rex*, Sun and Huang (2015) manipulated a water-holding bract barrier that strongly affected seed predation without a detected effect on legitimate pollinator or nectar-robber visitation, providing a practical selective-access defence system without an attraction manipulation. Santangelo et al. (2019) similarly demonstrates a defence-by-herbivore-suppression-by-hand-pollination backbone, although defence is whole-plant HCN rather than a strict floral \\(D\\).",
"Other faces expose different missing axes. Kessler et al. (2015) crossed scent and nectar, but nectar is reward rather than a justified defence axis. *Pedicularis rex* supplies selective floral-associated defence without attraction manipulation. Santangelo et al. (2019) supplies a defence×herbivore-suppression×hand-pollination backbone, but defence is whole-plant HCN rather than strict floral \\(D\\)."
),
(
"The strongest conclusion from the reanalysis and coverage audit is narrower and more useful than the claim that attraction–defence biology is understudied. The retained route synthesis shows that the four constituent marginal pathways recur across 25 independent biological clusters, including same-system and context-switching architectures. The 17-system design audit then shows that sophisticated experimental faces of the target architecture also recur: Kessler et al. (2008) supplies an A×D-like trait face, Theis and Adler (2012) an A×G×pollination-supplementation bridge, Santangelo et al. (2019) a defence×consumer×pollination-supplementation bridge, and Egan et al. (2021) a consumer-factorial backbone. What remains missing is closure of these faces on the same biologically valid trait coordinates and outcome scale.",
"The route synthesis shows that constituent pathways recur across 25 independent biological clusters, while the 17-system audit shows that complementary experimental faces also recur: an A×D-like trait face (Kessler et al. 2008), A×G×pollination-supplementation (Theis and Adler 2012), defence×consumer×pollination-supplementation (Santangelo et al. 2019), and a consumer factorial (Egan et al. 2021). What remains missing is closure on the same valid trait coordinates and outcome scale."
),
(
"This distinction matters because adding more studies of marginal pathways will not solve the same problem. Evidence that attraction affects pollination, attraction affects antagonists, defence affects antagonists and defence affects pollinators demonstrates biological plausibility. It does not determine the cross-trait interaction in those channels. Likewise, observing a total \\(A\\times D\\) interaction does not determine how much of it came from each pathway. The missing information is structural.",
"More marginal-pathway studies establish plausibility but cannot determine cross-trait channel interactions, and a total \\(A\\times D\\) interaction cannot allocate them. The missing information is structural."
),
(
"The four constituent ecological pathway families recur across independent systems, while high-information studies already occupy complementary faces of the identification frontier. A direct A×D-like trait factorial, A×G×pollination-supplementation and defence×consumer×pollination-supplementation bridges, a consumer factorial, a selective floral defence manipulation and a linked public-data panel all exist, but in different systems. The empirical gap is therefore design fragmentation: the next experiment can reuse a strong existing backbone and add the missing module that most reduces its identified set.",
"Constituent pathways recur, and high-information studies already occupy complementary faces of the identification frontier, but in different systems. The empirical gap is therefore design fragmentation: reuse a strong existing backbone and add the missing module that most reduces its identified set."
),
]

for old,new in repls:
    if old not in text:
        raise RuntimeError('missing compaction target: ' + old[:90])
    text = text.replace(old,new,1)

required = [
    'Seventeen high-information systems are retained',
    '17 screened systems',
    'fragmented identification frontier',
    'Theis and Adler (2012)',
    'A\\times G\\times P_{\\mathrm{supp}}',
    'Santangelo et al. (2019)',
    '0/17',
    '56 directional route records',
    '25 independent biological study clusters',
    '\\mathcal I(\\delta)',
    '\\kappa_\\Delta\\ge0',
]
for token in required:
    if token not in text:
        raise RuntimeError('required scientific result lost: ' + token)

P.write_text(text,encoding='utf-8')
