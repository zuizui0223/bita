# From floral trait interactions to mechanism identification: a crossed-intervention framework for attraction and defence

**Authors and affiliations:** [Author-controlled; insert final publication names and affiliations before submission.]

**Corresponding author:** [Author-controlled; insert name and active e-mail address.]

**ORCID(s):** [Insert after author approval.]

## Abstract

Ecologists often detect trait interactions on fitness without knowing which ecological pathway produced them. Floral attraction and defence make this problem clear: attraction can increase pollination and antagonist exposure, whereas defence can reduce damage while impeding pollinators or imposing joint costs. A total attraction-by-defence interaction therefore does not identify its mechanism, and a positive interaction need not mean that attraction has become beneficial. We separate three nested outcome claims from the mechanism question. On a predeclared reproductive scale, a design-based interval for the total attraction-by-defence interaction lying wholly above zero identifies positive interaction relief (Level 1). Constraint release additionally requires that the attraction effect without defence is nonpositive and the attraction effect with defence is positive (Level 2); strict reversal requires a negative-to-positive change (Level 3). We define the measurable two-level interaction, \(\Delta_{AD}W=W_{11}-W_{10}-W_{01}+W_{00}\), and show that it defines an identified set of compatible antagonist-relief, pollinator-interference and joint-channel allocations. Explicit restrictions or partial channel measurements shrink this set. A crossed \(A\times D\times\) antagonist \(\times\) pollinator experiment can allocate the biotic channels when consumer interventions are selective, attraction and defence contrasts remain invariant, pollinator-independent reproduction is measured, and the four-way interaction supports channel separability. The remaining joint channel requires an independent assay rather than residual labelling. Published systems occupy complementary parts of this design. Kessler et al. (2008) supplies a manipulated attraction-by-defence-like factorial: under registered aggregate constraints, \(A_1\) is uniformly positive (approximately +0.200 to +0.240), whereas \(A_0\) remains confined to an interval spanning zero (approximately -0.030 to +0.030), and \(\Delta_{AD}\) remains positive. Exact source/design-based uncertainty and flower-restricted defence scope remain unresolved, so strict Level-2/3 release is not identified. Egan et al. (2021) supplies the complementary consumer factorial, and a public *Impatiens capensis* reanalysis reaches randomized context modification of observational traits. Across 56 route records from 25 independent biological clusters, all four constituent marginal pathways recur; this establishes recurrence, not channel identification, but none of 17 screened high-information systems combines the full allocation design and independent joint-cost assay. The outcome-level gap is therefore strict release under design-based uncertainty rather than mere interaction detection; the mechanism-level gap is the missing intersection of existing design components. This staged framework distinguishes interaction relief, functional release and cue privatization and turns the remaining gaps into concrete experiments.

**Keywords:** causal identification; factorial experiment; floral defence; floral traits; florivory; pollination; trait interaction

## 1. Introduction

Ecological interactions are often easy to detect and difficult to allocate mechanistically. A focal phenotype may affect several partners at once, those partners can have opposing effects on fitness, and the same net response can be produced by different combinations of underlying pathways. Context dependence then becomes more than statistical heterogeneity: it can reflect a change in which causal pathway dominates. This is a general difficulty for ecological inference because a measured total effect can remain informative about phenotype while being uninformative about mechanism (Catford et al. 2022).

Flowers provide a useful case. Floral colour, scent, display and reward can increase pollinator attraction, but floral signals and rewards can also expose flowers to florivores, seed predators, nectar robbers and other exploiters. Conversely, chemical or physical floral defences can reduce antagonist damage while also changing pollinator behaviour. These joint effects have long motivated work on pollinator–herbivore conflict, florivory, floral defence and multivariate selection (McCall and Irwin 2006; Strauss and Whittall 2006; Adler 2008; Kessler and Halitschke 2009; Lucas-Barbosa 2016). The broad biological point is therefore not new: attraction, defence, mutualists and antagonists can interact.

Viewed from the prior one-trait problem, a distinct defence trait is a candidate route for releasing attraction from antagonist exposure. A positive attraction-by-defence interaction means that defence improves the reproductive return to the declared attraction contrast; it does not by itself show that attraction has crossed from non-beneficial to beneficial. We therefore reserve **functional constraint release** for the stronger outcome in which attraction is nonpositive without defence but positive with defence. This turns the biological question from whether defence exists into whether the relief, interference and cost terms are jointly favorable on the same attraction-by-defence coordinate, and whether that improvement is large enough to change the sign of the attraction effect. The escape-route interpretation is thus a two-trait allocation and outcome hypothesis, not another name for the one-trait observation that a signal attracts both audiences. It is also functional rather than necessarily informational: defence may restore the reproductive return to attraction while antagonists continue to detect the same cue. It does not by itself demonstrate cue privatization or a historical shared-to-private signal transition, which belong to the separate one-trait SCH question.

A narrower inference problem remains. Suppose a study reports that an attraction trait \(A\) and a defence trait \(D\) interact on reproduction. What, exactly, has been learned? A valid same-scale interaction interval wholly above zero establishes positive interaction relief: defence makes the attraction effect more positive. It is not sufficient to establish constraint release because both attraction effects can remain negative. To test release we must also estimate the attraction effect without defence, \(A_0\), and with defence, \(A_1\). Nonpositive-to-positive release requires \(A_0\le0<A_1\), whereas strict reversal requires \(A_0<0<A_1\). None of these outcome claims is sufficient to decide why the interaction is positive. A positive \(A\times D\) interaction could arise because defence disproportionately protects the reproductive value generated by attraction. It could also arise because some additional joint benefit appears only when both traits are present. A negative interaction could arise because defence disproportionately obstructs pollinator benefits, because the two traits are jointly costly, or because another pathway has been omitted. The sign of the total interaction does not by itself allocate these possibilities.

