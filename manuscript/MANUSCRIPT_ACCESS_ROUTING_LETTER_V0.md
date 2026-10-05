# Access constraints predict interaction routing across bird and insect visitor networks


## Abstract

Access constraints can remove interactions or change their route. Existing studies link floral mismatch to nectar robbery; we separate routing from participation. In an Ecuadorian bird–flower network, tube–bill mismatch predicted robbery across 259 plant species (rho=0.503, p=0.0001) and within bird species. A preregistered culmen-only participation model suggested no filtering, but a post-open 1.8× tongue-reach sensitivity reversed that inference: legitimate feeding declined under barriers (RR=0.154, 95% CI 0.087–0.271) while robbery-only counts were unresolved (0.816, 0.358–1.860). An independent Afrotropical insect network showed the same routing direction across 57 plant species (rho=0.347, p=0.0086); equal-network rho_J=0.428 (p=0.0001). Thus mismatch predicts route composition, while inferred filtering depends on physiological reach; standardized network generality remains k=2.

## Introduction

Access-restricting structures are often treated as filters: if a consumer cannot use the normal route, interaction frequency should decline. Yet flexible consumers can change handling mode or entry route. Flowers expose this distinction because structures mediating legitimate pollination also confront robbers and thieves; a barrier may therefore alter interaction pathways rather than simply remove interactions.

We frame this as an **effective access domain**. Legitimate and bypass routes can differ in geometry, susceptibility or handling cost, so increasing mismatch with the legitimate route need not eliminate use when a bypass remains available. Our prediction is therefore:

> **As mismatch with the legitimate access route increases, exploitation should shift toward bypass routes rather than merely decline.**

The component associations are already known. Aubert et al. (2026) showed that nectar robbing in Andean bird–flower interactions occurred mostly when bills were shorter than flower tubes, and Sakhalkar et al. (2023) likewise found that long tubes or spurs can restrict thieving while being associated with robbing. Nor is behavioral switching itself new: legitimate visitation and robbing are alternative handling tactics whose relative efficiencies can depend on the consumer–plant combination (Bronstein et al. 2017; Lichtenberg et al. 2018), and floral traits can bias tactic use experimentally (Leonard et al. 2013). The unresolved question is how access mismatch partitions **route composition from interaction occurrence** at network scale, whether routing persists within consumer species, and whether a common routing estimand recurs across faunas.

We use the all-Ecuador EPHI bird–flower network as the primary test because its camera design permits route composition and zero-inclusive participation to be reconstructed. Trait matching yields 2,265 bird × plant × site units across 18 sites, aggregated to 259 plant species for primary inference. The Afrotropical Sakhalkar et al. (2023) network provides an independent insect contrast between robbing and thieving.

Our analysis separates three quantities: plant- and within-bird **route composition**; zero-inclusive participation under a binary access threshold, including post-open physiological-reach sensitivities; and an equal-weight cross-fauna routing statistic. A frozen direct-study frame supplies null, opposite and mixed boundary cases. Source-audited floral-defence cases remain mechanistic context, not independent validation.

## Theory and predictions

Let \(L\) denote the legitimate access route to a floral reward and \(B\) a bypass route. Let \(M\) represent mismatch between a consumer's access phenotype and the legitimate route. As mismatch increases, the utility or feasibility of the legitimate route declines,

\[
A_L(M)\downarrow,
\]

whereas bypass access can remain available,

\[
A_B>0.
\]

If exploiters can switch behavior, increasing \(M\) should therefore increase the relative use of \(B\). The exact functional form need not be common across taxa. The minimal prediction is ordinal:

\[
M \uparrow
\quad\Rightarrow\quad
\text{bypass propensity} \uparrow.
\]

More precisely, the relevant quantity is the **relative route cost**, not absolute
flower size. Let \(C_L(x)\) and \(C_B(x)\) denote the costs of legitimate and
bypass access under trait state \(x\). A simple route-choice model gives

\[
\operatorname{logit} P(B\mid x)
=
\alpha+\beta\{C_L(x)-C_B(x)\},
\qquad \beta>0.
\]

Hence the sign of a geometry–robbery association is determined by

\[
\frac{dC_L}{dx}-\frac{dC_B}{dx}.
\]

Geometry should increase robbery when it penalizes legitimate access more strongly
than bypass, have little routing effect when both routes are similarly constrained,
and reduce robbery when bypass itself is disproportionately hardened.

