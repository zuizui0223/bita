# When are floral attraction and defence complementary? A one-sided mechanistic bound and cross-system patterns

**Authors and affiliations:** [Author-controlled; insert final publication names and affiliations before submission.]

**Corresponding author:** [Author-controlled; insert name and active e-mail address.]

**ORCID(s):** [Insert available 16-digit ORCID identifiers after author approval.]

**Open Research statement:** Analysis code, source-adjudication products, and generated readouts are maintained in the public project repository. The exact immutable release, repository licence, and archival DOI for the submitted version are author-controlled release fields and will be inserted before submission.

## Abstract

A recurring challenge in ecology is to extract general structure from interactions whose net effects vary among contexts. Flowers provide a tractable case because attraction can recruit mutualists and antagonists, while defence can reduce antagonist damage yet interfere with pollination or impose joint costs. We ask first not where attraction and defence are complementary, but where complementarity is impossible. After an explicit orientation gate, the local mixed fitness effect is organized as antagonist relief minus pollinator interference minus direct joint-cost curvature, \(W_{AD}=\rho-\iota-\kappa\). The algebra is deliberately elementary: bookkeeping yields a one-sided bound—under non-negative joint-cost curvature, complementarity requires antagonist relief to exceed pollinator interference. We prove this algebraically and use 2,592 evaluations across four response-shape variants to verify implementation and quantify looseness: about 23% of points inside this selectivity window remain substitutable. Theory then defines the evidence classes for a mechanism-first synthesis of 56 route-level records from 25 independent biological study clusters. Floral larceny reduces female fitness on average (log response ratio -0.210; 48 clusters), yet only 35/48 effects are negative, the 95% prediction interval spans -1.13 to +0.71, and declared moderators explain only 0-8% of heterogeneity. Constituent mechanisms and switching architectures therefore recur, but their realized balance is strongly context dependent. Direct \(A\times D\) evidence remains sparse and direct joint-cost curvature unmeasured. The study shows how mechanism-first synthesis can replace a search for universal mean effects with testable boundaries on what ecological interactions can do.

**Keywords:** attraction-defence interaction; floral defence; florivory; mechanism; meta-analysis; pollination

## 1. Introduction

### 1.1 Ecological problem

A recurring problem in ecology is that net interaction outcomes can conceal opposing causal channels. The same trait can improve performance through one interaction partner while reducing it through another, so context-dependent net signs do not by themselves reveal a general mechanism. More generally, context dependence can reflect genuine interaction effects rather than noise, and naming a relationship as context dependent without resolving its causes provides limited explanatory or predictive leverage (Catford et al. 2022). Flowers provide a tractable case because they interact simultaneously with organisms that increase reproduction and organisms that diminish it. Signals, rewards, and floral structures recruit pollinators, but the same flowers are exposed to florivores, nectar robbers, pathogens, and other exploiters. A trait that changes attraction or access can therefore alter several ecological pathways at once.

This creates two plausible but opposing expectations. Greater attraction can increase the reproductive value that defence protects, favouring complementarity. Yet defence can also obstruct legitimate visitors or add joint construction costs, making the same trait combination substitutable. The central problem is therefore not whether attraction and defence are universally synergistic or universally traded off, but **what determines the local sign of their interaction**.

### 1.2 Existing theories

Multivariate selection and fitness-landscape theory already provide general descriptions of cross-trait fitness curvature (Lande and Arnold 1983; Phillips and Arnold 1989; Blows and Brooks 2003). Ecological interaction studies likewise show that pollinators, herbivores, and other partners can modify one another's fitness effects, including non-additive consequences relevant to floral evolution (Herrera et al. 2002; Knauer et al. 2018). Attractive floral signals can recruit antagonists as well as mutualists, and antagonist suppression can reverse the net consequences of organisms that also deter pollinators (Theis and Adler 2012; Knauer et al. 2018).

The attraction-defence problem itself also has a substantial conceptual lineage. Non-pollinator agents can impose direct or indirect selection on floral traits, including conflict when antagonists and pollinators share trait preferences (Strauss and Whittall 2006), and florivory has been framed explicitly as the intersection of pollination and herbivory because damage to flowers can alter both direct reproduction and pollination pathways (McCall and Irwin 2006). Attraction and resistance have likewise been considered as linked targets of pollinator- and herbivore-mediated selection (Adler 2008). Chemical frameworks have proposed that tissue specificity, inducibility, resource allocation, and pleiotropy can create or relax conflicts between defence and pollinator attraction (Kessler and Halitschke 2009). Broader reviews likewise emphasize evolutionary interdependence between reproduction and defence and the need to integrate herbivore-induced responses, pollination, resource allocation, and plant fitness within the same systems (Johnson et al. 2015; Lucas-Barbosa 2016). Empirical work further shows that these effects can depend on herbivore identity, feeding mode, visitor identity, and plant state (Rusman et al. 2018). A full-factorial manipulation of herbivory and pollination in woodland strawberry further showed that selection on defence- and attraction-related traits depended on the other interaction partner (Egan et al. 2021), while pollinator-mediated selection itself is well known to vary with antagonists, resources, community context, populations, and years (Sletvold 2019).

More recent eco-coevolutionary theory goes further by modelling pollination benefits, attraction, defence, and their costs jointly, asking when antagonistic interactions can evolve toward net mutualism and how community context shifts that outcome (Johnson et al. 2021). These studies establish that attraction-defence balance, non-additivity, trade-offs, and context-dependent evolutionary outcomes are not new ideas.

What remains less explicit is a narrower inference problem. Before predicting how attraction and defence coevolve, or where complementarity occurs, can any region of mechanism space be ruled out as incompatible with local attraction-defence complementarity? The close literature provides rich mechanisms, factorial manipulations of ecological agents, and conditional predictions, but it does not by itself supply the focal one-sided exclusion rule used here for the local \(A\times D\) fitness curvature under an explicit joint-cost sign premise. In particular, manipulating pollination and herbivory can identify diffuse or conflicting selection on measured traits without constituting a factorial manipulation of the focal attraction and defence traits themselves (Egan et al. 2021). Nor does it uniquely allocate an observed total cross-trait curvature among antagonist relief, pollinator interference, and direct joint cost. This is a positioning claim about the inferential form of the present synthesis, not a priority claim that attraction-defence coupling or context dependence was previously unrecognized.

### 1.3 Ecological inference gap

We therefore ask a deliberately narrower question: **before predicting where attraction-defence complementarity occurs, can we identify where it cannot occur?** For one focal attraction trait and one flower-specific antagonist-reducing trait, complementarity means that either trait strengthens the local marginal fitness effect of the other on declared trait and outcome coordinates; substitutability means that it weakens that effect. This is narrower than asking whether the traits covary, whether correlational selection exists, where a fitness optimum lies, or whether an interaction evolves from antagonism to mutualism.

The mathematical step needed for this narrower question is intentionally simple rather than technically elaborate. Once biologically distinct channels are declared, the aim is to extract the weakest sign condition that rules out complementarity, not to replace existing evolutionary or community models with a more complicated dynamical system. The empirical literature then creates a second identification problem. Many studies measure floral signals, chemical or physical defences, pollinator responses, florivory, or nectar larceny, but few manipulate the same attraction and defence axes together on a common outcome scale. A defensible synthesis must therefore distinguish constituent-path evidence, same-system linkage, and direct \(A\times D\) evidence rather than pooling them as if they estimated one quantity. The contribution sought here is consequently not a new interaction type or a new mixed partial, but a mechanism-defined boundary on what the focal interaction can do and an evidence architecture for asking whether the mechanisms defining that boundary recur in nature.

