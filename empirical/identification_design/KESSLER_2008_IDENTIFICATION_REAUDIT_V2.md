# Kessler et al. 2008 identification re-audit v2

## Scope

This re-audit asks how far Kessler, Gase & Baldwin (2008; DOI `10.1126/science.1160072`) reaches under the discrete BITA identification design. It does not treat the experiment as a local mixed-partial estimate and does not infer `rho_delta`, `iota_delta`, or `kappa_delta` from marginal consumer responses.

## Experimental trait structure

The field experiment independently blocked the dominant floral attractant benzylacetone (BA) and nicotine production in all four combinations:

```text
EV    A+, D+
PMT   A+, D-
CHAL  A-, D+
CP    A-, D-
```

The biological mapping is unusually close to the focal trait architecture:

```text
A = floral benzylacetone emission
D candidate = floral-nectar nicotine / nicotine-associated repellent state
```

BA has a direct floral-attraction role. Nicotine changes floral visitor behaviour and the source reports reduced florivory and nectar robbing when nicotine is present. The main biological caveat is intervention scope: `Napmt1/2` silencing reduces nicotine systemically, so the manipulated D coordinate is not flower-exclusive even though nectar nicotine is the focal floral phenotype.

## Female outcrossing information recoverable from the published article

The main article reports that three flowers on 41–60 plants of each transgenic genotype were emasculated on each of five experimental days. Across all genotypes:

```text
601 antherectomized flowers total
127 flowers on one windy day -> 0 capsules, no active pollinators
474 flowers on the remaining four informative days
87 mature capsules produced from those 474 flowers before subsequent losses
```

The article explicitly points to supplementary Fig. S8A for individual-day values. The published genotype summary has the `A+,D+` EV state at about 35% capsule maturation, while each state missing BA, nicotine, or both lies around 12–14%.

The descriptive aggregate interaction is therefore robustly positive over the rounded published range:

```text
probability-scale Delta_AD = p11 - p10 - p01 + p00
published rounded range:   approximately +0.19 to +0.25

logit interaction beta_AD: approximately +1.019 to +1.551
interaction OR:             approximately 2.77 to 4.71
```

This already establishes a stronger point than a channel-specific service anchor: Kessler 2008 contains a **manipulated two-trait common reproductive surface** with a positive published aggregate interaction sign.

## Registered supplement recovery

The former next step—recover Fig. S8A / day-by-genotype values—has now been executed as a registered fail-closed probe.

GitHub Actions run `33187904211` tested five current and legacy Science supporting-material routes. All five returned HTTP 403. The result is recorded in:

- `empirical/identification_design/KESSLER_2008_SUPPLEMENT_ACCESS_RECEIPT_V1.json`
- `empirical/identification_design/KESSLER_2008_SUPPLEMENT_ACCESS_RECEIPT_V1.md`

Thus:

```text
SUPPLEMENT_PDF:              NOT RECOVERED FROM REGISTERED PUBLIC ROUTES
FIG_S8A_DAY_VALUES:          NOT EVALUABLE
SOURCE_REPORTED_AXD_SE_CI:   NOT RECOVERED
```

This access result is not evidence that the original interaction was nonsignificant. It only prevents a source-scale uncertainty estimate from being reconstructed from the registered routes.

## Registered aggregate uncertainty sensitivity

Because the supplement is inaccessible, the strongest lawful next step is to ask what the published aggregate constraints alone can and cannot support without pretending to reconstruct the source ANOVA.

GitHub Actions run `33188639818` enumerated integer allocations satisfying:

```text
sum n = 474 informative flowers
sum y = 87 capsules
EV fraction = 34.5–35.5%
PMT/CHAL/CP fractions = 11.5–14.5%
```

and varied the maximum ratio of largest to smallest genotype denominator from 1.25 to 3.0. Across 137,477 to 3,052,260 feasible allocations per profile:

```text
minimum probability-scale Delta: +0.1731 to +0.1710
minimum naive probability z:      2.461 to 2.296
minimum logit beta:               +0.891 to +0.876
minimum logit z:                   1.763 to 1.593
minimum logit CI lower bound:     -0.100 to -0.205
```

