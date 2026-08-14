from pathlib import Path

MANUSCRIPT = Path("manuscript/MANUSCRIPT_THEORETICAL_ECOLOGY.md")
WORKFLOW = Path(".github/workflows/_paperize-integration-tmp.yml")
SCRIPT = Path(__file__)

text = MANUSCRIPT.read_text(encoding="utf-8")

methods_start = text.index("### 4.1 Theory-to-pattern evidence map")
methods_end = text.index("### 4.2 Quantitative meta-analytic modules")
methods_block = r'''### 4.1 Theory-to-pattern evidence map

The empirical synthesis was organized around the four theory-derived marginal routes \(A\rightarrow\)pollination, \(A\rightarrow\)antagonism, \(D\rightarrow\)antagonism, and \(D\rightarrow\)pollination. Evidence was admitted only when the focal floral context, trait axis, response, and study identity could be source-adjudicated. Same-system evidence was tracked separately from unrelated marginal studies, and direct \(A\times D\) evidence required a distinct attraction axis, a flower-specific antagonist-reducing defence/access axis, and an interaction on a common outcome.

A registered expansion targeted empty or weakly replicated theory-facing cells rather than article count. New records were admitted as independent biological clusters under the same route and organ rules; studies lacking a clean focal \(A\) or flower-specific \(D\) were retained as context programs outside route-ledger N. Expansion stopped after two consecutive targeted screening batches yielded no new admissible Pattern class, and a parallel quantitative search yielded no additional synthesis with a distinct theory-facing axis.

Within-system changes were retained rather than averaged away. The coding ontology included trait intensity, resource or exposure context, consumer identity and function, response stage or scale, compound or mechanism identity, guarded defence, spatial or temporal filtering, attack mode, visitor functional-mode switching, lifecycle-stage role reversal, and population or trait-class dependence. Because the underlying outcomes are non-equivalent, we did not fit a cross-outcome grand moderator coefficient. Completion required explicit states for all four marginal routes, saturation of the direct-interaction and direct joint-cost searches, same-system linkage, mapped conditionality, two reproduced quantitative modules, explicit status for secondary contextual syntheses, and preservation of the inference boundary between constituent evidence and the theoretical mixed partial.

'''
text = text[:methods_start] + methods_block + text[methods_end:]

integration_start = text.index("## 6. Integration — from mechanism to pattern")
integration_end = text.index("## 7. Conclusions")
integration_block = r'''## 6. Integration — from mechanism to pattern

### 6.1 What generalizes is a one-sided window, not a sign rule

Part I gives the recurrent route-separation Pattern a precise role. Under non-negative joint-cost curvature, antagonist relief must exceed pollinator interference before complementarity is possible. Spatial, temporal, chemical, and attack-mode separation can therefore move a system into a permissive selectivity window, but they cannot by themselves determine the sign of \(W_{AD}\). The failed converse is essential: recurrent discrimination mechanisms identify where complementarity is allowed, not where it must occur.

Part II supplies the corresponding biology. Guarded states, consumer-specific barriers, attack-mode filtering, and shifts of the same visitor between legitimate pollination and robbery all alter the balance between \(\rho\) and \(\iota\). Floral larceny further shows that the antagonist-exposure gate is non-zero on average but strongly heterogeneous. Together, the theory and synthesis support a moving permissive window: the required mechanisms recur, while exposure and joint cost determine whether the permitted state is actually complementary.

### 6.2 Recurrence does not identify total curvature

Part II provides constituent-path evidence and does not calibrate \(W_{AD}\). The Leal and Sasidharan modules, the secondary contextual syntheses, and the same-system route panel establish recurrent biological channels and switching states, but none is algebraically equivalent to the focal attraction-defence mixed partial. This is the empirical counterpart of Proposition 1: more observations of total fitness or more unrelated route studies cannot recover channel allocation without linked measurements or interventions on the same focal traits.

The sparse direct layer therefore identifies two distinct empirical gaps. Total \(W_{AD}\) requires a focal attraction × defence design on a common outcome; the strict total-outcome candidate remains sign-unresolved, while crossed floral-trait evidence shows consumer-context-dependent channel interactions without identifying total curvature. Direct joint-cost curvature has zero strict estimates in the admitted evidence layer, so \(\kappa\) remains unidentified, not zero. Under the one-sided theorem, a negative joint-cost curvature is the only escape route from the selectivity window in the declared family, and it must be sufficiently negative relative to the relief-interference difference.

The framework is related to correlational selection rather than a replacement for it. On suitable standardized trait and relative-fitness coordinates, \(W_{AD}\) may correspond to a correlational-selection term; the contribution here is the ecological allocation and inference boundary attached to that curvature. Predictions about trait covariance, genetic correlation, evolutionary trajectories, or equilibria still require genetic architecture, inheritance, constraints, and dynamics beyond the local mixed partial.

### 6.3 Context moves the window as a joint ecological state

The environmental analysis likewise yields a balance, not a verbal rule that more antagonists must favour complementarity or more pollinators must favour substitutability. In the larceny synthesis, antagonist exposure reduces female fitness on average, yet the prediction interval spans both signs and the declared moderators explain little of the heterogeneity. The current context axes therefore do not locate the selectivity window reliably in a new system.

Antagonist exposure also reduces legitimate visitation, showing that realised \(H\) and \(P\) need not be independent. In the separable corollary, allowing \(P\) to decline with \(H\) adds a positive correction to \(\partial W_{AD}/\partial H\) because the pollinator-interference channel weakens while antagonist relief is loaded. This makes the separable result conservative in direction for that specific coupling, but it does not calibrate the total derivative or justify a general regime prediction. Prospective applications should therefore measure exposure and channel responses jointly rather than treat a named pressure variable as a sufficient context descriptor.

### 6.4 Falsification before calibration

The one-sided theorem changes the empirical order of operations. A **2 × 2 allocation** design — neither focal trait, attraction only, defence only, and both — can first test the sign of direct joint-cost curvature using an appropriately defined construction, resource, or physiological cost. A sufficiently negative cross-cost would falsify the one-sided bound for that focal trait pair without requiring pollinators, antagonists, or total-fitness measurement.

A separate **full attraction × defence factorial** has a harder purpose: estimating total \(W_{AD}\) and its channel allocation. That design must manipulate the two focal traits in the same biological units and measure compatible mutualist contribution, antagonist loss, direct cost, and total fitness. The remaining unknowns are therefore no longer open-ended gaps inside the present argument. They are two explicit next tests: a cheap applicability/falsification gate followed, when needed, by full mechanistic calibration.

'''
text = text[:integration_start] + integration_block + text[integration_end:]

MANUSCRIPT.write_text(text, encoding="utf-8")

# This transformer is intentionally self-cleaning: it exists only to make one
# exact editorial update through GitHub Actions, then disappears from the tree.
if WORKFLOW.exists():
    WORKFLOW.unlink()
if SCRIPT.exists():
    SCRIPT.unlink()