### 1.4 Conditional biological hypothesis

Our hypothesis is explicitly conditional. A flower-specific defence trait can preserve attraction-generated value by reducing antagonist damage, but the same trait can reduce legitimate pollinator use or carry a direct joint cost. Floral signals can recruit antagonists, resistance can impose pollination costs, and floral chemistry can have variable pollinator effects, so each channel has biological precedent (Strauss et al. 1999; Theis and Adler 2012; Wright et al. 2013; Richardson et al. 2015; Stevenson et al. 2017).

These routes imply neither universal complementarity nor universal antagonism. Their balance must be evaluated for a specified attraction trait, a specified flower-specific antagonist-reducing trait, a specified outcome scale, and a specified ecological context.

### 1.5 Two-part contribution: mechanism and pattern

The paper is organized as two linked but inferentially distinct parts. **Part I — Mechanism** asks what mechanism determines the sign and whether any statement stronger than a case-specific balance survives response-shape variation. After an explicit orientation gate, we separate antagonist relief, pollinator interference, and direct joint cost, prove structural non-identifiability of the channel allocation from total fitness alone, and derive a one-sided result: under non-negative joint-cost curvature, complementarity is confined to a selectivity window where antagonist relief exceeds pollinator interference. The window is necessary, not sufficient.

**Part II — Pattern** asks what cross-system patterns recur in the mechanism classes defined by Part I. Quantitative meta-analysis is used only where compatible effect scales exist; otherwise source-adjudicated study clusters map recurrence, same-system co-occurrence, switching, and identification gaps without manufacturing a common effect size. This synthesis tests whether the constituent biology and exposure gate recur, not whether the full mixed partial has one universal sign.

The logic is therefore **Mechanism \(\rightarrow\) Pattern**, not theory \(\rightarrow\) validation. Part I first defines the mechanism classes and derives the structural constraint; those theory-defined classes then determine what counts as relevant evidence in Part II. The empirical synthesis therefore does not search for a pattern and infer a mechanism afterward. It asks whether the already-defined constituent routes, same-system combinations, switching architectures, and identification gaps recur independently across biological systems, while keeping direct estimation of the full mixed partial separate.

This ordering is also the paper's broader contribution to ecological synthesis. It answers a general concern raised by work on mechanistic context dependence: interaction effects need theory that specifies what varies and why, rather than a post hoc label for heterogeneous outcomes (Catford et al. 2022). When heterogeneous studies cannot estimate one common focal interaction, theory can first define exclusion conditions and evidence classes, after which synthesis can ask which components recur without promoting them to the full interaction. What is intended to generalize is this inference sequence, not the specific floral inequality: any application to another ecological system would require re-deriving its causal channels, orientations, and sign premises.

### 1.6 Paper organization

Sections 2–3 develop and test the mechanistic theory. Sections 4–5 define and report the cross-system Pattern synthesis. Section 6 integrates what became structurally general, what recurs biologically, what remains context dependent, and which experiment can next falsify or calibrate the framework. Section 7 concludes.

## 2. Part I — Mechanistic theory: mechanism and principle

### 2.1 Focal traits and outcome scale

Let \(A\) denote one measured floral attraction trait, \(D\) one measured flower-specific trait with an operationally defined antagonist-reduction role, and \(W(A,D;E)\) a declared fitness or biological-outcome score under ecological context \(E\). We use defence/access limitation only for a focal flower-specific trait with such an antagonist-reduction role; collateral obstruction of legitimate pollinators is a possible effect of that same trait, not the definition of defence. Neither \(A\) nor \(D\) is an omnibus index. Each application must declare its biological measurement scale.

The local attraction-defence interaction is

\[
W_{AD}=\frac{\partial^2 W}{\partial A\,\partial D}.
\]

On the declared coordinates and outcome scale, \(W_{AD}>0\) means that increasing either trait strengthens the local marginal effect of the other. We call this local complementarity. \(W_{AD}<0\) means that increasing either trait weakens the local marginal effect of the other, which we call local substitutability. These labels describe local curvature only. In particular, \(W_{AD}>0\) does not imply that either first derivative \(W_A\) or \(W_D\) is positive.

Positive affine rescaling of either trait preserves the sign of a nonzero mixed partial. Arbitrary nonlinear transformations need not. The sign is therefore a property of the declared biological parameterization rather than a transformation-free classification.

### 2.2 Signed channel decomposition

Write total outcome as mutualist contribution \(M\), antagonist loss \(G\), and a direct cost channel \(C\):

\[
W=M-G-C.
\]

Differentiation gives the signed identity

\[
W_{AD}=M_{AD}-G_{AD}-C_{AD}.
\]

Here \(C_{AD}\) is direct joint-cost curvature. Direct construction, allocation, or physiological costs are possible biological sources of this term, but the mathematical object is the cross-curvature of the declared cost channel, not total energetic cost.

This identity is algebraic. Biological labels do not determine the signs of the component mixed partials. Showing that \(D\) lowers pollinator visitation does not alone establish \(M_{AD}<0\); it must lower the marginal mutualist return to the same focal \(A\). Likewise, showing that \(D\) reduces antagonist damage does not alone establish \(G_{AD}<0\); it must reduce the marginal antagonist cost associated with the same focal \(A\).

### 2.3 Orientation gate and local sign criterion

Within a neighbourhood where the focal model establishes

\[
M_{AD}\le 0,\qquad G_{AD}\le 0,\qquad C_{AD}\ge 0,
\]

define non-negative magnitudes

\[
\iota=-M_{AD},\qquad \rho=-G_{AD},\qquad \kappa=C_{AD}.
\]

Then

\[
W_{AD}=\rho-\iota-\kappa.
\]

The local sign criterion is therefore

\[
W_{AD}>0 \iff \rho>\iota+\kappa,
\]

with equality defining the local break-even boundary. This oriented form is valid only after the orientation gate has been justified for the focal application. The channel architecture, orientation gate, and inference boundary are summarized in Fig. 1 and Table 1.

### 2.4 Mechanism non-identifiability

**Proposition 1.** Observation of total \(W(A,D)\), including exact knowledge of \(W_{AD}\), does not uniquely identify \(M_{AD}\), \(G_{AD}\), and \(C_{AD}\).

**Argument.** For any smooth function \(Q(A,D)\), define

\[
M^*=M+Q,\qquad G^*=G+Q,\qquad C^*=C.
\]

Then \(M^*-G^*-C^*=W\), while \(M^*_{AD}=M_{AD}+Q_{AD}\) and \(G^*_{AD}=G_{AD}+Q_{AD}\). The observed total outcome surface is unchanged although the channel curvatures differ. Equivalent reallocations can be constructed involving \(C\). This proves structural non-identifiability from total \(W\), even under noiseless and complete observation of that surface. It does not imply non-identifiability after channel-specific interventions, measurements, or justified structural restrictions.

### 2.5 Environmental comparative statics

Let pollinator service \(P\) and antagonist pressure \(H\) be exogenous context indices. In an oriented neighbourhood,

\[
W_{AD}(P,H)=\rho(P,H)-\iota(P,H)-\kappa(P,H).
\]

