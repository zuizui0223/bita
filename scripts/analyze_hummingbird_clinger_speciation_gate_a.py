#!/usr/bin/env python3
"""Gate A: test whether Colwell clinger state predicts lower hummingbird speciation.

This script implements the frozen v2 amendment:
- behaviour labels from Colwell et al. 2023 Supplemental Spreadsheet S1;
- independently estimated species-level speciation rates from Barreto et al. 2023;
- baseline adjustment for bill length, body mass, elevation, climatic niche breadth,
  and major clade;
- 9,999 within-clade label permutations.

It downloads only public, frozen source files and writes one JSON receipt.
"""
from __future__ import annotations

import argparse
import io
import json
import math
import re
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import requests

COLWELL_S1_URL = "https://dataverse.harvard.edu/api/access/datafile/6961274"
FIGSHARE_API = "https://api.figshare.com/v2/articles/22493044"
DEFAULT_SEED = 20261007
DEFAULT_PERMUTATIONS = 9999


def norm_text(value: object) -> str:
    s = str(value if value is not None else "").strip().lower()
    s = s.replace("_", " ")
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def norm_species(value: object) -> str:
    s = str(value if value is not None else "").strip()
    s = s.replace("_", " ")
    s = re.sub(r"\s+", " ", s).strip()
    if not s:
        return ""
    parts = s.split()
    if len(parts) < 2:
        return s
    return f"{parts[0].capitalize()} {parts[1].lower()}"


def request_bytes(url: str, timeout: int = 90) -> bytes:
    headers = {"User-Agent": "bita-reproducible-research/1.0"}
    last = None
    for attempt in range(6):
        try:
            r = requests.get(url, timeout=timeout, headers=headers)
            r.raise_for_status()
            return r.content
        except Exception as exc:
            last = exc
            if attempt == 5:
                raise
    raise RuntimeError(last)


def request_json(url: str) -> dict:
    return json.loads(request_bytes(url).decode("utf-8"))


def load_colwell_state() -> pd.DataFrame:
    raw = request_bytes(COLWELL_S1_URL)
    grid = pd.read_csv(io.BytesIO(raw), header=None, dtype=str, keep_default_na=False)
    header_i = None
    for i in range(min(len(grid), 40)):
        row = [norm_text(x) for x in grid.iloc[i].tolist()]
        if any(x == "feeding style" for x in row) and any("genus species" == x for x in row):
            header_i = i
            break
    if header_i is None:
        raise RuntimeError("COLWELL_HEADER_NOT_FOUND")

    header = [str(x).strip() for x in grid.iloc[header_i].tolist()]
    df = grid.iloc[header_i + 1 :].copy()
    df.columns = header
    df = df.loc[:, [c for c in df.columns if c and not str(c).startswith("Unnamed")]]

    nmap = {norm_text(c): c for c in df.columns}
    species_col = next((orig for n, orig in nmap.items() if n == "genus species"), None)
    clade_col = next((orig for n, orig in nmap.items() if n == "clade"), None)
    if species_col is None or clade_col is None:
        raise RuntimeError(f"COLWELL_CORE_COLUMNS_NOT_FOUND:{list(df.columns)}")

    style_patterns = [
        "feeds from the ground",
        "feeds legitimaely while clinging",
        "feeds using existing openings in flowers while clinging",
        "pierces flowers to feed while clinging",
        "feeds on the wing through existing pierces",
        "pierces flowers to feed on the wing",
    ]
    style_cols: list[str] = []
    for pat in style_patterns:
        exact = next((orig for n, orig in nmap.items() if n == pat), None)
        if exact is None:
            # tolerate spelling/wording drift but do not silently substitute unrelated fields
            tokens = set(pat.split())
            candidates = []
            for n, orig in nmap.items():
                if not n.startswith("feeds") and not n.startswith("pierces"):
                    continue
                score = len(tokens & set(n.split()))
                candidates.append((score, n, orig))
            candidates.sort(reverse=True)
            if candidates and candidates[0][0] >= max(3, len(tokens) - 2):
                exact = candidates[0][2]
        if exact is None:
            raise RuntimeError(f"COLWELL_STYLE_COLUMN_NOT_FOUND:{pat}")
        style_cols.append(exact)

    def active(v: object) -> int:
        s = norm_text(v)
        return int(s not in {"", "0", "no", "na", "nan", "none", "false"})

    out = pd.DataFrame(
        {
            "species": df[species_col].map(norm_species),
            "clade_colwell": df[clade_col].astype(str).str.strip(),
        }
    )
    style = pd.DataFrame({f"style_{i+1}": df[c].map(active) for i, c in enumerate(style_cols)})
    out = pd.concat([out, style], axis=1)
    out["clinger"] = (style.iloc[:, :4].sum(axis=1) > 0).astype(int)
    out["unorthodox"] = (style.sum(axis=1) > 0).astype(int)
    out["onwing_pierce_only"] = (
        (out["clinger"] == 0) & (style.iloc[:, 4:6].sum(axis=1) > 0)
    ).astype(int)
    # Match Colwell et al.'s published 66-clinger versus 144 presumed-non-clinger
    # contrast. The 10 species documented only feeding through pierces on the wing
    # are a third source-defined group and are not coded as primary non-clingers.
    out["clinger_primary"] = np.where(
        out["clinger"] == 1,
        1.0,
        np.where(out["unorthodox"] == 0, 0.0, np.nan),
    )
    # Secondary behavior state: any documented bypass through an existing or
    # self-made floral opening, whether clinging or hovering.
    out["bypass_capable"] = (style.iloc[:, 2:6].sum(axis=1) > 0).astype(int)
    out = out[out["species"].str.contains(" ", regex=False)].copy()
    out = out.drop_duplicates("species", keep="first")
    return out


