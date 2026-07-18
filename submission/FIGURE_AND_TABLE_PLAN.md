# Figure and table plan for Theoretical Ecology submission

## Main-text figures

### Figure 1. Mechanistic architecture of the local attraction–defence interaction

**Purpose:** show the biological question before the algebra.

**Panel A:** one declared attraction trait `A` affects mutualist service and antagonist exposure.

**Panel B:** one declared flower-specific defence/access-limitation trait `D` reduces antagonist damage but may interfere with legitimate pollinator use.

**Panel C:** attraction and defence may also generate direct joint-cost curvature.

**Panel D:** local balance

```text
W_AD = antagonist relief - mutualist interference - direct joint-cost curvature.
```

**Caption draft:**

> Figure 1. Mechanistic routes contributing to the local interaction between one focal floral attraction trait and one focal flower-specific defence/access-limitation trait. Attraction may increase mutualist service while also increasing antagonist exposure. Defence may reduce the antagonist loss associated with attraction, but the same focal trait may interfere with legitimate pollinator use. Attraction and defence may additionally interact through direct construction, allocation, or physiological costs. After the orientation conditions are established, these routes contribute antagonist relief (`rho`), mutualist interference (`iota`), and direct joint-cost curvature (`kappa`) to the local mixed partial `W_AD = rho - iota - kappa`. The diagram does not imply that all routes occur in every system or that the component curvatures are identifiable from total fitness alone.

### Figure 2. Conditional sign regimes in the implemented corollary

Use the existing generated SVG from `scripts/build_part_i_regime_figure_svg.py` as the source. Do not redraw values manually.

**Purpose:** illustrate that opposite sign-dominant regimes arise under contrasting channel strengths while response-shape agreement can remain high within a fixed biological scenario.

**Caption draft:**

> Figure 2. Finite sensitivity of the local attraction–defence mixed partial in the endpoint-normalized implemented corollary. The declared design evaluates local attraction and defence coordinates, exogenous pollinator-service and antagonist-pressure indices, an auxiliary reproductive-assurance moderator, four biological parameter scenarios, and four endpoint-normalized response-shape variants. Contrasting scenarios produce sign-dominant complementary and substitutable regimes. Counts and percentages describe occupancy of the declared finite tested set only; they are not estimates of the prevalence of either sign in nature. Response-shape unanimity is evaluated within fixed biological scenarios, whereas the full tested set deliberately combines scenarios with opposing route strengths.

## Main-text tables

### Table 1. Definitions and inference boundaries

| Symbol | Meaning | Required declaration | Does not imply |
|---|---|---|---|
| `A` | one focal attraction trait | measurement and orientation | omnibus floral attractiveness |
| `D` | one focal flower-specific defence/access trait | antagonist-reduction role and measurement | any trait that merely blocks pollinators |
| `W` | fitness or biological-outcome scale | units, transformation, ecological context | transformation-invariant fitness |
| `W_AD` | local mixed partial | focal coordinates and point | trait covariance, optimum, trajectory |
| `rho` | antagonist-relief magnitude | orientation gate | total defence benefit |
| `iota` | mutualist-interference magnitude | orientation gate | total pollination cost |
| `kappa` | direct joint-cost curvature | cost-channel definition | total energetic cost |

### Table 2. Canonical finite sensitivity design and results

Include only values generated from the canonical readout:

- coordinates for `A`, `D`, `P`, `H`, and auxiliary `R`;
- number of biological scenarios;
- number of response-shape variants;
- 2,592 total evaluations;
- sign counts;
- within-scenario response-shape agreement;
- full-tested-set agreement;
- numerical zero tolerance and minimum absolute mixed partial.

Do not include a column labelled probability, prevalence, support, or frequency in nature.

## Supplementary figures and tables

### Figure S1
Analytic versus finite-difference derivative agreement for each endpoint-normalized response-shape variant.

### Figure S2
Scenario-specific sign maps separated by response-shape variant.

### Table S1
Complete parameter definitions, values, units or dimensionless scaling, and biological interpretation.

### Table S2
All 162 local cases and the four-scenario × four-shape classification summaries.

### Table S3
Preliminary literature route records, clearly labelled as abstract-level context and not quantitative validation.

## Production rules

1. Generate figures only from committed scripts and canonical inputs.
2. Record the exact commit SHA used for final exports.
3. Export vector PDF or EPS for submission and retain SVG as the reproducible source.
4. Use consistent symbols with the manuscript: `rho`, `iota`, and `kappa`.
5. Never display 51.8% and 48.2% without “unweighted finite-grid occupancy” in the same panel or caption.
6. Keep `R` visually subordinate and label it as an auxiliary moderator.
