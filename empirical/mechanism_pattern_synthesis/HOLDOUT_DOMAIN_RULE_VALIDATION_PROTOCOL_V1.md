# Hold-out validation protocol v1 — effective-domain separation rule

## Registration point

This protocol is committed **before executing the new hold-out search batch**. It is intended to reduce circularity after the domain-separation rule was developed from the existing source-adjudicated evidence set.

## Fixed rule under test

For one flower-specific antagonist-reducing defence/access trait D:

```text
separated antagonist vs pollinator effective domains
    -> antagonist reduction with limited/no pollinator interference

overlapping effective domains
    -> antagonist reduction plus pollinator interference

antagonist bypass or tolerance of the D domain
    -> focal antagonist-reduction channel weak/null despite D expression
```

Effective domain may be defined by susceptibility, dose/exposure, attack route, geometry, spatial position, developmental time, visitor functional mode, or response stage.

## Competing rules

The hold-out batch will also record whether each result is equally explained by:

1. defence-strength-only;
2. chemical-versus-physical modality class;
3. consumer-taxonomic-identity-only.

No competing rule may be redefined after observing the hold-out outcomes.

## Hold-out universe

Primary empirical papers published **2020–2026** that were not already used to derive `COMPETING_HYPOTHESIS_FALSIFICATION_MATRIX_V1.md`.

Exclude the already-used derivation systems/programs:

```text
Catalpa
Pedicularis rex
Thunia alba
Codonopsis lanceolata
Chrysothemis friedrichsthaliana
Bejaria resinosa
Salvia miltiorrhiza
Polemonium 2PE threshold program
Asclepias cardenolide program
Nicotiana Kessler/Baldwin 2007, Kessler 2008, Kessler 2015
Gelsemium
Aconitum
Rivest/Lupinus pollen-alkaloid context program
```

## Fixed search classes

Search primary-source literature using these concept classes, with date restriction 2020–2026:

```text
1. floral defence pollinator antagonist manipulation flower barrier
2. floral chemical defence pollinator herbivore nectar manipulation
3. floral physical defence pollinator florivore barrier manipulation
4. nectar secondary metabolite pollinator antagonist experiment
5. flower trait pollinator herbivore access manipulation
```

Searches may use equivalent syntax required by the database, but the biological concepts may not be changed after seeing results.

## Eligibility gate

A study enters the hold-out validation only if all are true:

1. primary empirical study;
2. a flower-specific trait/manipulation can be operationally evaluated as D or as a candidate D;
3. the study measures an antagonist response and either a legitimate-pollinator response or a pollination/reproductive response relevant to pollinator function;
4. the D mechanism/access geometry is described sufficiently to classify a priori as `separated`, `overlapping`, or `bypass/tolerance` from the experimental architecture;
5. the system is independent of the derivation systems listed above.

Studies that fail the D gate remain failures and cannot be promoted because their outcome happens to fit the rule.

## Coding order

For each eligible study:

### Stage A — architecture code

Code from methods/manipulation description:

```text
predicted_state = separated | overlapping | bypass/tolerance | unclear
separating_coordinate = dose | susceptibility | attack_route | geometry | space | time | functional_mode | response_stage | other_declared
```

### Stage B — outcome code

Then record:

```text
antagonist_effect = reduced | null | increased | mixed
pollinator_effect = preserved/null | impaired | improved/routed | mixed
```

If architecture cannot be classified without using outcome information, code `unclear` and exclude that study from confirmatory success/failure scoring.

## Fixed success criterion

Do not use a p-value meta-analysis across incompatible outcomes.

The rule passes the first hold-out gate if:

```text
- at least 4 independent architecture-classifiable hold-out systems are recovered; and
- >= 75% of those systems match the pre-coded three-state prediction; and
- no single coherent fourth state appears in >= 2 independent systems that the rule cannot represent; and
- at least one recovered system is a genuine boundary/failure case rather than a selective-support case.
```

This threshold is a registered diagnostic rule, not a population-frequency claim.

If fewer than 4 eligible systems exist, verdict = `INSUFFICIENT_HOLDOUT_CAPACITY`, not PASS.

## Failure conditions

The domain rule is weakened if any of the following occurs:

1. two or more independent systems with clear pre-coded domain separation show strong pollinator interference while antagonist reduction remains effective, without another overlapping domain being identifiable;
2. two or more systems with clear domain overlap preserve pollination despite effective antagonist reduction and no susceptibility/route distinction;
3. a repeatable fourth state is required that cannot be represented as separation, overlap, or bypass/tolerance;
4. a simpler fixed competing rule predicts the hold-out systems at least as well without system-specific exceptions.

## Reporting boundary

Hold-out results will be reported separately from the derivation evidence. They will not be added retroactively to claim that the rule was preregistered before its discovery.
