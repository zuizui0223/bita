# Head–tail depth-audit preliminary readout v1

## Scope

This note records a qualitative check of the first generated head–tail audit
packet. It is **not** the completed source-coding result and does not replace the
frozen coding sheet. It identifies an immediate constraint on how the packet must
be read.

## Observation

In the `A_to_antagonism` priority queue, many high-ranked candidates are plainly
outside the direct `A -> H` estimand at abstract level. They include:

```text
A -> P studies
  flower colour / petal microstructure -> pollinator preference or visitation

H -> P studies
  florivory / floral damage -> visitor frequency or reproductive success

environment -> A or environment -> H studies
  drought -> floral traits
  elevation/resource variation -> florivory
```

The same issue is visible in the current `B_to_pollination` queue: many candidates
concern floral morphology or scent in pollination, without establishing a
flower-specific defence/barrier or an access-restriction cost. These are potential
A traits unless the source documents a defensive or restrictive mechanism.

## Consequence

The head–tail audit still serves its intended purpose: it measures whether direct
route studies remain in the tail after the same conservative source coding is
applied to both rank bands. But it must not be used as an automatic effect-source
queue. Direct-route coding must apply the following exclusions before any study is
promoted to a Part B effect candidate:

```text
A_to_antagonism
  exclude A -> P, H -> P, environment -> trait, and environment -> H studies
  retain only direct floral attraction/display trait -> antagonist outcome studies

B_to_pollination
  exclude attraction-only scent/morphology studies
  retain only flower-specific defence/barrier/access-restriction -> pollination or
  visitor-use studies, with the mechanism traceable in the source
```

## Decision

Do not expand the Crossref depth cap to 5,000 records per query. Complete the
small source audit first, but treat its output as an audit of retrieval precision,
not a source of automatically eligible effects. The validated `c_D` chemical-
barrier manipulation literature remains the most practical route for the next
quantitative extraction; the `d_A` source search must proceed in separate visual
and scent/reward strata.

## Boundary

This preliminary readout is based on titles and available metadata abstracts from
the generated packet. It does not code a direct route as present, assign effect
direction, estimate an effect, or alter the verified Part B effect table.
