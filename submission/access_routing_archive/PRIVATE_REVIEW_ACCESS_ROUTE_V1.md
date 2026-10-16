# Optional Zenodo private-review route — source-backed submission decision

Status: **POTENTIAL ALTERNATIVE, NOT AUTHOR- OR EDITOR-APPROVED**
Date audited: 2026-10-11
PR branch: `paper/route-rate-riskset-qualification-v1`
Paper: *Higher nectar robbery prevalence under access mismatch need not reflect higher robbery rates*

## Why this is a separate branch of the release decision

The existing repository submission gate is intentionally stricter:
it requires the Zenodo DOI to be registered, published, and resolvable
before the final external submission. That remains the **safe default**.

However, the current Ecology Letters Wiley Author Guidelines, §19,
distinguish two deadlines:

> Data and code must be supplied and accessible to editors and reviewers
> at the time of submission, and permanently archived in an accessible
> repository before publication.

The same section says data/code DOI(s) are required at initial submission,
while recognizing a repository **private-for-peer-review** option.
These statements open a potential path to submit with **restricted,
reviewer-accessible material** instead of public data, but do **not**
explicitly resolve whether a **reserved but not yet registered** Zenodo DOI
is acceptable in the DOI field of the Ecology Letters submission system.

Authoritative sources:
- Ecology Letters Author Guidelines:
  https://onlinelibrary.wiley.com/page/journal/14610248/homepage/forauthors.html
  (§19 Data and Code Availability)
- Zenodo: reserve DOI before publication:
  https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/
- Zenodo: link sharing:
  https://help.zenodo.org/docs/share/link-sharing/

## Zenodo documented functions

- A draft can reserve a DOI via **Digital Object Identifier → No →
  Get a DOI now!**. The reserved DOI only becomes registered when the
  Zenodo record is published.
- Zenodo supports **Can preview draft** sharing links. This permission
  allows a link-holder to see *unpublished drafts* and related files.
- **Can edit** links are broader: they permit changes to the unpublished
  draft and must not be given to journal reviewers.
- Deleting the draft loses its reserved DOI.
- Draft preview links should be treated as **confidential access links**,
  not committed in a public GitHub issue, source repository, or manuscript
  that will be publicly deposited.

## Two paths, both requiring author approval

### A. Public Zenodo DOI before submission (safe existing gate)

1. The author reserves the genuine DOI in their Zenodo draft, reviews
   the author metadata and license, and supplies the DOI.
2. Apply the DOI to manuscript, title page, cover and repository status
   files using `scripts/apply_reserved_archive_doi.py`.
3. Build the exact ZIP from the DOI-bearing reviewed source commit;
   validate source SHA and SHA256.
4. Upload the exact ZIP to the same draft; author checks metadata, file
   inventory and license and explicitly **publishes**.
5. Verify published DOI resolution and data/code accessibility.
6. Final author signoff and journal submission.

### B. Non-public data during peer review (only after editorial confirmation)

1. Ask *Ecology Letters* editorial office explicitly whether they
   accept a Zenodo **reserved/unregistered DOI** at initial submission,
   provided reviewers can access a saved, fully uploaded draft through
   a **Can preview draft** link; confirm where the confidential link
   should be entered in the submission system.
2. If permitted, author reserves the DOI and uploads the **exact final
   ZIP** into the same draft, then checks that a visitor using the
   private preview link can see/download all required archive files.
3. Include the reserved DOI and **accurate** status wording in the
   manuscript; do not say the dataset is already publicly archived if
   the draft remains unpublished.
4. Supply the confidential access link **only in the journal's private
   data-review field/approved confidential channel**, never in GitHub
   source or public DOI metadata.
5. Keep all author approvals and the frozen package hash; publication
   of the archive and public DOI verification must occur before the
   journal's publication deadline.

Until the journal's acceptance of a reserved DOI and draft-preview
link is confirmed, **path B is not an authorized submission gate**.
The current `audit_letter_release_gate.py` will correctly remain
`submission_ready=false` since it cannot verify such an external
review-access arrangement.

## Exact editorial-office clarification to seek

> Would Ecology Letters accept, at initial submission, a Zenodo dataset
> whose DOI has been reserved but not yet registered because the record
> remains an unpublished draft, provided the editors and reviewers are
> supplied a confidential Zenodo “Can preview draft” link granting
> access to the complete data, metadata and code? If yes, which
> submission field should contain the private link, and at what stage
> must the DOI become registered and publicly resolving?

This is a source-grounded **question**, not an assertion of permission.

## Unchanged blockers

Neither path permits automatic filling of author-controlled personal
information, research-data license selection, authorship approval or
claims that editorial review has occurred. The paper is not submitted,
the Zenodo DOI has not been reserved in this project, and a confidential
review link has not been created.
