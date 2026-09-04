# When does a trait trade-off resolve by differentiation rather than compromise? Linking trait architecture to mechanism identification

**Working integrated Chapter 2 draft — not yet the canonical submission source.**

**Authors and affiliations:** [Author-controlled]

**Corresponding author:** [Author-controlled]

## Abstract

A multifunctional trait can be pulled toward different phenotypic states by different functions. One evolutionary solution is compromise: the same trait remains shared and settles at a state that is suboptimal for each function considered separately. Another is differentiation: functions become partitioned across partly independent trait axes. General theory has long shown that functional trade-offs can favour specialization, but connecting that idea to measurable ecological conflicts remains difficult because structural separation need not imply functional independence and because a successful multi-trait phenotype does not reveal which ecological pathway generated its advantage. We formulate this transition as an explicit architecture comparison. In a quadratic baseline, two functions with preferred states \(\theta_1\) and \(\theta_2\) share one trait \(z\), or are expressed through two traits \(x\) and \(y\) subject to residual coupling \(\lambda\) and an additional architecture cost \(K\). The shared architecture loses \(L_S^*=w_1w_2(\theta_1-\theta_2)^2/(w_1+w_2)\) relative to separate function-specific optima. Differentiation retains only a fraction \(s=w_1w_2/[w_1w_2+\lambda(w_1+w_2)]\) of the possible phenotypic separation, and this same fraction is the proportion of shared-axis conflict loss that can be recovered. Thus \(\Delta_{arch}=sL_S^*-K\): differentiation is favoured when recovered compromise loss exceeds the extra cost of a differentiated architecture. A registered 300-condition robustness grid spanning convex power-loss shapes, asymmetric functional weights, optimum distances and residual coupling preserves the qualitative result: recoverable loss is positive in all 300 nonzero-conflict evaluations, increases with optimum separation in 60/60 declared series, and never increases with residual coupling in 60/60 series. Empirical systems illustrate both sides of the model. Structurally separate oral and pharyngeal jaws in cichlids relax a feeding trade-off yet retain evolutionary and genetic integration, whereas *Dalechampia* shows repeated historical redeployment and addition of functional structures. We then use floral attraction and defence as a mechanistic worked case showing that, once multiple trait axes exist, their total interaction still does not identify why the conflict is relieved. Existing floral evidence contains the required pathways but distributes the necessary identification dimensions across different experiments. The resulting framework links shared-trait balance, incomplete trait differentiation and causal mechanism identification without equating structural modularity with evolutionary independence.

**Keywords:** functional trade-off; multifunctionality; trait differentiation; modularity; specialization; causal identification; ecological interactions

## 1. Introduction

Traits are rarely built for a single consequence. A morphological, chemical or behavioural coordinate can contribute simultaneously to several functions, and those functions need not favour the same phenotype. Such multifunctionality creates a basic architectural problem: should one trait continue to serve several demands, accepting a compromise among them, or should the functions become more separable across multiple traits? The first solution preserves integration. The second creates division of labour within the phenotype.

The compromise side of this problem is increasingly explicit in trait ecology. A multifunctional trait can be far from the optimum for any one function because its realized value reflects the combined fitness contributions of several functions and environments (Sack and Buckley 2020). The same logic appears in ecological conflicts in which one phenotype benefits one interaction while worsening another. Floral signals provide a familiar example: colour, scent, display and reward can attract pollinators while simultaneously altering exposure to florivores, seed predators, nectar robbers or other exploiters. But this is only one realization of a broader problem. A single feeding apparatus can face incompatible mechanical demands, a single gene product can contribute to competing functions, and a single structure can be constrained by several performance optima.

The alternative to compromise is not a new idea. Theory on functional specialization, division of labour, modularity and evolving pleiotropy has established that multiple modules can specialize when trade-offs are sufficiently strong and when specialization is not offset by redundancy, robustness or other costs (Rüffler et al. 2012; Guillaume and Otto 2012). Consequently, the novelty of a new trait-differentiation framework cannot be the statement that trade-offs sometimes favour specialization. The more useful unresolved problem is empirical and inferential: how can a measured one-trait ecological compromise be connected to a multi-trait architecture, how much of the original conflict is actually released when the new traits remain partly coupled, and how can the ecological mechanism of that release be identified?