This distinction matters because existing ecological experiments often contain only one half of the necessary design. Trait-factorial studies manipulate two floral phenotypes but leave pollinators and antagonists embedded in the same field environment. Consumer-factorial studies manipulate pollination and herbivory while floral traits remain measured rather than experimentally crossed. Both designs are valuable, but they answer different questions. Treating either as a direct estimate of a channel-resolved attraction–defence mechanism creates an identification error rather than merely a problem of low power.

Here we develop a framework around that distinction. The contribution is not a new ecological interaction type and not a mathematically elaborate theorem. It is an operational answer to six questions: **What quantity can an attraction-by-defence experiment directly estimate? When does that quantity establish interaction relief? When do the same four cells establish nonpositive-to-positive constraint release or strict reversal? Which additional interventions are required to allocate that interaction among biological channels? Which assumptions can be tested inside the experiment? And where do the closest existing studies stop along that identification sequence?**

The framework has three changes from a theorem-led approach. First, the main estimand is a discrete two-level interaction that corresponds to an actual factorial experiment rather than an abstract local derivative. Second, antagonist relief and pollinator interference are defined through crossed interventions, not inferred from marginal associations. Third, any remaining joint channel is kept unallocated until an independent cost assay gives it biological meaning. A simple sign identity then becomes useful as a diagnostic: it can constrain a hidden joint channel after the observable contrasts have been estimated, rather than being presented as the primary discovery.

We then use existing studies as identification stress tests. A rare *Nicotiana attenuata* experiment (Kessler et al. 2008) comes close to the trait side of the design by experimentally crossing floral benzylacetone and nicotine production. A woodland strawberry experiment (Egan et al. 2021) comes close to the consumer side by crossing herbivory and pollination environments. A public *Impatiens capensis* dataset (Soper Gorden and Adler 2018) allows us to test how far observational attraction and defence traits can be pushed when randomized interaction treatments are also present. These examples reveal a consistent gap: trait-interaction estimation and mechanism allocation have usually been achieved in different experiments.

We therefore use existing evidence in two empirical layers. First, the retained source-adjudicated mechanism-route synthesis asks whether the four marginal pathways required by the decomposition—attraction to pollination, attraction to antagonism, defence to antagonism, and defence to pollination—recur across independent biological systems. Second, a stricter identification-coverage audit asks whether those recurrent ingredients have been crossed on the same attraction and defence coordinates with selective consumer interventions and an independent joint-cost assay. This preserves the original Mechanism → Pattern logic while preventing marginal recurrence from being relabelled as channel identification.

## 2. The estimand: a trait interaction that can actually be measured

### 2.1 Discrete attraction-by-defence interaction and nested outcome claims

Let \(A\) be a focal floral attraction trait and \(D\) a focal flower-associated trait whose antagonist-reducing role is justified independently of the response used to test the model. For an outcome \(W\), define two experimentally meaningful levels of each trait, \(A\in\{0,1\}\) and \(D\in\{0,1\}\). The factorial interaction is

\[
\Delta_{AD}W = W_{11}-W_{10}-W_{01}+W_{00}.
\]

Define the attraction effect under low and high defence as

\[
A_0=W_{10}-W_{00},\qquad A_1=W_{11}-W_{01}.
\]

Then

\[
\Delta_{AD}W=A_1-A_0.
\]

This identity separates three nested outcome claims. **Level 1 — positive interaction relief** is \(\Delta_{AD}W>0\), meaning that defence shifts the attraction effect in a positive direction. **Level 2 — constraint release** additionally requires \(A_0\le0\) and \(A_1>0\). **Level 3 — strict reversal** requires \(A_0<0\) and \(A_1>0\). Strict reversal therefore implies constraint release, which implies positive interaction relief; the reverse implications do not hold.

The interaction is a secant contrast across the chosen trait levels. Its interpretation depends on the biological trait contrasts and outcome scale and is not invariant to arbitrary nonlinear transformations. A design-based interval for \(\Delta_{AD}W\) wholly above zero identifies Level-1 positive interaction relief. It does not by itself identify Level 2 or 3: for example, \(A_0=-0.8\) and \(A_1=-0.2\) give a strongly positive interaction while attraction remains detrimental in both defence states. With compatible uncertainty intervals, a sufficient Level-2 decision is \(\operatorname{upper}(A_0)\le0\) and \(\operatorname{lower}(A_1)>0\); Level 3 replaces the first weak inequality with a strict one. None of these outcome decisions allocates the sign among antagonist relief, pollinator interference and the remaining joint channel.

The continuous mixed partial \(\partial^2W/\partial A\partial D\) remains useful as a small-contrast limit, but it is not the primary experimental estimand here. The discrete form has two advantages: it corresponds directly to a factorial manipulation, and it makes the identification assumptions visible in the same scale on which the data are collected.

### 2.2 From non-identification to an identified set

For bookkeeping, write the reproductive outcome as

\[
W=M-G-C,
\]

where \(M\) is a mutualist-mediated contribution, \(G\) is antagonist-mediated loss, and \(C\) is a remaining direct or allocation channel. Orient the corresponding two-level channel contrasts as

