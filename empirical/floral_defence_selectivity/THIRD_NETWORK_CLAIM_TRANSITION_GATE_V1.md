# Third-network claim transition gate v1

## Purpose

A real third network changes the evidence state even if its result is
null-compatible or opposite in sign. After the first eligible confirmatory run,
the project may not keep presenting the paper as though only two networks had
been tested.

This gate converts a **verified retained third-network bundle** into a
manuscript-update plan without editing the manuscript automatically.

## Production entry point

~~~bash
python scripts/plan_third_network_claim_transition.py \
  confirmatory_analysis_v1 \
  --source-dir frozen_confirmatory_inputs \
  --existing-network-archive-dir access-routing-letter-data-code-v1/data_archive \
  --output third_network_claim_transition.json
~~~

The command requires:

1. a completed confirmatory bundle;
2. a passing full-bundle SHA256 verification;
3. a recheck of the original frozen third-network source inputs;
4. a second recheck of the exact frozen Letter archive for the existing two networks,
   requiring equality with the archive provenance recorded in the confirmatory receipt;
5. production existing-network mode:
   `FROZEN_LETTER_ANALYSIS_ARCHIVE_V1`, validated against the exact frozen
   Letter analysis archive bytes and the canonical k=2 result;
6. an exact 40-character repository commit;
7. third-network confirmatory gate pass;
8. joint network count exactly 3.

Synthetic/development bundles cannot enter the production claim lane.

## Frozen common claim

Once the eligible third network has been analysed, the preregistered common
statement is:

> **The same standardized access-routing association has now been tested in
> three independently sampled visitor networks spanning three major visitor
> faunas.**

This statement reports the scope of the test. It does **not** say that all three
networks recovered the predicted direction.

## Direction-specific reporting

### Third effect positive

If the retained third-network effect is positive:

~~~text
claim_state = THREE_NETWORK_DIRECTIONAL_CONCORDANCE
~~~

when the k=3 receipt also records all three effects as positive.

Licensed reporting:

- state the exact `rho_T` and two-sided permutation `p_T`;
- state that all three observed network effects are positive;
- report the equal-network `rho_J3` and its permutation p-value.

Do not convert sign concordance into universal causality or a population-level
network mean.

### Third effect opposite

If the retained third-network effect is negative:

~~~text
claim_state = THREE_NETWORK_DIRECTIONAL_NONCONCORDANCE
~~~

The manuscript must state that the directional recurrence from the insect and
bird networks did **not** extend to all three networks. The third network remains
in the k=3 statistic and cannot be replaced.

### Third effect exactly zero

If the retained third-network rank effect is exactly zero:

~~~text
claim_state = THREE_NETWORK_ZERO_THIRD_EFFECT
~~~

Report the zero third effect and the k=3 result. Do not describe the third fauna
as directionally corroborating the prediction.

## No p-value selection rule

The third network is retained regardless of its p-value.

The planner reports the exact two-sided p-value but does not use p<0.05 as a
dataset-retention or manuscript-inclusion gate.

~~~text
positive + small p     -> retained
positive + large p     -> retained
opposite + small p     -> retained
opposite + large p     -> retained
zero                   -> retained
~~~

## Required manuscript updates

A real verified third-network analysis requires review of:

- manuscript title;
- Abstract;
- third-network Methods;
- third-network Results;
- k=3 joint Results;
- Discussion claim ceiling;
- Conclusion;
- Figure plan;
- cover letter;
- title-page counts and Data Accessibility;
- submission-scope state.

The planner emits these locations as structured update targets.

## Prohibited transitions

Even after k=3, do not claim:

- a population-level mean across all ecological networks;
- universal causality;
- estimated between-network heterogeneity from three networks;
- raw-observation pooling;
- a universal causal effect of one access trait;
- that an unfavorable third network can be omitted or replaced.

## Automation boundary

~~~text
automatic_manuscript_edit_permitted = false
~~~

The planner produces a claim contract, not a manuscript patch. A later
manuscript revision must cite and preserve the verified confirmatory receipt and
its direction.