This distinction matters because having two structures is not equivalent to having two independent functions. Cichlid fishes illustrate the point unusually clearly. Oral and pharyngeal jaws structurally separate prey capture and prey processing and can permit trait combinations that would be constrained in a single jaw system (Burress et al. 2020). Yet the two systems can remain evolutionarily and genetically integrated (Conith and Albertson 2021). Differentiation is therefore naturally continuous: new axes may relax a conflict without making each function private to one axis. Historical trait evolution is similarly more complicated than simple splitting. In *Dalechampia*, pollination rewards and defensive functions have repeatedly been redeployed among structures and new lines of defence have accumulated through adaptation and exaptation (Armbruster et al. 2009). Real architectures can be partly decoupled, repeatedly reassigned and historically contingent.

We use these observations to frame a two-stage problem. The first stage asks an architecture question: **when does the best differentiated phenotype outperform the best one-trait compromise?** The second asks an identification question: **once several trait axes exist, what ecological mechanism produces their joint fitness effect?** These are logically distinct. An architecture can be favoured because it releases one constraint while simultaneously creating another. Likewise, a positive interaction between two traits can indicate that one trait improves the return to the other without identifying whether that improvement arose through protection from an antagonist, improved access to a mutualist, a direct construction benefit, or some unmeasured pathway.

Our contribution is therefore a bridge rather than a claim of theoretical priority. First, we write the shared-versus-differentiated architecture comparison on explicit trait coordinates and derive a transparent quadratic result. The key quantity is the fitness loss generated by forcing conflicting functional optima onto one axis. Residual coupling determines what fraction of that loss can be recovered after differentiation; an additional architecture cost determines whether the recovered amount is enough to make differentiation worthwhile. Second, we test whether this qualitative boundary depends on quadratic response shapes using a preregistered finite family of convex power-loss models. Third, we connect the architecture result to the existing BITA mechanism-identification framework. Floral attraction and defence become a worked ecological case in which multiple trait axes affect mutualists, antagonists and fitness, allowing us to ask what existing experiments can and cannot identify.

The resulting paper is organized around the sequence **balance → differentiation → identification**. Section 2 defines the shared and differentiated architectures and derives the architecture-gain boundary. Section 3 tests response-shape robustness. Section 4 shows why structural differentiation can remain incomplete and places cichlid and *Dalechampia* evidence against the model. Section 5 uses the floral two-trait system to show why an apparently successful differentiated architecture still requires mechanism-resolving interventions. Section 6 integrates the evolutionary and inferential implications.

## 2. From shared-trait compromise to differentiated architecture

### 2.1 Shared-axis architecture

Let one trait coordinate \(z\) contribute to two functions whose preferred states are \(\theta_1\) and \(\theta_2\). Let \(w_1>0\) and \(w_2>0\) scale the fitness importance or curvature of each functional demand. In the quadratic baseline, the loss relative to simultaneously occupying both function-specific optima is

\[
L_S(z)=w_1(z-\theta_1)^2+w_2(z-\theta_2)^2.
\]

Equivalently, normalized fitness is \(W_S(z)=-L_S(z)\). The best shared phenotype is

\[
z^*=\frac{w_1\theta_1+w_2\theta_2}{w_1+w_2},
\]

with minimum unavoidable conflict loss

\[
L_S^*=\frac{w_1w_2}{w_1+w_2}(\theta_1-\theta_2)^2.
\]

This quantity formalizes the compromise problem. If the functional optima coincide, \(L_S^*=0\) and there is no loss to recover by splitting the axis. If the optima diverge, the best shared phenotype lies between them and the cost of integration increases quadratically with their distance.

The interpretation is deliberately broader than any one biological system. \(\theta_1-\theta_2\) may represent incompatible mechanical requirements, different ecological audiences, conflicting physiological functions or any other case in which the same measured coordinate is pulled toward different states.

### 2.2 Differentiated architecture with residual cross-talk

Now allow two trait coordinates, \(x\) and \(y\). Trait \(x\) can approach the preferred state of function 1 and trait \(y\) the preferred state of function 2, but the axes need not be fully independent. We represent remaining functional, developmental or coordination coupling by \(\lambda\ge0\) and a fixed additional cost of maintaining the differentiated architecture by \(K\ge0\):

\[
L_D(x,y)=w_1(x-\theta_1)^2+w_2(y-\theta_2)^2+\lambda(x-y)^2+K.
\]

