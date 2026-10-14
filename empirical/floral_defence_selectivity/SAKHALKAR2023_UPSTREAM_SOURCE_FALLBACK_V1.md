# Sakhalkar 2023 upstream-source fallback provenance (2026-10-14)

## Why this exists

The frozen Sakhalkar 2023 Zenodo archive (`10.5281/zenodo.8398202`) returned HTTP 504 across five independent Letter CI jobs on 2026-10-13 (run IDs 38427535280, 38427535475, 38427535305, 38427535535 and 38427535538). Those failures occurred during source retrieval **before** the network analysis; they are not evidence of a different ecological result. More unbounded retries of the same URL would not solve this single-provider failure.

## Sources and verified identifiers

**Primary:** the existing Zenodo release:

```text
DOI     10.5281/zenodo.8398202
ZIP     SaileeSakhalkar/cheaters-among-pollinators-ecosphere-v1.0.0.zip
```

**Transport fallback after transient failure only:** Sakhalkar et al.'s author-maintained public GitHub repository, with no moving branch ref:

```text
REPO       SaileeSakhalkar/cheaters-among-pollinators-ecosphere
TAG        v1.0.0
COMMIT     605d76245a8e89ec9932d0ce5368e47f1ecabd5c
WORKBOOK   input/cheaters_visitation_and_trait_data.xlsx
SIZE       755561 bytes
GIT BLOB   0ee25ea58c12e5641d0eda9926f8aa87bb5e35e6
```

The tag → commit and commit tree → workbook blob/size were read from the **upstream GitHub Git refs/trees**, not inferred from a filename. The retrieval fallback asks GitHub for an archive of **that immutable commit** and verifies the extracted workbook's Git blob SHA-1, calculated using `sha1(b"blob <size>\\0" + workbook)`. Wrong file count, wrong workbook size, mismatched digest, oversized or malformed ZIP, or unreachable author source each fails closed.

The GitHub ZIP container may not be byte-identical to the Zenodo-exported ZIP (path prefixes and ZIP metadata can differ). The gate guarantees the workbook is exactly the one identified by the author repository's tagged Git object. It **does not by itself establish** independent byte identity with the Zenodo workbook unless a separate source-to-source comparison is recorded. All downstream published aggregate input counts and manuscript-facing results must still match the existing frozen receipts before anything is promoted.

## Retrieval rule

1. Try the original Zenodo URL with **four** bounded attempts on transient HTTP 5xx/network failures.
2. On Zenodo HTTP 4xx (nontransient), **stop**. Do not silently switch versions or providers.
3. Only after transient failure, request the author's **pinned tagged commit** archive, check ZIP limits, one primary workbook, exact size and Git blob SHA.
4. Print `SOURCE_PROVENANCE` to the CI stderr log upon verified author-source fallback; do not print raw biological rows.
5. Continue the source workbook → analysis-ready data → **fresh** analysis and frozen-results comparison. Do not substitute a hardcoded JSON result, synthetic workbook, or an arbitrary cached file as a supposedly fresh public-data analysis.

The downloader, its deterministic fallback integrity tests, and the live tagged-upstream audit are maintained in:

- `scripts/audit_sakhalkar2023_zenodo.py`
- `tests/test_sakhalkar2023_zenodo_audit.py`
- `.github/workflows/audit-sakhalkar2023-zenodo.yml`

The audit workflow invokes the pinned author source **directly** as a separate live check even if Zenodo works, and asserts that the tagged workbook contains `cheater_data` and `plant_traits` sheets; it reports only metadata and the fixed commit ID.

## Scientific and release gates unchanged

The target scientific freeze is Sakhalkar `n=57`, plant-level `rho=0.3468`, permutation `p=0.0086`, and the independent Ecuador result `rho=0.5032`; equal-network `rho_J=0.4282`, `k=2`. Those values are verified by existing archive-only reproduction rather than replaced by the fallback logic. A live fallback connection and the frozen analytical comparisons must both pass for a green full package.

No raw third-party ZIP or taxon-labelled workbook is added to the BITA repository or final anonymized analysis-ready archive. Author-controlled final archive license, Zenodo deposition, author approval, exact DOI-bearing source provenance, and journal submission remain **blocked** until their separate release gates pass. The fallback does not authorize publication or weaken those gates.
