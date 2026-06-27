# Megachile host-evidence protocol

## Purpose

This protocol creates the candidate plant universe for the first formal Megachile analysis. It separates evidence that a bee **cuts leaves or petals for nesting** from evidence of floral visitation, nesting near a plant, or geographic co-occurrence.

The first formal plant universe is not "all plants that overlap a bee". It is a taxonomically reconciled, evidence-graded list of plants with documented nesting-material use by Japanese *Megachile* species.

## Unit of evidence

One row is one bee--plant observation or one explicitly stated bee--plant interaction in one source. A source that lists ten plants contributes ten rows. Do not pool sources into one untraceable host list.

## Allowed interaction types

```text
leaf_cutting_direct
petal_cutting_direct
nest_lining_direct
resin_collection_direct
nest_material_unspecified
floral_visit_only
nest_near_plant_only
co_occurrence_only
unknown
```

Only the first four types are direct material-use evidence. `nest_material_unspecified` can be retained for review but is excluded from the primary leaf-cutting universe unless the original source can be checked.

## Evidence grades

```text
A  Direct observation, photograph, experimental nest inspection, or specimen-associated nest material with bee and plant identified to species.
B  Direct material-use evidence, but either bee or plant only resolved to genus / species group.
C  Secondary literature or curated catalogue explicitly citing a primary source; primary source not yet checked.
D  General natural-history statement, garden observation, or source without a checkable observation.
E  Floral visit, co-occurrence, or other non-material association.
```

Primary analysis:

\[
\mathcal P_{\rm primary}=\{\text{records with interaction type in direct material use and grade A or B}\}.
\]

Sensitivity analysis may add grade C after source audit. Grades D and E are never treated as primary host evidence.

## Geographic rule

The first Japanese analysis accepts records from Japan only. Records from outside Japan may be kept in the table as biological context, but their `include_in_primary_host_universe` value must be `FALSE`.

## Taxonomy rule

Keep both names:

- `*_name_reported`: exactly as printed by the source;
- `*_name_accepted`: current reconciled name;
- `taxon_reconciliation_status`: `accepted`, `synonym_resolved`, `genus_only`, `unresolved`, or `not_checked`.

A row with unresolved plant taxonomy cannot enter a species-level trait analysis. It can remain in the evidence ledger.

## Source hierarchy

Prioritise acquisition in this order:

1. peer-reviewed nest biology or behaviour studies;
2. Japanese taxonomic, faunal, or natural-history monographs with observation detail;
3. museum / institutional specimen and nesting records with stable identifiers;
4. curated interaction databases that expose the original citation;
5. photographs only when the material-use event and both taxa are verifiable;
6. informal web observations only as leads, never as final evidence without review.

## Minimum metadata

A record is not analysis-ready unless it has:

```text
bee name reported
plant name reported
interaction type
source type and stable source ID
source locator (page, figure, specimen record, or URL fragment)
evidence grade
country or explicit Japan status
taxon reconciliation status
```

Coordinates, date, and locality are optional but should be retained whenever available.

## Output tables

### 1. Evidence ledger

All candidate records, including rejected and uncertain ones.

### 2. Primary host universe

One row per accepted plant taxon, with:

```text
plant_name_accepted
number_of_direct_records
number_of_bee_species
supporting_source_count
evidence_grade_best
Japan_record_count
trait_coverage_status
```

### 3. Bee--plant material-use matrix

A sparse matrix with explicit evidence weights, not raw counts alone. The weight rule is declared before analysis and must distinguish direct species-level evidence from genus-level evidence.

## Claims allowed after this protocol

The resulting universe identifies plants with documented nesting-material use by the included bee set. It does not estimate preference, availability, or defence effectiveness.

Those require, respectively:

- a background availability model;
- local occurrence / abundance and phenology data;
- a trait-to-cutting-cost or damage experiment, or an appropriate observational design.