\[
\rho_\Delta=-\Delta_{AD}G,\qquad
\iota_\Delta=-\Delta_{AD}M,
\]

and write \(\kappa_\Delta=\Delta_{AD}C\) as a bookkeeping coordinate whose biological interpretation still requires an independent assay. Then

\[
\Delta_{AD}W=\rho_\Delta-\iota_\Delta-\kappa_\Delta.
\]

If the observed total interaction is \(\Delta_{AD}W=\delta\), the compatible channel allocations form the identified set

\[
\mathcal I(\delta)=\{(\rho,\iota,\kappa):\rho-\iota-\kappa=\delta\}.
\]

With no additional information this is a two-dimensional plane in three-dimensional channel space. More precise measurement of the same total four-cell surface does not collapse that plane to a point; the obstacle is structural rather than sampling error. Biological restrictions or channel-specific measurements can nevertheless intersect and shrink the set, so the relevant progression is from non-identification, through partial identification, to point identification.

Positive \(\rho_\Delta\) means that defence reduces antagonist loss more strongly at high attraction than at low attraction. Positive \(\iota_\Delta\) means that defence erodes the mutualist return to attraction. The experimental problem is therefore to replace assumptions about these coordinates with contrasts that identify or bound them.

## 3. A crossed intervention design for channel identification

### 3.1 The 16-cell experiment

The minimum general design crosses four binary factors:

\[
A\times D\times E_G\times E_P,
\]

where \(E_G\) indexes antagonist access and \(E_P\) indexes pollinator access. With two levels of each factor there are 16 cells. The attraction and defence manipulations must be biologically identical across consumer states; otherwise the interaction changes coordinates as well as context.

The design is not sufficient simply because 16 cells exist. Its causal interpretation requires selective interventions. Changing antagonist access must not simultaneously change pollinator access, the attraction manipulation or the defence manipulation. Likewise, changing pollinator access must not alter antagonist exposure through the same physical barrier or chemical treatment. Broad bags, nets or insecticides often fail this requirement. Selectivity is therefore a property of the biological system and intervention, not a statistical adjustment that can be added after the experiment.

### 3.2 Antagonist relief

At a fixed pollinator state \(p\), define the fitness recovered by antagonist exclusion as

\[
R_G(A,D;p)=W(A,D,E_G=0,E_P=p)-W(A,D,E_G=1,E_P=p).
\]

If the antagonist intervention is selective, this contrast isolates antagonist-mediated loss on the chosen outcome scale. The attraction-by-defence interaction in that loss is

\[
\widehat{\rho}_{\Delta,p}=-\Delta_{AD}R_G(\cdot,\cdot;p).
\]

The important point is that a main effect of defence on damage is not \(\rho_\Delta\). The estimand asks whether the defence effect on antagonist loss itself depends on the attraction state.

### 3.3 Pollinator interference and the non-zero baseline problem

At a fixed antagonist state \(g\), define the pollinator-dependent increment

\[
J_P(A,D;g)=W(A,D,E_G=g,E_P=1)-W(A,D,E_G=g,E_P=0).
\]

The directly identified interaction in this increment is

\[
\iota_{\Delta}^{\mathrm{inc}}=-\Delta_{AD}J_P.
\]

This is not automatically the total \(\iota_\Delta=-\Delta_{AD}M_1\), because reproduction may continue when pollinators are excluded. Autonomous selfing, apomixis, resource reallocation, microclimatic effects of exclusion, or direct physical effects of \(D\) can make the pollinator-absent baseline depend on both \(A\) and \(D\). Let

\[
m_{0,\Delta}=\Delta_{AD}M_0.
\]

Then

\[
\iota_\Delta=\iota_{\Delta}^{\mathrm{inc}}-m_{0,\Delta}.
\]

A self-incompatible system may justify \(m_{0,\Delta}\approx0\) for a suitable reproductive endpoint, but zero should not be assumed merely for convenience. Otherwise \(m_{0,\Delta}\) must be estimated as part of the design.

### 3.4 The experiment tests its own separability assumption

If antagonist and pollinator channels are separable in the proposed additive representation, the antagonist-relief contrast should not depend on whether pollinators are present, and the pollinator-increment contrast should not depend on whether antagonists are present. Thus

\[
\widehat{\rho}_{\Delta,1}-\widehat{\rho}_{\Delta,0}=0
\]

and

\[
\widehat{\iota}^{\mathrm{inc}}_{\Delta,1}-\widehat{\iota}^{\mathrm{inc}}_{\Delta,0}=0.
\]

These are not two independent tests. Algebraically they are the same \(A\times D\times E_G\times E_P\) four-way interaction with opposite signs. A non-zero four-way term therefore diagnoses cross-consumer coupling on the attraction-by-defence interaction itself. In that case, forcing the data into a single \(\rho_\Delta\) and \(\iota_\Delta\) would hide a biological failure of the proposed decomposition.

In real data, separability should be evaluated with uncertainty-aware contrasts or equivalence bounds rather than by accepting a null-hypothesis test. The deterministic implementation in the accompanying code uses a numerical tolerance only for simulation and regression testing.

### 3.5 Joint cost must be measured independently

Once \(\rho_\Delta\), \(\iota_\Delta\) and the full-context \(\Delta_{AD}W\) are available, one can calculate

\[
U_\Delta=\rho_\Delta-\iota_\Delta-\Delta_{AD}W.
\]

