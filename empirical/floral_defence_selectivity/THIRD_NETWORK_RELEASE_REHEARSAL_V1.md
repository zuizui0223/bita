# Third-network release rehearsal v1

## Status

~~~text
MODE = DEVELOPMENT_ONLY_SYNTHETIC
SCIENTIFIC_CLAIM_ALLOWED = NO
PRODUCTION_CODE_PATH = EXERCISED
POSITIVE_NULL_OPPOSITE = ALL_REQUIRED
~~~

This rehearsal closes the software gap between the synthetic field/data E2E and
the eventual real confirmatory release chain.

It runs the actual production components in sequence:

~~~text
synthetic frozen source inputs
        ->
transactional confirmatory bundle
        ->
BUNDLE_SHA256SUMS
        ->
read-only bundle verifier
        ->
original source-input SHA256 recheck
        ->
retained-result claim-transition planner
~~~

The rehearsal never edits manuscript files and can never promote a scientific
claim.

## Entry point

~~~bash
python scripts/run_third_network_release_rehearsal.py \
  --output-dir artifacts/third_network_release_rehearsal/positive \
  --scenario positive \
  --permutations 49
~~~

Allowed development scenarios:

~~~text
positive
null
opposite
~~~

All three use the same frozen input, reliability, build, analysis, verification
and claim-transition code.

## Required output

Each scenario must contain:

- `synthetic_fixture/`;
- `confirmatory_bundle/`;
- `confirmatory_bundle/BUNDLE_SHA256SUMS.txt`;
- `bundle_verification.json`;
- `claim_transition_plan.json`;
- `release_rehearsal_receipt.json`.

The receipt must report:

~~~text
status = PASS
bundle_verification_status = CONFIRMATORY_BUNDLE_VERIFIED
source_recheck_mode = SOURCE_INPUTS_RECHECKED
existing_network_inputs_verified = true
third_network_must_be_retained = true
scientific_claim_allowed = false
automatic_manuscript_edit_permitted = false
~~~

## Why this is separate from the synthetic E2E

The synthetic E2E proves that the prospective data pipeline can produce an
eligible third-network analysis and k=3 statistic.

The release rehearsal additionally proves that the **post-analysis production
chain** works:

1. transactional production-style bundle assembly;
2. complete bundle checksums;
3. exact Sakhalkar + Aubert/EPHI analysis-input rows saved and rehashed;
4. independent third-network source-input recheck;
5. bundle verification;
6. retained-result claim mapping.

A future real dataset should therefore require no new analysis architecture—only
replacement of the synthetic frozen inputs with the real frozen inputs.

## Retention rule

Positive, null-like and opposite synthetic third effects are all carried through
the same release chain.

No scenario may be dropped because it is unfavorable.

## Claim boundary

Passing this rehearsal demonstrates software wiring and integrity only. It does
not support the access-routing hypothesis, does not increase real network count
above k=2, and does not authorize manuscript modification.
