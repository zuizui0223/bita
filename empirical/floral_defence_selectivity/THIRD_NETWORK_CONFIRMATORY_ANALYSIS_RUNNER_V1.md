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

The output directory must be empty. Reusing a populated directory fails with
`CONFIRMATORY_OUTPUT_DIR_NOT_EMPTY`, preventing accidental overwrite of the
first confirmatory run.

## Receipt

The production receipt is:

~~~text
BITA_THIRD_NETWORK_CONFIRMATORY_ANALYSIS_V1
CONFIRMATORY_ANALYSIS_COMPLETE
~~~

It records:

- exact repository commit;
- existing-network input mode;
- input-freeze status;
- route reliability status and kappa;
- number of third-network analysis units;
- third-network rho, two-sided p-value, sign and seed;
- k=3 equal-network rho, p-value, concordance and seed;
- SHA256 for every generated scientific output;
- SHA256 receipts for source confirmatory inputs.

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
claims. A separate claim-update step must read the frozen receipt and apply the
predeclared claim ceiling.

Until real data exist:

~~~text
REAL_THIRD_NETWORK_DATA = NOT_COLLECTED
REAL_JOINT_NETWORK_K = 2
CONFIRMATORY_RUNNER = IMPLEMENTED_NOT_EXECUTED_ON_REAL_DATA
~~~
