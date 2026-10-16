# BITA Ecology Letters Letter — staging verification and release gate (2026-10-13)

**Status: STAGING REPRODUCTION VERIFIED; AUTHOR/DOI RELEASE BLOCKED.**

This is a timestamped readout of GitHub Actions and its own release-gate receipt, not an independent external publication audit. No manuscript statistics, source data, or author-controlled values are changed by this document.

## Exact reviewed build

- Review: [PR #360](https://github.com/zuizui0223/bita/pull/360) (still **draft**, base `main`).
- PR head tested: `a64126bcf552d9bf14c5ee2fa799a631a1dba3cb`.
- Source checked out in the PR build: `1aef68fef7f1e7024239b803c7d2c3af10598c6c`, the ephemeral two-parent GitHub virtual merge of `main` `98c0a41d...` and PR head `a64126bc...`. It is **not** the exact DOI-bearing final source commit.
- [Full Letter package run 38405508198](https://github.com/zuizui0223/bita/actions/runs/38405508198) — **success**, artifact ID `11820125855`, artifact name `access-routing-letter-package`.
- [Python CI run 38405508262](https://github.com/zuizui0223/bita/actions/runs/38405508262) — **success**.
- [Sakhalkar Zenodo archive audit 38405508034](https://github.com/zuizui0223/bita/actions/runs/38405508034) — **success**.
- [Sakhalkar network re-analysis 38405508031](https://github.com/zuizui0223/bita/actions/runs/38405508031) — **success**.
- [Submission scope guard 38405507904](https://github.com/zuizui0223/bita/actions/runs/38405507904) and [legacy-package guard 38405507881](https://github.com/zuizui0223/bita/actions/runs/38405507881) — **success**.

## What the build demonstrably completed

The full package job recorded successful steps for all of the following:

1. Manuscript/figure/submission regression tests; archive DOI absent-state check.
2. Figures 1–3; export of the exact analysis-ready V5 archive source tables from public inputs.
3. **Archive-only** recomputation of headline analyses, with comparison to frozen/retained results and effective-reach point estimates.
4. Source and archive package assembly, ZIP and SHA256 checksum generation, Word source creation, PDF rendering/text validation and inventory verification.
5. Fail-closed staging release audit and upload of the staging artifact.

The CI release audit printed:

```text
analysis                                  BITA_LETTER_OFFLINE_RELEASE_GATE_V1
stage                                     INTEGRITY_VERIFIED_BUT_RELEASE_BLOCKED
integrity.all_checksums_match            true
integrity.inner.verified                 69
integrity.inner.listed                   69
integrity.errors                         []
submission_ready                         false
DOI_NOT_RESERVED                         true
AUTHOR_METADATA_INCOMPLETE               true
SOURCE_COMMIT_NOT_REVIEWED_HEAD          true
DOI_PUBLICATION_NOT_VERIFIED             true
```

This is positive evidence that **this staging build** reproduces its frozen source-backed outputs and passes its own integrity checks. It is not evidence that a Zenodo deposit or journal submission exists.

## Why the retry repair is confirmed

The earlier [failed run 38404861148](https://github.com/zuizui0223/bita/actions/runs/38404861148) stopped during Sakhalkar public ZIP retrieval with `http.client.RemoteDisconnected`. The download helper had bounded retries for HTTP 5xx and `URLError` but did not catch that directly raised connection exception. The subsequent PR head includes a fix for retryable transport errors and two deterministic success/exhaustion tests. The Sakhalkar audit, re-analysis, full package and multi-Python CI then succeeded. Do **not** equate transient download success with permanent provider availability.

## Current science claim ceiling

The manuscript's conditional prevalence association (P1, 259 Ecuadorian plant species) and its post-open opportunity-based rate contrasts (P2, bird × waypoint grain) are **different estimands**, not an algebraic decomposition. For the 1.8× hummingbird M1 audit, the 19,903 constructed opportunities yield distinct fitted supports: legitimate 15,377; robbery 3,371; intersection 2,900. Therefore the ratio of separately fitted rate ratios 5.31 is **descriptive**, not a joint common-risk-set substitution or individual tactic-switching estimate.

Scientific results remain frozen: P1 `rho=0.503`; separate 1.8× P2 legitimate `RR=0.154 (0.087–0.271)` and robbery `RR=0.816 (0.358–1.860)`, robbery effect direction unresolved; independent insect `rho=0.347`; equal-network `rho_J=0.428`, `k=2`. The P2 effective-reach change was explicitly **post-open**.

See `docs/LETTER_ESTIMAND_SELF_AUDIT_2026_10_13.md` and `docs/ACCESS_ROUTING_NOVELTY_BOUNDARY_V1.md` for claim controls.

## External fail-closed blockers

The audit showed these author-controlled metadata gaps: final authors, affiliations, mailing address, telephone, e-mail, authorship, funding, acknowledgments, competing interests, AI-assisted workflow disclosure, author-relative novelty, archive license, final all-author approval and originality/no-concurrent-submission declaration.

No genuine Zenodo DOI is reserved in the checked package. An exact-source DOI-bearing archive must be built **after** the author-approved DOI and declarations are inserted; its embedded commit and complete checksums must be checked against that final source. The resulting ZIP must be deposited into the correct Zenodo record, published, and its public DOI independently resolved. The confidential-review alternative described in `submission/access_routing_archive/PRIVATE_REVIEW_ACCESS_ROUTE_V1.md` requires explicit editorial approval and is not an implicit bypass.

**Do not merge, submit, publish an archive, or claim `submission_ready=true` merely because this CI staging receipt passes.**

## Practical next gate

With code/CI completed, the next action requiring external authorization is an **author-approved DOI reservation and completion of `submission/ECOLOGY_LETTERS_LETTER_AUTHOR_METADATA_V1.json`**. Preserve PR #360 in draft until those gates are met or the author explicitly approves a different publication plan.
