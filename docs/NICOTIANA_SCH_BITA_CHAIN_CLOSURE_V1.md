# Nicotiana SCH–BITA chain-closure plan v1

## Decision

The *Nicotiana attenuata* programme is the highest-information candidate for closing the sequence from a one-trait dual-audience conflict to a second-trait functional response. It is not already a direct complete chain.

```text
current status:
PROGRAM_COMPOSITE_NEAR_COMPLETE
DIRECT_COMPLETE_CHAIN_NOT_ESTABLISHED
```

The programme is ranked first because different primary studies in the same plant system recover unusually complementary pieces:

```text
A attracts mutualists and an antagonist
+ an A × D-like reproductive factorial exists
+ flower-specific defence biology is experimentally tractable
```

The missing object is still their intersection on one invariant `A`, one independently manipulated flower-specific `D`, one common reproductive outcome, and a design-based uncertainty model.

## Source-role ledger

### Kessler et al. 2015 — one-trait receiver overlap

Kessler et al. (2015; DOI `10.7554/eLife.07641`) experimentally uncoupled floral benzylacetone and nectar production. The study showed that these attraction/reward components affected outcrossing by separately tested pollinator guilds and hawkmoth oviposition.

Admitted use:

```text
DIRECT_PROGRAM_LEVEL_SAME_SYSTEM_A_RECEIVER_OVERLAP
```

It supports the proposition that an experimentally varied attraction coordinate can be tracked by mutualists and an antagonist in *N. attenuata*.

Prohibited promotion:

- hawkmoth oviposition is not itself antagonist-mediated reproductive loss on the same scale as outcrossing;
- separate receiver and reproductive outcomes do not estimate a common net `W(A)` decomposition;
- this study contains no second antagonist-reducing trait `D` crossed with the same `A`.

### Kessler, Gase & Baldwin 2008 — trait-factorial reproductive anchor

Kessler et al. (2008; DOI `10.1126/science.1160072`) blocked benzylacetone production and nicotine production in all four combinations in a native field experiment. The study reports reproductive outcomes and visitor/antagonist consequences. The repository reconstruction preserves a positive aggregate interaction sign across the published rounded capsule proportions.

Admitted use:

```text
DIRECT_AxD_LIKE_REPRODUCTIVE_SURFACE
AGGREGATE_SIGN_ROBUST
```

Prohibited promotion:

- exact source/design-based interaction uncertainty is not recovered;
- nicotine suppression is systemic rather than demonstrated to be flower-restricted;
- consumer responses are consequences of the trait states, not selective antagonist and pollinator toggles;
- the study does not identify `rho_delta`, baseline-corrected `iota_delta`, `m0_delta`, separability or `kappa_delta`;
- a positive `Delta_AD W` does not by itself identify `A0 <= 0 < A1` or `A0 < 0 < A1`.

### Li et al. 2017 — flower-specific defence sector

Li et al. (2017; DOI `10.1073/pnas.1703463114`) identifies a flower-specific jasmonate-signalling sector regulating constitutive floral defence in *N. attenuata*.

Admitted use:

```text
FLOWER_SPECIFIC_D_MECHANISM_AND_TOOL_CANDIDATE
```

This makes it plausible to construct a cleaner floral `D` intervention than systemic nicotine suppression.

Prohibited promotion:

- a signalling sector is not yet one declared quantitative `D` coordinate;
- a candidate output must be shown independently to reduce the focal antagonist route;
- the intervention must be verified not to alter benzylacetone, nectar, vegetative defence, flower development or the declared `A` contrast.

### Li et al. 2018 — upstream pleiotropy warning

Li et al. (2018; DOI `10.1111/jipb.12607`) reports that jasmonate-signalling perturbation changes floral attraction/reward outputs and florivore attack or damage.

Admitted use:

```text
COORDINATE_STABILITY_WARNING
```

The study demonstrates why an upstream JA perturbation cannot automatically serve as the BITA `D` manipulation: if it changes benzylacetone or nectar while changing defence, then `A` and `D` are not independently crossed.

## Why the programme is near-complete but not complete

| Chain element | Current programme evidence | Current status |
|---|---|---|
| declared attraction coordinate `A` | benzylacetone is experimentally manipulable | available |
| pollinator response to `A` | direct programme evidence | available |
| antagonist response to `A` | direct hawkmoth oviposition evidence | available |
| antagonist-mediated reproductive loss on the same `W(A)` scale | not matched to the receiver evidence | missing |
| distinct antagonist-reducing `D` | nicotine-like and flower-specific JA-regulated candidates | available in principle |
| invariant, independently crossed `A × D` | 2008 is close, but systemic `D`; upstream JA tools risk moving `A` | incomplete |
| `A0`, `A1`, `Delta_AD W` with design-based intervals | not recovered from the historical source | missing |
| selective antagonist/pollinator toggles | absent from the same trait factorial | missing |
| pollinator-absent baseline `m0_delta` | absent | missing |
| four-way separability diagnostic | absent | missing |
| independent joint-cost assay | absent | missing |

The programme therefore supports a composite bridge, not a source-merging estimate. Results from different papers must not be algebraically combined as though they were cells of one experiment.