def load_figshare_tables() -> tuple[list[tuple[str, pd.DataFrame]], dict]:
    meta = request_json(FIGSHARE_API)
    files = meta.get("files", [])
    tables: list[tuple[str, pd.DataFrame]] = []
    manifest = []
    for f in files:
        name = str(f.get("name") or f.get("filename") or "")
        url = f.get("download_url")
        if not url:
            continue
        manifest.append({"name": name, "url": url, "size": f.get("size")})
        low = name.lower()
        if not low.endswith((".csv", ".tsv", ".txt", ".xlsx", ".xls")):
            continue
        data = request_bytes(url)
        try:
            if low.endswith(".csv"):
                tab = pd.read_csv(io.BytesIO(data))
            elif low.endswith(".tsv"):
                tab = pd.read_csv(io.BytesIO(data), sep="\t")
            elif low.endswith(".txt"):
                # try tab then comma
                txt = data.decode("utf-8", errors="replace")
                tab = pd.read_csv(io.StringIO(txt), sep="\t")
                if tab.shape[1] == 1:
                    tab = pd.read_csv(io.StringIO(txt))
            else:
                tab = pd.read_excel(io.BytesIO(data))
        except Exception:
            continue
        tables.append((name, tab))
    return tables, {"article_id": meta.get("id"), "title": meta.get("title"), "files": manifest}


def find_species_column(df: pd.DataFrame) -> str | None:
    scored = []
    for c in df.columns:
        n = norm_text(c)
        score = 0
        if n in {"species", "species name", "genus species", "scientific name", "taxon"}:
            score += 10
        if "species" in n:
            score += 5
        if "name" in n:
            score += 1
        if score:
            vals = df[c].astype(str).map(norm_species)
            score += int(vals.str.contains(" ", regex=False).mean() * 5)
            scored.append((score, c))
    return max(scored)[1] if scored else None


def numeric_fraction(series: pd.Series) -> float:
    return pd.to_numeric(series, errors="coerce").notna().mean()


def choose_barreto_table(tables: list[tuple[str, pd.DataFrame]], states: pd.DataFrame):
    state_names = set(states["species"])
    best = None
    diagnostics = []
    for name, df in tables:
        sp = find_species_column(df)
        if sp is None:
            diagnostics.append({"file": name, "species_col": None, "overlap": 0, "columns": list(map(str, df.columns))})
            continue
        names = set(df[sp].map(norm_species))
        overlap = len(state_names & names)
        item = {"file": name, "species_col": str(sp), "overlap": overlap, "columns": list(map(str, df.columns))}
        diagnostics.append(item)
        if best is None or overlap > best[0]:
            best = (overlap, name, df.copy(), sp)
    if best is None or best[0] < 50:
        raise RuntimeError("NO_BARRETO_TABLE_WITH_SUFFICIENT_SPECIES_OVERLAP:" + json.dumps(diagnostics))
    return best[1], best[2], best[3], diagnostics


