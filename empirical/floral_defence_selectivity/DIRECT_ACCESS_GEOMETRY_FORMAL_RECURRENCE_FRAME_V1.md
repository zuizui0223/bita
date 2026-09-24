# Formal recurrence frame for access geometry → nectar robbery v1

## Status

~~~text
FRAME_FREEZE_DATE = 2026-09-24
HISTORICAL_FRAME = LEAL_2025_ROBBER_STUDIES
HISTORICAL_STUDY_FIELD_LABELS = 56
HISTORICAL_SOURCE_RESOLVED_PROGRAMS = NOT_YET_FINAL
PROVENANCE_CONFLICT_LABELS = 2
HISTORICAL_DIRECT_ELIGIBLE_SET = RESOLVED_INVARIANT_TO_SOURCE_SPLIT
HISTORICAL_DIRECT_GEOMETRY_ELIGIBLE_PROGRAMS = 4
PROVENANCE_CONFLICT_CAN_ADD_DIRECT_GEOMETRY_ELIGIBLE_PROGRAM = NO
DIRECT_DISCOVERY_PROGRAMS = 24
DIRECT_DISCOVERY_OVERLAP_WITH_HISTORICAL_FRAME = 4
FORMAL_RECURRENCE_RESULT = NOT_YET_OPENED
~~~

## Purpose

The current direct access-geometry corpus contains 24 study programs, but it was
assembled by bounded discovery and therefore cannot support a prevalence estimate,
sign test, or pooled recurrence statistic.

This file freezes the next, stricter lane: build an outcome-independent sampling
frame first, then screen every record for the same geometry → robbery eligibility
contract.

## Stage H — historical sampling frame

The historical frame begins from the complete set of **56 distinct values of the
`study` field** among nectar-robber rows in the public dataset accompanying:

> Leal LC, Koski MH, Irwin RE, Bronstein JL (2025). Costs of floral larceny:
> a meta-analytical evaluation of nectar robbing and nectar theft on
> animal-pollinated plants. *Ecology* 106:e70036.
> DOI: 10.1002/ecy.70036.
> Public data: 10.5281/zenodo.14773082.

The exact 56 source labels are frozen in:

- `LEAL2025_ROBBER_STUDY_FRAME_V1.csv`

The source meta-analysis was designed around consequences of floral larceny, not
around floral geometry. Therefore this frame is useful as an outcome-independent
historical anchor but is **not assumed to contain every direct geometry study**.

A source-provenance audit found that four multi-plant labels are legitimate
multi-species programs but two labels (`Varma&Sinu2019` and
`Zhangetal2009a`) combine rows that cannot all originate from the named source.
The 56 values must therefore not be treated as 56 verified independent programs.
See `LEAL2025_STUDY_LABEL_PROVENANCE_AUDIT_V1.md`.

The conflict components were then audited independently for the direct geometry
question. The verified Sesamum, Embothrium and Corydalis sources, and every
currently plausible Glechoma source component, all fail the frozen
geometry→robbery eligibility contract. Thus source splitting can change the count
of all historical programs but **cannot add another historical direct-geometry
eligible program**. The historical eligible set is stable at four. See
`LEAL2025_PROVENANCE_ELIGIBILITY_INVARIANCE_V1.md`.

## Stage U — systematic update / gap fill

To avoid treating the Leal frame as complete, a separate update frame must cover
studies missed by that fitness-cost review and all later publications.

The update search is frozen to the period:

~~~text
START_DATE = 2000-01-01
END_DATE   = 2026-09-24
~~~

The early overlap is deliberate. It allows the update search to detect direct
geometry studies that the fitness-cost frame omitted, rather than assuming the two
review questions have identical coverage.

Minimum query families:

~~~text
("nectar robbing" OR "nectar robbery" OR "floral larceny")
AND
("corolla length" OR "tube length" OR "flower length" OR "flower size"
 OR "floral morphology" OR "accessibility" OR "trait mismatch")

("nectar robbing" OR "nectar robbery")
AND
("bill length" OR "tongue length" OR "proboscis" OR "rostrum"
 OR "flowerpiercer" OR "hummingbird" OR "sunbird" OR "bumblebee")
~~~

A record enters the screening frame from bibliographic match alone. Outcome
direction must not determine whether it is retained for full-text eligibility
screening.

Stage-U batches 1–2 are frozen in
`DIRECT_ACCESS_GEOMETRY_STAGE_U_REGISTRY_V1.csv`. Batch 1 recovered three new
Gelsemium programs. Batch 2 plus the final fixed-synonym pass recovered six further
eligible programs spanning Penstemon, experimental Sesamum, an Andean
Bombus–Digitalis mismatch, Tirpitzia, Linaria, and Primula florindae. Duplicate,
secondary-synthesis, non-geometric, and otherwise ineligible candidates remain in
the registry with explicit reasons. This is progress toward, not completion of,
the systematic update frame.

## Eligibility screening

Every frame record is screened against
`DIRECT_ACCESS_GEOMETRY_ROBBERY_CONTRACT_V1.md`.

For each study program, freeze before effect-direction coding:

1. independent biological study identity;
2. floral or visitor–flower access predictor;
3. direct route-resolved robbery outcome;
4. analysis scale;
5. independence from any duplicate report.

Only after those fields are frozen may direction be coded as
`POSITIVE / NULL / OPPOSITE / MIXED`.

## Current overlap audit

The 24-study direct corpus is cross-walked against the 56-label historical
frame in:

- `DIRECT_ACCESS_GEOMETRY_LEAL2025_CROSSWALK_V1.csv`

Current overlap is 4/24 direct programs:

- Lara & Ornelas 2001;
- Castro, Silveira & Navarro 2009 (source label `Castroetal_2008`);
- Carrió & Güemes 2019;
- Rojas-Nossa, Sánchez & Navarro 2016.

This confirms that the historical fitness-cost frame alone is insufficient for the
geometry question and that Stage U is necessary.

## Formal analysis gate

Do not calculate a recurrence p-value from the 24-study direct corpus.

A formal directional recurrence analysis opens only after:

~~~text
HISTORICAL_DIRECT_ELIGIBLE_SET = RESOLVED
HISTORICAL_FRAME_SCREENED = COMPLETE
FORMAL_BIBLIOGRAPHIC_UPDATE_FRAME = COMPLETE
DUPLICATES_RESOLVED = COMPLETE
ELIGIBILITY_FROZEN_BEFORE_DIRECTION_CODING = COMPLETE
~~~

The unresolved row-level provenance still blocks a claim about the exact total
number of historical biological programs, but it no longer blocks the historical
direct-geometry eligible set. Formal recurrence therefore now hinges on one
remaining inferential gate: a finite, exportable, deduplicated bibliographic
update frame beyond the Leal anchor.

At that point, report at minimum:

- number of unique eligible study programs;
- counts of positive / null / opposite / mixed;
- study-scale and fauna composition;
- sensitivity excluding discovery-exposed records;
- sensitivity treating mixed studies conservatively;
- no pooled effect size unless a genuinely commensurate effect scale exists.

The primary Letter network statistic remains `k = 2` regardless of this
supporting literature synthesis.