This prediction is compatible with the broader effective-exposure framework developed for floral defence selectivity. There, a selective window exists when the antagonist experiences a focal trait strongly enough to be suppressed before the legitimate visitor crosses its own interference threshold. Bypass is a boundary condition: if the antagonist does not traverse the defended domain, effective exposure to the focal defence falls even as exploitation persists.

The network test focuses only on the route-switching consequence. It does not require the access constraint itself to have evolved as a defence, nor does it assume a shared physiological mechanism across insects and birds.

We test four predictions.

**P1. Bird access barriers.** Across bird–plant interactions, flowers whose tubes exceed visitor bill length should experience greater robbery, and continuous tube–bill mismatch should be positively associated with robbery rate.

**P2. Participation versus routing.** If higher robbery is only the residual composition left after filtering, access barriers should reduce total resolved feeding visitation. If barriers primarily redirect route use, total visitation need not decline; we therefore distinguish suppression, equivalence, amplification and unresolved participation before interpreting the route shift.

**P3. Insect route switching.** Across plant species, stronger floral access constraint should be associated with a shift from nectar thieving through the floral opening toward nectar robbing by bypass.

**P4. Cross-network recurrence.** After converting each network to a rank-based association between access constraint and bypass propensity, the two network effects should be positive and their equal-network joint statistic should exceed a null generated by network-appropriate permutations.

## Methods

### Primary Ecuadorian bird–flower test

We analyse the public all-Ecuador EPHI data as an extension of Aubert et al. (2026), not an exact reconstruction of their three-transect mixed model. The mirror contains 54,471 interaction rows across 18 sites plus camera, plant-trait and bird-trait tables. Metadata state that unspecified piercing values are most probably legitimate (`no`) because some observers entered the field only for piercing events. We therefore recoded blank/NA as non-robbing in the primary analysis, excluded distinct non-binary states, and retained explicit yes/no complete cases as a sensitivity. Camera waypoints linked interactions to plant/site identities; tube length was compared with culmen length after unit conversion.

For each bird–plant pair within site, we calculated

\[
M=\log(T/B),
\]

where \(T\) is flower tube length and \(B\) mean bird culmen length. Positive \(M\) indicates that the flower tube exceeds bill length. We also defined a binary access barrier as \(T>B\).

Individual interactions were first aggregated to bird species × plant species × site units. Under the metadata-informed missing-as-no rule, 49,237 trait-matched interactions yielded 2,265 pair-site units across 18 sites and 259 plant species. We calculated robbery rate within each pair-site unit.

To avoid treating repeated pair-sites as independent, the primary analysis averaged mismatch and robbery rate within plant species (259 species) and permuted robbery ranks across species. For the binary contrast, each plant species observed in both barrier states contributed one paired difference (130 species), with whole-species label swaps.

We separately tested the behavioral prediction within bird species. Pair-site rows were first averaged across sites to bird × plant dyads; mismatch and robbery were then ranked and centered within each bird species, and robbery ranks were permuted only within birds. We also retained one barrier-minus-accessible difference per bird species. A correlation of one mean mismatch and robbery value per bird was treated only as a between-bird diagnostic. Complete-case yes/no results and pair-site/site summaries were sensitivities. All permutation tests used 9,999 iterations.

Before opening its result, we preregistered a plant-species shape analysis: a monotone sigmoid estimated a switching midpoint (x^*), 999 species bootstraps quantified midpoint uncertainty, and a quadratic 9,999-permutation diagnostic tested upper turnover. Localization required an interior midpoint within the 5–95% mismatch support; equality proximity required its 90% bootstrap interval to lie within (pmlog(1.25)).

### Zero-inclusive participation decomposition

To test whether increased robbery merely reflected the composition of residual interactions after filtering, we froze a zero-inclusive participation analysis before opening its mismatch effect. Opportunities were clean EPHI camera waypoints (`camera_problem=no`) crossed with target bird species observed elsewhere at the same site during the focal camera interval; explicit `no_feeding` records were excluded. The primary count pooled resolved legitimate and robbing feeding records. We fit a Poisson log-linear model with waypoint and bird-species fixed effects and a binary barrier term (tube length > culmen), with delete-one-plant-species jackknife intervals. Waypoint fixed effects absorb sampling effort and time-invariant waypoint-level plant or reward main effects, while bird fixed effects absorb baseline bird use. Because each retained waypoint contains one plant identity, tube length is constant within waypoint; the barrier coefficient is therefore a cross-classified bird × waypoint threshold estimand, not the plant-level P1 contrast. Indeed continuous log(tube/culmen) is exactly additive in waypoint-level tube and bird-level culmen and is not separately identifiable with both fixed effects. The public EPHI tables contain no direct nectar-reward covariate, so bird-specific reward responses and temporal reward variation remain potential confounders.

