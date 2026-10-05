# Access constraints predict interaction routing across bird and insect visitor networks


## Abstract

Access mismatch can alter both whether an interaction occurs and how it occurs, but these margins need not share a morphological threshold. In an all-Ecuador bird–flower network, tube–bill mismatch predicted robbery across 259 plant species (rho=0.503, p=0.0001) and within bird species. A preregistered zero-inclusive model using the source-defined tube>culmen barrier gave higher pooled feeding (rate ratio 1.772), but a post-open hummingbird-only sensitivity using a published 80% tongue-extension correction reversed participation: pooled rate ratio 0.229 (95% CI 0.147–0.355) and legitimate rate ratio 0.154 (0.087–0.271), while robbery-only counts remained unresolved. The continuous routing association was unchanged. An independent Afrotropical insect network showed the same route direction (rho=0.347), yielding rho_J=0.428. Relational mismatch therefore robustly predicts interaction routing, whereas filtering depends on functional reach rather than raw trait equality.

## Introduction

Access-restricting structures are usually treated as filters: if an exploiter cannot use the normal route, interaction frequency should decline. Flexible consumers can also change handling mode, attack site or route of entry. Flowers make this distinction explicit because structures that mediate legitimate pollination also confront robbers, thieves and other antagonists. Chemical and physical floral defences can deter some consumers while sparing others, and their effects change with exposure, consumer identity and context (Adler & Irwin 2005; Johnson et al. 2015; Lucas-Barbosa 2016; Rusman et al. 2018). A barrier may therefore reorganize interaction pathways as well as remove interactions.

We formalize this as an **effective access domain**. A legitimate visitor and an antagonist can differ in geometry, susceptibility, timing or attack route, so the same trait need not impose the same effective constraint on both. A selective defence is possible when antagonist use is restricted before legitimate visitation is impaired. But even a strong access constraint need not suppress antagonism if a bypass remains available. Instead, an exploiter can switch from using the legitimate opening to piercing, robbing or another alternative route.

This yields a simple prediction that is more general than any one floral defence:

> **As mismatch with the legitimate access route increases, exploitation should shift toward bypass routes; filtering and rerouting may occur separately or together.**

The component associations are already known. Aubert et al. (2026) showed that nectar robbing in Andean bird–flower interactions occurred mostly when bird bills were shorter than flower tubes. Sakhalkar et al. (2023) likewise found that long floral tubes or spurs can restrict thieving while being associated with robbing in Afrotropical visitor communities. Earlier direct studies also linked floral geometry to robbery in individual systems (Rojas-Nossa et al. 2016; Stanley & Cosnett 2021). Nor is behavioral switching itself new: legitimate visitation and robbing are established alternative handling tactics, and their relative efficiencies can depend on the bee–plant combination (Bronstein et al. 2017; Lichtenberg et al. 2018); floral traits can experimentally bias the relative use of those tactics (Leonard et al. 2013). The unresolved question is therefore not whether access geometry can correlate with cheating, or whether individuals can switch tactics. It is how **route composition and interaction occurrence separate along a relational mismatch axis**, whether the routing signal persists within consumer species rather than reflecting fixed consumer identity, and whether the same route-based estimand recurs across independently assembled faunas.

We address those distinctions rather than treating the two source datasets as discovery datasets. The all-Ecuador EPHI bird–flower network provides the primary test because its camera design permits both route composition and zero-inclusive participation to be reconstructed. After metadata-informed treatment of unspecified piercing records and trait matching, it contains 2,265 bird × plant × site units across 18 sites, aggregated to 259 plant species for primary inference (Aubert et al. 2026; EPHI public data). The Afrotropical insect–flower network of Sakhalkar et al. (2023) is an independent corroborative system with a different route contrast, robbing versus thieving among plant species.

