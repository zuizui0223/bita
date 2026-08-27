"""Prepare a manuscript SVG for journal figure export.

Journal illustrations should not carry redundant outer titles/captions. Canonical
SVGs retain standalone-review titles where present, while this deterministic
preprocessor removes only declared outer-title text elements. Panel labels,
equations, annotations, route headers, and accessibility metadata remain.
"""

from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path


VISIBLE_TITLE_PREFIXES = (
    # Historical theorem-led figures retained for provenance/export compatibility.
    "Figure 1.",
    "Figure 2.",
    "Figure 3.",
    "Meta-analytic pattern architecture and identification boundary",
    "Quantitative evidence narrows the problem",
    "without identifying the total interaction",
    # Canonical identification-design figures.
    "A total trait interaction does not identify its mechanism",
    "Crossed interventions identify channels and test separability",
    "Do not define the joint cost as a residual",
    "Existing studies occupy complementary parts of the identification design",
    "Constituent channels recur, but mechanism allocation remains unidentified",
    "Experimental faces recur, but mechanism allocation remains unidentified",
    "An executable path from interaction detection to mechanism identification",
)


def text_content(element: ET.Element) -> str:
    return "".join(element.itertext()).strip()


def _text_y(element: ET.Element) -> float:
    raw_y = element.attrib.get("y")
    if raw_y is not None:
        try:
            return float(raw_y)
        except ValueError:
            pass

    # Matplotlib commonly positions SVG text through transform="translate(x y)".
    transform = element.attrib.get("transform", "")
    match = re.search(r"translate\(\s*[-+0-9.eE]+(?:[ ,]+)([-+0-9.eE]+)", transform)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            pass
    return 9999.0


def prepare(source: Path, output: Path) -> int:
    tree = ET.parse(source)
    root = tree.getroot()
    removed = 0

    for parent in root.iter():
        for child in list(parent):
            if not child.tag.endswith("text"):
                continue
            content = text_content(child)
            if any(content.startswith(prefix) for prefix in VISIBLE_TITLE_PREFIXES):
                # Only remove declared titles near the upper edge. The 80-unit
                # threshold accommodates both hand-authored and Matplotlib SVGs.
                if _text_y(child) <= 80:
                    parent.remove(child)
                    removed += 1

    output.parent.mkdir(parents=True, exist_ok=True)
    tree.write(output, encoding="unicode", xml_declaration=False)
    return removed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("output")
    parser.add_argument("--expected-removed", type=int, default=1)
    args = parser.parse_args()
    source = Path(args.source)
    output = Path(args.output)
    removed = prepare(source, output)
    if removed != args.expected_removed:
        raise SystemExit(
            f"expected {args.expected_removed} visible outer title element(s) in "
            f"{source.name}; removed={removed}"
        )
    print(f"prepared {output}: removed {removed} visible outer title element(s)")


if __name__ == "__main__":
    main()
