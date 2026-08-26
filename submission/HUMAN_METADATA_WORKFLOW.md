# Human metadata workflow

The scientific manuscript and machine-controlled submission package are complete. The remaining release-controlled information is intentionally isolated from scientific source files.

## Single input file

Copy and fill:

```text
submission/AUTHOR_METADATA_INPUT_TEMPLATE.json
```

Keep author order exactly as approved for publication. Do not infer missing names, affiliations, ORCIDs, funding, competing interests, licences, or approval states from repository history.

The JSON collects:

- final publication names and author order;
- affiliations and optional present addresses;
- e-mail addresses and the single corresponding author;
- ORCIDs (`N/A` may be used only when the author explicitly confirms that choice);
- CRediT roles;
- funding statement and grants;
- acknowledgments;
- competing-interest statement;
- repository/software/data licence statement;
- explicit all-author approval, Ecology-submission agreement, and no-simultaneous-consideration confirmation;
- reviewer/opposed-reviewer fields only when the live portal requests them.

## Validation

Schema-only validation, safe while the template remains blank:

```bash
python scripts/validate_author_metadata.py
```

Final completeness gate after the author-approved values have been entered:

```bash
python scripts/validate_author_metadata.py submission/AUTHOR_METADATA_INPUT_TEMPLATE.json --require-complete
```

The final gate requires exactly one corresponding author, non-empty publication names/affiliations/e-mails/CRediT roles, explicit funding and competing-interest statements, a licence statement, and all three submission confirmations set to `true`. Reviewer lists are not required because their number and fields depend on the live ScholarOne portal.

## After the completeness gate passes

1. propagate the approved metadata into the title page, declarations, cover letter, and portal template;
2. rebuild the canonical Ecology package;
3. rerun CI, submission-scope, candidate/canonical package builds, and Fig1–Fig5 EPS export;
4. visually inspect every Main and Appendix page again;
5. confirm the portal fields exactly match the frozen files;
6. obtain all-author approval of that exact version before upload.

The metadata file is a release-control surface, not a source of scientific claims.