Thus,

\[
\frac{\partial W_{AD}}{\partial H}
=\frac{\partial \rho}{\partial H}
-\frac{\partial \iota}{\partial H}
-\frac{\partial \kappa}{\partial H},
\]

and

\[
\frac{\partial W_{AD}}{\partial P}
=\frac{\partial \rho}{\partial P}
-\frac{\partial \iota}{\partial P}
-\frac{\partial \kappa}{\partial P}.
\]

The explicit local directional conditions are

\[
\frac{\partial W_{AD}}{\partial H}>0
\iff
\frac{\partial \rho}{\partial H}
>
\frac{\partial \iota}{\partial H}
+
\frac{\partial \kappa}{\partial H},
\]

and

\[
\frac{\partial W_{AD}}{\partial P}<0
\iff
\frac{\partial \iota}{\partial P}
+
\frac{\partial \kappa}{\partial P}
>
\frac{\partial \rho}{\partial P}.
\]

Equalities define local environmental break-even conditions, and reverse inequalities reverse the direction. Greater antagonist pressure therefore moves the interaction toward complementarity only under the first inequality. Greater pollinator service moves the interaction toward substitutability only under the second. Verbal claims about more antagonists or more pollinators are insufficient without these conditions.

### 2.6 Implemented corollary and finite sensitivity analysis

The implemented corollary uses declared nonlinear response functions for attraction, defence, mutualist service, antagonist damage, and direct joint cost. Four response-shape variants were endpoint-normalized over \(A,D\in[0,1]\), so attraction response at \(A=1\), defence response at \(D=1\), and direct joint-cost scale at \(A=D=1\) match across variants.

The finite design evaluated \(A,D\in\{0.2,0.5,0.8\}\), pollinator-service and antagonist-pressure indices \(P,H\in\{0.2,0.5,0.8\}\), and an auxiliary reproductive-assurance moderator \(R\in\{0,0.5\}\). \(R\) is not a third focal trait. Four biological parameter scenarios and four endpoint-normalized response-shape variants yielded 2,592 mixed-partial evaluations.

Analytic mixed partials were checked against independently implemented finite-difference derivatives. The absolute numerical tolerance for classifying zero was \(10^{-10}\) on the declared score scale. Finite-grid percentages are descriptive occupancies under the declared design, not probabilities or estimates of prevalence in nature.

### 2.7 Selectivity window and one-sided bound

For the deployed oriented family, define the **selectivity window** as the region in which antagonist relief exceeds pollinator interference before the direct joint-cost term is charged.

**Theorem 1 (one-sided selectivity bound).** If direct joint-cost curvature is non-negative, \(\kappa\ge0\), then

\[
W_{AD}>0 \;\Longrightarrow\; \rho>\iota.
\]

Equivalently, complementarity does not occur outside the selectivity window.

The proof is immediate from \(W_{AD}=\rho-\iota-\kappa\): if \(W_{AD}>0\) and \(\kappa\ge0\), then \(\rho-\iota=W_{AD}+\kappa>0\). The proof uses only the additive relief-minus-interference-minus-cost structure and \(\kappa\ge0\), preserved by all four declared endpoint-normalized response-shape variants. The signs of \(\rho\) and \(\iota\) are not used by this implication; their non-negativity belongs to the oriented baseline interpretation rather than to Theorem 1 itself. When \(\kappa=0\), the implication runs both ways and the window becomes the exact sign criterion.

The algebra is therefore one line. Its ecological meaning is also simple: if simultaneous attraction-defence investment does not have negative joint-cost curvature, a flower cannot be locally attraction-defence complementary unless antagonist relief exceeds pollinator interference. Crossing that relief-versus-interference threshold only makes complementarity possible; it does not make it inevitable, because a positive joint-cost term can still reverse the sign.

The converse is not generally true when \(\kappa>0\). Outside the window, complementarity would require \(\kappa<\rho-\iota\le0\). Thus a **negative joint-cost curvature is necessary for the bound to fail, and sufficient when negative enough**. Because the implemented parameterization constrains direct joint cost to be non-negative, this is a structural result of the declared family rather than an empirical statement about joint-cost curvature in nature.

## 3. Part I results — mechanistic sign regimes

### 3.1 General sign criterion

The oriented local interaction was complementary exactly when antagonist relief exceeded the sum of mutualist interference and direct joint-cost curvature. It was substitutable when the opposing terms exceeded antagonist relief. This result did not require attraction and defence to have a fixed relationship, and complementarity did not imply that both traits had positive marginal effects.

### 3.2 Environmental direction cannot be inferred from pressure alone

The unrestricted derivatives showed that increased antagonist pressure did not necessarily increase complementarity, because antagonist pressure could also modify pollinator interference or direct joint-cost curvature. Similarly, increased pollinator service did not necessarily favour substitutability. Directional predictions required the explicit inequalities among all context derivatives given above.

### 3.3 Finite sensitivity analysis

Across the 2,592 declared evaluations, 1,342 were complementary and 1,250 were substitutable; none fell within the numerical zero tolerance. These correspond to unweighted finite-grid occupancies of 51.8% and 48.2%, respectively, and must not be interpreted as natural frequencies.

Across 648 fixed case-by-parameter-scenario summaries, 480 were unanimous across the four response-shape variants and 168 were mixed or sensitive. In the high-antagonism-tracking, low-pollination-obstruction, low-direct-joint-cost scenario, 617 of 648 evaluations were complementary and 144 of 162 local cases were unanimous across response shapes. In the high-pollination-obstruction and high-direct-joint-cost scenario, 610 of 648 evaluations were substitutable and 138 of 162 local cases were unanimous.

After combining all four deliberately contrasting biological scenarios and response shapes, none of the 162 local cases was unanimous across the full tested set. This is expected for a conditional theory in which biologically decisive route strengths are deliberately varied.

### 3.4 Verification of the one-sided selectivity bound

The theorem itself is algebraic; the declared grid verifies that the implementation obeys its premises across the full finite design. Among 2,592 evaluations, all 1,342 complementary evaluations occurred inside the selectivity window, giving **zero false negatives** for the bound. The converse was loose: 397 in-window evaluations were substitutable, so the share of in-window points that were genuinely complementary was 77.2%; approximately 23% of the window therefore failed as a sufficient criterion.

When direct joint cost was forced to zero, the window and the sign criterion coincided exactly across the same declared design. These fractions are unweighted finite-grid occupancies, not estimates of natural prevalence. Their role is to distinguish an exact structural implication from the false two-sided rule that the finite design itself rejects. The finite design and its regime/verification readout are summarized in Fig. 2 and Table 2; analytic-versus-finite-difference checks and scenario-specific maps are provided in Supplementary Figs. S1–S2 and Tables S1–S2.

## 4. Part II — Meta-analysis and cross-study pattern synthesis

Part II asks whether the mechanism classes derived in Part I recur across independent biological systems and whether their realized state changes systematically with context. We use **meta-analysis** only where study outcomes can be expressed on a defensible common quantitative scale. Where outcome scales are intrinsically non-equivalent, we retain a source-adjudicated cross-study pattern map rather than pooling incompatible quantities. Accordingly, cross-system generality here means recurrence across independent systems and robustness within the admitted synthesis, not prevalence in nature.

### 4.1 Theory-to-pattern evidence map

