# Formal direct access-geometry recurrence summary contract v1

## Purpose

This contract defines the final reporting gate after the frozen Q1–Q8
bibliographic frame and full-text screening are complete.

It converts a finite, outcome-blind search frame into a **descriptive recurrence
summary at the independent biological-program level**. It does not turn the
literature into additional network replicates and does not estimate natural
prevalence.

## Required gates

The summary may be generated only when all of the following pass:

~~~text
HISTORICAL_DIRECT_ELIGIBLE_SET = RESOLVED_AT_4
Q1_Q8_FRAME = FROZEN_OUTCOME_BLIND
KNOWN_24_PROGRAM_RECALL = COMPLETE_OR_PROVIDER_ABSENCE_ACCOUNTED
FULLTEXT_SCREEN = COMPLETE
PENDING_RECORDS = 0
BIOLOGICAL_PROGRAM_IDS = UNIQUE
DUPLICATE_TARGETS = VALID_ELIGIBLE_PROGRAMS
~~~

If the frozen Q1–Q8 search fails to recover a pre-existing direct program, the
summary still fails closed unless the miss is independently adjudicated as a
**selected-provider coverage absence** before any new-record direction coding.
Such a provider-absent known program is reported outside the formal denominator;
its already-known direction is not injected into the finite-frame counts.

A provider-absence exception requires the selected database, a documented
provider query returning zero target records, independent verification that the
publication exists, and zero unresolved known-corpus misses. This keeps the
recall audit informative without making a finite provider-defined frame
impossible merely because the provider does not index an otherwise verified
paper.

## Unit of evidence

The formal unit is one **independent biological study program**.

Multiple bibliographic reports of the same program are represented once.
Rows classified as `DUPLICATE_BIOLOGICAL_PROGRAM` do not increase the
denominator.

## Direction coding

Every eligible program must be exactly one of:

~~~text
POSITIVE
NULL
OPPOSITE
MIXED
~~~

The final summary reports these four counts directly.

No program is converted into a pseudo-continuous effect solely to enable pooling.

## Historical anchor

The Leal 2025 historical source-label audit contributes a resolved eligibility
check:

~~~text
historical direct-geometry eligible programs = 4
directions = 2 POSITIVE / 1 NULL / 1 MIXED
~~~

These four programs already occur in the bounded direct corpus and must be
recovered within the frozen bibliographic frame. They are **not added a second
time** to the formal denominator.

## Allowed formal output

Once all gates pass, report:

- total unique eligible direct programs in the frozen Q1–Q8 frame;
- positive / null / opposite / mixed counts;
- number of pre-existing direct programs recovered inside the selected provider frame;
- number and IDs of pre-existing direct programs independently verified as absent from the selected provider, reported outside the denominator;
- number of newly eligible programs found by the formal frame;
- duplicate and ineligible record counts;
- frozen-frame record count and source database.

Allowed wording:

> Within the frozen Q1–Q8 bibliographic frame, N independent study programs
> directly tested the access-geometry → nectar-robbery relation; directions were
> P positive, Z null, O opposite and M mixed.

## Prohibited inference

Version 1 intentionally does **not** calculate:

- a binomial/sign-test p-value;
- a pooled effect size;
- natural prevalence of the mechanism;
- a universal probability that access constraints cause robbery;
- any change from the primary standardized network statistic `k = 2`.

A later inferential statistic would require a separately frozen model before
inspection of newly adjudicated directions. The current formal output is the
finite-frame directional evidence distribution.

## Claim hierarchy

~~~text
STANDARDIZED_NETWORK_RESULT = k_2
FORMAL_LITERATURE_RESULT = FINITE_FRAME_PROGRAM_LEVEL_DIRECTION_COUNTS
NATURAL_PREVALENCE = NOT_ESTIMATED
POOLED_EFFECT = NOT_ESTIMATED
FORMAL_DIRECTION_P_VALUE = NOT_COMPUTED
~~~
