# B-to-P precision queue correction

## What Batch 0 exposed

The first precision-expansion queue ranked all shallow-screen priority records
from the B-to-P discovery corpus. It correctly preserved recall, but it did not
require both the archived `metadata_B_signal` and `metadata_P_signal` at queue
selection. The first 20 therefore contained corolla morphology, reward,
visual-signal, microbial, and community pollination studies whose titles or
queries matched but did not establish a barrier role.

This was a workflow-selection issue, not an empirical result.

## Corrected queue

The corrected B-to-P calibration queue requires:

```text
metadata_B_signal = true
metadata_P_signal = true
```

and then orders candidates by:

```text
abstract available first
non-review metadata first
original query rank
stable candidate ID
```

This is still only a discovery/triage rule. It does not classify a trait as B.
The source-screen gate remains:

```text
flower-specific chemical or physical trait
+ independently stated barrier/deterrence/access role
+ direct pollinator outcome
+ recoverable direction
```

## Why preserve the earlier queue

The initial artifact remains a valid record of what the original broader
selection returned. The corrected queue is a new, separately reproducible
source-screening order that better matches the B-to-P precision question.