# Target journal strategy — one-sided Mechanism → Pattern paper

## First target

**Theoretical Ecology — Regular Article**

Canonical title:

> **When are floral attraction and defence complementary? A one-sided mechanistic bound and cross-system patterns**

## Why the paper fits

The submission is built around an ecological question rather than a mathematical object: when do floral attraction and flower-specific antagonist reduction reinforce rather than obstruct one another?

The paper has two linked but inferentially distinct parts:

> **Part I — Mechanism:** derive the local channel balance, non-identifiability boundary, and the one-sided selectivity theorem.
>
> **Part II — Pattern:** ask which mechanism-derived routes and switching architectures recur across systems, using quantitative synthesis only where effect scales are compatible.

The central theoretical contribution is not the mixed partial itself and not the bookkeeping identity

```text
W_AD = rho - iota - kappa
```

but the stronger one-sided result:

```text
if kappa >= 0 and W_AD > 0, then rho > iota
```

Thus complementarity cannot occur outside the selectivity window under the declared premise. The converse is false. Across 2,592 declared evaluations there are zero counterexamples to the forward implication, while window precision is 77.2%.

## Empirical role

Part II is not presented as validation or calibration of total `W_AD`. Its role is to establish what is recurrent, what switches with context, whether the antagonist-pressure gate is open in nature, and which parameters remain unidentified.

Canonical Pattern state:

```text
56 route-level records
25 independent biological study clusters
A -> pollination:         5
A -> antagonism:          8
D -> antagonism:         18
D -> pollination:        10
same-system multi-route: 14
context/sign-switch:     17
context-only programs:    7  (excluded from route-ledger N)
```

The Leal floral-larceny module shows an average antagonist-pressure cost but strong system dependence: female-fitness LRR about `-0.210` across 48 clusters, 35/48 negative, prediction interval about `-1.13` to `+0.71`, and declared moderators explaining only 0–8% of heterogeneity.

The paper therefore supports:

> **a one-sided mechanistic theorem plus recurrent but context-dependent empirical Pattern**

not a universal positive or negative sign of `W_AD`.

## Strongest novelty position

The manuscript should foreground five contributions, in this order:

1. **one-sided selectivity bound** — a necessary permissive region rather than a two-sided sign criterion;
2. **exact failure mode** — sufficiently negative joint-cost curvature is the unique escape route from the bound in the declared family;
3. **tractable falsification gate** — a 2 × 2 joint-allocation experiment can test the sign of the decisive cost interaction before a harder full fitness factorial;
4. **mechanism-facing inference architecture** — antagonist relief, pollinator interference, and joint cost are kept distinct after an explicit orientation gate, with total-fitness non-identifiability made explicit;
5. **Mechanism → Pattern synthesis architecture** — incompatible outcomes are not forced into one grand effect, while recurrence, same-system linkage, switching, and direct-identification gaps are mapped separately.

Do not claim novelty for correlational selection, cross-trait curvature, attraction exposing plants to antagonists, defence carrying pollination costs, pollinator–herbivore nonadditivity, or context dependence itself.

## Reviewer-risk positioning

### “The theorem is mathematically immediate.”

Agree. The contribution is ecological: extracting a response-shape-robust impossibility boundary, rejecting the intuitive two-sided rule, and identifying the specific biological assumption that can break the bound.

### “The selectivity window is circular.”

It is defined from relief versus interference before joint cost is charged and is **not** claimed to predict complementarity by itself. Its value is the one-sided implication and falsifiable failure mode.

### “Part II does not estimate the theory parameters.”

Correct and intentional. Proposition 1 and the evidence hierarchy prohibit relabelling marginal route evidence as `rho`, `iota`, `kappa`, or total `W_AD`.

### “The route ledger is not a meta-analysis.”

Correct. It is a source-adjudicated Pattern scaffold. Meta-analysis is reserved for effect-compatible modules.

### “The H-gate is too heterogeneous for prediction.”

The heterogeneity is the result: the gate can be open on average but its realised state varies, and current coarse moderators do not locate the window reliably in a new system.

### “`c_AD` is assumed rather than measured.”

Correct. Non-negative joint cost is a declared premise, not established biology. The theorem identifies exactly how to falsify its applicability for a focal trait pair.

## Editorial priorities before external submission

1. keep the title and Abstract centered on the one-sided bound;
2. keep the Introduction short enough that Theorem 1 arrives as the first clear payoff;
3. preserve the distinction between structural theorem, finite-grid verification, and empirical Pattern;
4. avoid allowing the Sasidharan or secondary contextual modules to dominate the paper's main arc;
5. keep the Discussion organized around what became general, what recurs, what remains context dependent, and what experiment comes next;
6. end on the 2 × 2 falsification gate versus the full `A × D` calibration factorial, not generic calls for more data.

## Submission cascade

Current order:

```text
scientific freeze
→ repository cleanup / claim freeze
→ reader-facing manuscript paperization
→ synchronized portal metadata and cover letter
→ final rendered-file QA
→ author-controlled metadata/declarations/reviewer/licence completion
→ immutable release + archival DOI
→ final release-commit CI/export
→ authenticated Theoretical Ecology submission
```

No additional broad evidence search is a default prerequisite for submission.
