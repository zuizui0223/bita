from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"
BG = ROOT / "docs" / "BACKGROUND_NOVELTY_GAP_REVIEW.md"
BP = ROOT / "docs" / "INTRODUCTION_BLUEPRINT.md"
WF = ROOT / ".github" / "workflows" / "_background-gap-patch-tmp.yml"
SELF = Path(__file__)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f"{label}: expected 1 match, found {n}")
    return text.replace(old, new, 1)

# Manuscript: sharpen prior-art boundary and mechanism-first logic.
text = MAN.read_text(encoding="utf-8")
old = '''### 1.2 Existing theories

Multivariate selection and fitness-landscape theory already provide general descriptions of cross-trait fitness curvature (Lande and Arnold 1983; Phillips and Arnold 1989; Blows and Brooks 2003). Ecological interaction studies likewise show that pollinators, herbivores, and other partners can modify one another's fitness effects, including non-additive consequences relevant to floral evolution (Herrera et al. 2002; Knauer et al. 2018).

Those frameworks establish that trait combinations and ecological partners need not act additively, but they do not by themselves allocate a total cross-trait curvature among ecological causes. The same observed interaction can arise because defence preserves attraction-generated value from antagonists, because defence interferes with pollinator returns, because the two traits share direct costs, or through some combination of these channels. Total fitness curvature therefore does not uniquely identify mechanism.

### 1.3 Ecological inference gap

We ask: **When does one attraction trait and one defence trait become locally complementary rather than substitutable?** Complementarity means that either trait strengthens the local marginal fitness effect of the other on declared trait and outcome coordinates; substitutability means that it weakens that effect. This is narrower than asking whether the traits covary, whether correlational selection exists, or where a fitness optimum lies.

The empirical literature creates the same identification problem. Many studies measure floral signals, chemical or physical defences, pollinator responses, florivory, or nectar larceny, but few manipulate the same attraction and defence axes together on a common outcome scale. A defensible synthesis must therefore distinguish constituent-path evidence, same-system linkage, and direct \\(A\\times D\\) evidence rather than pooling them as if they estimated one quantity.
'''
new = '''### 1.2 Existing theories

Multivariate selection and fitness-landscape theory already provide general descriptions of cross-trait fitness curvature (Lande and Arnold 1983; Phillips and Arnold 1989; Blows and Brooks 2003). Ecological interaction studies likewise show that pollinators, herbivores, and other partners can modify one another's fitness effects, including non-additive consequences relevant to floral evolution (Herrera et al. 2002; Knauer et al. 2018). Attractive floral signals can recruit antagonists as well as mutualists, and antagonist suppression can reverse the net consequences of organisms that also deter pollinators (Theis and Adler 2012; Knauer et al. 2018).

More recent eco-coevolutionary theory goes further by modelling pollination benefits, attraction, defence, and their costs jointly, asking when antagonistic interactions can evolve toward net mutualism and how community context shifts that outcome (Johnson et al. 2021). These studies establish that attraction-defence balance, non-additivity, trade-offs, and context-dependent evolutionary outcomes are not new ideas.

What remains less explicit is a narrower inference problem. Before predicting how attraction and defence coevolve, or where complementarity occurs, can any region of mechanism space be ruled out as incompatible with local attraction-defence complementarity? Existing frameworks describe net interaction outcomes, evolutionary transitions, or system-specific balances, but they do not by themselves isolate a one-sided exclusion rule for the focal \\(A\\times D\\) fitness curvature. Nor do they uniquely allocate an observed total cross-trait curvature among antagonist relief, pollinator interference, and direct joint cost.

### 1.3 Ecological inference gap

We therefore ask a deliberately narrower question: **before predicting where attraction-defence complementarity occurs, can we identify where it cannot occur?** For one focal attraction trait and one flower-specific antagonist-reducing trait, complementarity means that either trait strengthens the local marginal fitness effect of the other on declared trait and outcome coordinates; substitutability means that it weakens that effect. This is narrower than asking whether the traits covary, whether correlational selection exists, where a fitness optimum lies, or whether an interaction evolves from antagonism to mutualism.

The empirical literature creates a second identification problem. Many studies measure floral signals, chemical or physical defences, pollinator responses, florivory, or nectar larceny, but few manipulate the same attraction and defence axes together on a common outcome scale. A defensible synthesis must therefore distinguish constituent-path evidence, same-system linkage, and direct \\(A\\times D\\) evidence rather than pooling them as if they estimated one quantity. The contribution sought here is consequently not a new interaction type or a new mixed partial, but a mechanism-defined boundary on what the focal interaction can do and an evidence architecture for asking whether the mechanisms defining that boundary recur in nature.
'''
text = replace_once(text, old, new, "manuscript prior-art gap")