The first two terms reward function-specific specialization. The coupling term penalizes separation. The fixed term captures any extra developmental, energetic, regulatory or maintenance burden that is not already represented by continuous displacement losses.

Let

\[
D=w_1w_2+\lambda(w_1+w_2).
\]

Then the differentiated optimum is

\[
x^*=\frac{w_1w_2\theta_1+w_1\lambda\theta_1+w_2\lambda\theta_2}{D},
\]

\[
y^*=\frac{w_1w_2\theta_2+w_1\lambda\theta_1+w_2\lambda\theta_2}{D}.
\]

The residual loss before paying \(K\) is

\[
L_{D,0}^*=\frac{w_1w_2\lambda}{D}(\theta_1-\theta_2)^2.
\]

When \(\lambda=0\), the functions can be completely decoupled and the optima are recovered exactly: \(x^*=\theta_1\) and \(y^*=\theta_2\). As \(\lambda\) becomes large, the two traits are increasingly forced to move together and the differentiated optimum approaches the shared compromise.

### 2.3 Decoupling fraction and the amount of compromise that can be recovered

The optimized separation between the two differentiated trait coordinates is

\[
|x^*-y^*|
=
\frac{w_1w_2}{D}|\theta_1-\theta_2|.
\]

Define the **decoupling fraction**

\[
s
=
\frac{|x^*-y^*|}{|\theta_1-\theta_2|}
=
\frac{w_1w_2}{w_1w_2+\lambda(w_1+w_2)},
\]

for \(\theta_1\ne\theta_2\). This quantity ranges from 1 under complete functional decoupling toward 0 under arbitrarily strong residual coupling.

A useful identity follows. The amount of shared-axis conflict loss recovered by the differentiated architecture before paying its fixed cost is

\[
R=L_S^*-L_{D,0}^*.
\]

Substitution gives

\[
R
=
\frac{w_1^2w_2^2(\theta_1-\theta_2)^2}
{(w_1+w_2)[w_1w_2+\lambda(w_1+w_2)]},
\]

and therefore

\[
\boxed{R=sL_S^*.}
\]

In the quadratic baseline, the same factor that describes how much phenotypic separation survives residual coupling also describes how much of the original compromise loss is recoverable.

This gives the optimized architecture gain

\[
\boxed{\Delta_{arch}=W_D^*-W_S^*=sL_S^*-K.}
\]

Hence

\[
\boxed{\Delta_{arch}>0 \iff K<sL_S^*.}
\]

The architecture decision therefore has three components with direct biological interpretations:

1. **conflict load, \(L_S^*\)** — how costly it is to force the two functions onto one trait;
2. **decoupling fraction, \(s\)** — what fraction of that conflict can actually be released by the differentiated architecture;
3. **architecture cost, \(K\)** — what must be paid to maintain the extra axis.

A strong trade-off does not guarantee differentiation if the new axes remain tightly coupled or expensive. Conversely, modest functional conflict can favour differentiation if decoupling is efficient and the additional architecture is cheap.

### 2.4 Comparative statics

The closed form yields four immediate predictions. First, increasing \(|\theta_1-\theta_2|\) increases the conflict load and therefore the maximum amount available to support differentiation. Second, increasing residual coupling \(\lambda\) decreases \(s\), reducing both trait separation and recoverable fitness. Third, increasing \(K\) shifts the architecture boundary one-for-one toward the shared solution. Fourth, when \(\theta_1=\theta_2\), the conflict load is zero and this conflict-relief mechanism cannot favour differentiation.

The weights \(w_1\) and \(w_2\) affect both the location of the shared compromise and the value of releasing it. If one function dominates fitness, the shared phenotype already lies close to that function's optimum, reducing the part of the trade-off that can be recovered by specializing the weaker function. Thus environmental changes that alter functional importance can move the architecture boundary even if the trait-development system itself is unchanged.

These results describe optimized phenotypes, not a mutation-by-mutation evolutionary trajectory. They say when the differentiated architecture has higher attainable fitness under the declared model. They do not specify whether a lineage can reach that architecture, how long the transition takes, or whether genetic constraints prevent it.

## 3. Robustness beyond quadratic response shapes

### 3.1 Convex power-loss family

Quadratic stabilizing losses are analytically convenient but biologically restrictive. We therefore repeated the architecture comparison with

