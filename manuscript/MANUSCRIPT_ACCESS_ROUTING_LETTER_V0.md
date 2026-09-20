# Access constraints reroute floral exploitation across bird and insect visitor networks

**Ecology Letters Letter candidate v0**

## Abstract

Access constraints may reroute exploitation rather than eliminate it. We test this prediction primarily in an all-Ecuador bird–flower network and then ask whether a smaller independent insect network recovers the same direction. Across 1,378 bird × plant × site units, robbery was higher when flower tubes exceeded bird bills (0.307 versus 0.081); site-adjusted tube–bill mismatch correlated with robbery (\(\rho=0.351\), within-site permutation \(p=0.0001\)), with the same direction in 15 of 17 comparable sites. In an Afrotropical insect network, floral tube length was associated with a shift from thieving toward robbing among 57 plant species (\(\rho=0.347\), \(p=0.0086\)), although multitrait sensitivity did not isolate tube length uniquely. An equal-network joint test gave \(\rho_J=0.349\), \(p=0.0001\). Thus access constraints can reorganize interaction routes, while \(k=2\) limits claims about broader network generality.

## Introduction

Biological structures that restrict access are often interpreted as barriers: if an exploiter cannot use the normal route, interaction frequency should decline. This logic appears throughout consumer–resource ecology, from prey defences to host barriers and floral architectures. Yet many antagonists are behaviorally flexible. They can change handling mode, attack site or route of entry, turning a barrier from a simple filter into a device that reorganizes interaction pathways.

Flowers provide a particularly clear setting for this problem. The same reproductive structures must remain accessible to mutualists while limiting florivores, nectar robbers, thieves, seed predators and other exploiters. Floral chemistry, sticky surfaces, water-filled bracts, hairs, slippery tissues and geometric barriers can all reduce antagonist use, but their consequences for legitimate visitors vary widely (Johnson et al. 2015; Lucas-Barbosa 2016; Rusman et al. 2018). Nectar secondary compounds can selectively deter some consumers while being tolerated by others (Adler & Irwin 2005; Gegear et al. 2007; Barlow et al. 2017), and the same trait can change from selective to interfering as dose or exposure increases (Galen et al. 2011; Jones & Agrawal 2016). These observations suggest that a trait's ecological effect depends less on its broad category than on which consumers actually encounter it, through what route, and at what intensity.

We formalize this as an **effective access domain**. A legitimate visitor and an antagonist can differ in geometry, susceptibility, timing or attack route, so the same trait need not impose the same effective constraint on both. A selective defence is possible when antagonist use is restricted before legitimate visitation is impaired. But even a strong access constraint need not suppress antagonism if a bypass remains available. Instead, an exploiter can switch from using the legitimate opening to piercing, robbing or another alternative route.

This yields a simple prediction that is more general than any one floral defence:

> **As mismatch with the legitimate access route increases, exploitation should shift toward bypass routes rather than merely decline.**

Existing floral studies support pieces of this logic, but the prediction has not been tested as a common standardized association across independently assembled visitor networks with different faunas. We therefore use the all-Ecuador EPHI bird–flower network as the primary quantitative test because it contains 1,378 trait-matched bird × plant × site units across 18 sites and supports both binary barrier and continuous mismatch contrasts (Aubert et al. 2026; EPHI public data). We then use the smaller Afrotropical insect–flower network of Sakhalkar et al. (2023) as an independent corroborative test on a different cheating contrast: robbing versus thieving among plant species.

Our analysis has two levels. We first test the routing prediction within the Ecuadorian network and ask whether the independent insect network recovers the same directional association on its native biological scale. We then define one standardized rank association per network and combine them with equal network weight in a predeclared permutation test. This prevents the much larger bird dataset from dominating the smaller insect dataset by observation count alone. Source-audited floral-defence cases are used only as mechanistic context for the access/exposure interpretation, not as an independent validation dataset.

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

This prediction is compatible with the broader effective-exposure framework developed for floral defence selectivity. There, a selective window exists when the antagonist experiences a focal trait strongly enough to be suppressed before the legitimate visitor crosses its own interference threshold. Bypass is a boundary condition: if the antagonist does not traverse the defended domain, effective exposure to the focal defence falls even as exploitation persists.

The network test focuses only on the route-switching consequence. It does not require the access constraint itself to have evolved as a defence, nor does it assume a shared physiological mechanism across insects and birds.

We test three predictions.

**P1. Bird access barriers.** Across bird–plant interactions, flowers whose tubes exceed visitor bill length should experience greater robbery, and continuous tube–bill mismatch should be positively associated with robbery rate.

