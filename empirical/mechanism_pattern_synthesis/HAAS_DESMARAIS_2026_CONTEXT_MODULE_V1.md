# Haas-Desmarais et al. 2026 antagonist-pressure context module v1

## Source

Haas-Desmarais S, Castagneyrol B, Abdala-Roberts L, Lortie CJ, Traveset A, Moreira X. **The effect of herbivory on pollinators: a revisited meta-analysis.** *Annals of Botany* 137(4):879–885. DOI: `10.1093/aob/mcaf258`.

Publication timeline: online 16 October 2025; issue April 2026.

Primary article and supplementary-data landing page are open access through Oxford Academic / PubMed Central.

## Why this module is being audited

This synthesis is unusually large and directly quantifies how antagonist pressure changes three outcome classes relevant to the theory-facing environmental layer:

```text
H -> floral phenotype / reward-related floral traits
H -> pollinator attraction
H -> plant reproductive output
```

It is **not** a study of the focal defence trait `D` and cannot be used as direct evidence for `D -> antagonism`, `D -> pollination`, `rho`, `iota`, `kappa`, or `W_AD`.

## Published data architecture

The authors extended earlier syntheses and report:

```text
171 studies
1,348 study cases
```

The new search added 51 studies / 460 study cases after screening 894 publications retrieved with updated herbivory × pollination search strings.

Responses were grouped into:

1. floral traits — flower number, floral size, nectar volume/concentration, phenology;
2. pollinator attraction — abundance/diversity, visit counts, flowers visited, visit duration;
3. plant reproduction — seed/fruit number and weight, seed viability.

Context axes:

```text
damage type: natural vs simulated
plant tissue: roots / leaves / flowers / stems / mixed
```

## Effect scale and dependence

Each study case was converted to Hedges' g, oriented so negative values mean lower response under herbivory.

The published analyses used multilevel mixed-effects meta-analysis with replicate analysis nested within study ID. Shared-control dependence was represented with a sampling-error variance–covariance matrix. The authors also report sensitivity and publication-bias analyses in the supplementary material.

This dependence treatment is materially stronger than treating 1,348 cases as independent observations.

## Published quantitative results

Overall across response classes:

```text
mean Hedges' g = -0.20 ± 0.04 SE
z = -5.42
P < 0.0001
tau^2 = 0.26
Q_T = 5275.72
I^2 = 71.4%
```

The primary Pattern is not simply a negative grand mean. Heterogeneity is substantial, and moderators are significant:

```text
response variable: significant
damage type: Q_M = 10.31, P = 0.006
plant tissue: Q_M = 22.97, P = 0.003
damage type × tissue: Q_M = 27.91, P < 0.001
```

The response-class test is also significant (`Q_M = 15.41`, `P < 0.001`).

## Published state changes

The source reports the following qualitative states in the updated dataset.

### Floral traits

- natural leaf damage: negative;
- natural flower damage: non-significant;
- natural root/stem/mixed damage: non-significant;
- simulated flower damage: negative;
- simulated stem damage: negative;
- simulated root/leaf/mixed damage: non-significant.

### Pollinator attraction

- natural leaf damage: negative;
- natural flower damage: negative;
- natural root/stem/mixed damage: non-significant;
- simulated leaf damage: negative;
- simulated flower/mixed damage: non-significant;
- no simulated-stem summary is shown in the published Table 1.

### Plant reproduction

- natural leaf damage: negative;
- natural flower damage: negative;
- natural root/stem/mixed damage: non-significant;
- simulated leaf/flower/stem/mixed damage: non-significant;
- the published Table 1 does not show a simulated-root reproduction row.

The key cross-study result is therefore **tissue- and damage-mode-dependent opening/closing of antagonist effects across floral phenotype, pollinator attraction, and reproduction**.

## Theory-facing mapping

Admitted mapping:

```text
H context can alter floral phenotype
H context can alter pollinator service
H context can alter reproductive output
H effects depend on tissue and natural/simulated damage state
```

This independently supports the Part I warning that an environmental antagonist-pressure axis cannot be assumed to act through one isolated channel or in one universal direction/magnitude.

It also strengthens the empirical interpretation that `H` and effective pollinator service may be coupled ecological states.

## What this module does NOT identify

```text
herbivory treatment != defence trait D
H -> pollinator effect != M_AD
H -> reproduction effect != W_AD
H -> floral phenotype effect != A or D curvature
negative g != rho
moderator contrast != dW_AD/dH
```

The module cannot be algebraically inserted into `W_AD = rho - iota - kappa`.

## Relationship to existing Part II modules

### Versus Leal et al. 2025

Leal isolates floral larceny and quantifies reward, visitation, and female-fitness costs. Haas-Desmarais spans broader herbivory modes and tissues and explicitly tests tissue × damage-type heterogeneity.

The modules therefore replicate a broad **antagonist-cost / pollinator-coupling Pattern** in independent synthesis universes while contributing different contextual resolution.

### Versus Sasidharan et al. 2023

Sasidharan addresses shared floral-signal responses across pollinators and florivores. Haas-Desmarais addresses how antagonist damage changes floral traits, pollinator attraction, and reproduction.

The biological axes are complementary rather than duplicate.

## Current adjudication

```text
source identity:                  PASS
data architecture reported:      PASS
dependence treatment reported:   PASS
quantitative cross-study result: PASS
context moderator structure:     PASS
theory inference boundary:       PASS
raw deposited reanalysis here:   NOT YET REPRODUCED
```

### Decision

**ADMIT_AS_PUBLISHED_META_SYNTHESIS_PENDING_SUPPLEMENT_REPRODUCTION**

It is already admissible as a published independent context module in the Pattern architecture, but should not replace the current fully reproduced Leal/Sasidharan modules until the supplementary files have been locally reconstructed and checked.

## Manuscript-ready conservative claim

> An independent updated meta-analysis of 171 studies and 1,348 study cases found that herbivory reduced floral traits, pollinator attraction, and reproduction on average, but the effects depended strongly on damaged tissue and whether damage was natural or simulated. This cross-study pattern supports an environmental-context interpretation in which antagonist pressure can alter several channels simultaneously; it does not identify a floral defence trait or the attraction–defence mixed partial.
