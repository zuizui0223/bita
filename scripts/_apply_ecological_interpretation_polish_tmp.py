from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"
REFTEST = ROOT / "tests" / "test_manuscript_references.py"
NEWTEST = ROOT / "tests" / "test_ecological_interpretation_and_simplicity.py"
BACKGROUND = ROOT / "docs" / "BACKGROUND_NOVELTY_GAP_REVIEW.md"
FIT = ROOT / "submission" / "ECOLOGY_CONCEPTS_SYNTHESIS_FIT_AUDIT.md"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f"{label}: expected 1 target, found {n}")
    return text.replace(old, new, 1)


text = MAN.read_text(encoding="utf-8")

text = replace_once(
    text,
    "The decomposition is bookkeeping, but it yields a one-sided bound: when joint-cost curvature is non-negative, complementarity can occur only where antagonist relief exceeds pollinator interference.",
    "The algebra is deliberately elementary: the decomposition is bookkeeping, and its ecological payoff is a one-sided bound—when joint-cost curvature is non-negative, complementarity can occur only where antagonist relief exceeds pollinator interference.",
    "abstract simplicity",
)

text = replace_once(
    text,
    "A recurring problem in ecology is that net interaction outcomes can conceal opposing causal channels. The same trait can improve performance through one interaction partner while reducing it through another, so context-dependent net signs do not by themselves reveal a general mechanism. Flowers provide a tractable case because they interact simultaneously with organisms that increase reproduction and organisms that diminish it.",
    "A recurring problem in ecology is that net interaction outcomes can conceal opposing causal channels. The same trait can improve performance through one interaction partner while reducing it through another, so context-dependent net signs do not by themselves reveal a general mechanism. More generally, context dependence can reflect genuine interaction effects rather than noise, and naming a relationship as context dependent without resolving its causes provides limited explanatory or predictive leverage (Catford et al. 2022). Flowers provide a tractable case because they interact simultaneously with organisms that increase reproduction and organisms that diminish it.",
    "intro general context dependence",
)

old_existing = """Multivariate selection and fitness-landscape theory already provide general descriptions of cross-trait fitness curvature (Lande and Arnold 1983; Phillips and Arnold 1989; Blows and Brooks 2003). Ecological interaction studies likewise show that pollinators, herbivores, and other partners can modify one another's fitness effects, including non-additive consequences relevant to floral evolution (Herrera et al. 2002; Knauer et al. 2018). Attractive floral signals can recruit antagonists as well as mutualists, and antagonist suppression can reverse the net consequences of organisms that also deter pollinators (Theis and Adler 2012; Knauer et al. 2018).

More recent eco-coevolutionary theory goes further by modelling pollination benefits, attraction, defence, and their costs jointly, asking when antagonistic interactions can evolve toward net mutualism and how community context shifts that outcome (Johnson et al. 2021). These studies establish that attraction-defence balance, non-additivity, trade-offs, and context-dependent evolutionary outcomes are not new ideas.

What remains less explicit is a narrower inference problem. Before predicting how attraction and defence coevolve, or where complementarity occurs, can any region of mechanism space be ruled out as incompatible with local attraction-defence complementarity? Existing frameworks describe net interaction outcomes, evolutionary transitions, or system-specific balances, but they do not by themselves isolate a one-sided exclusion rule for the focal \(A\times D\) fitness curvature. Nor do they uniquely allocate an observed total cross-trait curvature among antagonist relief, pollinator interference, and direct joint cost."""