\[
L_S(z)=w_1|z-\theta_1|^p+w_2|z-\theta_2|^p,
\]

and

\[
L_D(x,y)=w_1|x-\theta_1|^p+w_2|y-\theta_2|^p
+\lambda|x-y|^q+K,
\]

where \(p>1\) and \(q>1\). The optimized solutions were obtained deterministically by nested golden-section minimization over the interval bounded by the two function-specific optima. The numerical code has no external optimization dependency and reproduces the analytic quadratic solution when \(p=q=2\).

### 3.2 Registered finite design

The matched-curvature design crossed four functional powers (1.5, 2, 3, 4), three weighting schemes ((1,1), (0.4,2), (3,0.7)), five coupling strengths (0, 0.1, 0.5, 2, 10) and five optimum distances (0.1, 0.25, 0.5, 1, 2), giving 300 evaluations at \(K=0\). Additional checks used mismatched functional and coupling curvatures, \((p,q)=(1.5,2),(2,4),(4,2)\), and placed \(K\) just below and above the numerically recovered conflict-loss threshold.

This is a finite robustness design, not an exhaustive theorem over all possible fitness surfaces. In particular, it does not include nonconvex, multimodal, frequency-dependent or dynamically changing landscapes.

### 3.3 Robustness results

All 300 nonzero-conflict evaluations had positive recoverable conflict loss before the fixed architecture cost was charged. Across the 60 fixed combinations of response shape, weighting and coupling, increasing the distance between function-specific optima increased the recoverable loss in 60/60 series. Across the 60 fixed combinations of response shape, weighting and optimum distance, increasing residual coupling never increased recoverable loss in 60/60 series. The recoverable amount ranged from approximately \(4.46\times10^{-6}\) to 2.656 on the declared normalized loss scales.

The mismatched-curvature checks retained the same cost-threshold logic: setting \(K\) to 90% of the recovered pre-cost benefit favoured differentiation, whereas setting it to 110% favoured the shared architecture in all three registered cases.

Thus the quadratic closed form is not the sole source of the qualitative result. Within the declared convex family, conflict strength raises the potential value of differentiation, residual cross-talk erodes it, and the architecture changes only when the recoverable amount exceeds the extra cost.

## 4. Trait differentiation is often incomplete in real systems

### 4.1 Structural differentiation does not imply independence

The explicit coupling term is not merely a mathematical precaution. Cichlid feeding systems show why a differentiated architecture should be treated as a continuum. Oral and pharyngeal jaws physically separate prey capture from prey processing. In Neotropical cichlids, this separation is associated with relaxed evolutionary integration and with trait combinations that would be difficult under a single jaw system constrained by a force-motion trade-off (Burress et al. 2020). Yet the same study found feeding-ecology-dependent alignment between evolutionary rates of the two systems, and work on African cichlids found evolutionary and genetic integration between oral and pharyngeal jaw shape (Conith and Albertson 2021).

These results are compatible with a state in which \(0<s<1\): structural differentiation creates room for function-specific trait combinations, while residual ecological, developmental or genetic coupling prevents complete independence. We do not estimate \(s\) or \(\lambda\) from these studies; the point is that the model's incomplete-differentiation state corresponds to observed biological architecture rather than to a purely hypothetical intermediate.

### 4.2 Historical redeployment can accompany differentiation

Trait architecture can also change by exaptation and redeployment rather than clean duplication followed by specialization. Comparative analyses of 81 *Dalechampia* taxa found repeated associations between pollination and defence systems, including losses of a resin reward followed by defensive redeployment of resiniferous structures in several lineages, as well as the accumulation of complementary lines of defence (Armbruster et al. 2009). Five of seven inferred defence innovations were interpreted as exaptations.

This system establishes that function-structure assignments can be historically reassigned and multiplied. It does not establish that a quantified shared-trait compromise selected for those changes, nor does it estimate \(\Delta_{arch}\). We therefore use *Dalechampia* as architecture-state and historical plausibility evidence rather than as a causal test of the differentiation threshold.

### 4.3 Empirical claim boundary

The architecture theory yields a clear prospective measurement problem. A strong test would require estimates of the fitness surface under a shared or weakly differentiated state, the attainable separation of function-specific phenotypes, the residual coupling after differentiation, and the added cost of the differentiated architecture. Comparative evidence can establish repeated state associations; experimental evolution or developmental manipulation could more directly test whether reducing coupling or architecture cost changes the favored solution.