The empirical synthesis was organized around the four theory-derived marginal routes \(A\rightarrow\)pollination, \(A\rightarrow\)antagonism, \(D\rightarrow\)antagonism, and \(D\rightarrow\)pollination. Evidence was admitted only when the focal floral context, trait axis, response, and study identity could be source-adjudicated. Same-system evidence was tracked separately from unrelated marginal studies, and direct \(A\times D\) evidence required a distinct attraction axis, a flower-specific antagonist-reducing defence/access axis, and an interaction on a common outcome.

A registered expansion targeted empty or weakly replicated theory-facing cells rather than article count. New records were admitted as independent biological clusters under the same route and organ rules; studies lacking a clean focal \(A\) or flower-specific \(D\) were retained as context programs outside route-ledger N. Expansion stopped after two consecutive targeted screening batches yielded no new admissible Pattern class, and a parallel quantitative search yielded no additional synthesis with a distinct theory-facing axis.

Within-system changes were retained rather than averaged away. The coding ontology included trait intensity, resource or exposure context, consumer identity and function, response stage or scale, compound or mechanism identity, guarded defence, spatial or temporal filtering, attack mode, visitor functional-mode switching, lifecycle-stage role reversal, and population or trait-class dependence. Because the underlying outcomes are non-equivalent, we did not fit a cross-outcome grand moderator coefficient. Completion required explicit states for all four marginal routes, saturation of the direct-interaction and direct joint-cost searches, same-system linkage, mapped conditionality, two reproduced quantitative modules, explicit status for secondary contextual syntheses, and preservation of the inference boundary between constituent evidence and the theoretical mixed partial.

### 4.2 Quantitative meta-analytic modules

#### 4.2.1 Meta-analysis 1: floral-larceny antagonist-pressure pattern

The first quantitative module reanalysed the deposited effect-size data underlying Leal et al. (2025). Effects were recomputed from deposited group means as oriented log response ratios rather than trusting the deposited effect-size label. Effects were reduced to one aggregate per independent study cluster within each outcome stratum before random-effects synthesis. The primary within-cluster correlation choice was conservative, and sensitivity analyses varied that choice and reinstated quarantined rows whose deposited point estimates disagreed in sign with their own group means.

The admissible role of this module is to test whether realised floral-antagonist pressure can impose measurable costs on reward availability, legitimate visitation, and plant reproduction, and to audit whether antagonist exposure and pollinator service are empirically separable. It is not an estimate of \(\rho\), \(\iota\), \(\kappa\), or \(W_{AD}\).

#### 4.2.2 Meta-analytic synthesis 2: floral-volatile consumer-response pattern

The second quantitative module reanalysed the current deposited supplementary workbook of Sasidharan et al. (2023). Citation strings were normalized conservatively and linked only by exact normalized identity or explicit shared DOI, recovering 32 study components without fuzzy merging. Physiological detection was analysed on unique floral-volatile-compound × insect × consumer-role test units. Influence was assessed by deleting each recovered study component in turn and by an equal-weight study-role summary.

Behavioral responses were categorical and heterogeneous across assay types, so no common continuous effect size was manufactured. Repeated compound × insect × role units that disagreed across studies were retained as context dependence. Differences between current deposited counts and printed article tables were recorded explicitly rather than resolved by arbitrary row deletion.

#### 4.2.3 Secondary cross-synthesis/context modules

Three additional syntheses were retained as independent contextual modules rather than promoted to co-equal reproduced meta-analyses. Haas-Desmarais et al. (2026) provide a published multilevel synthesis of 171 studies and 1,348 study cases on herbivory effects on floral traits, pollinator attraction, and reproduction; we independently retrieved and hashed the publisher supplementary package, but did not reconstruct its raw effect-size table locally, and herbivory treatment is not equated with the focal floral defence trait \(D\). Caruso et al. (2019) provide a published selection synthesis whose main uncertainty-bearing analysis uses 755 directional selection gradients with standard errors from 36 articles; the Dryad landing record and workbook identities were verified, but current file-byte access was blocked, so the study remains a published selection-context module rather than a local reanalysis. Junker and Blüthgen (2010) synthesize 18 publications and 425 floral-scent response observations; their visitor-dependence categories provide an independent consumer-filtering Pattern but are not treated as identical to pollinator-versus-antagonist roles.

These modules test recurrence of tissue, trait-class, consumer, assay, and selection-context dependence. Their study or observation counts are never added to the route-ledger cluster total, and their effect scales are not pooled with the Leal or Sasidharan modules.

### 4.3 Computational and AI-assisted workflow transparency

During analysis and manuscript development, large language models from OpenAI and Anthropic were used to assist code generation, structured literature triage, reproducibility checks, and manuscript drafting and editing. AI-generated output was not treated as empirical evidence. Source claims entered the admitted evidence architecture only through source-linked audit records, numerical results were generated or reconstructed from committed code and data products, and manuscript-facing counts and figures were protected by repository regression tests. The authors retain responsibility for the final scientific content and must confirm this disclosure together with the exact submitted version.

## 5. Part II results — meta-analytic patterns across systems

### 5.1 Pattern scaffold: mechanism recurrence and same-system architecture

The saturated source-adjudicated route ledger contained 56 effect or directional records across 25 independent biological study clusters. All four marginal route families had explicit empirical states. Independent cluster counts were five for \(A\rightarrow\)pollination, eight for \(A\rightarrow\)antagonism, eighteen for \(D\rightarrow\)antagonism, and ten for \(D\rightarrow\)pollination. These overlapping counts describe evidence capacity in the screened architecture and are not estimates of mechanism prevalence in nature.

Fourteen study clusters contained at least two theory-relevant marginal routes in the same biological system. Attraction-side recurrence now includes visual and colour/scent signal axes associated with antagonist use as well as shared mutualist-antagonist tracking; a recombinant *Silene* signal system independently links floral colour and scent dimensions to seed-predator host choice (Page et al. 2014). Defence-side recurrence spans chemical deterrence and several distinct physical solutions, including liquid-filled bracts or calyces, sticky corolla surfaces, slippery wax-covered perianths, petal hairs, and spur-enclosing bracts. In *Pedicularis rex*, a water-filled bract strongly reduced seed predation while showing no detected effect on legitimate pollinator or nectar-robber visitation, because robbers could bypass the barrier's attack geometry (Sun and Huang 2015). In *Thunia alba*, removing a spur-enclosing bract shifted the same *Bombus* visitor from legitimate pollination toward nectar robbery without increasing hourly arrival frequency, while pollinia transfer and fruit set declined (Wu and Gao 2024).

The same-system panel therefore supports guarded defence, shared signal tracking, attack-mode filtering, and visitor functional-mode routing as recurrent biological states. It still does not identify the full mixed partial because the component routes are generally not estimated on a common outcome scale.

### 5.2 Identification-gap pattern: direct interaction scarcity and joint cost

The registered direct \(A\times D\) search reached its stopping rule with one strict total reproductive-outcome cluster: Soper Gorden and Adler's (2018) *Impatiens capensis* study. The reconstructed interaction for chasmogamous fruits per plant per day was \(-0.0820\pm0.0548\) SE, whereas the interaction for seeds per chasmogamous fruit was \(+0.1040\pm0.1043\) SE. Both confidence intervals included zero, so the cleanest total-outcome candidate remained sign-unresolved and reproductive-component dependent in point direction.

