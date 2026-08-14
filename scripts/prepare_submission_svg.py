"""Prepare a manuscript SVG for journal figure export.

Theoretical Ecology asks that titles/captions not be embedded in illustrations.
The repository's canonical SVGs retain visible top titles for standalone review,
while this deterministic export preprocessor removes only those outer title text
elements. Panel labels, equations, annotations, and accessibility metadata remain.
"""

from __future__ import annotations

import argparse
import xml.etree.ElementTree as ET
from pathlib import Path


VISIBLE_TITLE_PREFIXES = (
    "Figure 1.",
    "Figure 2.",
    "Figure 3.",
    "Meta-analytic pattern architecture and identification boundary",
)


def text_content(element: ET.Element) -> str:
    return "".join(element.itertext()).strip()


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
                # Only remove an outer title near the top edge; panel headings and
                # ordinary annotations elsewhere in the illustration are retained.
                try:
                    y = float(child.attrib.get("y", "9999"))
                except ValueError:
                    y = 9999.0
                if y <= 60:
                    parent.remove(child)
                    removed += 1

    output.parent.mkdir(parents=True, exist_ok=True)
    tree.write(output, encoding="unicode", xml_declaration=False)
    return removed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("output")
    args = parser.parse_args()
    source = Path(args.source)
    output = Path(args.output)
    removed = prepare(source, output)
    if removed != 1:
        raise SystemExit(f"expected exactly one visible outer title in {source.name}; removed={removed}")
    print(f"prepared {output}: removed one visible outer title")


if __name__ == "__main__":
    main()
