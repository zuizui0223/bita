# BITA exact startup thresholds implementation plan

## Design
Continue Draft #363 from c30aa3331eceaa657f779626ff2d2efdf22a0b18.
Goal: turn the existing exact exponential-cost feasibility result into reproducible critical cost and conflict-distance bounds without new biological assumptions.
Choose a normalized analytic bracket rather than a grid optimizer: with r=tau/s, v=u/s, Q(v)=v(2-v)/(1-exp(-v/r)), the unique positive maximum lies in (1-r,1) for r<1; for r>=1 the maximum is the limit Q(0)=2r. Standard-library bisection and a small-argument series avoid grid dependence and cancellation. Float-unresolved windows must not be labeled absent.
Non-goals: modifying manuscripts, natural data, existing landscape code, statistical evidence counts, or main; no genetic fixation or empirical calibration claim.

## Tasks and gates
1. Add tests/test_startup_thresholds.py: pinned 60-digit independent reference values, r>=1 exclusion, scaling invariance, 540-cell count concordance, inputs that must fail, small-r and r≈1 resolution behavior. Run before production file exists and record failure.
2. Add trait_architecture/startup_thresholds.py with startup_cost_window and conflict_distance_thresholds. Run tests; independently verify with mpmath and source-equation gains.
3. Add scripts/analyze_startup_thresholds.py, a JSON readout and mathematical note. Include the two thresholds and finite-jump-vs-continuous boundary, and explicitly retain all empirical limits.
4. Commit additive files to existing draft branch only via GitHub connector; validate readback, full repository CI and unchanged manuscript/main.

## Environment ruling
Direct GitHub git clone failed because the container cannot resolve github.com. Use connector reads/writes and a private local scratch directory; do not claim a full local checkout. Full repository verification must run in GitHub Actions. No subagent tool is available: perform self-review plus an independent high-precision numerical oracle, without calling it independent scientific review.
