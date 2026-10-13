# Ecology Letters Letter figure plan v0

Candidate manuscript:

manuscript/MANUSCRIPT_ACCESS_ROUTING_LETTER_V0.md

Target:

~~~text
article type: Letter
main figures: 3
journal maximum display items: 6
~~~

## Figure 1 — Higher robbery share can arise by different biological routes

Purpose: make the non-identifiability concrete before any dataset-specific result.

### Panel A — baseline

Use schematic counts only:

~~~text
legitimate = 90
robbery = 10
robbery share = 10%
~~~

### Panel B — numerator-driven increase

Keep legitimate use fixed and increase robbery:

~~~text
legitimate = 90
robbery = 45
robbery share = 33%
~~~

### Panel C — denominator loss

Let legitimate interaction collapse while robbery does not increase:

~~~text
legitimate = 10
robbery = 8
robbery share = 44%
~~~

The critical visual point is that robbery prevalence rises even though robbery itself
falls from 10 to 8.

### Panel D — Ecuadorian reach-scenario sensitivity

Show all four access definitions, not a preferred multiplier as the single headline:

~~~text
reach / culmen    legitimate RR (95% CI)    robbery RR (95% CI)      descriptive RR ratio
1.00 bill-only    1.883 (1.111–3.190)       0.463 (0.147–1.461)      0.246 (0.070–0.869)
4/3  corrected    0.354 (0.197–0.635)       0.851 (0.328–2.212)      2.406 (0.862–6.720)
1.80 corrected    0.154 (0.087–0.271)       0.816 (0.358–1.860)      5.311 (1.923–14.672)
2.00 corrected    0.100 (0.065–0.155)       1.393 (0.729–2.663)     13.876 (6.504–29.603)
~~~

The uncorrected 1.00× condition is the frozen preregistered anatomical bill-length proxy, **not** a second validated functional-reach estimate: tongue extension makes exposed culmen incomplete. Do not delete it; show its legitimate-rate sign reversal. The three corrected values are **post-open assumptions**, not species-specific physiological measurements for all 49 hummingbird species.

Label the invariant **within the 4/3–2.0× scenario set**: all legitimate CIs exclude 1 in the reduction direction, while all robbery CIs include 1 (unresolved rate direction). The descriptive RR-ratio range is 2.41–13.88; the 4/3 ratio interval includes 1. Per-scenario jackknife intervals exclude multiplier uncertainty, and route-specific fixed-effect fits have different positive-margin supports. This panel cannot identify a common-risk-set substitution, individual switching or the fraction of P1 prevalence due to either route.

The schematic A–C counts are illustrations; D reports observational Ecuadorian model contrasts, not an algebraic P1 decomposition.

Main message:

> observed robbery share cannot identify absolute route changes; the decline in legitimate feeding is consistent across specified tongue-reach scenarios but depends on replacing the incomplete bill-only barrier definition.
---

## Figure 2 — Robbery share versus route-specific participation

Use the existing two-network public-data figure as the base.

### Panel A — Aubert / EPHI birds: primary test

~~~text
primary n = 259 plant species
plant-level mismatch rho = 0.5032
permutation p = 0.0001
paired plant barrier contrast = +0.0915 across 130 species

consumer-grain behavior:
36 bird species with both barrier states
mean within-bird barrier contrast = +0.0933
label-swap p = 0.0001
28 bird species / 1,285 bird×plant dyads
within-bird centered-rank rho = 0.3398
within-bird permutation p = 0.0001

descriptive pair-site scale:
n = 2,265
barrier robbery = 0.147
accessible robbery = 0.020

zero-inclusive participation layer:
trait-matched opportunity edges = 19,909
culmen-only pooled RR = 1.7717 (95% CI 1.1050–2.8405)
post-open 4/3–2.0× effective reach:
  legitimate RR = 0.100–0.354 (all 95% CIs exclude 1)
  robbery RR = 0.816–1.393 (all 95% CIs include 1)
  descriptive separately fitted RR-ratio range = 2.41–13.88
  4/3× ratio 95% CI = 0.862–6.720 (includes 1)
  bill-only RR legitimate = 1.883 (direction reversed)
~~~

### Panel B — site robustness

~~~text
18 comparable sites
18 positive barrier effects
sign-test p = 7.63e-6
site-stratified permutation p = 0.0001
~~~

Main message:

> in Ecuador, corrected reach scenarios consistently estimate lower legitimate use while robbery-rate direction is unresolved; the insect network independently corroborates only the routing association.

---

## Figure 3 — One standardized cross-network routing test

Purpose: make the new Letter contribution visually unmistakable.

### Panel A — network rank effects

Show three aligned estimates:

~~~text
Aubert/EPHI birds — primary:
  plant-species rho = 0.5032
  n = 259 plant species

Sakhalkar insects — corroborative:
  rho = 0.3468
  n = 57 plant species

equal-network Fisher-z joint:
  rho_J = 0.4282
  permutation p = 0.0001
~~~

Do not draw pseudo-confidence intervals that have not been estimated.

### Panel B — permutation logic

Show:

~~~text
Sakhalkar:
  shuffle response across species

Aubert:
  shuffle response ranks across plant species
  after within-species aggregation

joint:
  equal network weight
~~~

### Panel C — what direct studies can identify

Show the post-hoc design audit of the frozen 33-program direct frame:

~~~text
7  strict zero-inclusive both-route rates
18 robbery-prevalence-only
6  conditional route choice
1  both-route counts without verified common zero denominator
1  other route-resolved but not both-route-rate identifiable
~~~

Label this explicitly as a **post-hoc finite-frame design audit**, not a prevalence estimate for the broader literature and not an increment to standardized network \(k\).

Main message:

> the Ecuadorian analysis addresses an estimand that most programs in the frozen direct frame do not identify: which absolute route changes under the observed prevalence shift.

## Supplementary figure routing

Move detailed macro-paper material to Supporting Information:

- full 17-system state matrix;
- strict Stage-2 exact table;
- full eight-system conditionality tracks;
- Kessler identification bridge;
- legacy identified-set / intervention figures.

The Letter should not visually reopen the mechanism-identification paper.
