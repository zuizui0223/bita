from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__)
WORKFLOW = ROOT / ".github" / "workflows" / "_reviewer-a-f-patch-tmp.yml"


def replace_once(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match in {path}, got {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


# A — reconnect the imported Leal module to the current broad-meta contract.
broad = ROOT / "trait_architecture" / "broad_meta_analysis.py"
replace_once(
    broad,
    '''DIRECT_ROUTES = frozenset({
    "A_to_pollination",
    "A_to_antagonism",
    "B_to_antagonism",
    "B_to_pollination",
})''',
    '''DIRECT_ROUTES = frozenset({
    "A_to_pollination",
    "A_to_antagonism",
    "B_to_antagonism",
    "B_to_pollination",
    "H_to_fitness",
    "H_to_pollination",
    "H_to_reward",
})''',
    "add larceny H routes",
)
replace_once(
    broad,
    '''ROUTE_TRAIT_ROLE = {
    "A_to_pollination": "A",
    "A_to_antagonism": "A",
    "B_to_antagonism": "B",
    "B_to_pollination": "B",
}''',
    '''ROUTE_TRAIT_ROLE = {
    "A_to_pollination": "A",
    "A_to_antagonism": "A",
    "B_to_antagonism": "B",
    "B_to_pollination": "B",
    "H_to_fitness": "H",
    "H_to_pollination": "H",
    "H_to_reward": "H",
}''',
    "add larceny H roles",
)
replace_once(
    broad,
    '''ROUTE_EXPECTED_SIGN = {
    "A_to_pollination": "positive",
    "A_to_antagonism": "positive",
    "B_to_antagonism": "negative",
    "B_to_pollination": "negative",
}''',
    '''ROUTE_EXPECTED_SIGN = {
    "A_to_pollination": "positive",
    "A_to_antagonism": "positive",
    "B_to_antagonism": "negative",
    "B_to_pollination": "negative",
    "H_to_fitness": "negative",
    "H_to_pollination": "negative",
    "H_to_reward": "negative",
}''',
    "add larceny H expected signs",
)

strata = ROOT / "empirical" / "broad_reality_evidence" / "broad_meta_analysis_strata.csv"
text = strata.read_text(encoding="utf-8")
larceny_rows = '''HF_larceny_female_lrr_comparative,H_to_fitness,nectar_larceny,female_reproductive_success,log_response_ratio,comparative,3,5,negative,H,Exposure to nectar larceny relative to an unexposed control is associated with lower female reproductive success; under bridge assumption B2 a non-zero negative pooled effect is what opens the multiplicative H gate on the antagonist-relief channel
HP_larceny_visitation_lrr_comparative,H_to_pollination,nectar_larceny,visitation_rate,log_response_ratio,comparative,3,5,negative,P_exogeneity_audit,Exposure to nectar larceny relative to an unexposed control is associated with lower legitimate visitation; this is an audit of the corollary's assumption that pollinator service P is exogenous to antagonist pressure H and is not a channel estimate
HR_larceny_nectar_lrr_comparative,H_to_reward,nectar_larceny,nectar_standing_crop,log_response_ratio,comparative,3,5,negative,H_mechanism,Exposure to nectar larceny relative to an unexposed control is associated with lower nectar standing crop; the declared mechanism linking the larceny exposure to any change in visitation
HF_larceny_male_lrr_comparative,H_to_fitness,nectar_larceny,male_reproductive_success,log_response_ratio,comparative,3,5,negative,H,Exposure to nectar larceny relative to an unexposed control is associated with lower male reproductive success; the secondary fitness component of the same H gate
'''
if "HF_larceny_female_lrr_comparative" not in text:
    if not text.endswith("\n"):
        text += "\n"
    strata.write_text(text + larceny_rows, encoding="utf-8")

# B/C/D/E/F — manuscript corrections.
manuscript = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"
replace_once(
    manuscript,
    "Across 2,592 declared evaluations and four response-shape variants we find no counterexample, whereas about 23% of points inside this selectivity window remain substitutable, so the window is necessary but not sufficient.",
    "We prove this implication algebraically, then use 2,592 declared evaluations across four response-shape variants to verify the implementation and quantify the bound's looseness: about 23% of points inside this selectivity window remain substitutable, so the window is necessary but not sufficient.",
    "abstract proof-versus-grid wording",
)
replace_once(
    manuscript,
    "**Theorem 1 (one-sided selectivity bound).** If the three deployed terms are non-negative, then",
    "**Theorem 1 (one-sided selectivity bound).** If direct joint-cost curvature is non-negative, \\(\\kappa\\ge0\\), then",
    "theorem premise",
)
replace_once(
    manuscript,
    "The proof uses only the non-negative relief-minus-interference-minus-cost structure, preserved by all four declared endpoint-normalized response-shape variants. When \\(\\kappa=0\\), the implication runs both ways and the window becomes the exact sign criterion.",
    "The proof uses only the additive relief-minus-interference-minus-cost structure and \\(\\kappa\\ge0\\), preserved by all four declared endpoint-normalized response-shape variants. The signs of \\(\\rho\\) and \\(\\iota\\) are not used by this implication; their non-negativity belongs to the oriented baseline interpretation rather than to Theorem 1 itself. When \\(\\kappa=0\\), the implication runs both ways and the window becomes the exact sign criterion.",
    "theorem proof assumption scope",
)
replace_once(
    manuscript,
    "During analysis and manuscript development, an OpenAI large language model was used to assist code generation, structured literature triage, and manuscript drafting.",
    "During analysis and manuscript development, large language models from OpenAI and Anthropic were used to assist code generation, structured literature triage, reproducibility checks, and manuscript drafting and editing.",
    "AI disclosure providers",
)
replace_once(
    manuscript,
    "Fourteen same-system clusters show that routes can co-occur, while 17 sign/state-switch clusters and seven context-only programs show that trait intensity, resources, exposure, consumer identity, attack geometry, response stage, population, visitor functional mode, and even consumer lifecycle can change which channel is expressed.",
    "Fourteen same-system clusters show that routes can co-occur, while 17 sign/state-switch clusters and seven context-only programs show that trait intensity, resources, exposure, consumer identity, attack geometry, response stage, population, visitor functional mode, and even consumer lifecycle can change which channel is expressed. These annotations are not additive counts: same-system and sign/state-switch classifications can overlap within the 25-cluster route universe, while the seven context-only programs are explicitly outside route-ledger N.",
    "overlapping empirical categories",
)
replace_once(
    manuscript,
    "The two reproduced quantitative syntheses retain their principal direction under their declared influence checks. The three secondary contextual syntheses independently reinforce strong tissue, consumer, trait-class, assay, and selection-context dependence, but remain explicitly separated by evidence status and effect scale.",
    "The Leal pooled directions retain their declared influence and sensitivity checks. The Sasidharan assembled contrast remains positive in all leave-one-study-component-out refits, but this is robustness of the assembled cross-study composition rather than a within-study consumer-role effect: only three study components contain both physiological roles and all three paired differences are zero. The three secondary contextual syntheses independently reinforce strong tissue, consumer, trait-class, assay, and selection-context dependence, but remain explicitly separated by evidence status and effect scale.",
    "Sasidharan synthesis boundary",
)
replace_once(
    manuscript,
    "All code, declared configurations, generated readouts, source-adjudication products, saturation receipts, and validation tests required for the fixed theory, finite sensitivity analysis, and saturated mechanism-Pattern synthesis are maintained in the associated repository. The completed Leal et al. (2025) larceny module is pinned to immutable repository commit `ed33b25593c0d90ad6657753f6f5501d9efc7b82`; the Sasidharan et al. (2023) module uses the 32-component citation topology as its canonical dependence structure.",
    "All code, declared configurations, generated readouts, source-adjudication products, saturation receipts, and validation tests required for the fixed theory, finite sensitivity analysis, and saturated mechanism-Pattern synthesis are maintained in the associated repository. The complete Leal et al. (2025) larceny module, including its effect rows, moderator coding, context-dependence implementation, committed results, and integrity tests, is included directly in the canonical repository tree; its provenance is additionally pinned to immutable commit `ed33b25593c0d90ad6657753f6f5501d9efc7b82`. The Sasidharan et al. (2023) module uses the 32-component citation topology as its canonical dependence structure.",
    "data availability local Leal assets",
)

# B — keep theorem guardrails and derivation docs aligned.
claim = ROOT / "manuscript" / "CLAIM_FREEZE.md"
replace_once(
    claim,
    "Within the declared relief-minus-interference-minus-cost family, if the three oriented terms are non-negative,",
    "Within the declared relief-minus-interference-minus-cost family, if direct joint-cost curvature is non-negative (`kappa >= 0`),",
    "claim freeze theorem premise",
)
replace_once(
    claim,
    "Therefore complementarity cannot occur outside the selectivity window.\n\nThe converse is not claimed.",
    "Therefore complementarity cannot occur outside the selectivity window. The signs of `rho` and `iota` are not required for this implication; their non-negative magnitude interpretation belongs to the orientation gate used by the baseline mechanism.\n\nThe converse is not claimed.",
    "claim freeze theorem clarification",
)

bound = ROOT / "docs" / "SELECTIVITY_WINDOW_BOUND.md"
replace_once(
    bound,
    "> **Theorem.** If all three terms are non-negative, then `W_AD > 0` implies the point is inside the\n> selectivity window. Equivalently: **complementarity never occurs outside the window.**",
    "> **Theorem.** If `joint_cost_curvature_term >= 0`, then `W_AD > 0` implies the point is inside the\n> selectivity window. Equivalently: **complementarity never occurs outside the window.**",
    "bound theorem premise",
)
replace_once(
    bound,
    "`baseline`, `saturating_attraction`, `saturating_defence`, `saturating_both_curved_cost` — preserve\nthe `relief − interference − cost` structure with all three terms non-negative. The proof uses only\nthat structure, so it holds under every variant rather than only the baseline exponential form.",
    "`baseline`, `saturating_attraction`, `saturating_defence`, `saturating_both_curved_cost` — preserve\nthe additive `relief − interference − cost` structure with non-negative joint-cost curvature. The proof\nuses only that additive structure and the sign of the joint-cost term; relief and interference need not\nbe non-negative for the implication itself. It therefore holds under every declared variant rather than\nonly the baseline exponential form.",
    "bound form-independence premise",
)
replace_once(
    bound,
    "- The theorem is about **this corollary's functional family**. It uses only that the three terms are\n  non-negative and enter as `relief − interference − cost`. A model where interference can be\n  negative still satisfies it (the window condition then holds automatically), but a model with a\n  different additive structure is not covered.",
    "- The theorem is about the declared additive `relief − interference − cost` structure. It requires\n  only `joint_cost_curvature_term >= 0`; the signs of relief and interference are not premises of the\n  implication. A model where interference is negative can therefore still satisfy the theorem, while a\n  model with a different additive structure is not covered.",
    "bound boundary premise",
)

# D/A — update live manifest from external-only pin to canonical local reproducibility.
manifest = ROOT / "SUPPLEMENT_MANIFEST.md"
replace_once(
    manifest,
    "The completed module is pinned to immutable repository provenance:",
    "The completed module is included directly in the canonical repository tree and is also pinned to immutable provenance:",
    "manifest local Leal module",
)
replace_once(
    manifest,
    "Canonical source/result products at the immutable commit include:",
    "Canonical source/result products now present in the current tree, with provenance traced to that immutable commit, include:",
    "manifest Leal source location",
)
replace_once(
    manifest,
    "- associated analysis scripts and tests.",
    "- `scripts/run_larceny_gate.py`, `scripts/run_context_dependence.py`, and `trait_architecture/context_dependence.py`;\n- integrity tests for effect ingestion, context dependence, and the declared larceny gate.",
    "manifest Leal code paths",
)

# A — require the restored module in the active submission scope.
scope = ROOT / "tests" / "test_submission_scope.py"
replace_once(
    scope,
    '''    "scripts/run_broad_meta_analysis.py",
    "scripts/validate_current_theory_meta.py",
]''',
    '''    "scripts/run_broad_meta_analysis.py",
    "scripts/validate_current_theory_meta.py",
    # Canonical Leal larceny module used by the manuscript's H-gate claims.
    "empirical/broad_reality_evidence/larceny_gate/LARCENY_GATE_PROTOCOL_V1.md",
    "empirical/broad_reality_evidence/larceny_gate/LARCENY_GATE_READOUT_V1.md",
    "empirical/broad_reality_evidence/larceny_gate/larceny_effect_rows.csv",
    "empirical/broad_reality_evidence/larceny_gate/larceny_moderator_coding.csv",
    "empirical/broad_reality_evidence/larceny_gate/larceny_moderator_registry.csv",
    "empirical/broad_reality_evidence/larceny_gate/results/larceny_pooled_summary.csv",
    "empirical/broad_reality_evidence/larceny_gate/results/context_meta_regression_models.csv",
    "scripts/ingest_deposited_larceny_dataset.py",
    "scripts/run_larceny_gate.py",
    "scripts/run_context_dependence.py",
    "trait_architecture/context_dependence.py",
    "trait_architecture/deposited_effect_ingest.py",
    "tests/test_larceny_gate_declaration.py",
]''',
    "submission scope Leal required paths",
)

# Make the modern-estimator sensitivity consume the canonical local copy while retaining the immutable provenance pin.
modern = ROOT / "scripts" / "run_leal_modern_estimator_sensitivity.py"
replace_once(
    modern,
    "It reuses the already cluster-aggregated contributing\neffects from that commit and asks whether the three informative directions remain",
    "The canonical contributing effects are now present in the current repository tree with provenance\npinned to that commit. This script reads the local canonical copy and asks whether the three informative directions remain",
    "modern sensitivity docstring local copy",
)
replace_once(
    modern,
    "    text = _git_show(PINNED_COMMIT, PINNED_PATH)\n",
    "    local_path = ROOT / PINNED_PATH\n    if not local_path.is_file():\n        raise FileNotFoundError(f\"canonical Leal contributing effects missing: {local_path}\")\n    text = local_path.read_text(encoding=\"utf-8\")\n",
    "modern sensitivity local read",
)

# Remove the one-time mutation machinery from the final tree.
if WORKFLOW.exists():
    WORKFLOW.unlink()
if SELF.exists():
    SELF.unlink()
