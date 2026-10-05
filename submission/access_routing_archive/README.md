# Ecology Letters access-routing data/code archive staging

This directory defines the archive that must receive a permanent DOI **before external submission** of the access-routing Letter.

## Required archive contents

The build workflow generates an `artifacts/letter/data_archive/` directory containing:

- `sakhalkar_species_analysis.csv` — 57 anonymous plant-species analysis units used for the insect routing and multitrait analyses;
- `aubert_ephi_pair_site_analysis.csv` — 2,265 anonymous bird × plant × site aggregation units under the metadata-informed missing-as-no rule, with anonymized plant- and bird-species cluster IDs; these reproduce both the 259-plant primary routing inference and the paired/continuous within-bird behavioral sensitivities;
- `aubert_ephi_participation_opportunities.csv` — the zero-inclusive clean-waypoint × locally available bird opportunity table used to reproduce the frozen pooled participation rate ratio, the post-open robbing versus legitimate/non-robbing decomposition, and the hummingbird-only effective-reach sensitivity; it includes `primary_count`, `robbing_count`, `legitimate_count` and anonymous `bird_group` with relabelled waypoint, plant, bird and site identifiers;
- `metadata.csv` — file/column descriptions and units;
- `archive_manifest.json` — source DOIs, row counts and identifier policy;
- `archive_reproduction.json` — statistics regenerated using only the archived analysis tables, including pooled and route-specific participation, the preregistered threshold/boundary audit, and the post-open hummingbird effective-reach sensitivity;
- `supporting_literature/DIRECT_ACCESS_GEOMETRY_ROBBERY_CORPUS_V1.csv` — the 24-program bounded direct geometry → robbery supporting corpus;
- `supporting_literature/DIRECT_ACCESS_GEOMETRY_STAGE_U_REGISTRY_V1.csv` — included, duplicate and excluded Stage-U update candidates with explicit reasons;
- `supporting_literature/LEAL2025_DIRECT_GEOMETRY_SCREEN_V1.csv` — complete 56-label historical geometry screen;
- `supporting_literature/DIRECT_ACCESS_GEOMETRY_ELIGIBILITY_DECISIONS_V23.csv` — complete frozen eligibility/direction decisions for the formal 857-record OpenAlex frame;
- `supporting_literature/DIRECT_ACCESS_GEOMETRY_FULLTEXT_COMPLETE_RECEIPT_V1.json` — receipt that no formal-frame records remain pending;
- `supporting_literature/DIRECT_ACCESS_GEOMETRY_FORMAL_RECURRENCE_SUMMARY_V1.json` — frozen finite-frame summary of 33 eligible direct programs (22 positive, 5 null, 4 opposite, 2 mixed);
- `supporting_literature/DIRECT_ACCESS_GEOMETRY_BOUNDARY_MECHANISM_AUDIT_V1.csv` and `.md` — post hoc mechanism audit of the four opposite and two mixed formal-frame programs;
- `supporting_literature/DIRECT_ACCESS_GEOMETRY_BOUNDARY_MECHANISM_SUMMARY_V1.json` — frozen descriptive boundary partition;
- the direct-evidence eligibility contract, bounded-search receipts, Leal crosswalk and provenance receipts needed to audit the supporting-corpus counts.

The submission archive must also include the exact code used to export and reproduce the tables:

- `scripts/export_access_routing_archive.py`
- `scripts/reproduce_access_routing_archive.py`
- `scripts/analyze_aubert2026_route_specific_participation_postopen.py`
- `scripts/analyze_aubert2026_routing_threshold.py`
- `scripts/audit_aubert2026_threshold_bootstrap_boundary.py`
- `scripts/analyze_aubert2026_hummingbird_reach_sensitivity.py`
- `scripts/reproduce_aubert2026_hummingbird_reach_archive.py`
- `scripts/summarize_direct_access_geometry_corpus.py`
- `scripts/validate_direct_access_geometry_stage_u.py`
- `scripts/validate_direct_access_geometry_formal_frame.py`
- `scripts/validate_leal2025_direct_geometry_screen.py`
- the imported BITA analysis modules required by those scripts;
- frozen aggregate JSON outputs used in the manuscript, including the first-open participation and threshold results with their freeze/receipt files;
- `diagnostic_receipts/AUBERT2026_POSTOPEN_DIAGNOSTICS_RECEIPT_V1.json`, preserving workflow/artifact provenance and hashes for the post-open route split and bootstrap boundary audit;
- `analysis_contracts/HUMMINGBIRD_EFFECTIVE_REACH_SENSITIVITY_FREEZE_V1.md` and `diagnostic_receipts/aubert2026_hummingbird_effective_reach_sensitivity.json`, preserving the frozen post-open reach sensitivity and its result;
- this README.

## Supporting direct-evidence boundary

The literature files reproduce the manuscript's completed formal-frame statement:

~~~text
857 unique OpenAlex records
33 eligible independent direct study programs
22 positive
5 null
4 opposite
2 mixed
pending full text = 0
network-k contribution = 0
~~~

These counts describe one frozen provider-defined bibliographic frame. They are not a prevalence estimate, sign test or pooled effect. The standardized routing synthesis remains based on two independent networks only. The older 24-program bounded corpus is retained only as provenance for the targeted-search history and is not the manuscript's final formal denominator.

## Public source data

Underlying public data remain attributed to their original repositories:

- Sakhalkar et al. 2023: Zenodo DOI `10.5281/zenodo.8398202`
- EPHI Ecuador mirror: Zenodo DOI `10.5281/zenodo.14185547`

The archive does not silently republish source species identifiers. It contains the exact analysis-ready units needed to reproduce the reported statistics. EPHI waypoint, site, plant-species and bird-species labels are deterministically relabelled so the primary routing analysis, within-bird sensitivities and zero-inclusive participation model can be reproduced without exposing source taxon names.

## Reproduction

Inside the deposited archive directory:

~~~bash
PYTHONPATH=code python code/scripts/reproduce_access_routing_archive.py \
  --input-dir . \
  --output archive_reproduction_recheck.json
~~~

This command uses only the deposited analysis tables and deposited code; it does not redownload the source datasets.

The workflow verifies that the regenerated headline values agree with the committed frozen first-open results and retained post-open diagnostics. It must recover the culmen-only route split and 585/999 threshold boundary mass, and from the V5 anonymous tables reproduce the 1.8× hummingbird-reach result: pooled RR 0.2287, legitimate RR 0.1537 (95% CI 0.0872–0.2710), robbery RR 0.8164 (0.3583–1.8602), and robbery/legitimate RR ratio 5.311 (1.923–14.672).

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
