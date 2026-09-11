# Trait interaction is not ecological mechanism: an identification framework for multifunctional traits

**Canonical BITA full-paper science source**

**Target class:** Ecology Concepts & Synthesis / conceptual-methodological ecology

**Authors and affiliations:** [Author-controlled]

## Abstract

Ecologists frequently infer mechanism from statistical interaction. Yet when two traits jointly affect fitness through several ecological channels, the same total interaction can be produced by many different pathway allocations. Floral attraction and defence make this problem explicit: attraction can increase pollination and antagonist exposure, whereas defence can reduce antagonist damage while interfering with pollination or imposing a direct joint cost. We separate the measurable trait interaction from the mechanisms compatible with it. For a two-level attraction-by-defence factorial, the directly estimable interaction is \(\Delta_{AD}W=W_{11}-W_{10}-W_{01}+W_{00}\). A positive value shows that defence makes the attraction effect more positive, but it does not by itself establish functional release and it does not identify whether the gain arose through antagonist relief, pollinator interference, or a remaining joint channel. Writing \(\Delta_{AD}W=\rho_\Delta-\iota_\Delta-\kappa_\Delta\) defines an identified set of compatible mechanisms rather than a point allocation. Explicit biological restrictions and partial channel measurements shrink this set. A crossed \(A\times D\times\) antagonist \(\times\) pollinator experiment can identify the two consumer-mediated channels when interventions are selective, the trait contrasts remain invariant, pollinator-independent reproduction is characterized, and the four-way interaction supports channel separability; the remaining joint channel requires an independent assay rather than residual labelling. A source-adjudicated synthesis contains 56 directional route records from 25 independent biological clusters and shows recurrence of all four constituent marginal pathways, while a stricter audit of 17 high-information systems finds complementary experimental faces but no system that closes the full allocation design plus independent joint-cost assay. Existing biology is therefore recurrent but identification is fragmented. BITA's contribution is a promotion ladder from interaction detection to partial identification and mechanism allocation, not a claim that interaction itself reveals mechanism.

**Keywords:** causal identification; ecological mechanism; factorial experiment; partial identification; trait interaction; pollination; antagonism; floral defence

## 1. Introduction

A trait interaction is easy to estimate and easy to over-interpret. When two phenotypic coordinates jointly affect reproduction, a non-zero interaction shows nonadditivity on the declared outcome scale. It does not reveal which biological route generated that nonadditivity. This distinction becomes important whenever the same traits act through several ecological partners or physiological channels.

Flowers provide a useful worked system. Floral colour, scent, display and reward can increase pollinator attraction while also changing exposure to florivores, nectar robbers, seed predators, or ovipositing herbivores. Chemical and physical floral defences can reduce antagonist use, but they may also alter pollinator behaviour or carry direct allocation and construction costs. A positive attraction-by-defence interaction can therefore arise from several causal allocations.

The inferential problem is structural rather than merely statistical. More precise estimation of the same four-cell attraction-by-defence surface does not reveal a unique channel allocation if several decompositions remain compatible with that surface. The correct target is therefore an identification ladder: what is identified by the observed interaction, what stronger outcome claims require additional contrasts, which mechanisms remain in an identified set, which restrictions shrink that set, and which selective interventions are required for point identification?

The broader architecture-value question—how a measured one-axis conflict becomes recoverable benefit, architecture margin, accessibility, invasion, fixation, and occupancy—is owned by the companion SLK framework. BITA begins later and asks a different question: **once multiple trait axes exist and interact on fitness, what ecological mechanism generated their joint effect?** The separation is deliberate. A favorable architecture and an identified mechanism are different estimands.

We make four contributions. First, we distinguish three nested outcome claims from the mechanism question: positive interaction relief, functional constraint release, and strict reversal. Second, we show that a total trait interaction defines an identified set of compatible channel allocations rather than a unique mechanism. Third, we give a crossed intervention design that can allocate antagonist and pollinator channels while testing its own separability assumption. Fourth, we place published systems on this identification ladder using a source-adjudicated route synthesis and a high-information design audit.

## 2. What a trait interaction actually identifies

Let \(A\in\{0,1\}\) be a focal attraction contrast and \(D\in\{0,1\}\) a focal defence contrast. On a predeclared reproductive outcome \(W\), define

\[
\Delta_{AD}W=W_{11}-W_{10}-W_{01}+W_{00}.
\]

Also define the attraction effect under low and high defence,

