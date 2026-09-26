"""Apply explicit duplicate-record adjudications to the formal direct-access ledger."""
from __future__ import annotations
import argparse,csv,json
from pathlib import Path
from scripts.build_direct_access_geometry_fulltext_decision_template import FIELDS

BATCH_FIELDS=("frame_id","duplicate_of_program_id","source_identifier","decision_basis","notes")

def _read(path:Path):
    with path.open(encoding="utf-8-sig",newline="") as h:
        r=csv.DictReader(h); return tuple(r.fieldnames or ()),list(r)

def apply(decisions_path:Path,batch_path:Path,output_path:Path,receipt_path:Path):
    df,rows=_read(decisions_path); bf,batch=_read(batch_path)
    if df!=FIELDS: raise ValueError("DUP_APPLY_DECISION_SCHEMA_MISMATCH")
    if bf!=BATCH_FIELDS: raise ValueError("DUP_APPLY_BATCH_SCHEMA_MISMATCH")
    by_id={r["frame_id"].strip():r for r in rows}
    eligible={
        r["biological_program_id"].strip()
        for r in rows
        if r["decision_status"].strip()=="ELIGIBLE_DIRECT"
        and r["biological_program_id"].strip()
    }
    applied=[]
    for b in batch:
        fid=b["frame_id"].strip(); target=b["duplicate_of_program_id"].strip()
        d=by_id.get(fid)
        if d is None: raise ValueError(f"DUP_APPLY_UNKNOWN_FRAME:{fid}")
        if d["decision_status"].strip()!="PENDING_FULLTEXT":
            raise ValueError(f"DUP_APPLY_NOT_PENDING:{fid}:{d['decision_status']}")
        if target not in eligible:
            raise ValueError(f"DUP_APPLY_TARGET_NOT_ELIGIBLE:{fid}:{target}")
        if not b["source_identifier"].strip() or not b["decision_basis"].strip():
            raise ValueError(f"DUP_APPLY_MISSING_PROVENANCE:{fid}")
        d["decision_status"]="DUPLICATE_BIOLOGICAL_PROGRAM"
        d["biological_program_id"]=""
        d["direction"]=""
        d["duplicate_of_program_id"]=target
        d["decision_basis"]=b["decision_basis"].strip()
        d["source_identifier"]=b["source_identifier"].strip()
        d["notes"]=b["notes"].strip()
        applied.append({"frame_id":fid,"duplicate_of":target})
    output_path.parent.mkdir(parents=True,exist_ok=True)
    with output_path.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=FIELDS);w.writeheader();w.writerows(rows)
    receipt={
        "schema":"BITA_DIRECT_ACCESS_GEOMETRY_DUPLICATE_APPLY_V1",
        "status":"EXPLICIT_DUPLICATE_RECORDS_RESOLVED",
        "applied_records":applied,
        "duplicate_records_after_apply":sum(r["decision_status"].strip()=="DUPLICATE_BIOLOGICAL_PROGRAM" for r in rows),
        "pending_records_after_apply":sum(r["decision_status"].strip()=="PENDING_FULLTEXT" for r in rows),
        "effect_direction_imported":False,
    }
    receipt_path.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return receipt

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--decisions",type=Path,required=True)
    p.add_argument("--batch",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--receipt",type=Path,required=True)
    a=p.parse_args()
    print(json.dumps(apply(a.decisions,a.batch,a.output,a.receipt),indent=2,sort_keys=True))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
