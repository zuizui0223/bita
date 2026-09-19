# Access and exposure domains organize floral defence selectivity and interaction routing across plant–visitor systems

**Candidate refocused BITA manuscript v0 — not yet canonical**

**Paper type:** comparative macro-ecological synthesis + public-data reanalysis

**Authors and affiliations:** [Author-controlled]

## Abstract

Flowers must remain accessible and attractive to mutualists while limiting antagonists that use the same reproductive structures and rewards. Floral defence is therefore often described as a trade-off, yet the same chemical or physical trait can suppress antagonists, interfere with pollinators, or fail when exploiters bypass it. We develop a simple effective-exposure theory in which a focal defence/access axis of intensity \(x\) is experienced by antagonists and pollinators through channel-specific coefficients \(q_H\) and \(q_P\), with response thresholds \(\tau_H\) and \(\tau_P\). A selective window exists when \(\tau_H/q_H < x < \tau_P/q_P\): the antagonist channel is suppressed before pollinator interference begins. The framework predicts selective states under separated access or susceptibility, interference under strong overlap, loss of defence under bypass, and within-system switching as dose or exposure crosses response thresholds. We tested these predictions using three evidence layers. A source-adjudicated matched-defence corpus contains 17 independent systems; 15 have an effective antagonist-reduction route. The strict direct pollinator subset remains small: two separated systems show preserved or improved pollinator function, whereas one overlapped system shows impairment. However, a broader ecological-state analysis is more informative: all nine scorable historical systems and both systematic-expansion systems matched the fixed architecture prediction that separated domains show no observed pollinator interference, transitional domains show mixed responses, and overlap shows impairment. A coarse defence-modality classifier recovered only 6/9 historical systems in leave-one-out prediction and 1/2 expansion systems. Four separated historical systems contributing to state recovery are null-compatible rather than equivalence-supported, so the broader result is a qualitative state analysis rather than proof of zero pollinator cost. Eight independent defence-side systems also show recurrent switching with dose, cumulative exposure, consumer identity, response stage, or temporal expression. Fourth, reanalysis of the public Sakhalkar et al. (2023) Afrotropical visitor network showed that floral tube length is associated with cheating route among 57 plant species (\(\rho=0.347\), permutation \(p=0.0086\)): longer tubes shift exploitation from thieving through the floral opening toward nectar robbing by bypass. Across case, within-system, and community scales, floral defence selectivity is best treated as a state of trait × consumer × context. Existing BITA identification results remain as claim discipline: these patterns support a recurrent access/exposure mechanism but not a universal causal coefficient or prevalence estimate.

**Keywords:** floral defence; pollination; nectar robbing; florivory; trait matching; interaction networks; visitor filtering; ecological antagonism

## 1. Introduction

Flowers mediate opposing ecological demands. Traits that advertise rewards or permit access can increase pollination, but the same flowers are exposed to florivores, nectar robbers, nectar thieves, seed predators, ovipositing herbivores, and other exploiters. Conversely, traits that reduce antagonist use can interfere with legitimate visitors because both functional groups encounter the same floral surface, reward, volatile, or opening (Johnson et al. 2015; Lucas-Barbosa 2016; Rusman et al. 2018).

This conflict has often been summarized as a pollination–defence trade-off (Kessler & Halitschke 2009; Johnson et al. 2015). That description is incomplete. Floral defence is not uniformly costly to mutualists. Nectar secondary compounds can strongly deter some visitors while being tolerated by others (Adler & Irwin 2005; Gegear et al. 2007; Barlow et al. 2017). Physical barriers can block one attack route while leaving another route accessible. Sticky surfaces can suppress florivores but also trap beneficial insects. The same chemical can be selective at one dose and broadly deterrent at another (Galen et al. 2011; Jones & Agrawal 2016; Villalona et al. 2020). An apparently strong barrier can also fail if an antagonist simply bypasses it.

