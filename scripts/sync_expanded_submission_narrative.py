"""Synchronize repository-facing narrative and bibliography to the saturated Pattern manuscript."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"


def sync_readme(text: str) -> str:
    old = '''### Theory-to-pattern scaffold

The heterogeneous route ledger is **not a grand meta-analysis**. It maps the quantitative and directional evidence onto the mechanism classes derived in Part I:

```text
38 source-adjudicated effect/directional records
14 independent biological study clusters
A_to_pollination:   4 clusters
A_to_antagonism:    5
D_to_antagonism:   10
D_to_pollination:   7
same-system:       10 clusters
context/sign switch: 11 clusters
direct A x D:       1 strict cluster, sign unresolved
direct joint cost:  0 strict estimates, kappa unidentified
```

Incompatible response constructs are not averaged merely to manufacture a pooled effect.'''
    new = '''### Theory-to-pattern scaffold

The heterogeneous route ledger is **not a grand meta-analysis**. It maps quantitative and directional evidence onto the mechanism classes derived in Part I. After the registered saturation expansion:

```text
56 source-adjudicated effect/directional records
25 independent biological study clusters
A_to_pollination:    5 clusters
A_to_antagonism:     8
D_to_antagonism:    18
D_to_pollination:   10
same-system:        14 clusters
context/sign switch: 17 clusters
context-only programs: 7, excluded from route-ledger N
direct A x D:        1 strict cluster, sign unresolved
direct joint cost:   0 strict estimates, kappa unidentified
```

The expansion adds visual and multidimensional attraction-signal systems, chemically and physically distinct flower-specific defence mechanisms, guarded states, spatial/temporal/attack-mode filtering, visitor functional-mode switching, and lifecycle-stage role reversal. Incompatible response constructs are not averaged merely to manufacture a pooled effect.'''
    if old in text:
        text = text.replace(old, new, 1)
    elif "56 source-adjudicated effect/directional records" not in text:
        raise RuntimeError("README scaffold anchor not found")

    quantitative_anchor = '''Only three study components contain both physiological consumer roles and all three paired differences are zero, so the assembled contrast is not treated as a causal within-study role effect. Behavioral disagreements remain part of the context-dependence result.'''
    quantitative_extra = '''Only three study components contain both physiological consumer roles and all three paired differences are zero, so the assembled contrast is not treated as a causal within-study role effect. Behavioral disagreements remain part of the context-dependence result.

### Secondary contextual syntheses

Three additional published syntheses are retained without pooling their incompatible scales with the two reproduced modules:

- Haas-Desmarais et al. 2026: 171 studies / 1,348 study cases; publisher supplement package independently retrieved and hashed; herbivory is not relabelled as focal `D`.
- Caruso et al. 2019: main selection analysis of 755 gradients with SE from 36 articles; Dryad landing/API metadata verified, file-byte access currently blocked; selection gradients are not `W_AD`.
- Junker & Blüthgen 2010: 18 publications / 425 floral-scent response observations; floral-resource dependence is an independent consumer-filtering pattern, not a pollinator/antagonist identity map.'''
    if "### Secondary contextual syntheses" not in text:
        if quantitative_anchor not in text:
            raise RuntimeError("README quantitative anchor not found")
        text = text.replace(quantitative_anchor, quantitative_extra, 1)

    framing = (
        "\nThe **fixed theoretical core** and the **mechanism-pattern empirical synthesis** are kept inferentially separate: "
        "the synthesis asks **what is recurrent, what is context dependent, and what remains unidentified**. "
        "The finite sensitivity analysis **is not an empirically calibrated regime map**, and none of the route counts estimates prevalence in nature.\n"
    )
    marker = "the synthesis asks **what is recurrent, what is context dependent, and what remains unidentified**"
    if marker not in text:
        insert_after = "The paper is not “theory + illustrative literature.” Part I derives why and when attraction and defence become locally complementary or substitutable. Part II tests which mechanism-derived patterns recur across independent systems, where their state changes with context, and which quantities remain unidentified.\n"
        if insert_after not in text:
            raise RuntimeError("README framing anchor not found")
        text = text.replace(insert_after, insert_after + framing, 1)
    return text


def sync_bibliography(text: str) -> str:
    body, after_refs = text.split("\n## References\n\n", 1)
    statements_marker = "\n\n## Statements and Declarations\n"
    if statements_marker in after_refs:
        refs, suffix = after_refs.split(statements_marker, 1)
        suffix = statements_marker + suffix
    else:
        refs, suffix = after_refs, ""

    existing = [block.strip() for block in refs.strip().split("\n\n") if block.strip()]
    new_refs = [
        "Caruso CM, Eisen KE, Martin RA, Sletvold N (2019) A meta-analysis of the agents of selection on floral traits. *Evolution* 73:4–14. https://doi.org/10.1111/evo.13639",
        "Haas-Desmarais S, Castagneyrol B, Abdala-Roberts L, Lortie CJ, Traveset A, Moreira X (2026) The effect of herbivory on pollinators: a revisited meta-analysis. *Annals of Botany* 137:879–885. https://doi.org/10.1093/aob/mcaf258",
        "Junker RR, Blüthgen N (2010) Floral scents repel facultative flower visitors, but attract obligate ones. *Annals of Botany* 105:777–782. https://doi.org/10.1093/aob/mcq045",
    ]
    by_doi = {}
    for block in existing + new_refs:
        doi = block.rsplit("https://doi.org/", 1)[-1] if "https://doi.org/" in block else block
        by_doi[doi] = block
    if len(by_doi) != 20:
        raise RuntimeError(f"Expected 20 unique bibliography entries after expansion, found {len(by_doi)}")
    ordered = sorted(by_doi.values(), key=lambda block: block.split()[0].casefold())
    assembled = body.rstrip() + "\n\n## References\n\n" + "\n\n".join(ordered) + suffix
    return assembled.rstrip() + "\n"


def main() -> None:
    README.write_text(sync_readme(README.read_text(encoding="utf-8")), encoding="utf-8")
    MANUSCRIPT.write_text(sync_bibliography(MANUSCRIPT.read_text(encoding="utf-8")), encoding="utf-8")
    print("synchronized README and 20-entry expanded bibliography")


if __name__ == "__main__":
    main()