The positive **sign** survives every declared aggregate-compatible profile. Formal uncertainty does not: the auxiliary logit interval can cross zero, and at the broadest denominator profile a variance inflation of only about 1.37 would reduce the worst naive probability-scale z to 1.96.

The aggregate analysis is therefore deliberately classified as:

```text
DIRECT_FACTORIAL_SIGN_POSITIVE
AGGREGATE_SIGN_ROBUST
FORMAL_SOURCE_UNCERTAINTY_UNRESOLVED
```

It is not a recovered source day-stratified interaction CI. Full receipts are `KESSLER_2008_AGGREGATE_BOUNDS_V1.json` and `KESSLER_2008_AGGREGATE_BOUNDS_V1.md`.

## What this study identifies

This study now provides the strongest experimentally crossed A/D-like trait architecture in BITA:

```text
A manipulated:                         YES
D-candidate manipulated:               YES
same 2x2 experimental plants:          YES
shared female reproductive outcome:    YES
shared male reproductive outcome:      YES
probability-scale Delta_AD sign:        POSITIVE under published constraints
aggregate sign robustness:             YES across registered integer profiles
source/design-based A×D SE / CI:        NOT RECOVERED
formal interval wholly above zero:     NOT ESTABLISHED
```

The empirical gap is therefore **not the absence of a manipulated A×D reproductive surface**. The outcome-level gap is defensible source/design-based uncertainty on that surface, plus the systemic-nicotine scope caveat.

## Why channel identification still fails

The BITA allocation framework requires the trait factorial to be crossed with selective antagonist and pollinator interventions. Kessler 2008 does not provide that design. Pollinator visitation, nectar robbing and florivory are measured consequences of the four genotype states, not independently randomized consumer presence/absence toggles crossed with A×D.

Consequently the study cannot recover:

```text
rho_delta
iota_increment_delta
m0_delta
iota_total_delta
A×D×G×P separability diagnostic
independent kappa_delta
```

The consumer observations help explain why the phenotype matters, but they cannot be algebraically substituted for the missing consumer-intervention contrasts.

## Organ-scope caveat

Nicotine biosynthesis is not restricted to nectar. The transformed `Napmt1/2` state changes nicotine throughout the plant. Plant-level fitness differences can therefore contain non-floral consequences of nicotine suppression. This does not erase the factorial result, but it prevents the experiment from being treated as a perfectly isolated flower-specific D intervention.

## Current identification classification

```text
DIRECT_DISCRETE_AXD:                   YES
DIRECT_AXD_SIGN:                       POSITIVE under published aggregate constraints
AGGREGATE_SIGN_ROBUSTNESS:             ACHIEVED
FORMAL_AXD_SOURCE_UNCERTAINTY:         UNRESOLVED
FLOWER_SPECIFIC_D_INTERVENTION:        PARTIAL / SYSTEMIC CAVEAT
SELECTIVE_G_TOGGLE:                    NO
SELECTIVE_P_TOGGLE:                    NO
M0_DELTA:                              NO
INDEPENDENT_KAPPA_ASSAY:               NO
FULL_CHANNEL_IDENTIFICATION:           NO
```

## Consequence for the paper

Kessler 2008 changes the paper's empirical premise in two stages. First, it shows that direct attraction-by-defence-like experimentation is not absent. Second, the registered recovery work shows that the positive factorial sign is unusually robust even though formal source uncertainty remains unavailable.

The sharper distinction is now:

```text
manipulated trait surface recovered
+ positive aggregate sign recovered
versus
formal escape interval not yet identified
versus
mechanism allocation not identified
```

These are three different information levels and should not be collapsed.

## Next action

1. Continue only targeted lawful recovery of Fig. S8A / source uncertainty rather than repeating generic searches for an A×D factorial.
2. If source-scale uncertainty remains inaccessible, prioritize a second manipulated A×D common reproductive surface with complete uncertainty and cleaner flower-specific D scope.
3. For mechanism attribution, add selective consumer interventions and an independent joint-cost assay rather than extracting `rho`, `iota`, or `kappa` from the existing marginal visitor data.