def find_column(df: pd.DataFrame, include_sets: list[set[str]], exclude: set[str] = set()) -> str | None:
    best: tuple[int, str] | None = None
    for c in df.columns:
        n = norm_text(c)
        toks = set(n.split())
        if exclude & toks:
            continue
        for inc in include_sets:
            score = len(inc & toks)
            if score == len(inc):
                bonus = 5 if numeric_fraction(df[c]) >= 0.5 else 0
                cand = (10 * score + bonus - len(toks), str(c))
                if best is None or cand > best:
                    best = cand
    return best[1] if best else None


def speciation_columns(df: pd.DataFrame) -> dict[str, list[str]]:
    out = {"BAMM": [], "ClaDS": [], "DR": []}
    trait_words = {
        "bill", "mass", "body", "temperature", "precipitation", "elevation",
        "temp", "prec", "niche", "evolution", "evol", "trait"
    }
    for c in df.columns:
        if numeric_fraction(df[c]) < 0.5:
            continue
        n = norm_text(c)
        toks = set(n.split())
        if trait_words & toks and not ({"speciation", "diversification"} & toks):
            continue
        if "bamm" in toks and ({"speciation", "diversification", "lambda", "rate"} & toks):
            out["BAMM"].append(str(c))
        elif "clads" in toks and ({"speciation", "diversification", "lambda", "rate"} & toks):
            out["ClaDS"].append(str(c))
        elif n == "dr" or ("dr" in toks and ({"speciation", "diversification", "rate"} & toks)):
            out["DR"].append(str(c))

    # Fallback if source uses terse column names such as BAMM / ClaDS.
    for fam, token in [("BAMM", "bamm"), ("ClaDS", "clads")]:
        if not out[fam]:
            for c in df.columns:
                if token in norm_text(c).split() and numeric_fraction(df[c]) >= 0.5:
                    out[fam].append(str(c))
    return out


def choose_one_per_family(candidates: dict[str, list[str]]) -> dict[str, str]:
    chosen = {}
    for fam, cols in candidates.items():
        if not cols:
            continue
        # Prefer explicit McGuire columns, then shortest semantically focused name.
        ranked = sorted(
            cols,
            key=lambda c: (
                0 if "mcguire" in norm_text(c) else 1,
                0 if ("speciation" in norm_text(c) or "diversification" in norm_text(c)) else 1,
                len(norm_text(c)),
                norm_text(c),
            ),
        )
        chosen[fam] = ranked[0]
    return chosen


def zscore(x: pd.Series) -> pd.Series:
    x = pd.to_numeric(x, errors="coerce").astype(float)
    sd = float(x.std(ddof=0))
    if not math.isfinite(sd) or sd <= 0:
        return pd.Series(np.nan, index=x.index)
    return (x - float(x.mean())) / sd


def safe_log(x: pd.Series) -> pd.Series:
    x = pd.to_numeric(x, errors="coerce").astype(float)
    return np.log(x.where(x > 0))


def build_design(df: pd.DataFrame, covariates: dict[str, str], state_col: str, outcome_col: str):
    w = pd.DataFrame(index=df.index)
    w["outcome"] = zscore(df[outcome_col])
    w["bill"] = zscore(safe_log(df[covariates["bill"]]))
    w["mass"] = zscore(safe_log(df[covariates["mass"]]))
    w["elev"] = zscore(df[covariates["elevation"]])
    w["temp_breadth"] = zscore(df[covariates["temp_breadth"]])
    w["precip_breadth"] = zscore(df[covariates["precip_breadth"]])
    w["state"] = pd.to_numeric(df[state_col], errors="coerce")
    w["clade"] = df["analysis_clade"].astype(str)
    w["species"] = df["species"].astype(str)
    w = w.replace([np.inf, -np.inf], np.nan).dropna().copy()

    dummies = pd.get_dummies(w["clade"], prefix="clade", drop_first=True, dtype=float)
    X = np.column_stack(
        [
            np.ones(len(w)),
            w[["bill", "mass", "elev", "temp_breadth", "precip_breadth"]].to_numpy(float),
            dummies.to_numpy(float),
        ]
    )
    y = w["outcome"].to_numpy(float)
    s = w["state"].to_numpy(float)
    return w, X, y, s


