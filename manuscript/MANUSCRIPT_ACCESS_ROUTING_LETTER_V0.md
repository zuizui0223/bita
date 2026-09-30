# Access constraints reroute floral exploitation across bird and insect visitor networks


## Abstract

Access constraints may reroute exploitation rather than suppress it. We test this prediction in an all-Ecuador bird–flower network and an independent Afrotropical insect network. Across 259 Ecuadorian plant species, tube–bill mismatch correlated with robbery (\(\rho=0.503\), permutation \(p=0.0001\)), and within-bird analyses recovered the same direction. A zero-inclusive, pre-frozen participation analysis then showed that Ecuadorian barrier dyads also had higher total route-resolved exploitation after waypoint and bird main effects (rate ratio 1.77, 95% plant-jackknife CI 1.11–2.84). In 57 insect-network plant species, tube length was associated with a shift from thieving toward robbing (\(\rho=0.347\), \(p=0.0086\)); the equal-network joint routing effect was \(\rho_J=0.428\), \(p=0.0001\). A frozen OpenAlex frame resolved 33 direct programs (22 positive, 5 null, 4 opposite, 2 mixed). Access constraints can therefore amplify exploitation while changing how it occurs, although standardized network replication remains \(k=2\).

## Introduction

Access-restricting structures are usually treated as filters: if an exploiter cannot use the normal route, interaction frequency should decline. But flexible consumers can instead change handling mode, attack site or route of entry. Flowers make this distinction explicit because structures that mediate legitimate pollination also confront robbers, thieves and other antagonists. Chemical and physical floral defences can deter some consumers while sparing others, and their effects change with exposure, consumer identity and context (Adler & Irwin 2005; Johnson et al. 2015; Lucas-Barbosa 2016; Rusman et al. 2018). A barrier may therefore reorganize interaction pathways rather than simply remove interactions.

We formalize this as an **effective access domain**. A legitimate visitor and an antagonist can differ in geometry, susceptibility, timing or attack route, so the same trait need not impose the same effective constraint on both. A selective defence is possible when antagonist use is restricted before legitimate visitation is impaired. But even a strong access constraint need not suppress antagonism if a bypass remains available. Instead, an exploiter can switch from using the legitimate opening to piercing, robbing or another alternative route.

This yields a simple prediction that is more general than any one floral defence:

> **As mismatch with the legitimate access route increases, exploitation should shift toward bypass routes rather than merely decline.**

Direct studies already show both the predicted direction and boundary cases: longer flowers were more frequently robbed across four communities (Rojas-Nossa et al. 2016) and in naturalised *Fuchsia* (Stanley & Cosnett 2021), whereas longer corollas predicted lower robbery in the primary model across bird-pollinated *Erica* populations (Coetzee et al. 2026). These studies lack a common visitor × plant estimand and therefore provide context rather than additional standardized network replicates.

The prediction has not been tested as a common standardized association across independently assembled visitor networks with different faunas. We therefore use the all-Ecuador EPHI bird–flower network as the primary quantitative test. After metadata-informed treatment of unspecified piercing records and trait matching, it contains 2,265 bird × plant × site units across 18 sites, which we aggregate to 259 plant species for primary inference (Aubert et al. 2026; EPHI public data). We then use the smaller Afrotropical insect–flower network of Sakhalkar et al. (2023) as an independent corroborative test on a different cheating contrast: robbing versus thieving among plant species.

Our analysis separates two questions. First, does mismatch change **how** observed exploitation occurs? We test route composition in Ecuador and ask whether the independent insect network recovers the same direction, then combine one plant-species rank effect per network with equal weight. Second, does the Ecuadorian access barrier change **how much** exploitation occurs? For that question we reconstruct zero-inclusive local bird opportunities and estimate total route-resolved interaction intensity under a model frozen before its effect was opened. Source-audited floral-defence cases provide mechanistic context, not independent validation.

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

We test three predictions.

**P1. Bird access barriers.** Across bird–plant interactions, flowers whose tubes exceed visitor bill length should experience greater robbery, and continuous tube–bill mismatch should be positively associated with robbery rate.

**P2. Insect route switching.** Across plant species, stronger floral access constraint should be associated with a shift from nectar thieving through the floral opening toward nectar robbing by bypass.

