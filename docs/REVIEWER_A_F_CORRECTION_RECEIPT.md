# Reviewer A–F correction receipt

This receipt records the disposition of the six pre-submission manuscript audit points raised against the canonical paperization state. It is a correction record, not a new scientific result.

## A — Leal data availability and reproducibility

**Accepted and fixed.** The complete canonical Leal et al. (2025) larceny module is restored directly to the current repository tree from immutable provenance commit `ed33b25593c0d90ad6657753f6f5501d9efc7b82`.

Restored scope includes the declared protocol/readout, effect rows, moderator coding/registry, recomputation audit, committed pooled/context outputs, context-dependence and deposited-effect code, offline runners, and integrity tests.

The current broad-meta contract is minimally extended with the three H routes and four declared larceny strata required by that module. `tests/test_submission_scope.py` now makes the Leal module mandatory, and `.github/workflows/validate-larceny-module.yml` reruns the module offline and diffs key regenerated outputs against the committed canonical results.

The import exposed one real compatibility break introduced by a later repository cleanup: the Leal context-dependence module imports the public `random_effects_pool()` API, while current `broad_meta_analysis.py` retained only its internal `_der_simonian_laird()` implementation. The public wrapper has been restored as a thin delegation to the current internal routine, so there is one numerical implementation rather than a duplicated legacy estimator.

The modern-estimator sensitivity now reads the canonical local contributing-effect file. The immutable source commit remains recorded as provenance, but reproducibility no longer depends on fetching an otherwise-unmerged historical branch.

## B — theorem premise

**Accepted and strengthened.** Theorem 1 now requires only non-negative direct joint-cost curvature (`kappa >= 0`). The proof is

```text
rho - iota = W_AD + kappa > 0.
```

The signs of `rho` and `iota` are not used by the implication. Their non-negative magnitude interpretation remains part of the oriented baseline mechanism, not a premise of the one-sided theorem. Manuscript, claim freeze, and selectivity-bound documentation are synchronized to this distinction.

## C — proof versus finite-grid verification

**Accepted.** The Abstract no longer presents the 2,592 evaluations as evidence for the theorem. It states that the implication is proved algebraically and that the grid verifies the implementation and quantifies looseness of the necessary window.

## D — 56/25 count provenance and non-additivity

**Verified and clarified.** `PATTERN_EXPANSION_READOUT_V1.json` records the admitted combined state as 56 route records / 25 independent biological clusters, same-system 14, sign/state-switch 17, and context-only 7. Its interpretation boundary explicitly says route counts overlap and must not be summed.

The manuscript now states that same-system and sign/state-switch annotations may overlap within the 25-cluster route universe and that the seven context-only programs are outside route-ledger N. A regression test pins the manuscript-facing counts to the readout.

## E — AI disclosure

**Accepted.** Repository history documents substantive Anthropic/Claude-assisted development in addition to later OpenAI-assisted work. The Methods disclosure now names large language models from **OpenAI and Anthropic** without inventing an exhaustive model/version list. The existing boundary remains: AI output is not empirical evidence and authors retain responsibility for the submitted content.

## F — Sasidharan synthesis wording

**Accepted.** The integration paragraph now separates the two robustness claims. Leal pooled directions retain their declared influence/sensitivity checks. Sasidharan's assembled contrast remains positive under leave-one-study-component-out deletion, but that is explicitly described as robustness of the assembled cross-study composition, not a within-study consumer-role effect; only three components contain both roles and all three paired differences are zero.

## No change to frozen scientific quantities

This correction does not change the 2,592-evaluation results, 77.2% selectivity-window precision, 56/25 Pattern counts, Leal pooled effects, Sasidharan assembled contrast, direct A×D evidence state, or direct joint-cost evidence state.
