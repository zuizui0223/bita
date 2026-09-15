# Ecology Concepts & Synthesis fit audit

Checked against the official Ecology Author Guidelines revised **April 2026** and the current active BITA review artifact.

## Editorial fit

**PASS for the active mechanism-identification paper.**

Active title:

> **Trait interaction is not ecological mechanism: an identification framework for multifunctional traits**

The transferable contribution is the promotion ladder from **trait interaction** to **mechanism identification**:

```text
measure a focal trait interaction
-> separate nested outcome claims
-> represent compatible mechanism allocations as an identified set
-> add explicit restrictions / partial channel measurements
-> use selective consumer interventions
-> test four-way separability
-> independently assay any remaining joint channel
```

The detailed floral attraction/defence case is a worked system rather than the definition of the paper.

## April 2026 format/compliance fit

The current package is within the normal Concepts & Synthesis length route and is being tested against the journal-facing constraints:

```text
standard Main limit:       <=30 pages
current Main:               21 pages before this title-page patch
current Appendix:           10 pages
current Main figures:       5 embedded
title:                      <=120 characters (current = 101)
Abstract:                   <=350 words (current <350)
keywords:                   6-12, alphabetical (current = 8)
Main format:                Word DOCX
Appendix route:             separate PDF preferred
continuous line numbering: enabled
page:                       Letter, 1-inch margins
font/spacing:               12-pt Times New Roman, double spaced
```

If a future Main grows above 30 pages, the workflow currently fails closed rather than silently relying on the journal's 31–50 page exception. Deliberately using that exception would require the journal's detailed two-part length justification in the cover letter.

The generated title page contains journal/manuscript type, active title, author/affiliation placeholders, corresponding-author placeholder, Open Research Statement and alphabetized keywords before the Abstract section break.

## Active scientific package

Canonical science source:

```text
manuscript/MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md
```

Active builder/workflow:

```text
scripts/build_bita_mechanism_candidate_sources.py
.github/workflows/build-bita-mechanism-review-package.yml
```

Authoritative reader-facing artifact/receipt:

```text
bita-mechanism-identification-review-package
PACKAGE_QA_RECEIPT.txt
```

#210 independently reproduced a 21-page Main + 10-page Appendix package with five embedded Main figures. The receipt, not historical hard-coded page counts, remains the source of truth after every rebuild.

## Mechanism-identification fit

The active paper distinguishes the measurable total interaction

```text
Delta_AD W = W11 - W10 - W01 + W00
```

from its compatible ecological allocations

```text
Delta_AD W = rho_delta - iota_delta - kappa_delta.
```

The total interaction therefore defines an identified set rather than a unique mechanism. Stronger claims require explicit restrictions, selective antagonist and pollinator interventions, pollinator-independent baseline handling, the four-way separability diagnostic, and independent evidence for any remaining joint channel.

## Empirical synthesis fit

The source-adjudicated empirical spine contains:

```text
56 directional route records
25 independent biological clusters
17 high-information systems
```

All four constituent marginal route families recur, while no screened high-information system closes the full allocation design plus an independent remaining-channel assay. The empirical synthesis is therefore:

```text
RECURRENT_CONSTITUENT_BIOLOGY
+
FRAGMENTED_IDENTIFICATION
```

These counts are recurrence / identification-capacity diagnostics, not natural-prevalence estimates.

## Boundary with SCH and SLK

```text
SCH: identify whether multifunctionality has been promoted to functional conflict / L
SLK: transport identified conflict through value -> accessibility -> invasion -> fixation -> occupancy
BITA: once traits interact on fitness, identify the ecological mechanism allocation
```

Historical BITA architecture derivations remain provenance, not active Main-text novelty.

## Identification invariants preserved

- total interaction alone defines a set, not unique channel allocation;
- positive interaction relief is weaker than functional release and strict reversal;
- partial bounds are conditional on declared restrictions;
- point-identification requires selective `A x D x antagonist x pollinator` intervention structure;
- pollinator-independent reproduction is measured/corrected rather than assumed absent;
- the four-way interaction is a separability diagnostic, not nuisance variation;
- an unallocated residual is not called biological cost by subtraction;
- marginal route recurrence is not channel identification or prevalence;
- positive `A x D` interaction is not evidence of historical trait splitting.

## Open Research fit

The generated title page carries the review-stage Open Research Statement, which is also copied to the portal metadata template. The internal review artifact may bundle selected derived files for reproducibility and QA, but journal-facing data/code follow the ESA Open Research repository/archive route rather than being uploaded as ordinary Supporting Information data files.

A permanent DOI for the exact accepted data/code release remains an acceptance-stage task.

## AI disclosure boundary

Repository provenance documents AI-assisted coding, literature triage, reproducibility checking and drafting/editing, but that provenance is not the final journal disclosure. Under the April 2026 ESA guidance, if the final use is beyond routine spelling/grammar/general editing, author-approved disclosure must be synchronized across the relevant manuscript section, **Acknowledgments**, and the **submission form**. This remains an author-controlled pre-upload blocker.

## Remaining submission blockers

Scientific package rebuild, page counting and review-package visual artifacts are no longer blockers. Remaining work is:

1. confirm final author list/order, affiliations, corresponding author and ORCIDs;
2. approve CRediT, funding, Acknowledgments, competing interests and licence wording;
3. approve and place the final AI disclosure if required;
4. confirm any live-portal fields not represented in the manuscript;
5. perform one final exact rebuild and page-by-page QA after metadata insertion;
6. obtain all-author approval and perform authenticated portal upload.

## Fallbacks

1. The American Naturalist — strongest alternative for a more formal conceptual/inference presentation.
2. Methods in Ecology and Evolution — possible if the identification/design contribution is emphasized methodologically.
3. Another conceptual/methodological ecology venue if editorial scope feedback requires it.
