# Manuscript audit v2: implementation-to-claim check

## Scope

This audit compares the canonical manuscript against the active theory API, canonical sensitivity readout, submission scope, and supplement manifest. It is a pre-submission claim audit, not a new analysis.

## Verified alignments

### Focal quantity

The manuscript definition

```text
W_AD = d2W / dA dD
```

matches the active theory contract. It is correctly treated as a local mixed curvature on declared trait and outcome coordinates, not as a covariance, genetic correlation, optimum, or evolutionary trajectory.

### Signed decomposition

The manuscript identity

```text
W_AD = M_AD - G_AD - C_AD
```

matches the signed bookkeeping layer. The text correctly states that biological labels do not determine component signs and that total `W` does not identify the channel curvatures.

### Orientation gate

The manuscript conditions

```text
M_AD <= 0
G_AD <= 0
C_AD >= 0
```

match the active `OrientedSignCriterion`. The corresponding magnitudes are

```text
iota  = -M_AD
rho   = -G_AD
kappa =  C_AD
```

and the implemented criterion is

```text
W_AD = rho - iota - kappa.
```

### Environmental derivatives

The manuscript equations match `RegimeDerivativeBalance`:

```text
dW_AD/dH = rho_H - iota_H - kappa_H
dW_AD/dP = rho_P - iota_P - kappa_P.
```

The manuscript must state the explicit directional inequalities, not only refer to a corresponding condition:

```text
dW_AD/dH > 0 iff rho_H > iota_H + kappa_H
dW_AD/dP < 0 iff iota_P + kappa_P > rho_P.
```

Equalities define local environmental break-even conditions. Reverse inequalities reverse the direction.

### Finite sensitivity results

The manuscript numbers agree with the canonical `endpoint_normalized_grid_v2` readout:

- 2,592 total evaluations;
- 1,342 complementary;
- 1,250 substitutable;
- 0 numerically neutral;
- 480 of 648 fixed case × scenario summaries unanimous across the four response shapes;
- 168 mixed or sensitive;
- 0 of 162 local cases unanimous across the deliberately heterogeneous full tested set.

The current wording correctly treats these values as finite-design diagnostics rather than empirical frequencies.

## Required manuscript corrections before submission

### 1. Define the admissible scope of `D`

The phrase “defence or access-limitation trait” is too broad unless qualified. A focal `D` is admissible only when it has a declared flower-specific antagonist-reduction role. A structure that only obstructs pollinators is not sufficient to instantiate the complete defence mechanism.

Recommended sentence:

> We use defence/access limitation only for a focal flower-specific trait with an operationally defined antagonist-reduction role; collateral obstruction of legitimate pollinators is a possible effect of that same trait, not the definition of defence.

### 2. Use one cost term consistently

Use **direct joint-cost curvature** throughout. Avoid switching among “shared cost”, “joint cost”, “allocation trade-off”, and “construction cost” as if they were interchangeable. Direct construction, allocation, and physiological costs are possible biological sources of the mathematical term, but the theoretical object is `C_AD`.

### 3. State environmental inequalities explicitly

The present prose correctly rejects universal pressure effects but should display the exact inequalities above. This is a core analytical contribution and should not be hidden in prose.

### 4. Distinguish local complementarity from positive marginal effects

`W_AD > 0` means that one trait increases the marginal effect of the other. It does not require either first derivative, `W_A` or `W_D`, to be positive. Add this sentence to prevent “complementary” from being read as “both beneficial”.

### 5. Tighten the non-identifiability claim

Proposition 1 is valid. The manuscript should emphasize that the reallocation argument proves structural non-identifiability from total `W`, even with noiseless and complete observation of the total surface. It does not prove that mechanisms are unidentifiable after channel-specific interventions or structural restrictions.

### 6. Limit the literature claim

The active literature registry is abstract-level, single-coder, and has no eligible quantitative effect rows. It may motivate route plausibility only. Do not call it a systematic review, meta-analysis result, empirical validation, or calibration dataset in the manuscript or cover letter.

### 7. Clarify the role of reproductive assurance `R`

`R` is an auxiliary background moderator in the implemented corollary. It must remain outside the title, abstract claim, primary theorem, and keywords. Methods may document it transparently.

## Reviewer-facing risk register

| Risk | Current status | Required defence |
|---|---|---|
| “This is correlational selection with new labels” | Partly addressed | Lead with mechanism non-identifiability, orientation gate, and environmental derivative conditions |
| “The decomposition is a tautology” | Partly addressed | State that algebra is not the contribution; the contribution is the inference architecture and experimentally testable separation |
| “Complementarity means both traits are favoured” | Not explicit enough | State that the mixed sign does not determine first derivatives |
| “Defence is defined by the desired result” | Needs tightening | Require an operational antagonist-reduction role independent of pollinator obstruction |
| “The numerical grid is arbitrary” | Addressed in part | Keep it as finite sensitivity; report coordinates, scenarios, normalization, and no prevalence claim |
| “The literature validates only one pathway” | Correctly bounded | Keep all literature evidence subordinate to theory and route plausibility |
| “No evolutionary model is presented” | Correctly bounded | Present this as a local ecological diagnostic, not an evolutionary endpoint model |

## Submission decision after audit

The manuscript is suitable for continued preparation as a *Theoretical Ecology* Research Article. It is not yet portal-ready because final figures, author metadata, archive DOI, full reference verification, and the explicit manuscript corrections above remain incomplete.