A higher-specificity crossed floral-trait program nevertheless shows that channel-level interaction signs can reverse with consumer context. Kessler et al. (2015) independently crossed floral benzylacetone emission with floral nectar production. With \(D\) oriented as nectar restriction, source-mean pollination-channel crossed contrasts were \(-0.790\) for the native visitor community, \(-0.432\) under *Manduca sexta*, and \(+0.8699\) under *Hyles lineata*. These values are direct crossed-trait contrasts on a mutualist-mediated outcome, not estimates of total \(W_{AD}\), and the published summaries do not identify an interaction standard error or confidence interval. They therefore strengthen the context-dependence Pattern without resolving total curvature.

The independent direct joint-cost search reached its stopping rule with zero strict eligible estimates of the additional intrinsic cost of simultaneous investment in distinct floral attraction and defence/access axes. The correct empirical state for \(\kappa\) is uncertainty, not zero. After Theorem 1 this gap has sharper meaning: the sign of direct joint-cost curvature is the minimal empirical gate for whether the one-sided selectivity bound applies biologically to a focal trait pair.

### 5.3 Conditionality pattern: mechanism channels open, close, and change role

Seventeen independent study clusters contained source-verified changes in sign or biological state across contexts. Seven additional context programs were retained outside route-ledger N because their focal manipulation was environmental pressure, damage, pollination syndrome, or a broader reproductive module rather than a clean marginal \(A\) or flower-specific \(D\) route.

The resulting ontology is broader than a list of positive-versus-negative reversals. Trait intensity, reward or exposure context, consumer identity, response stage, compound identity, and population context can change effect state. Physical defences can also be spatially or temporally gated: body size, floral position, attack mode, or the pollinator-critical stage determines which consumer can cross a barrier. Guarded states recur in which antagonist reduction is strong but a pollinator penalty is not detected on the tested response. Conversely, the same visitor can change ecological function without a change in identity: floral access architecture can route a visitor between legitimate pollination and robbery. A separate *Silene stellata* system extends this principle across the consumer lifecycle, with adult *Hadena* contributing pollination while larvae impose seed-predation costs and selection differs through male and female fitness pathways (Zhou et al. 2020).

Conditionality therefore occurs as true direction changes, as threshold-like opening or closing of channels, and as changes in the ecological role carried by the same consumer taxon. This is the empirical Pattern most directly aligned with the Part I balance criterion.

### 5.4 Meta-analysis 1: floral larceny opened an average antagonist-pressure gate but not a universal one

The Leal et al. (2025) deposited-synthesis reanalysis recovered a pooled log response ratio of \(-0.210\) for female reproductive success across 48 independent study clusters, \(-0.483\) for nectar standing crop across 28 clusters, and \(-0.291\) for legitimate visitation across 22 clusters. These correspond to approximately 19%, 38%, and 25% reductions on the response-ratio scale, respectively. Male reproductive success was highly heterogeneous and uninformative.

The female-fitness direction was repeatable but not universal: 35 of 48 clusters (73%) were negative, while the 95% prediction interval was \(-1.13,+0.71\) and significantly positive systems occurred. The female-fitness, reward, and visitation pooled directions survived every leave-one-cluster-out refit, the declared within-cluster correlation choices, and reinstatement of quarantined sign-discrepant source rows. Six declared moderator analyses detected no statistically resolved context dependence and explained only 0-8% of the extreme heterogeneity. The synthesis therefore establishes that the antagonist-pressure gate can be open on average while leaving its realised magnitude and even sign strongly system dependent.

The apparent reward-depletion sequence is not treated as a demonstrated mechanism. Only five clusters measured nectar standing crop, legitimate visitation, and female fitness together, and only two of those showed all three arrows negative. Among the eleven clusters measuring both nectar and visitation, the within-study association between reward depletion and visitation loss was \(r=-0.17\), opposite in sign to the simplest reward-depletion prediction and indistinguishable from zero at that sample size. The three pooled arrows are therefore constituent-path evidence, not an end-to-end within-study mechanism chain.

Larceny exposure also reduced legitimate visitation, demonstrating that the environmental indices \(H\) and \(P\) need not be empirically separable. This observation does not estimate \(W_{AD}\); it shows that exposure can move more than one channel at once and that the location of the selectivity window is itself an empirical ecological state.

### 5.5 Meta-analytic synthesis 2: floral volatile responses were shared but composition-dependent

The Sasidharan et al. (2023) current deposited synthesis contained 151 detected and 69 non-detected physiological pollinator test units, and 84 detected and 19 non-detected florivore test units. The assembled florivore-minus-pollinator risk difference was \(+0.129\), with a risk ratio of 1.188. Removing each of the 32 conservatively recovered study components in turn left the risk difference positive in all 32 refits, with a range of approximately +0.087 to +0.207.

This assembled contrast was not reproduced as a within-study role effect. Only three study components contained physiological detection data for both consumer roles, and all three paired differences were zero. The result is therefore a robust cross-study pattern in the current deposit but remains vulnerable to study-by-role composition as a causal explanation.

Behavioral evidence reinforced the context-dependence conclusion. Six repeated floral-volatile-compound × insect × role units were discordant across source studies, and all six switched between attraction and no response rather than attraction and repulsion. Shared attraction across pollinators and florivores was recurrent, whereas shared repulsion was rarer, but the exact attractive count differed between current deposited data and printed table summaries. The module therefore supports shared consumer tracking and context sensitivity while preserving source-version uncertainty.

### 5.6 Cross-system pattern: recurrent mechanisms, conditional balance

Taken together, Part II identifies a general empirical Pattern that is narrower and more defensible than a universal attraction-defence sign. The four constituent route families recur across 25 independent source-adjudicated biological systems, including repeated visual/scent attraction signals and chemically or physically distinct antagonist-reducing traits. Fourteen same-system clusters show that routes can co-occur, while 17 sign/state-switch clusters and seven context-only programs show that trait intensity, resources, exposure, consumer identity, attack geometry, response stage, population, visitor functional mode, and even consumer lifecycle can change which channel is expressed. These annotations are not additive counts: same-system and sign/state-switch classifications can overlap within the 25-cluster route universe, while the seven context-only programs are explicitly outside route-ledger N.

The Leal pooled directions retain their declared influence and sensitivity checks. The Sasidharan assembled contrast remains positive in all leave-one-study-component-out refits, but this is robustness of the assembled cross-study composition rather than a within-study consumer-role effect: only three study components contain both physiological roles and all three paired differences are zero. The three secondary contextual syntheses independently reinforce strong tissue, consumer, trait-class, assay, and selection-context dependence, but remain explicitly separated by evidence status and effect scale. Direct \(A\times D\) remains one sign-unresolved strict cluster, and direct joint-cost evidence remains zero strict estimates. The meta-analytic Pattern is therefore **recurrent mechanisms plus context-dependent balance**, not a universal value or sign of \(W_{AD}\). The cross-system evidence architecture is summarized in Fig. 3 and Table 3, with the quantitative modules in Table 4. The reproduced quantitative results and their identification boundary are shown directly in Fig. 4, while the 14 same-system multi-route clusters are shown study-by-study in Fig. 5. Full route, conditionality, direct-identification, and stopping-rule records are provided in Tables S3–S6, with numerical implementation and robustness diagnostics in Supplementary Figs. S1–S3.

