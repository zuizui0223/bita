# BITA Submission Candidate V1

## Status

~~~text
scientific package:          READY
analysis reproducibility:    VERIFIED
four main evidence layers:   FROZEN
two-network validation:      VERIFIED
main figures:                READY
Ecology Letters proposal:    READY
external proposal email:     NOT SENT
old canonical manuscript:    PRESERVED
PR #224:                     OPEN / DRAFT
~~~

## Verified analysis state

Code/tests/package head:

~~~text
81a5186e543dc68180acabcdfe722b40fd0df1ca
~~~

At that head:

- CI: SUCCESS;
- submission-scope: SUCCESS;
- legacy submission-package guard: SUCCESS;
- effective-domain state recovery: SUCCESS;
- Sakhalkar network: SUCCESS;
- Sakhalkar multitrait sensitivity: SUCCESS;
- Aubert Dryad audit: SUCCESS;
- Aubert Zenodo mirror audit: SUCCESS;
- Aubert all-Ecuador access-barrier extension: SUCCESS;
- Figure 1–3 build: SUCCESS;
- two-network Figure 4 build: SUCCESS.

The Aubert workflow reproduced the frozen aggregate result exactly after the proposal-requirement tests were added.

## Main ecological package

### Layer 1 — route-level D macro corpus

~~~text
17 unique D study programs
chemical 9 / physical 7 / reward-access 1
10 same-study pollinator follow-ups
~~~

Pollinator states among those ten:

~~~text
context-dependent 4
null-compatible 3
improved 1
interference 1
unresolved 1
~~~

### Layer 2 — effective-domain matched-system recovery

~~~text
historical scorable: 9 / 9 aligned
systematic expansion: 2 / 2 aligned
pooled scorable: 11 / 11 aligned

coarse modality comparator:
  historical LOO: 6 / 9
  expansion:      1 / 2
~~~

Strict direction-supported Stage-2 remains descriptive only:

~~~text
n = 3
Fisher p = 0.333
~~~

### Layer 3 — within-D conditionality

~~~text
8 independent state-switch systems
~~~

Axes include dose/expression, cumulative exposure, consumer identity, response stage and timing.

### Layer 4 — independent network routing

Sakhalkar insects:

~~~text
n = 57 species
rho = 0.346786
permutation p = 0.0086
~~~

Aubert/EPHI birds:

~~~text
18 Ecuador sites
1,378 bird × plant × site units
barrier robbery = 0.30698
accessible robbery = 0.08139
difference = +0.22560
permutation p = 0.0001
15 / 17 comparable sites positive
site-stratified permutation p = 0.0001
~~~

The two network effect sizes are not pooled.

## Main manuscript

Candidate source:

`manuscript/MANUSCRIPT_FLORAL_DEFENCE_SELECTIVITY_V0.md`

Approximate current main-text source length:

~~~text
~5,780 words before final bibliography / journal styling
~~~

Main figures:

1. effective-exposure theory;
2. D-route macro landscape + matched-system recovery;
3. within-D state switching;
4. two-network access routing.

## Ecology Letters proposal package

Proposal:

`submission/ECOLOGY_LETTERS_SYNTHESIS_PROPOSAL_V0.md`

Current proposal body:

~~~text
277 words
official maximum = 300
status = PASS
~~~

Email draft:

`submission/ECOLOGY_LETTERS_SYNTHESIS_PROPOSAL_EMAIL_V1.md`

Required recipients:

~~~text
ecolets@cefe.cnrs.fr
ecolets2@cefe.cnrs.fr
~~~

Proposal requirement guard:

`tests/test_ecology_letters_proposal.py`

It checks:

- <=300 words;
- nature / novelty / disciplinary contribution;
- author qualification;
- both editorial addresses;
- current two-network evidence;
- no false invitation/submission claim.

## Claim ceilings retained

Do not claim:

- natural prevalence from the screened literature corpus;
- null-compatible = no pollinator cost;
- domain > modality from strict n=3;
- causal network effects;
- tube length as a uniquely identified driver in Sakhalkar;
- exact replication of Aubert et al. 2026;
- one pooled effect size across the two networks;
- universal q or tau values.

## Legacy BITA preservation

The V1 submission candidate does not overwrite:

- `manuscript/MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md`;
- 56-route / 25 historical cluster-label evidence;
- direct A×D systems;
- Kessler bounds;
- partial-identification framework;
- intervention / separability logic;
- larceny synthesis;
- supplementary A-side signal-leakage result.

## External-action boundary

No email has been sent.

No merge to main has been performed.

No canonical manuscript has been replaced.

The next external action is the Ecology Letters Synthesis proposal email, which remains gated on an explicit send instruction.