Exposed culmen is also not the full nectar-reach phenotype. Hummingbirds extend the tongue beyond the bill, and prior network studies have corrected bill length by one-third or by 80%; the latter was based on *Selasphorus rufus* experiments in which maximal tongue extension approached bill length, although efficient extraction declined well before maximum reach (Grant & Temeles 1992; Vizentin-Bugoni et al. 2016). After observing the culmen-only result, we therefore froze a post-open sensitivity restricted to hummingbirds (excluding *Diglossa* flowerpiercers) and reclassified the same opportunity edges using effective reach multipliers of 4/3, 1.8 and 2.0 times culmen. We refit pooled, legitimate and robbing counts with the same fixed effects and jackknife. These fixed multipliers translate continuous log mismatch by a constant, so they cannot by themselves convert a support-boundary sigmoid midpoint into an interior threshold; their informative target is the binary participation contrast.

### Independent Afrotropical insect corroboration

We reanalysed the public Sakhalkar et al. (2023) Afrotropical visitor and floral-trait dataset. Generic visiting records were excluded following the source analysis; all calculations use the currently deposited Zenodo workbook.

Visit frequencies were aggregated to plant species before inference. For each species with tube-length data and at least one robbing or thieving interaction, we calculated

\[
B_i=
\frac{R_i-T_i}{R_i+T_i},
\]

where \(R_i\) is robbing frequency and \(T_i\) thieving frequency. Thus \(B_i=1\) denotes robbery only and \(B_i=-1\) thieving only. Fifty-seven plant species met these criteria.

We tested the association between floral tube length and \(B_i\) with Spearman rank correlation and a fixed-seed two-sided permutation test using 9,999 permutations. Plant species were the inferential units; individual visits were not treated as independent replicates.

Because tube length can covary with other floral traits, we also retained the source paper's parsimonious robber predictor set—tube length, tube width and flower shape—in a robustness analysis. This sensitivity is used only to set the claim ceiling on tube length as an independent predictor.

### Joint cross-network test

Raw observations were not pooled. Each network contributed one plant-species rank association between access constraint and bypass propensity: tube length versus robbing–thieving balance in Sakhalkar, and mean tube–bill mismatch versus mean robbery in Aubert/EPHI under the metadata-informed missing-as-no rule.

Because the two datasets represent two independent networks rather than pooled interchangeable observations, they received equal weight. The primary joint effect was the Fisher-z mean,

\[
r_J=
\tanh
\left[
\frac{
\operatorname{atanh}(r_S)+
\operatorname{atanh}(r_A)
}{2}
\right].
\]

The permutation null acted on plant-species units in both datasets. In each network, response ranks were shuffled across plant species and the network correlation was recomputed; the two permuted correlations were then combined with equal network weight. We used 9,999 permutations, two-sided tests and the standard plus-one correction. Thus a reported permutation \(p=0.0001\) is the Monte Carlo resolution limit, corresponding to zero of 9,999 permuted statistics reaching the observed magnitude before the plus-one correction.

### Formal direct access-geometry literature frame

We froze an outcome-blind OpenAlex frame for empirical studies that quantitatively related an independently measured access-geometry variable to route-resolved robbery/bypass. Eligibility was fixed before direction coding for new records; positive, null, mixed and opposite results used the same rule. Eight predefined query families produced 1,699 rows and 857 deduplicated records. The frame recovered 23 of 24 pre-existing direct programs; the remaining program was independently verified absent from OpenAlex and stays outside the denominator. Unknown records were direction-blind screened and then adjudicated from primary sources; no records remain pending.

We report only the finite-frame direction distribution—no prevalence estimate, sign test, pooled effect or increment to network `k`. After directions were frozen, we post hoc audited the four opposite and two mixed programs for source evidence that the focal geometry directly hardened bypass. Because this subset was selected by direction, the audit interprets boundaries rather than validating predictions.

### Floral-defence evidence as mechanistic context

The network analysis does not identify the evolutionary origin of floral barriers. We therefore use the existing 17-program defence corpus only as mechanistic context. Its matched effective-domain classifications are author-coded, not outcome-blind independently recoded, and heterogeneous endpoints are not pooled; this material is not an independent validation dataset.

