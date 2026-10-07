# Colwell feeding-state coding correction v1

Status: **SOURCE-CODING CORRECTION AFTER FIRST TRIAGE OPEN**

Date: 2026-10-07
Branch: `analysis/ecological-stability-evolutionary-transience-v1`

## Error found

The first implementation reconstructed clinger state from raw feeding-style indicator
columns using only values equal to 1. Some source cells use `0.5` for mixed/partial
style records, so this reconstruction yielded 64 clingers, 147 presumed non-clingers,
and 9 excluded on-wing piercers rather than the published source totals.

This is a source-coding error, not a statistical-model choice.

## Authoritative source coding

Colwell et al. assign every species a single `Feeding style code` in Supplemental
Spreadsheet S1. Its observed counts exactly reproduce the paper:

```text
codes 1–5: clinging-required feeding categories
            6 + 21 + 11 + 26 + 2 = 66 species

code 6:     feeds through pierces on the wing
            10 species

code 7:     presumed non-clinger / orthodox legitimate-on-wing
            144 species
```

This matches the article's explicit statement of 66 known clingers, 10 unorthodox
on-wing piercers, and 144 presumed non-clingers.

## Correction rule

All analyses using the Colwell binary state must henceforth use:

```text
Feeding style code in {1,2,3,4,5} -> state 1 (clinger)
Feeding style code == 6            -> excluded from binary state contrast
Feeding style code == 7            -> state 0 (presumed non-clinger)
```

No ecological or macroevolutionary outcome is used in this correction.

## Consequence for already-opened tests

- The continuous morphology part of
  `PREVALENCE_ADAPTATION_DECOUPLING_FIRST_OPEN_V1.md` is unchanged because it does
  not use the binary clinger label.
- Its clinger/non-clinger corroboration must be recomputed and the original values
  retained in history as superseded-by-source-correction.
- The clinger-speciation-rate triage must be rerun with the authoritative code.
- The preregistered endpoint/statistic/permutation rules are unchanged.

This correction cannot be used to change endpoints, select a favorable speciation-rate
metric, remap taxa, or alter the decision rule after outcomes have been seen.