new_existing = """Multivariate selection and fitness-landscape theory already provide general descriptions of cross-trait fitness curvature (Lande and Arnold 1983; Phillips and Arnold 1989; Blows and Brooks 2003). Ecological interaction studies likewise show that pollinators, herbivores, and other partners can modify one another's fitness effects, including non-additive consequences relevant to floral evolution (Herrera et al. 2002; Knauer et al. 2018). Attractive floral signals can recruit antagonists as well as mutualists, and antagonist suppression can reverse the net consequences of organisms that also deter pollinators (Theis and Adler 2012; Knauer et al. 2018).

The attraction-defence problem itself also has a substantial conceptual lineage. Non-pollinator agents can impose direct or indirect selection on floral traits, including conflict when antagonists and pollinators share trait preferences (Strauss and Whittall 2006), and attraction and resistance have explicitly been considered as linked targets of pollinator- and herbivore-mediated selection (Adler 2008). Chemical frameworks have proposed that tissue specificity, inducibility, resource allocation, and pleiotropy can create or relax conflicts between defence and pollinator attraction (Kessler and Halitschke 2009). Broader reviews likewise emphasize evolutionary interdependence between reproduction and defence and the need to integrate herbivore-induced responses, pollination, resource allocation, and plant fitness within the same systems (Johnson et al. 2015; Lucas-Barbosa 2016). Empirical work further shows that these effects can depend on herbivore identity, feeding mode, visitor identity, and plant state (Rusman et al. 2018), while pollinator-mediated selection itself is well known to vary with antagonists, resources, community context, populations, and years (Sletvold 2019).

More recent eco-coevolutionary theory goes further by modelling pollination benefits, attraction, defence, and their costs jointly, asking when antagonistic interactions can evolve toward net mutualism and how community context shifts that outcome (Johnson et al. 2021). These studies establish that attraction-defence balance, non-additivity, trade-offs, ecological costs, and context-dependent evolutionary outcomes are not new ideas.

What remains less explicit is a narrower inference problem. Before predicting how attraction and defence coevolve, or where complementarity occurs, can any region of mechanism space be ruled out as incompatible with local attraction-defence complementarity? The close literature provides rich mechanisms and conditional predictions, but it does not by itself supply the focal one-sided exclusion used here for the local \(A\times D\) fitness curvature under an explicit joint-cost sign premise. Nor does it uniquely allocate an observed total cross-trait curvature among antagonist relief, pollinator interference, and direct joint cost. This is a positioning claim about the inferential form of the present synthesis, not a priority claim that attraction-defence coupling or context dependence was previously unrecognized."""
text = replace_once(text, old_existing, new_existing, "existing theories expansion")

text = replace_once(
    text,
    "The empirical literature creates a second identification problem. Many studies measure floral signals, chemical or physical defences, pollinator responses, florivory, or nectar larceny, but few manipulate the same attraction and defence axes together on a common outcome scale.",
    "The mathematical step needed for this narrower question is intentionally simple rather than technically elaborate. Once biologically distinct channels are declared, the aim is to extract the weakest sign condition that rules out complementarity, not to replace existing evolutionary or community models with a more complicated dynamical system. The empirical literature then creates a second identification problem. Many studies measure floral signals, chemical or physical defences, pollinator responses, florivory, or nectar larceny, but few manipulate the same attraction and defence axes together on a common outcome scale.",
    "intro simplicity statement",
)

text = replace_once(
    text,
    "This ordering is also the paper's broader contribution to ecological synthesis. When heterogeneous studies cannot estimate one common focal interaction, theory can first define exclusion conditions and evidence classes, after which synthesis can ask which components recur without promoting them to the full interaction.",
    "This ordering is also the paper's broader contribution to ecological synthesis. It answers a general concern raised by work on mechanistic context dependence: interaction effects need theory that specifies what varies and why, rather than a post hoc label for heterogeneous outcomes (Catford et al. 2022). When heterogeneous studies cannot estimate one common focal interaction, theory can first define exclusion conditions and evidence classes, after which synthesis can ask which components recur without promoting them to the full interaction.",
    "mechanism pattern context literature",
)

proof_old = """The proof is immediate from \(W_{AD}=\rho-\iota-\kappa\): if \(W_{AD}>0\) and \(\kappa\ge0\), then \(\rho-\iota=W_{AD}+\kappa>0\). The proof uses only the additive relief-minus-interference-minus-cost structure and \(\kappa\ge0\), preserved by all four declared endpoint-normalized response-shape variants. The signs of \(\rho\) and \(\iota\) are not used by this implication; their non-negativity belongs to the oriented baseline interpretation rather than to Theorem 1 itself. When \(\kappa=0\), the implication runs both ways and the window becomes the exact sign criterion.

The converse is not generally true when \(\kappa>0\)."""
proof_new = """The proof is immediate from \(W_{AD}=\rho-\iota-\kappa\): if \(W_{AD}>0\) and \(\kappa\ge0\), then \(\rho-\iota=W_{AD}+\kappa>0\). The proof uses only the additive relief-minus-interference-minus-cost structure and \(\kappa\ge0\), preserved by all four declared endpoint-normalized response-shape variants. The signs of \(\rho\) and \(\iota\) are not used by this implication; their non-negativity belongs to the oriented baseline interpretation rather than to Theorem 1 itself. When \(\kappa=0\), the implication runs both ways and the window becomes the exact sign criterion.

The algebra is therefore one line. Its ecological meaning is also simple: if simultaneous attraction-defence investment does not have negative joint-cost curvature, a flower cannot be locally attraction-defence complementary unless antagonist relief exceeds pollinator interference. Crossing that relief-versus-interference threshold only makes complementarity possible; it does not make it inevitable, because a positive joint-cost term can still reverse the sign.

The converse is not generally true when \(\kappa>0\)."""
text = replace_once(text, proof_old, proof_new, "plain language theorem")

