# Ecology Letters access-routing data/code archive staging

This directory defines the archive that must receive a permanent DOI **before external submission** of the access-routing Letter.

## Required archive contents

The build workflow generates an `artifacts/letter/data_archive/` directory containing:

- `sakhalkar_species_analysis.csv` — 57 anonymous plant-species analysis units used for the insect routing and multitrait analyses;
- `aubert_ephi_pair_site_analysis.csv` — 2,265 anonymous bird × plant × site aggregation units under the metadata-informed missing-as-no rule, with anonymized plant- and bird-species cluster IDs; these reproduce both the 259-plant primary inference and the paired/continuous within-bird behavioral sensitivities;
- `aubert_ephi_participation_opportunities.csv` — zero-inclusive clean-camera waypoint × locally available bird opportunities used for the frozen participation-rate model, with anonymous waypoint, site, plant and bird IDs and the primary/strict/broad interaction counts;
- `metadata.csv` — file/column descriptions and units;
- `archive_manifest.json` — source DOIs, row counts and identifier policy;
- `archive_reproduction.json` — statistics regenerated using only the archived analysis tables;
- `supporting_literature/DIRECT_ACCESS_GEOMETRY_ELIGIBILITY_DECISIONS_V23.csv` — the complete 857-record frozen OpenAlex decision ledger;
- `supporting_literature/DIRECT_ACCESS_GEOMETRY_FULLTEXT_COMPLETE_RECEIPT_V1.json` — zero-pending full-text eligibility receipt;
- `supporting_literature/DIRECT_ACCESS_GEOMETRY_FORMAL_RECURRENCE_SUMMARY_V1.json` — frozen 33-program finite-frame direction summary;
- `supporting_literature/DIRECT_ACCESS_GEOMETRY_BOUNDARY_MECHANISM_AUDIT_V1.csv` and `.md` — post hoc mechanism audit of the four opposite and two mixed formal-frame programs;
- `supporting_literature/DIRECT_ACCESS_GEOMETRY_BOUNDARY_MECHANISM_SUMMARY_V1.json` — frozen descriptive boundary partition and 1/23 versus 3/10 search-origin contrast;
- `supporting_literature/DIRECT_ACCESS_GEOMETRY_ROBBERY_CORPUS_V1.csv` and Stage-U/Leal files — historical bounded-corpus provenance retained for audit, not the manuscript's final formal denominator.

The submission archive must also include the exact code used to export and reproduce the tables:

- `scripts/export_access_routing_archive.py`
- `scripts/reproduce_access_routing_archive.py`
- `scripts/analyze_aubert2026_participation_route_decomposition.py`
- `scripts/summarize_direct_access_geometry_corpus.py`
- `scripts/validate_direct_access_geometry_stage_u.py`
- `scripts/validate_direct_access_geometry_formal_frame.py`
- `scripts/validate_leal2025_direct_geometry_screen.py`
- the imported BITA analysis modules required by those scripts;
- frozen aggregate JSON outputs used in the manuscript, including the first-open participation result and receipt;
- the frozen participation preregistration and denominator/equivalence contract;
- this README.

## Formal direct-evidence boundary

The literature files reproduce the manuscript's completed frozen OpenAlex frame:

~~~text
frame records = 857
eligible independent direct programs = 33
positive = 22
null = 5
opposite = 4
mixed = 2
duplicate bibliographic records = 6
ineligible records = 818
pending full text = 0
network-k contribution = 0
~~~

These counts describe a finite provider-defined frame. They are **not** an estimate
of natural prevalence, a sign test, a pooled meta-analytic effect, or an additional
standardized-network replicate. The equal-network routing statistic remains
`k=2`. The older 24-program bounded corpus is retained only as provenance for the
pre-existing evidence base; it is not the final formal denominator. One pre-existing
program independently verified absent from OpenAlex is reported outside the
33-program denominator rather than injected into it.

## Public source data

Underlying public data remain attributed to their original repositories:

- Sakhalkar et al. 2023: Zenodo DOI `10.5281/zenodo.8398202`
- EPHI Ecuador mirror: Zenodo DOI `10.5281/zenodo.14185547`

The archive does not silently republish source species identifiers. It contains the exact analysis-ready units needed to reproduce the reported statistics. EPHI site, plant-species and bird-species labels are deterministically relabelled so the primary plant-species analysis and bird-species dependence sensitivity can be reproduced without exposing source taxon names.

## Reproduction

Inside the deposited archive directory:

~~~bash
PYTHONPATH=code python code/scripts/reproduce_access_routing_archive.py \
  --input-dir . \
  --output archive_reproduction_recheck.json
~~~

This command uses only the deposited analysis tables and deposited code; it does not redownload the source datasets.

The workflow verifies that the regenerated headline values agree with the committed frozen results, including the Ecuador participation rate ratio, plant-cluster jackknife confidence intervals, first-open outcome class, and strict/broad feeding sensitivities.

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