These examples suggest that the important ecological object is not defence class alone. What matters is whether the focal antagonist and legitimate pollinator actually experience the same effective domain of the trait. “Domain” here is deliberately broad. It can be biochemical susceptibility, spatial access, attack route, cumulative exposure, temporal overlap, visitor functional mode, or the response stage at which the interaction is measured.

We formalize this idea as an effective-exposure threshold model (Fig. 1). The model generates four testable states: separated domains should create a selective window; overlapping domains should narrow or close that window; bypass should eliminate the focal antagonist-reduction effect; and increasing exposure should move systems from ineffective to selective to pollinator-interfering states. A related access prediction is that barriers need not eliminate exploitation: if a bypass route exists, increasing mismatch can shift animals from use of the legitimate opening toward robbery.

We test these predictions using four linked evidence layers. First, we deduplicate the legacy D-side route corpus at the study-program level and quantify implementation breadth, pollinator-follow-up coverage, and pollination-state heterogeneity. Second, we construct a stricter matched-defence corpus in which one flower-associated defence or access axis is linked to both antagonist and pollinator outcomes within the same study system. Third, we recover within-system state transitions from earlier BITA evidence on dose, exposure, consumer identity, response stage, and temporal expression. Fourth, we independently reanalyse a public Afrotropical flower-visitor dataset to ask whether floral tube length predicts the balance between nectar thieving through the floral opening and nectar robbing by bypass.

This refocus preserves rather than discards earlier BITA results. The previous 56-route / 25-cluster synthesis established recurrence of attraction, antagonism, defence, and pollination pathways; direct attraction-by-defence factorials showed context-dependent interaction signs; and the identification framework showed that a total trait interaction does not uniquely identify an ecological channel allocation. Those results remain important, but here they become the evidential and inferential foundation for a biological question: **what ecological architecture makes floral defence selective?**

## 2. Effective-exposure theory

Let \(x\ge0\) denote the expressed intensity of a focal defence or access trait. Let \(q_H\) and \(q_P\) describe how strongly the antagonist and pollinator channels effectively experience that trait. These coefficients can summarize susceptibility, access geometry, attack route, time overlap, cumulative exposure, or functional mode.

We write effective exposure as

\[
z_H=q_Hx,\qquad z_P=q_Px.
\]

Let \(\tau_H\) be the effective exposure required to suppress antagonist use and \(\tau_P\) the exposure at which pollinator interference begins. The corresponding trait-intensity thresholds are

\[
x_H^*=\frac{\tau_H}{q_H},\qquad
x_P^*=\frac{\tau_P}{q_P}.
\]

A selective window exists when

\[
\boxed{x_H^*<x_P^*}
\]

and realised expression falls between the thresholds:

\[
\boxed{x_H^*<x<x_P^*.}
\]

Within this interval the antagonist channel is suppressed before pollinator interference is triggered.

### 2.1 Separated domains

If antagonists are more exposed or susceptible than legitimate pollinators, \(q_H\gg q_P\), the antagonist threshold falls relative to the pollinator threshold and the selective window widens. Separation can arise through body size, geometry, timing, attack route, biochemical tolerance, or visitor functional mode.

**Prediction 1:** effective antagonist-reducing traits with separated domains should more often retain pollinator-compatible states.

### 2.2 Overlap

If antagonists and pollinators experience similar exposure, \(q_H\approx q_P\), selectivity depends mainly on their response thresholds. If those thresholds are similar, the selective window is narrow or absent.

**Prediction 2:** strong overlap should increase the likelihood that an antagonist-reducing state also interferes with pollination.

### 2.3 Bypass and tolerance

If antagonists bypass the defended route or are effectively insensitive, \(q_H\rightarrow0\), then \(x_H^*\rightarrow\infty\).

**Prediction 3:** conspicuous traits can fail as focal defences when antagonists do not traverse the defended domain.

### 2.4 State transitions

Increasing \(x\) gives an ordered sequence:

~~~text
x < x_H*
    focal defence ineffective

x_H* < x < x_P*
    selective / guarded window

x > x_P*
    antagonist suppressed + pollinator interference
~~~

