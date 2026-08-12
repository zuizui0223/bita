# Manuscript audit v4 — Mechanism → Pattern pre-submission check

## Verdict

**YES: the canonical manuscript is now structurally and inferentially a two-part paper: mathematical Mechanism first, meta-analytic Pattern second.**

It is no longer organized as theory Methods followed by a mixed bag of literature evidence. The current canonical order is:

```text
1 Introduction
2 Part I — Mechanistic theory: mechanism and principle
3 Part I results — mechanistic sign regimes
4 Part II — Meta-analysis and cross-study pattern synthesis
5 Part II results — meta-analytic patterns across systems
6 Integration — from mechanism to pattern
7 Conclusions
```

This audit checks that the labels correspond to actual scientific content rather than cosmetic section renaming.

## Part I — Mechanism: PASS

Part I contains the fixed mathematical theory and no empirical synthesis.

### Mechanistic objects retained unchanged

```text
W_AD = M_AD - G_AD - C_AD
orientation gate:
M_AD <= 0, G_AD <= 0, C_AD >= 0
W_AD = rho - iota - kappa
W_AD > 0 iff rho > iota + kappa
```

Also retained:

- focal `A`, `D`, and outcome-scale declarations;
- Proposition 1: total `W` does not identify component channel curvatures;
- unrestricted environmental derivatives for antagonist pressure `H` and pollinator service `P`;
- explicit break-even inequalities;
- endpoint-normalized finite sensitivity analysis;
- canonical 2,592 evaluations with all numerical results unchanged.

### Mechanism conclusion

Part I answers **why and under what conditions the sign changes**. It does not claim a universal direction of attraction–defence interaction.

Figures 1–2 and Tables 1–2 are correctly assigned to this half.

## Part II — Pattern: PASS

Part II asks **which mechanism-derived patterns recur across systems and where context changes the realized balance**.

Crucially, it contains real quantitative cross-study synthesis rather than only a literature map.

### Meta-analysis 1 — Leal et al. 2025: PASS

This is a random-effects meta-analysis on compatible oriented log-response-ratio scales, aggregated by independent study cluster within outcome stratum.

Canonical cross-study patterns:

```text
female reproductive success  LRR -0.210  48 independent clusters
nectar standing crop          LRR -0.483  28
legitimate visitation         LRR -0.291  22
```

Direction survives the declared correlation, quarantine, and leave-one-cluster-out sensitivities. Very high heterogeneity remains visible and is part of the Pattern result rather than hidden.

### Meta-analytic synthesis 2 — Sasidharan et al. 2023: PASS with explicit design boundary

This is a quantitative cross-study synthesis using a conservative 32-study-component topology.

Canonical pattern:

```text
florivore physiological detection  84/103
pollinator physiological detection 151/220
assembled risk difference           +0.129
LOCO direction positive             32/32
```

The manuscript correctly retains the key limitation: only three study components contain both roles and all three paired differences are zero. Behavioral disagreements remain evidence of context dependence. The synthesis is therefore not mislabeled as a causal within-study role effect.

### Theory-to-pattern scaffold: PASS, not misrepresented as a grand meta-analysis

The 38-record / 14-independent-cluster route architecture maps cross-study recurrence onto the Part I mechanism classes:

```text
A -> pollination   4 clusters
A -> antagonism    5
D -> antagonism   10
D -> pollination   7
same-system       10
context switches  11
direct A x D       1 strict cluster, sign unresolved
direct joint cost  0 strict estimates
```

This scaffold is deliberately **not** pooled into one grand effect because the outcome constructs are not commensurable. That choice strengthens the meta-analytic design rather than weakening it.

### Pattern conclusion

The supported cross-system conclusion is:

> **recurrent constituent mechanisms + context-dependent balance**

not:

> a universal positive or negative `W_AD`.

This is exactly the kind of Pattern expected from the Part I mechanism: changing relative strength of antagonist relief, pollinator interference, and joint cost changes the sign/state.

Figure 3 and Tables 3–4 are correctly assigned to Part II. Quantitative robustness panels remain Supplementary Figure S4.

## Mechanism → Pattern linkage: PASS

The manuscript now makes the bridge explicit at four levels:

1. **Abstract:** asks a mechanism question and a cross-system pattern question separately.
2. **Section architecture:** Part I and Part II are physically separated.
3. **Figures/Tables:** Figures/Tables 1–2 = Mechanism; Figure 3/Tables 3–4 = Pattern.
4. **Integration:** Section 6 interprets the meta-analytic pattern through the mechanism without calling the pattern an estimate of the mixed partial.

The paper therefore reads as:

```text
derive mechanism
→ derive conditional predictions
→ quantify recurrent cross-study patterns
→ retain heterogeneity/conditionality
→ identify where direct interaction data are still missing
```

## Inference-boundary audit: PASS

The following distinctions remain explicit:

```text
marginal route evidence != W_AD
same-system evidence != direct A x D
route counts != prevalence
finite-grid occupancy != prevalence
Leal pooled effects != rho/iota/kappa
Sasidharan assembled contrast != causal paired role effect
zero joint-cost studies != kappa = 0
```

No additional theory, parameter, or biological mechanism was introduced during restructuring.

## Reviewer-facing assessment

The strongest current novelty claim is not “we invented a new mixed partial” and not “the meta-analysis proves the model.” It is the **Mechanism → Pattern connection**:

- a local mathematical mechanism gives a conditional sign principle;
- quantitative cross-study synthesis shows recurrent constituent effects but large heterogeneity;
- the pattern scaffold shows repeated context/state switching;
- direct interaction and joint-cost evidence are sparse exactly where the mathematical decomposition says identification requires them.

That is coherent with a theoretical-ecology contribution and avoids overclaiming the empirical layer.

## Remaining non-scientific submission blockers

The scientific architecture is no longer a blocker. Remaining items are external/author-controlled:

- final author order/publication names and affiliations;
- corresponding author/email and ORCIDs;
- CRediT, funding, acknowledgements, competing-interest confirmation;
- repository licence choice;
- final house-style references;
- exact release/tag and archival DOI;
- final EPS export and full CI from that exact submission commit;
- authenticated entry into the journal submission portal.

## Decision

```text
Mechanism half:            PASS
Meta-analytic Pattern half: PASS
Mechanism -> Pattern link:  PASS
scientific submission gate: GO
portal submission:          requires author metadata + authenticated external portal
```
