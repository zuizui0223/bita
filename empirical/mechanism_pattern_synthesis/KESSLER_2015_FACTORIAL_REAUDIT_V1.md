# Kessler et al. (2015) — *Nicotiana attenuata* factorial re-audit

## Source and design

```text
article DOI: 10.7554/eLife.07641
A-like signal axis: benzylacetone floral scent (CHAL silencing removes scent)
reward axis: floral nectar production (SWEET9 silencing removes nectar)
fully crossed lines: EV / CHAL / SWEET9 / CHAL×SWEET9
```

The RNAi design independently removes floral scent and nectar and includes the double-silenced cross. It is therefore a genuine 2×2 floral-phenotype experiment rather than a correlational co-measurement study.

## Why it does not become strict Tier 1 `A x D`

The active direct-interaction protocol requires a declared attraction axis and an independently justified **flower-specific antagonist-reducing defence/access axis**.

SWEET9 is best described by the source as removal of a floral **reward**. Nectar absence reduces hawkmoth oviposition, but the same reward is also directly involved in pollination services. Treating `no nectar` as a defence trait solely because antagonists lay fewer eggs would redefine a reward axis post hoc into `D`.

Accordingly:

```text
factorial A-like × reward contrast: structurally present
strict A × D contrast:              not established
```

The paper also analyzes the four transformed lines using Friedman signed-rank tests and pairwise comparisons rather than reporting a formal scent × nectar interaction coefficient with uncertainty.

## Public supplementary-data audit

The eLife figures/data page states that supplementary/source material is distributed in the public article ZIP. A bounded GitHub Actions audit downloaded the declared ZIP successfully.

```text
workflow run: 31457174360
artifact:     9088554499
archive member count: 3
```

All three archive members are TIFF figure supplements:

```text
Figure 2 supplement 1: nectar accumulation
Figure 2 supplement 2: flower volatiles
Figure 2 supplement 3: leaf-volatile PCA
```

No CSV, XLSX, text source table, or observation-level dataset for Figure 2 pollination/oviposition outcomes is contained in that archive. Therefore a new uncertainty-bearing factorial interaction cannot be reconstructed from the public supplement route.

## Same-system scent routes retained

Although the strict `A x D` gate fails, the source contains unusually strong same-system evidence that one floral attraction signal affects both mutualistic and antagonistic channels.

### Scent → pollination service

For pollination by single *Manduca sexta* in the tent, scent-silenced CHAL plants produced only **17.4%** of the seeds produced by scented EV controls (`p < 0.001`). The double-silenced line produced 5.2% of EV seeds. This is experimental evidence that benzylacetone contributes strongly to *M. sexta*-mediated pollination success.

The effect is consumer-specific: for *Hyles lineata*, CHAL alone produced 96.6% of EV seeds (`p = 0.853`), and only the double-silenced line was strongly reduced. The source therefore also provides an explicit pollinator-identity moderator.

### Scent → antagonist oviposition

In the field, scent-silenced CHAL plants received **43.1%** of the *M. sexta* eggs found on scented EV plants (`p = 0.046`). In a single-moth tent assay CHAL received 81.9% of EV eggs (`p = 0.096`). Thus floral scent also increases the antagonist/offspring-placement channel, with a stronger resolved difference in the field assay.

The paper verified that non-flowering transformed plants did not differ in oviposition, which supports the interpretation that the relevant contrast is associated with floral traits rather than a constitutive leaf phenotype.

## Classification

```text
strict direct A x D:             no
reason:                          second axis is reward, not independently established D; no formal interaction coefficient
same-system A_to_pollination:    yes, experimental
same-system A_to_antagonism:     yes, experimental
consumer-identity conditionality:yes
public raw Figure-2 outcome data: not recovered
```

This study is therefore more valuable in the mechanism-pattern synthesis as a **Tier-2 attraction-tracking system** than as a forced Tier-1 direct interaction. It shows that the same scent signal can increase pollinator-mediated reproduction and hawkmoth oviposition, while its pollination value changes sharply among pollinator species.
