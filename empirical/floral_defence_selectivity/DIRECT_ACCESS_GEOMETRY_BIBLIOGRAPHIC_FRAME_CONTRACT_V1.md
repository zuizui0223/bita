# Direct access-geometry formal bibliographic update-frame contract v1

## Purpose

The 24-program direct access-geometry → nectar-robbery corpus is supporting
evidence, not a formal prevalence denominator. A formal recurrence analysis opens
only after a finite bibliographic update frame is frozen **before outcome-direction
screening**.

This contract defines that frame import. It does not query a database itself.

Implemented import tools:

- `scripts/normalize_direct_access_geometry_bibliographic_export.py` converts
  Scopus CSV, Web of Science TSV, Crossref JSON, OpenAlex JSON, or a compatible
  generic CSV into the frozen raw schema without relevance filtering;
- `scripts/prepare_direct_access_geometry_bibliographic_frame.py` requires exactly
  one Q1–Q8 export file from one source database, normalizes all eight, then runs
  deterministic deduplication and receipt generation;
- `DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_EXPORT_PACKET_V1.md` is the execution
  packet for the remaining external export step.

## Frozen date window

~~~text
FROM_DATE = 2000-01-01
THROUGH_DATE = 2026-09-24
~~~

Records outside this publication window must not enter the formal update frame.

## Frozen query IDs

Run each query independently in one bibliographic database/export system and retain
the complete raw result rows returned under the date window.

~~~text
Q1 = "nectar robbing" AND "corolla length"
Q2 = "nectar robbery" AND "corolla length"
Q3 = ("nectar robbing" OR "nectar robbery") AND ("tube length" OR "tube depth")
Q4 = ("nectar robbing" OR "nectar robbery") AND ("flower size" OR "flower width")
Q5 = ("nectar robbing" OR "nectar robbery" OR "floral larceny")
     AND ("floral morphology" OR "nectar accessibility" OR "trait mismatch")
Q6 = ("nectar robbing" OR "nectar robbery")
     AND ("tongue length" OR proboscis OR glossa OR "bill length")
Q7 = ("nectar robbing" OR "nectar robbery")
     AND ("morphological constraint" OR "morphological constraints"
          OR "short-tongued")
Q8 = ("nectar robbing" OR "nectar robbery")
     AND ("switch to robbing" OR "switching to robbing" OR "shortened corolla")
~~~

No query may be added or removed after direction screening begins.

## Required raw-export CSV schema

Each result row must have:

~~~text
source_db
query_id
record_id
doi
title
year
authors
publication
url
search_date
~~~

- `source_db`: e.g. OpenAlex, Crossref, Scopus, WebOfScience.
- `query_id`: one of Q1–Q8.
- `record_id`: database-native identifier; may differ across sources.
- `doi`: blank if absent.
- `title`: required in the normalized frame. If an OpenAlex result has both provider-native `title` and `display_name` null, retain the record outcome-blind using the deterministic label `[OpenAlex untitled work <record_id>]`; do not drop it or enrich it from another database.
- `year`: required four-digit publication year.
- `search_date`: date on which the export was generated.

The raw export must preserve **all results returned by each frozen query**. Do not
pre-remove records for irrelevance, direction, study design, species, or outcome.

## Deterministic deduplication

The frame builder:

1. normalizes DOI strings;
2. uses DOI as the primary deduplication key when present;
3. otherwise uses normalized title + publication year;
4. combines all source databases / query IDs for a duplicate record;
5. sorts the final frame by deterministic key;
6. writes a SHA256-bound receipt.

Deduplication is bibliographic only. It does not determine biological independence.
Study-program deduplication happens later during full-text eligibility screening.

## Completeness gate

A formal frame is complete only if:

- every Q1–Q8 has at least one exported row;
- every row falls within 2000–2026-09-24;
- no normalized title/year is missing; provider-native null OpenAlex titles are retained with the frozen deterministic placeholder rather than excluded;
- query IDs are valid;
- all raw exports used are SHA256-recorded in the receipt.

If a frozen query legitimately returns zero results, record a separate zero-result
query receipt rather than omitting the query. The current v1 importer requires at
least one row per query, so a zero-result query requires a pre-screen amendment.

## Outcome-blind boundary

At frame construction time do not code:

- positive / null / opposite / mixed direction;
- whether the result supports BITA;
- robbery effect magnitude;
- p-values or coefficients.

The frame records only bibliographic provenance. Full-text eligibility is screened
after the frame hash is frozen.

## Formal inference gate

~~~text
HISTORICAL_DIRECT_ELIGIBLE_SET = RESOLVED_AT_4
BOUNDED_SUPPORTING_CORPUS = 24_PROGRAMS
FORMAL_BIBLIOGRAPHIC_UPDATE_FRAME = REQUIRED
FORMAL_RECURRENCE_RESULT = CLOSED
PRIMARY_STANDARDIZED_NETWORK_K = 2
~~~
