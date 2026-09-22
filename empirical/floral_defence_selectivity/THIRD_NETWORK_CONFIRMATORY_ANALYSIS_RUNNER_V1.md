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
  --output-dir confirmatory_analysis_v1 \
  --repository-commit <exact-git-sha>
~~~

The default confirmatory run uses 9,999 permutations and the already frozen
third-network / k=3 seeds.

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
- existing-network input mode;
- the exact Sakhalkar and Aubert/EPHI analysis-input rows actually entering the
  k=3 calculation, saved as bundle JSON files;
- stable-content SHA256, file SHA256, row count and source DOI for each existing
  network input;
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
and k=3 headline values, and the exact bundled existing-network analysis inputs.
For Sakhalkar and Aubert/EPHI it reloads the saved rows, recomputes row count,
stable-content SHA256 and file SHA256, and checks the source DOI. It can also
optionally recheck the original frozen third-network source-input hashes.

Any mismatch returns:

~~~text
CONFIRMATORY_BUNDLE_INVALID
~~~

Verification is read-only and cannot promote or alter a manuscript claim.


## Archival release package

After bundle verification and claim-transition planning, freeze the complete
confirmatory state into the deterministic release package:

~~~bash
python scripts/package_third_network_confirmatory_release.py \
  confirmatory_analysis_v1 \
  --source-dir frozen_confirmatory_inputs \
  --output-dir third_network_confirmatory_release_v1
~~~

The package stores the complete confirmatory bundle, all six frozen third-network
source inputs, exact Sakhalkar/Aubert rows entering k=3, retained-result claim
plan, frozen protocol documents and the minimal replay code.

Offline replay requires no public-data download:

~~~bash
PYTHONPATH=code python \
  code/scripts/reproduce_third_network_confirmatory_release.py . \
  --output reproduction.json
~~~

The required replay status is `REPRODUCTION_MATCH`.

Archive construction does not itself permit a manuscript claim or automatic
manuscript edit; the claim-transition plan remains authoritative.
