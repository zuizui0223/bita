"""Recover measured yeast Fcy1 growth validation from author's original plate workbooks.

This checks a selected 18-allele validation panel, not the natural prevalence
of complementation. Units are genotype pairs sharing variants/assay designs,
not independent evolutionary transitions. Reproduction requires pandas,
numpy and openpyxl ONLY for the external-author data import.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import re
from pathlib import Path
from statistics import mean

SOURCE_COMMIT = "f124cef96a3b5806a096b679b2bd57b68aec6514"
SOURCE_POSITIVE_BLOB = "36839a3fd2eb05a521a070d11e60cde1748a682e"
SOURCE_NOTEBOOK_BLOB = "2ebafd783a94506aa349e46a1429fb2c98c16319"
VALIDATION_ALLELES = (
    "R53D", "R53I", "H62C", "E64C", "E64S", "E64V", "E69L",
    "G72P", "R73G", "L74P", "Y79S", "M93G", "A97F", "M100W",
    "F153*", "D155A", "D155S", "I156P",
)
THRESHOLD = .02
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = (ROOT / "empirical/trait_architecture_history/"
                  "despres2024_growth_validation_readout.json")


def git_blob_sha(payload: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(payload)).encode("ascii") + b"\0" + payload
    ).hexdigest()


def load_author_positives(path: Path) -> set[tuple[str, str]]:
    if git_blob_sha(path.read_bytes()) != SOURCE_POSITIVE_BLOB:
        raise ValueError("positive-pair source Git blob SHA mismatch")
    with path.open(newline="", encoding="utf-8") as stream:
        raw = list(csv.DictReader(stream))
    if len(raw) != 207:
        raise ValueError("source positives must have 207 rows")
    positive = set()
    for rec in raw:
        pair = tuple(sorted((rec["allele_1"], rec["allele_2"])))
        if pair in positive or pair[0] == pair[1]:
            raise ValueError("duplicate or invalid positive pair")
        positive.add(pair)
    return positive


def classify_panel(
    rows: list[dict],
    screened: set[tuple[str, str]],
    threshold: float = THRESHOLD,
    allow_unmeasured: bool = True,
) -> list[dict]:
    """Use means of available reciprocal growth values as in the author notebook."""
    if not math.isfinite(threshold) or threshold <= 0:
        raise ValueError("invalid threshold")
    found = set()
    result = []
    for row in rows:
        a, b = row["pair"]
        pair = tuple(sorted((a, b)))
        if not a or not b or pair in found:
            raise ValueError("duplicate or invalid unordered pair")
        found.add(pair)
        rates = row["rates"]
        if len(rates) != 2:
            raise ValueError("expected reciprocal growth values")
        observed = []
        for v in rates:
            if v is None:
                continue
            if not isinstance(v, (float, int)) or not math.isfinite(v):
                raise ValueError("growth rate must be finite when measured")
            observed.append(float(v))
        if not observed and not allow_unmeasured:
            raise ValueError("unmeasured genotype pair")
        avg = mean(observed) if observed else None
        positive_screen = pair in screened
        measured_positive = None if avg is None else avg >= threshold
        if measured_positive is None:
            status = "UNMEASURED"
        elif positive_screen and measured_positive:
            status = "TP"
        elif positive_screen and not measured_positive:
            status = "FP"
        elif not positive_screen and measured_positive:
            status = "FN"
        else:
            status = "TN"
        result.append({
            "allele_1": pair[0], "allele_2": pair[1],
            "source_screen_positive": positive_screen,
            "mean_growth_od_per_hour": avg,
            "n_measured_reciprocal_directions": len(observed),
            "growth_positive_at_0_02": measured_positive,
            "status": status,
        })
    if not screened.issubset(found):
        raise ValueError("positive screening pair absent from validation panel")
    return sorted(result, key=lambda r: (r["allele_1"], r["allele_2"]))


def summarize_classification(classified: list[dict]) -> dict:
    counts = {code: sum(row["status"] == code for row in classified)
              for code in ("TP", "FP", "FN", "TN", "UNMEASURED")}
    tp, fp, fn, tn, missing = (counts[k] for k in ("TP", "FP", "FN", "TN", "UNMEASURED"))
    def safe(n, d):
        return n/d if d else None
    return {
        "n_total": len(classified),
        "n_measured": len(classified)-missing,
        "n_missing": missing,
        "true_positive": tp,
        "false_positive": fp,
        "false_negative": fn,
        "true_negative": tn,
        "screen_precision": safe(tp, tp+fp),
        "screen_sensitivity": safe(tp, tp+fn),
        "screen_specificity": safe(tn, tn+fp),
        "screen_negative_predictive_value": safe(tn, tn+fn),
        "n_single_direction_measured": sum(
            x["n_measured_reciprocal_directions"] == 1 for x in classified),
        "n_both_directions_measured": sum(
            x["n_measured_reciprocal_directions"] == 2 for x in classified),
        "false_positive_pairs": [
            x for x in classified if x["status"] == "FP"],
        "false_negative_pairs": [
            x for x in classified if x["status"] == "FN"],
        "unmeasured_pairs": [
            x for x in classified if x["status"] == "UNMEASURED"],
    }


def reproduce_original_plate_analysis(source_root: Path) -> dict:
    """Mirror author notebook input layout, exclusions, growth-rate estimator."""
    import pandas as pd
    import numpy as np

    dataset = source_root / "validations_analysis"
    positive_csv = dataset / "indep_crosses.csv"
    positives = load_author_positives(positive_csv)
    plan_a = pd.read_excel(dataset / "data/validations_mat_a_nat.xlsx")
    plan_b = pd.read_excel(dataset / "data/validations_mat_alpha_hph.xlsx")
    def mapping(plan):
        return {str(int(row.number)): str(row.strain)
                for row in plan.itertuples()
                if pd.notna(row.number) and pd.notna(row.strain)}
    map_a, map_b = mapping(plan_a), mapping(plan_b)
    layout = pd.read_csv(dataset / "data/array_LOF.csv", index_col=0)
    if len(layout) != 2304:
        raise ValueError("plate layout must have 2304 wells")
    keys = {(int(r.n_384well),r.quadrant,r.well): idx
            for idx, r in layout.iterrows()}
    if len(keys) != len(layout):
        raise ValueError("duplicate well/plate/quadrant key")
    layout["growth_rate"] = np.nan

    growth_sources = sorted((dataset / "lofxlof_crosses").glob("plate_*_*.xlsx"))
    expected_files = {f"plate_{plate}_{quadrant}.xlsx"
                      for plate in range(1, 7) for quadrant in "ABCD"}
    actual_files = {p.name for p in growth_sources}
    # The original author's source repository publishes 23/24 quadrants.
    # plate_6_D.xlsx is not deposited; preserve missing wells as missing.
    if expected_files - actual_files != {"plate_6_D.xlsx"} or actual_files - expected_files:
        raise ValueError("unexpected original-plate availability; expected missing 6_D only")
    manifest = []
    for path in growth_sources:
        match = re.fullmatch(r"plate_([1-6])_([A-D])\.xlsx", path.name)
        if match is None:
            raise ValueError("unexpected plate name")
        plate, quadrant = int(match.group(1)), match.group(2)
        df = pd.read_excel(path, skiprows=[0, 2]+list(range(99,133)), index_col=0)
        df.rename(columns={
            name: float(str(name).strip("s")) / 3600
            for name in df.columns
        }, inplace=True)
        source_time = df.T
        if len(source_time.columns) != 96:
            raise ValueError("each source plate needs 96 well time-series")
        early = source_time.loc[source_time.index <= 21]
        for well in source_time.columns:
            diff = early[well].diff() * 4
            top5 = diff.nlargest(5)
            if len(top5) < 5:
                raise ValueError("fewer than five growth-curve derivative points")
            growth_rate = float(np.median(top5))
            idx = keys[(plate, quadrant, well)]
            layout.at[idx,"growth_rate"] = growth_rate
        manifest.append({
            "name": path.name,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        })
    # Original source notebook specifically invalidates this measurement.
    layout.at[2103, "growth_rate"] = np.nan
    # Match the original notebook's explicit source strain exclusions.
    layout = layout[~layout["Mata"].isin(["43", "3", "Empty"])]
    layout = layout[~layout["MatAlpha"].isin(["Empty"])]
    layout = layout.copy()
    layout["mutant_a"] = layout["Mata"].map(map_a)
    layout["mutant_alpha"] = layout["MatAlpha"].map(map_b)
    if layout["mutant_a"].isna().any() or layout["mutant_alpha"].isna().any():
        raise ValueError("unresolved genotype plan mapping")
    observed = layout.pivot_table(index="mutant_alpha", columns="mutant_a",
                                  values="growth_rate")
    panel = []
    def lookup(a, b):
        if a not in observed.index or b not in observed.columns:
            return None
        val = observed.at[a,b]
        return float(val) if pd.notna(val) else None
    all_genotypes = set(VALIDATION_ALLELES)
    panel_hits = {pair for pair in positives
                  if pair[0] in all_genotypes and pair[1] in all_genotypes}
    for a,b in itertools.combinations_with_replacement(VALIDATION_ALLELES, 2):
        panel.append({"pair": (a,b), "rates": (lookup(a,b), lookup(b,a))})
    classified = classify_panel(panel,panel_hits)
    counts = summarize_classification(classified)
    return {
        "paper_doi": "10.1126/science.ado5719",
        "original_repo": "Landrylab/Despres_et_al_2024",
        "original_ref": SOURCE_COMMIT,
        "original_positive_csv_blob": SOURCE_POSITIVE_BLOB,
        "source_notebook_blob": SOURCE_NOTEBOOK_BLOB,
        "experimental_design": "18 selected Fcy1 LOF alleles, all 171 unordered pairs, reciprocal growth measurements",
        "growth_assay": "cytosine 16 micrograms/ml, OD/h; median of top five quarter-hour optical density derivatives before 21 hours",
        "source_screen_classification": "207 positive-pair source screen; only 27 pairs in 18-allele panel",
        "threshold_od_per_hour": THRESHOLD,
        "counts": counts,
        "n_positives_from_source_inside_panel": len(panel_hits),
        "plate_workbook_sha256": manifest,
        "n_growth_assay_plate_workbooks": len(manifest),
        "pair_values": classified,
        "inference_boundary": (
            "Selected validation subset, not full eligible genotype universe. "
            "Shared alleles, correlated reciprocal measurements, assay growth "
            "and source screening selection preclude a natural complementation "
            "prevalence estimate or naive pair-independent population p value. "
            "Screen/growth discordance does not identify an environmental mechanism. "
            "No historical origins, ancestral/shared architecture fitness counterfactual, "
            "or BITA activation cost K(u) is measured."
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = reproduce_original_plate_analysis(args.source_dir)
    expected = dict(true_positive=24, false_positive=3, false_negative=3,
                    true_negative=137, n_missing=4, n_total=171, n_measured=167)
    for key, value in expected.items():
        if result["counts"][key] != value:
            raise AssertionError(f"author notebook mismatch at {key}: {result['counts'][key]} vs {value}")
    if result["n_positives_from_source_inside_panel"] != 27:
        raise AssertionError("wrong selected positive count")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)+"\n",
                          encoding="utf-8")
    print("BITA_FCY1_GROWTH_RECEIPT:"+json.dumps({
        "n": result["counts"]["n_total"],
        "counts": result["counts"],
        "source": result["original_positive_csv_blob"],
        "output": str(args.output),
    },ensure_ascii=False))


if __name__ == "__main__":
    main()
