# Ecology Letters access-routing data/code archive staging

This directory defines the archive that must receive a permanent DOI **before external submission** of the access-routing Letter.

## Required archive contents

The build workflow generates an `artifacts/letter/data_archive/` directory containing:

- `sakhalkar_species_analysis.csv` — 57 anonymous plant-species analysis units used for the insect routing and multitrait analyses;
- `aubert_ephi_pair_site_analysis.csv` — 1,378 anonymous bird × plant × site analysis units used for the Ecuadorian routing analyses;
- `metadata.csv` — file/column descriptions and units;
- `archive_manifest.json` — source DOIs, row counts and identifier policy;
- `archive_reproduction.json` — statistics regenerated using only the archived analysis tables.

The submission archive must also include the exact code used to export and reproduce the tables:

- `scripts/export_access_routing_archive.py`
- `scripts/reproduce_access_routing_archive.py`
- the imported BITA analysis modules required by those scripts;
- frozen aggregate JSON outputs used in the manuscript;
- this README.

## Public source data

Underlying public data remain attributed to their original repositories:

- Sakhalkar et al. 2023: Zenodo DOI `10.5281/zenodo.8398202`
- EPHI Ecuador mirror: Zenodo DOI `10.5281/zenodo.14185547`

The archive does not silently republish source species identifiers. It contains the exact analysis-ready units needed to reproduce the reported statistics. EPHI site labels are deterministically relabelled while preserving within-site permutation groups.

## Reproduction

Inside the deposited archive directory:

~~~bash
PYTHONPATH=code python code/scripts/reproduce_access_routing_archive.py \
  --input-dir . \
  --output archive_reproduction_recheck.json
~~~

This command uses only the deposited analysis tables and deposited code; it does not redownload the source datasets.

The workflow verifies that the regenerated headline values agree with the committed frozen results.

## Deposit-ready package

The CI workflow additionally creates one upload-ready archive:

~~~text
access-routing-letter-data-code-v1.zip
access-routing-letter-data-code-v1.sha256
~~~

The ZIP contains the complete `data_archive/` directory. Internal file checksums are stored in `FILE_SHA256SUMS.txt`. Use `DEPOSIT_CHECKLIST_V1.md` for the final DOI-deposit sequence.

## DOI gate

Use a **reserved Zenodo DOI before the final package build**. This avoids a
self-referential archive cycle in which minting the DOI changes the repository
commit recorded inside the deposited ZIP.

~~~text
1. create and save the Zenodo draft
2. reserve the DOI in the draft
3. insert that reserved DOI into the manuscript/title page/cover/status
4. commit those DOI insertions
5. build the final package from that exact commit
6. upload access-routing-letter-data-code-v1.zip to the same Zenodo draft
7. verify the ZIP SHA256 and publish the record
~~~

Before step 5, update all of:

1. `submission/ECOLOGY_LETTERS_LETTER_TITLE_PAGE_V1.md`
2. `manuscript/MANUSCRIPT_ACCESS_ROUTING_LETTER_V0.md`
3. `submission/ECOLOGY_LETTERS_LETTER_COVER_V0.md`
4. `docs/PUBLICATION_STATUS.md`
5. issue #227

~~~text
ACCESS_ROUTING_ARCHIVE_DOI = RESERVED_DOI_REQUIRED_BEFORE_FINAL_PACKAGE_BUILD
~~~

The reserved DOI is not registered until the Zenodo record is published. Do not
delete the draft after reserving the DOI. Do not mark the external submission
gate ready until the published DOI resolves for editors/reviewers.