The present paper stops one level below a historical causation claim. It shows that the architecture states and partial-decoupling conditions represented by the model occur in biological systems and then asks how mechanism should be identified once multiple axes exist.

## 5. Once several trait axes exist, their fitness interaction still does not identify mechanism

### 5.1 Floral attraction and defence as a worked case

The existing BITA floral analysis provides a detailed example of the second inferential stage. Let \(A\) be one focal floral attraction trait and \(D\) a distinct flower-associated trait with an independently justified antagonist-reducing role. For an experimentally meaningful two-level design, define

\[
\Delta_{AD}W=W_{11}-W_{10}-W_{01}+W_{00}.
\]

Let

\[
A_0=W_{10}-W_{00},\qquad A_1=W_{11}-W_{01},
\]

so that \(\Delta_{AD}W=A_1-A_0\).

Three outcome claims must be separated. **Positive interaction relief** requires only \(\Delta_{AD}W>0\). **Functional constraint release** additionally requires \(A_0\le0<A_1\). **Strict reversal** requires \(A_0<0<A_1\). Thus a positive interaction can make a poor trait combination less poor without making the original focal trait beneficial.

This distinction parallels the architecture problem. Adding a second axis is not equivalent to releasing the original trade-off, just as structural separation is not equivalent to functional independence.

### 5.2 Identified set of ecological mechanisms

For the floral worked case, write reproductive outcome as a mutualist-mediated contribution \(M\), antagonist-mediated loss \(G\), and a remaining direct or allocation channel \(C\):

\[
W=M-G-C.
\]

Orient the two-trait channel interactions as

\[
\rho_\Delta=-\Delta_{AD}G,\qquad
\iota_\Delta=-\Delta_{AD}M,\qquad
\kappa_\Delta=\Delta_{AD}C.
\]

Then

\[
\Delta_{AD}W=\rho_\Delta-\iota_\Delta-\kappa_\Delta.
\]

Observing \(\Delta_{AD}W=\delta\) therefore defines an identified set

\[
\mathcal I(\delta)=\{(\rho,\iota,\kappa):\rho-\iota-\kappa=\delta\},
\]

not a unique mechanism. Better measurement of the same four total-fitness cells cannot by itself collapse this set to a point.

### 5.3 Crossed interventions for channel allocation

Point identification of the biotic channels requires additional interventions. The existing BITA design crosses

\[
A\times D\times E_G\times E_P,
\]

where \(E_G\) controls antagonist access and \(E_P\) controls pollinator access. The interventions must be selective and the trait manipulations must remain biologically invariant across consumer states. Antagonist exclusion identifies how the \(A\times D\) interaction changes antagonist-mediated loss; pollinator exclusion identifies the pollinator-dependent increment, with explicit treatment of reproduction that persists without pollinators.

The design also tests its own separability assumption. Differences in the inferred \(A\times D\) antagonist-relief term across pollinator states and differences in the pollinator-increment term across antagonist states are the same four-way \(A\times D\times E_G\times E_P\) interaction with opposite signs. A nonzero four-way term therefore indicates cross-consumer coupling and invalidates a simple additive channel allocation.

Any remaining residual must not automatically be called a construction or allocation cost. The joint channel requires an independent assay before receiving that biological label.

### 5.4 Existing floral studies occupy complementary design faces

Published floral systems contain many of the required ingredients but rarely their intersection. The current source-adjudicated route synthesis contains 56 route records from 25 independent biological study clusters and recovers all four constituent marginal pathway families. These counts establish recurrence capacity, not natural prevalence and not channel-interaction magnitudes.

A stricter high-information audit identifies 17 systems that occupy complementary parts of the required design. Kessler et al. (2008) provides a rare manipulated attraction-by-defence-like factorial in *Nicotiana attenuata*. Under the registered aggregate reconstruction, the attraction effect in the high-defence state, \(A_1\), remains approximately +0.200 to +0.240, while \(A_0\) remains in an interval spanning zero, approximately -0.030 to +0.030, and the total interaction remains positive. Exact source/design-based uncertainty and the scope of systemic nicotine suppression prevent promotion to strict Level-2 or Level-3 release. Egan et al. (2021) provides a complementary consumer factorial, while a public *Impatiens capensis* reanalysis reaches randomized context modification of observational traits. No screened high-information system combines the complete channel-allocation design with an independent joint-channel assay.

