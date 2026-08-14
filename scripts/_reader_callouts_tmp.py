from pathlib import Path

MANUSCRIPT = Path("manuscript/MANUSCRIPT_THEORETICAL_ECOLOGY.md")
WORKFLOW = Path(".github/workflows/_reader-callouts-tmp.yml")
SCRIPT = Path(__file__)

text = MANUSCRIPT.read_text(encoding="utf-8")

needle1 = "This oriented form is valid only after the orientation gate has been justified for the focal application.\n\n### 2.4 Mechanism non-identifiability"
replacement1 = "This oriented form is valid only after the orientation gate has been justified for the focal application. The channel architecture, orientation gate, and inference boundary are summarized in Fig. 1 and Table 1.\n\n### 2.4 Mechanism non-identifiability"
if needle1 not in text:
    raise SystemExit("missing callout insertion marker 1")
text = text.replace(needle1, replacement1, 1)

needle2 = "These fractions are unweighted finite-grid occupancies, not estimates of natural prevalence. Their role is to distinguish an exact structural implication from the false two-sided rule that the finite design itself rejects.\n\n## 4. Part II — Meta-analysis and cross-study pattern synthesis"
replacement2 = "These fractions are unweighted finite-grid occupancies, not estimates of natural prevalence. Their role is to distinguish an exact structural implication from the false two-sided rule that the finite design itself rejects. The finite design and its regime/verification readout are summarized in Fig. 2 and Table 2; analytic-versus-finite-difference checks and scenario-specific maps are provided in Supplementary Figs. S1–S2 and Tables S1–S2.\n\n## 4. Part II — Meta-analysis and cross-study pattern synthesis"
if needle2 not in text:
    raise SystemExit("missing callout insertion marker 2")
text = text.replace(needle2, replacement2, 1)

needle3 = "The two reproduced quantitative syntheses retain their principal direction under their declared influence checks. The three secondary contextual syntheses independently reinforce strong tissue, consumer, trait-class, assay, and selection-context dependence, but remain explicitly separated by evidence status and effect scale. Direct \\(A\\times D\\) remains one sign-unresolved strict cluster, and direct joint-cost evidence remains zero strict estimates. The meta-analytic Pattern is therefore **recurrent mechanisms plus context-dependent balance**, not a universal value or sign of \\(W_{AD}\\).\n\n## 6. Integration — from mechanism to pattern"
replacement3 = "The two reproduced quantitative syntheses retain their principal direction under their declared influence checks. The three secondary contextual syntheses independently reinforce strong tissue, consumer, trait-class, assay, and selection-context dependence, but remain explicitly separated by evidence status and effect scale. Direct \\(A\\times D\\) remains one sign-unresolved strict cluster, and direct joint-cost evidence remains zero strict estimates. The meta-analytic Pattern is therefore **recurrent mechanisms plus context-dependent balance**, not a universal value or sign of \\(W_{AD}\\). The cross-system evidence architecture is summarized in Fig. 3 and Table 3, with the quantitative modules in Table 4; full route, conditionality, direct-identification, and stopping-rule records are provided in Tables S3–S6, with same-system and module-robustness displays in Supplementary Figs. S3–S4.\n\n## 6. Integration — from mechanism to pattern"
if needle3 not in text:
    raise SystemExit("missing callout insertion marker 3")
text = text.replace(needle3, replacement3, 1)

MANUSCRIPT.write_text(text, encoding="utf-8")

if WORKFLOW.exists():
    WORKFLOW.unlink()
if SCRIPT.exists():
    SCRIPT.unlink()
