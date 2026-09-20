# Sakhalkar 2023 multitrait routing sensitivity v1

## Purpose

The main BITA network result is a species-level Spearman association between tube length and robbing-versus-thieving balance.

This sensitivity analysis asks whether that association can be promoted to a unique tube-length effect after adjusting for the floral traits used in the source paper's parsimonious route models.

Predictors were frozen from the source paper before fitting the BITA route-balance response:

~~~text
robber source model: tube_length + tube_width + shape
thief source model:  tube_length + brightness + shape
union:               tube_length + tube_width + brightness + shape
~~~

## Data coverage

Among the 57 cheating-exposed species:

~~~text
tube_length  57 / 57
tube_width   57 / 57
shape        57 / 57
brightness    0 / 57
~~~

Therefore:

~~~text
robber-source model complete cases = 57
thief-source model complete cases  = 0
union model complete cases         = 0
~~~

The deposited workbook does not contain usable brightness values under the source-defined field name, so the thief-source and union models cannot be reproduced without adding or imputing external trait data. No imputation is used.

## Robber-source multitrait model

Species-level rank model:

~~~text
predictors = tube_length + tube_width + shape
n = 57
R2 = 0.290239
full-model permutation p = 0.2016
~~~

Block-drop tests:

~~~text
tube_length:
  delta R2 = 0.02880
  permutation p = 0.2110
  BH q = 0.6330

tube_width:
  delta R2 = 0.01091
  permutation p = 0.4487
  BH q = 0.6731

shape:
  delta R2 = 0.15140
  permutation p = 0.7447
  BH q = 0.7447
~~~

## Numerical-audit note

The 2026-09-20 numerical audit replaced the original absolute-scale ridge with a dimensionless ridge applied after matrix equilibration. Regeneration changed only floating-point tail digits of the fitted R2 / block-drop R2 values; all printed values, permutation p-values, BH decisions, and the claim ceiling are unchanged.

## Interpretation

The univariate BITA result remains:

~~~text
tube length vs robbing-thieving balance
Spearman rho = 0.346786
permutation p = 0.0086
~~~

but the current source-defined multitrait sensitivity does **not** establish tube length as a statistically unique predictor after simultaneous adjustment for tube width and a 12-level shape factor.

This does not contradict the route association. It narrows the claim:

> **tube length is associated with cheating-route balance across species, but the current deposited data do not isolate tube length from correlated floral morphology as the unique driver.**

## Why the sensitivity is conservative

The 57-species cheating subset contains 12 shape categories. Dummy-coding those levels consumes substantial model complexity, and the source paper's original route models were not designed around the BITA robbing-versus-thieving balance response.

Therefore a non-significant partial block is not evidence that tube length is biologically irrelevant.

Equally, BITA must not use the significant univariate association to claim that tube length alone causes route switching.

## Manuscript role

Keep the simple species-level association in the main Results because it directly tests the predeclared route-switch prediction.

Report this multitrait analysis as a robustness / claim-ceiling result:

- no unique-causal tube-length claim;
- no claim that tube length outperforms shape or tube width;
- thief-source and union models remain unavailable from the current deposited trait fields;
- the ecological interpretation should use 'access geometry' more strongly than 'tube length alone'.

## Provenance

Workflow run: 35486351356

Artifact digest:

sha256:c2ed9131a072270862d76f066e12f9453afe5a0f5705b41e5ef3f77791108513
