# Access-routing Letter DOI deposit checklist v1

This checklist starts from the green CI artifact produced by
`.github/workflows/build-access-routing-letter-package.yml`.

## Artifact to deposit

Use the single deposit-ready file:

```text
access-routing-letter-data-code-v1.zip
```

Verify it against:

```text
access-routing-letter-data-code-v1.sha256
```

The ZIP contains the exact analysis-ready tables, metadata, archive-only
reproduction output, source/frozen-result receipts and code required to reproduce
the Letter statistics.

## Before upload

1. Download the latest `access-routing-letter-package` artifact generated from
   the exact submission commit.
2. Verify the ZIP SHA256 against
   `access-routing-letter-data-code-v1.sha256`.
3. Open `data_archive/FILE_SHA256SUMS.txt` and confirm every archived file has
   a checksum.
4. Review `ZENODO_METADATA_TEMPLATE.md`.
5. Supply the final creator list / ORCIDs and select a license compatible with
   the derived analysis tables and code.
6. Do not add source species identifiers or uncited third-party raw files.

## Repository deposit

Deposit the ZIP in Zenodo, Dryad, Figshare, OSF or another Ecology Letters
accepted DOI-granting repository. A private-for-peer-review link is acceptable
at initial submission if the repository supports it; the archive must become
permanently accessible before publication.

The deposit metadata must cite the two source datasets:

- 10.5281/zenodo.8398202
- 10.5281/zenodo.14185547

and the associated source papers:

- 10.1002/ecs2.4696
- 10.1002/oik.11552

## After DOI minting

Replace the archive placeholder in:

1. `submission/ECOLOGY_LETTERS_LETTER_TITLE_PAGE_V1.md`
2. `manuscript/MANUSCRIPT_ACCESS_ROUTING_LETTER_V0.md`
3. `submission/ECOLOGY_LETTERS_LETTER_COVER_V0.md`
4. `docs/PUBLICATION_STATUS.md`
5. issue #227

Then rerun the Letter package workflow from the DOI-inserted commit.

## Submission gate

Do not submit while any of these remain:

```text
ACCESS_ROUTING_ARCHIVE_DOI = REQUIRED
FINAL_AUTHOR_LIST_AND_AFFILIATIONS = REQUIRED
AUTHORSHIP_STATEMENT = REQUIRED
CONFLICT_OF_INTEREST = REQUIRED
FUNDING_ACKNOWLEDGMENTS = REQUIRED
AUTHOR_RELATIVE_NOVELTY_STATEMENT = REQUIRED
```