\[
A_0=W_{10}-W_{00},\qquad A_1=W_{11}-W_{01},
\]

so that

\[
\Delta_{AD}W=A_1-A_0.
\]

This separates three biologically different claims.

**Level 1 — positive interaction relief:** \(\Delta_{AD}W>0\). Defence makes the attraction effect more positive.

**Level 2 — functional constraint release:** \(A_0\le0<A_1\). Attraction is non-beneficial without defence but beneficial with defence.

**Level 3 — strict reversal:** \(A_0<0<A_1\). Attraction changes from detrimental to beneficial.

Level 3 implies Level 2, and Level 2 implies Level 1, but not conversely. A strongly positive interaction can occur while attraction remains negative in both defence states. Therefore a positive interaction is not synonymous with release.

These outcome claims are still not mechanism claims. Write reproductive outcome as

\[
W=M-G-C,
\]

where \(M\) is a mutualist-mediated contribution, \(G\) is antagonist-mediated loss, and \(C\) is a remaining direct or allocation channel. Orient the attraction-by-defence interactions as

\[
\rho_\Delta=-\Delta_{AD}G,\qquad
\iota_\Delta=-\Delta_{AD}M,\qquad
\kappa_\Delta=\Delta_{AD}C.
\]

Then

\[
\boxed{\Delta_{AD}W=\rho_\Delta-\iota_\Delta-\kappa_\Delta.}
\]

If the measured total interaction is \(\delta\), the compatible mechanisms form

\[
\mathcal I(\delta)=\{(\rho,\iota,\kappa):\rho-\iota-\kappa=\delta\}.
\]

Without additional information, this is an identified set rather than a point. Increasing sample size around \(\delta\) narrows uncertainty in the total interaction but does not collapse the mechanism set.

A positive \(\rho_\Delta\) means that defence reduces antagonist loss more strongly when attraction is high. A positive \(\iota_\Delta\) means that defence erodes the mutualist return to attraction. The remaining \(\kappa_\Delta\) should not be called construction cost merely because it closes an accounting identity; that biological label requires an independent assay.

## 3. Partial identification before full mechanism allocation

Mechanism inference need not jump directly from a four-cell trait factorial to a large fully crossed experiment. Explicit restrictions can shrink the identified set.

For example, if an independent biological argument supports

\[
\kappa_\Delta\ge0,
\]

then

\[
\rho_\Delta-\iota_\Delta
=\Delta_{AD}W+\kappa_\Delta
\ge\Delta_{AD}W.
\]

Thus a positive total interaction implies that antagonist relief exceeds pollinator interference by at least the observed interaction on the declared scale, conditional on the non-negative joint-cost restriction. This is a partial-identification result, not a universal theorem.

Likewise, an independent bounded assay for \(\kappa_\Delta\) narrows the possible biotic balance. A selective estimate of either antagonist relief or pollinator interference shrinks the remaining coordinates further. BITA therefore treats identification as graded:

```text
interaction detection
        ↓
identified set
        ↓
biological restrictions / partial channel measurement
        ↓
partial identification
        ↓
selective crossed intervention
        ↓
consumer-channel allocation
        ↓
independent remaining-channel assay
        ↓
mechanism-resolved interpretation
```

This ladder is the core methodological object of the paper.

## 4. A crossed intervention design for channel identification

The minimum general design crosses four binary factors,

\[
A\times D\times E_G\times E_P,
\]

where \(E_G\) indexes antagonist access and \(E_P\) indexes pollinator access. The 16 cells are necessary but not sufficient. The causal interpretation requires selective consumer interventions and invariant attraction and defence contrasts across consumer states.

### 4.1 Antagonist relief

At fixed pollinator state \(p\), define fitness recovered by antagonist exclusion as

\[
R_G(A,D;p)=W(A,D,E_G=0,E_P=p)-W(A,D,E_G=1,E_P=p).
\]

The attraction-by-defence interaction in this exclusion contrast identifies the corresponding antagonist-relief component when the intervention is selective. A main effect of defence on damage is not enough; the target asks whether defence changes the antagonist cost of attraction.

### 4.2 Pollinator interference and the zero-baseline trap

At fixed antagonist state \(g\), define the pollinator-dependent increment

\[
J_P(A,D;g)=W(A,D,E_G=g,E_P=1)-W(A,D,E_G=g,E_P=0).
\]