**Prediction 4:** increasing dose, cumulative exposure, or response-stage exposure can close an initially selective window without changing the broad defence class.

### 2.5 Route switching

An access barrier need not eliminate antagonistic use. Let \(L\) denote access through the legitimate floral opening and \(B\) a bypass route. If legitimate access falls as geometric mismatch increases but \(B\) remains available, exploitation can switch route rather than disappear.

**Prediction 5:** increasing floral access constraint should shift cheating from thieving through the normal opening toward nectar robbing by bypass.

## 3. Methods

### 3.1 Evidence architecture and preservation of prior BITA results

The source-adjudicated BITA evidence base contains 56 directional route records from 25 historical cluster labels. A stricter earlier audit retained 17 high-information systems for mechanism-identification questions. Those files remain unchanged and serve as provenance. Before route-level macro analysis, we re-audited D-side independence by DOI and study identity. One Takeda 2021 experiment had entered the legacy ledger under two cluster labels through separate ingestion paths; the macro lane therefore uses 17 unique D-to-antagonism study programs rather than the historical count of 18 labels.

For the present analysis we built a new matched-defence layer under empirical/floral_defence_selectivity/. The primary unit is

~~~text
one independent study cluster
× one flower-associated defence/access axis
× one declared ecological context.
~~~

Repeated outcomes, doses, years, populations, consumers, or reproductive endpoints do not automatically create independent replication.

### 3.2 Matched-defence eligibility

A system was admitted to the primary matched-D corpus only when the focal trait had an independently supported antagonist-reducing role and both antagonist and legitimate-pollinator or pollination-function information were available for the same biological system under the frozen evidence contract.

Architecture information and outcome information were stored separately. Domain classification was not back-filled from the desired outcome. Architecture states were:

~~~text
SEPARATED
OVERLAPPED
BYPASS_TOLERANCE
TRANSITIONAL
UNCLEAR
~~~

We additionally recorded the separating coordinate, defence modality, antagonist guild, pollinator guild, design class, and coding origin.

Pollinator outcomes were coded as:

~~~text
PRESERVED_OR_IMPROVED
IMPAIRED
NO_DETECTED_CHANGE
MIXED
UNRESOLVED
~~~

A non-significant contrast was not treated as equivalence. NO_DETECTED_CHANGE therefore remained distinct from PRESERVED_OR_IMPROVED.

### 3.3 Corpus cohorts

To control circularity, systems were separated into:

~~~text
historical derivation
systematic expansion
registered hold-out
~~~

The current matched-D registry contains 14 historical systems, two systematic-expansion systems, and one hold-out.

Targeted searches were used only to fill missing Stage-2 cells. The eligibility rule was not relaxed after candidate outcomes were seen. Linked multi-paper programmes and systems failing the antagonist-benefit or same-D gate were retained as context rather than added to strict N.

### 3.4 Strict Stage-2 model gate

The strict Stage-2 comparison included only systems satisfying:

~~~text
antagonist route = EFFECTIVE
domain = SEPARATED or OVERLAPPED
pollinator state = PRESERVED_OR_IMPROVED or IMPAIRED
~~~

Because only three systems currently satisfy this gate, we preclude a high-dimensional meta-regression. We report the 2×2 table and a two-sided Fisher exact test.

A secondary sensitivity includes separated systems with NO_DETECTED_CHANGE on the pollinator side as “compatible-or-null”, but these systems are not reclassified as equivalence-supported preservation.

We also explicitly test whether domain relation and broad defence modality are separable in the strict subset. If they are perfectly confounded, no comparison claiming that domain structure outperforms chemical-versus-physical class is permitted.

### 3.5 Defence-side conditionality

We filtered the existing BITA sign-switch ledger to defence-side systems. Eight independent study clusters were retained. State switches were classified by their principal changing ecological axis: dose/expression, cumulative exposure or reward context, consumer identity, response stage, or temporal expression.

We did not pool heterogeneous outcome metrics into a synthetic effect size. The aim was recurrence of ordered state transitions, not a universal threshold ratio.

