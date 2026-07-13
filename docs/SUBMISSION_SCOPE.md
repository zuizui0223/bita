# Submission scope

This repository is the computational supplement for the current local-theory manuscript, with a preliminary literature-context layer.

## Active submission layers

1. **Primary claim:** local theory for one declared floral attraction trait and one declared flower-specific barrier/defence trait on one declared outcome scale.
2. **Finite-set sensitivity analysis:** the implemented baseline corollary is evaluated across declared phenotype/regime points, biological parameter scenarios, and endpoint-normalized response-shape variants.
3. **Auxiliary moderator:** reproductive assurance `R` is retained only as a background moderator of the pollination-mediated channel in the implemented corollary. It is not a third focal trait and must not be promoted to the manuscript's core claim.
4. **Preliminary literature context:** abstract-level route records are used only to show that a collateral pollinator-cost pathway is biologically plausible in some systems. They are not a second independent submission claim, a full-text systematic review, or a parameter-calibrating meta-analysis.
5. Reproducible figures, readouts, tests, provenance records, and inference-boundary checks required for the primary theory claim and its preliminary context.

## Excluded from the submission

The following are not part of the active supplement:

- the former *Impatiens capensis* linked case study and re-expressed four-arrow effect anchors;
- optimum-search, strategy-classification, and covariance-among-optima analyses;
- matched-flower study-card discovery or D1/D2/D3 evidence architecture;
- global network-backbone, TRY-request, and trait-coverage audit machinery;
- observational or randomized models fitted to third-party raw observations;
- candidate scouting, repository probes, and source-access workflows;
- superseded Part B moderator, leverage-priority, and future-data-collection pipelines;
- superseded manuscript drafts, planning notes, and historical cleanup records.

Git history remains the archive for these exploratory branches. They must not be restored unless a future manuscript explicitly depends on them.

## Inclusion rule

A file belongs in the active repository only when it does at least one of the following:

- defines or tests the current focal-pair local theory;
- generates or validates a current sensitivity result, table, or figure;
- supports or validates the retained preliminary route-level literature context;
- documents data provenance, reproduction steps, assumptions, or inferential boundaries;
- prevents retired exploratory material from re-entering the submission tree.

Historical interest, future usefulness, or a green unit test is not sufficient reason to retain a file.

## Inference rule

The repository must not blur the following levels:

```text
abstract-level route context
!= system-specific channel curvature
!= complete A x D mixed partial
!= environmental derivative of the mixed partial
!= trait covariance or evolutionary endpoint
```

The implemented auxiliary moderator `R` may change the local mixed partial through the pollination-mediated channel, but this does not change the identity of the focal theory: the submission claim remains the local interaction between the declared `A` and `D` pair.

Every active document and output must preserve these boundaries.