## Results

### Primary Ecuadorian test: access mismatch predicts robbery

The Ecuadorian network retained the predicted routing direction after the metadata-informed missingness correction and after moving inference to plant species. Across 259 plant species, mean tube–bill mismatch was positively associated with mean robbery rate,

\[
\rho=0.5032,
\qquad
p_{\mathrm{perm}}=0.0001.
\]

The binary barrier contrast gave the same result. Among 130 plant species observed in both barrier and accessible states, the mean within-species barrier-minus-accessible robbery difference was +0.0915; 75 of 82 nonzero species differences were positive, and the whole-species label-swap permutation gave \(p=0.0001\).

At the descriptive pair-site scale, the missing-as-no analysis yielded 2,265 units. Mean robbery was 0.147 under barriers and 0.020 when accessible, a difference of +0.127. All 18 sites containing both states showed higher mean robbery under the barrier state (two-sided sign test \(p=7.63\times10^{-6}\); site-stratified permutation \(p=0.0001\)).

The result was not created by the missing-value recoding. In the explicit yes/no complete-case sensitivity, the plant-species correlation was \(\rho=0.570\) (permutation \(p=0.0001\)), and the mean paired species difference was +0.155 (label-swap \(p=0.0001\)). The correction substantially reduced absolute robbery rates and the pair-site contrast, but not its direction.

Bird-grain analyses separated within-bird route switching from between-bird differences. Thirty-six bird species occurred in both barrier states; their mean within-bird barrier-minus-accessible robbery difference was +0.0933 (whole-bird label-swap \(p=0.0001\)). The continuous within-bird analysis used 1,285 bird × plant dyads from 28 eligible bird species and also remained positive (centered-rank \(\rho=0.340\), within-bird permutation \(p=0.0001\)); 24 of 28 bird-specific correlations were positive (median \(\rho=0.338\), sign-test \(p=0.00018\)). Within-bird mismatch was not narrowly ranged: the median species-level span was 2.31 log units. By contrast, correlating one mean mismatch and one mean robbery value across all 50 bird species gave \(\rho=0.086\), \(p=0.551\). The contrast is therefore hierarchical rather than a simple lack-of-range problem: between-bird mean mismatch does not predict mean robbery, whereas changes in mismatch across flowers used by the same bird species predict route switching.

The shape analysis did not localize a sharp threshold near tube–bill equality. The sigmoid midpoint reached the upper 95% support boundary (x^*=0.920); in a post-open audit, 585 of 999 finite bootstrap fits (58.6%) also landed on that upper search boundary, so the original 90% percentile interval (0.118–0.920) is better read as boundary-limited uncertainty than as an ordinary interior threshold interval. Curvature exceeded the permutation null (p=0.0049), and the derivative remained positive at the 90th-percentile mismatch, so no interior upper turnover was supported.

### Participation inference depends on the physiological reach threshold

The preregistered culmen-only participation analysis contained 19,909 trait-matched opportunity edges across 5,254 clean camera waypoints, 50 bird species and 288 plant species. Under the frozen barrier (T>B), pooled resolved feeding was higher under barriers (RR 1.772, 95% plant-jackknife CI 1.105–2.841). The post-open route split showed that this was carried by legitimate/non-robbing feeding (RR 1.883, 1.111–3.190), not robbery-only counts (RR 0.463, 0.147–1.461). Those numbers are retained as the frozen culmen-only result, but they do not establish that effective access barriers preserve legitimate feeding.

The post-open hummingbird-only reach sensitivity changed that interpretation while strengthening P1. With the conservative (4/3) reach multiplier, the paired plant robbery contrast increased from +0.091 to +0.191 ((p=0.0001)), but pooled feeding fell (RR 0.435, 0.255–0.742) and legitimate feeding fell more strongly (0.354, 0.197–0.635); robbery-only counts remained unresolved (0.851, 0.328–2.212). With the 1.8 multiplier used in a prior hummingbird-network analysis, the paired robbery contrast was +0.259 ((p=0.0001)), pooled RR was 0.229 (0.147–0.355), legitimate RR was 0.154 (0.087–0.271), and robbery RR was 0.816 (0.358–1.860). The robbery-to-legitimate RR ratio was then 5.31 (1.92–14.67). A 2.0 maximum-reach stress test gave the same qualitative separation: legitimate RR 0.100 (0.065–0.155), robbery RR 1.393 (0.729–2.663). Thus the no-filtering interpretation is not robust to plausible tongue reach; under the 1.8 correction, severe mismatch selectively suppresses legitimate feeding while bypass use is comparatively retained.