### 3.6 Sakhalkar community-network reanalysis

Sakhalkar et al. (2023) provide public data and code for Afrotropical flower-visitor communities. We retrieved the public Zenodo archive and independently audited its workbook structure.

The main visitation sheet contained 18,440 data rows. Following the source R script, rows coded as behavior == "visiting" were excluded, leaving 14,383 analysed records in the deposited workbook. This is eight fewer than the 14,391 visits stated in the published summary; we use the deposited data as currently available rather than forcing agreement.

For each plant species we summed the source-normalized frequencies of robbing and thieving. For species with both tube-length information and at least one cheating route, we defined

\[
B_i=
\frac{R_i-T_i}{R_i+T_i},
\]

where \(R_i\) is robbing frequency and \(T_i\) thieving frequency. \(B_i=1\) denotes all robbery, \(B_i=-1\) all thieving.

We tested the association between tube length and \(B_i\) with a species-level Spearman correlation. A fixed-seed two-sided permutation test used 9,999 permutations. The species, not individual visits, were the inferential units.

## 4. Results

### 4.1 The broader D-side corpus spans implementation classes and heterogeneous pollinator consequences

After deduplicating the repeated Takeda 2021 study identity, the legacy D-side route corpus contains 17 unique study programs. Sixteen provide direction-supported antagonist-reduction evidence and one, *Impatiens capensis*, remains unresolved.

The 17 programs span three broad implementation classes:

~~~text
chemical       9
physical       7
reward/access  1
~~~

Same-study pollinator consequences were measured in 10 of the 17 programs (58.8%). Follow-up coverage was 7/9 for chemical defences, 2/7 for physical defences, and 1/1 for the reward/access system. The chemical-versus-physical follow-up imbalance was not conventionally significant (Fisher two-sided \(p=0.126\)), but it reveals that the evidence base is much richer in pollinator-side measurement for chemical than for physical defences.

Among the 10 programs with D-to-pollination information, pollinator responses were not dominated by a single fixed penalty:

~~~text
CONTEXT_DEPENDENT  4
NULL_COMPATIBLE    3
IMPROVED           1
INTERFERENCE       1
UNRESOLVED         1
~~~

The context-dependent programs comprise dose/expression dependence in *Polemonium*, cumulative-exposure dependence in *Asclepias*, response-stage dependence in *Nicotiana*, and separated dose thresholds in *Aconitum*. The null-compatible programs are *Ipomopsis*, *Pedicularis*, and *Catalpa*; *Thunia* provides the improved/routing state; high-gelsemine *Gelsemium* provides the fixed interference state.

These counts describe the source-adjudicated evidence base rather than natural prevalence. D-role admission itself is conditioned on antagonist-reduction evidence. Their macro-ecological value is therefore in showing implementation breadth and heterogeneity of mutualist consequences, not estimating how often selective defence occurs in nature.

### 4.1 Effective-domain architecture recovers qualitative pollinator state across systems

The matched-D registry contains 17 independent systems. Fifteen have an effective focal antagonist-reduction route (Fig. 2).

For the broader macro state-recovery analysis, pollinator outcomes were reduced to three explicitly heterogeneous state families:

~~~text
PRESERVED_OR_IMPROVED / NO_DETECTED_CHANGE
    -> NO_INTERFERENCE_OBSERVED

MIXED
    -> MIXED

IMPAIRED
    -> IMPAIRED
~~~

The first category does not equate a null-compatible result with equivalence; it records only that interference was not detected on the source outcome.

Nine historical systems were scorable under the fixed domain-state mapping:

~~~text
SEPARATED    -> NO_INTERFERENCE_OBSERVED
TRANSITIONAL -> MIXED
OVERLAPPED   -> IMPAIRED
~~~

All nine were recovered by that rule. Given the observed fixed category margins (4 separated, 4 transitional, 1 overlapped), one perfect allocation has probability \(1/630=0.00159\) under random reassignment. Because these historical systems contributed to theory formation, this value is descriptive rather than confirmatory.

