# Ipomopsis aggregata 2004 defence-selectivity audit v1

## Source

Irwin RE, Adler LS, Brody AK. 2004. The dual role of floral traits: pollinator attraction and plant defense. *Ecology* 85:1503–1511. DOI `10.1890/03-0390`.

A stable institutional full-text copy is available through Virginia Tech VTechWorks (`hdl.handle.net/10919/24802`). The paper explicitly tests whether dilute nectar can deter nectar-robbing *Bombus occidentalis* without deterring hummingbird pollinators.

## Design

This is an observational/path-analysis study rather than a randomized nectar-concentration manipulation. In 1998 the authors sampled plants across four sites, measured nectar sugar concentration, nectar robbing, pollinator visitation via pollen receipt to stigmas, and seed production, then compared four a-priori SEMs.

The source reports:

- plants with dilute nectar experienced significantly less robbing;
- the nectar-concentration -> hummingbird-visitation relationship was positive in the source's fitted path description but not statistically significant;
- pollinators strongly avoided robbed plants;
- the best-supported model therefore places much of the potential benefit of dilute nectar through reduced robbing and the downstream avoidance of robbed plants by pollinators.

The paper's own conclusion is that dilute nectar deters nectar-robbing bumblebees without detectable evidence of direct hummingbird deterrence in this dataset.

## Why this is not promoted to the primary quantitative matched-anchor registry

The study is highly relevant biologically, but its focal evidence is a covariance/path structure under natural trait variation. It is not a shared treatment contrast like Catalpa, Pedicularis, or Thunia. The paper reports the correlation matrix and standardized path diagram, but the current extraction does not yield a treatment-effect metric directly commensurate with the manipulation-based matched anchors.

Accordingly:

```text
biological selectivity state:       supported
same-trait antagonist/pollinator:    yes
randomized/shared treatment:         no
quantitative matched anchor:         no
universality support:                OBSERVATIONAL_REPLICATION
```

## Mechanism-first interpretation

Ipomopsis independently replicates the higher-level selectivity pattern in a reward/access trait: a nectar state associated with reduced robber use need not carry a detectable direct pollinator deterrence signal. It therefore strengthens cross-system recurrence, but does not contribute an experimental matched contrast or a direct estimate of `W_AD`.

## Inference boundary

Do not reinterpret the SEM path structure as a direct attraction x defence interaction. Nectar concentration has overlapping reward and resistance roles here, and the observed covariance structure does not identify `rho`, `iota`, `kappa`, or the mixed partial.
