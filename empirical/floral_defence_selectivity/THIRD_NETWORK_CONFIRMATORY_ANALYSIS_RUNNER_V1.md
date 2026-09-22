# Third-network confirmatory analysis runner v1

## Purpose

Once real confirmatory route and morphology data exist, the analysis must not be
assembled manually from separate commands. The sole production entry point is:

~~~bash
python scripts/run_third_network_confirmatory_pipeline.py \
  confirmatory_events.csv \
  plant_traits.csv \
  mammal_traits.csv \
  camera_deployment.csv \
  confirmatory_freeze_receipt.json \
  field_readiness_receipt.json \
  --existing-network-archive-dir access-routing-letter-data-code-v1/data_archive \
  --output-dir confirmatory_analysis_v1 \
  --repository-commit <exact-git-sha>
~~~

The default confirmatory run uses 9,999 permutations and the already frozen
third-network / k=3 seeds.

The existing insect and bird networks are **not redownloaded** during this run.
They must come from the exact Ecology Letters analysis-ready archive containing
`sakhalkar_species_analysis.csv`, `aubert_ephi_pair_site_analysis.csv`, and
`archive_manifest.json`. Before the third-network analysis starts, those tables
must reproduce the committed frozen k=2 values for the Sakhalkar rho, Aubert
site-adjusted rho, Aubert global descriptive rho, unit/site counts, and the
equal-network Fisher-z joint rho.

## One-way execution chain

~~~text
real confirmatory inputs
        |
        v
field-readiness + pre-video freeze chain revalidated
        |
        v
deterministic 20% route reliability subset
        |
        v
kappa_LBAN >= 0.80 required
        |
        v
all route/morphology/camera inputs SHA256 frozen
        |
        v
checksum-verifying analysis-unit builder
        |
        v
frozen third-network r_T + two-sided permutation p
        |
        v
equal-network k=3 analysis
        |
        v
confirmatory_analysis_receipt.json
~~~

The final output directory must be absent or empty. The runner writes first to
a sibling `.inprogress` staging directory and atomically renames that directory
to the requested output path only after the full third-network and k=3 chain
succeeds.

A handled analysis failure removes the staging directory and leaves no partial
final result. A pre-existing staging directory is treated as evidence of an
interrupted prior process and fails closed with
`CONFIRMATORY_STAGING_DIR_EXISTS`; it is never silently reused or deleted.

Reusing a populated final directory fails with
`CONFIRMATORY_OUTPUT_DIR_NOT_EMPTY`, preventing accidental overwrite of the
first completed confirmatory run.

## Receipt

The production receipt is:

~~~text
BITA_THIRD_NETWORK_CONFIRMATORY_ANALYSIS_V1
CONFIRMATORY_ANALYSIS_COMPLETE
~~~

It records:

- exact 40-character repository commit, checked against the current checkout
  when Git metadata are available;
- existing-network input mode = `FROZEN_LETTER_ANALYSIS_ARCHIVE_V1`;
- SHA256 for both exact Letter analysis tables, their archive manifest, and the
  canonical repository k=2 receipt;
- PASS receipt that the archive reproduces the committed k=2 observed effects;
- stable JSON SHA256 digests and source DOIs for the Sakhalkar and Aubert/EPHI
  analysis inputs actually entering the k=3 calculation;
- input-freeze status;
- route reliability status and kappa;
- number of third-network analysis units;
- third-network rho, two-sided p-value, sign and seed;
- k=3 equal-network rho, p-value, concordance and seed;
- SHA256 for every generated scientific output;
- SHA256 receipts for source confirmatory inputs;
- `BUNDLE_SHA256SUMS.txt`, which hashes the completed receipt itself plus every
  other file in the final analysis directory.

## Result-direction rule

The runner contains no success gate on the sign or p-value of the third
network.

~~~text
positive -> retained
null-compatible -> retained
opposite -> retained
~~~

An eligible opposite result therefore produces a completed receipt and enters
the k=3 statistic as the third network. It is not replaced by a more favorable
system.

## Manuscript boundary

A completed runner receipt does **not** automatically edit or promote manuscript
claims. The next mandatory step is the read-only claim-transition planner:

~~~bash
python scripts/plan_third_network_claim_transition.py \
  confirmatory_analysis_v1 \
  --source-dir frozen_confirmatory_inputs \
  --output third_network_claim_transition.json
~~~

The planner requires a verified bundle plus rechecked frozen source inputs and
applies the predeclared claim ceiling without selecting on sign or p-value.

Until real data exist:

~~~text
REAL_THIRD_NETWORK_DATA = NOT_COLLECTED
REAL_JOINT_NETWORK_K = 2
CONFIRMATORY_RUNNER = IMPLEMENTED_NOT_EXECUTED_ON_REAL_DATA
~~~


## Transaction boundary

The final result directory is a success object, not a scratch workspace.

~~~text
<output>.inprogress
        |
        | all gates + r_T + k=3 + receipt succeed
        v
<output>
~~~

No final directory is exposed after a handled partial failure. This prevents a
half-built input manifest or third-network result from being mistaken for a
completed confirmatory analysis.


## Independent bundle verification

After a completed run is moved, copied or archived, verify it without rerunning
the science:

~~~bash
python scripts/verify_third_network_confirmatory_bundle.py \
  confirmatory_analysis_v1
~~~

If the original frozen input files are available in one directory, recheck them
as well:

~~~bash
python scripts/verify_third_network_confirmatory_bundle.py \
  confirmatory_analysis_v1 \
  --source-dir frozen_confirmatory_inputs
~~~

The verifier first checks `BUNDLE_SHA256SUMS.txt` against the complete file
inventory, including the analysis receipt itself. It then checks the nested
generated-output SHA256 receipts, manifest/receipt consistency, third-network
and k=3 headline values, existing-network input digests/source DOIs, and
optionally the original source-input hashes.

Any mismatch returns:

~~~text
CONFIRMATORY_BUNDLE_INVALID
~~~

Verification is read-only and cannot promote or alter a manuscript claim.


## Existing-network immutability

The real k=3 run is intentionally offline with respect to the two existing
networks.

~~~text
Letter analysis-ready archive
        |
        v
57 Sakhalkar species + 1,378 Aubert/EPHI pair-site units
        |
        v
recompute observed r_S, r_A and r_J2
        |
        v
must equal committed joint_access_routing.json
        |
        v
only then add the retained third network
~~~

The production CLI does not accept an alternate k=2 result receipt. The
canonical comparison target is fixed by the repository checkout used for the
recorded production commit.