## 6. Integration — from mechanism to pattern

### 6.1 A simple bound on a complex ecological balance

The central mathematical result is simpler than the surrounding ecological notation may suggest: it is a one-line exclusion, not a high-dimensional prediction of nature. Part I gives the recurrent route-separation Pattern a precise role. Under non-negative joint-cost curvature, antagonist relief must exceed pollinator interference before complementarity is possible. Spatial, temporal, chemical, and attack-mode separation can therefore move a system into a permissive selectivity window, but they cannot by themselves determine the sign of \(W_{AD}\). The failed converse is essential: recurrent discrimination mechanisms identify where complementarity is allowed, not where it must occur.

Biologically, the selectivity window is best read as a functional-discrimination condition rather than as a label attached to a defence trait. Earlier work already framed florivory as an explicit bridge between pollination and herbivory (McCall and Irwin 2006), proposed tissue specificity and inducibility as ways to reduce conflict between defence and pollinator attraction (Kessler and Halitschke 2009), and showed that herbivore-plant-pollinator effects can depend on the identity and mode of interacting consumers (Lucas-Barbosa 2016; Rusman et al. 2018). In the present synthesis, guarded defence, consumer-specific barriers, attack-mode filtering, and visitor routing are therefore interpreted as empirical states consistent with increasing antagonist relief relative to pollinator interference. These studies do not directly estimate \(\rho-\iota\), however, so their role is to show that the required route separation is biologically realizable, not to classify individual systems as mathematically inside the window.

Part II supplies the corresponding biology. Guarded states, consumer-specific barriers, attack-mode filtering, and shifts of the same visitor between legitimate pollination and robbery all alter the balance between \(\rho\) and \(\iota\). Floral larceny further shows that the antagonist-exposure gate is non-zero on average but strongly heterogeneous. Together, the theory and synthesis support a moving permissive window: the required mechanisms recur, while exposure and joint cost determine whether the permitted state is actually complementary.

### 6.2 Recurrence does not identify total curvature

Part II provides constituent-path evidence and does not calibrate \(W_{AD}\). The Leal and Sasidharan modules, the secondary contextual syntheses, and the same-system route panel establish recurrent biological channels and switching states, but none is algebraically equivalent to the focal attraction-defence mixed partial. This is the empirical counterpart of Proposition 1: more observations of total fitness or more unrelated route studies cannot recover channel allocation without linked measurements or interventions on the same focal traits.

The sparse direct layer therefore identifies two distinct empirical gaps. Total \(W_{AD}\) requires a focal attraction × defence design on a common outcome; the strict total-outcome candidate remains sign-unresolved, while crossed floral-trait evidence shows consumer-context-dependent channel interactions without identifying total curvature. Direct joint-cost curvature has zero strict estimates in the admitted evidence layer, so \(\kappa\) remains unidentified, not zero. Under the one-sided theorem, a negative joint-cost curvature is the only escape route from the selectivity window in the declared family, and it must be sufficiently negative relative to the relief-interference difference.

Shared construction, allocation, biochemical, developmental, or physiological constraints are plausible biological sources of joint-cost curvature. Allocation costs, pleiotropy, and defence-reproduction coupling have long been discussed as mechanisms connecting attraction and defence (Kessler and Halitschke 2009; Johnson et al. 2015; Lucas-Barbosa 2016), but those literatures should not be equated with the specific cross-curvature \(\kappa\). The strict audit recovered marginal attraction costs, marginal defence costs, trait integration or covariance, and inferred resource reallocation rather than a direct estimate of the additional cost of simultaneous investment in distinct \(A\) and \(D\) axes. These observations therefore motivate hypotheses about \(\kappa\); they do not identify it.

The framework is related to correlational selection rather than a replacement for it. On suitable standardized trait and relative-fitness coordinates, \(W_{AD}\) may correspond to a correlational-selection term; the contribution here is the ecological allocation and inference boundary attached to that curvature. Predictions about trait covariance, genetic correlation, evolutionary trajectories, or equilibria still require genetic architecture, inheritance, constraints, and dynamics beyond the local mixed partial.

### 6.3 Context moves the window as a joint ecological state

The environmental analysis likewise yields a balance, not a verbal rule that more antagonists must favour complementarity or more pollinators must favour substitutability. In the larceny synthesis, antagonist exposure reduces female fitness on average, yet the prediction interval spans both signs and the declared moderators explain little of the heterogeneity. The current context axes therefore do not locate the selectivity window reliably in a new system.

Ecologically, context is therefore better treated as a coupled state of consumer identity, attack mode, reward or resource conditions, exposure, and response stage than as a single named pressure variable. This distinction parallels the broader separation between mechanistic context dependence caused by interaction effects and apparent context dependence generated by confounding, inference, or methodological differences (Catford et al. 2022). The source-adjudication and evidence hierarchy used here are important precisely because both possibilities can coexist across a heterogeneous literature. The recurrent within-system sign/state switches are not treated as noise around one universal effect; where source design supports them, they indicate that the balance among causal channels itself changes among ecological states. This interpretation is consistent with long-standing evidence that pollinator-mediated selection varies with antagonists, resources, community context, populations, and years (Sletvold 2019), and with factorial evidence that the selective effect of one interaction partner can depend on the presence or ecological effect of the other (Egan et al. 2021).

Antagonist exposure also reduces legitimate visitation, showing that realised \(H\) and \(P\) need not be independent. In the separable corollary, allowing \(P\) to decline with \(H\) adds a positive correction to \(\partial W_{AD}/\partial H\) because the pollinator-interference channel weakens while antagonist relief is loaded. This makes the separable result conservative in direction for that specific coupling, but it does not calibrate the total derivative or justify a general regime prediction. Prospective applications should therefore measure exposure and channel responses jointly rather than treat a named pressure variable as a sufficient context descriptor.

### 6.4 Falsification before calibration

The one-sided theorem changes the empirical order of operations. A **2 × 2 allocation** design — neither focal trait, attraction only, defence only, and both — can first test the sign of direct joint-cost curvature using an appropriately defined construction, resource, or physiological cost. A sufficiently negative cross-cost would falsify the one-sided bound for that focal trait pair without requiring pollinators, antagonists, or total-fitness measurement.

A separate **full attraction × defence factorial** has a harder purpose: estimating total \(W_{AD}\) and its channel allocation. That design must manipulate the two focal traits in the same biological units and measure compatible mutualist contribution, antagonist loss, direct cost, and total fitness. The remaining unknowns are therefore no longer open-ended gaps inside the present argument. They are two explicit next tests: a cheap applicability/falsification gate followed, when needed, by full mechanistic calibration.

The mechanism-first order therefore turns synthesis into experimental triage. The literature need not be enlarged indefinitely once the structural uncertainty has been localized: a comparatively cheap test of \(\kappa\) can challenge applicability of the bound, whereas only a channel-resolved factorial can calibrate the full interaction. The synthesis thus resolves an empirical ambiguity by converting heterogeneous evidence into an ordered sequence of falsification and calibration rather than another call for undirected data collection. The quantitative evidence, remaining identification gaps, and the two ordered next tests are summarized in Fig. 5.

### 6.5 What transfers beyond the floral case

