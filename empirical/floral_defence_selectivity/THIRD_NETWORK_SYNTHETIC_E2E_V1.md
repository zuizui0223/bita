# Third-network synthetic end-to-end development receipt v1

## Purpose

The prospective third-network code is now required to pass one complete synthetic
execution chain before any real confirmatory data are integrated.

The synthetic runner is:

~~~bash
python scripts/run_third_network_synthetic_e2e.py \
  --output-dir artifacts/third_network_synthetic_e2e
~~~

It executes the actual production modules in this order:

~~~text
route-blind presurvey
-> presurvey receipt + SHA256
-> pre-video confirmatory freeze
-> field-readiness evaluator
-> field-readiness receipt + confirmatory-freeze hash binding
-> confirmatory route / plant / mammal / camera input tables
-> input-freeze manifest
-> checksum-verifying unit builder
-> 72 mammal x plant x site units
-> third-network r_T
-> equal-network synthetic k=3 integration
-> synthetic_e2e_receipt.json
~~~

## Development-only boundary

Every E2E receipt must contain:

~~~text
mode = DEVELOPMENT_ONLY_SYNTHETIC
scientific_claim_allowed = false
~~~

Synthetic route values are intentionally generated to exercise the positive
routing path and the complete software wiring. They are not observations, do not
update the manuscript, and cannot lift the real k=2 ceiling.

## Chain-of-custody guard

The input-freeze stage no longer accepts a field-readiness JSON containing only
a READY label.

It requires:

- the field-readiness schema version;
- every required readiness gate = true;
- the field receipt's recorded confirmatory-freeze SHA256 to equal the exact
  confirmatory-freeze file supplied to input freezing;
- the field receipt's final sites to equal the final sites in that freeze;
- the field system to match the frozen design system.

This closes the last synthetic shortcut between field readiness and
route/morphology integration.

## Real-data state

~~~text
REAL_THIRD_NETWORK_DATA = NOT_COLLECTED
REAL_JOINT_NETWORK_K = 2
SYNTHETIC_E2E = DEVELOPMENT_VALIDATION_ONLY
~~~


## Outcome-direction scenario matrix

The development runner supports three synthetic route generators:

~~~text
positive  -> r_T expected > 0
null      -> structured route variation approximately orthogonal to M
opposite  -> r_T expected < 0
~~~

All three must pass the **same** presurvey, readiness, freeze, join and
confirmatory sample gates.

The null and opposite scenarios are deliberately not rejected or replaced.
Their receipts must still report:

~~~text
third_network_status = CONFIRMATORY_GATE_PASS
k3_network_count = 3
scientific_claim_allowed = false
~~~

For the opposite scenario, k3 direction concordance must be
`not_3_of_3_positive`. This is a software contract enforcing the preregistered
rule that an unfavorable real third-network result remains the third
confirmatory network.