Our analysis separates three estimands that previous trait–robbery associations do not by themselves distinguish. First, plant- and within-bird analyses ask whether mismatch predicts **route composition** as a relational consumer–resource property. Second, a zero-inclusive participation analysis, frozen before its effect was opened, asks whether the same barrier reduces resolved feeding visitation or whether legitimate use persists while route composition changes. Third, we place the bird and insect systems on one standardized rank-based routing scale with equal network weight, then use a frozen direct-study frame to locate null, opposite and mixed boundary cases. Source-audited floral-defence cases remain mechanistic context, not independent validation.

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

**P2. Participation versus routing.** Route composition and interaction occurrence are distinct margins. We therefore test whether the source-defined binary barrier changes zero-inclusive feeding participation, and separately ask whether that conclusion survives a functional-reach sensitivity for hummingbirds.

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

To test whether increased robbery merely reflected the composition of residual interactions after filtering, we froze a zero-inclusive participation analysis before opening its mismatch effect. Opportunities were clean EPHI camera waypoints (`camera_problem=no`) crossed with target bird species observed elsewhere at the same site during the focal camera interval; explicit `no_feeding` records were excluded from the count. The primary count pooled resolved legitimate and robbing feeding records while retaining the Letter's missing-piercing-as-legitimate rule. We fit a Poisson log-linear model with waypoint and bird-species fixed effects and a binary barrier term (tube length > culmen). Thus the barrier coefficient estimates a barrier/access rate ratio for resolved feeding visits, not robbery alone. Each clean waypoint maps to one plant identity, so tube length is constant within waypoint; waypoint fixed effects therefore absorb sampling effort and any time-invariant plant, tube-length or reward main effect. Identification of the barrier coefficient comes from differences among locally available bird species in whether their culmen falls below that waypoint's tube length, net of each bird species' baseline use. This is a different conditional grain from P1, where mismatch varies across flowers used by a bird and is aggregated toward plant-level route composition; P2 is not a second estimate of the same plant-level barrier contrast. The public EPHI tables contain no direct nectar-reward covariate, so bird-specific reward responses and within-deployment temporal reward variation remain potential confounders. Uncertainty used delete-one-plant-species jackknife intervals. Before opening the effect we froze a 0.80–1.25 equivalence margin and four outcome classes: no material participation loss, reduction plus routing, increase plus routing, or unresolved participation.

Because culmen length is not functional reach in hummingbirds, we later added an explicitly post-open Trochilidae-only sensitivity. Fixed reach multipliers transform mismatch as \(M_k=M-\log k\), so they cannot alter continuous ranks or move a fitted midpoint off the same support boundary; they can alter only binary barrier classification. We retained the source definition (\(k=1\)), a one-third tongue-extension sensitivity used in hummingbird networks (\(k=4/3\)), and a maximum-reach stress test (\(k=2\)). After this sensitivity was opened, a deeper literature audit recovered the 80% correction used as the primary network convention by Vizentin-Bugoni et al. (2016); we therefore report \(k=1.8\) explicitly as a post-open literature-anchored extension. *Diglossa* was excluded because a hummingbird tongue multiplier is not transferable to flowerpiercers.

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

### Functional reach reverses the participation inference

The preregistered source-defined barrier (tube length > culmen) contained 19,909 opportunity edges and gave higher pooled resolved-feeding visitation under barriers (rate ratio 1.772, 95% plant-jackknife CI 1.105–2.841). The post-open route split attributed this to legitimate/non-robbing feeding (1.883, 1.111–3.190), while robbery-only counts did not increase detectably (0.463, 0.147–1.461). These estimates should not be described as increased exploitation or robbery.

That no-filtering interpretation was not robust to functional reach. Restricting the sensitivity to Trochilidae and defining a barrier with the published 80% tongue-extension correction (tube > 1.8 × culmen) reduced the barrier fraction from 0.572 to 0.258 and reversed participation: pooled feeding rate ratio 0.229 (95% CI 0.147–0.355) and legitimate/non-robbing rate ratio 0.154 (0.087–0.271). Robbery-only counts remained unresolved (0.816, 0.359–1.857). The more conservative one-third extension gave the same qualitative filtering result (pooled 0.435, 0.255–0.741; legitimate 0.354, 0.197–0.635; robbery 0.851, 0.328–2.207).