text = replace_once(
    text,
    "### 6.1 What generalizes is a one-sided window, not a sign rule\n\nPart I gives the recurrent route-separation Pattern a precise role.",
    "### 6.1 A simple bound on a complex ecological balance\n\nThe central mathematical result is simpler than the surrounding ecological notation may suggest: it is a one-line exclusion, not a high-dimensional prediction of nature. Part I gives the recurrent route-separation Pattern a precise role.",
    "discussion simple heading",
)

text = replace_once(
    text,
    "Biologically, the selectivity window is best read as a discrimination condition rather than as a label attached to a defence trait. Guarded defence, consumer-specific barriers, attack-mode filtering, and visitor routing can generate empirical states consistent with large antagonist relief relative to pollinator interference. These studies do not directly estimate \(\rho-\iota\), however, so their role is to show that the required route separation is biologically realizable, not to classify individual systems as inside the window.",
    "Biologically, the selectivity window is best read as a functional-discrimination condition rather than as a label attached to a defence trait. Earlier work already proposed tissue specificity and inducibility as ways to reduce conflict between defence and pollinator attraction (Kessler and Halitschke 2009), and later integrative and empirical studies show that herbivore-plant-pollinator effects can depend on the identity and mode of the interacting consumers (Lucas-Barbosa 2016; Rusman et al. 2018). In the present synthesis, guarded defence, consumer-specific barriers, attack-mode filtering, and visitor routing are therefore interpreted as empirical states consistent with increasing antagonist relief relative to pollinator interference. These studies do not directly estimate \(\rho-\iota\), however, so their role is to show that the required route separation is biologically realizable, not to classify individual systems as mathematically inside the window.",
    "discussion selectivity interpretation",
)

text = replace_once(
    text,
    "Shared construction, allocation, or physiological constraints are plausible biological sources of joint-cost curvature, but the strict audit recovered marginal attraction costs, marginal defence costs, trait integration or covariance, and inferred resource reallocation rather than a direct estimate of the additional cost of simultaneous investment in distinct \(A\) and \(D\) axes. These observations therefore motivate hypotheses about \(\kappa\); they do not identify it.",
    "Shared construction, allocation, biochemical, developmental, or physiological constraints are plausible biological sources of joint-cost curvature. Allocation costs, pleiotropy, and defence-reproduction coupling have long been discussed as mechanisms connecting attraction and defence (Kessler and Halitschke 2009; Johnson et al. 2015; Lucas-Barbosa 2016), but those literatures should not be equated with the specific cross-curvature \(\kappa\). The strict audit recovered marginal attraction costs, marginal defence costs, trait integration or covariance, and inferred resource reallocation rather than a direct estimate of the additional cost of simultaneous investment in distinct \(A\) and \(D\) axes. These observations therefore motivate hypotheses about \(\kappa\); they do not identify it.",
    "discussion kappa literature",
)

text = replace_once(
    text,
    "Ecologically, context is therefore better treated as a coupled state of consumer identity, attack mode, reward or resource conditions, exposure, and response stage than as a single named pressure variable. The recurrent sign/state switches in Part II are not noise around one universal effect; they are evidence that the balance among causal channels itself changes among ecological states.",
    "Ecologically, context is therefore better treated as a coupled state of consumer identity, attack mode, reward or resource conditions, exposure, and response stage than as a single named pressure variable. This distinction parallels the broader separation between mechanistic context dependence caused by interaction effects and apparent context dependence generated by confounding, inference, or methodological differences (Catford et al. 2022). The source-adjudication and evidence hierarchy used here are important precisely because both possibilities can coexist across a heterogeneous literature. The recurrent within-system sign/state switches are not treated as noise around one universal effect; where source design supports them, they indicate that the balance among causal channels itself changes among ecological states. This interpretation is consistent with long-standing evidence that pollinator-mediated selection varies with antagonists, resources, community context, populations, and years (Sletvold 2019).",
    "discussion context interpretation",
)

