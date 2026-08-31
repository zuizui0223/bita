# Kessler et al. 2008 identification re-audit v3

## Scope

This re-audit asks how far Kessler, Gase & Baldwin (2008; DOI `10.1126/science.1160072`) reaches under the discrete BITA outcome hierarchy and the mechanism-allocation design. It preserves the source/manipulation caveats and separates four distinct questions:

```text
1. does a manipulated A×D-like reproductive surface exist?
2. is the total interaction sign identified under published aggregate constraints?
3. do A0 and A1 identify Level-2/3 release?
4. are rho / iota / kappa point-identified?
```

## Experimental mapping

```text
EV    A+, D+
PMT   A+, D-
CHAL  A-, D+
CP    A-, D-
```

with

```text
A = floral benzylacetone emission
D candidate = nicotine-associated floral/nectar repellent state
```

BA has a direct floral-attraction role. Nicotine changes floral visitor behaviour and reduces nectar robbery / florivory, but `Napmt1/2` silencing is systemic, so the D intervention is not flower-exclusive.

## Published female-outcrossing constraints

The accessible main article gives:

```text
601 antherectomized flowers across five experimental days
127 flowers on one wind-only day -> zero capsules and no active pollinators
474 flowers on the four informative days
87 capsules before later losses
EV mean approximately 35%
PMT / CHAL / CP means approximately 12–14%
```

Exact genotype-by-day values remain in Fig. S8A, which was not recovered from the registered public Science routes.

## Registered aggregate Stage-1 decomposition

The current Stage-1 contrasts are

```text
A0       = p10 - p00
A1       = p11 - p01
Delta_AD = A1 - A0
```

GitHub Actions run `33357523448` enumerated every integer allocation compatible with the registered aggregate constraints under maximum denominator ratios 1.25, 1.5, 2.0 and 3.0.

Across all four profiles:

```text
A0 identified set:       [-0.0299275, +0.0299275]
A1 identified set:       [+0.2001327, +0.2398387]
minimum Delta_AD:        +0.1710239
minimum naive z(Delta):   2.2960104
minimum logit z:          1.5932234
minimum logit CI lower:  -0.2048849
```

The decisive refinement is:

```text
A1 > 0 for every compatible allocation
A0 spans zero
```

Therefore the defended attraction effect is sign-identified as positive under the declared aggregate restrictions. The strict release ambiguity has been localized entirely to the undefended attraction effect.

## Outcome claim hierarchy

The registered hierarchy is

```text
Level 1: Delta_AD > 0
Level 2: A0 <= 0 and A1 > 0
Level 3: A0 < 0 and A1 > 0
```

Current Kessler classification:

```text
Level 1 total-interaction sign:        STRONG POSITIVE AGGREGATE ANCHOR
A1 defended attraction effect:         POSITIVE UNDER ALL DECLARED PROFILES
A0 undefended attraction effect:       SIGN UNRESOLVED
Level 2 strict constraint release:     NOT IDENTIFIED
Level 3 strict reversal:               NOT IDENTIFIED
```

The smallest descriptive epsilon for which every compatible allocation satisfies

```text
A0 <= epsilon
```

is `0.0299275`, about three percentage points on the capsule-probability scale. This is an identified-set width, not a biological equivalence margin and not permission to relabel Level 2 after seeing the data.

This produces the fail-closed decision token:

```text
A1_POSITIVE_A0_SIGN_UNRESOLVED_PARTIAL_IDENTIFICATION
```

rather than the older undifferentiated statement `Levels 2/3 unresolved`.

## Source/design uncertainty boundary

The aggregate enumeration is not the source ANOVA. The exact genotype-by-day values, plant-level clustering and source interaction SE/CI remain unavailable.

Thus:

```text
aggregate Delta_AD sign robust:           YES
aggregate A1 sign robust:                 YES
strict Level 2 from aggregate set:        NO
source/design interaction interval > 0:   NOT ESTABLISHED
```

The auxiliary pooled-binomial probability result is not promoted to source-scale significance, and the auxiliary logit interval already demonstrates scale/variance sensitivity by crossing zero under compatible allocations.

## Mechanism allocation remains unresolved

Kessler 2008 does not independently randomize antagonist and pollinator access on top of the A×D trait factorial. Its visitor, florivory and robbery measures are consequences of genotype state, not selective consumer toggles.

Consequently it does not point-identify:

```text
rho_delta
iota_increment_delta
m0_delta
iota_total_delta
A×D×G×P separability diagnostic
independent kappa_delta
```

The study identifies an outcome surface much more strongly than it identifies its channel allocation.

## Current classification

```text
DIRECT_DISCRETE_AXD:                         YES
DIRECT_AXD_SIGN:                             POSITIVE under aggregate restrictions
A1_DEFENDED_ATTRACTION_SIGN:                 POSITIVE / IDENTIFIED UNDER AGGREGATE SET
A0_UNDEFENDED_ATTRACTION_SIGN:               UNRESOLVED WITHIN ±0.02993
LEVEL2_CONSTRAINT_RELEASE:                   UNRESOLVED
LEVEL3_STRICT_REVERSAL:                      UNRESOLVED
FORMAL_AXD_SOURCE_UNCERTAINTY:               UNRESOLVED
FLOWER_SPECIFIC_D_INTERVENTION:              PARTIAL / SYSTEMIC CAVEAT
SELECTIVE_G_TOGGLE:                          NO
SELECTIVE_P_TOGGLE:                          NO
INDEPENDENT_KAPPA_ASSAY:                     NO
FULL_CHANNEL_IDENTIFICATION:                 NO
```

## Consequence for BITA

The empirical gap is now narrower than before:

```text
manipulated A×D reproductive surface         ACHIEVED
positive total interaction sign              ACHIEVED
positive attraction effect with defence      ACHIEVED under aggregate restrictions
sign of attraction effect without defence    UNRESOLVED within about ±3 percentage points
strict Level-2/3 release                     UNRESOLVED
source-scale uncertainty                     UNRESOLVED
mechanism allocation                         UNRESOLVED
```

This matters conceptually. BITA no longer needs another system merely to show that defence can coexist with a strong positive attraction response. What remains decisive for a strong 'release' claim is evidence that the attraction effect without defence is genuinely nonpositive, plus compatible source/design uncertainty.

## Next action

1. Keep lawful Fig. S8A/source-uncertainty recovery targeted rather than reopening broad literature search.
2. Search specifically for a manipulated A×D system whose four-cell reproductive outcome can identify `A0 <= 0` and `A1 > 0` with design-based uncertainty and cleaner flower-specific D scope.
3. Treat a prospective Kessler-type replication as a Level-2/3 design problem, not merely a Level-1 interaction-power problem.
4. Add selective consumer interventions and an independent joint-cost assay only when mechanism attribution is required.

## Provenance

```text
Stage-1 partial-ID workflow: 33357523448
head SHA at run:              a0ee9d04f312a715b0ad7360f314bb131a94494c
receipt: empirical/identification_design/KESSLER_2008_STAGE1_PARTIAL_IDENTIFICATION_RECEIPT_V2.json
```