As a coarse comparator, leave-one-out prediction from broad defence modality recovered 6/9 historical systems. The derivation-set modality rule classified chemical systems as MIXED, physical and reward-access systems as NO_INTERFERENCE_OBSERVED, with MIXED as the fallback.

Two post-rule systematic-expansion systems were also scorable. *Caryopteris* and *Phlox* both matched the domain-state prediction (2/2), whereas the derivation-trained modality classifier recovered only *Caryopteris* (1/2). Their architecture coding was source-mechanistic/post hoc rather than prospectively blinded, so this remains post-rule corroboration rather than independent confirmation.

The registered *Erica* hold-out is coded SEPARATED and has a positive pollination direction, but remains DIRECTION_ONLY / UNRESOLVED and is therefore not scored.

Across the 11 scorable historical + expansion systems, the state mapping is 11/11 aligned:

~~~text
SEPARATED     6 -> NO_INTERFERENCE_OBSERVED 6
TRANSITIONAL  4 -> MIXED                    4
OVERLAPPED    1 -> IMPAIRED                 1
~~~

The corresponding fixed-margin perfect-allocation probability is \(1/2310=0.000433\), again retained only as a descriptive alignment statistic.

The strict direction-supported Stage-2 subset is nested within this broader state analysis and contains only three systems:

~~~text
                         compatible   impaired
SEPARATED                     2           0
OVERLAPPED                    0           1
~~~

The two separated systems are *Thunia alba* (Wu & Gao 2024) and *Caryopteris divaricata* (Tie et al. 2023). The overlapped interference state is high-gelsemine *Gelsemium sempervirens* (Adler & Irwin 2005).

The two-sided Fisher exact test is

\[
p=0.333.
\]

The strict result is therefore directionally coherent but not an inferentially decisive cross-system contrast. Its role is high-specificity confirmation of the state labels, not the primary macro-scale sample size.

Four additional separated systems—*Catalpa speciosa* (Stephenson 1982), *Pedicularis rex* (Sun & Huang 2015), *Ipomopsis aggregata*, and *Phlox paniculata* (Junker et al. 2011)—combine an effective antagonist route with a null-compatible pollinator contrast. If these are included only as a weaker “compatible-or-null” sensitivity, the table becomes

~~~text
                         compatible-or-null   impaired
SEPARATED                           6              0
OVERLAPPED                          0              1
~~~

with Fisher \(p=0.143\).

These four systems remain null-compatible rather than equivalence-supported and are not counted as strict preservation.

The strict systems also perfectly confound domain relation with broad modality: the two separated strict systems are physical, whereas the overlapped strict system is chemical. Consequently, the present data do not identify whether domain relation predicts strict pollinator state better than chemical-versus-physical category.

### 4.3 Bypass can eliminate focal defence efficacy

The explicit BYPASS_TOLERANCE boundary is the *Salvia* system. The focal barrier does not reduce nectar-robber use because robbers can access the corolla without traversing the proposed defended structure. The antagonist contrast is null-compatible.

This is consistent with Prediction 3: a trait can be structurally conspicuous yet functionally irrelevant to the focal antagonist if effective exposure is near zero.

### 4.4 Selectivity changes state within systems

Eight independent defence-side clusters preserve the earlier BITA conditionality result (Fig. 3).

Realised defence state changes with:

1. dose or trait expression;
2. cumulative exposure or reward context;
3. consumer identity;
4. response stage;
5. temporal expression.

Four systems provide particularly clear ordered exposure patterns. In *Polemonium*, moderate 2-phenylethanol expression has no detected pollination cost, whereas high expression interferes with bumblebee visitation and pollination (Galen et al. 2011). In *Asclepias*, short exposure can be tolerated while extended exposure produces deterrence (Jones & Agrawal 2016), and strongly elevated nectar cardenolides can produce negative consumption responses beyond the natural-range pattern (Villalona et al. 2020). In *Aconitum*, robber deterrence occurs at substantially lower exposure than pronounced pollinator interference (Barlow et al. 2017). *Nicotiana* shows response-stage dependence in which arrival, handling, and consumption need not respond in the same direction (Kessler & Baldwin 2007).