**P2. Insect route switching.** Across plant species, stronger floral access constraint should be associated with a shift from nectar thieving through the floral opening toward nectar robbing by bypass.

**P3. Cross-network recurrence.** After converting each network to a rank-based association between access constraint and bypass propensity, the two network effects should be positive and their equal-network joint statistic should exceed a null generated by network-appropriate permutations.

## Methods

### Primary Ecuadorian bird–flower test

Aubert et al. (2026) analysed nectar robbing as a consequence of trait mismatch between flowers and avian visitors. Anonymous file-byte retrieval from the paper's Dryad archive was blocked in our CI environment, but the broader Ecuador EPHI dataset is publicly mirrored on Zenodo. We therefore conduct an independent all-Ecuador extension rather than an exact replication of the source three-transect mixed-effects model.

The mirror contains 54,471 interaction rows, 6,198 camera records, 4,371 plant-trait records and 10,988 hummingbird-trait records across 18 Ecuador sites. Resolved interactions were joined through camera waypoints to plant species and sites and then to floral and bird traits. Plant tube length is recorded in centimetres and culmen length in millimetres; culmen length was converted to centimetres before comparison.

For each bird–plant pair within site, we calculated

\[
M=\log(T/B),
\]

where \(T\) is flower tube length and \(B\) mean bird culmen length. Positive \(M\) indicates that the flower tube exceeds bill length. We also defined a binary access barrier as \(T>B\).

Individual interactions were aggregated to bird species × plant species × site units. After trait matching, 1,378 pair-site units remained across 18 sites. We calculated robbery rate within each unit.

The primary native-scale analyses were (i) the difference in mean robbery rate between barrier and accessible pair-sites and (ii) the Spearman association between continuous mismatch and robbery rate. Permutation tests used 9,999 iterations. We also compared barrier and accessible states within sites and repeated the analysis after requiring at least two or at least five resolved interactions per pair-site unit.

### Independent Afrotropical insect corroboration

We reanalysed the public dataset of Sakhalkar et al. (2023), which records flower visitors, cheating behavior and floral traits in Afrotropical forests. The current Zenodo workbook contains 18,440 visitation rows. Following the source analysis, rows coded as generic visiting behavior were excluded, leaving 14,383 analysed rows in the deposited file. This is eight fewer than the 14,391 visits reported in the publication summary; we use the deposited data as currently available rather than forcing equality.

Visit frequencies were aggregated to plant species before inference. For each species with tube-length data and at least one robbing or thieving interaction, we calculated

\[
B_i=
\frac{R_i-T_i}{R_i+T_i},
\]

where \(R_i\) is robbing frequency and \(T_i\) thieving frequency. Thus \(B_i=1\) denotes robbery only and \(B_i=-1\) thieving only. Fifty-seven plant species met these criteria.

We tested the association between floral tube length and \(B_i\) with Spearman rank correlation and a fixed-seed two-sided permutation test using 9,999 permutations. Plant species were the inferential units; individual visits were not treated as independent replicates.

Because tube length can covary with other floral traits, we also retained the source paper's parsimonious robber predictor set—tube length, tube width and flower shape—in a robustness analysis. This sensitivity is used only to set the claim ceiling on tube length as an independent predictor.

### Joint cross-network test

The two datasets differ in response scale and inferential unit, so raw observations were not pooled. Instead, each network contributed one standardized rank association in the same biological direction:

\[
\text{access constraint}
\longrightarrow
\text{bypass propensity}.
\]

For Sakhalkar, the effect was the Spearman correlation between tube length and robbing–thieving balance.

For Aubert/EPHI, global ranks of \(M\) and robbery rate were centered within site before correlation. This removes site-specific rank means so among-site composition does not define the network contribution. The unadjusted global correlation was retained only as a descriptive reference.

Because the two datasets represent two independent networks rather than 1,435 interchangeable sampling units, they received equal weight. The primary joint effect was the Fisher-z mean,

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

The permutation null preserved each dataset's sampling structure. In Sakhalkar, bypass-response values were shuffled across plant species. In Aubert/EPHI, robbery-rate ranks were shuffled within site. For every permutation, both network correlations and the equal-network joint effect were recomputed. We used 9,999 permutations and a two-sided test.

### Mechanistic corroboration from floral-defence systems

The network analysis tests route switching rather than the evolutionary origin of floral barriers. To evaluate whether its interpretation is compatible with independent floral-defence evidence, we use an existing source-adjudicated corpus assembled under a frozen same-trait evidence contract.

