from __future__ import annotations

import csv
from pathlib import Path

import pytest

from scripts.apply_direct_access_geometry_direction_batch import BATCH_FIELDS, apply
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
        apply(decisions,batch,tmp_path/"out.csv",tmp_path/"receipt.json")


def test_apply_codes_direction_after_freeze(tmp_path: Path) -> None:
    decisions=tmp_path/"decisions.csv"; batch=tmp_path/"batch.csv"
    _write(decisions, FIELDS, [_decision(
        "ELIGIBILITY_FROZEN_DIRECTION_UNCODED;state=ELIGIBLE_DIRECT_NEW;"
        "program=Study_2024;independence=NEW_INDEPENDENT_PROGRAM;"
        "basis=x;source=10.1/x"
    )])
    _write(batch, BATCH_FIELDS, [_batch()])
    result=apply(decisions,batch,tmp_path/"out.csv",tmp_path/"receipt.json")
    rows=list(csv.DictReader((tmp_path/"out.csv").open(encoding="utf-8")))
    assert rows[0]["decision_status"]=="ELIGIBLE_DIRECT"
    assert rows[0]["direction"]=="POSITIVE"
    assert result["direction_counts"]["POSITIVE"]==1
    assert result["eligible_direct_total_after_apply"]==1
