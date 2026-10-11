# Ecology Letters Letter — offline release-readiness audit (2026-10-11)

Status: **STAGING ARCHIVE INTEGRITY PASS; EXTERNAL SUBMISSION BLOCKED**
Review PR: [#360](https://github.com/zuizui0223/bita/pull/360)
The exact artifact inspected was produced by the PR-triggered
[full Letter package run 38104520450](https://github.com/zuizui0223/bita/actions/runs/38104520450)
(artifact `11689970940`).

## Verified staging artifact

- GitHub Actions full package workflow: **success**, including all internal
  archive-only reproduction checks, frozen-estimate comparisons, DOCX→PDF,
  manuscript figure generation and package inventory.
- Standardized input data archive schema: `BITA_ACCESS_ROUTING_LETTER_ARCHIVE_V5`.
- Frozen analysis table rows:
  - Sakhalkar: 57 plants
  - Aubert/EPHI pair-site: 2,265
  - Ecuador zero-inclusive opportunity: 19,909
- Nested `access-routing-letter-data-code-v1.zip` SHA-256:
  `c06a68dd9dd629b32ee3ec710e7099f81acbe139ec17e307ea9ed0ed9a082ff7`
- Independent check: the adjacent `.sha256` file **matches** this ZIP's bytes.
- `data_archive/FILE_SHA256SUMS.txt`: **69/69** listed files pass
  SHA-256; no unlisted inner archive files other than the checksum file
  itself; no mismatched or missing files.
- Stage artifact contains the refreshed scientific manuscript, cover,
  title page, figure SVGs, review DOCX, and a PDF render.

## The virtual-merge provenance distinction

- Source commit embedded inside the CI package:
  `e453fd7ed9641bc983a1ac3a34e91236d830cb66`
- Verified GitHub commit message:
  `Merge 38707dcdfc07420278c7325c47102c8df2856f8b into 98c0a41d3334078eff9cbf8a300d42bf57ae5355`
- Its parents are the `main` SHA and the reviewed PR branch SHA.

This is the **ephemeral GitHub pull_request merge ref** used for validation;
it is not the final DOI-bearing source commit. The stage archive must **not**
be uploaded as if it were the final exact-source Zenodo release artifact.

## Local fail-closed audit

`scripts/audit_letter_release_gate.py` and
`tests/test_audit_letter_release_gate.py` reproduce this distinction
in addition to checking inner/outer SHA integrity, frozen row counts,
a consistent reserved-DOI receipt and author-controlled fields.

Observed stage classification:

```text
INTEGRITY_VERIFIED_BUT_RELEASE_BLOCKED

integrity.all_checksums_match             true
inner files                               70 (69 checksummed + checksum list)
recorded archive source SHA              e453fd7ed964...
source SHA matches reviewed PR head       false (expected: PR virtual merge)
DOI reserved in current archive          false
author metadata complete                 false
DOI publication/resolution verified      false
submission_ready                         false
```

The current author metadata file is
`submission/ECOLOGY_LETTERS_LETTER_AUTHOR_METADATA_V1.json`,
whose `authors` array, `affiliations` mapping and declaration
fields are intentionally blank; do not infer author-controlled values.

## External steps (cannot be auto-completed without author approval)

1. **Author-controlled:** reserve a real Zenodo record DOI in a draft.
   Do not paste an access token into a chat; the previously attempted
   GitHub secret-based reservation stopped at missing `ZENODO_ACCESS_TOKEN`.
2. **Author-controlled:** fill and approve the final author list,
   affiliations, correspondence, authorship, conflicts, funding,
   acknowledgments, archive license, disclosure and originality fields.
3. Apply the actual reserved DOI using the now tested fail-closed
   `scripts/apply_reserved_archive_doi.py`.
4. Freeze the **exact DOI-bearing submission commit** and rebuild from
   that commit (not the pull-request merge ref). Independently verify
   source SHA, all checksums, manuscript/cover/title DOI consistency.
5. Upload that exact ZIP to the original reserved Zenodo draft,
   publish it, then **confirm publicly resolving DOI** before submitting.

All numeric results and the current `main` branch remain unchanged.
The archive inspected here is for review/staging only. The offline gate
**cannot verify Zenodo publication by itself** and must never output
`submission_ready=true` without independent external verification.