The broad defence-side corpus contains 17 unique study programs spanning chemical, physical and reward/access implementations. A stricter matched-system layer classifies each focal defence by effective access/exposure architecture—separated, transitional, overlapped or bypass—and records pollinator outcomes separately from architecture coding. Heterogeneous endpoints are not pooled into a common effect size. We use this layer only as mechanistic corroboration and not as the primary inferential test of the Letter.

## Results

### Primary Ecuadorian test: access mismatch predicts robbery

The Ecuadorian network showed the same routing direction. Mean robbery rate was 0.307 when flower tubes exceeded bird bills and 0.081 when they did not, a difference of +0.226 (\(p_{\mathrm{perm}}=0.0001\)).

Continuous mismatch was also positively associated with robbery rate across all 1,378 pair-site units,

\[
\rho_{\mathrm{global}}=0.4183,
\qquad
p_{\mathrm{perm}}=0.0001.
\]

The pattern was not generated solely by among-site composition. Seventeen sites contained both barrier and accessible pair-sites; 15 showed higher robbery under the barrier state. The mean within-site difference was +0.144, the two-sided sign-test \(p=0.00235\), and the site-stratified permutation \(p=0.0001\).

The result also persisted when sparsely observed pair-site units were removed. Requiring at least five interactions left 702 units, with mean robbery rates of 0.320 under barriers and 0.0556 when accessible; mismatch and robbery remained positively associated (\(\rho=0.505\), permutation \(p=0.0001\)). At the cross-network level, the equal-network joint effect also persisted under this filter (\(r_J=0.385\), permutation \(p=0.0001\)).

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

After removing site-specific rank means, the Aubert/EPHI effect was

\[
r_A=0.3505
\]

with within-site permutation \(p=0.0001\). The close agreement between independently assembled datasets was not imposed by sample-size weighting.

The equal-network Fisher-z mean was

\[
\boxed{r_J=0.3487}
\]

and the two-sided joint permutation test gave

\[
\boxed{p_{\mathrm{joint}}=0.0001}.
\]

Both observed network effects were positive. Under the joint permutation null, the probability that both permuted effects were positive was 0.2536, close to the 0.25 expectation for two approximately symmetric directional nulls.

Thus the strongest empirical result is not merely that each source dataset contains an access association. A common standardized prediction is recovered at nearly the same rank-effect magnitude in an insect network and a bird network.

### Floral-defence cases provide mechanistic context, not independent validation

The broader defence-side corpus contains 17 unique study programs: nine chemical, seven physical and one reward/access implementation. Ten studies also measured pollinator consequences under the same focal defence, and those outcomes were heterogeneous rather than showing one fixed pollinator penalty. Eight independent systems additionally show within-trait state changes with dose, cumulative exposure, consumer identity, response stage or timing.

The matched effective-domain classifications are author-coded from source descriptions, and historical systems contributed to development of the framework. They have not yet undergone outcome-blinded independent recoding. We therefore do not use the matched-domain layer as an independent validation dataset, report no inter-rater agreement statistic, and do not make an 11/11 success-rate argument in this Letter.

These cases motivate the access/exposure mechanism and its experimental predictions. The quantitative inferential contribution of the Letter is the Ecuadorian network test, the independent insect corroboration, and their equal-network joint statistic.

## Discussion

### Access barriers reorganize interactions rather than simply suppress them

The central result is a cross-fauna recurrence of the same routing prediction. Insects and birds differ radically in body size, sensory biology, handling behavior and floral interactions, and the two public datasets were assembled independently for different purposes. Yet after expressing each system as a rank association between access constraint and bypass propensity, their effects were nearly identical: \(r_S=0.347\) and \(r_A=0.351\). The equal-network joint effect was \(r_J=0.349\).

This changes the interpretation of floral barriers. A structure that makes the normal route difficult does not necessarily terminate exploitation. If an alternative route remains profitable, the ecological response can be behavioral rerouting. Nectar robbing is therefore not merely residual exploitation that survives a failed barrier; it can be the expected interaction mode when access through the legitimate floral opening becomes mismatched.

The same logic should apply beyond nectar robbing. Any ecological system with a constrained legitimate route and an available bypass can generate route switching: consumers can attack another tissue, enter from another side, change handling mode or exploit another stage. The general object is not a particular flower structure but the relation between consumer morphology or behavior and the accessible domain of the resource.

### A relational view clarifies floral defence selectivity

The source-audited defence corpus is used here only as mechanistic context, not as a validation dataset. It helps explain why broad labels such as chemical versus physical defence are insufficient: the same nominal defence can be selective at one exposure and interfering at another, and physically similar structures can affect consumers differently depending on body size, timing or attack route.

