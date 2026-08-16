from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "trait_architecture" / "broad_meta_analysis.py"
SELF = Path(__file__)
WORKFLOW = ROOT / ".github" / "workflows" / "_restore-random-effects-api-tmp.yml"

text = TARGET.read_text(encoding="utf-8")
needle = '''    return {
        "pooled_effect": pooled,
        "pooled_standard_error": pooled_se,
        "ci_low": pooled - Z_975 * pooled_se,
        "ci_high": pooled + Z_975 * pooled_se,
        "z_value": z_value,
        "two_sided_p_value": p_value,
        "tau_squared_DL": tau_squared,
        "Q": q,
        "Q_df": float(df),
        "I_squared_percent": i_squared,
    }


def _matches_stratum'''
replacement = '''    return {
        "pooled_effect": pooled,
        "pooled_standard_error": pooled_se,
        "ci_low": pooled - Z_975 * pooled_se,
        "ci_high": pooled + Z_975 * pooled_se,
        "z_value": z_value,
        "two_sided_p_value": p_value,
        "tau_squared_DL": tau_squared,
        "Q": q,
        "Q_df": float(df),
        "I_squared_percent": i_squared,
    }


def random_effects_pool(estimates: list[EffectEstimate]) -> dict[str, float]:
    """Public compatibility API for one already-compatible effect set.

    The canonical Leal context-dependence module uses this public function.
    Keep the implementation delegated to the same current DerSimonian-Laird
    routine used by ``meta_analysis`` so the wrapper cannot drift numerically.
    """

    return _der_simonian_laird(estimates)


def _matches_stratum'''
if text.count(needle) != 1:
    raise RuntimeError(f"expected one DerSimonian-Laird insertion point, got {text.count(needle)}")
TARGET.write_text(text.replace(needle, replacement, 1), encoding="utf-8")

if WORKFLOW.exists():
    WORKFLOW.unlink()
if SELF.exists():
    SELF.unlink()
