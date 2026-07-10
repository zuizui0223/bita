# Retired exploratory workflows v1

## Purpose

This cleanup retires one-off exploratory workflows that are no longer part of the
active manuscript path after the Impatiens empirical-core and Results merges. The
underlying source readouts and stopping-decision documents remain in the repository.

This is a conservative cleanup: it removes workflow triggers, not the full code
modules behind every historical probe.

## Retired workflows

```text
.github/workflows/audit-dalechampia-linked-panel.yml
.github/workflows/probe-web-of-life.yml
.github/workflows/probe-wol-orientation.yml
.github/workflows/prepare-try-wol-request.yml
.github/workflows/probe-bien-floral-traits.yml
.github/workflows/probe-bien-leaf-feasibility.yml
.github/workflows/probe-bien-wol-attraction-coverage.yml
.github/workflows/inspect-impatiens-dryad-version.yml
.github/workflows/inspect-impatiens-dryad-structure.yml
.github/workflows/inspect-impatiens-dryad-csv-headers.yml
.github/workflows/inspect-impatiens-dryad-archive-headers.yml
```

## Rationale

These workflows were useful during source discovery, public-data feasibility checks,
or early Impatiens archive inspection. Their outcomes have either been superseded by
current readouts or absorbed into the active empirical workflow.

Current active paths are:

```text
.github/workflows/run-impatiens-empirical-core.yml
.github/workflows/part-b-integrity.yml
current theory/meta validation workflows that protect final claims
```

## What remains intentionally preserved

```text
1. Source readout documents that justify why routes were stopped or retained.
2. Candidate scouting tables and Part B integrity checks.
3. Impatiens empirical-core configs, scripts, tests, and workflow.
4. Part A theory and robustness code.
5. Historical scripts/modules until a separate import/reference audit confirms they
   are safe to delete.
```

## Next cleanup pass

A later cleanup can remove historical scripts and tests only after checking that they
are not imported by active workflows, manuscript documents, current evidence maps, or
integrity guards.