In the effective-exposure view, a defence is selective when antagonists cross their response threshold before legitimate visitors do. Bypass is a limiting case: if antagonists stop traversing the defended domain, effective exposure to the focal defence falls even as exploitation persists. The network result provides a community-scale manifestation of that boundary condition.

This also explains why a barrier can simultaneously reduce one antagonistic mode and increase the relative importance of another. Measuring only total visitation or total damage can therefore miss an important ecological response. Future studies should distinguish legitimate use, thieving, robbing and other handling modes rather than treating all antagonist interactions as one count.

### What the joint test does—and does not—establish

The joint analysis was designed to test recurrence without pretending that the two datasets share a raw effect scale. Plant species in the Sakhalkar network and bird × plant × site units in the Ecuadorian network are not interchangeable observations. Equal network weighting therefore reflects the scientific question—whether the same directional relationship appears in independent networks—rather than the relative row counts in the underlying datasets.

The joint statistic contains only \(k=2\) independent network-level contributions. Its permutation \(p\)-value tests whether these two networks jointly show a stronger standardized routing signal than their network-specific nulls; it does not estimate between-network heterogeneity, a population-level mean across ecological networks, or generality beyond the two network systems analysed here. Broader generality remains a prediction for replication across additional independent networks.

The result remains observational. Floral tube length was not randomly assigned, and correlated morphology prevents a unique tube-length claim in the insect network. The Ecuador analysis is an all-site extension using the public EPHI mirror, not an exact reconstruction of Aubert et al.'s three-transect mixed model. Our claim is consequently about a recurrent rank-based routing association, not a universal causal coefficient.

The matched floral-defence material is mechanistic context rather than independent validation. Historical systems contributed to development of the effective-domain framing, the domain coding has not yet been outcome-blind independently replicated, null-compatible outcomes are not equivalence tests, and the strict direction-supported matched subset remains small. These limitations are precisely why the network analyses—not the matched-domain alignment—carry the inferential contribution of the Letter.

### Predictions

The routing framework generates direct experimental tests.

First, manipulating access geometry while keeping reward constant should change the ratio of legitimate entry to bypass behavior. A graded manipulation should be especially informative: the model predicts not merely fewer interactions but a shift in route composition as access mismatch increases.

Second, the effect should depend on whether a viable bypass exists. Closing both legitimate and bypass routes should reduce total exploitation, whereas selectively constraining only the legitimate route should increase the relative frequency of bypass.

Third, consumer morphology should interact with floral geometry. The same flower should produce different route choices among visitors with different access phenotypes, providing a direct test of the effective-domain mechanism.

Finally, defence experiments should measure pollinator response and antagonist route simultaneously. Our literature audit found abundant antagonist-focused work but much thinner pollinator-side follow-up for physical barriers, leaving exactly the experiments needed to connect route switching to selective defence.

## Conclusion

Across an all-Ecuador bird–flower network and an independent Afrotropical insect network, stronger constraint on the legitimate floral access route is associated with greater bypass exploitation. A joint equal-network rank test yields \(r_J=0.349\) with permutation \(p=0.0001\). Source-audited floral-defence cases provide mechanistic context for access and exposure dependence rather than an independent validation claim.

The ecological implication is simple: **barriers do not only filter interactions; they can reroute them.** Treating access architecture as a determinant of interaction mode provides a general, testable way to connect floral defence, cheating behavior and mutualist–antagonist trade-offs without assuming that one trait has one fixed ecological effect.

## Data accessibility and reproducibility

The analyses use public data from Sakhalkar et al. (2023; Zenodo DOI 10.5281/zenodo.8398202) and the EPHI Ecuador mirror (Zenodo DOI 10.5281/zenodo.14185547) associated with the trait-matching framework of Aubert et al. (2026). Aggregate analysis outputs, source-audited evidence registries, tests and workflows are maintained in the project repository. Raw species and site identifiers are not emitted by the joint aggregate workflow.

## References

Use the focused BITA reference pool and retain the primary network sources:

- Sakhalkar SP et al. 2023. *Ecosphere* 14:e4696. DOI 10.1002/ecs2.4696.
- Aubert S et al. 2026. *Oikos* 2026(3):e11552. DOI 10.1002/oik.11552.
- Johnson MTJ, Campbell SA, Barrett SCH. 2015.
- Lucas-Barbosa D. 2016.
- Rusman Q, Lucas-Barbosa D, Poelman EH. 2018.
- Adler LS, Irwin RE. 2005.
- Gegear RJ, Manson JS, Thomson JD. 2007.
- Barlow SE et al. 2017.
- Galen C et al. 2011.
- Jones PL, Agrawal AA. 2016.
