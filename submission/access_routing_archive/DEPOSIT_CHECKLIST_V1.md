# Access-routing Letter DOI deposit checklist v2

This checklist uses Zenodo's DOI-reservation flow so that the DOI can be inserted
into the Letter **before** the exact submission-commit archive is built.

## Phase 1 — reserve the DOI

1. Create a new Zenodo upload draft.
2. Fill the minimum metadata needed to save the draft.
3. In the DOI field, choose that the upload does not already have a DOI and use
   **Get a DOI now!** to reserve one.
4. Copy the reserved DOI exactly.
5. Do **not** delete this draft; deleting it loses the reserved DOI.
6. The reserved DOI must be a **new BITA data/code deposit record**, not either of the original source dataset DOIs (`10.5281/zenodo.8398202` or `10.5281/zenodo.14185547`). The DOI applicator rejects accidentally reusing either source DOI. Never paste Zenodo access tokens or private draft-preview URLs in public repository files or chat.

At this point the DOI is reserved but not yet registered. Registration occurs
when the Zenodo record is published.

**Confidential-review alternative (not yet editorially authorized):**
Ecology Letters' data/code policy also permits private-for-peer-review
access, while Zenodo supports `Can preview draft` links. A DOI reserved
but not yet registered may require explicit confirmation from the
journal's editorial office. See
`PRIVATE_REVIEW_ACCESS_ROUTE_V1.md` before considering such a route.
Do not place a confidential draft-preview link in public GitHub files.
The normal publication-and-public-DOI gate below remains in force
unless the editor confirms an alternative.

## Phase 2 — freeze the DOI-bearing submission commit

Replace the archive placeholder with the reserved DOI in:

1. `submission/ECOLOGY_LETTERS_LETTER_TITLE_PAGE_V1.md`
2. `manuscript/MANUSCRIPT_ACCESS_ROUTING_LETTER_V0.md`
3. `submission/ECOLOGY_LETTERS_LETTER_COVER_V0.md`
4. `docs/PUBLICATION_STATUS.md`
5. issue #227

Use the fail-closed applicator on the real DOI, from a reviewed checkout:

```bash
# Set this locally to the genuine DOI from YOUR saved Zenodo draft.
# Do not commit credentials or a confidential preview URL.
test -n "$RESERVED_ZENODO_DOI"
python scripts/apply_reserved_archive_doi.py --doi "$RESERVED_ZENODO_DOI"
python scripts/apply_reserved_archive_doi.py --check-only
```

`RESERVED_ZENODO_DOI` must be set to the actual new record DOI before running. The applicator modifies submission files and writes a reservation receipt; it does **not** publish a Zenodo deposit.

Complete the **author-controlled** JSON schema in `submission/ECOLOGY_LETTERS_LETTER_AUTHOR_METADATA_V1.json`, have every author approve the actual submission version, and verify with:

```bash
python scripts/validate_ecology_letters_letter_author_metadata.py --require-complete
```

The archive release gate now uses this same full validator: a nonempty author string list is **not** enough; correctly structured author names, affiliation links, e-mails, exactly one corresponding author and declarations are required. Metadata values must be genuine JSON strings, not numbers or booleans coerced into text. Author metadata is **not automatically copied** into the title page or cover: replace their actual author-controlled placeholders consistently before release. The release auditor additionally checks that the approved JSON and packaged documents agree on **author order and names, affiliation/email strings, corresponding author and contact information, author contributions, funding, acknowledgments, conflicts, AI-assisted workflow declaration, cover-letter novelty disclosure and the corresponding-author signature**. Field-level mismatch names appear in the audit receipt; no private author values are echoed there. A successful JSON-only validator is not a complete submission readiness approval.

Personal mailing addresses, telephone numbers and email addresses committed to a public repository become public; obtain deliberate author approval before putting them in the branch or a published artifact.

Freeze the final reviewed DOI-bearing source commit **after** these author-controlled changes. That exact commit is the source for the final archive build.

## Phase 3 — build the final deposit file

Run `.github/workflows/build-access-routing-letter-package.yml` with **workflow_dispatch on the branch containing the exact reviewed DOI-bearing submission commit**. GitHub's ordinary `pull_request` trigger uses a synthetic virtual merge commit; a successful PR artifact therefore does **not** prove that `data_archive/REPOSITORY_COMMIT.txt` matches the reviewed branch HEAD.

Record the exact `GITHUB_SHA` that the workflow checked out. If it differs from the final approved DOI-bearing commit, the resulting ZIP remains staging-only, even if its internal checksums and science reproduction pass.

Use:

```text
access-routing-letter-data-code-v1.zip
```

Verify it against:

```text
access-routing-letter-data-code-v1.sha256
```

Also confirm:

- `data_archive/REPOSITORY_COMMIT.txt` equals the exact DOI-bearing submission
  commit;
- `data_archive/FILE_SHA256SUMS.txt` covers every archived file;
- the archive-only reproduction matches the frozen first-open Letter results;
- the routine archive-only reproduction matches the retained culmen-only route split, threshold boundary audit (585/999 upper-boundary bootstrap fits), and V5 effective-reach point estimates (including 1.8× legitimate RR 0.154 and robbery RR 0.816); the archived dedicated full-jackknife code reproduces the retained confidence intervals and descriptive ratio of separately fitted robbery/legitimate RRs 5.311 (different positive-margin support sets; not a common-risk-set substitution factor);
- the ZIP contains no source species identifiers or uncited third-party raw files.

## Phase 4 — upload to the reserved Zenodo draft

Upload the final ZIP to the **same draft that owns the reserved DOI**.

Complete the metadata using `ZENODO_METADATA_TEMPLATE.md`, including:

- final creator list and ORCIDs;
- a compatible license;
- source dataset identifiers:
  - 10.5281/zenodo.8398202
  - 10.5281/zenodo.14185547
- associated source papers:
  - 10.1002/ecs2.4696
  - 10.1002/oik.11552

Before publication, verify the uploaded ZIP SHA256 against the workflow receipt.

## Phase 5 — publish and verify

Publish the Zenodo record. The reserved DOI is then registered.

After publication:

1. open the DOI from a clean browser session;
2. confirm the record resolves and the intended files are accessible to
   editors/reviewers;
3. rerun the Letter package checks if any repository file changed after the
   DOI-bearing submission commit;
4. update issue #227 with the DOI, Zenodo record URL, final ZIP SHA256 and exact
   submission commit.

## Submission gate

Do not submit while any of these remain:

```text
ACCESS_ROUTING_ARCHIVE_DOI = NOT_PUBLISHED_OR_NOT_RESOLVING
FINAL_AUTHOR_LIST_AND_AFFILIATIONS = REQUIRED
AUTHORSHIP_STATEMENT = REQUIRED
CONFLICT_OF_INTEREST = REQUIRED
FUNDING_ACKNOWLEDGMENTS = REQUIRED
AUTHOR_RELATIVE_NOVELTY_STATEMENT = REQUIRED
```