old = '''The logic is therefore **Mechanism \\(\\rightarrow\\) Pattern**, not theory \\(\\rightarrow\\) validation. The theoretical result states what is structurally permitted under declared premises; the empirical synthesis asks how often the required channels and switching architectures are independently realised and where direct identification remains missing.
'''
new = '''The logic is therefore **Mechanism \\(\\rightarrow\\) Pattern**, not theory \\(\\rightarrow\\) validation. Part I first defines the mechanism classes and derives the structural constraint; those theory-defined classes then determine what counts as relevant evidence in Part II. The empirical synthesis therefore does not search for a pattern and infer a mechanism afterward. It asks whether the already-defined constituent routes, same-system combinations, switching architectures, and identification gaps recur independently across biological systems, while keeping direct estimation of the full mixed partial separate.
'''
text = replace_once(text, old, new, "manuscript mechanism-pattern logic")

# Add close theoretical prior art to References if absent.
if "Johnson CA" not in text:
    lines = text.splitlines()
    ref = "Johnson CA, Smith GP, Yule K, Davidowitz G, Bronstein JL, Ferrière R (2021) Coevolutionary transitions from antagonism to mutualism explained by the Co-Opted Antagonist Hypothesis. *Nature Communications* 12:2867. https://doi.org/10.1038/s41467-021-23177-x"
    insert_at = None
    for i, line in enumerate(lines):
        if line.startswith("Knauer AC"):
            insert_at = i
            break
    if insert_at is None:
        raise RuntimeError("could not locate alphabetical reference insertion point")
    lines.insert(insert_at, ref)
    lines.insert(insert_at + 1, "")
    text = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
MAN.write_text(text, encoding="utf-8")

# Background/novelty review: make the impossibility-boundary gap explicit.
text = BG.read_text(encoding="utf-8")
old = '''The defensible contribution is narrower:

> a focal-pair local diagnostic framework that separates antagonist relief, mutualist interference, and direct joint-cost curvature; states that the mechanism decomposition is not identified by total fitness alone; requires an explicit orientation gate before assigning non-negative mechanism labels; derives the full environmental derivative balance; and enforces strict boundaries between route existence, channel curvature, the complete mixed partial, trait covariance, and evolutionary endpoints.

A targeted review did not identify an earlier paper combining all of those elements for one floral attraction × flower-specific defence/barrier pair. This is a provisional positioning statement, not a claim of exhaustive priority.
'''
new = '''The defensible contribution is narrower:

> a focal-pair local diagnostic framework that separates antagonist relief, mutualist interference, and direct joint-cost curvature; states that the mechanism decomposition is not identified by total fitness alone; derives a one-sided impossibility boundary under non-negative joint-cost curvature; and then uses those theory-defined mechanism classes to structure a Mechanism → Pattern synthesis rather than inferring mechanism from an observed aggregate Pattern.

The targeted review confirms that the component ideas are established: cross-trait curvature, pollinator-herbivore non-additivity, attraction of antagonists, pollination costs, context-dependent net effects, and eco-coevolutionary attraction-defence models all predate this manuscript. What was not identified in that review is an earlier focal attraction × defence treatment that isolates the specific one-sided implication `W_AD > 0 => rho > iota` under non-negative joint-cost curvature and uses that exclusion rule to define a falsifiable empirical applicability gate. This is a provisional positioning statement, not a claim of exhaustive priority or mathematical sophistication.
'''
text = replace_once(text, old, new, "background bottom line")

anchor = '''### 5. Mutualism–antagonism balance can switch across ecological regimes

Population-dynamic models have shown transitions between mutualistic and antagonistic outcomes when one interaction partner supplies benefits at one life stage and costs at another. Such work establishes that context-dependent sign changes are a broader ecological idea; the current manuscript should not claim novelty for regime transitions themselves.

Example: Revilla TA, Encinas-Viso F. 2014. Dynamical transitions in a pollination–herbivory interaction. arXiv:1404.4804.
'''
addition = anchor + '''
### 6. Attraction, defence, benefits, and costs have already been modelled eco-coevolutionarily

Johnson et al. (2021) explicitly model coevolution of pollination benefits, attraction, and defence in plant–insect interactions that can transition from antagonism to mutualism. Their framework also varies trait costs and community context. The current manuscript therefore must not claim novelty for jointly modelling attraction and defence, for identifying cost-sensitive outcomes, or for deriving ecological transition boundaries in general.

Reference: Johnson CA, Smith GP, Yule K, Davidowitz G, Bronstein JL, Ferrière R. 2021. Coevolutionary transitions from antagonism to mutualism explained by the Co-Opted Antagonist Hypothesis. *Nature Communications* 12:2867. DOI: 10.1038/s41467-021-23177-x.
'''
text = replace_once(text, anchor, addition, "background Johnson prior art")

old = '''Four inferential gaps remain.

### Gap 1: net effects do not identify mechanisms
'''
new = '''Five inferential gaps remain.

### Gap 0: existing balance models do not by themselves provide the focal one-sided impossibility boundary

Prior work asks how non-additive fitness effects arise, how ecological context changes net outcomes, or how attraction, defence, and pollination benefits coevolve. The narrower unresolved question is whether the local focal-pair mechanism implies a region in which attraction-defence complementarity is impossible before any attempt is made to predict where complementarity occurs. The present theorem addresses that question by treating the selectivity window as a necessary permissive region rather than a sufficient sign rule.

### Gap 1: net effects do not identify mechanisms
'''
text = replace_once(text, old, new, "background gap zero")
BG.write_text(text, encoding="utf-8")