The routing result itself was stable. Among hummingbirds, the plant-level continuous mismatch–robbery correlation remained \(\rho=0.503\) under every fixed multiplier because scaling translates all mismatch values equally. The paired binary robbery contrast strengthened from +0.091 at culmen-only equality to +0.259 across 105 plant species under the 80% reach correction (permutation \(p=0.0001\)). Fixed rescaling also translated the sigmoid midpoint and its support together, so the threshold remained boundary-limited rather than becoming an interior equality threshold.
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

The frozen OpenAlex frame contained 857 unique records and 33 eligible direct study programs: 22 positive, five null, four opposite and two mixed. Formal search added ten programs, including three opposite cases, so the frame did not merely reinforce the targeted literature. We report this finite direction distribution descriptively—without a prevalence estimate, sign test or pooled effect. A post hoc audit found that two opposite cases directly hardened bypass access; the remaining reversals or mixed cases left bypass cost unresolved or varied by context.

### Floral-defence cases provide mechanistic context, not independent validation

The 17-program defence corpus is retained only as mechanistic context. Its matched effective-domain classifications are author-coded and historically informed, so we do not treat them as independent validation or make an 11/11 success-rate argument.

## Discussion

### Access barriers reorganize interactions rather than simply suppress them

The central contribution is not the discovery that floral mismatch can accompany robbery; that association is already known. It is that **interaction route and interaction occurrence are distinct functional margins**. Relational mismatch predicts route composition within bird species and across the independent insect network (\(r_S=0.347\), \(r_A=0.503\), joint \(r_J=0.428\)), whereas whether mismatch filters feeding depends on how morphology is translated into functional access.

The standardized replication count remains \(k=2\). The 33-program formal frame broadens biological context but is not commensurate with the network statistic. Case et al. (2026) provide concordant directional evidence from 11 Hawaiian lobelioids and seven bird species, but we retain it as directional corroboration rather than a third standardized network contribution.

The zero-inclusive analysis reveals why raw trait equality should not be equated with functional access. Under the source-defined culmen threshold, barrier-classified opportunities appeared to preserve legitimate feeding. Hummingbirds, however, extend the tongue beyond the bill, and previous network studies have corrected effective reach accordingly. Once the barrier was defined using the published 80% extension, pooled and legitimate feeding were strongly reduced, while the continuous mismatch–robbery association was unchanged and the binary robbery contrast strengthened. Thus the robust result is not “routing without filtering.” Relational mismatch predicts route composition, whereas filtering emerges only when the binary classifier is tied more closely to functional reach. The robbery-only rate did not show a detectable absolute increase, so the shift toward robbery can be produced by suppression of the legitimate route rather than by more robbery events.

P1 and P2 still condition on different dimensions of the bird–plant matrix. P1 varies flowers within birds and asks whether mismatch predicts robbery share; P2 holds each waypoint plant fixed and obtains the participation contrast from differences among bird species at that flower, net of bird baseline use. The reach sensitivity resolves the apparent directional conflict without making the estimands identical: it changes which bird–waypoint pairs count as functionally constrained. Species-specific tongue extension, corolla opening and nectar depth remain unmeasured, so the reach-corrected analysis is a biological sensitivity rather than a newly identified universal threshold.

Within-bird ranks remained positive while bird-species means did not, showing that route use is a relational property of bird–flower matching rather than only a fixed consumer attribute.

The routing response remained graded rather than localized at trait equality: the sigmoid midpoint and 58.6% of bootstrap fits sat at the upper support boundary, and fixed reach multipliers translate the midpoint and support together rather than creating an interior threshold.

The same logic should apply beyond nectar robbing. Any ecological system with a constrained legitimate route and an available bypass can generate route switching: consumers can attack another tissue, enter from another side, change handling mode or exploit another stage. The general object is not a particular flower structure but the relation between consumer morphology or behavior and the accessible domain of the resource.