text = replace_once(
    text,
    "Nothing in the inferential sequence requires flowers, although the biological decomposition developed here does.",
    "Nothing in the inferential sequence requires flowers, although the biological decomposition developed here does. In this sense the manuscript follows the broader recommendation that mechanistic context dependence should be organized by explicit interaction theory to improve explanation and transferability (Catford et al. 2022), while remaining deliberately conservative about transporting any particular sign rule.",
    "discussion transfer literature",
)

# Bibliography insertions, preserving alphabetical first-author order.
insertions = [
    (
        "## References\n\nBlows MW, Brooks R (2003)",
        "## References\n\nAdler LS (2008) Selection by pollinators and herbivores on attraction and defense. In: Tilmon KJ (ed) *Specialization, Speciation, and Radiation: The Evolutionary Biology of Herbivorous Insects*, pp 162–173. University of California Press. https://doi.org/10.1525/california/9780520251328.003.0012\n\nBlows MW, Brooks R (2003)",
        "Adler reference",
    ),
    (
        "Caruso CM, Eisen KE, Martin RA, Sletvold N (2019) A meta-analysis of the agents of selection on floral traits. *Evolution* 73:4–14. https://doi.org/10.1111/evo.13639\n\nHaas-Desmarais",
        "Caruso CM, Eisen KE, Martin RA, Sletvold N (2019) A meta-analysis of the agents of selection on floral traits. *Evolution* 73:4–14. https://doi.org/10.1111/evo.13639\n\nCatford JA, Wilson JRU, Pyšek P, Hulme PE, Duncan RP (2022) Addressing context dependence in ecology. *Trends in Ecology & Evolution* 37:158–170. https://doi.org/10.1016/j.tree.2021.09.007\n\nHaas-Desmarais",
        "Catford reference",
    ),
    (
        "Johnson CA, Smith GP, Yule K, Davidowitz G, Bronstein JL, Ferrière R (2021) Coevolutionary transitions from antagonism to mutualism explained by the Co-Opted Antagonist Hypothesis. *Nature Communications* 12:2867. https://doi.org/10.1038/s41467-021-23177-x\n\nJunker",
        "Johnson CA, Smith GP, Yule K, Davidowitz G, Bronstein JL, Ferrière R (2021) Coevolutionary transitions from antagonism to mutualism explained by the Co-Opted Antagonist Hypothesis. *Nature Communications* 12:2867. https://doi.org/10.1038/s41467-021-23177-x\n\nJohnson MTJ, Campbell SA, Barrett SCH (2015) Evolutionary interactions between plant reproduction and defense against herbivores. *Annual Review of Ecology, Evolution, and Systematics* 46:191–213. https://doi.org/10.1146/annurev-ecolsys-112414-054215\n\nJunker",
        "Johnson 2015 reference",
    ),
    (
        "Junker RR, Blüthgen N (2010) Floral scents repel facultative flower visitors, but attract obligate ones. *Annals of Botany* 105:777–782. https://doi.org/10.1093/aob/mcq045\n\nKnauer",
        "Junker RR, Blüthgen N (2010) Floral scents repel facultative flower visitors, but attract obligate ones. *Annals of Botany* 105:777–782. https://doi.org/10.1093/aob/mcq045\n\nKessler A, Halitschke R (2009) Testing the potential for conflicting selection on floral chemical traits by pollinators and herbivores: predictions and case study. *Functional Ecology* 23:901–912. https://doi.org/10.1111/j.1365-2435.2009.01639.x\n\nKnauer",
        "Kessler reference",
    ),
    (
        "Leal LC et al. (2025) Costs of floral larceny: a meta-analytical evaluation of nectar robbing and nectar theft on animal-pollinated plants. *Ecology* 106:e70036. https://doi.org/10.1002/ecy.70036\n\nPage",
        "Leal LC et al. (2025) Costs of floral larceny: a meta-analytical evaluation of nectar robbing and nectar theft on animal-pollinated plants. *Ecology* 106:e70036. https://doi.org/10.1002/ecy.70036\n\nLucas-Barbosa D (2016) Integrating studies on plant-pollinator and plant-herbivore interactions. *Trends in Plant Science* 21:125–133. https://doi.org/10.1016/j.tplants.2015.10.013\n\nPage",
        "Lucas-Barbosa reference",
    ),
    (
        "Richardson LL et al. (2015) Secondary metabolites in floral nectar reduce parasite infections in bumblebees. *Proceedings of the Royal Society B* 282:20142471. https://doi.org/10.1098/rspb.2014.2471\n\nSasidharan",
        "Richardson LL et al. (2015) Secondary metabolites in floral nectar reduce parasite infections in bumblebees. *Proceedings of the Royal Society B* 282:20142471. https://doi.org/10.1098/rspb.2014.2471\n\nRusman Q, Lucas-Barbosa D, Poelman EH (2018) Dealing with mutualists and antagonists: specificity of plant-mediated interactions between herbivores and flower visitors, and consequences for plant fitness. *Functional Ecology* 32:1022–1035. https://doi.org/10.1111/1365-2435.13035\n\nSasidharan",
        "Rusman reference",
    ),
    (
        "Sasidharan R, Junker RR, Eilers EJ, Müller C (2023) Floral volatiles evoke partially similar responses in both florivores and pollinators and are correlated with non-volatile reward chemicals. *Annals of Botany* 132:1–14. https://doi.org/10.1093/aob/mcad064\n\nSoper",
        "Sasidharan R, Junker RR, Eilers EJ, Müller C (2023) Floral volatiles evoke partially similar responses in both florivores and pollinators and are correlated with non-volatile reward chemicals. *Annals of Botany* 132:1–14. https://doi.org/10.1093/aob/mcad064\n\nSletvold N (2019) The context dependence of pollinator-mediated selection in natural populations. *International Journal of Plant Sciences* 180:934–943. https://doi.org/10.1086/705584\n\nSoper",
        "Sletvold reference",
    ),
    (
        "Strauss SY, Siemens DH, Decher MB, Mitchell-Olds T (1999) Ecological costs of plant resistance to herbivores in the currency of pollination. *Evolution* 53:1105–1113. https://doi.org/10.1111/j.1558-5646.1999.tb04525.x\n\nSun",
        "Strauss SY, Siemens DH, Decher MB, Mitchell-Olds T (1999) Ecological costs of plant resistance to herbivores in the currency of pollination. *Evolution* 53:1105–1113. https://doi.org/10.1111/j.1558-5646.1999.tb04525.x\n\nStrauss SY, Whittall JB (2006) Non-pollinator agents of selection on floral traits. In: Harder LD, Barrett SCH (eds) *Ecology and Evolution of Flowers*, pp 120–138. Oxford University Press. https://doi.org/10.1093/oso/9780198570851.003.0007\n\nSun",
        "Strauss Whittall reference",
    ),
]
for old, new, label in insertions:
    text = replace_once(text, old, new, label)

