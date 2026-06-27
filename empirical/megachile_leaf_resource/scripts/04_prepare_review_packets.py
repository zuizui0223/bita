#!/usr/bin/env python3
"""Create source-specific packets for LLM-assisted candidate extraction.

This script does not call an LLM. It writes JSON packets that can be supplied to
an LLM with the embedded instruction, while retaining the exact source metadata
and locally saved text used for extraction.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

PROMPT = """You are extracting candidate Megachile nesting-material evidence from one source.\n\nReturn JSON only. Do not infer missing facts. A record requires a source locator and an exact short quote or paraphrase grounded in the supplied text.\n\nFor every possible bee--plant statement, return an object with:\n- bee_name_reported\n- plant_name_reported\n- interaction_type: one of leaf_cutting_direct, petal_cutting_direct, nest_lining_direct, resin_collection_direct, nest_material_unspecified, floral_visit_only, nest_near_plant_only, co_occurrence_only, unknown\n- candidate_evidence_grade: A, B, C, D, or E\n- source_locator\n- evidence_quote\n- locality_reported\n- uncertainty_note\n\nRules:\n1. Floral visitation is floral_visit_only, not nesting-material use.\n2. Do not treat a plant list as direct evidence unless the text explicitly links the bee and plant to material use.\n3. Use grade A only for direct species-level bee and plant evidence; B when one taxon is less resolved; C for secondary citation; D for vague claims; E for non-material association.\n4. Return an empty list when no candidate evidence is present.\n"""


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--text-dir", type=Path, required=True, help="One optional <source_id>.txt file per source")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    rows = read_rows(args.metadata)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    missing_text = 0
    for row in rows:
        source_id = row.get("source_id", "").strip()
        if not source_id:
            raise ValueError("metadata row lacks source_id")
        text_path = args.text_dir / f"{source_id}.txt"
        source_text = text_path.read_text(encoding="utf-8") if text_path.exists() else ""
        if not source_text:
            missing_text += 1
        packet = {
            "source_id": source_id,
            "metadata": row,
            "source_text_path": str(text_path),
            "source_text_present": bool(source_text),
            "instruction": PROMPT,
            "source_text": source_text,
        }
        with (args.output_dir / f"{source_id}.json").open("w", encoding="utf-8") as handle:
            json.dump(packet, handle, ensure_ascii=False, indent=2)
    print(f"wrote {len(rows)} review packets; {missing_text} have no local source text yet")


if __name__ == "__main__":
    main()
