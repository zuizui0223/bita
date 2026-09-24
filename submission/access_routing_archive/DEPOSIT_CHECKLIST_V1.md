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

At this point the DOI is reserved but not yet registered. Registration occurs
when the Zenodo record is published.

## Phase 2 — freeze the DOI-bearing submission commit

Replace the archive placeholder with the reserved DOI in:

1. `submission/ECOLOGY_LETTERS_LETTER_TITLE_PAGE_V1.md`
2. `manuscript/MANUSCRIPT_ACCESS_ROUTING_LETTER_V0.md`
3. `submission/ECOLOGY_LETTERS_LETTER_COVER_V0.md`
4. `docs/PUBLICATION_STATUS.md`
5. issue #227

Then fill the author-controlled submission fields and commit the resulting
submission state. That exact commit is the source for the final archive build.

## Phase 3 — build the final deposit file

Run `.github/workflows/build-access-routing-letter-package.yml` from the exact
DOI-bearing submission commit.

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
- the archive-only reproduction matches the frozen Letter results;
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
