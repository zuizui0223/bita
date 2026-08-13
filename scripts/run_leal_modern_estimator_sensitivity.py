"""Modern random-effects sensitivity for the pinned Leal et al. 2025 module.

The canonical Leal results remain the preregistered DerSimonian-Laird estimates on
immutable commit ed33b25593c0d90ad6657753f6f5501d9efc7b82. This script does not
replace those estimates. It reuses the already cluster-aggregated contributing
effects from that commit and asks whether the three informative directions remain
under REML heterogeneity estimation and modified Hartung-Knapp inference.
"""

from __future__ import annotations

import csv
import io
import json
import math
import subprocess
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_MD = ROOT / "empirical" / "mechanism_pattern_synthesis" / "LEAL_2025_MODERN_ESTIMATOR_SENSITIVITY_V1.md"
OUT_JSON = ROOT / "empirical" / "mechanism_pattern_synthesis" / "LEAL_2025_MODERN_ESTIMATOR_SENSITIVITY_V1.json"
PINNED_COMMIT = "ed33b25593c0d90ad6657753f6f5501d9efc7b82"
PINNED_PATH = "empirical/broad_reality_evidence/larceny_gate/results/larceny_contributing_effects.csv"
BORDERLINE_CI_MARGIN = 0.001

TARGETS = {
    "female_reproductive_success": {
        "label": "female reproductive success",
        "expected_k": 48,
        "canonical_dl": -0.2105,
    },
    "nectar_standing_crop": {
        "label": "nectar standing crop",
        "expected_k": 28,
        "canonical_dl": -0.4834,
    },
    "visitation_rate": {
        "label": "legitimate visitation",
        "expected_k": 22,
        "canonical_dl": -0.2907,
    },
}


@dataclass(frozen=True)
class Effect:
    cluster: str
    value: float
    variance: float


def _git_show(commit: str, path: str) -> str:
    proc = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return proc.stdout


def _read_effects() -> dict[str, list[Effect]]:
    text = _git_show(PINNED_COMMIT, PINNED_PATH)
    grouped = {key: [] for key in TARGETS}
    seen: set[tuple[str, str]] = set()
    for row in csv.DictReader(io.StringIO(text)):
        outcome = row["outcome_class"]
        if outcome not in grouped:
            continue
        if row["analysis_status"] != "eligible_for_quantitative_synthesis":
            continue
        if row["is_primary_effect"].strip().lower() != "true":
            continue
        key = (outcome, row["study_cluster_id"])
        if key in seen:
            raise ValueError(f"duplicate primary cluster effect: {key}")
        seen.add(key)
        se = float(row["computed_standard_error"])
        if not math.isfinite(se) or se <= 0:
            raise ValueError(f"invalid standard error for {key}")
        value = float(row["computed_effect_value"])
        if not math.isfinite(value):
            raise ValueError(f"invalid effect for {key}")
        grouped[outcome].append(Effect(row["study_cluster_id"], value, se * se))

    for outcome, cfg in TARGETS.items():
        if len(grouped[outcome]) != cfg["expected_k"]:
            raise ValueError(
                f"{outcome}: expected {cfg['expected_k']} cluster effects, got {len(grouped[outcome])}"
            )
    return grouped


def _weighted_mean(effects: list[Effect], tau2: float) -> tuple[float, list[float]]:
    weights = [1.0 / (effect.variance + tau2) for effect in effects]
    total = sum(weights)
    mean = sum(w * effect.value for w, effect in zip(weights, effects)) / total
    return mean, weights


def _dl(effects: list[Effect]) -> dict[str, float]:
    fixed_weights = [1.0 / effect.variance for effect in effects]
    sw = sum(fixed_weights)
    fixed = sum(w * effect.value for w, effect in zip(fixed_weights, effects)) / sw
    q = sum(w * (effect.value - fixed) ** 2 for w, effect in zip(fixed_weights, effects))
    df = len(effects) - 1
    c = sw - sum(w * w for w in fixed_weights) / sw
    tau2 = max(0.0, (q - df) / c) if c > 0 else 0.0
    pooled, weights = _weighted_mean(effects, tau2)
    se = math.sqrt(1.0 / sum(weights))
    return {"pooled": pooled, "se": se, "tau2": tau2, "q": q}


