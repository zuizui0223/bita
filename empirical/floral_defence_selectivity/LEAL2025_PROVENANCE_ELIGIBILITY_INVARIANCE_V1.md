# Leal 2025 provenance-conflict geometry-eligibility invariance v1

## Decision

The two unresolved Leal `study`-label provenance conflicts still prevent a
source-resolved count of all historical biological programs, but they **do not
affect the set of historical studies eligible for the direct
access-geometry → robbery question**.

~~~text
HISTORICAL_STUDY_FIELD_LABELS = 56
PROVENANCE_CONFLICT_LABELS = 2
HISTORICAL_DIRECT_GEOMETRY_ELIGIBLE_LABELS = 4
PROVENANCE_CONFLICT_CAN_ADD_DIRECT_GEOMETRY_ELIGIBLE_PROGRAM = NO
HISTORICAL_DIRECT_ELIGIBLE_SET = RESOLVED_INVARIANT_TO_SOURCE_SPLIT
SOURCE_RESOLVED_ALL_PROGRAM_DENOMINATOR = NOT_YET_FINAL
~~~

## Conflict 1 — Varma&Sinu2019

The mixed Leal label contains records for:

- *Sesamum radiatum*;
- *Embothrium coccineum*.

### Verified named source: Varma & Sinu 2019

Varma & Sinu (2019), DOI `10.1038/s41598-019-44741-y`, tests the consequences
of naturally robbed versus unrobbed *Sesamum radiatum* flowers for pollinator
behaviour and maternal reproduction. Its stated predictors are robbery state /
visit type, not flower access geometry.

Geometry eligibility:

~~~text
DIRECT_GEOMETRY_TO_ROBBERY = NO
~~~

### Plausible Embothrium source

Valdivia, Orellana & Morales-Paredes (2018), DOI
`10.5735/085.055.0403`, studies ant-mediated nectar robbing in
*Embothrium coccineum*. Its stated question is whether robbery changes nectar,
visitor behaviour and seed production. The paper does not test floral access
geometry as a predictor of whether robbery occurs.

Geometry eligibility:

~~~text
DIRECT_GEOMETRY_TO_ROBBERY = NO
~~~

Exact row-level reassignment of the two *Embothrium* effect-size rows remains
unverified, so the source label itself stays provenance-conflicted. But either
verified/credible source component is geometry-ineligible.

## Conflict 2 — Zhangetal2009a

The mixed Leal label contains:

- *Corydalis ternatifolia*;
- *C. tomentella*;
- *C. incisa*;
- *Glechoma longituba*.

### Verified Corydalis source

Zhang et al. (2009), DOI `10.1093/aob/mcp104`, explicitly selected three
*Corydalis* species with very similar floral morphology to test how mating system
changes the reproductive consequences of robbery. It records robbery rates but
does not model access geometry as the predictor of robbery.

Geometry eligibility:

~~~text
DIRECT_GEOMETRY_TO_ROBBERY = NO
~~~

### Plausible Glechoma source family

The contemporaneous Zhang-group *Glechoma longituba* programs currently relevant
to the unresolved rows include:

- Zhang et al. 2007, DOI `10.1007/s11258-006-9244-y`;
- Zhang et al. 2009, DOI `10.1111/j.1420-9101.2008.01669.x`;
- Zhang et al. 2011, DOI `10.1111/j.1438-8677.2009.00279.x`.

These studies respectively focus on robbery and reproductive fitness, selective
robbing between sexual morphs and its reproductive consequences, and behavioural
differences between male and female carpenter-bee robbers / energetic payoff.
None tests plant–visitor mechanical access geometry as the predictor of robbery.

Geometry eligibility for every currently plausible Glechoma component:

~~~text
DIRECT_GEOMETRY_TO_ROBBERY = NO
~~~

Exact row-level source assignment for the two Glechoma records remains unresolved,
but resolving it cannot add a direct-geometry eligible study under the frozen
contract.

## Consequence

The historical direct-geometry screen can now make a stronger statement:

~~~text
50 source labels = geometry-ineligible
4 source labels  = direct-geometry eligible
2 source labels  = provenance-conflicted, but all plausible components
                   independently geometry-ineligible
~~~

Therefore the **historical eligible set is stable at four programs** even though
the all-study source-resolved denominator remains unavailable.

This does **not** open the formal recurrence statistic. The remaining inferential
blocker is the lack of a finite, exportable, deduplicated geometry-specific
bibliographic update frame. The bounded Stage-U web search remains supporting
evidence only.

The primary standardized network result remains `k = 2`.
