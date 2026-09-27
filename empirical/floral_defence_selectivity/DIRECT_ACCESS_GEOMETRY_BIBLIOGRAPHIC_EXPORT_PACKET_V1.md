# Direct access-geometry Q1-Q8 bibliographic export packet v1

## Current gate

~~~text
HISTORICAL_DIRECT_ELIGIBLE_SET = RESOLVED_AT_4
BOUNDED_SUPPORTING_CORPUS = 24_PROGRAMS
Q1_Q8_QUERY_CONTRACT = FROZEN
BIBLIOGRAPHIC_FRAME_BUILDER = IMPLEMENTED
PROVIDER_EXPORT_NORMALIZER = IMPLEMENTED
ONE_COMMAND_INTAKE = IMPLEMENTED
POST_FREEZE_SCREEN_BOOTSTRAP = IMPLEMENTED
KNOWN_DIRECT_PROGRAM_MATCH = DOI_THEN_TITLE_YEAR_ALIAS
FULLTEXT_DECISION_TEMPLATE = IMPLEMENTED_KNOWN_PREFILL_UNKNOWN_PENDING
FULLTEXT_DECISION_GATE = IMPLEMENTED_FAIL_CLOSED
FORMAL_RECURRENCE_SUMMARY_GATE = IMPLEMENTED_DESCRIPTIVE_NO_PVALUE
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
- a record lacks year or record ID; non-OpenAlex missing titles still fail, while OpenAlex null titles are retained with the frozen deterministic provider-ID placeholder;
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


## Single-ZIP intake

The entire external handoff can be one ZIP file containing exactly:

~~~text
Q1.csv
Q2.csv
Q3.csv
Q4.csv
Q5.csv
Q6.csv
Q7.csv
Q8.csv
QUERY_COUNTS.csv
~~~

Each query file may instead use `.tsv`, `.txt`, or `.json` when appropriate
for the chosen database/export format. Keep all files at the ZIP root; nested
directories are rejected.

Run:

~~~bash
python scripts/ingest_direct_access_geometry_bibliographic_export_zip.py \
  --zip PATH_TO_Q1_Q8_EXPORT_PACKET.zip \
  --output-dir empirical/floral_defence_selectivity/formal_bibliographic_frame_v1 \
  --search-date YYYY-MM-DD
~~~

The ZIP intake rejects:

- path traversal;
- nested paths;
- symlinks;
- extra/missing files;
- unsupported query file formats;
- oversized files/archive payloads;
- extreme compression ratios;
- missing or inconsistent query-count manifests.

After safe extraction it runs the same count verification, provider normalization,
Q1–Q8 completeness checks, deterministic deduplication and SHA-bound frame receipt.
It then automatically runs the post-freeze known-program bootstrap, writes the
pending full-text screening ledger, and records known-corpus recall without coding
direction for any new record.

This is now the preferred external handoff because it reduces the remaining input
to one file **and the remaining repository command to one invocation**.


## Post-freeze screening bootstrap

**The preferred single-ZIP intake runs this step automatically.** The standalone
command below is retained for directory-based intake, repair, or explicit reruns
against an already frozen frame.

After the frame intake has created:

~~~text
DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_FRAME_V1.csv
DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_FRAME_RECEIPT_V1.json
~~~

run:

~~~bash
python scripts/bootstrap_direct_access_geometry_bibliographic_screen.py \
  --frame empirical/floral_defence_selectivity/formal_bibliographic_frame_v1/DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_FRAME_V1.csv \
  --frame-receipt empirical/floral_defence_selectivity/formal_bibliographic_frame_v1/DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_FRAME_RECEIPT_V1.json \
  --output empirical/floral_defence_selectivity/formal_bibliographic_frame_v1/DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_SCREEN_V1.csv \
  --receipt empirical/floral_defence_selectivity/formal_bibliographic_frame_v1/DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_SCREEN_BOOTSTRAP_RECEIPT_V1.json
~~~

This step runs **only after** the outcome-blind frame is frozen. It:

1. matches DOI-bearing records to the current 24-program direct corpus;
2. matches the two DOI-less known programs by frozen normalized title + year;
3. copies direction only for records already known before the formal frame;
4. leaves every new bibliographic record as
   `PENDING_FULLTEXT_ELIGIBILITY` with a blank direction;
5. reports any of the 24 known direct programs that the frozen Q1–Q8 frame failed
   to recover;
6. keeps `formal_recurrence_result_open = false`.

Title aliases for the two DOI-less direct programs are frozen in:

- `DIRECT_ACCESS_GEOMETRY_KNOWN_TITLE_ALIASES_V1.csv`.

Generated post-freeze files:

~~~text
DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_SCREEN_V1.csv
DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_SCREEN_BOOTSTRAP_RECEIPT_V1.json
~~~

This removes known-study rediscovery work while preserving the outcome-blind
boundary for all new records.


## Direction-blind title/abstract triage

After the frame is frozen and known-corpus/provider-coverage accounting is fixed,
new OpenAlex records may undergo one conservative title/abstract triage before
full-text retrieval.

The automated rule is frozen as:

~~~text
abstract missing                         -> RETAIN FOR FULL TEXT
any robbery / larceny / illegitimate
route signal in title or abstract       -> RETAIN FOR FULL TEXT
available title + abstract with no
robbery/bypass-route signal             -> INELIGIBLE_TITLE_ABSTRACT_NO_ROUTE_OUTCOME
~~~

This stage may inspect whether a route-resolved robbery outcome is plausibly present,
because that is part of the predeclared eligibility contract. It must not inspect or
code whether the geometry–robbery association is positive, null, opposite, or mixed.

When a deduplicated frame record maps to multiple OpenAlex Work IDs, all provider
records are checked. A record is auto-excluded only if every mapped Work has an
abstract and the combined title/abstract text contains no frozen route signal.
Any missing abstract forces retention for full text.

The script is:

~~~bash
python scripts/screen_direct_access_geometry_openalex_title_abstract.py \
  --frame .../DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_FRAME_V1.csv \
  --decisions .../DIRECT_ACCESS_GEOMETRY_FULLTEXT_DECISIONS_V1.csv \
  --output .../DIRECT_ACCESS_GEOMETRY_ELIGIBILITY_DECISIONS_V2.csv \
  --receipt .../DIRECT_ACCESS_GEOMETRY_TITLE_ABSTRACT_SCREEN_RECEIPT_V1.json
~~~

## Full-text eligibility decision gate

The single-ZIP intake also creates:

~~~text
DIRECT_ACCESS_GEOMETRY_FULLTEXT_DECISIONS_V1.csv
~~~

Known direct-corpus matches are prefilled and must remain unchanged. Every new
bibliographic record starts as:

~~~text
decision_status = PENDING_FULLTEXT
direction = <blank>
~~~

After full-text adjudication, use one of:

~~~text
ELIGIBLE_DIRECT
DUPLICATE_BIOLOGICAL_PROGRAM
INELIGIBLE_<REASON>
~~~

For `ELIGIBLE_DIRECT`, provide a unique biological-program ID, one of
`POSITIVE / NULL / OPPOSITE / MIXED`, a decision basis, and a source identifier.
For duplicates, provide the target biological-program ID. Ineligible rows must not
carry a direction.

Validate while screening:

~~~bash
python scripts/validate_direct_access_geometry_fulltext_decisions.py \
  --screen empirical/floral_defence_selectivity/formal_bibliographic_frame_v1/DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_SCREEN_V1.csv \
  --decisions empirical/floral_defence_selectivity/formal_bibliographic_frame_v1/DIRECT_ACCESS_GEOMETRY_FULLTEXT_DECISIONS_V1.csv
~~~

Open the completion gate only after every pending record is adjudicated:

~~~bash
python scripts/validate_direct_access_geometry_fulltext_decisions.py \
  --screen empirical/floral_defence_selectivity/formal_bibliographic_frame_v1/DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_SCREEN_V1.csv \
  --decisions empirical/floral_defence_selectivity/formal_bibliographic_frame_v1/DIRECT_ACCESS_GEOMETRY_FULLTEXT_DECISIONS_V1.csv \
  --require-complete \
  --output empirical/floral_defence_selectivity/formal_bibliographic_frame_v1/DIRECT_ACCESS_GEOMETRY_FULLTEXT_DECISION_RECEIPT_V1.json
~~~

Even a complete full-text screen keeps
`formal_recurrence_result_open = false`; it only advances the next gate to
`FORMAL_RECURRENCE_SUMMARY`.


## Formal finite-frame recurrence summary

After `--require-complete` passes for the full-text decision file, run:

~~~bash
python scripts/summarize_direct_access_geometry_formal_recurrence.py \
  --screen empirical/floral_defence_selectivity/formal_bibliographic_frame_v1/DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_SCREEN_V1.csv \
  --decisions empirical/floral_defence_selectivity/formal_bibliographic_frame_v1/DIRECT_ACCESS_GEOMETRY_FULLTEXT_DECISIONS_V1.csv \
  --bootstrap-receipt empirical/floral_defence_selectivity/formal_bibliographic_frame_v1/DIRECT_ACCESS_GEOMETRY_BIBLIOGRAPHIC_SCREEN_BOOTSTRAP_RECEIPT_V1.json \
  --output empirical/floral_defence_selectivity/formal_bibliographic_frame_v1/DIRECT_ACCESS_GEOMETRY_FORMAL_RECURRENCE_SUMMARY_V1.json
~~~

This final gate requires:

- complete recall of all 24 pre-existing direct programs by the frozen Q1–Q8 frame;
- a complete full-text decision for every frame record;
- unique biological-program IDs;
- valid duplicate targets;
- the resolved four-program historical direct-eligible anchor;
- one source database for the entire Q1–Q8 frame.

Its formal output is **descriptive program-level direction counts**:

~~~text
eligible programs
positive
null
opposite
mixed
new eligible programs found by the formal frame
duplicate records
ineligible records
~~~

Version 1 deliberately does **not** calculate a direction p-value, pooled effect,
natural prevalence, or any replacement for the standardized network statistic
`k = 2`.

Contract:

- `DIRECT_ACCESS_GEOMETRY_FORMAL_RECURRENCE_SUMMARY_CONTRACT_V1.md`.