The symbol \(U_\Delta\) is deliberate. This residual is not automatically a joint construction or allocation cost. Imperfect exclusion, baseline misspecification, omitted pathways, scale mismatch and failure of additivity can all enter it.

The cost channel therefore requires a separate \(A\times D\) assay under conditions that suppress or standardize pollinator- and antagonist-mediated effects. Depending on the biological system, suitable endpoints could include construction cost, carbon or nitrogen allocation, floral longevity, reward production, secondary-metabolite production, biomass, or reproduction under standardized hand pollination and controlled antagonist exposure. The key requirement is independence from the residual definition.

Let the independently measured cost interaction be

\[
\kappa_\Delta=\Delta_{AD}C_{\mathrm{assay}}.
\]

Sign agreement between \(U_\Delta\) and \(\kappa_\Delta\) supports the intended channel allocation. Magnitude agreement requires the assay and reproductive outcome to be placed on a defensibly common scale. Disagreement is informative: it points to a missing channel, a non-selective intervention, or an inadequate cost assay rather than being silently absorbed into \(\kappa\).

### 3.6 Partial identification before point identification

The same accounting identity is useful before all channel terms have been measured. Rearranging gives

\[
\rho_\Delta-\iota_\Delta=\Delta_{AD}W+\kappa_\Delta.
\]

Thus any defensible bound on the remaining joint-cost channel maps directly to a bound on the biotic balance. In particular,

\[
\kappa_\Delta\ge0
\quad\Longrightarrow\quad
\rho_\Delta-\iota_\Delta\ge\Delta_{AD}W.
\]

If complementarity is observed, \(\Delta_{AD}W>0\), this restriction forces antagonist relief to exceed pollinator interference by at least the observed total interaction on the declared scale, even though \(\rho_\Delta\) and \(\iota_\Delta\) can remain individually unidentified. This is the useful interpretation of the earlier one-sided relation: a sharp partial-identification bound under an explicit restriction, not a standalone prediction theorem.

Additional measurements shrink the identified set. A bounded independent cost assay narrows \(\rho_\Delta-\iota_\Delta\); a selective estimate of either consumer channel narrows the remaining coordinates; and the crossed intervention design, after baseline correction and a successful separability check, point-identifies the two biotic channels. Once those channels are measured, the identity also provides a diagnostic in the opposite direction: if \(\Delta_{AD}W>0\) but \(\rho_\Delta\le\iota_\Delta\), the still-unallocated joint channel required by the data must be negative. Calling that channel \(\kappa_\Delta\) still requires the independent assay.

The explanatory reach is therefore ordered by method. Route synthesis establishes that the constituent biology recurs; a same-scale \(A\times D\) factorial estimates \(A_0\), \(A_1\) and the total interaction and can distinguish interaction relief from stronger release claims when compatible uncertainty is available; identified-set algebra enumerates the mechanisms compatible with the total; explicit restrictions or channel observations provide partial identification; and only selective crossed consumer interventions plus baseline and separability checks allocate the biotic channels. An independent assay is still required before the remaining residual is named as joint cost. The present evidence reaches constituent recurrence, a strong aggregate Level-1 anchor with partial identification of \(A_0\) and \(A_1\), several partial trait- or consumer-factorial anchors, and a fragmented identification frontier. It does not reach strict Level-2/3 release with source/design uncertainty or full channel allocation in any screened system. Thus the contribution is not a claim that BITA recovered the realized mechanism, but a precise account of **which method explains which part of the question, where current evidence stops, and what smallest augmentation moves it further**.

## 4. From mechanism to pattern: recurrence before identification

### 4.1 Constituent ecological channels recur across systems

The identification problem would be biologically uninteresting if the proposed channels were peculiar to a single model system. The retained source-adjudicated mechanism-route synthesis instead contains 56 directional route records from 25 independent biological study clusters. Coverage includes attraction → pollination in 5 clusters, attraction → antagonism in 8, defence → antagonism in 18, and defence → pollination in 10. Fourteen clusters contain more than one route in the same biological system, and 17 show context- or state-dependent switching. These categories overlap: route counts are not additive independent-study totals, and none of these counts is an estimate of natural prevalence.

The conclusion is deliberately limited. The constituent ecological ingredients required by the channel decomposition recur across systems, so the framework is not built around one exceptional case. But marginal route recurrence does not estimate \(\Delta_{AD}W\), \(\rho_\Delta\), \(\iota_\Delta\), or \(\kappa_\Delta\). The Mechanism → Pattern bridge is therefore two-stage: first establish recurrence of the biological channels; then ask whether any existing experiment jointly identifies their allocation on the same attraction-by-defence contrast.

### 4.2 Identification-coverage audit

We reclassified a high-information set of published floral systems according to the experimental information required above. The screen was designed to expose distinct design classes, not to estimate their prevalence in the literature. For each study we asked whether \(A\) and \(D\) were distinct and biologically justified, whether they were manipulated or observed, whether a shared \(A\times D\) outcome was available, whether antagonist and pollinator interventions were crossed with the trait states, whether the pollinator-absent baseline could be characterized, and whether a joint-cost assay existed.