Its attraction-by-defence interaction identifies the pollinator-dependent part of \(\iota_\Delta\), but not necessarily the whole channel. Reproduction can continue under pollinator exclusion through autonomous selfing, apomixis, resource reallocation, or treatment effects. The pollinator-absent baseline interaction must therefore be estimated or independently justified as negligible.

### 4.3 The four-way interaction is a separability diagnostic

If antagonist and pollinator channels are separable on the proposed additive representation, the antagonist-relief interaction should not depend on pollinator state, and the pollinator-increment interaction should not depend on antagonist state. Algebraically these are the same \(A\times D\times E_G\times E_P\) four-way interaction up to sign.

A non-zero four-way term is therefore evidence that the proposed two-channel decomposition fails: consumer pathways interact on the trait interaction itself. This is a biological result, not a nuisance term to absorb. Empirical equivalence should be assessed with uncertainty-aware criteria rather than by interpreting failure to reject a null as proof of separability.

### 4.4 The remaining joint channel requires an independent assay

After estimating the total interaction and consumer-mediated channels, define the unallocated remainder

\[
U_\Delta=\rho_\Delta-\iota_\Delta-\Delta_{AD}W.
\]

BITA deliberately calls this \(U_\Delta\), not cost. Intervention leakage, omitted channels, baseline misspecification, scale mismatch, and nonadditivity can all enter the remainder. Only an independent \(A\times D\) assay conducted under conditions that standardize or suppress the focal consumer pathways can support a biological cost interpretation.

## 5. The empirical pattern: recurrent pathways, fragmented identification

A source-adjudicated synthesis contains **56 directional route records from 25 independent biological clusters**. All four constituent marginal pathways recur: attraction affects pollination, attraction affects antagonists, defence affects antagonists, and defence can affect pollination. Fourteen clusters contain more than one route in the same biological system, and 17 show context- or state-dependent switching. These overlapping counts establish recurrence, not natural prevalence.

A stricter audit retained **17 high-information systems** because they approach the identification target or expose informative failure modes. None closes the entire sequence from trait interaction through selective consumer allocation to an independent joint-channel assay. The resulting pattern is a **fragmented identification frontier**.

*Kessler et al. (2008)* provides the strongest direct attraction-by-defence-like trait factorial in *Nicotiana attenuata*. Under registered aggregate constraints, the defended attraction effect \(A_1\) remains positive, approximately +0.200 to +0.240, while the undefended attraction effect \(A_0\) remains confined to an interval spanning zero, approximately -0.030 to +0.030. The total interaction remains positive under those aggregate constraints. This is strong Level-1 evidence and asymmetric partial identification of the stronger release claim, but exact source/design-based uncertainty is unresolved, and systemic nicotine manipulation leaves the flower-restricted defence scope imperfectly isolated. It does not allocate the mechanism.

*Egan et al. (2021)* provides a complementary consumer-factorial face: herbivory and pollination environments are crossed, but the focal attraction and defence traits are measured rather than independently manipulated as an \(A\times D\) factorial. It identifies context-dependent selection, not channel allocation for a manipulated trait interaction.

The public *Impatiens capensis* system of Soper Gorden and Adler (2018) reaches another face: observational attraction and defence coordinates are measured under randomized interaction treatments. Reanalysis can ask whether the observational \(A\times D\) association changes under robbing, florivory, or pollination treatments, but causal trait-channel identification remains unavailable because the traits themselves were not randomized.

Other systems add further pieces: attraction crossed with antagonist removal and pollination supplementation, selective flower-associated defence manipulations, or defence-by-herbivore-suppression-by-hand-pollination designs. Their failure modes differ, but none supplies the full allocation sequence plus an independent joint-cost assay.

The important conclusion is therefore not “no one has studied these mechanisms.” The mechanisms are biologically recurrent and experimentally tractable. What is missing is their intersection on the same trait coordinates and outcome scale.

## 6. Designing the next identifiable experiment

BITA implies a staged design.

**Stage 1: outcome surface.** Run the four-cell \(A\times D\) factorial and estimate \(A_0\), \(A_1\), and \(\Delta_{AD}W\) with compatible design-based uncertainty. This separates interaction relief from Level-2 release and Level-3 reversal.

**Stage 2: channel pilots.** On the same trait coordinates, estimate plausible antagonist-relief, pollinator-interference, pollinator-independent baseline, and cross-consumer coupling effects.

**Stage 3: crossed consumer intervention.** Run the selective \(A\times D\times E_G\times E_P\) design. Estimate consumer-channel contrasts and the four-way separability diagnostic.

