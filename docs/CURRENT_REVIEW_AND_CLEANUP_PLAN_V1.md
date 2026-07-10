# Current review and cleanup plan v1

## Why this exists

This file summarizes the repository state after the manuscript Results merge and
sets the cleanup boundary. It does not add analyses, definitions, or parameters.

## Current result status

The project has shifted from a hoped-for universal pooled meta-analysis to a
three-part manuscript structure:

```text
1. Formal conditional attraction-defence theory.
2. Literature evidence map and evidence-gap audit.
3. Impatiens capensis response-scale empirical case study.
```

This matches the frozen hypothesis direction: attraction and defence/access traits
are not assumed to be universally complementary or universally substitutable. Their
relationship depends on the balance between defence benefits against antagonists,
pollination costs, and shared costs. The literature route currently supports the
reality of pollination costs for some defence/access traits, while the remaining
parameters are not generally identifiable from existing public studies.

## Locked Impatiens result summary

```text
D candidate -> pollinator use:
  RR 0.682 [0.479, 0.972]
  observational pollination-cost-like association

D candidate -> natural floral damage:
  OR 1.121 [0.990, 1.269]
  no resolved protective direction

A -> pollinator use:
  RR 0.981 [0.626, 1.539]
  unresolved

A -> natural floral damage:
  OR 1.064 [0.933, 1.213]
  unresolved

A × D candidate -> seeds per CH fruit:
  RR 1.008 [0.968, 1.049]
  unresolved component surface

randomized imposed florivory -> CH fruits/day:
  beta -0.290 [-0.540, -0.040]
  randomized downstream reproductive-component cost

phenology -> CH fruits/day:
  beta -0.493 [-0.617, -0.369]
  strong reproductive-component association
```

## Safe interpretation

The current empirical claim is asymmetric:

```text
The floral-tannin candidate is associated with reduced pollinator use,
but it is not resolved as protective against natural floral damage.
Imposed florivory experimentally reduces CH fruit production.
```

This supports a case-study constraint on the theory, not a direct empirical proof of
complementarity, substitutability, a total-fitness mixed partial, or `c_AD`.

## Cleanup boundary

Repository cleanup should now remove or retire implementation that is no longer part
of the active manuscript path.

Safe cleanup categories:

```text
1. One-off exploratory workflows for abandoned public-data probes.
2. Candidate-screen workflows whose result has already been converted to a readout.
3. Old route-discovery helpers that are not referenced by the current manuscript,
   active README path, or CI.
```

Do not delete yet:

```text
1. Impatiens empirical-core code, configs, tests, workflows, and readouts.
2. Part A mathematical/theory code.
3. Part B integrity guards and final evidence-map artifacts.
4. Candidate readout documents that justify stopping decisions.
5. Anything referenced by current manuscript skeleton, Results, or Results tables.
```

## Immediate cleanup recommendation

First PR should be conservative:

```text
- Update README to reflect the current manuscript architecture.
- Remove stale one-off exploratory workflows that are not required to reproduce the
  current manuscript path.
- Add a legacy-retirement note for exploratory source-probe scripts before deleting
  any code modules.
```

A second cleanup PR can remove code modules after import/reference checks confirm
that no current tests, docs, or workflows depend on them.
