# Public-resource screen for the complete matched-flower search universe

## Purpose

The OpenAlex harvest is a **broad discovery universe**, not a final empirical
dataset. Its initial run produced 258 unique candidate works. The project must
not mistake a small pilot reading queue for the search universe, nor mistake
258 heterogeneous articles for 258 comparable biological observations.

This protocol screens every harvested candidate for **positive signs of publicly
retrievable evidence** before considering author data requests.

```text
Harvested candidate universe
→ automated public-resource discovery for every candidate
→ full-text/table screen of every positive resource lead
→ M0 / M1 / M2 / D1 evidence classification
→ only if public D1 = 0, consider a bounded author request
```

## Automated sources

The script `scripts/screen_public_matched_evidence.py` uses three bounded
sources of retrieval leads:

1. **OpenAlex harvest metadata**
   - OA status and OA URL already returned by the seed harvest.
2. **One public HTML landing page for OA candidates**
   - discovers links labelled as supplement/supporting information/data;
   - discovers known repository hosts and machine-readable file suffixes;
   - never downloads a PDF, supplement, or data file during this step.
3. **DataCite public DOI metadata**
   - retains only Dataset, Collection, or Software DOI records that explicitly
     name the article DOI in `relatedIdentifiers`;
   - a title match, citation match, or vague search result does not count.

## Interpretation rules

```text
positive link found
→ retrieval lead only
→ inspect the linked content and full text

no link found / landing page fails / API fails
→ not_discovered
→ never conclude no supplement, no repository, or no data

any automatic row
→ stays M0_candidate_needs_full_text
→ never becomes M1, M2, or D1 automatically
```

## What is screened manually after the run

Every candidate in `public_resource_positive_leads.csv` is screened without a
numeric cap. The order is the public-evidence priority score, which uses only:

```text
predeclared interaction/trait metadata signals
+ OA URL
+ public supplement/repository/data-file links
+ explicit DataCite related-dataset records
```

Citation count is never used to rank a candidate.

A candidate can advance only when a human verifies the fields in
`matched_flower_study_cards.csv`, including independent A_flower/B_flower
measures, both interaction channels and denominators, alignment, linkage, and a
recoverable table.

## Pedicularis rule

The *Pedicularis rex* study remains M2 while its individual rows are not public.
Do not request its data merely because it is currently nearest to D1. Consider a
request only after:

```text
1. every positive public-resource lead from the complete harvest is screened;
2. all accessible supplements/repositories that could contain a D1 panel are
   checked; and
3. public D1 = 0.
```

At that point, a data request is a documented contingency, not the default data
strategy.
