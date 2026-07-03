## What
Splits the empirical program into Part A (math, unchanged) and Part B
(meta-analysis as *support*, not proof). Part B pools the four marginal arrows
(b_A, d_A, e_F, c_D) separately from their own literatures, so independence is
counted per-arrow — resolving the fixed-corpus collapse (17,933 → 0 poolable).

## Layers (all implemented + tested)
- B1 direction map / B2 per-arrow envelopes (reuse broad_meta_analysis)
- B3 moderator/conditionality engine (part_b_moderator.py)
- B4 break-even bound on the unmeasured c_AD (part_b_support.py)
- B5 evidence synthesis + regime-leverage priority queue (part_b_arrow_evidence.py)
- One reproducible pipeline: part_b_pipeline.py / scripts/run_part_b_support.py

## Result on real data (PART_B_RESULTS_READOUT_v1.md)
- c_D has B1 directional support (3 clusters, 100% compatible)
- 5 verified single-cluster anchors span the 4 arrows; none poolable yet
- d_A is the contested, highest-leverage crux (Impatiens −0.09 vs Gymnadenia
  +0.57; leverage +0.67) → B5 recommends coding the pollination_generalization
  moderator, scaffolded in D_A_MODERATOR_CODING_PROTOCOL_v1.md

## Boundary
Support for the theorem's conditionality, not joint-panel (D1/D2) identification.
Scale/design separation and honesty prohibitions retained; c_AD bounded, never estimated.
