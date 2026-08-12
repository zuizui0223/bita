from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manuscript = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"
marker = "The saturated source-adjudicated route ledger contained 56 effect or directional records across 25 independent biological study clusters."

if marker in manuscript.read_text(encoding="utf-8"):
    print("Pattern manuscript promotion already applied")
else:
    from promote_pattern_expansion_to_manuscript_v2 import main
    main()
