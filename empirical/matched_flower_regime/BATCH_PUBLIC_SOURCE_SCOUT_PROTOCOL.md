# Batch public-source scout protocol

## Purpose

The broad OpenAlex harvest is a discovery universe, not a biological dataset.
Most papers will not expose ideal matched A/B/P/H data. The immediate empirical
strategy is therefore:

```text
broad shallow public-source retrieval
→ rank reachable source routes
→ manually screen only reachable/high-signal leads
→ register whatever can be proved, without forcing D1/D2/D3
```

This protocol prevents two opposite mistakes:

1. treating 258 heterogeneous papers as if they were 258 comparable observations;
2. getting stuck on a small number of attractive but inaccessible papers.

## What the batch scout records

For every harvested candidate with a DOI, the scout records DOI-exact public
source routes from:

```text
Crossref exact article metadata and publisher links
OpenAlex open-access full-text locations
Dryad / DataCite / Zenodo repository-resolution receipts
```

The output files are:

```text
batch_public_source_summary.csv
batch_public_source_positive_leads.csv
batch_public_source_receipts.csv
batch_public_source_failures.csv
batch_public_source_report.json
```

## What counts as a positive lead

A positive lead means only that a public route may be worth inspecting. Examples:

```text
public PDF candidate
publisher content/text-mining link
repository landing candidate
repository file manifest
```

A positive lead is **not** evidence of a usable trait-path estimate.

## What is never inferred automatically

```text
A_flower or B_flower trait function
pollination or antagonist denominator
site/time alignment
individual/population linkage
reported coefficient and uncertainty
M1 / M2 / D1 / D2 / D3 status
author-contact priority
```

Every automatic row remains:

```text
M0_public_source_lead_only
```

## Manual follow-up order

Manual screening follows the batch `source_priority_score`, but any source can
advance only after actual source inspection verifies methods, tables, trait
function, denominators, linkage, and uncertainty.

## Author-contact rule

No author request is made from this batch scout. Author contact remains a later
contingency only after public-source screening and accessible source inspection
show that public D1 is zero.
