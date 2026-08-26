# Theis & Adler 2012 identification re-audit v1

## Source

Theis N, Adler LS. 2012. Advertising to the enemy: enhanced floral fragrance increases beetle attraction and reduces plant reproduction. *Ecology* 93:430–435. DOI `10.1890/11-0825.1`.

The publisher abstract states that the study manipulated **fragrance, pollination, and florivores** in *Cucurbita pepo* var. *texana*. The publisher page links a Figshare research-data collection (`10.6084/m9.figshare.c.3304428`).

A contemporaneous *American Scientist* report by Elsa Youngsteadt, based on the study and author interviews, provides the factorial details not exposed in the accessible publisher abstract: 168 Texas gourd vines were used; fragrance was enhanced with 1,4-dimethoxybenzene-treated swabs; beetles were manually removed every half hour from half of both fragrance-enhanced and control flowers; and half of the female flowers in each of the four fragrance × beetle-removal combinations were hand pollinated.

The original article full Methods were not directly retrievable in the current audit environment, so the exact design coding below is restricted to facts jointly supported by the publisher abstract and this contemporaneous study report. It does not infer undocumented randomization details or cell counts.

## Recoverable design structure

The accessible evidence supports a crossed reproductive design of the form

```text
fragrance enhancement (A):          control / enhanced
florivore treatment (G-like):       natural beetle exposure / repeated manual beetle removal
pollination treatment (P-supp):     natural pollination / supplemental hand pollination
```

The report explicitly states that hand pollination was applied to half of the female flowers **within each of the four fragrance × beetle combinations**. Thus the female reproductive experiment contains an `A × florivore-removal × pollination-supplementation` factorial backbone.

This is substantially closer to the target architecture than a study that merely measures visitor responses to manipulated fragrance, because attraction, an antagonist intervention, and a pollination intervention occur on the same crossed experimental surface.

## Why it is not a target P toggle

Supplemental hand pollination is not equivalent to the framework's selective pollinator-access contrast. Natural pollinators were not removed in the supplemented flowers; hand pollination instead supplies pollen and reduces pollen limitation / pollinator-choice dependence. It is therefore a randomized **pollination supplementation** treatment, not `P = absent/present`.

Accordingly, the study cannot by itself identify the pollinator increment used for `iota_delta`, nor can it characterize the pollinator-absent baseline `m0_delta`.

## Why it still cannot identify attraction–defence allocation

There is no independently manipulated antagonist-reducing defence coordinate `D`. Floral fragrance is the focal attraction coordinate and also changes antagonist attraction, but using one dual-route signal as both A and D would violate the requirement for distinct coordinates.

The study therefore lacks:

```text
independent D axis
A × D trait factorial
selective pollinator absent/present toggle
m0_delta
A × D × G × P separability diagnostic
independent kappa assay
```

Repeated manual beetle removal is an antagonist intervention, but the current audit does not equate it with perfect antagonist absence. Its value is that it supplies a crossed G-like manipulation on the same A and reproductive coordinates.

## Identification classification

```text
A_MANIPULATED:                         YES
D_AXIS:                                NO
A_x_G_CROSSED:                         YES
POLLINATION_SUPPLEMENTATION_CROSSED:   YES
A_x_G_x_PSUPP_BACKBONE:                YES
SELECTIVE_P_ACCESS_TOGGLE:             NO
M0_DELTA:                              NO
INDEPENDENT_KAPPA_ASSAY:               NO
FULL_CHANNEL_IDENTIFICATION:           NO
```

## Consequence for the identification frontier

Theis & Adler 2012 adds a new frontier face between a pure attraction experiment and the target four-factor architecture:

> **a manipulated attraction × antagonist-removal × pollination-supplementation bridge that is missing a distinct defence coordinate and a true pollinator-access toggle.**

This materially strengthens the design-fragmentation synthesis. Existing work has already crossed one focal floral attraction manipulation with both an antagonist intervention and a pollination intervention on female reproduction. The missing target is not all consumer manipulation; it is the addition of a biologically valid D coordinate plus the stricter P-access/baseline/separability/cost requirements.

## Minimum augmentation

The most direct conceptual extension is:

1. add an independently manipulable flower-associated antagonist-reducing `D` to the existing fragrance × beetle-removal backbone;
2. replace or complement supplemental hand pollination with a selective pollinator-access contrast capable of identifying the pollinator increment and `m0_delta`;
3. test the A×D×G×P four-way separability contrast;
4. add an independent A×D joint-cost assay.

This is a design recommendation, not a claim that those manipulations are technically feasible in *Cucurbita* without further system-development work.
