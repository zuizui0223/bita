"""Relabel Figure 3 source and committed SVG for the Mechanism -> Pattern paper.

Only presentation strings are changed. Counts, coordinates, equations, and
quantitative results remain byte-for-byte unchanged except for those labels.
"""
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATHS = (
    ROOT / "scripts" / "build_empirical_mechanism_figure_svg.py",
    ROOT / "manuscript" / "figures" / "FIGURE_3_EMPIRICAL_MECHANISM_ARCHITECTURE.svg",
)

REPLACEMENTS = {
    "Empirical mechanism-pattern architecture and identification boundary": "Meta-analytic pattern architecture and identification boundary",
    "Source-adjudicated mechanism evidence": "Cross-study pattern scaffold",
    "Linked architecture and conditionality": "Recurrence and conditionality",
    "Quantitative module 1 · floral larceny": "Meta-analysis 1 · floral larceny",
    "Quantitative module 2 · floral volatiles": "Meta-analytic synthesis 2 · floral volatiles",
    "Evidence above supports mechanism recurrence / conditionality, not W_AD": "Evidence above supports recurrent patterns / conditionality, not W_AD",
}


def main() -> None:
    for path in PATHS:
        text = path.read_text(encoding="utf-8")
        changed = text
        for old, new in REPLACEMENTS.items():
            changed = changed.replace(old, new)
        if changed == text:
            # Idempotent reruns are allowed only when the new vocabulary exists.
            if "Meta-analytic pattern architecture and identification boundary" not in text:
                raise RuntimeError(f"Expected Figure 3 labels not found in {path}")
        path.write_text(changed, encoding="utf-8")


if __name__ == "__main__":
    main()
