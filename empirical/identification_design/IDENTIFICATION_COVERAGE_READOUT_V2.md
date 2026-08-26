# Identification coverage readout v2

## Main result

The closest existing studies split the required design into different pieces rather than identifying the full channel architecture in one experiment.

The strongest contrast is:

```text
Kessler et al. 2008
  -> manipulated A×D-like floral phenotype factorial
  -> direct discrete reproductive interaction sign recoverable
  -> no crossed selective antagonist/pollinator toggles

Egan et al. 2021
  -> crossed herbivory × pollination agent factorial
  -> selection on attraction/defence-related traits
  -> no independently manipulated A×D trait factorial
```

The missing intersection is therefore not “floral attraction–defence experiments do not exist.” The missing intersection is:

```text
manipulated A×D traits
+
selective G×P consumer interventions
+
pollinator-absent A×D baseline characterization
+
independent A×D cost assay.
```

## Kessler 2008: direct discrete trait-interaction anchor

Kessler, Gase & Baldwin (2008; `10.1126/science.1160072`) independently blocked floral benzylacetone and nicotine production in four transgenic states. The published female-outcrossing aggregate remains sign-robustly positive under the source-reported ranges:

```text
probability-scale Delta_AD: +0.19 to +0.25
logit interaction beta_AD:  +1.019 to +1.551
interaction OR:              2.77 to 4.71
```

The source reports 601 antherectomized flowers over five experimental days, including one no-pollinator wind day with 127 flowers and zero capsules, leaving 474 informative flowers that produced 87 mature capsules. Exact genotype-by-day values are referred to supplementary Fig. S8A.

What is now defensible:

```text
A×D-like traits experimentally crossed: YES
direct discrete reproductive interaction sign: POSITIVE under published aggregate constraints
formal source A×D uncertainty: UNRESOLVED
```

What remains unavailable:

```text
selective antagonist toggle
selective pollinator toggle
rho_delta
iota_increment_delta
m0_delta
A×D×G×P separability diagnostic
independent kappa_delta
```

The nicotine manipulation is also systemic, so the D intervention is not perfectly flower-restricted.

## Impatiens 2018: public-data retrofit reaches context modification, not channel identification

The Dryad-backed *Impatiens capensis* panel provides observational flower redness (A), floral condensed tannins (D), randomized supplemental robbing/florivory/pollination assignments, and two reproductive components.

A registered hierarchical retrofit tested whether the observational A×D association changed under each randomized agent treatment. Every target interval included zero for both reproductive components. The source therefore reaches:

```text
observational A×D
+
randomized agent modification of observational A×D
```

but not the required channel contrasts, because A/D are not randomized and the agent treatments add interaction intensity rather than selectively switching consumers present/absent.

## Kessler 2015: phenotype factorial with an invalid D axis

The publisher-hosted all-additional-files ZIP was re-audited directly. It contains three TIFF image supplements and no obvious machine-readable source-data file. This confirms the previous source-data limitation for re-estimating an uncertainty-bearing scent×nectar interaction from the publisher package.

More importantly, nectar production/removal is a reward axis, not an independently justified antagonist-reducing D axis. Even perfect raw data would therefore not make this study a strict A×D identification design.

## Pedicularis rex: system-selection anchor

Sun & Huang (2015; `10.1093/aobpla/plv019`) experimentally manipulated a water-holding bract barrier. The same manipulation strongly changed seed predation while showing no detected effect on legitimate pollinator or nectar-robber visitation. It is valuable not because it estimates rho or iota, but because it illustrates a biological system in which consumer selectivity may be achievable through attack route/access geometry.

## High-information coverage matrix

`HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V1.csv` now records 16 high-information systems spanning the direct-A×D audit, near-direct candidates, and the selective-D anchor.

Current fixed findings:

```text
screened high-information systems: 16
systems with full A×D-like trait factorial closest to target: Kessler 2008
systems with crossed G×P-like consumer factorial closest to target: Egan 2021
systems with independent kappa assay: 0
systems with full rho/iota/kappa identification: 0
```

These are coverage statements for the screened high-information set, not prevalence estimates for all floral ecology studies.

## Consequence for the theory

The headline inequality should no longer carry the paper. The experimentally meaningful hierarchy is:

```text
1. measure Delta_AD W on declared discrete trait contrasts;
2. establish selective consumer interventions;
3. estimate rho_delta and pollinator-dependent iota_increment_delta;
4. characterize m0_delta before interpreting total iota_delta;
5. test the A×D×G×P separability contrast;
6. retain any remaining joint channel as unallocated;
7. measure kappa independently rather than defining it as the residual;
8. use the sign identity to constrain any still-unobserved joint channel.
```

The algebra is then a diagnostic layer inside an identification design, not the novelty claim by itself.

## Manuscript implication

Part II should be rewritten from “cross-system Pattern validation of the mechanistic theorem” to “identification coverage of existing evidence.” The existing route ledger can remain as background showing that component mechanisms recur, but its principal role becomes explaining why marginal route evidence does not identify the required causal contrasts.

The 2,592 finite-grid evaluations should remain only as implementation/model-family sensitivity, preferably outside the Abstract and Conclusions.
