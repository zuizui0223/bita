"""Source-bounded 3+3-line contrasts; generations are not independent replicates."""
import copy

import pytest

from scripts.analyze_bita_elife2025_replica_analysis import (
    exact_perm, read_rows, summarize,
)

def test_two_sided_exact_permutation_minimum_with_six_lines():
    result = exact_perm((0, 0, 0), (1, 1, 1))
    assert result["permutations"] == 20
    assert result["p_two_sided"] == pytest.approx(.1)

def test_replication_and_recovered_endpoints():
    result = summarize(read_rows())
    assert result["fig2_robustness"]["n_values"] == 30
    assert result["fig3_normalized_fluorescence"]["n_values"] == 36
    assert result["independent_biological_replicates_per_group"] == 3
    assert result["fig2_robustness"]["final_gen"]["difference_double_minus_single"] == pytest.approx(.05517153213399)
    assert result["fig3_normalized_fluorescence"]["final_gen"]["difference_double_minus_single"] == pytest.approx(-.0759771773333)
    assert result["fig2_robustness"]["trajectory_auc"]["difference_double_minus_single"] == pytest.approx(.0893479943144)
    assert result["fig3_normalized_fluorescence"]["trajectory_auc"]["difference_double_minus_single"] == pytest.approx(-.0393710794667)
    assert result["fig3_normalized_fluorescence"]["final_gen"]["p_two_sided"] == pytest.approx(.5)
    assert result["pooled_meta_analysis_performed"] is False
    assert result["evolutionary_origin_or_hysteresis_identified"] is False

def test_duplicate_original_source_row_rejected():
    rows = read_rows()
    rows[0]["source_row"] = rows[1]["source_row"]
    with pytest.raises(ValueError, match="duplicate original"):
        summarize(rows)

def test_duplicate_line_generation_rejected():
    rows = read_rows()
    rows[0]["biological_replicate"] = rows[1]["biological_replicate"]
    with pytest.raises(ValueError, match="duplicate biological"):
        summarize(rows)

def test_nonfinite_and_wrong_source_rejected():
    rows=read_rows()
    rows[0]["value"]=float("nan")
    with pytest.raises(ValueError):
        summarize(rows)
    rows=read_rows()
    rows[0]["publisher_xlsx_sha256"]="0"*64
    with pytest.raises(ValueError, match="source identity"):
        summarize(rows)

def test_incorrect_repeated_generation_is_not_independent():
    rows=read_rows()
    assert {r["biological_replicate"] for r in rows} == {"X","Y","Z"}
    assert len(rows)==66
    assert len({(r["figure"],r["copy_group"],r["biological_replicate"]) for r in rows})==12