The empirical gap is therefore **fragmented identification**, not absence of relevant biology. Trait manipulations, consumer interventions, reproductive endpoints and mechanistic measurements exist, but are usually distributed among different studies.

## 6. Discussion

### 6.1 A trade-off has two qualitatively different resolutions

The central distinction is between optimizing a shared trait and changing the architecture that carries the functions. If one coordinate remains responsible for both functions, the best attainable phenotype is a compromise and the residual loss \(L_S^*\) is unavoidable under that architecture. Differentiation creates a larger phenotype space, but only the part of that space that is genuinely decoupled can recover the compromise loss. The additional architecture must then pay for itself.

This separates two questions that are often blurred. Strong conflicting selection can move the optimum of a multifunctional trait without selecting for modularization. Conversely, a duplicated or structurally separate system can remain so tightly coupled that little of the original conflict is released. The relevant comparison is not one trait versus two traits in name, but the best attainable fitness under each architecture.

### 6.2 The decoupling fraction gives a useful intermediate state

The identity \(R=sL_S^*\) makes partial differentiation explicit. In the quadratic baseline, \(s\) simultaneously measures the retained separation between function-specific trait optima and the fraction of shared-axis loss that is recoverable. This makes the model useful even when complete specialization is biologically unrealistic.

The cichlid evidence is instructive precisely because it is not a clean story of independence. Structurally separate jaw systems can relax mechanical constraints while remaining correlated through ecology, genetics and development. Such systems should not be classified simply as either integrated or modular. They occupy intermediate architecture states in which trait separation is real but incomplete.

### 6.3 Relation to existing specialization and multifunctionality theory

The architecture result sits within a mature theoretical literature. Rüffler et al. (2012) showed that functional specialization and division of labour depend on performance functions, positional effects, interactions among modules and robustness. Guillaume and Otto (2012) showed that pleiotropy versus specialization depends on functional trade-offs and the mapping from functionality to fitness. Sack and Buckley (2020) emphasized that multifunctional traits are optimized across functions rather than independently for each one.

Our contribution is therefore not the existence of specialization. It is the interface among three levels that are usually treated separately: an empirically measured shared-trait compromise, a tractable architecture-gain calculation with explicit incomplete decoupling, and a causal identification problem after multiple traits exist. This interface matters because an observed multi-trait phenotype can be consistent with the architecture theory while leaving the ecological pathway responsible for its advantage unidentified.

### 6.4 Differentiation and mechanism identification are distinct inferential problems

The floral worked case makes this distinction concrete. Suppose an attraction trait and a defence trait interact positively on reproduction. That result establishes neither that the two traits originated by splitting an ancestral multifunctional trait nor that the positive interaction arose through the mechanism suggested by their names. It may represent antagonist relief, pollinator interference of lower magnitude, a joint construction effect or an omitted pathway. Mechanistic explanation requires interventions that isolate the relevant channels.

This point generalizes beyond flowers. Whenever differentiated modules interact on a common performance or fitness scale, structural modularity should not be used as a mechanism label. Architecture answers where functions are carried. Identification answers what causal paths make that architecture successful.

### 6.5 Environmental change can move both the compromise and the differentiation boundary

Functional weights need not be fixed. If ecological context changes the relative importance of the two functions, the shared optimum shifts and the loss generated by the weaker function can shrink or expand. The value of differentiation therefore depends not only on intrinsic trait-development architecture but also on the environment loading each function.

This suggests a direct link to Chapter 1. A shared trait may appear stably balanced in one environment because \(L_S^*\) is small or because one function dominates. In another environment, the same underlying functions may produce a larger compromise loss and move the system closer to the differentiation threshold. The Chapter 1 balance is therefore not merely an endpoint; it provides the empirical quantity whose cost Chapter 2 asks whether architecture can recover.

### 6.6 Testable predictions

The framework generates several prospective predictions.

First, systems in which function-specific optima are farther apart should show stronger selection for architectural decoupling, provided suitable developmental variation exists. Second, among systems with comparable conflict load, those with stronger residual genetic, developmental or ecological coupling should retain more integrated trait combinations. Third, the appearance of an additional module should be disfavoured when its maintenance or coordination cost is high even under severe functional conflict. Fourth, partial differentiation should be common: two structures can show measurable function-specific specialization while remaining correlated. Fifth, after a differentiated architecture appears, total cross-trait interactions should often remain mechanistically ambiguous unless consumer or pathway interventions are crossed with the trait axes.

