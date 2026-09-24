# Third-network confirmatory release package v1

## Purpose

After a real third-network confirmatory run and retained-result claim transition,
the final analysis state must be archivable without depending on mutable working
directories or future downloads of the two existing public networks.

The package therefore contains the **exact inputs and code actually used** for
the three-network analysis.

## Production entry point

~~~bash
python scripts/package_third_network_confirmatory_release.py \
  confirmatory_analysis_v1 \
  --source-dir frozen_confirmatory_inputs \
  --output-dir third_network_confirmatory_release_v1
~~~

Production is the default and fails unless:

- the confirmatory bundle passes full SHA256 verification;
- the six frozen third-network source inputs are rechecked;
- the existing-network input mode is
  `PUBLIC_EXISTING_NETWORKS_FIXED_DOI_REBUILD`;
- the analysis receipt contains an exact 40-character repository commit;
- the current checkout is that exact repository commit;
- the retained-result claim-transition plan passes the production gate.

Synthetic/development rehearsal bundles require the explicit
`--development-only` switch.

## Archive contents

~~~text
confirmatory_bundle/
  exact third-network results
  exact Sakhalkar analysis rows entering k=3
  exact Aubert/EPHI analysis rows entering k=3
  input-freeze manifest
  analysis receipt
  BUNDLE_SHA256SUMS.txt

frozen_inputs/
  confirmatory event table
  plant morphology table
  mammal morphology table
  camera deployment table
  pre-video confirmatory freeze receipt
  field-readiness receipt

claim_transition_plan.json

protocol/
  preregistration
  prospective design
  route coding manual
  pilot split
  seed receipt
  production runner contract
  claim-transition contract
  release rehearsal contract
  frozen code manifest

code/
  minimal offline replay code

release_manifest.json
FILE_SHA256SUMS.txt
README.md
~~~

Raw camera video is not required for numerical replay of the confirmatory
analysis. Its long-term archival policy remains separate from the exact
analysis-input archive.

## Read-only release integrity verification

Before scientific replay, verify the package shell itself:

~~~bash
PYTHONPATH=code python code/scripts/verify_third_network_release_package.py .
~~~

When the adjacent deterministic ZIP and SHA256 receipt are available, require
their recheck explicitly:

~~~bash
PYTHONPATH=code python code/scripts/verify_third_network_release_package.py . \
  --zip ../third_network_confirmatory_release_v1.zip \
  --sha256-receipt ../third_network_confirmatory_release_v1.zip.sha256 \
  --require-archive
~~~

The verifier checks:

- exact `FILE_SHA256SUMS.txt` inventory;
- every package-file digest;
- release-manifest claim guardrails;
- frozen-input / code / protocol digest maps;
- nested confirmatory bundle verification;
- ZIP member inventory and bytes;
- fixed ZIP timestamps and `ZIP_STORED` method;
- adjacent ZIP SHA256 receipt.

The verifier is read-only and does not recompute or change the scientific result.

Archive-shell verification is also strict. Every ZIP member must be a regular Unix file with mode `0644`, `create_system=3`, fixed timestamp `1980-01-01 00:00:00`, `ZIP_STORED` compression, no encryption, no per-member extra/comment payload, and no directory/symlink/special-file metadata. The ZIP-level comment must be empty. Thus changing only archive metadata while preserving file bytes is still treated as release tampering.

## Offline replay

After extraction:

~~~bash
PYTHONPATH=code python code/scripts/reproduce_third_network_confirmatory_release.py . \
  --output reproduction.json
~~~

The replay:

1. verifies the complete confirmatory bundle;
2. rechecks all six frozen third-network inputs;
3. rebuilds mammal × plant × site analysis units;
4. recomputes the frozen third-network effect with its recorded seed and
   permutation count;
5. reloads the exact bundled Sakhalkar and Aubert/EPHI rows;
6. recomputes the equal-network k=3 statistic;
7. compares the recomputed scientific outputs with the archived outputs.

Success requires:

~~~text
REPRODUCTION_MATCH
~~~

No public-data network access is required.

## Deterministic ZIP

The packager writes:

~~~text
<third_network_release>.zip
<third_network_release>.zip.sha256
~~~

ZIP members are sorted, receive fixed metadata/time, and are stored with
`ZIP_STORED` rather than DEFLATE. Avoiding compression removes zlib-version
behavior from the byte stream.

The CI contract freezes one identical synthetic input fixture, rebuilds the
scientific bundle and archive independently under Python 3.10, 3.11 and 3.12,
and requires one identical ZIP SHA256 across all three environments. Generated
scientific receipt floats use the shared 15-significant-digit archival
serialization rule; raw/source analysis rows are never quantized. The same
frozen inputs and repository code must also remain path-independent.

This cross-Python byte-identity comparison is a blocking release-package gate,
not an informational diagnostic.

This makes the ZIP SHA256 an immutable submission/archive receipt rather than an
environment-specific compression artifact.

## Development rehearsal

For synthetic fixtures only:

~~~bash
python scripts/package_third_network_confirmatory_release.py \
  synthetic_confirmatory_bundle \
  --source-dir synthetic_fixture \
  --output-dir development_release \
  --development-only
~~~

A development archive is permanently labelled synthetic and cannot by itself
license a scientific claim or manuscript edit.

## Claim boundary

The archive is a reproducibility object. Even for a real production package:

~~~text
scientific_claim_allowed_by_archive_alone = false
automatic_manuscript_edit_permitted = false
~~~

The separate retained-result claim-transition plan remains authoritative for
what can be written in the manuscript.