def state_beta_and_permutation(
    w: pd.DataFrame,
    X: np.ndarray,
    y: np.ndarray,
    s: np.ndarray,
    permutations: int,
    seed: int,
) -> dict:
    pinv = np.linalg.pinv(X)
    y_r = y - X @ (pinv @ y)
    s_r = s - X @ (pinv @ s)
    denom = float(s_r @ s_r)
    if denom <= 1e-12:
        raise RuntimeError("STATE_NOT_IDENTIFIABLE_AFTER_BASELINE")
    beta = float((s_r @ y_r) / denom)

    rng = np.random.default_rng(seed)
    groups = {}
    for idx, clade in enumerate(w["clade"].tolist()):
        groups.setdefault(clade, []).append(idx)

    null = np.empty(permutations, dtype=float)
    for b in range(permutations):
        sp = s.copy()
        for inds in groups.values():
            vals = sp[inds].copy()
            rng.shuffle(vals)
            sp[inds] = vals
        spr = sp - X @ (pinv @ sp)
        den = float(spr @ spr)
        null[b] = np.nan if den <= 1e-12 else float((spr @ y_r) / den)
    null = null[np.isfinite(null)]
    p_one_sided_lower = float((1 + np.sum(null <= beta)) / (1 + len(null)))
    p_two_sided = float((1 + np.sum(np.abs(null) >= abs(beta))) / (1 + len(null)))
    return {
        "beta_state": beta,
        "permutation_p_lower": p_one_sided_lower,
        "permutation_p_two_sided": p_two_sided,
        "null_n": int(len(null)),
        "null_q025": float(np.quantile(null, 0.025)),
        "null_median": float(np.quantile(null, 0.5)),
        "null_q975": float(np.quantile(null, 0.975)),
    }


