"""Direction-blind document-type screen for formal full-text candidates."""
from __future__ import annotations

import argparse
import csv
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from scripts.bootstrap_direct_access_geometry_bibliographic_screen import FRAME_FIELDS
from scripts.build_direct_access_geometry_fulltext_decision_template import FIELDS
from scripts.screen_direct_access_geometry_openalex_title_abstract import _openalex_ids

SECONDARY_TYPES = {"review", "editorial", "reference-entry", "peer-review"}


def _read(path: Path) -> tuple[tuple[str, ...], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return tuple(reader.fieldnames or ()), list(reader)


def _get_json(url: str, attempts: int = 6) -> dict[str, Any]:
    req = urllib.request.Request(
        url,
        headers={"User-Agent":"bita-formal-doctype-screen/1.0","Accept":"application/json"},
    )
    last: Exception | None = None
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            last = exc
            if exc.code not in {429,500,502,503,504}:
                raise
        except (urllib.error.URLError, TimeoutError) as exc:
            last = exc
        time.sleep(min(30,2**attempt))
    assert last is not None
    raise last


def _fetch_types(ids: list[str], batch_size: int = 50) -> tuple[dict[str,str], list[str]]:
    out: dict[str,str] = {}
    missing: list[str] = []
    unique=sorted(set(ids))
    for start in range(0,len(unique),batch_size):
        chunk=unique[start:start+batch_size]
        params={
            "filter":"openalex_id:"+"|".join(chunk),
            "per-page":"100",
            "select":"id,type",
        }
        p=_get_json("https://api.openalex.org/works?"+urllib.parse.urlencode(params))
        rows=p.get("results")
        if not isinstance(rows,list):
            raise RuntimeError("DOCTYPE_OPENALEX_RESULTS_MALFORMED")
        seen=set()
        for row in rows:
            if not isinstance(row,dict):
                continue
            oid=str(row.get("id") or "").removeprefix("https://openalex.org/")
            if oid:
                seen.add(oid)
                out[oid]=str(row.get("type") or "").strip()
        missing.extend(sorted(set(chunk)-seen))
        time.sleep(0.12)
    return out,sorted(set(missing))


def run(
    frame_path: Path,
    decisions_path: Path,
    output_path: Path,
    audit_path: Path,
    receipt_path: Path,
) -> dict[str,Any]:
    ff,frame=_read(frame_path)
    df,decisions=_read(decisions_path)
    if ff != FRAME_FIELDS:
        raise ValueError("DOCTYPE_FRAME_SCHEMA_MISMATCH")
    if df != FIELDS:
        raise ValueError("DOCTYPE_DECISION_SCHEMA_MISMATCH")
    by_id={r["frame_id"].strip():r for r in frame}

    pending=[r for r in decisions if r["decision_status"].strip()=="PENDING_FULLTEXT"]
    ids_by_frame={}
    all_ids=[]
    for d in pending:
        ids=_openalex_ids(by_id[d["frame_id"].strip()]["source_record_ids"])
        ids_by_frame[d["frame_id"].strip()]=ids
        all_ids.extend(ids)

    types,missing=_fetch_types(all_ids)
    missing_set=set(missing)
    excluded=0
    retained=0
    audit=[]

    for d in pending:
        fid=d["frame_id"].strip()
        ids=ids_by_frame[fid]
        observed=[types[i] for i in ids if i in types and types[i]]
        missing_here=[i for i in ids if i in missing_set]
        all_secondary=bool(observed) and not missing_here and all(t in SECONDARY_TYPES for t in observed)
        if all_secondary:
            d["decision_status"]="INELIGIBLE_SECONDARY_DOCUMENT_TYPE"
            d["decision_basis"]="DIRECTION_BLIND_OPENALEX_DOCUMENT_TYPE_SECONDARY"
            d["source_identifier"]="|".join(f"OpenAlex:{i}" for i in ids)
            d["notes"]="All provider records are review/editorial/reference-entry/peer-review; direction not inspected."
            excluded += 1
            state="EXCLUDED_SECONDARY_TYPE"
        else:
            retained += 1
            state="RETAINED_PRIMARY_OR_UNRESOLVED_TYPE"
        audit.append({
            "frame_id":fid,
            "title":d["title"].strip(),
            "openalex_ids":"|".join(ids),
            "openalex_types":"|".join(observed),
            "provider_ids_missing":"|".join(missing_here),
            "document_type_state":state,
        })

    output_path.parent.mkdir(parents=True,exist_ok=True)
    with output_path.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=(
            "frame_id","title","openalex_ids","openalex_types",
            "provider_ids_missing","document_type_state",
        ))
        w.writeheader();w.writerows(audit)
    # output_path is audit; decisions next to it with fixed sibling naming handled by explicit arg below?
    receipt={
        "schema":"BITA_DIRECT_ACCESS_GEOMETRY_DOCUMENT_TYPE_SCREEN_V1",
        "status":"DIRECTION_BLIND_DOCUMENT_TYPE_SCREEN_COMPLETE",
        "pending_input_records":len(pending),
        "excluded_secondary_document_type":excluded,
        "retained_primary_or_unresolved_type":retained,
        "provider_work_ids_missing":missing,
        "effect_direction_inspected":False,
    }
    receipt_path.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return {"receipt":receipt,"decisions":decisions}


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--frame",type=Path,required=True)
    parser.add_argument("--decisions",type=Path,required=True)
    parser.add_argument("--output-decisions",type=Path,required=True)
    parser.add_argument("--audit",type=Path,required=True)
    parser.add_argument("--receipt",type=Path,required=True)
    args=parser.parse_args()
    result=run(args.frame,args.decisions,args.audit,args.receipt)
    args.output_decisions.parent.mkdir(parents=True,exist_ok=True)
    with args.output_decisions.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=FIELDS);w.writeheader();w.writerows(result["decisions"])
    print(json.dumps(result["receipt"],indent=2,sort_keys=True))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