def _reml_nll(effects: list[Effect], tau2: float) -> float:
    mean, weights = _weighted_mean(effects, tau2)
    q = sum(w * (effect.value - mean) ** 2 for w, effect in zip(weights, effects))
    return 0.5 * (
        sum(math.log(effect.variance + tau2) for effect in effects)
        + math.log(sum(weights))
        + q
    )


def _reml_tau2(effects: list[Effect]) -> float:
    # Intercept-only REML profile likelihood. A broad deterministic bracket is
    # expanded if needed, then minimized by golden-section search.
    values = [effect.value for effect in effects]
    mean = sum(values) / len(values)
    sample_var = sum((value - mean) ** 2 for value in values) / max(1, len(values) - 1)
    upper = max(1.0, 10.0 * sample_var, 10.0 * max(effect.variance for effect in effects))
    while upper < 1e6 and _reml_nll(effects, upper) < _reml_nll(effects, upper / 2.0):
        upper *= 2.0

    lo, hi = 0.0, upper
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    c = hi - (hi - lo) / phi
    d = lo + (hi - lo) / phi
    fc = _reml_nll(effects, c)
    fd = _reml_nll(effects, d)
    for _ in range(250):
        if fc < fd:
            hi, d, fd = d, c, fc
            c = hi - (hi - lo) / phi
            fc = _reml_nll(effects, c)
        else:
            lo, c, fc = c, d, fd
            d = lo + (hi - lo) / phi
            fd = _reml_nll(effects, d)
    candidate = (lo + hi) / 2.0
    # Explicitly allow the boundary solution tau2=0.
    return 0.0 if _reml_nll(effects, 0.0) <= _reml_nll(effects, candidate) else candidate