### Independent insect corroboration recovers the same routing direction

Among the 57 Sakhalkar plant species, tube length was positively associated with robbing–thieving balance,

\[
\rho=0.3468,
\qquad
p_{\mathrm{perm}}=0.0086.
\]

Thus longer flowers were associated with relatively greater use of robbery rather than thieving through the floral opening. Robber-only species had a median tube length of 2.089 on the deposited trait scale, compared with 0.677 for thief-only species.

The source-defined multitrait sensitivity did not isolate tube length as a unique partial predictor after accounting for tube width and a 12-level flower-shape factor (full-model permutation \(p=0.202\); tube-length block \(p=0.211\)). We therefore interpret the insect result as an association with access geometry rather than as evidence that tube length alone is causal.

### One standardized routing effect recurs across networks

For the joint analysis, the Sakhalkar rank effect was

\[
r_S=0.3468.
\]

Using the same plant-species inferential grain, the Aubert/EPHI effect was

\[
r_A=0.5032
\]

with species-level permutation \(p=0.0001\). The two networks therefore agreed in direction without requiring equal raw effect magnitudes.

The equal-network Fisher-z mean was

\[
\boxed{r_J=0.4282}
\]

and the two-sided joint permutation test gave

\[
\boxed{p_{\mathrm{joint}}=0.0001}.
\]

Both observed network effects were positive. Under the joint permutation null, the probability that both permuted effects were positive was 0.2527, close to the 0.25 expectation for two approximately symmetric directional nulls.

Thus the strongest empirical result is not merely that each source dataset contains an access association. The primary Ecuadorian test and independent insect corroboration recover the same routing direction after placing both networks on a plant-species inferential grain.

### A formal finite literature frame extends the routing test beyond two networks

The frozen OpenAlex frame contained 857 unique bibliographic records. After duplicate resolution and full eligibility adjudication, 33 independent study programs directly tested an access-geometry predictor against route-resolved nectar robbery or bypass use. Twenty-two showed the predicted direction, five were null, four were opposite and two were mixed across predeclared morphs, populations or access dimensions.

Twenty-three programs were pre-existing direct-corpus studies recovered inside the provider frame; only one was opposite (1/23, 4.3%). The formal search added ten independent programs—seven positive and three opposite (3/10, 30%). This asymmetry is descriptive, not a test of literature bias, but shows that formal search added reversals rather than merely reinforcing the earlier targeted corpus. One pre-existing program was independently verified as absent from OpenAlex and remains outside the denominator.

The post hoc mechanism audit further split the four opposite cases. Two directly documented focal structures that harden robber entry/bypass were both opposite-direction boundary cases. The other two reversals did not separately identify bypass cost: one was a broader mechanical-avoidance comparison and one invoked robber preference/context. The two mixed programs varied by floral morph or population. We therefore treat the audit as mechanism partitioning, not a success proportion or prospective sign prediction.

### Floral-defence cases provide mechanistic context, not independent validation

The broader defence-side corpus contains 17 unique study programs: nine chemical, seven physical and one reward/access implementation. Ten studies also measured pollinator consequences under the same focal defence, and those outcomes were heterogeneous rather than showing one fixed pollinator penalty. Eight independent systems additionally show within-trait state changes with dose, cumulative exposure, consumer identity, response stage or timing.

The matched effective-domain classifications are author-coded from source descriptions, and historical systems contributed to development of the framework. They have not yet undergone outcome-blinded independent recoding. We therefore do not use the matched-domain layer as an independent validation dataset, report no inter-rater agreement statistic, and do not make an 11/11 success-rate argument in this Letter.

These cases motivate the access/exposure mechanism and its experimental predictions. The quantitative inferential contribution of the Letter is the Ecuadorian network test, the independent insect corroboration, and their equal-network joint statistic.

## Discussion

### Access barriers reorganize interactions rather than simply suppress them

The central contribution is not the discovery that floral mismatch can accompany robbery; both source literatures already contain that association. It is the separation of **interaction occurrence from interaction route**. Ecuadorian mismatch predicts route composition within bird species, while the zero-inclusive model shows that inferred filtering depends on how reach is defined. The independent insect network recovers the same routing direction ((r_S=0.347), (r_A=0.503); equal-network (r_J=0.428)).