## Chain-closing Stage 0 — recover the historical outcome surface

Before a new field experiment, exhaust the lowest-cost historical closure route:

1. recover exact genotype-by-day denominators and capsule outcomes underlying the Kessler 2008 female-outcrossing figure;
2. preserve plant/day/block structure and exclusions;
3. estimate `A0`, `A1` and `Delta_AD W` on the additive probability scale;
4. report the three outcome levels separately;
5. keep the systemic-`D` scope caveat even if the formal interval becomes positive.

Stage 0 can close the formal uncertainty of the historical total surface. It cannot turn systemic nicotine suppression into a flower-restricted intervention or identify ecological channels.

## Chain-closing Stage 1 — one four-cell experiment that serves SCH and BITA

### Fixed coordinates

```text
A = benzylacetone production/emission contrast validated to change attraction
D = one flower-specific defence output validated to reduce a focal antagonist route
W = one predeclared plant reproductive endpoint measured in all four cells
```

The selected `D` must pass three pre-experiment gates:

```text
D reduces the focal antagonist outcome
D leaves the A manipulation and benzylacetone emission contrast invariant
D leaves vegetative defence and gross floral development acceptably unchanged
```

### Four trait cells

```text
A0 D0
A1 D0
A0 D1
A1 D1
```

Each matched block must contain all four cells. The primary analysis estimates, from common resamples or a predeclared hierarchical/randomization model,

```text
A0 = W10 - W00
A1 = W11 - W01
Delta_AD W = A1 - A0
```

### Linked SCH measurements

The same trait cells must also record:

- pollinator approach, visitation and a direct service proxy such as pollen transfer;
- focal antagonist approach, oviposition, robbing or florivory;
- antagonist damage or loss linked to the declared reproductive endpoint;
- the common plant reproductive outcome.

The one-trait conflict gate is evaluated first at low defence and then as a defence-conditioned response:

```text
Does the identical A contrast increase pollinator response?
Does it also increase antagonist response or loss?
Are those responses connected to the same declared plant outcome?
```

This closes SCH coverage and BITA outcome estimation in one experiment without pretending that receiver counts alone allocate fitness channels.

### Stage-1 outcome decisions

```text
Level 1: low(Delta_AD W) > 0
         positive interaction relief

Level 2: upper(A0) <= 0 and lower(A1) > 0
         nonpositive-to-positive constraint release

Level 3: upper(A0) < 0 and lower(A1) > 0
         strict negative-to-positive reversal
```

A failure to reach Level 2 is not a failed experiment. It distinguishes improvement of attraction from actual release of a non-beneficial state.

## Chain-closing Stage 2 — selectivity pilot before a 16-cell commitment

The same hawkmoth can contribute pollination and oviposition, so biological-role selectivity is the main feasibility problem. Do not commit immediately to a nominal 16-cell design.

First pilot whether pollinator and antagonist components can be toggled or standardized without moving `A` or `D`. Candidate strategies may exploit receiver guild, timing, access route, hand-pollination standardization or focal oviposition exclusion, but each must be validated rather than assumed selective.

The pilot must estimate plausible magnitude and variance for:

```text
rho_delta
pollinator increment interaction
a pollinator-absent baseline interaction m0_delta
the A × D × antagonist × pollinator coupling contrast
```

If selective toggles cannot be validated because one receiver performs both roles, retain a joint-role model instead of forcing the system into the separable BITA allocation.

## Chain-closing Stage 3 — mechanism allocation and independent cost

Only after Stage 2 establishes feasible contrasts should the study be re-powered for the complete crossed intervention. The design must then:

1. estimate antagonist relief on the same `A × D` coordinate;
2. estimate pollinator interference with baseline correction;
3. test the four-way separability contrast with an uncertainty-aware equivalence or bounded decision;
4. measure an independent `A × D` construction/allocation channel under standardized biotic conditions;
5. compare that assay with the unallocated reproductive residual without defining cost by subtraction.

## Failure conditions that remain informative

- **A changes under the D intervention:** the proposed two-coordinate experiment fails; redesign `D` downstream of the pleiotropic regulator.
- **A attracts pollinators but not the focal antagonist:** SCH shared-cue conflict is not supported for that receiver/coordinate, although BITA interaction estimation can continue.
- **Positive `Delta_AD W`, but `A1 <= 0`:** defence improves attraction without releasing it from a detrimental/non-beneficial state.
- **Level-2 or Level-3 outcome with non-zero four-way coupling:** functional release is real, but the separable `rho/iota` explanation is inadequate.
- **Residual and independent cost assay disagree:** retain an unallocated channel; inspect intervention selectivity, omitted pathways and scale mismatch.
- **No positive total interaction:** report substitution or neutrality; do not mine nearby endpoints for an escape claim.

## Priority judgment

```text
Existing-data closure priority: 1
Full mechanism-experiment practicality: conditional on selectivity pilot
```

*Nicotiana* is the best current programme for recovering the most links with the least conceptual transfer between species. *Pedicularis rex* remains the cleaner selective-`D` backbone if the dual-role hawkmoth system prevents valid consumer-channel separation.
