from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

THEOREM = '### One-sided selectivity bound\n\nThe balance yields one stronger structural statement than the bookkeeping identity. Define the **selectivity window** as the region where antagonist relief exceeds pollinator interference before direct joint cost is charged. Under the declared non-negative `relief - interference - cost` family,\n\n```text\nW_AD > 0  =>  inside the selectivity window\n```\n\nso **complementarity does not occur outside the window**. Across all 2,592 declared evaluations there are zero counterexamples. The converse is false: window precision is 77.2%, so about 23% of in-window evaluations are still substitutable. With joint cost set to zero, the window becomes the exact criterion.\n\nThe bound can fail only if joint-cost curvature is negative and sufficiently large in magnitude. Because `c_AD` is not directly measured in the strict evidence layer, its sign is the minimal empirical gate for the biological applicability of this one-sided theorem. See `docs/SELECTIVITY_WINDOW_BOUND.md`.'
EXTRA = 'Dependence, influence, sensitivity analyses, and extreme among-study heterogeneity remain explicit. For female reproductive success, 35/48 clusters are negative, but the 95% prediction interval is -1.13 to +0.71 and significantly positive systems occur. Six declared moderator analyses explain only 0-8% of the heterogeneity. The antagonist-pressure gate is therefore open on average, not universal, and the declared context axes do not yet locate its variation.\n\nThe apparent nectar -> visitation -> female-fitness sequence is not treated as a demonstrated within-study mechanism: only five clusters measured all three outcomes, two had all three negative, and the within-study nectar-visitation association across eleven shared clusters is `r = -0.17`.'
CROSS = '## Cross-system result\n\nThe empirical generality is deliberately hierarchical:\n\n> **recurrent constituent mechanisms + context-dependent balance inside a one-sided selectivity window**\n\nRoute separation, guarded defence, and consumer filtering recur across independent systems, but the theorem fixes their role: they identify where complementarity can occur, not that it must occur. Exposure (`H` relative to `P`) moves the window and is demonstrably heterogeneous. Direct joint-cost curvature determines whether the strongest one-sided bound is biologically applicable, yet its sign remains unmeasured. The cross-system Pattern therefore supports a moving permissive window rather than a universal positive or negative `W_AD`.\n\n'

def sync(text: str) -> str:
    if "### One-sided selectivity bound" not in text:
        anchor = "Within a neighbourhood where the orientation gate remains valid,\n"
        if anchor not in text:
            raise RuntimeError("README theorem insertion anchor not found")
        text = text.replace(anchor, THEOREM + "\n\n" + anchor, 1)

    anchor = "Dependence, influence, sensitivity analyses, and extreme among-study heterogeneity remain explicit."
    if "35/48 clusters are negative" not in text:
        if anchor not in text:
            raise RuntimeError("README larceny anchor not found")
        text = text.replace(anchor, EXTRA, 1)

    start = "## Cross-system result\n"
    end = "## Mechanism → Pattern inference boundary\n"
    if start not in text or end not in text:
        raise RuntimeError("README cross-system anchors not found")
    a = text.index(start); b = text.index(end, a)
    text = text[:a] + CROSS + "\n" + text[b:]

    current = "## Current decision\n"
    if current not in text:
        raise RuntimeError("README current-decision anchor not found")
    a = text.index(current)
    text = text[:a] + """## Current decision

The scientific story is closed at a deliberately one-sided boundary: the bookkeeping identity is not the novelty; the strongest structural result is the selectivity-window theorem, and Part II establishes recurrent pathways plus a heterogeneous antagonist-pressure gate without claiming a universal total sign. The next empirical hinge is the sign of `c_AD`, testable first with a 2 x 2 allocation experiment; a full `A x D` factorial remains the harder route to total `W_AD`.

Additional broad evidence searching is not a default blocker for this claim set. Remaining submission actions are author-controlled metadata/licence/archive fields and the authenticated journal portal.
"""
    return text

def main() -> None:
    text = README.read_text(encoding="utf-8")
    README.write_text(sync(text), encoding="utf-8")
    print("synchronized README one-sided selectivity story")

if __name__ == "__main__":
    main()