Seventeen high-information systems were retained. None reaches the full sequence from trait interaction to channel allocation and independent joint-cost measurement, but this is more informative than a binary 0-of-17 result. The studies occupy complementary lower-dimensional faces of the target \(A\times D\times E_G\times E_P\) architecture. Kessler et al. (2008) supplies the strongest direct \(A\times D\)-like trait face; Theis and Adler (2012) supplies a manipulated attraction \(\times\) beetle-removal \(\times\) pollination-supplementation bridge; Santangelo et al. (2019) supplies a defence \(\times\) herbivore-suppression \(\times\) hand-pollination backbone with observed floral traits; Egan et al. (2021) supplies the consumer-factorial face; Soper Gorden and Adler (2018) supplies observational A/D coordinates under randomized context modification; and Sun and Huang (2015) supplies a selective flower-associated defence mechanism. These are structural faces, not equivalent treatments: in particular, supplemental hand pollination is not a selective pollinator-access toggle. The empirical pattern is therefore a **fragmented identification frontier**. Existing studies contain different pieces of the information needed to shrink \(\mathcal I(\delta)\), but no screened system closes all dimensions of the allocation problem.

This reframes the practical question for each near miss. Rather than asking only whether a study fully identifies the mechanism, we ask which smallest additional intervention or measurement would most reduce its remaining identified set. The following systems make those missing dimensions concrete.

### 4.3 A trait-factorial anchor: Kessler et al. 2008

Kessler et al. (2008) generated four transformed *Nicotiana attenuata* states by independently blocking the dominant floral attractant benzylacetone and nicotine production. The resulting combinations correspond closely to an attraction-by-defence-like factorial: benzylacetone has a direct floral-attraction role, whereas nectar nicotine alters visitor behaviour and is associated with reduced nectar robbing and florivory. The main caveat is that nicotine biosynthesis was silenced systemically rather than only in flowers.

For female outcrossing, the study used antherectomized flowers, making capsule maturation dependent on cross-pollination. Published aggregate constraints include 474 informative flowers, 87 capsules, a benzylacetone-plus-nicotine capsule fraction near 35%, and the remaining three states near 12–14%. Enumerating integer cell allocations compatible with these aggregate constraints across four registered denominator-balance profiles yields

\[
A_0=p_{10}-p_{00}\in[-0.02993,+0.02993],
\]

\[
A_1=p_{11}-p_{01}\in[+0.20013,+0.23984],
\]

with a minimum probability-scale \(\Delta_{AD}W\) of +0.17102. Thus the attraction effect with defence is positive under every compatible allocation, whereas the attraction effect without defence remains narrowly zero-compatible. The broad stress test also preserves a positive total-interaction sign, with minimum naive probability-scale \(z\approx2.296\), but the auxiliary logit 95% interval can cross zero and the exact genotype-by-day denominators, plant dependence and source uncertainty model remain unrecovered.

Kessler is therefore the strongest historical Level-1 positive-interaction anchor and now provides an asymmetric partial-identification result: \(A_1\) is sign-identified positive under the declared aggregate restrictions, but \(A_0\) is not. It does **not** identify Level-2 constraint release or Level-3 strict reversal, because compatible allocations exist with \(A_0>0\). Nor is the aggregate enumeration a substitute for source/design-based confidence intervals. The approximately three-percentage-point upper width of the \(A_0\) set is an identified-set width, not a retrospectively chosen equivalence margin. Systemic nicotine manipulation adds a separate intervention-scope caveat.

This study therefore changes the empirical premise in an important way. Direct attraction-by-defence-like trait factorials are not wholly absent, and the historical aggregate data constrain more than the sign of \(\Delta_{AD}W\). What remains absent here is strict release with source/design uncertainty and mechanism allocation: pollinator visitation, robbing and florivory are measured consequences of the trait states rather than independently crossed consumer interventions. Thus the outcome surface is approached much more closely than \(\rho_\Delta\), \(\iota_\Delta\), \(m_{0,\Delta}\), the four-way separability diagnostic, or \(\kappa_\Delta\).

### 4.4 A consumer-factorial counterpart: Egan et al. 2021

Egan et al. (2021) provides the complementary design half. In *Fragaria vesca*, herbivory and pollination environment were crossed experimentally, and the experiment quantified how these agents altered selection on attraction- and defence-related traits. This is precisely the kind of consumer manipulation that trait-factorial studies often lack.

However, the focal traits were measured rather than independently manipulated as an \(A\times D\) factorial, and several defence-related metabolites were leaf-derived rather than flower-specific. The study therefore identifies context-dependent selection under a consumer factorial, not the channel decomposition of a manipulated floral attraction-by-defence interaction.

Together, Kessler et al. (2008) and Egan et al. (2021) illustrate the identification gap more clearly than a general literature count. One contains much of the trait factorial and lacks the crossed consumer intervention; the other contains much of the consumer factorial and lacks the crossed trait manipulation. The missing object is their intersection.

### 4.5 Public-data retrofit: Soper Gorden and Adler 2018

The public *Impatiens capensis* dataset of Soper Gorden and Adler (2018) provides a different test. Early-season flower redness and floral condensed tannins were measured on the same plants, and previous work in the same system supports a floral-defence role for condensed tannins. The experiment also randomized supplemental robbing, florivory and pollination treatments.

Earlier analyses estimated observational \(A\times D\) terms on two reproductive components, but both were imprecise. We therefore fit a stricter hierarchical retrofit asking whether the observational \(A\times D\) association itself changed under each randomized interaction treatment. The model retained the complete randomized robbing-by-florivory-by-pollination factorial, the lower-order trait-by-treatment terms needed for hierarchy, the three targeted \(A\times D\times\)treatment modifiers, and a pre-treatment phenology covariate. HC3 intervals were used.