Nothing in the inferential sequence requires flowers, although the biological decomposition developed here does. In this sense the manuscript follows the broader recommendation that mechanistic context dependence should be organized by explicit interaction theory to improve explanation and transferability (Catford et al. 2022), while remaining deliberately conservative about transporting any particular sign rule. In another multi-partner ecological system, the focal variables and outcome would first need to be declared, the net interaction decomposed into biologically defensible channels, and any one-sided constraint re-derived under explicit sign premises. Only then should those theory-defined channels be used to organize heterogeneous evidence. What transfers is therefore the workflow—**constraint before pattern**—not the particular floral route signs or the inequality derived from them. This distinction permits broader conceptual use without turning a bounded floral result into an unsupported universal law.

## 7. Conclusions

Under non-negative joint-cost curvature, floral attraction-defence complementarity cannot occur outside the selectivity window in which antagonist relief exceeds pollinator interference. This is the paper's strongest structural result; the identity \(W_{AD}=\rho-\iota-\kappa\) is only its bookkeeping scaffold. The 2,592-evaluation implementation contains no counterexample to the one-sided implication, while approximately 23% of in-window evaluations remain substitutable, so the window is a necessary permissive region rather than a universal sign criterion.

Across systems, the constituent mechanisms and switching architectures recur, but their realised balance remains context dependent. Floral larceny opens the antagonist-pressure gate on average, yet 35 of 48 female-fitness effects are negative, the 95% prediction interval spans \(-1.13,+0.71\), and the declared moderators explain only 0-8% of the heterogeneity. Part II therefore supports recurrence and conditionality rather than calibration of total \(W_{AD}\); the within-study reward-mediated mechanism chain is not demonstrated.

The remaining uncertainty has become experimentally specific rather than conceptually open-ended. Direct joint-cost curvature is unidentified, not zero, and a sufficiently negative value is the unique escape route from the one-sided bound in the declared family. A 2 × 2 allocation experiment can test that applicability gate, whereas a full attraction × defence factorial is still required to estimate total \(W_{AD}\) and allocate it among ecological channels. The theory therefore ends not with a request for more broad evidence, but with a concrete falsification test and a separate calibration experiment.

More broadly, the paper offers a strategy for synthesis under context dependence: derive a mechanistic exclusion before searching for a universal mean effect, then use the resulting evidence architecture to identify which mechanisms recur and which minimal measurements can falsify the boundary.

## Figure captions

**Fig. 1** Mechanistic architecture of the local attraction-defence interaction. Attraction may increase mutualist service and antagonist exposure. A focal flower-specific defence trait is defined by an operational antagonist-reduction role, but the same trait may interfere with legitimate pollinator use. Attraction and defence may also interact through direct joint-cost curvature. After the orientation gate is established, the local mixed partial is \(W_{AD}=\rho-\iota-\kappa\), where \(\rho\) is antagonist relief, \(\iota\) is mutualist interference, and \(\kappa\) is direct joint-cost curvature. The diagram does not imply that every route occurs in every system or that the components are identifiable from total fitness alone

**Fig. 2** Conditional sign regimes in the endpoint-normalized implemented corollary. The declared finite design evaluates focal attraction and defence coordinates, exogenous pollinator-service and antagonist-pressure indices, an auxiliary reproductive-assurance moderator, four biological parameter scenarios, and four endpoint-normalized response-shape variants. Counts and percentages are unweighted occupancies of the declared finite tested set, not estimates of prevalence in nature. Response-shape unanimity is evaluated within fixed biological scenarios, whereas the full tested set deliberately combines scenarios with opposing route strengths

**Fig. 3** Meta-analytic pattern architecture and identification boundary. Source-adjudicated evidence is organized as four marginal route families, same-system multi-route regimes, context/sign-switch and context-only programs, two reproduced quantitative synthesis modules, three secondary contextual syntheses, the saturated direct \(A\times D\) layer, and the direct joint-cost search. Counts indicate evidence capacity in the screened architecture rather than prevalence. Guarded defence, spatial/temporal filtering, visitor functional-mode switching, and lifecycle-role reversal are recurrent state classes. Marginal, same-system, and secondary contextual evidence terminate at the inference boundary and are not combined into an estimate of \(W_{AD}\)

**Fig. 4** Quantitative evidence, identification boundary, and next empirical tests. The Leal et al. floral-larceny module shows negative pooled directions for female fitness, nectar standing crop, and legitimate visitation while retaining a female-fitness prediction interval spanning both signs and weak moderator explanation. The Sasidharan et al. floral-volatile module retains a positive assembled florivore-minus-pollinator contrast under all leave-one-component-out refits but lacks a paired within-study consumer-role difference. Neither module estimates \(\rho\), \(\iota\), \(\kappa\), or total \(W_{AD}\). The remaining direct-identification state is one strict sign-unresolved total-outcome cluster and zero strict joint-cost estimates, motivating first a 2 × 2 cost assay for the sign of \(\kappa\), then a full attraction × defence factorial for total and channel-resolved calibration.

**Fig. 5** Same-system route architecture across the saturated evidence universe. Rows are the 14 independent biological clusters with at least two linked marginal route families, or an explicit same-system linkage retained by the evidence audit. Filled cells indicate categorical presence of A → pollination, A → antagonism, D → antagonism, and D → pollination routes. The matrix shows recurrence of linked constituent mechanisms within biological systems; cells are not effect sizes and do not constitute direct \(A\times D\) evidence.

## Table captions

**Table 1. Definitions, required declarations, and inference boundaries for the focal local theory.**

**Table 2. Declared endpoint-normalized finite sensitivity design, numerical convention, and canonical sign and agreement results.**

**Table 3. Cross-study pattern scaffold: source-adjudicated mechanism recurrence, same-system architecture, conditionality, direct-interaction state, and direct joint-cost evidence state.**

**Table 4. Quantitative meta-analytic modules, recurrent patterns, robustness checks, and prohibited interpretations.**

## References

Adler LS (2008) Selection by pollinators and herbivores on attraction and defense. In: Tilmon KJ (ed) *Specialization, Speciation, and Radiation: The Evolutionary Biology of Herbivorous Insects*, pp 162–173. University of California Press. https://doi.org/10.1525/california/9780520251328.003.0012

Blows MW, Brooks R (2003) Measuring nonlinear selection. *The American Naturalist* 162:815–820. https://doi.org/10.1086/378905

Caruso CM, Eisen KE, Martin RA, Sletvold N (2019) A meta-analysis of the agents of selection on floral traits. *Evolution* 73:4–14. https://doi.org/10.1111/evo.13639

Catford JA, Wilson JRU, Pyšek P, Hulme PE, Duncan RP (2022) Addressing context dependence in ecology. *Trends in Ecology & Evolution* 37:158–170. https://doi.org/10.1016/j.tree.2021.09.007

Egan PA, Muola A, Parachnowitsch AL, Stenberg JA (2021) Pollinators and herbivores interactively shape selection on strawberry defence and attraction. *Evolution Letters* 5:636–643. https://doi.org/10.1002/evl3.262

Haas-Desmarais S, Castagneyrol B, Abdala-Roberts L, Lortie CJ, Traveset A, Moreira X (2026) The effect of herbivory on pollinators: a revisited meta-analysis. *Annals of Botany* 137:879–885. https://doi.org/10.1093/aob/mcaf258

Herrera CM et al. (2002) Interaction of pollinators and herbivores on plant fitness suggests a pathway for correlated evolution of mutualism- and antagonism-related traits. *Proceedings of the National Academy of Sciences USA* 99:16823–16828. https://doi.org/10.1073/pnas.252362799

