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

~~~text
ACCESS_ROUTING_ARCHIVE_DOI = REQUIRED_BEFORE_SUBMISSION
~~~

Once a DOI is minted, update all of:

1. `submission/ECOLOGY_LETTERS_LETTER_TITLE_PAGE_V1.md`
2. `manuscript/MANUSCRIPT_ACCESS_ROUTING_LETTER_V0.md`
3. `submission/ECOLOGY_LETTERS_LETTER_COVER_V0.md`
4. `docs/PUBLICATION_STATUS.md`
5. issue #227

Do not mark the external submission gate ready until the DOI resolves for editors/reviewers.


## Future k=3 use

The two analysis-ready CSVs are also the **only permitted production inputs for
the existing insect and bird networks** when a real third visitor network is
analysed.

The future k=3 production pipeline does not redownload or reconstruct Sakhalkar
or Aubert/EPHI. It requires these exact frozen bytes:

~~~text
sakhalkar_species_analysis.csv
  sha256 = 810ad672bf552e7fab0ad09193ef2502304511f741051b6edbab9c9d94a9074d

aubert_ephi_pair_site_analysis.csv
  sha256 = 3a873bb82b43b00df1e72c36c27d3740ff728b9d2a751f4fece6fdbbc20a40af

archive_manifest.json
  sha256 = 875ea2f77674034e20d18a7ac56f9d4d4240bfe9b22b90bf28f53f44028557c7
~~~

Their provenance is frozen in:

`empirical/floral_defence_selectivity/EXISTING_NETWORK_ARCHIVE_FREEZE_RECEIPT_V1.json`

Before any third network enters the equal-network k=3 statistic, the loader also
recomputes the observed Sakhalkar rho, Aubert site-adjusted/global rhos, unit/site
counts and the two-network Fisher-z rho and requires agreement with the canonical
repository `joint_access_routing.json`.
