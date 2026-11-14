# BITA reversible-environment continuation plan

> Execute inline; this is a continuation of author-requested BITA theory work.

**Goal:** Test whether the already-specified startup model permits different entry and persistence thresholds; do not add biological data or alter the active Letter.
**Architecture:** Add a standard-library equilibrium/threshold calculator, an executable readout, regression tests and a source-bounded interpretation. Import the frozen sharp-threshold module unchanged.
**Tech Stack:** Python >=3.10, pytest; independent local mpmath/SciPy checks only.
**Spec:** Existing gain d²[2hu-(h+lambda)u²]-c[1-exp(-u/tau)], u in [0,1]. Keep weights/cost/tau fixed while varying d. Interpret paths only under explicitly added quasi-static projected-gradient dynamics.

## Constraints and alternatives
No population genetics, historical-origin claim, manuscript edit or main merge. A fresh empirical test would need source access and measured histories; existing source-audited data lack this counterfactual. Use an analytic bifurcation calculation rather than a forward-only walk (which cannot test reversal) or a coarse scan that can miss narrow equilibria. This implementation choice is the assistant's, under the user's instruction to proceed.

## Review focus
Near-fold degeneracy must not be assigned strict stability; underflow must not imply a zero fold; no hysteresis for tau>=s; zero-cost case is a negative control; different starting states require a declared dynamic law rather than treating a global optimum as a trajectory.

## Tasks
- [ ] Test first: exact fold values, derivative/curvature identities, equilibrium roots, basin dependence, continuous/zero-cost controls, scaling and numerical boundaries. Observe failure for missing module.
- [ ] Implement `trait_architecture/startup_hysteresis.py`; rerun these and the previous 31 tests.
- [ ] Generate `scripts/analyze_startup_hysteresis.py` and frozen JSON, with exact thresholds plus slow continuation. Independently check derivatives/roots with high precision and two-sided projected gradient integration.
- [ ] Write the proof and observable predictions; mark original-data meta evidence as untested, not synthetic replication. Verify final diff, push only additive files to existing Draft #363, and inspect full-repository CI at the exact commit.
