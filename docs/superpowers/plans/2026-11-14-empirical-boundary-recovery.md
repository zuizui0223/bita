# Public-data architecture-boundary recovery implementation plan

Goal: Recover a real empirical contrast after the theoretical entry/benefit/persistence thresholds, without adding theory or mistaking genetic backgrounds for historical hysteresis.
Architecture: Manually source-check published Table 1 rescue IDs, validate against author-reported group totals, then recompute all-started-population binary contrasts. Retain a three-publication boundary ledger; no pooled meta-analysis.
Tech stack: Python >=3.10 standard library; pytest for verification.
Scope: New standalone files only, on an empirical branch based on BITA PR #363 head 6166870a. Manuscripts and existing theory remain unchanged.

Design decisions: Do not infer replicate-level growth measurements from a reported endpoint; do not digitize inaccessible figures. Use source counts rather than waiting for unavailable supplemental ZIP. Retain unresolved rescue mechanisms. Do not compare 2012 and 2026 as a controlled regime experiment, and do not require K(u) for evidence admission. Three publication records are not three independent taxonomic systems.

1. [ ] Freeze 2026 Table 1 route rows and aggregate denominators, with explicit publication/experiment identity and source locators. Supplement/raw assay access remains unavailable.
2. [ ] Write failing tests for validated inputs, totals, exact tests, interval endpoints, unresolved-route retention and claim boundaries.
3. [ ] Implement pure-standard-library extraction validator and exact Fisher/Wilson-Newcombe/Katz-RR/Holm readout. Tests must pass; compare to scipy/statsmodels independently locally.
4. [ ] Generate JSON and English/Japanese readout; add scope and nonexchangeability ledger. No shared-vs-split fitness or hysteresis effect may be claimed.
5. [ ] Publish additive Draft PR, verify uploaded bytes and full-repository CI at the actual head; no merge or submission.

Review focus: nonmutator mut+ is not mutator; table lists only positive-rescue populations; the one unresolved route is positive rescue; absence from endpoint table does not imply biochemical impossibility; WGS-only amplification evidence has no 48-population surveillance denominator.