**P3. Cross-network recurrence.** After converting each network to a rank-based association between access constraint and bypass propensity, the two network effects should be positive and their equal-network joint statistic should exceed a null generated by network-appropriate permutations.

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

To distinguish rerouting from participation filtering, we separately reconstructed zero-inclusive bird × waypoint opportunities using only cameras explicitly coded as problem-free. A bird entered a waypoint's opportunity pool only if it was observed at a problem-free camera in the same site during the waypoint's sampling interval; explicit nonfeeding records were excluded from exploitation counts. Before opening the effect, we froze a Poisson log-linear model with waypoint and bird-species fixed effects and a barrier indicator. Its estimand was the barrier/access rate ratio in total route-resolved exploitation. Uncertainty used delete-one-plant-species jackknife intervals; a 90% CI inside 0.80–1.25 was the prespecified equivalence criterion.

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

### Access barriers increase total exploitation rate in Ecuador

The zero-inclusive participation analysis contained 19,909 trait-matched bird × waypoint opportunities (6,519 positive and 13,390 zero). After waypoint and bird-species main effects, barrier dyads had a higher total route-resolved exploitation rate than accessible dyads (rate ratio 1.77, 95% plant-cluster jackknife CI 1.11–2.84; 90% CI 1.19–2.63). The prespecified outcome was therefore **participation increase plus routing**, not suppression plus rerouting. Strict-feeding and broad-feeding sensitivities gave rate ratios of 1.71 and 1.77, respectively.

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

The formal search added reversals rather than merely reinforcing the earlier targeted corpus. In a post hoc mechanism audit, two of the four opposite programs directly documented structures that hardened robber entry/bypass; the remaining reversals did not separately identify bypass cost, and the mixed programs varied across morphs or populations. We therefore treat this as boundary-mechanism partitioning, not a success proportion or prospective prediction test.

### Floral-defence cases provide mechanistic context, not independent validation

The broader defence-side corpus contains 17 unique study programs: nine chemical, seven physical and one reward/access implementation. Ten studies also measured pollinator consequences under the same focal defence, and those outcomes were heterogeneous rather than showing one fixed pollinator penalty. Eight independent systems additionally show within-trait state changes with dose, cumulative exposure, consumer identity, response stage or timing.

The matched effective-domain classifications are author-coded from source descriptions, and historical systems contributed to development of the framework. They have not yet undergone outcome-blinded independent recoding. We therefore do not use the matched-domain layer as an independent validation dataset, report no inter-rater agreement statistic, and do not make an 11/11 success-rate argument in this Letter.

These cases motivate the access/exposure mechanism and its experimental predictions. The quantitative inferential contribution of the Letter is the Ecuadorian network test, the independent insect corroboration, and their equal-network joint statistic.

## Discussion

### Access barriers can amplify as well as reroute exploitation

The central result is a cross-fauna recurrence of the same routing prediction. Insects and birds differ radically in body size, sensory biology, handling behavior and floral interactions, and the two public datasets were assembled independently for different purposes. After expressing each system as a plant-species rank association between access constraint and bypass propensity, both effects were positive: \(r_S=0.347\) and \(r_A=0.503\). The equal-network joint effect was \(r_J=0.428\).

The standardized replication count is therefore still only two networks, but the biological phenomenon is not represented by only two empirical examples. The formal bibliographic frame resolved 33 independent direct programs spanning experimental, population and community designs, including five null, four opposite and two mixed outcomes. Ten programs were newly eligible relative to the pre-existing direct corpus, and three of those ten were opposite rather than supportive. Those studies cannot be pooled into the network statistic, but they show that access geometry and robbery have been tested repeatedly in distinct systems and that formal search adds boundary cases as well as supporting cases.

A third independent multispecies bird–flower dataset points in the same direction at the level of the published analysis. Case et al. (2026) analysed Hawaiian lobelioids with pairwise bill-minus-flower matching and reported that nectar robbing declined as bill length approached flower length; under our orientation, greater flower-minus-bill mismatch therefore corresponds to greater robbery. The deposited interaction-file metadata span 11 plant and seven bird species. Because this direction was already public before our reanalysis lane and the study does not satisfy the frozen non-avian third-fauna criterion, we treat it as directional corroboration rather than a third standardized network contribution. The equal-network statistic and standardized replication count remain \(k=2\).