**Stage 4: independent remaining-channel assay.** Only after consumer-channel identification should the unallocated remainder be compared with an independent cost or allocation assay.

This ordering prevents two common errors. A design powered to detect \(\Delta_{AD}>0\) is not necessarily powered to decide whether \(A_0\le0<A_1\), especially when \(A_0\) lies close to zero. And a residual from the reproductive model is not granted a mechanistic name before an independent assay exists.

## 7. Relation to SCH and SLK

BITA is not the paper that establishes the upstream conflict budget or the architecture-value threshold.

**SCH** asks whether multifunctionality has actually been promoted to identified functional conflict on one shared coordinate. Its central warning is `multifunctionality != conflict`.

**SLK** transports an identified conflict budget through recoverable benefit and architecture value into accessibility, invasion, fixation, and occupancy. Its central sequence is `L -> R -> Phi -> accessibility -> invasion -> fixation -> occupancy`.

**BITA** begins after multiple trait axes are empirically relevant and asks whether their observed interaction has actually been promoted to mechanism. Its central warning is `trait interaction != mechanism`.

```text
SCH:    have opposing functional demands been identified?
SLK:    when can that conflict become favored and realized architecture?
BITA:   once traits interact, which ecological route generated the gain?
```

The architecture quantities \(R\), \(s\), \(K\), and \(\Phi\) may appear in BITA only as upstream context or externally supplied bridge variables. They are not the novelty center of this paper.

## 8. Discussion

The main result is a change in what counts as evidence. A trait interaction is an estimand, not a mechanism label. A positive interaction can justify a directional statement about how one trait modifies the effect of another. Stronger functional-release claims require additional outcome contrasts. Mechanism allocation requires still more information: selective interventions, baseline characterization, a separability gate, and an independent assay for any remaining channel.

This principle extends beyond flowers. The same identification problem appears whenever two traits affect several opposing ecological pathways: dispersal versus retention, defence versus competitive performance, habitat structure that facilitates one interaction while obstructing another, or behavioural syndromes that alter both resource gain and risk.

The empirical synthesis also changes the interpretation of missing evidence. Across the current 56-route / 25-cluster synthesis, the constituent biology recurs. Across the 17-system high-information frontier, sophisticated pieces of the necessary design already exist. The gap is not lack of plausible mechanisms; it is that the pieces usually occur in different experiments. That diagnosis points directly to the next experiment.

## 9. Claim ceiling

Current evidence supports:

1. recurrence of all four constituent marginal pathway families across independent biological systems;
2. existence of both direct attraction-by-defence-like trait factorials and consumer factorials;
3. a strong aggregate positive-interaction anchor in Kessler et al. (2008), with positive defended attraction effect under registered constraints;
4. zero-compatible undefended attraction effect in that aggregate reconstruction, so strict Level-2/3 release remains unidentified;
5. no screened high-information system closing the full channel-allocation design plus independent remaining-channel assay.

Current evidence does **not** establish prevalence of trait differentiation, a universal mechanism, historical trait splitting, cue privatization, or a completed point allocation of \(\rho_\Delta\), \(\iota_\Delta\), and \(\kappa_\Delta\) in any screened biological system.

## 10. Conclusion

Trait interaction and ecological mechanism are different inferential objects. A four-cell factorial can establish nonadditivity and, with the right outcome contrasts, distinguish interaction relief from stronger functional release. But the same total interaction remains compatible with many antagonist-relief, pollinator-interference, and joint-channel allocations. BITA turns that ambiguity into an explicit programme:

```text
total interaction
→ identified set
→ partial identification
→ selective crossed intervention
→ separability test
→ independent remaining-channel assay.
```

Published floral systems already contain the biological pathways and many required experimental components. What they lack is the full intersection of those components on the same trait coordinates and reproductive scale. The next advance is therefore not another claim that two traits interact, but an experiment designed to show why.

## Open Research statement

Analysis code, source-audit products, route-synthesis tables, identification estimands, public-data reanalyses, and design-coverage products are maintained in the project repository. A permanent archive of the accepted code and data-derived outputs should accompany publication.

## Author contributions, funding, acknowledgments and competing interests

[Author-controlled; complete before submission.]

## References

Use `manuscript/TRAIT_DIFFERENTIATION_REFERENCES_V1.md` as the canonical focused reference pool. The longer mechanism-identification provenance text remains preserved in `manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md`.