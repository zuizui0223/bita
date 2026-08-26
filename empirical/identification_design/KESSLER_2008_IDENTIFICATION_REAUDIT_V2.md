# Kessler et al. 2008 identification re-audit v2

## Scope

This re-audit asks how far Kessler, Gase & Baldwin (2008; DOI `10.1126/science.1160072`) reaches under the new discrete identification design. It does not treat the paper as a local mixed-partial estimate and does not infer `rho_delta`, `iota_delta`, or `kappa_delta` from marginal consumer responses.

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

BA has a direct floral-attraction role. Nicotine changes floral visitor behaviour and the source reports reduced florivory and nectar robbing when nicotine is present. The main caveat is intervention scope: `Napmt1/2` silencing reduces nicotine systemically, so the manipulated D coordinate is not flower-exclusive even though nectar nicotine is the focal floral phenotype.

## Female outcrossing information recoverable from the published article

The main article reports that three flowers on 41–60 plants of each transgenic genotype were emasculated on each of five experimental days. Across all genotypes:

```text
601 antherectomized flowers total
127 flowers on one windy day -> 0 capsules, no active pollinators
474 flowers on the remaining four informative days
87 mature capsules produced from those 474 flowers before subsequent losses
```

The article explicitly points to supplementary Fig. S8A for individual-day values. The published genotype summary has the `A+,D+` EV state at about 35% capsule maturation, while each state missing BA, nicotine, or both lies around 12–14%.

The existing sensitivity reconstruction therefore remains valid:

```text
probability-scale Delta_AD = p11 - p10 - p01 + p00
published rounded range:   +0.19 to +0.25

logit interaction beta_AD: +1.019 to +1.551
interaction OR:             2.77 to 4.71
```

The sign is robust to the published rounded range on both scales. A broad integer-allocation stress test also retained a positive interaction sign, but formal significance was not allocation-robust because exact genotype-by-day denominators and the original factorial uncertainty are not available in the accessible aggregate record.

## What this study identifies

This study provides the strongest current experimentally crossed A/D-like trait architecture in the project:

```text
A manipulated:                         YES
D-candidate manipulated:               YES
same 2x2 experimental plants:          YES
shared female reproductive outcome:    YES
shared male reproductive outcome:      YES
probability-scale Delta_AD sign:        POSITIVE under published rounded range
logit-scale interaction sign:          POSITIVE under published rounded range
source-reported A×D SE / CI:            NO
```

The result should therefore be described as a **direct discrete factorial sign-positive anchor with unresolved formal interaction uncertainty**, not as a continuous local `W_AD` estimate.

## Why channel identification still fails

The new framework requires the trait factorial to be crossed with selective antagonist and pollinator interventions. Kessler 2008 does not provide that design. Pollinator visitation, nectar robbing and florivory are measured consequences of the four genotype states, not independently randomized consumer presence/absence toggles crossed with A×D.

Consequently the study cannot recover:

```text
rho_delta
iota_increment_delta
m0_delta
iota_total_delta
A×D×G×P separability diagnostic
independent kappa_delta
```

The consumer observations can explain why the phenotype matters, but they cannot be algebraically substituted for the missing consumer-intervention contrasts.

## Organ-scope caveat

Nicotine biosynthesis is not restricted to nectar. The transformed `Napmt1/2` state changes nicotine throughout the plant. Plant-level fitness differences can therefore contain non-floral consequences of nicotine suppression. This does not erase the floral factorial result, but it prevents the experiment from being treated as a perfectly isolated flower-specific D intervention.

A future implementation can solve this by using a tissue-restricted or local floral manipulation. Later inducible transgenic methods in *Nicotiana attenuata* demonstrate that spatially restricted gene manipulation is technically feasible, but that later capability is not evidence that the 2008 intervention itself was flower-specific.

## Identification classification

```text
DIRECT_DISCRETE_AXD:                   YES
DIRECT_AXD_SIGN:                       POSITIVE under published aggregate constraints
FORMAL_AXD_UNCERTAINTY:                UNRESOLVED
FLOWER_SPECIFIC_D_INTERVENTION:        PARTIAL / SYSTEMIC CAVEAT
SELECTIVE_G_TOGGLE:                    NO
SELECTIVE_P_TOGGLE:                    NO
M0_DELTA:                              NO
INDEPENDENT_KAPPA_ASSAY:               NO
FULL_CHANNEL_IDENTIFICATION:           NO
```

## Consequence for the new paper

Kessler 2008 changes the argument in an important way. The empirical gap is **not** simply that nobody has crossed attraction and defence-like floral traits. At least one unusually close 2×2 field experiment already exists and yields a sign-robust positive discrete interaction under the published aggregate constraints.

The sharper gap is that the trait factorial has not been crossed with the consumer interventions and independent cost assay required to identify the channel decomposition. The new contribution is therefore the distinction between:

```text
trait interaction identified
versus
mechanism allocation identified.
```

That distinction should replace any claim that direct A×D experimentation is absent altogether.
