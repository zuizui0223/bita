# Paperization pass v1

This file converts the frozen scientific result into an editorial plan. It does not reopen analysis.

## Recommended title

**When are floral attraction and defence complementary? A one-sided mechanistic bound and cross-system patterns**

Why this is preferred over the current title:

- it places the strongest new result in the title rather than the generic phrase “mechanistic theory”;
- it avoids implying that every Part II component is a conventional meta-analysis;
- it remains readable to a broad ecological audience and makes the biological question primary.

A conservative alternative is the current title:

**When are floral attraction and defence complementary? Mechanistic theory and meta-analytic patterns across mutualists and antagonists**

Do not use “universal criterion”, “general law of complementarity”, or equivalent two-sided wording.

## Revised abstract candidate

Flowers must attract mutualists while limiting exploitation by antagonists, creating the possibility that attraction and defence either reinforce or obstruct one another. We ask when one focal attraction trait and one flower-specific antagonist-reducing trait are locally complementary, and which parts of that mechanism recur across biological systems. After an explicit orientation gate, their local mixed fitness effect can be organized as antagonist relief minus pollinator interference minus direct joint-cost curvature, `W_AD = rho - iota - kappa`. The decomposition itself is bookkeeping, but it yields a stronger one-sided result: when joint-cost curvature is non-negative, complementarity can occur only where antagonist relief exceeds pollinator interference. Across 2,592 declared evaluations and four response-shape variants we find no counterexample, whereas about 23% of points inside this selectivity window remain substitutable, so the window is necessary but not sufficient. A mechanism-first synthesis then maps 56 route-level records from 25 independent biological study clusters. Floral larceny reduces female fitness on average (log response ratio `-0.210`; 48 clusters), yet only 35/48 effects are negative, the 95% prediction interval spans `-1.13` to `+0.71`, and declared moderators explain only 0–8% of heterogeneity. Thus the constituent mechanisms and switching architecture recur, but their realized balance is strongly context dependent. Direct attraction × defence evidence remains sparse and direct joint-cost curvature unmeasured. The resulting theory is therefore a one-sided mechanistic bound, not a universal sign rule; the sign of joint-cost curvature is the minimal next test of its biological applicability.

## Main-text revision priorities

### 1. Introduction: shorten before strengthening

The current Introduction is scientifically sound but repeats the same inference gap through several formulations. The final version should reach the paper's distinctive question faster.

Target flow:

1. flowers simultaneously face mutualists and antagonists;
2. attraction can increase value and exposure, while defence can reduce antagonism and interfere with mutualists;
3. existing multivariate selection/fitness-surface theory identifies total cross-trait curvature but not its ecological channel allocation;
4. our question is therefore mechanistic: what balance determines the sign, and is any part of that balance structurally general?;
5. contribution: oriented decomposition → non-identifiability → one-sided bound → mechanism-first empirical Pattern.

Editorial target: reduce Introduction length by roughly 15–25% without removing prior-art citations or inference boundaries.

### 2. Make Theorem 1 the first unmistakable payoff

The paper should not make the reader wait through the finite-grid details to understand the strongest result. The theorem is algebraic and should be presented as such. Its importance is ecological, not mathematical difficulty:

- it converts a many-channel trade-off into a one-sided impossibility statement;
- it separates a necessary permissive window from the false sufficient rule;
- it identifies the exact type of biological assumption that can break the bound.

Keep the 2,592 evaluations as implementation verification and looseness diagnostics, not as the proof.

### 3. Separate three ideas in the Discussion

Use the compact triad:

- **discrimination** — can defence separate antagonist effects from pollinator interference?;
- **exposure** — are antagonist and pollinator pressures actually loaded strongly enough for discrimination to matter?;
- **affordability** — does simultaneous attraction and defence carry positive, zero, or negative joint cost?;

The selectivity window captures the first two channel magnitudes before joint cost is charged; `c_AD` supplies the affordability gate. This is a reader-facing interpretation, not a new fitted model.

### 4. Move search-history detail out of the narrative

Main text should retain only the registered inclusion logic, evidence levels, and saturation rule needed to interpret the synthesis. Detailed statements about individual source-access failures, historical search batches, promotion steps, or workflow evolution belong in the supplement/provenance layer unless they directly change an admitted inference.

The reader should see a deliberate synthesis design, not the chronology of repository development.

### 5. Keep the Leal result as an exposure-gate result