MAN.write_text(text, encoding="utf-8")

# Update citation spine regression.
r = REFTEST.read_text(encoding="utf-8")
r = r.replace(
    '        "10.1038/s41467-021-23177-x",\n',
    '        "10.1038/s41467-021-23177-x",\n'
    '        "10.1016/j.tree.2021.09.007",\n'
    '        "10.1525/california/9780520251328.003.0012",\n'
    '        "10.1146/annurev-ecolsys-112414-054215",\n'
    '        "10.1111/j.1365-2435.2009.01639.x",\n'
    '        "10.1016/j.tplants.2015.10.013",\n'
    '        "10.1111/1365-2435.13035",\n'
    '        "10.1086/705584",\n'
    '        "10.1093/oso/9780198570851.003.0007",\n'
)
r = r.replace(
    '        "Johnson et al. 2021": "Johnson CA, Smith GP, Yule K, Davidowitz G, Bronstein JL, Ferrière R (2021)",\n',
    '        "Johnson et al. 2021": "Johnson CA, Smith GP, Yule K, Davidowitz G, Bronstein JL, Ferrière R (2021)",\n'
    '        "Johnson et al. 2015": "Johnson MTJ, Campbell SA, Barrett SCH (2015)",\n'
    '        "Catford et al. 2022": "Catford JA, Wilson JRU, Pyšek P, Hulme PE, Duncan RP (2022)",\n'
    '        "Strauss and Whittall 2006": "Strauss SY, Whittall JB (2006)",\n'
    '        "Adler 2008": "Adler LS (2008)",\n'
    '        "Kessler and Halitschke 2009": "Kessler A, Halitschke R (2009)",\n'
    '        "Lucas-Barbosa 2016": "Lucas-Barbosa D (2016)",\n'
    '        "Rusman et al. 2018": "Rusman Q, Lucas-Barbosa D, Poelman EH (2018)",\n'
    '        "Sletvold 2019": "Sletvold N (2019)",\n'
)
r = r.replace("assert len(entries) == 21", "assert len(entries) == 29")
REFTEST.write_text(r, encoding="utf-8")

