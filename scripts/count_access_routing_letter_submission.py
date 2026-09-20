"""Count Ecology Letters submission metrics for the access-routing Letter."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_ACCESS_ROUTING_LETTER_V0.md"
DEFAULT_FIGURE_PLAN = ROOT / "manuscript" / "FIGURE_PLAN_ACCESS_ROUTING_LETTER_V0.md"


def _section(text: str, start: str, end: str | None) -> str:
    if start not in text:
        raise ValueError(f"missing section: {start}")
    body = text.split(start, 1)[1]
    if end is not None:
        if end not in body:
            raise ValueError(f"missing section end: {end}")
        body = body.split(end, 1)[0]
    return body.strip()


def _words(text: str) -> list[str]:
    text = re.sub(r"~~~[\s\S]*?~~~", " ", text)
    text = re.sub(r"\\\[[\s\S]*?\\\]", " ", text)
    text = re.sub(r"\\\([^)]*\\\)", " ", text)
    text = re.sub(r"^#+\s+.*$", " ", text, flags=re.MULTILINE)
    text = re.sub(r"^>\s*", "", text, flags=re.MULTILINE)
    text = text.replace("**", "").replace("*", "").replace(chr(96), "")
    return [token for token in re.split(r"\s+", text.strip()) if token]


def summarize(manuscript: str, figure_plan: str) -> dict[str, object]:
    abstract = _section(manuscript, "## Abstract", "## Introduction")
    main = _section(manuscript, "## Introduction", "## Data accessibility and reproducibility")
    references = _section(manuscript, "## References", None)

    ref_entries = [
        paragraph.strip()
        for paragraph in re.split(r"\n\s*\n", references)
        if paragraph.strip()
    ]
    figures = len(re.findall(r"^## Figure\s+\d+\b", figure_plan, flags=re.MULTILINE))

    return {
        "article_type": "Letter",
        "abstract_words": len(_words(abstract)),
        "main_text_words": len(_words(main)),
        "reference_count": len(ref_entries),
        "figure_count": figures,
        "table_count": 0,
        "textbox_count": 0,
        "display_item_count": figures,
        "word_count_definition": (
            "Main text is counted from Introduction through Conclusion, excluding "
            "Abstract, Data accessibility/reproducibility, References, and figure plan."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manuscript", type=Path, default=DEFAULT_MANUSCRIPT)
    parser.add_argument("--figure-plan", type=Path, default=DEFAULT_FIGURE_PLAN)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = summarize(
        args.manuscript.read_text(encoding="utf-8"),
        args.figure_plan.read_text(encoding="utf-8"),
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