The standardized replication count is therefore still only two networks. A third independent multispecies bird–flower dataset (Case et al. 2026; 11 plant and seven bird species) is directionally concordant but remains directional corroboration rather than a third standardized network contribution; the standardized replication count remains (k=2). The formal frame adds 33 direct programs, including null, opposite and mixed outcomes, but these are not pooled into the network statistic.

P1 and P2 answer different questions. P1 is a plant-level association between continuous mismatch and robbery share. P2 is a cross-classified bird × waypoint threshold estimand: with waypoint and bird fixed effects, its coefficient is identified by which birds cross the chosen access threshold within a fixed plant/waypoint. Under the preregistered culmen-only threshold, P2 appeared to preserve legitimate feeding. That interpretation reversed with literature-motivated tongue reach. At 1.8× culmen, legitimate feeding fell to RR 0.154, robbery-only counts remained unresolved, and the robbery-to-legitimate RR ratio was 5.31. The coherent reading is not “routing without filtering”: severe effective mismatch selectively filters the legitimate route while bypass use is comparatively buffered. This post-open sensitivity uses fixed rather than measured species-specific tongue extension, and geometry was not randomized, so the result remains observational.

The within-bird result rules out a purely consumer-fixed explanation: route use changes with the consumer–resource relation, making interaction mode a relational property of trait matching. The routing response is also better supported as graded across the sampled mismatch range than as a sharp equality threshold. The fitted midpoint remains at the upper 95% support boundary, 585 of 999 bootstraps also hit that boundary, and no interior upper turnover was supported. Constant reach correction cannot rescue localization because it translates both mismatch and search support; a species-specific reach model would be required to change relative positions.

The relative-cost view organizes, rather than invents, the mechanism. Relative route cost is the mechanistic interpretation: geometry should promote robbery when it penalizes legitimate access more strongly than bypass, and can yield null or opposite effects when bypass is similarly or more constrained. In the post hoc audit, two opposite cases directly documented geometry that hardened robber entry; other reversals left bypass cost unresolved or involved additional context. Because those cases were selected by frozen direction, this does not show that the theory prospectively predicts every exception.

The evidence therefore supports a nested claim rather than a universal law. Two standardized networks establish observational recurrence, within-bird analyses establish relational routing, and the effective-reach sensitivity shows how selective legitimate-route filtering can generate higher robbery share without requiring more robbery events. Generality beyond the two network systems and causal sign reversal under manipulated route costs remain prospective predictions.

### A relational view clarifies floral defence selectivity

The defence corpus remains mechanistic context because broad labels such as chemical or physical defence do not specify who encounters a trait or by which route. In an effective-exposure view, selectivity depends on antagonists crossing a response threshold before legitimate visitors; bypass is the limiting case in which antagonists stop traversing the defended domain while exploitation persists. Consequently, total visitation or damage can hide route switching. Experiments should distinguish legitimate use, thieving, robbing and other handling modes.

### What the joint test does—and does not—establish

The joint analysis was designed to test recurrence without pretending that the two datasets share a raw effect scale. Plant species in the Sakhalkar network and bird × plant × site units in the Ecuadorian network are not interchangeable observations. Equal network weighting therefore reflects the scientific question—whether the same directional relationship appears in independent networks—rather than the relative row counts in the underlying datasets.

The joint statistic contains only \(k=2\) independent network-level contributions. Its permutation \(p\)-value tests whether these two networks jointly show a stronger standardized routing signal than their network-specific nulls; it does not estimate between-network heterogeneity, a population-level mean across ecological networks, or generality beyond the two network systems analysed here. Broader generality remains a prediction for replication across additional independent networks.

The result remains observational. Floral geometry was not randomized, and correlated morphology prevents a unique tube-length claim in the insect network. The Ecuador analysis is an all-site extension rather than an exact reconstruction of Aubert et al.'s three-transect model. Its primary result aggregates to plant species, while two within-bird analyses independently recover the routing direction. The null correlation among bird-species means asks a different between-species question and is retained as a boundary, not discarded. The result is not a universal causal coefficient.

The matched floral-defence material is mechanistic context rather than independent validation. Historical systems contributed to development of the effective-domain framing, the domain coding has not yet been outcome-blind independently replicated, null-compatible outcomes are not equivalence tests, and the strict direction-supported matched subset remains small. These limitations are precisely why the network analyses—not the matched-domain alignment—carry the inferential contribution of the Letter.

### Predictions

The routing framework generates direct experimental tests.