These predictions can be tested using comparative data, experimental evolution, developmental manipulation and factorial field experiments. A particularly strong design would measure a multifunctional shared-trait surface, manipulate or compare an independently varying second axis, estimate residual coupling, and assay the channels through which the resulting phenotype changes fitness.

### 6.7 Limits

The theory deliberately omits several processes. It compares optimized architecture states rather than modelling mutation, inheritance, genetic covariance, branching or transition times. The quadratic result assumes smooth convex losses; the robustness analysis broadens response shape but remains within a finite convex family. Nonconvex or frequency-dependent landscapes can create multiple local optima and may alter the architecture boundary qualitatively. The fixed architecture cost \(K\) is a coarse summary and may itself depend on trait values or environment. Likewise, the coupling penalty \(\lambda(x-y)^2\) compresses distinct genetic, developmental, biomechanical and ecological sources of integration into one effective term.

The empirical evidence also has a strict ceiling. Cichlid and *Dalechampia* studies establish relevant architecture states and historical reorganizations but do not estimate the BITA threshold. The floral corpus identifies recurrent pathways and a fragmented experimental frontier but does not reconstruct the historical origin of differentiated traits. A stronger claim that a particular one-axis trade-off caused the evolution of a particular second trait requires historical or experimental-transition evidence not provided here.

## 7. Conclusions

When a single trait serves functions with different preferred states, compromise has a measurable fitness cost. Differentiation can recover only the fraction of that loss that the new trait axes actually decouple. In the quadratic baseline this yields a compact architecture rule,

\[
\Delta_{arch}=sL_S^*-K,
\]

where \(L_S^*\) is the shared-trait conflict load, \(s\) is the surviving fraction of function-specific separation, and \(K\) is the extra architecture cost. The qualitative structure persists across the declared nonquadratic robustness family.

The rule reframes trait differentiation as neither inevitable specialization nor simple multiplication of structures. Two axes may remain strongly coupled, and structural differentiation can be only partial. Empirical jaw systems illustrate this intermediate state, while *Dalechampia* illustrates historical redeployment and accumulation of functional structures.

Finally, differentiation does not end the inference problem. Once multiple traits exist, their total fitness interaction still does not identify the ecological pathway that makes the architecture work. The floral BITA case shows how crossed interventions and independent channel assays can resolve that second problem. Together, the SCH/BITA programme therefore moves from **how conflicting functions balance on one trait** to **when the conflict is worth partitioning across traits, and how to identify the mechanism of that partitioned phenotype**.

## References added for the Chapter 2 reframe

Armbruster, W. S., Lee, J. & Baldwin, B. G. (2009). Macroevolutionary patterns of defense and pollination in *Dalechampia* vines: adaptation, exaptation, and evolutionary novelty. *Proceedings of the National Academy of Sciences USA* 106(43):18085–18090. https://doi.org/10.1073/pnas.0907051106

Burress, E. D., Martinez, C. M. & Wainwright, P. C. (2020). Decoupled jaws promote trophic diversity in cichlid fishes. *Evolution* 74(5):950–961. https://doi.org/10.1111/evo.13971

Conith, A. J. & Albertson, R. C. (2021). The cichlid oral and pharyngeal jaws are evolutionarily and genetically coupled. *Nature Communications* 12:5477. https://doi.org/10.1038/s41467-021-25755-5

Guillaume, F. & Otto, S. P. (2012). Gene functional trade-offs and the evolution of pleiotropy. *Genetics* 192(4):1389–1409. https://doi.org/10.1534/genetics.112.143214

Rüffler, C., Hermisson, J. & Wagner, G. P. (2012). Evolution of functional specialization and division of labor. *Proceedings of the National Academy of Sciences USA* 109(6):E326–E335. https://doi.org/10.1073/pnas.1110521109

Sack, L. & Buckley, T. N. (2020). Trait Multi-Functionality in Plant Stress Response. *Integrative and Comparative Biology* 60(1):98–112. https://doi.org/10.1093/icb/icz152

**Existing floral references and methods:** retain and integrate the source-checked reference spine from `IDENTIFICATION_DESIGN_REFERENCES.md` when this draft is promoted to the canonical manuscript.
