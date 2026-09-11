# BITA manuscript claim freeze

This file is the editorial guardrail for the active BITA full paper after the SLK publication split.

## Active thesis

> **Trait interaction is not ecological mechanism.**

The paper asks what a measured cross-trait fitness interaction identifies, what stronger outcome claims require additional contrasts, which mechanisms remain compatible with the total interaction, and what intervention structure is required for mechanism allocation.

The active manuscript must not drift back into being the general architecture-value paper. The `L -> R -> Phi -> accessibility -> invasion -> fixation -> occupancy` spine belongs to SLK.

## Frozen outcome hierarchy

For focal trait contrasts `A` and `D`,

```text
Delta_AD W = W11 - W10 - W01 + W00
A0 = W10 - W00
A1 = W11 - W01
Delta_AD W = A1 - A0
```

The only permitted nested outcome claims are:

```text
Level 1  Delta_AD W > 0     positive interaction relief
Level 2  A0 <= 0 < A1       functional constraint release
Level 3  A0 < 0 < A1        strict reversal
```

Do not use `Delta_AD W > 0` as shorthand for Level 2 or Level 3.

## Frozen mechanism-identification object

Use the declared bookkeeping decomposition

```text
Delta_AD W = rho_delta - iota_delta - kappa_delta
```

with the interpretation:

- `rho_delta`: antagonist-relief allocation on the declared scale;
- `iota_delta`: pollinator-interference allocation on the declared scale;
- `kappa_delta`: independently justified remaining direct/allocation channel.

A measured total interaction `delta` defines

```text
I(delta) = {(rho,iota,kappa): rho-iota-kappa=delta}
```

rather than a unique mechanism.

The paper must explicitly state that greater precision in `Delta_AD W` does not by itself point-identify the channel allocation.

## Frozen identification ladder

```text
interaction detection
-> identified set
-> partial identification under explicit restrictions or partial channel measurement
-> selective A x D x antagonist x pollinator intervention
-> pollinator-absent baseline handling
-> four-way separability diagnostic
-> independent remaining-channel assay
-> mechanism-resolved interpretation
```

A residual from the reproductive outcome is not automatically `kappa_delta`.

## Frozen separability claim

The `A x D x antagonist x pollinator` four-way interaction is the diagnostic for whether the proposed antagonist and pollinator channel allocations remain separable across the alternate consumer state.

A non-zero four-way term is biologically informative and must not be hidden as nuisance variation. A near-zero estimate supports separability only under a prospectively justified uncertainty/equivalence rule; failure to reject zero is not proof of separability.

## Frozen partial-identification result

If an independently justified restriction gives

```text
kappa_delta >= 0,
```

then

```text
rho_delta - iota_delta
= Delta_AD W + kappa_delta
>= Delta_AD W.
```

This is a conditional partial-identification bound, not a universal theorem. Its validity is limited by the biological credibility of the restriction.

## Frozen empirical synthesis

The source-adjudicated route synthesis contains:

```text
56 directional route records
25 independent biological clusters
```

All four constituent marginal route families recur. These counts establish recurrence capacity only. They are not prevalence estimates and do not estimate the total interaction or its channel allocation.

The authoritative high-information frontier contains:

```text
17 systems
```

No screened system closes the full allocation design plus an independent remaining-channel assay.

Frozen empirical interpretation:

```text
RECURRENT_CONSTITUENT_BIOLOGY
+
FRAGMENTED_IDENTIFICATION
```

## Frozen strongest system-level anchor

For Kessler et al. (2008), under the registered aggregate constraints:

```text
A1 approximately +0.200 to +0.240
A0 approximately -0.030 to +0.030
Delta_AD remains positive
```

Permitted interpretation:

- strong aggregate Level-1 positive-interaction anchor;
- defended attraction effect `A1` sign-identified positive under declared constraints;
- undefended attraction effect `A0` remains zero-compatible;
- strict Level-2/3 release is not identified;
- exact source/design-based uncertainty remains unresolved;
- systemic nicotine manipulation leaves the focal defence scope imperfectly bounded;
- ecological channel allocation remains unidentified.

Do not promote this anchor beyond those statements.

## Frozen programme ownership

### SCH owns

```text
multifunctionality != identified functional conflict
state-specific optimum != pure-function optimum
```

and the promotion gates required before a shared-coordinate conflict budget is exported downstream.

### SLK owns

```text
L -> R -> Phi -> accessibility -> invasion -> fixation -> occupancy
```

including architecture value, the minimum quadratic bridge `R=sL`, population transport, and INV1.

### BITA owns

```text
trait interaction != ecological mechanism
```

plus identified sets, partial identification, selective crossed consumer interventions, separability diagnostics, remaining-channel assays, and the empirical identification frontier.

Older BITA architecture derivations remain versioned technical provenance. They may be cited as background but must not be presented as the active paper's central novelty.

## Claims that must not appear

Do not claim:

- a positive trait interaction identifies mechanism;
- a positive trait interaction proves trait differentiation;
- a positive interaction proves historical splitting, modularization, or cue privatization;
- marginal route recurrence identifies a joint mechanism;
- the 56/25 corpus estimates natural prevalence;
- the 17-system frontier estimates literature prevalence;
- a residual by subtraction is a measured cost;
- structural separation implies functional, developmental, or genetic independence;
- the active BITA paper owns the general `Phi=R-K` architecture-value threshold;
- the active BITA paper owns accessibility, invasion, fixation, or occupancy results;
- historical origin of differentiated traits has been reconstructed by the current evidence.

## Canonical manuscript status

Active canonical science source:

```text
manuscript/MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md
```

The file name is retained for provenance, but the scientific paper is now the mechanism-identification paper.

Longer mature identification provenance source:

```text
manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md
```

The old integrated architecture-plus-mechanism generated submission package is stale and must not be uploaded.

## Remaining manuscript work

1. Rebuild the figure set around the identification ladder, identified set, crossed intervention, and fragmented empirical frontier.
2. Reconcile figure captions with the new canonical Main.
3. Regenerate Appendix routing so architecture-value derivations are background/provenance rather than Main claims.
4. Rewrite the cover letter around `trait interaction != mechanism`.
5. Rebuild DOCX/PDF and repeat page-limit and visual QA.
6. Add author-controlled metadata only after the new scientific package is green.

## Editorial test

Every Main-text claim should pass five questions:

1. Does it distinguish a measured interaction from a mechanism allocation?
2. Does it distinguish Level 1 interaction relief from Levels 2/3 release?
3. Are restrictions used for partial identification explicit?
4. Is any residual mechanism named only after independent evidence?
5. Does the claim avoid re-importing architecture-value novelty already owned by SLK?

If any answer is no, revise before submission.