The relative-cost view clarifies some, but not all, reversals. This is an application of established foraging logic—relative efficiencies of legitimate and robbing tactics already vary among bee–plant combinations (Lichtenberg et al. 2018)—to the sign of trait–routing associations across systems, not a new theory of tactic choice. Geometry should promote robbery only when it raises legitimate-route cost more than bypass cost. Within the post hoc audit of the six non-positive programs, two opposite cases directly documented geometry that hardened robber entry; the remaining reversals left bypass cost unresolved or implicated additional behavioral context, and mixed programs varied across morphs or populations. This partition identifies plausible boundary mechanisms but, because cases were selected by frozen direction, does not show that the theory prospectively predicts every exception.

The evidence therefore supports a nested claim rather than a universal law. The two networks establish observational recurrence and the within-bird analyses show that routing varies within consumer species. The Ecuadorian participation sensitivity further shows that occurrence cannot be inferred from raw trait equality: reach-corrected barriers strongly suppress legitimate feeding even though the routing association persists. Relative route cost is the mechanistic interpretation that unifies routing with positive, null and opposite boundary cases. Generality beyond the analysed networks, species-specific functional reach, and causal sign reversal when bypass cost itself is manipulated remain prospective predictions.

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

Across an all-Ecuador bird–flower network and an independent Afrotropical insect network, stronger mismatch with the legitimate floral access route was associated with greater bypass use; the equal-network rank effect was \(r_J=0.428\) (permutation \(p=0.0001\)). In Ecuador, this routing signal persisted within bird species and was invariant to fixed hummingbird reach corrections.

The participation result depended on how access was defined. A preregistered culmen-only barrier suggested preserved feeding, but a post-open hummingbird sensitivity using a published 80% tongue-extension correction instead showed strong reductions in pooled and legitimate feeding. The robust ecological conclusion is therefore that **relational mismatch predicts interaction routing, while binary filtering depends on functional reach rather than raw trait equality**. Absolute robbery counts need not increase for robbery to become more prevalent when the legitimate route is constrained.

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
- Vizentin-Bugoni J, Maruyama PK, Debastiani VJ, Duarte LDS, Dalsgaard B, Sazima M (2016) Influences of sampling effort on detected patterns and structuring processes of a Neotropical plant–hummingbird network. *Journal of Animal Ecology* 85:262–272. https://doi.org/10.1111/1365-2656.12459
- Rojas-Nossa SV, Sánchez JM, Navarro L (2016) Nectar robbing: a common phenomenon mainly determined by accessibility constraints, nectar volume and density of energy rewards. *Oikos* 125:1044–1055. https://doi.org/10.1111/oik.02685
- Stanley DA, Cosnett E (2021) Catching the thief: Nectar robbing behaviour by bumblebees on naturalised *Fuchsia magellanica* in Ireland. *Journal of Pollination Ecology* 29:240–248. https://doi.org/10.26786/1920-7603(2021)620
- Coetzee A, Seymour CL, Spottiswoode CN, Pirie MD, van der Niet T (2026) Is bee-avoidance by bird-pollinated flowers driven by nectar robbing in *Erica*? *Functional Ecology* 40:1046–1060. https://doi.org/10.1111/1365-2435.70276
- Leal LC, Koski MH, Irwin RE, Bronstein JL (2025) Costs of floral larceny: a meta-analytical evaluation of nectar robbing and nectar theft on animal-pollinated plants. *Ecology* 106:e70036. https://doi.org/10.1002/ecy.70036
- Case SB, Hagemann ME, Drake DR, Postelli K, Pender RJ, Millikin PW, Rico-Guevara A (2026) Bird extinctions shift bill–flower trait matching in Hawaiian lobelioids. *Functional Ecology* 40:2972–2981. https://doi.org/10.1111/1365-2435.70415