These systems are consistent with the threshold sequence

\[
x<x_H^*
\rightarrow
x_H^*<x<x_P^*
\rightarrow
x>x_P^*,
\]

that is, ineffective → selective → interfering.

No common numerical threshold ratio is inferred because doses, traits, consumers, and outcome constructs differ among studies.

### 4.5 Floral geometry predicts cheating route at community scale

The Sakhalkar et al. (2023) dataset contained 183 visited plant species after source-defined filtering; 182 had matched trait data (Fig. 4). Robbing occurred in 26 plant species and thieving in 39.

Fifty-seven plant species had tube-length information and non-zero robbing or thieving frequency. Tube length was positively associated with robbing-versus-thieving balance:

\[
\rho=0.346786,
\qquad
p_{\mathrm{perm}}=0.0086.
\]

Thus, as tube length increased, cheating shifted toward nectar robbing relative to nectar thieving.

The same pattern appeared in a simple descriptive contrast. Median tube length was 2.0893 in robber-only species and 0.6766 in thief-only species, approximately a threefold difference on the deposited trait scale.

This supports Prediction 5 at the level of a cross-species association. A source-defined multitrait sensitivity using tube length, tube width, and a 12-level shape factor did not isolate tube length as a unique partial predictor (full-model permutation p=0.202; tube-length block p=0.211), and the deposited workbook lacked usable brightness values needed for the source-defined thief model. We therefore interpret the result as evidence that access geometry is associated with cheating route, not that tube length alone uniquely causes the switch.

### 4.6 Post-rule evidence is directionally consistent but does not close confirmation

The effective-domain interpretation was originally developed using the historical evidence set. We therefore evaluated subsequent evidence separately.

*Caryopteris divaricata*, recovered by systematic expansion, provides a separated geometric system in which shorter-tubed flowers experience less robbing and higher legitimate visitation under natural robbing pressure; trait-associated differences are not retained when robbers are excluded (Tie et al. 2023).

*Phlox paniculata*, also recovered after rule formulation, provides an experimental chemical system in which intact floral terpenes repel ants while flying flower visitors show no detected treatment difference (Junker et al. 2011). This is compatible with selectivity but remains null-compatible.

The registered 2026 *Erica* hold-out was coded as geometrically separated before promoting the focal outcome direction (Coetzee et al. 2026). Longer corollas predict reduced bee robbing and a positive pollination-rate direction, but the latter remains boundary evidence and is coded DIRECTION_ONLY / UNRESOLVED.

These post-rule systems do not justify a success percentage. They differ in design and claim strength. Together with the independent Sakhalkar network, they are directionally consistent with the effective-domain framework while leaving formal confirmatory validation open.

### 4.7 Legacy BITA systems explain why selectivity is a context property

Kessler et al. (2015) remains a particularly informative bridge. When nectar absence is treated only as a broad antagonist-reducing access restriction, its pollination cost changes with consumer identity: *Manduca sexta* pollination declines strongly without nectar, whereas *Hyles lineata* retains pollination service when scent remains available. The same crossed scent × nectar architecture also produces different source-mean interaction signs across pollinator contexts.

This linked result is not added as a new matched-D replication because nectar is a reward axis and the strict defence interpretation is contested. It nevertheless demonstrates the central biological point: the cost of a floral access state depends on which consumer encounters it and how that consumer uses the flower.

## 5. Discussion

### 5.1 Floral defence selectivity is an ecological state, not a defence-class property

Across the four evidence layers, the recurring pattern is conditional rather than categorical. The broader state-recovery analysis strengthens that point: the fixed effective-domain mapping recovered all 11 scorable historical + expansion systems, whereas a coarse modality-only classifier missed several systems. A floral defence is not inherently safe or costly to pollination. Its outcome depends on who experiences it, through what route, at what intensity, and at what stage.