First, the strongest causal test is a factorial manipulation of route costs while reward is held constant. Raising legitimate-route cost while bypass cost is fixed should increase bypass; raising bypass cost while legitimate cost is fixed should decrease bypass; raising both similarly should produce little route-composition shift. This prospective sign-reversal test directly distinguishes relative route cost from absolute barrier strength.

Second, graded manipulations should separate rerouting from suppression. Selectively constraining only the legitimate route should increase the relative frequency of bypass, whereas closing both routes should primarily reduce total exploitation.

Third, consumer morphology should interact with floral geometry. The same flower should produce different route choices among visitors with different access phenotypes, providing a direct test of the effective-domain mechanism.

Finally, defence experiments should measure pollinator response and antagonist route simultaneously. Our literature audit found abundant antagonist-focused work but much thinner pollinator-side follow-up for physical barriers, leaving exactly the experiments needed to connect route switching to selective defence.

## Conclusion

Across bird and insect networks, access mismatch predicts greater use of bypass routes. In Ecuador, the effect is relational within bird species, while zero-inclusive inference depends strongly on physiological reach: under a literature-based 1.8× correction, legitimate feeding is selectively filtered and robbery is comparatively retained. The equal-network routing effect is (r_J=0.428) ((p=0.0001)), with standardized replication limited to (k=2). Access geometry should therefore be treated as a determinant of **how interactions occur**, not only whether they occur.

## Data accessibility and reproducibility

**A permanent analysis-data/code archive DOI is required before submission.** The submission archive will contain the exact analysis-ready tables used for inference, column metadata, reproduction code, frozen derived outputs, and the formal direct-evidence bibliographic frame with its eligibility, direction-coding, search and provenance receipts. The archive tables omit source taxon labels and deterministically relabel EPHI site, plant and bird identifiers while preserving the clustering needed for plant-species, within-bird and site sensitivities.

Underlying public source data are Sakhalkar et al. (2023), Zenodo DOI 10.5281/zenodo.8398202, and the EPHI Ecuador mirror, Zenodo DOI 10.5281/zenodo.14185547, associated with Aubert et al. (2026).

Final submission wording after deposit:

> The analysis-ready data tables, metadata, analysis code, frozen derived outputs and bounded direct-evidence audit supporting this Letter are archived at **[ACCESS-ROUTING ARCHIVE DOI]**. Underlying public source datasets are archived by their original authors at Zenodo DOI 10.5281/zenodo.8398202 and Zenodo DOI 10.5281/zenodo.14185547.

## Acknowledgments, funding and conflict of interest

**AUTHOR-CONTROLLED — REQUIRED BEFORE SUBMISSION.**

Insert the final acknowledgments and funding statement here. All authors must also provide the collective conflict-of-interest disclosure required by Ecology Letters. If there are no relevant conflicts, replace this placeholder with the author-approved no-conflict statement.

## References

