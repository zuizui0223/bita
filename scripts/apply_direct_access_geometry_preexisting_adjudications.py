"""Apply source adjudications frozen before formal-frame direction coding."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from scripts.build_direct_access_geometry_fulltext_decision_template import FIELDS

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"empirical"/"floral_defence_selectivity"
DEFAULT_STAGE_U=BASE/"DIRECT_ACCESS_GEOMETRY_STAGE_U_REGISTRY_V1.csv"
DEFAULT_FIXED=BASE/"DIRECT_ACCESS_GEOMETRY_FORMAL_FIXED_EXCLUSIONS_V1.csv"


def _read(path:Path):
    with path.open(encoding="utf-8-sig",newline="") as h:
        r=csv.DictReader(h)
        return tuple(r.fieldnames or ()),list(r)


def _norm_doi(value:str)->str:
    x=(value or "").strip().casefold()
    for prefix in ("https://doi.org/","http://doi.org/","doi:"):
        if x.startswith(prefix):
            x=x[len(prefix):]
    return x.rstrip(" .;,")


def run(decisions_path:Path, output_path:Path, receipt_path:Path,
        stage_u_path:Path=DEFAULT_STAGE_U, fixed_path:Path=DEFAULT_FIXED):
    df,decisions=_read(decisions_path)
    if df != FIELDS:
        raise ValueError("PREEXISTING_ADJUDICATION_DECISION_SCHEMA_MISMATCH")
    _,stage=_read(stage_u_path)
    _,fixed=_read(fixed_path)

    stage_by_doi={}
    for r in stage:
        key=_norm_doi(r.get("source_identifier",""))
        if key.startswith("10."):
            if key in stage_by_doi:
                raise ValueError("PREEXISTING_ADJUDICATION_DUPLICATE_STAGE_U_DOI:"+key)
            stage_by_doi[key]=r

    fixed_by_doi={}
    for r in fixed:
        key=_norm_doi(r["source_identifier"])
        if not key:
            raise ValueError("PREEXISTING_ADJUDICATION_FIXED_EMPTY_ID")
        fixed_by_doi[key]=r

    eligible_ids={
        r["biological_program_id"].strip()
        for r in decisions
        if r["decision_status"].strip()=="ELIGIBLE_DIRECT"
        and r["biological_program_id"].strip()
    }

    counts={
        "stage_u_ineligible_applied":0,
        "stage_u_duplicate_applied":0,
        "fixed_exclusion_applied":0,
        "stage_u_eligible_pending_guarded":0,
    }
    applied=[]

    for d in decisions:
        if d["decision_status"].strip()!="PENDING_FULLTEXT":
            continue
        doi=_norm_doi(d["doi"])
        if doi in fixed_by_doi:
            f=fixed_by_doi[doi]
            d["decision_status"]=f["exclusion_status"].strip()
            d["decision_basis"]=f["decision_basis"].strip()
            d["source_identifier"]=doi
            d["notes"]=f["notes"].strip()
            counts["fixed_exclusion_applied"]+=1
            applied.append({"frame_id":d["frame_id"],"source":"FIXED","status":d["decision_status"],"target":""})
            continue

        r=stage_by_doi.get(doi)
        if not r:
            continue
        status=r["eligibility_status"].strip()
        relation=r["relation_to_existing_corpus"].strip()
        reason=r["reason"].strip()

        if status.startswith("INELIGIBLE_"):
            d["decision_status"]=status
            d["decision_basis"]="PREEXISTING_STAGE_U_SOURCE_ADJUDICATION"
            d["source_identifier"]=doi
            d["notes"]=reason
            counts["stage_u_ineligible_applied"]+=1
            applied.append({"frame_id":d["frame_id"],"source":"STAGE_U","status":status,"target":""})
        elif status=="DUPLICATE_COMPONENT_OF_LATER_SYNTHESIS":
            prefix="DUPLICATE_OF_"
            if not relation.startswith(prefix):
                raise ValueError("PREEXISTING_ADJUDICATION_BAD_DUPLICATE_TARGET:"+relation)
            target=relation[len(prefix):]
            if target not in eligible_ids:
                raise ValueError("PREEXISTING_ADJUDICATION_DUPLICATE_TARGET_NOT_ELIGIBLE:"+target)
            d["decision_status"]="DUPLICATE_BIOLOGICAL_PROGRAM"
            d["duplicate_of_program_id"]=target
            d["decision_basis"]="PREEXISTING_STAGE_U_DUPLICATE_ADJUDICATION"
            d["source_identifier"]=doi
            d["notes"]=reason
            counts["stage_u_duplicate_applied"]+=1
            applied.append({"frame_id":d["frame_id"],"source":"STAGE_U","status":"DUPLICATE_BIOLOGICAL_PROGRAM","target":target})
        elif status=="ELIGIBLE":
            # Never import exposed direction for a record the formal bootstrap did
            # not already identify as a known direct-corpus match.
            counts["stage_u_eligible_pending_guarded"]+=1
        else:
            # Other registry states remain pending rather than guessed.
            continue

    output_path.parent.mkdir(parents=True,exist_ok=True)
    with output_path.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=FIELDS);w.writeheader();w.writerows(decisions)

    receipt={
        "schema":"BITA_DIRECT_ACCESS_GEOMETRY_PREEXISTING_ADJUDICATION_REUSE_V1",
        "status":"PREEXISTING_DIRECTION_BLIND_ADJUDICATIONS_APPLIED",
        **counts,
        "applied_records":applied,
        "effect_direction_imported_for_new_formal_records":False,
        "remaining_pending_records":sum(r["decision_status"].strip()=="PENDING_FULLTEXT" for r in decisions),
    }
    receipt_path.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return receipt


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--decisions",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--receipt",type=Path,required=True)
    p.add_argument("--stage-u",type=Path,default=DEFAULT_STAGE_U)
    p.add_argument("--fixed",type=Path,default=DEFAULT_FIXED)
    a=p.parse_args()
    print(json.dumps(run(a.decisions,a.output,a.receipt,a.stage_u,a.fixed),indent=2,sort_keys=True))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