The broader route-level corpus shows that D implementations span chemical, physical, and reward/access mechanisms while pollinator consequences vary among context-dependent, null-compatible, improved, interference, and unresolved states. The stricter matched-D evidence is smaller but aligned with the predicted state structure. Within-system data show that the same nominal defence can move between states as exposure changes. The community network provides a quantitatively independent consequence: access geometry predicts whether exploiters use the normal floral opening or switch to robbery.

This combination matters because each layer addresses a different weakness in the others. Case-level systems give close biological interpretation but limited generality. Within-system transitions establish that states are not fixed properties of trait categories. The network analysis provides breadth across many plant species but is observational. Their convergence is stronger than treating any one layer as definitive.

### 5.2 Separation can arise through several biological coordinates

The effective-exposure coefficients \(q_H\) and \(q_P\) are not intended as universal measurable constants. They summarize distinct mechanisms that determine how much of a focal trait reaches each consumer.

In physical systems, separation can arise from body size, attack geometry, developmental stage, or functional mode. In chemical systems, it can arise from tolerance, dose, or cumulative exposure. Temporal expression can separate a florivore-active window from a pollinator-active window. Response-stage separation can allow visitors to arrive but shorten residence or consumption.

This common formal structure explains why “chemical versus physical” is an incomplete biological classification even though the current strict data cannot statistically compare the two explanations. Both broad classes contain multiple effective-domain states.

### 5.3 Barriers reroute exploitation rather than simply eliminating it

The Sakhalkar reanalysis (Fig. 4) adds a result that the case synthesis alone could not provide. Longer floral tubes are associated with a shift from thieving to robbing across plant species. A source-defined multitrait sensitivity does not identify tube length as a unique partial driver after accounting for correlated morphology, so the broader interpretation is that floral access geometry is associated with the behavioral route of cheating.

This suggests that floral defence should often be analysed as a routing problem. Blocking the legitimate path can reduce one exploitative mode while increasing the relative value of bypass. That perspective links physical barriers, nectar robbing, visitor handling, and trait matching within one ecological framework.

Independent experiments support the same routing interpretation outside the strict matched-D corpus. Leonard et al. (2013) manipulated nectar-guide patterns on artificial flowers used by bumblebees that could either visit legitimately or rob; nectar guides increased the relative frequency and efficiency of legitimate visits. At a broader geographic scale, Adler et al. (2016) found that *Gelsemium sempervirens* genotypes from a high-robbing region were roughly half as likely to be robbed but also received roughly half as many pollinator visits in common gardens. Neither study enters the matched-D N: the first manipulates a routing signal rather than a validated defence axis, and the second does not isolate one causal floral D. Together they broaden the access-routing pattern beyond the primary evidence design.

It also changes how “successful defence” should be evaluated. A reduction in entry through one route is not sufficient if antagonists compensate through another route.

### 5.4 The selective window is dynamic

The defence-side conditionality systems (Fig. 3) show why static comparisons can be misleading. If antagonist and pollinator thresholds differ, a system can appear selective at one dose but costly at another. A pollinator can also cross a threshold only after repeated exposure or only at a later behavioral stage.

This predicts that ecological variation in trait intensity, visitor assemblage, and phenology can shift the same plant population among defence states without requiring evolutionary change in the underlying trait class.

The immediate empirical implication is to measure exposure and response stage rather than treating a compound or structure as a single binary category.

### 5.5 What the previous identification framework still contributes

The earlier BITA result—trait interaction is not ecological mechanism—remains important, but its role changes.

The effective-exposure model generates biological predictions. The identification framework limits how strongly those predictions are interpreted from heterogeneous evidence. A positive matched pattern does not by itself identify a unique pathway allocation, null-compatible pollinator responses are not proof of no cost, and linked multi-paper evidence is not silently promoted to same-study replication.

The previous decomposition

\[
\Delta_{AD}W=\rho_\Delta-\iota_\Delta-\kappa_\Delta
\]

and the associated identified-set logic therefore remain valuable for experiments that aim to partition antagonist relief, pollinator interference, and remaining channels. They are not the headline result of the present macro paper.