Johnson CA, Smith GP, Yule K, Davidowitz G, Bronstein JL, Ferrière R (2021) Coevolutionary transitions from antagonism to mutualism explained by the Co-Opted Antagonist Hypothesis. *Nature Communications* 12:2867. https://doi.org/10.1038/s41467-021-23177-x

Johnson MTJ, Campbell SA, Barrett SCH (2015) Evolutionary interactions between plant reproduction and defense against herbivores. *Annual Review of Ecology, Evolution, and Systematics* 46:191–213. https://doi.org/10.1146/annurev-ecolsys-112414-054215

Junker RR, Blüthgen N (2010) Floral scents repel facultative flower visitors, but attract obligate ones. *Annals of Botany* 105:777–782. https://doi.org/10.1093/aob/mcq045

Kessler A, Halitschke R (2009) Testing the potential for conflicting selection on floral chemical traits by pollinators and herbivores: predictions and case study. *Functional Ecology* 23:901–912. https://doi.org/10.1111/j.1365-2435.2009.01639.x

Knauer AC, Bakhtiari M, Schiestl FP (2018) Crab spiders impact floral-signal evolution indirectly through removal of florivores. *Nature Communications* 9:1367. https://doi.org/10.1038/s41467-018-03792-x

Lande R, Arnold SJ (1983) The measurement of selection on correlated characters. *Evolution* 37:1210–1226. https://doi.org/10.2307/2408842

Leal LC et al. (2025) Costs of floral larceny: a meta-analytical evaluation of nectar robbing and nectar theft on animal-pollinated plants. *Ecology* 106:e70036. https://doi.org/10.1002/ecy.70036

Lucas-Barbosa D (2016) Integrating studies on plant-pollinator and plant-herbivore interactions. *Trends in Plant Science* 21:125–133. https://doi.org/10.1016/j.tplants.2015.10.013

McCall AC, Irwin RE (2006) Florivory: the intersection of pollination and herbivory. *Ecology Letters* 9:1351–1365. https://doi.org/10.1111/j.1461-0248.2006.00975.x

Page P, Favre A, Schiestl FP, Karrenberg S (2014) Do flower color and floral scent of *Silene* species affect host preference of *Hadena bicruris*, a seed-eating pollinator, under field conditions? *PLoS ONE* 9:e98755. https://doi.org/10.1371/journal.pone.0098755

Phillips PC, Arnold SJ (1989) Visualizing multivariate selection. *Evolution* 43:1209–1222. https://doi.org/10.2307/2409357

Richardson LL et al. (2015) Secondary metabolites in floral nectar reduce parasite infections in bumblebees. *Proceedings of the Royal Society B* 282:20142471. https://doi.org/10.1098/rspb.2014.2471

Rusman Q, Lucas-Barbosa D, Poelman EH (2018) Dealing with mutualists and antagonists: specificity of plant-mediated interactions between herbivores and flower visitors, and consequences for plant fitness. *Functional Ecology* 32:1022–1035. https://doi.org/10.1111/1365-2435.13035

Sasidharan R, Junker RR, Eilers EJ, Müller C (2023) Floral volatiles evoke partially similar responses in both florivores and pollinators and are correlated with non-volatile reward chemicals. *Annals of Botany* 132:1–14. https://doi.org/10.1093/aob/mcad064

Sletvold N (2019) The context dependence of pollinator-mediated selection in natural populations. *International Journal of Plant Sciences* 180:934–943. https://doi.org/10.1086/705584

Soper Gorden NL, Adler LS (2018) Consequences of multiple flower-insect interactions for subsequent plant-insect interactions and plant reproduction. *American Journal of Botany* 105:1835–1846. https://doi.org/10.1002/ajb2.1182

Stevenson PC, Nicolson SW, Wright GA (2017) Plant secondary metabolites in nectar: impacts on pollinators and ecological functions. *Functional Ecology* 31:65–75. https://doi.org/10.1111/1365-2435.12761

Strauss SY, Siemens DH, Decher MB, Mitchell-Olds T (1999) Ecological costs of plant resistance to herbivores in the currency of pollination. *Evolution* 53:1105–1113. https://doi.org/10.1111/j.1558-5646.1999.tb04525.x

Strauss SY, Whittall JB (2006) Non-pollinator agents of selection on floral traits. In: Harder LD, Barrett SCH (eds) *Ecology and Evolution of Flowers*, pp 120–138. Oxford University Press. https://doi.org/10.1093/oso/9780198570851.003.0007

Sun SG, Huang SQ (2015) Rainwater in cupulate bracts repels seed herbivores in a bumblebee-pollinated subalpine flower. *AoB PLANTS* 7:plv019. https://doi.org/10.1093/aobpla/plv019

Theis N, Adler LS (2012) Advertising to the enemy: enhanced floral fragrance increases beetle attraction and reduces plant reproduction. *Ecology* 93:430–435. https://doi.org/10.1890/11-0825.1

Wright GA et al. (2013) Caffeine in floral nectar enhances a pollinator's memory of reward. *Science* 339:1202–1204. https://doi.org/10.1126/science.1228806

Wu SM, Gao JY (2024) The conspicuously large bracts influence reproductive success in *Thunia alba* (Orchidaceae). *Journal of Plant Ecology* 17:rtad036. https://doi.org/10.1093/jpe/rtad036

Zhou J, Reynolds RJ, Zimmer EA, Dudash MR, Fenster CB (2020) Variable and sexually conflicting selection on *Silene stellata* floral traits by a putative moth pollinator selective agent. *Evolution* 74:1321–1334. https://doi.org/10.1111/evo.13965

## Acknowledgments

[Author-controlled acknowledgments to be completed before submission.]

OpenAI ChatGPT and Anthropic Claude were used during analysis and manuscript development for code-generation assistance, structured literature triage, reproducibility checks, and manuscript drafting and editing, as described in Section 4.3. AI-generated output was not treated as empirical evidence, and the authors retain responsibility for all scientific claims, citations, code, and text. The exact submitted disclosure must be confirmed by all authors.

## Statements and Declarations

### Funding

[Author confirmation required. State all funding agencies and grant numbers, or explicitly state that no funds, grants, or other support were received.]

### Competing interests

[Author confirmation required. Provide the final financial and non-financial competing-interest statement for all authors through both the manuscript and submission interface.]

### Author contributions

[Author-controlled. Complete the contribution statement after the final author list and CRediT roles are approved.]

### Data and code availability

All code, declared configurations, generated readouts, source-adjudication products, saturation receipts, and validation tests required for the fixed theory, finite sensitivity analysis, and saturated mechanism-Pattern synthesis are maintained in the associated repository. The complete Leal et al. (2025) larceny module, including its effect rows, moderator coding, context-dependence implementation, committed results, and integrity tests, is included directly in the canonical repository tree; its provenance is additionally pinned to immutable commit `ed33b25593c0d90ad6657753f6f5501d9efc7b82`. The Sasidharan et al. (2023) module uses the 32-component citation topology as its canonical dependence structure. Pattern-expansion ledgers, context programs, stopping-gate records, the Haas-Desmarais supplement receipt, and the Caruso Dryad access-state receipt are versioned with the manuscript branch. A versioned archival DOI will be added before submission.