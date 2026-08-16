# Reviewer A–F merge gate

Merge this correction only when all of the following are green on the final PR head:

- core CI on Python 3.10 / 3.11 / 3.12;
- `submission-scope` including required Leal paths;
- canonical Leal larceny module offline recomputation and committed-output diffs;
- Leal REML + modified Hartung-Knapp sensitivity from the local canonical contributing effects;
- claim-freeze regressions for the kappa-only theorem premise, proof-versus-grid Abstract wording, overlapping Pattern annotations, dual-provider AI disclosure, and Sasidharan composition boundary;
- existing manuscript/figure/supplement checks triggered by the changed files.

A green gate means the correction restores reproducibility and narrows/strengthens inference without changing frozen numerical results.