def analyze_state(
    joined: pd.DataFrame,
    state_col: str,
    outcomes: dict[str, str],
    covariates: dict[str, str],
    permutations: int,
    seed: int,
    exclude_coquettes: bool = False,
) -> dict:
    d = joined.copy()
    if exclude_coquettes:
        d = d[d["analysis_clade"].map(norm_text) != "coquettes"].copy()

    results = {}
    for j, (fam, col) in enumerate(sorted(outcomes.items())):
        w, X, y, s = build_design(d, covariates, state_col, col)
        res = state_beta_and_permutation(w, X, y, s, permutations, seed + 1000 * j)
        res.update(
            {
                "outcome_column": col,
                "n": int(len(w)),
                "state_1_n": int(w["state"].sum()),
                "state_0_n": int(len(w) - w["state"].sum()),
                "clades": int(w["clade"].nunique()),
            }
        )
        results[fam] = res

    betas = [v["beta_state"] for v in results.values()]
    negatives = sum(b < 0 for b in betas)
    return {
        "state": state_col,
        "exclude_coquettes": exclude_coquettes,
        "estimator_results": results,
        "median_beta": float(np.median(betas)) if betas else None,
        "negative_estimator_families": int(negatives),
        "eligible_estimator_families": int(len(betas)),
        "directional_gate_support": bool(betas and np.median(betas) < 0 and negatives >= 2),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("output")
    ap.add_argument("--permutations", type=int, default=DEFAULT_PERMUTATIONS)
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED)
    args = ap.parse_args()

    states = load_colwell_state()
    tables, figmeta = load_figshare_tables()
    fname, bdf, spcol, table_diag = choose_barreto_table(tables, states)
    bdf = bdf.copy()
    bdf["species"] = bdf[spcol].map(norm_species)

    merged = bdf.merge(states, on="species", how="inner")
    clade_candidates = [c for c in bdf.columns if norm_text(c) == "clade" or "clade" in norm_text(c)]
    if clade_candidates:
        merged["analysis_clade"] = merged[clade_candidates[0]].astype(str).str.strip()
        merged.loc[merged["analysis_clade"].eq(""), "analysis_clade"] = merged["clade_colwell"]
    else:
        merged["analysis_clade"] = merged["clade_colwell"]

    candidates = speciation_columns(bdf)
    outcomes = choose_one_per_family(candidates)
    if len(outcomes) < 2:
        raise RuntimeError(
            "INSUFFICIENT_SPECIATION_ESTIMATOR_FAMILIES:"
            + json.dumps({"candidates": candidates, "columns": list(map(str, bdf.columns))})
        )

    covariates = {
        "bill": find_column(bdf, [{"bill", "length"}, {"culmen"}, {"bill"}], exclude={"rate", "evolution", "evol"}),
        "mass": find_column(bdf, [{"body", "mass"}, {"mass"}, {"weight"}], exclude={"rate", "evolution", "evol"}),
        "elevation": find_column(bdf, [{"mid", "elevation"}, {"elevation"}], exclude={"rate", "evolution", "evol"}),
        "temp_breadth": find_column(bdf, [{"temperature", "breadth"}, {"temp", "breadth"}, {"temperature", "range"}], exclude={"rate", "evolution", "evol"}),
        "precip_breadth": find_column(bdf, [{"precipitation", "breadth"}, {"precip", "breadth"}, {"precipitation", "range"}], exclude={"rate", "evolution", "evol"}),
    }
    missing_cov = [k for k, v in covariates.items() if v is None]
    if missing_cov:
        raise RuntimeError(
            "COVARIATE_MAPPING_FAILED:"
            + json.dumps({"missing": missing_cov, "mapped": covariates, "columns": list(map(str, bdf.columns))})
        )

    primary = analyze_state(merged, "clinger_primary", outcomes, covariates, args.permutations, args.seed, False)
    no_coquettes = analyze_state(merged, "clinger_primary", outcomes, covariates, args.permutations, args.seed + 50000, True)
    bypass = analyze_state(merged, "bypass_capable", outcomes, covariates, args.permutations, args.seed + 100000, False)

    gate = (
        primary["directional_gate_support"]
        and no_coquettes["directional_gate_support"]
    )
    receipt = {
        "analysis": "ecological_stability_evolutionary_transience_gate_a",
        "prereg_version": "V2_AMENDMENT",
        "seed": args.seed,
        "permutations": args.permutations,
        "sources": {
            "colwell_s1": COLWELL_S1_URL,
            "barreto_figshare_api": FIGSHARE_API,
            "barreto_selected_file": fname,
            "barreto_species_column": str(spcol),
            "figshare_manifest": figmeta,
        },
        "join_audit": {
            "colwell_species": int(states["species"].nunique()),
            "colwell_clingers": int(states["clinger"].sum()),
            "colwell_presumed_nonclingers": int((states["clinger_primary"] == 0).sum()),
            "colwell_onwing_pierce_only": int(states["onwing_pierce_only"].sum()),
            "colwell_bypass_capable": int(states["bypass_capable"].sum()),
            "barreto_rows": int(len(bdf)),
            "barreto_species": int(bdf["species"].nunique()),
            "joined_species": int(merged["species"].nunique()),
            "joined_clingers": int(merged["clinger"].sum()),
            "joined_primary_nonclingers": int((merged["clinger_primary"] == 0).sum()),
            "joined_onwing_pierce_only": int(merged["onwing_pierce_only"].sum()),
            "joined_bypass_capable": int(merged["bypass_capable"].sum()),
        },
        "schema": {
            "speciation_candidates": candidates,
            "chosen_outcomes": outcomes,
            "covariates": covariates,
            "clade_source": str(clade_candidates[0]) if clade_candidates else "Colwell S1",
            "table_diagnostics": table_diag,
        },
        "primary_clinger": primary,
        "sensitivity_exclude_coquettes": no_coquettes,
        "secondary_bypass_capable": bypass,
        "gate_a_pass": bool(gate),
        "decision": (
            "PROCEED_TO_GATE_B"
            if gate
            else "KILL_TRANSIENCE_HYPOTHESIS_UNDER_FROZEN_GATE"
        ),
        "claim_boundary": (
            "Gate A is a clade-stratified association using independently published "
            "species-level speciation estimates. It is not a causal state-dependent "
            "diversification analysis. Gate B explicit phylogenetic confirmation is "
            "required before any promotion."
        ),
    }
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({
        "join_audit": receipt["join_audit"],
        "chosen_outcomes": outcomes,
        "covariates": covariates,
        "primary": {
            fam: {
                "beta": x["beta_state"],
                "p_lower": x["permutation_p_lower"],
                "n": x["n"],
            }
            for fam, x in primary["estimator_results"].items()
        },
        "primary_median_beta": primary["median_beta"],
        "primary_negative_families": primary["negative_estimator_families"],
        "exclude_coquettes_median_beta": no_coquettes["median_beta"],
        "gate_a_pass": receipt["gate_a_pass"],
        "decision": receipt["decision"],
    }, indent=2))


if __name__ == "__main__":
    main()