NEWTEST.write_text(r'''from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"
AUDIT = ROOT / "docs" / "LITERATURE_POSITIONING_AUDIT_2026-08-21.md"


def test_elementary_math_is_explicit_at_reader_checkpoints() -> None:
    text = MAN.read_text(encoding="utf-8")
    abstract = text.split("## Abstract", 1)[1].split("**Keywords:**", 1)[0]
    theorem = text.split("**Theorem 1 (one-sided selectivity bound).**", 1)[1].split("## 3.", 1)[0]
    discussion = text.split("### 6.1 A simple bound on a complex ecological balance", 1)[1].split("### 6.2", 1)[0]
    assert "algebra is deliberately elementary" in abstract.lower()
    assert "The algebra is therefore one line" in theorem
    assert "one-line exclusion" in discussion
    assert "positive joint-cost term can still reverse the sign" in theorem


def test_ecological_interpretation_keeps_evidence_boundary() -> None:
    text = MAN.read_text(encoding="utf-8")
    assert "functional-discrimination condition" in text
    assert "do not directly estimate \\(\\rho-\\iota\\)" in text
    assert "not to classify individual systems as mathematically inside the window" in text
    assert "motivate hypotheses about \\(\\kappa\\); they do not identify it" in text


def test_context_dependence_is_mechanistic_not_blanket_heterogeneity() -> None:
    text = MAN.read_text(encoding="utf-8")
    assert "mechanistic context dependence" in text
    assert "apparent context dependence" in text
    assert "source-adjudication and evidence hierarchy" in text
    assert "Catford et al. 2022" in text


def test_close_prior_art_is_acknowledged_without_priority_claim() -> None:
    text = MAN.read_text(encoding="utf-8")
    intro = text.split("### 1.2 Existing theories", 1)[1].split("### 1.3", 1)[0]
    for token in (
        "Strauss and Whittall 2006",
        "Adler 2008",
        "Kessler and Halitschke 2009",
        "Johnson et al. 2015",
        "Lucas-Barbosa 2016",
        "Rusman et al. 2018",
        "Sletvold 2019",
    ):
        assert token in intro
    assert "not a priority claim" in intro


def test_targeted_literature_audit_documents_scope() -> None:
    audit = AUDIT.read_text(encoding="utf-8")
    assert "not a reopening of broad Pattern evidence discovery" in audit
    assert "The algebraic answer is elementary" in audit
    assert "Hypothesis-generating only" in audit
''', encoding="utf-8")

# Sync positioning docs without turning them into another evidence registry.
bg = BACKGROUND.read_text(encoding="utf-8")
if "## 2026-08-21 close-prior-art refresh" not in bg:
    bg += """\n\n## 2026-08-21 close-prior-art refresh\n\nA targeted positioning audit added the closest attraction-defence and context-dependence lineage: Strauss & Whittall (2006), Adler (2008), Kessler & Halitschke (2009), Johnson et al. (2015), Lucas-Barbosa (2016), Rusman et al. (2018), Sletvold (2019), and Catford et al. (2022). These sources strengthen the prior-art boundary rather than the novelty claim. The manuscript now states explicitly that the algebra is elementary and that the contribution is the ecological one-sided exclusion, failed converse, and falsification gate. Broad Pattern evidence search remains closed.\n"""
    BACKGROUND.write_text(bg, encoding="utf-8")

fit = FIT.read_text(encoding="utf-8")
if "Literature-positioning refresh" not in fit:
    fit += """\n\n## Literature-positioning refresh — 2026-08-21\n\nPASS. Close prior work on attraction/defence conflict, defence-reproduction coupling, multi-agent selection, and ecological context dependence is now explicit in the Introduction and Discussion. The manuscript does not claim that those topics are new. It explicitly communicates that the theorem's algebra is elementary and positions the conceptual advance as a mechanism-defined exclusion plus an ordered falsification/calibration programme.\n"""
    FIT.write_text(fit, encoding="utf-8")
