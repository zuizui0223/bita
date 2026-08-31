"""Inventory Jones et al. 2023 publisher CSVs without selecting effects.

This step exists to expose headers, row counts and low-cardinality experimental
fields before any primary contrast is chosen. It is deliberately descriptive.
"""
from __future__ import annotations
import argparse, csv, json
from collections import Counter
from pathlib import Path


def sniff(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    rows = list(csv.DictReader(text.splitlines()))
    headers = list(rows[0].keys()) if rows else []
    fields = {}
    for h in headers:
        values=[(r.get(h) or "").strip() for r in rows]
        nonblank=[v for v in values if v]
        counts=Counter(nonblank)
        if len(counts)<=25:
            fields[h]={"unique_count":len(counts),"values":dict(counts.most_common())}
        else:
            fields[h]={"unique_count":len(counts),"examples":[v for v,_ in counts.most_common(10)]}
    return {"filename":path.name,"row_count":len(rows),"headers":headers,"fields":fields}


def main(argv=None):
    ap=argparse.ArgumentParser(); ap.add_argument("input_dir"); ap.add_argument("output_json"); a=ap.parse_args(argv)
    root=Path(a.input_dir)
    report={"article_doi":"10.1111/oik.10103","files":[sniff(p) for p in sorted(root.glob("*.csv"))],
            "interpretation_boundary":"Inventory only; no dose, assay, outcome or effect is selected as primary here."}
    Path(a.output_json).write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2))
    return 0
if __name__=="__main__": raise SystemExit(main())