The Ecuadorian participation analysis closes an important alternative explanation. The robbery shift was not produced by a decline in total exploitation that left only a robbery-biased residue: after waypoint and bird main effects, barrier dyads had 1.77 times the total route-resolved exploitation rate of accessible dyads. Thus, in this observational bird network, access mismatch was associated with **amplification plus rerouting**. This amplification result is specific to Ecuador; the cross-fauna result remains the recurrence of routing direction across the two standardized networks.

The within-bird result sharpens this interpretation. The routing signal persisted after ranks were centered within bird species, whereas one mean mismatch and robbery value per bird species showed little association. The supported pattern is therefore not simply that some consumer species are intrinsically more prone to robbery. Route use changes with the consumer–resource relation, making interaction mode a relational property of trait matching rather than only a fixed consumer attribute.

The general object is therefore not a particular flower structure but the relation between consumer phenotype and the accessible routes through a resource.

The relative-cost view clarifies some, but not all, reversals. Geometry should promote robbery only when it raises legitimate-route cost more than bypass cost. Within the post hoc audit of the six non-positive programs, two opposite cases directly documented geometry that hardened robber entry; the remaining reversals left bypass cost unresolved or implicated additional behavioral context, and mixed programs varied across morphs or populations. This partition identifies plausible boundary mechanisms but, because cases were selected by frozen direction, does not show that the theory prospectively predicts every exception.

The evidence therefore supports a nested claim rather than a universal law. The two networks establish observational recurrence, and the within-bird analyses show that routing varies within consumer species. Relative route cost is the mechanistic interpretation that unifies the observed positive direction with null and opposite boundary cases. Generality beyond the analysed networks, and causal sign reversal when bypass cost itself is manipulated, remain prospective predictions.

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

Across an all-Ecuador bird–flower network and an independent Afrotropical insect network, stronger constraint on the legitimate floral access route is associated with greater bypass exploitation. After treating unspecified EPHI piercing records according to the source metadata and using plant species as the inferential unit in both networks, a joint equal-network rank test yields \(r_J=0.428\) with permutation \(p=0.0001\). A frozen finite bibliographic frame additionally resolves 33 direct access-geometry study programs—22 positive, five null, four opposite and two mixed—while only the two networks share the standardized estimand used for joint inference. Source-audited floral-defence cases provide mechanistic context for access and exposure dependence rather than an independent validation claim.

In Ecuador, barriers were associated not only with greater robbery propensity but with higher total route-resolved exploitation; across the bird and insect networks, the routing direction recurred. **Access architecture can therefore change both how interactions occur and, in at least one system, how much exploitation occurs.** Relative route cost provides a testable way to connect these outcomes without assuming that one trait has one fixed ecological effect.

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
- Rojas-Nossa SV, Sánchez JM, Navarro L (2016) Nectar robbing: a common phenomenon mainly determined by accessibility constraints, nectar volume and density of energy rewards. *Oikos* 125:1044–1055. https://doi.org/10.1111/oik.02685
- Stanley DA, Cosnett E (2021) Catching the thief: Nectar robbing behaviour by bumblebees on naturalised *Fuchsia magellanica* in Ireland. *Journal of Pollination Ecology* 29:240–248. https://doi.org/10.26786/1920-7603(2021)620
- Coetzee A, Seymour CL, Spottiswoode CN, Pirie MD, van der Niet T (2026) Is bee-avoidance by bird-pollinated flowers driven by nectar robbing in *Erica*? *Functional Ecology* 40:1046–1060. https://doi.org/10.1111/1365-2435.70276
- Leal LC, Koski MH, Irwin RE, Bronstein JL (2025) Costs of floral larceny: a meta-analytical evaluation of nectar robbing and nectar theft on animal-pollinated plants. *Ecology* 106:e70036. https://doi.org/10.1002/ecy.70036
- Case SB, Hagemann ME, Drake DR, Postelli K, Pender RJ, Millikin PW, Rico-Guevara A (2026) Bird extinctions shift bill–flower trait matching in Hawaiian lobelioids. *Functional Ecology* 40:2972–2981. https://doi.org/10.1111/1365-2435.70415