The female-fitness mean, prediction interval, robustness, and moderator failure are important because they show:

- antagonist pressure is not generically zero;
- the effect is repeatable at the pooled-direction level;
- realized state remains strongly system dependent;
- current coarse moderators do not solve new-system prediction.

Do not let the Leal module drift into a claim that it estimates `rho` or validates `W_AD`.

### 6. Keep Sasidharan secondary to the main logical arc

The Sasidharan reconstruction is useful support for shared consumer tracking and composition dependence, but it is not the paper's main quantitative payoff. In the final manuscript it should occupy less conceptual space than the one-sided theorem and H-gate result.

### 7. Tighten the Integration section

Section 6 currently contains the right content but repeats several boundaries already established in Methods/Results. The final discussion should be organized around four questions:

1. What became general? — the one-sided bound under its declared premise.
2. What recurs biologically? — constituent mechanisms and switching architectures.
3. What remains context dependent? — exposure and the realized balance inside the window.
4. What is the decisive next test? — the sign/magnitude of joint-cost curvature, followed separately by a full `A × D` calibration factorial.

### 8. Shorten the Conclusion

The final Conclusion should fit in three compact paragraphs:

- one-sided theorem and failed converse;
- recurrent but heterogeneous empirical Pattern;
- `c_AD` as generated falsification gate and the distinction between the cheap 2 × 2 cost test and hard full factorial.

Do not end on “more data are needed.” End on a specific falsifiable prediction produced by the theory.

## Reviewer-risk audit

### Risk A — “The theorem is mathematically trivial”

Expected response: agree that the proof is immediate. The claim is not mathematical sophistication. The contribution is extracting a form-robust ecological impossibility boundary from the mechanism decomposition, showing that the intuitive two-sided selectivity rule is false, and converting the boundary into a specific falsification experiment.

### Risk B — “The selectivity window is definitional or circular”

Expected response: the window is deliberately defined from the relief/interference balance before joint cost. It is not claimed to predict complementarity by itself. Its empirical and theoretical value comes from the one-sided implication and the identified failure mode, not from calling the ratio/region a new universal index.

### Risk C — “Part II does not estimate the theory parameters”

Expected response: correct, by design. Proposition 1 and the evidence hierarchy explain why marginal and same-system evidence cannot be relabelled as the total mixed partial. Part II tests recurrence, gate opening, conditionality, and identification gaps rather than pretending to calibrate `rho`, `iota`, `kappa`, or `W_AD`.

### Risk D — “The route ledger is not a meta-analysis”

Expected response: correct. The manuscript must call it a source-adjudicated cross-study Pattern scaffold. Meta-analysis is reserved for effect-compatible modules. This is one reason the recommended title uses “cross-system patterns” rather than describing the entire Part II as meta-analytic.

### Risk E — “The H-gate is too heterogeneous to be useful”

Expected response: the heterogeneity is part of the result. The gate is open on average, but its location varies and is not explained by the declared coarse moderators. This is precisely why the paper stops at a one-sided structural result rather than claiming prospective prediction from H alone.

### Risk F — “`c_AD` is assumed rather than measured”

Expected response: yes. The deployed non-negative parameterization is explicitly a premise, not established biology. The theorem identifies the premise's exact empirical vulnerability and reduces the first applicability test to a tractable 2 × 2 allocation experiment. A sufficiently negative cross-cost is a direct falsifier for the focal trait pair.

### Risk G — “Why Theoretical Ecology?”

The paper uses a compact theoretical mechanism to answer an ecological question, then tests the recurrence and limits of the derived architecture across systems. The final manuscript should prioritize biological interpretation and readability over additional algebra.

## Work that is complete and should not be reopened by default

- broad Pattern discovery and registered saturation;
- the 2,592-evaluation finite robustness design;
- the one-sided theorem and regression test;
- Leal primary pooled estimates and registered sensitivity family;
- Sasidharan 32-component dependence topology;
- direct-design and direct-joint-cost targeted exhaustion for the current claim set;
- main figure and supplementary reproducibility architecture.

## Remaining human-controlled items

These block external submission but not scientific paperization:

- final author order and publication names;
- affiliations and corresponding-author details;
- ORCIDs;
- CRediT roles;
- funding and acknowledgements;
- competing-interest confirmation;
- repository licence choice;
- archival release/DOI;
- reviewer suggestions/conflict checks;
- author-approved final rendered manuscript and supplement;
- authenticated journal-portal submission.