For chasmogamous fruits per plant per day (\(n=170\)), the fitted \(A\times D\) coefficient was -0.1628 (95% CI -0.3675 to +0.0419). The \(A\times D\) modifiers for robbing, florivory and pollination were -0.0434, -0.3078 and +0.0748 respectively, and all three intervals included zero. For seeds per chasmogamous fruit (\(n=85\)), the fitted \(A\times D\) coefficient was -0.0936 (95% CI -0.6643 to +0.4771); again, all three treatment-modification intervals included zero.

The reanalysis is useful because it shows exactly how far a rich public dataset can be pushed without changing the estimand by rhetoric. It reaches an observational trait interaction plus randomized modification of that interaction. It does not reach the channel estimands because the traits themselves were not randomized and the interaction treatments increased robbing, florivory or pollination rather than selectively toggling consumer presence and absence.

### 4.6 Complementary experimental faces

Theis and Adler (2012) adds a distinct structural face. Enhanced floral fragrance was crossed with repeated beetle removal and supplemental hand pollination on female reproduction, creating an attraction \(\times\) antagonist-removal \(\times\) pollination-supplementation backbone. This is substantially closer to the target architecture than a trait-only experiment, but it is not channel identification: the study lacks an independently manipulated defence coordinate, and supplemental hand pollination adds pollen rather than creating pollinator absence/presence. It therefore cannot identify the target pollinator increment or \(m_{0,\Delta}\).

Other systems isolate additional missing axes. Kessler et al. (2015) crossed floral scent and nectar production, but nectar is a reward axis rather than an independently justified antagonist-reducing defence trait. In *Pedicularis rex*, Sun and Huang (2015) manipulated a water-holding bract barrier that strongly affected seed predation without a detected effect on legitimate pollinator or nectar-robber visitation, but no independent attraction manipulation was present. Santangelo et al. (2019) provides a defence-by-herbivore-suppression-by-hand-pollination backbone, but its defence axis is whole-plant HCN rather than a strict flower-associated \(D\), and hand pollination again is not selective pollinator access.

Across the 17 screened systems, failure modes therefore differ—missing trait interactions, missing consumer factorials, invalid floral coordinates, missing attraction manipulation, missing pollinator-absent baseline characterization, or missing independent cost measurement—but no system closes the full allocation design or includes an independent attraction-by-defence joint-cost assay.

## 5. Designing an identifiable experiment

### 5.1 Choose the biological system before choosing the exclusion device

The main design difficulty is intervention selectivity, not the number of cells. Generic bags or broad pesticides can alter pollinators, antagonists and plant physiology simultaneously, destroying the channel interpretation. Candidate systems should instead exploit natural asymmetries such as body size, access route, diel activity or phenology. *Pedicularis rex* illustrates the useful logic: a consumer-specific access mechanism can first supply a selective defence manipulation, then an independent attraction manipulation and selective consumer toggles can be crossed onto that backbone.

### 5.2 Analysis sequence

Analysis should be staged rather than forcing the outcome and mechanism questions into one initial design. First, a four-cell \(A\times D\) experiment estimates \(A_0\), \(A_1\) and \(\Delta_{AD}W\) with design-based uncertainty. A positive \(\Delta_{AD}\) interval establishes Level-1 interaction relief; Level 2 additionally requires a nonpositive \(A_0\) interval bound and positive \(A_1\), and Level 3 requires a strictly negative \(A_0\) bound and positive \(A_1\). Second, channel pilots on the same trait coordinates estimate plausible effect sizes and variances for antagonist relief, pollinator interference, the pollinator-absent baseline and the four-way coupling contrast. Third, the selective 16-cell experiment is re-powered from those channel-scale quantities and paired with an independent joint-channel assay.

This hierarchy also changes prospective power planning. A design powered for \(\Delta_{AD}>0\) is not automatically powered for Level 2 or 3. If the true \(A_0\) lies exactly at zero, the probability that a two-sided 95% interval has its upper endpoint at or below zero approaches only \(\alpha/2=0.025\), regardless of how large the sample becomes. Under prospective sensitivity calculations with \(A_1=+0.22\), a weakly negative \(A_0=-0.03\) requires roughly 1,772 effective observations per cell for 80% joint Level-2/3 decision probability; with a design effect of 1.5 and 90% retention this becomes about 2,954 observations per cell, or 11,816 across the four cells. These are planning sensitivities rather than historical-effect claims. They show that strict release near the zero boundary is a precision problem distinct from detecting a positive interaction, and they rule out selecting a post-hoc tolerance merely because the historical \(A_0\) identified set is narrow.

Within the full design, analysis follows the causal contrasts. Estimate \(\Delta_{AD}W\) within consumer states, form antagonist-exclusion and pollinator-increment contrasts with propagated uncertainty, estimate or justify \(m_{0,\Delta}\), and then test the single \(A\times D\times E_G\times E_P\) four-way separability contrast. Only after these gates should the remaining joint channel be compared with the independent cost assay. The sampling model can be generalized, permutation-based or randomization-based; the required invariant is the contrast structure and its biological interpretation.

### 5.3 What counts as a successful outcome