# Introduction blueprint: encode the new narrative explicitly.
text = BP.read_text(encoding="utf-8")
old = '''## Paragraph 2 — Established evidence

Introduce four foundations:

1. multivariate selection can favour combinations of traits rather than isolated traits;
2. pollinators and herbivores can interact non-additively in their effects on plant fitness;
3. attractive floral signals can recruit antagonists as well as pollinators;
4. antagonist suppression can alter the net fitness consequences of floral signals and pollinator deterrence.

Anchor examples:

- Lande & Arnold 1983 — multivariate selection;
- Herrera et al. 2002 — non-additive pollinator × herbivore fitness effects;
- Theis & Adler 2012 — floral fragrance recruits florivores and reduces reproduction;
- Knauer et al. 2018 — florivore removal changes the net role of crab spiders in floral-signal evolution.

**Function:** show that the component biological routes are real and already recognized.

## Paragraph 3 — Inferential gap

Existing work commonly estimates net selection, the effect of one interacting guild, or a system-specific outcome. Such evidence does not automatically identify how a flower-specific defence/barrier changes the marginal fitness return to one focal attraction trait. A total interaction term also does not uniquely identify whether the source is antagonist relief, mutualist interference, or direct joint cost.

**Function:** move from known biology to the specific unresolved inference problem.
'''
new = '''## Paragraph 2 — Established evidence and close theoretical prior art

Introduce five foundations:

1. multivariate selection can favour combinations of traits rather than isolated traits;
2. pollinators and herbivores can interact non-additively in their effects on plant fitness;
3. attractive floral signals can recruit antagonists as well as pollinators;
4. antagonist suppression can alter the net fitness consequences of floral signals and pollinator deterrence;
5. eco-coevolutionary models already combine attraction, defence, pollination benefits, costs, and community context to study transitions between antagonism and mutualism.

Anchor examples:

- Lande & Arnold 1983 — multivariate selection;
- Herrera et al. 2002 — non-additive pollinator × herbivore fitness effects;
- Theis & Adler 2012 — floral fragrance recruits florivores and reduces reproduction;
- Knauer et al. 2018 — florivore removal changes the net role of crab spiders in floral-signal evolution;
- Johnson et al. 2021 — eco-coevolution of attraction, defence, pollination benefits, and costs.

**Function:** show that the biological ingredients and even close attraction-defence evolutionary models are established, so novelty must be narrower.

## Paragraph 3 — The one-sided inference gap

State the deliberately narrower question: **before predicting where complementarity occurs, can we identify where it cannot occur?** Existing work commonly estimates net selection, system-specific balances, ecological transition regions, or evolutionary outcomes. Such work does not by itself isolate a one-sided exclusion rule for the focal `A × D` curvature. A total interaction term also does not uniquely identify whether the source is antagonist relief, mutualist interference, or direct joint cost.

**Function:** move from known biology to the specific unresolved impossibility-boundary problem.
'''
text = replace_once(text, old, new, "blueprint prior art and gap")

old = '''## Paragraph 5 — Present contribution

State that the paper develops a focal-pair local diagnostic framework for one declared attraction trait `A`, one declared defence/barrier trait `D`, and one declared outcome scale `W`. The framework:

- separates signed bookkeeping from biological identification;
- requires an orientation gate before assigning non-negative mechanism labels;
- decomposes the local balance into antagonist relief, mutualist interference, and direct joint-cost curvature;
- derives the unrestricted environmental derivative balance before restricted special cases;
- enforces boundaries between route existence, channel curvature, total mixed partial, trait covariance, and evolutionary dynamics.

**Function:** present the actual novelty without claiming a new mixed partial or a first demonstration of mutualist–antagonist interactions.
'''
new = '''## Paragraph 5 — Present contribution and Mechanism → Pattern logic

State that the paper develops a focal-pair local diagnostic framework for one declared attraction trait `A`, one declared defence/barrier trait `D`, and one declared outcome scale `W`. The framework:

- separates signed bookkeeping from biological identification;
- requires an orientation gate before assigning non-negative mechanism labels;
- decomposes the local balance into antagonist relief, mutualist interference, and direct joint-cost curvature;
- derives the one-sided selectivity bound as a necessary permissive region, not a sufficient sign criterion;
- derives the unrestricted environmental derivative balance before restricted special cases;
- uses Part I to define the mechanism classes that Part II then searches for across independent systems;
- enforces boundaries between route existence, channel curvature, total mixed partial, trait covariance, and evolutionary dynamics.

**Function:** present the actual novelty as a simple mechanistic exclusion rule plus mechanism-first evidence architecture, without claiming a new mixed partial, a new attraction-defence model class, or a first demonstration of mutualist–antagonist interactions.
'''
text = replace_once(text, old, new, "blueprint contribution")
BP.write_text(text, encoding="utf-8")

if WF.exists():
    WF.unlink()
if SELF.exists():
    SELF.unlink()
