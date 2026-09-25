# Direct access-geometry Q1-Q8 bibliographic export packet v1

## Current gate

~~~text
HISTORICAL_DIRECT_ELIGIBLE_SET = RESOLVED_AT_4
BOUNDED_SUPPORTING_CORPUS = 24_PROGRAMS
Q1_Q8_QUERY_CONTRACT = FROZEN
BIBLIOGRAPHIC_FRAME_BUILDER = IMPLEMENTED
PROVIDER_EXPORT_NORMALIZER = IMPLEMENTED
ONE_COMMAND_INTAKE = IMPLEMENTED
FORMAL_UPDATE_FRAME = AWAITING_COMPLETE_Q1_Q8_EXPORT
FORMAL_RECURRENCE_RESULT = CLOSED
~~~

## What must be exported

Use **one bibliographic database/export system for all eight queries**.

The frozen publication window is:

~~~text
2000-01-01 through 2026-09-24
~~~

Run exactly Q1–Q8 from
`DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_FRAME_CONTRACT_V1.md`.

Do not exclude records by:

- relevance;
- taxon;
- study design;
- positive/null/opposite direction;
- whether the paper appears to support the access-routing hypothesis.

Export every result returned by each query under the frozen date window.

## File naming

Save the eight complete exports in one directory as:

~~~text
Q1.csv
Q2.csv
...
Q8.csv
~~~

For Web of Science tab-separated output, `.tsv` or `.txt` is also accepted.
For Crossref or OpenAlex JSON export, `.json` is accepted.

There must be exactly one supported file for every Q1–Q8.

Also record the database's displayed/exported **total result count** for each query
in:

`DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_QUERY_COUNT_TEMPLATE_V1.csv`

Fill all eight rows with:

~~~text
query_id
source_db
reported_total_rows
search_date
~~~

The intake requires the exported row count to equal the recorded database total for
every query. A truncated export therefore fails closed instead of silently becoming
the formal frame.

## Supported provider formats

The repository normalizer accepts:

- Scopus CSV;
- Web of Science TSV / tab-delimited TXT;
- Crossref JSON with `message.items`;
- OpenAlex JSON with `results`;
- generic CSV when it contains recognizable bibliographic field names.

Provider-native columns are preserved only as bibliographic input. The normalizer
maps them to:

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

It does not inspect abstracts, outcomes, coefficients, p-values or direction.

## One-command intake

After placing Q1–Q8 in one directory:

~~~bash
python scripts/prepare_direct_access_geometry_bibliographic_frame.py \
  --input-dir PATH_TO_Q1_Q8_EXPORTS \
  --output-dir empirical/floral_defence_selectivity/formal_bibliographic_frame_v1 \
  --search-date YYYY-MM-DD \
  --count-manifest PATH_TO_FILLED_QUERY_COUNT_CSV
~~~

If provider detection is ambiguous, add one explicit source:

~~~bash
--source-db Scopus
~~~

The intake will:

1. require exactly one file for every Q1–Q8;
2. require a Q1–Q8 count manifest from the same database/search date;
3. verify every export row count against the database-reported query total;
4. normalize all records without relevance filtering;
5. require title, year and database-native record ID;
6. reject records outside the frozen year window;
7. require all eight query IDs;
8. deduplicate by DOI, then normalized title + year;
9. write the frozen bibliographic frame;
10. write SHA256-bound receipts;
11. keep `formal_recurrence_result_open = false`.

## Generated files

~~~text
normalized_raw/Q1.csv ... Q8.csv
DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_FRAME_V1.csv
DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_FRAME_RECEIPT_V1.json
DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_INTAKE_RECEIPT_V1.json
~~~

## Fail-closed cases

The intake stops if:

- any Q1–Q8 file is missing;
- the Q1–Q8 count manifest is incomplete or malformed;
- an export file row count differs from the database-reported query total;
- more than one file is supplied for one query;
- source databases are mixed;
- a record lacks title, year or record ID;
- a publication year lies outside the frozen window;
- a provider export contains duplicate native record IDs within one query;
- a query yields zero rows under the current v1 contract.

A genuine zero-result query requires a protocol amendment before screening; it must
not be silently omitted.

## Environment note

The current execution environment cannot directly retrieve complete Crossref or
OpenAlex API result sets: direct API access is unavailable from the available web
and container network paths. This is an execution limitation, not evidence that a
query returns zero results.

Therefore the remaining external input is one complete Q1–Q8 export set from one
bibliographic system. Once those files exist, all subsequent normalization,
deduplication, hashing and frame freezing are repository-automated.
