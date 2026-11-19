"""Pineau 2024 character-displacement evidence gate: author F5 source/code.

This checks the published source workbook and the *original* R scripts, with
raw independent population lines kept separate from the repeated cluster
imaging and repeated times. A figure-code reference is not raw independent
replication.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import statistics
import zipfile
from pathlib import Path

from scripts.audit_bita_pineau2024_f2_workbook import (
    verify_author_bytes,
    get_workbook_sheets,
    get_shared_strings,
    read_cells,
    F2_NAMES,
)

AUTHOR_COMMIT = "071affa79f16f0a469f099058372a7488c35c0c2"
LOAD_DATA_BLOB = "77844c9c336d01ea264a0b2b30229f61191a7ff7"
PLOT_CODE_BLOB = "9ec49af81ba1805277223149644c9fe35ab47f0f"
F5_SHEETS = ("Fig5A", "SuppF5A", "SuppF5B")
REPEATED_SAMPLE_DAYS = (1, 5, 10, 15, 20, 40)


def git_blob_hash(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def validate_author_scripts(load: bytes, plot: bytes) -> dict:
    if git_blob_hash(load) != LOAD_DATA_BLOB or git_blob_hash(plot) != PLOT_CODE_BLOB:
        raise ValueError("original author F5 source scripts differ from Git blob")
    loading = load.decode("utf8")
    plotting = plot.decode("utf8")
    # Exact source code's repeated-measure population identities are crucial.
    loaded = set(re.findall(r"\b([ls]\d+)_d(?:1|5|10|15|20)\s*<-", loading))
    small = sorted(x for x in loaded if x.startswith("s"))
    large = sorted(x for x in loaded if x.startswith("l"))
    if small != ["s1", "s2", "s3", "s4"] or large != ["l1", "l3", "l4"]:
        raise ValueError("unanticipated original F5 lineage names")
    if "matrix(meansvec,7,6, byrow = T)" not in plotting:
        raise ValueError("source F5 R matrix has different source lineage/time grain")
    for source_token in ("colMeans(means[1:3,])", "colMeans(means[4:7,])",
                         "rgsmall <- lm(mnsmall~rep(days,4))",
                         "rglarge <- lm(mnlarge~rep(days,3))"):
        if source_token not in plotting:
            raise ValueError("author F5 code population/time assignments changed")
    if "source(\"Figure5_load-data.R\")" in loading:
        raise ValueError("unexpected changed input source R file")
    local_inputs = len(re.findall(r"\bread\.table\(", loading))
    return {
        "author_source_commit": AUTHOR_COMMIT,
        "load_data_R_blob_SHA1": git_blob_hash(load),
        "plot_R_blob_SHA1": git_blob_hash(plot),
        "small_population_codes_from_R": small,
        "large_population_codes_from_R": large,
        "small_independently_evolved_monoculture_replays_visible_in_author_code": len(small),
        "large_independently_evolved_monoculture_replays_visible_in_author_code": len(large),
        "author_R_fig5_rows": 7,
        "author_R_fig5_repeated_timepoints": 6,
        "author_R_fig5_expected_population_time_means": 42,
        "author_R_fig5_R_days": [0,5,10,15,20,40],
        "author_R_recorded_raw_file_read_calls": local_inputs,
        "author_R_input_files_are_machine_local_paths_not_in_public_repo": True,
        "original_fig5_R_regression_reuses_repeated_times_within_lines": True,
    }


def summarize_sheet(rows: list[dict], name: str) -> dict:
    if not rows:
        raise ValueError("empty author F5 worksheet")
    nonempty_cols = sorted(set().union(*(set(r["cells"]) for r in rows)))
    types = {"numeric":0,"strings":0,"missing":0,"formulas":0}
    numeric_rows = []
    for r in rows:
        num = [float(v) for v in r["cells"].values()
               if type(v) in (int,float)]
        st = [str(v) for v in r["cells"].values() if type(v) is str]
        types["numeric"]+=len(num)
        types["strings"]+=len(st)
        types["formulas"]+=r["formula_count"]
        if num:
            numeric_rows.append((r["excel_row"],num))
    summary = {
        "name": name,
        "nonempty_excel_rows":len(rows),
        "nonempty_excel_columns":len(nonempty_cols),
        "first_nonempty_excel_row":rows[0]["excel_row"],
        "last_nonempty_excel_row":rows[-1]["excel_row"],
        "cell_type_count":types,
        "source_numeric_row_count":len(numeric_rows),
        "numeric_excel_row_range":[numeric_rows[0][0],numeric_rows[-1][0]] if numeric_rows else None,
        "numeric_values_per_row_distribution":dict(sorted({
            str(n):sum(len(v)==n for _,v in numeric_rows)
            for _,v in numeric_rows
        }.items())),
        "first_six_source_header_tokens":[
            {"row":r["excel_row"],"text":[str(v)[:90] for v in r["cells"].values()
                                          if type(v) is str][:10]}
            for r in rows[:6]
        ],
        "contains_author_numeric_timecourse": len(numeric_rows) >= 5,
        "source_numeric_value_range": [
            min(min(v) for _,v in numeric_rows),
            max(max(v) for _,v in numeric_rows)
        ] if numeric_rows else None,
    }
    return summary


def analyze_original_workbook(original_xlsx: bytes, load_r: bytes, plot_r: bytes) -> dict:
    source = verify_author_bytes(original_xlsx)
    scripts = validate_author_scripts(load_r, plot_r)
    with zipfile.ZipFile(io.BytesIO(original_xlsx)) as z:
        workbook_sheets = get_workbook_sheets(z)
        strings=get_shared_strings(z)
        figure_sheets={
            sheet:summarize_sheet(read_cells(z,workbook_sheets[sheet],strings),sheet)
            for sheet in F5_SHEETS if sheet in workbook_sheets
        }
    if "Fig5A" not in figure_sheets:
        raise ValueError("original author workbook missing Fig5A")
    return {
        "paper_doi":"10.1038/s41559-024-02367-y",
        "author_workbook_bytes_SHA_verified":source,
        "author_original_R_code_gate":scripts,
        "figure5_sheet_summaries":figure_sheets,
        "paper_text_replication_conflicts": {
            "Methods_monoculture_populations_per_phenotype":4,
            "Figure5_caption_monoculture_populations_per_phenotype":5,
            "author_R_code_small_population_count":4,
            "author_R_code_large_population_count":3,
            "source_sample_size_not_reconciled":True,
        },
        "inference_scope": {
            "author_code_data_directory_not_available_in_public_github":True,
            "n_population_not_n_phenotyped_clusters_or_population_time_cells":True,
            "do_not_treat_R_ANCOVA_38_residual_df_as_independent_evolved_populations":True,
            "not_original_causal_evolutionary_architecture_invasion_probability":True,
            "no_meta_analysis_or_cross_research_programme_replication":True,
        },
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--xlsx",required=True,type=Path)
    p.add_argument("--load-r",required=True,type=Path)
    p.add_argument("--plot-r",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args()
    out=analyze_original_workbook(
        args.xlsx.read_bytes(),args.load_r.read_bytes(),args.plot_r.read_bytes())
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2,allow_nan=False,ensure_ascii=False)+"\n")
    print("BITA_PINEAU_F5_SOURCE_READOUT:"+json.dumps(out,separators=(",",":")),flush=True)


if __name__=="__main__":
    main()
