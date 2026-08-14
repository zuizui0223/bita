# Competing-hypothesis falsification matrix v1

## Purpose

The current mechanism-first program has converged on an **effective-domain separation** rule. This audit asks whether that rule is actually needed, or whether simpler explanations can account for the observed state changes.

The comparison is qualitative and source-adjudicated. It is not a prevalence analysis and it does not treat the screened systems as a random sample of nature.

## Candidate explanations

### H0a — defence-strength-only

A stronger floral defence should move systems monotonically toward stronger antagonist reduction and stronger pollinator interference. Geometry, consumer route, and response stage are secondary details.

### H0b — modality-only

Chemical and physical defences should form qualitatively distinct classes; apparent switching can be explained mainly by the material implementation of D.

### H0c — consumer-identity-only

The sign/state is determined mainly by which taxon visits the flower. Once visitor identity is fixed, the ecological role/effect should be comparatively stable.

### H1 — effective-domain separation

The focal state is determined by whether antagonists and legitimate pollinators experience overlapping or separable effective D domains. The separating coordinate can be dose, cumulative exposure, susceptibility, attack route, body-size/access geometry, space, time/development, functional behaviour, or response stage.

H1 predicts three recurring states:

```text
separated domains -> antagonist relief with limited pollinator interference
shared/overlapping domains -> antagonist relief plus pollinator interference
antagonist bypass / non-susceptibility -> focal D channel fails
```

## Discriminating systems

| System | Source-adjudicated transition | H0a strength-only | H0b modality-only | H0c identity-only | H1 domain separation |
|---|---|---|---|---|---|
| Polemonium 2PE | moderate expression is guarded-compatible; high expression deters pollinators | fails: same D changes state with dose | fails: both states are chemical | not sufficient | predicted by threshold overlap |
| Asclepias cardenolides | single-bout Bombus null; multi-day colony deterrence; monarch oviposition reduced while adult flower foraging is not | fails: same concentration can change with cumulative exposure | fails: same chemical | fails: same consumer can change response with exposure/stage | predicted by exposure/response domains |
| Nicotiana nectar repellents | pollinator arrival can increase while handling/nectar removal falls; ants decline | scalar-strength model cannot assign one pollinator sign | same chemical yields mixed response stages | same pollinator identity has stage-dependent effects | predicted by response-stage separation |
| Pedicularis rex | water barrier suppresses seed predation while nectar robbers bypass and pollinator visits remain null-compatible | fails: stronger/broad barrier is not the explanation | physical alone does not predict robber bypass | taxon identity alone does not encode attack route | predicted by attack-route separation/bypass |
| Thunia alba | same Bombus arrival rate roughly unchanged while bract architecture routes behaviour between legitimate pollination and robbery | fails: state changes without a visitor-abundance gradient | physical category does not predict functional routing | directly fails: same Bombus changes ecological role | predicted by functional-mode/access separation |
| Codonopsis lanceolata | ant approach surfaces are slippery but legitimate hornet foothold remains mechanically usable | strength alone misses spatial localization | physical category alone does not specify selective geometry | identity alone misses spatial access | predicted by spatial/access-domain separation |
| Chrysothemis friedrichsthaliana | pre-anthesis water calyx blocks oviposition; pollination occurs after anthesis; other antagonists can bypass | strength alone misses developmental timing | physical category alone does not predict stage specificity | identity alone misses life-stage access | predicted by temporal/developmental separation |
| Bejaria resinosa | sticky floral surface suppresses florivory but can exclude mutualistic insects too | compatible only as broad high-cost D, but gives no reason selectivity fails here | directly falsifies 'physical is pollinator-safe' | not sufficient | predicted as overlapping-domain boundary |
| Salvia miltiorrhiza | calyx manipulation changes other functions but robber and pollinator visitation are unaffected because robbers bypass | strength-only would misclassify a conspicuous barrier as effective D | physical category does not guarantee D efficacy | not sufficient | predicted as antagonist-bypass / D-failure state |
| Kessler 2015 Nicotiana | same crossed floral scent x nectar-restriction architecture yields negative Delta_AD for native community/Manduca but positive Delta_AD for Hyles | directly fails fixed trait-sign expectation | same chemical/trait implementation, opposite signs | consumer context matters, but identity alone does not explain the broader dose/geometry failures | predicted if effective mutualist/antagonist response domains differ by consumer context |

## Falsification result

### Defence strength alone is insufficient

The strongest rejection comes from within-mechanism state changes. Polemonium changes from guarded-compatible to pollinator-interfering with dose, and Asclepias changes with cumulative exposure. Nicotiana shows that even within one treatment the sign depends on whether arrival, handling, or consumption is measured. A one-dimensional 'more defence -> more cost' rule is therefore too coarse.

### Modality alone is rejected

Both chemical and physical systems contain selective, non-selective, and failed/bypassed states. Physical systems alone include selective geometry (Codonopsis), temporal separation (Chrysothemis), broad mutualist exclusion (Bejaria), and antagonist bypass (Salvia). Chemical systems likewise span guarded and interfering states. Material class is therefore not the universal discriminator.

### Consumer identity alone is insufficient

Consumer identity clearly matters, but it is not a sufficient rule. Thunia is the decisive counterexample because the same Bombus visitor changes functional role under altered floral access architecture. Asclepias and Nicotiana add within-consumer changes across exposure or response stage. Kessler 2015 establishes that consumer context can reverse a direct crossed-trait sign, but the broader evidence shows that the relevant state is the interaction between consumer properties and the effective trait domain, not taxon name by itself.

### Effective-domain separation survives the boundary cases

H1 is the only candidate among these four that predicts all three observed classes with one rule:

```text
1. selective/guarded state
2. non-selective/interference state
3. bypass/non-effective-D state
```

It also accommodates direct factorial sign heterogeneity without requiring a universal sign.

## Independence / circularity guard

This audit does **not** claim formal predictive accuracy. The systems were discovered through mechanism-oriented literature screening, not sampled randomly, and the domain-separation vocabulary was refined during the audit sequence. The present result is therefore a falsification-style comparison of explanatory sufficiency, not an out-of-sample validation.

A stronger future test would preregister the three-state rule and code a new literature batch blind to outcome, or manipulate a separating coordinate prospectively within one A x D factorial system.

## Current inference

The empirical conclusion can now be stated more sharply than 'context dependence':

> **The repeatable object is a conditional interaction architecture. Floral defence/access limitation preserves pollination when antagonist and pollinator effective response/access domains remain separable; pollinator interference appears when those domains overlap; and defence efficacy disappears when antagonists bypass or tolerate the domain.**

The rule is cross-modal and survives explicit counterexamples to simpler strength-, modality-, and identity-only explanations.

## What this still does not establish

- a universal numerical threshold;
- a population prevalence of each state;
- a universal positive or negative W_AD;
- formal interaction uncertainty for Kessler 2015 without replicate-level source data;
- the direct joint-cost channel kappa.