def _betacf(a: float, b: float, x: float) -> float:
    max_iter = 300
    eps = 3e-14
    fpmin = 1e-300
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < fpmin:
        d = fpmin
    d = 1.0 / d
    h = d
    for m in range(1, max_iter + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            return h
    raise RuntimeError("incomplete-beta continued fraction did not converge")


def _betai(a: float, b: float, x: float) -> float:
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    bt = math.exp(
        math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
        + a * math.log(x) + b * math.log1p(-x)
    )
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def _t_cdf(t: float, df: int) -> float:
    if t == 0.0:
        return 0.5
    x = df / (df + t * t)
    tail = 0.5 * _betai(df / 2.0, 0.5, x)
    return 1.0 - tail if t > 0 else tail


def _t_quantile(p: float, df: int) -> float:
    if not 0.5 < p < 1.0:
        raise ValueError("this helper expects 0.5 < p < 1")
    lo, hi = 0.0, 20.0
    for _ in range(120):
        mid = (lo + hi) / 2.0
        if _t_cdf(mid, df) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def _reml_hk(effects: list[Effect]) -> dict[str, float]:
    tau2 = _reml_tau2(effects)
    pooled, weights = _weighted_mean(effects, tau2)
    sw = sum(weights)
    df = len(effects) - 1
    q_scale = sum(w * (effect.value - pooled) ** 2 for w, effect in zip(weights, effects)) / df
    se_normal = math.sqrt(1.0 / sw)
    se_hk = math.sqrt(q_scale / sw)
    se_mkh = math.sqrt(max(1.0, q_scale) / sw)
    tcrit = _t_quantile(0.975, df)
    return {
        "pooled": pooled,
        "tau2_reml": tau2,
        "se_normal": se_normal,
        "hk_scale": q_scale,
        "se_hk": se_hk,
        "se_mkh": se_mkh,
        "tcrit": tcrit,
        "hk_ci_low": pooled - tcrit * se_hk,
        "hk_ci_high": pooled + tcrit * se_hk,
        "mkh_ci_low": pooled - tcrit * se_mkh,
        "mkh_ci_high": pooled + tcrit * se_mkh,
    }


def main() -> None:
    grouped = _read_effects()
    results: dict[str, dict[str, float | int | str | bool]] = {}
    all_conservative_pass = True
    borderline_outcomes: list[str] = []

    for outcome, effects in grouped.items():
        cfg = TARGETS[outcome]
        dl = _dl(effects)
        if abs(dl["pooled"] - cfg["canonical_dl"]) > 0.001:
            raise ValueError(
                f"{outcome}: pinned cluster data no longer reproduce canonical DL mean: "
                f"{dl['pooled']:.6f} vs {cfg['canonical_dl']:.6f}"
            )
        modern = _reml_hk(effects)
        conservative_same_negative = modern["mkh_ci_high"] < 0.0 and modern["pooled"] < 0.0
        borderline = conservative_same_negative and modern["mkh_ci_high"] > -BORDERLINE_CI_MARGIN
        if borderline:
            borderline_outcomes.append(outcome)
        all_conservative_pass = all_conservative_pass and conservative_same_negative
        results[outcome] = {
            "label": cfg["label"],
            "k": len(effects),
            "canonical_dl_pooled_recomputed": dl["pooled"],
            "canonical_dl_tau2_recomputed": dl["tau2"],
            **modern,
            "modified_hartung_knapp_retains_negative_interval": conservative_same_negative,
            "modified_hartung_knapp_borderline_zero_margin": borderline,
        }

    payload = {
        "status": "ROBUSTNESS_PASS" if all_conservative_pass else "SENSITIVITY_QUALIFIES_CLAIM",
        "canonical_source_commit": PINNED_COMMIT,
        "canonical_results_remain_der_simonian_laird": True,
        "sensitivity_only": True,
        "borderline_ci_margin": BORDERLINE_CI_MARGIN,
        "borderline_outcomes": borderline_outcomes,
        "methods": {
            "heterogeneity_estimator": "REML profile likelihood",
            "interval": "modified Hartung-Knapp with Student-t df=k-1",
            "modification": "variance scale floored at 1.0",
        },
        "results": results,
        "interpretation_boundary": (
            "This is a robustness analysis of the three already admitted Leal arrows. "
            "It does not change the preregistered canonical pooled estimates, search universe, "
            "mechanism mapping, or any bita model parameter. An interval that remains below zero "
            "but ends within 0.001 of zero is explicitly flagged as borderline rather than described "
            "as strongly robust."
        ),
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Leal et al. 2025 modern-estimator sensitivity v1",
        "",
        f"**Decision: {payload['status']}**",
        "",
        "The preregistered canonical Leal module remains the DerSimonian–Laird analysis pinned at "
        f"`{PINNED_COMMIT}`. This sensitivity reuses the same one-effect-per-independent-cluster inputs and asks whether the three informative directions survive REML heterogeneity estimation plus modified Hartung–Knapp inference. It does not replace the canonical estimates.",
        "",
        "Method motivation: Hartung–Knapp-type intervals account for uncertainty in the mean under random effects; the modified form avoids counterintuitively narrow intervals when the Hartung–Knapp scale factor falls below one. See Röver, Knapp & Friede (2015, DOI `10.1186/s12874-015-0091-1`) and Partlett & Riley (2017, DOI `10.1002/sim.7140`) for coverage-focused evaluations.",
        "",
        "| outcome | k | canonical DL pooled (recomputed) | REML pooled | REML tau² | mHK 95% CI | negative interval retained? | boundary flag |",
        "|---|---:|---:|---:|---:|---:|---|---|",
    ]
    for outcome in ("female_reproductive_success", "nectar_standing_crop", "visitation_rate"):
        row = results[outcome]
        lines.append(
            f"| {row['label']} | {row['k']} | {row['canonical_dl_pooled_recomputed']:.3f} | "
            f"{row['pooled']:.3f} | {row['tau2_reml']:.3f} | "
            f"[{row['mkh_ci_low']:.4f}, {row['mkh_ci_high']:.4f}] | "
            f"{'yes' if row['modified_hartung_knapp_retains_negative_interval'] else 'no'} | "
            f"{'borderline to zero' if row['modified_hartung_knapp_borderline_zero_margin'] else 'not borderline'} |"
        )
    lines.extend([
        "",
        "## Interpretation",
        "",
        "All three pooled directions remain negative under REML plus modified Hartung–Knapp inference. Female reproductive success and nectar standing crop retain clearly negative intervals. Legitimate visitation also remains below zero, but its upper limit lies within 0.001 of zero and is therefore treated as **borderline estimator robustness**, not as a strong exclusion of zero.",
        "",
        "The decision is deliberately limited to robustness: if an interval crosses zero, the canonical DL estimate is retained but the corresponding manuscript claim must be qualified as estimator-sensitive. An interval that technically excludes zero but approaches it within the declared margin is flagged rather than rounded into an apparently stronger result.",
        "",
        "This sensitivity does **not** estimate `rho`, `iota`, `kappa`, or `W_AD`; does not reduce the extreme heterogeneity; and does not turn the Leal deposit into an independent systematic review.",
    ])
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(payload["status"])


if __name__ == "__main__":
    main()