- Sakhalkar SP, Janeček Š, Klomberg Y, Mertens JEJ, Hodeček J, Tropek R (2023) Cheaters among pollinators: Nectar robbing and thieving vary spatiotemporally with floral traits in Afrotropical forests. *Ecosphere* 14:e4696. https://doi.org/10.1002/ecs2.4696
- Sakhalkar S, Janeček Š, Klomberg Y, Mertens JEJ, Hodeček J, Tropek R (2023) R code and datasets for flower-visitor interactions (pollinators, robbers, thieves) and plant traits from Mount Cameroon. Zenodo, v1.0.0. https://doi.org/10.5281/zenodo.8398202
- Aubert S, Duchenne F, Tinoco BA, Santander T, Guevara EA, Graham CH (2026) Trait matching affects the probability of nectar robbing in plant-pollinator networks. *Oikos* 2026(3):e11552. https://doi.org/10.1002/oik.11552
- Santander T, Varassin I, Maglianesi MA, et al. (2024) Plant-hummingbird interactions, floral abundance and floral traits for three altitudinal gradients in the Americas. Zenodo. https://doi.org/10.5281/zenodo.14185547
- Johnson MTJ, Campbell SA, Barrett SCH (2015) Evolutionary interactions between plant reproduction and defense against herbivores. *Annual Review of Ecology, Evolution, and Systematics* 46:191–213. https://doi.org/10.1146/annurev-ecolsys-112414-054215
- Lucas-Barbosa D (2016) Integrating studies on plant–pollinator and plant–herbivore interactions. *Trends in Plant Science* 21:125–133. https://doi.org/10.1016/j.tplants.2015.10.013
- Rusman Q, Lucas-Barbosa D, Poelman EH (2018) Dealing with mutualists and antagonists: specificity of plant-mediated interactions between herbivores and flower visitors, and consequences for plant fitness. *Functional Ecology* 32:1022–1035. https://doi.org/10.1111/1365-2435.13035
- Adler LS, Irwin RE (2005) Ecological costs and benefits of defenses in nectar. *Ecology* 86:2968–2978. https://doi.org/10.1890/05-0118
- Gegear RJ, Manson JS, Thomson JD (2007) Ecological context influences pollinator deterrence by alkaloids in floral nectar. *Ecology Letters* 10:375–382. https://doi.org/10.1111/j.1461-0248.2007.01027.x
- Barlow SE, Wright GA, Ma C, Barberis M, Farrell IW, Marr EC, Brankin A, Pavlik BM, Stevenson PC (2017) Distasteful nectar deters floral robbery. *Current Biology* 27:2552–2558.e3. https://doi.org/10.1016/j.cub.2017.07.012
- Galen C, Kaczorowski R, Todd SL, Geib J, Raguso RA (2011) Dosage-dependent impacts of a floral volatile compound on pollinators, larcenists, and the potential for floral evolution in the alpine skypilot *Polemonium viscosum*. *The American Naturalist* 177:258–272. https://doi.org/10.1086/657993
- Jones PL, Agrawal AA (2016) Consequences of toxic secondary compounds in nectar for mutualist bees and antagonist butterflies. *Ecology* 97:2570–2579. https://doi.org/10.1002/ecy.1483
- Bronstein JL, Barker JL, Lichtenberg EM, Richardson LL, Irwin RE (2017) The behavioral ecology of nectar robbing: why be tactic constant? *Current Opinion in Insect Science* 21:14–18. https://doi.org/10.1016/j.cois.2017.05.013
- Lichtenberg EM, Irwin RE, Bronstein JL (2018) Costs and benefits of alternative food handling tactics help explain facultative exploitation of pollination mutualisms. *Ecology* 99:1815–1824. https://doi.org/10.1002/ecy.2395
- Leonard AS, Brent J, Papaj DR, Dornhaus A (2013) Floral nectar guide patterns discourage nectar robbing by bumble bees. *PLoS ONE* 8:e55914. https://doi.org/10.1371/journal.pone.0055914
- Grant V, Temeles EJ (1992) Foraging ability of rufous hummingbirds on hummingbird flowers and hawkmoth flowers. *Proceedings of the National Academy of Sciences USA* 89:9400–9404. https://doi.org/10.1073/pnas.89.20.9400
- Vizentin-Bugoni J, Maruyama PK, Debastiani VJ, Duarte LS, Dalsgaard B, Sazima M (2016) Influences of sampling effort on detected patterns and structuring processes of a Neotropical plant–hummingbird network. *Journal of Animal Ecology* 85:262–272. https://doi.org/10.1111/1365-2656.12459
- Rojas-Nossa SV, Sánchez JM, Navarro L (2016) Nectar robbing: a common phenomenon mainly determined by accessibility constraints, nectar volume and density of energy rewards. *Oikos* 125:1044–1055. https://doi.org/10.1111/oik.02685
- Stanley DA, Cosnett E (2021) Catching the thief: Nectar robbing behaviour by bumblebees on naturalised *Fuchsia magellanica* in Ireland. *Journal of Pollination Ecology* 29:240–248. https://doi.org/10.26786/1920-7603(2021)620
- Coetzee A, Seymour CL, Spottiswoode CN, Pirie MD, van der Niet T (2026) Is bee-avoidance by bird-pollinated flowers driven by nectar robbing in *Erica*? *Functional Ecology* 40:1046–1060. https://doi.org/10.1111/1365-2435.70276
- Leal LC, Koski MH, Irwin RE, Bronstein JL (2025) Costs of floral larceny: a meta-analytical evaluation of nectar robbing and nectar theft on animal-pollinated plants. *Ecology* 106:e70036. https://doi.org/10.1002/ecy.70036
- Case SB, Hagemann ME, Drake DR, Postelli K, Pender RJ, Millikin PW, Rico-Guevara A (2026) Bird extinctions shift bill–flower trait matching in Hawaiian lobelioids. *Functional Ecology* 40:2972–2981. https://doi.org/10.1111/1365-2435.70415