The experiment is informative regardless of which outcome level is reached. A \(\Delta_{AD}\) interval wholly above zero identifies Level-1 interaction relief, one wholly below zero refutes positive relief for the declared contrast, and an interval crossing zero leaves Level 1 unresolved. If Level 1 is positive, \(A_0\) and \(A_1\) then distinguish improvement from release: \(\operatorname{upper}(A_0)\le0\) with \(\operatorname{lower}(A_1)>0\) identifies Level-2 constraint release, and \(\operatorname{upper}(A_0)<0\) with \(\operatorname{lower}(A_1)>0\) identifies Level-3 strict reversal. A positive \(A_1\) with zero-compatible \(A_0\) is a partial-identification result, not a failed experiment and not strict release. None of those states alone allocates the mechanism. Near-zero four-way coupling plus residual–assay agreement supports the proposed decomposition. Non-zero four-way coupling rejects separability. Residual–assay disagreement exposes a missing channel, intervention failure or scale mismatch. Finally, complementarity with \(\rho_\Delta\le\iota_\Delta\) forces a negative remaining joint channel on the chosen scale. Each outcome therefore resolves a different part of the identification problem rather than being labelled a failed experiment.

### 5.4 Computational and AI-assisted workflow transparency

OpenAI ChatGPT and Anthropic Claude were used for code-generation assistance, structured literature triage, reproducibility checks, and manuscript drafting/editing. AI-generated output was not treated as empirical evidence, and these tools did not determine study inclusion, evidence classification, or statistical conclusions. Source claims, numerical results, code, and citations were checked against the underlying analyses and sources. The authors retain responsibility for all scientific decisions and content.


## 6. Discussion

### 6.1 Constituent mechanisms recur; mechanism allocation remains missing

The strongest conclusion from the reanalysis and coverage audit is narrower and more useful than the claim that attraction–defence biology is understudied. The retained route synthesis shows that the four constituent marginal pathways recur across 25 independent biological clusters, including same-system and context-switching architectures. Ecologists also manipulate floral traits, pollination and antagonists in sophisticated experiments. Kessler et al. (2008) shows that a direct attraction-by-defence-like trait factorial can be built in the field, whereas Egan et al. (2021) shows that pollination and herbivory can be crossed to estimate context-dependent selection. What remains rare in the screened evidence is the intersection of these recurrent biological channels and these experimental design components on the same trait coordinates and outcome scale.

This distinction matters because adding more studies of marginal pathways will not solve the same problem. Evidence that attraction affects pollination, attraction affects antagonists, defence affects antagonists and defence affects pollinators demonstrates biological plausibility. It does not determine the cross-trait interaction in those channels. Likewise, observing a total \(A\times D\) interaction does not determine how much of it came from each pathway. The missing information is structural.

### 6.2 Why the algebra should be modest

The relation among \(\Delta_{AD}W\), antagonist relief, pollinator interference and a joint channel is bookkeeping, not a mathematical novelty claim. Its value is that it defines what can and cannot be learned at different information levels. A total interaction with design-based uncertainty decides Level-1 interaction relief when its interval excludes zero, but the total alone neither establishes strict release nor collapses the plane of compatible channel allocations. \(A_0\) and \(A_1\) provide the additional outcome information required for Levels 2 and 3, while an explicit restriction on \(\kappa_\Delta\) partially identifies the biotic balance \(\rho_\Delta-\iota_\Delta\). Selective consumer interventions shrink the mechanism set further, and the crossed design can point-identify the biotic channels when its causal gates pass.

This interpretation also recovers the useful content of the earlier one-sided inequality without overstating it. Under \(\kappa_\Delta\ge0\), a positive total interaction implies a positive biotic balance and, more sharply, \(\rho_\Delta-\iota_\Delta\ge\Delta_{AD}W\). The statement is strong only to the extent that the cost restriction is biologically supported. An independent cost assay therefore does more than label a residual: it can convert a qualitative assumption into an empirically bounded identified set.

The broader methodological point is that ecological mechanism inference need not jump directly from non-identification to an expensive fully crossed experiment. Intermediate information can be scientifically useful when its assumptions are explicit and its effect is stated as an interaction decision, a release decision, or a bound rather than an unsupported point allocation.

### 6.3 Beyond flowers

The same inference problem occurs whenever a phenotype affects several opposing ecological pathways. A dispersal trait can improve colonization while weakening local retention; a defence trait can reduce predation while lowering competitive performance; habitat structure can facilitate one interaction while obstructing another. In each case, a net interaction between traits can be estimated before its mechanism is identified.

The transferable principle is not the floral notation. It is the sequence: define a measurable interaction, distinguish interaction relief from an actual change in the sign of the focal trait effect, show which channel allocation is not identified from that interaction, design selective interventions for the missing contrasts, test whether the channels are separable, and independently measure any residual mechanism before naming it. Different systems will require different interventions and may fail the separability test for biologically interesting reasons.

### 6.4 Limits

The framework is intentionally demanding. A 16-cell design may be expensive, consumer exclusion may be imperfect, and high-order interactions require substantial replication. The discrete estimand also depends on the chosen trait levels and outcome scale. These are not incidental technicalities; they define the scope of the causal statement. The staged design reduces but does not eliminate this burden: the initial four-cell outcome experiment and later mechanism experiment answer different questions and must be powered on their own effect scales. Even within the four-cell experiment, Level-1 interaction power and Level-2/3 release power can differ by an order of magnitude when \(A_0\) is near zero.

The current empirical audit is likewise a high-information design audit rather than a systematic estimate of how often each design class occurs in the literature. The 17 systems were selected because they are close to the identification target or expose informative failure modes. Their face counts describe screened-set evidence capacity, not literature prevalence. A future systematic review could quantify design prevalence, but such a count is not needed to demonstrate the logical distinction among total interaction, consumer-context modification and channel identification.