### 5.6 Relation to previous floral macro-syntheses

Previous synthesis has shown that floral scent can differentially attract obligate visitors and repel facultative visitors (Junker & Blüthgen 2010), that herbivory can alter floral traits and pollination (Haas-Desmarais et al. 2026), that floral larceny has measurable reproductive and reward consequences (Leal et al. 2025), and that multiple ecological agents impose selection on floral phenotypes (Caruso et al. 2019). The present analysis does not claim novelty for those broad facts.

The narrower contribution is to organize same-defence evidence around effective exposure and to connect it to within-system threshold switching and independent community-scale route switching.

The strongest unresolved comparison is whether effective-domain structure explains strict pollinator outcomes better than defence modality, taxonomy, or other coarse predictors. The current strict subset is too small and confounded to answer that question.

## 6. Claim ceiling and next tests

Current evidence supports:

1. recurrent antagonist-reducing floral traits across chemical, physical, and access implementations;
2. qualitative pollinator-state recovery in 9/9 scorable historical systems and 2/2 systematic-expansion systems under the fixed domain-state mapping, with null-compatible outcomes kept distinct from preservation;
3. a narrower direction-supported Stage-2 pattern in three systems, retained as a high-specificity subset rather than the main sample size;
4. repeated within-system state switching with dose, exposure, consumer identity, response stage, and time;
5. a quantitative community-scale association between tube length and cheating route;
6. post-rule systems that are directionally compatible with the framework without completing confirmatory validation.

Current evidence does **not** establish:

1. a universal causal coefficient for effective-domain separation;
2. that domain relation statistically outperforms chemical-versus-physical class in the strict subset;
3. prevalence of selective floral defence in nature;
4. one pooled effect size across the heterogeneous biological outcomes;
5. a unique \(\rho_\Delta,\iota_\Delta,\kappa_\Delta\) allocation for any current macro-synthesis result.

The highest-value literature additions are therefore specific missing cells rather than more supportive examples:

~~~text
SEPARATED + chemical + direction-supported pollinator state
OVERLAPPED + physical + direction-supported pollinator state
~~~

A bounded targeted search recovered strong linked programmes but no new study satisfying the frozen same-study same-D gate. Future empirical work can fill the same cells directly by crossing defence intensity or access architecture with both antagonist and pollinator outcomes in the same system.

## 7. Conclusion

Floral defence is not simply a property of a compound or structure. It is a relational state produced by trait intensity, consumer susceptibility, access route, timing, and response threshold.

A simple effective-exposure model predicts when a selective window can exist, when overlap should impose mutualist costs, when bypass should defeat the focal defence, and when stronger expression should close the selective window. The qualitative state mapping recovers all 11 currently scorable historical + systematic-expansion systems, while the narrower strict subset remains too small for a conventional moderator meta-regression. An independent community reanalysis shows the same access logic at larger scale: longer flowers shift cheating toward robbery rather than eliminating exploitation.

The resulting ecological picture is therefore not “defence versus pollination” as a fixed trade-off. It is **interaction routing through unequal access and exposure domains**.

The previous BITA identification work remains as the inferential boundary around this result. The next advance is not to label every aligned pattern as mechanism, but to test the same effective-domain predictions in additional prospectively coded systems and experiments that close the currently sparse Stage-2 cells.

## Open Research statement

All evidence registries, source-adjudication notes, architecture and outcome codes, exact Stage-2 model gate, public-data reanalysis scripts, frozen aggregate results, and legacy BITA provenance are maintained in the project repository. The final submitted version should archive a permanent release of the analysis branch and all reproducible public-data outputs.

## Author contributions, funding, acknowledgments and competing interests

[Author-controlled; complete before submission.]

## References

The candidate manuscript uses the focused working bibliography in `manuscript/FLORAL_DEFENCE_SELECTIVITY_REFERENCES_V0.md`. Final reference style and the remaining bibliography normalization are deferred until target-journal selection.
