# Biotic Interaction Trait Architecture (BITA)

BITA's **primary submission paper** is now the Ecology Letters Letter:

> **Access constraints reroute floral exploitation across bird and insect visitor networks**

The broader floral-defence selectivity Synthesis remains preserved as the extended BITA evidence package and fallback manuscript architecture.

## Current submission thesis

> **Access constraints can reorganize ecological interactions by shifting exploitation from legitimate access toward bypass routes rather than simply eliminating use.**

The primary quantitative test is the all-Ecuador bird–flower network:

```text
1,378 bird × plant × site units
barrier robbery     = 0.307
accessible robbery  = 0.081
difference          = +0.226
site-adjusted rho   = 0.351
within-site permutation p = 0.0001
15 / 17 comparable sites in the same direction
```

A smaller independent Afrotropical insect network provides corroboration:

```text
57 plant species
tube length vs robbing–thieving balance
rho = 0.347
permutation p = 0.0086
multitrait tube-length block p = 0.211
```

The two networks contribute one rank association each with equal network weight:

```text
rho_J = 0.349
joint permutation p = 0.0001
independent network contributions k = 2
```

Because `k=2`, the joint test does not estimate between-network heterogeneity, a network-population mean, or generality beyond the two analysed systems.

## Mechanistic interpretation

The routing result is interpreted through the broader effective-access / exposure framework:

```text
legitimate route becomes harder to use
        |
        +--> exploitation declines, if no bypass exists
        |
        +--> exploitation reroutes, if bypass remains available
```

Source-audited floral-defence cases provide mechanistic context only. The matched effective-domain classifications are author-coded and have not yet undergone outcome-blind independent recoding, so the Letter does not use the matched-domain layer as independent validation and does not make an 11/11 success-rate argument.

## Manuscript graph

Primary submission:

- `manuscript/MANUSCRIPT_ACCESS_ROUTING_LETTER_V0.md`
- `manuscript/FIGURE_PLAN_ACCESS_ROUTING_LETTER_V0.md`
- `submission/ECOLOGY_LETTERS_LETTER_COVER_V0.md`
- `empirical/floral_defence_selectivity/results/joint_access_routing.json`

Extended Synthesis reserve:

- `manuscript/MANUSCRIPT_FLORAL_DEFENCE_SELECTIVITY_V0.md`
- `manuscript/CLAIM_FREEZE_MACRO_V0.md`
- `manuscript/MACRO_MANUSCRIPT_SOURCE_AUDIT_V0.md`
- `submission/ECOLOGY_LETTERS_SYNTHESIS_PROPOSAL_V0.md`
- `submission/FUNCTIONAL_ECOLOGY_ADAPTATION_V0.md`

Preserved mechanism-identification foundation:

- `manuscript/MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md`
- `manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md`
- `manuscript/CLAIM_FREEZE.md`

## Claim boundaries

Do not infer:

- causality from either network;
- a unique tube-length effect from Sakhalkar;
- generality across ecological networks from `k=2`;
- a common raw effect size across networks;
- independent validation from the author-coded matched-domain corpus;
- natural prevalence of selective defence;
- a universal mechanistic coefficient.

## Programme boundary

```text
SCH
functional conflict identification

SLK
architecture value and evolutionary realization

BITA
access / exposure asymmetry
        ->
interaction routing
        ->
selective defence / interference / bypass
```

## Submission route

```text
1. Ecology Letters — Letter
2. extended BITA Synthesis retained in reserve
3. Functional Ecology — Research Article fallback
4. Oikos — Research fallback
```

External submission remains author-controlled.

## Testing

```bash
python -m pip install -e '.[dev]'
pytest -m "not prose_contract"
pytest -m prose_contract
```