The marginal attraction routes also define a separate, simpler estimand that this paper does not test. For one attraction contrast, the general identity is \(\Delta_AW=\Delta_AM-\Delta_AG-\Delta_AC\); if direct attraction cost is standardized or measured independently, the biotic target can be written \(S_A=\Delta_AM-\Delta_AG\). The contrasts \(\Delta_AM\) and \(\Delta_AG\) can be estimated separately under a weaker design that measures or intervenes on both channels on the same \(A\) coordinate, without a second trait \(D\), an \(A\times D\) interaction, or the full crossed design developed here. Selective consumer intervention is one route to causal channel estimates, not a requirement for an initial coverage screen. The five attraction-to-pollination and eight attraction-to-antagonism clusters are therefore constituent evidence for the present decomposition, not an evaluation of the one-trait shared-cue hypothesis now developed separately in SCH. Treating the targets separately avoids interpreting failure to identify cross-trait channel allocation as failure of the simpler first-order question, while retaining the requirement that total \(W(A)\) alone does not allocate its channels.

The two repositories also describe different forms of relief from conflict. SCH's private or modularized cue architecture is an informational escape from one shared coordinate. BITA Level 1, \(\Delta_{AD}W>0\), is functional **interaction relief**: defence improves the marginal return to attraction and can occur while attraction remains detrimental. BITA Level 2 is the stronger functional constraint-release statement because attraction changes from non-beneficial without defence to beneficial with defence; Level 3 is strict negative-to-positive reversal. None of these outcome levels by itself demonstrates cue privatization, historical branching or disappearance of the original one-trait receiver overlap.

Finally, an independent cost assay may not be commensurate in magnitude with reproductive fitness. In that case its strongest use is sign and mechanistic validation rather than numerical closure of the accounting identity.

## 7. Conclusions

A floral attraction-by-defence interaction can be measured without its mechanism being point-identified, and a positive interaction should not be conflated with complete release of the underlying attraction conflict. A valid same-scale interval for the total interaction lying wholly above zero identifies Level-1 positive interaction relief on the declared reproductive scale. The same four cells identify Level-2 constraint release only when the attraction effect without defence is nonpositive and the attraction effect with defence is positive, and Level-3 strict reversal only when the former is strictly negative. A total interaction defines an identified set of compatible channel allocations; biologically justified restrictions or partial channel measurements can shrink that set; and a crossed attraction-by-defence-by-antagonist-by-pollinator experiment can point-identify the consumer-mediated contrasts when selective intervention, baseline and separability requirements are met. An independent cost assay then constrains whether the remaining joint channel can be interpreted as joint cost.

The four constituent ecological pathway families recur across independent systems, while the 17-system high-information audit shows that complementary experimental faces already exist but largely in different studies: a direct trait factorial, an attraction-by-antagonist-removal-by-pollination-supplementation bridge, a consumer factorial, a selective floral defence manipulation and a linked public-data panel. The empirical gap is therefore not absence of relevant biology but fragmentation of the information needed to allocate a joint interaction and to establish the strongest outcome claim. This also makes the next experiment study-specific: first estimate \(A_0\), \(A_1\) and \(\Delta_{AD}\) with compatible uncertainty, then add the measurement or intervention that most reduces the remaining identified set rather than simply collecting another marginal association.

At the outcome level, Kessler et al. (2008) supplies a manipulated positive aggregate-sign anchor and, under the registered aggregate restrictions, a sign-identified positive defended attraction effect \(A_1\). The undefended attraction effect \(A_0\) remains confined to approximately -0.030 to +0.030, exact source/design-based uncertainty is unavailable, and systemic nicotine suppression leaves the focal defence scope imperfectly bounded. Current complete-system evidence therefore supports strong Level-1 and asymmetric partial identification but not strict Level-2 constraint release or Level-3 reversal. This does **not** mean that \(\rho_\Delta\), \(\iota_\Delta\) and \(\kappa_\Delta\) must first be point-identified: a valid positive total interval would decide Level 1, and compatible \(A_0/A_1\) intervals would decide Levels 2/3 independently of mechanism allocation. At the mechanism level, flower-associated defences repeatedly reduce antagonist access or use, pollinator-preserving guarded states recur, and access geometry distinguishes selective, interfering and bypassable systems, but no screened system allocates all three channels. Neither result establishes informational escape or cue privatization.

The resulting framework closes the established sequence **interaction detection → outcome-level partial/stronger identification → mechanism identification**. It moves floral attraction-defence research from detecting non-additivity and cataloguing recurrent pathways to stating exactly what current evidence constrains, what remains unidentified, and which additional observation would resolve it.

## Open Research statement

Analysis code, identification estimands, source-audit products, the *Impatiens* public-data retrofit, and identification-coverage tables are maintained in the public project repository for peer review. A permanent archive of the accepted code and data-derived outputs will be created at the acceptance stage.

## Author contributions, funding, acknowledgments and competing interests

[Author-controlled; complete before submission.]

## References

The reference list will be reconciled against the existing canonical bibliography after the identification-design text is frozen. Core sources cited in this draft include Adler (2008), Catford et al. (2022), Egan et al. (2021), Kessler and Halitschke (2009), Kessler et al. (2008, 2015), Lucas-Barbosa (2016), McCall and Irwin (2006), Soper Gorden and Adler (2018), Strauss and Whittall (2006), Sun and Huang (2015), and Theis and Adler (2012).
