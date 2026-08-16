# Leal module canonicalization note

The Leal et al. (2025) larceny analysis was originally completed on immutable provenance commit `ed33b25593c0d90ad6657753f6f5501d9efc7b82`. The manuscript later retained its numerical results while the full analysis subtree was absent from the canonical main tree.

This correction imports the already-admitted module into the current canonical repository without changing its effect rows, moderator coding, pooled results, context-dependence results, or inference boundaries.

The immutable commit remains the provenance anchor. The current tree is now the submission/reproduction anchor.

This distinction is deliberate:

- **provenance anchor:** where the admitted module was originally frozen;
- **canonical reproduction anchor:** the current submission tree that contains the source-derived effect rows, code, results, tests, and declared strata required to rerun it offline.

No claim should again depend solely on reachability of a closed historical branch.
