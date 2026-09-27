from __future__ import annotations

import csv
from pathlib import Path

import pytest

from scripts.apply_direct_access_geometry_direction_batch import BATCH_FIELDS, ELIGIBILITY_FIELDS, apply
from scripts.build_direct_access_geometry_fulltext_decision_template import FIELDS


def _write(path: Path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _decision(notes: str) -> dict[str, str]:
    return {
        "frame_id":"bib1","doi":"10.1/x","title":"Study","year":"2024",
        "source_dbs":"OpenAlex","query_ids":"Q1","decision_status":"PENDING_FULLTEXT",
        "biological_program_id":"","direction":"","duplicate_of_program_id":"",
        "decision_basis":"","source_identifier":"","notes":notes,
    }


def _eligibility() -> dict[str, str]:
    return {
        "frame_id":"bib1","doi":"10.1/x","title":"Study",
        "eligibility_state":"ELIGIBLE_DIRECT_NEW",
        "biological_program_id":"Study_2024",
        "independence_relation":"NEW_INDEPENDENT_PROGRAM",
        "decision_basis":"primary",
        "source_identifier":"10.1/x",
        "direction_coded":"NO",
        "notes":"frozen",
    }


def _batch() -> dict[str, str]:
    return {
        "frame_id":"bib1","doi":"10.1/x","title":"Study",
        "biological_program_id":"Study_2024","direction":"POSITIVE",
        "orientation_basis":"constraint increases robbery",
        "source_identifier":"10.1/x","evidence_basis":"primary result",
        "notes":"frozen first",
    }


def test_apply_requires_prior_eligibility_freeze(tmp_path: Path) -> None:
    decisions=tmp_path/"decisions.csv"; batch=tmp_path/"batch.csv"
    _write(decisions, FIELDS, [_decision("")])
    _write(batch, BATCH_FIELDS, [_batch()])
    with pytest.raises(ValueError, match="DIR_APPLY_ELIGIBILITY_NOT_PRE_FROZEN"):
        apply(decisions,batch,[],tmp_path/"out.csv",tmp_path/"receipt.json")


def test_apply_codes_direction_after_freeze(tmp_path: Path) -> None:
    decisions=tmp_path/"decisions.csv"; batch=tmp_path/"batch.csv"; elig=tmp_path/"elig.csv"
    _write(decisions, FIELDS, [_decision("")])
    _write(batch, BATCH_FIELDS, [_batch()])
    _write(elig, ELIGIBILITY_FIELDS, [_eligibility()])
    result=apply(decisions,batch,[elig],tmp_path/"out.csv",tmp_path/"receipt.json")
    rows=list(csv.DictReader((tmp_path/"out.csv").open(encoding="utf-8")))
    assert rows[0]["decision_status"]=="ELIGIBLE_DIRECT"
    assert rows[0]["direction"]=="POSITIVE"
    assert result["direction_counts"]["POSITIVE"]==1
    assert result["eligible_direct_total_after_apply"]==1
