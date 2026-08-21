from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "tests" / "test_manuscript_references.py"
SELF = Path(__file__)
text = PATH.read_text(encoding="utf-8")
old = '    refs = after_refs.split("\\n## Statements and Declarations\\n", 1)[0]\n'
new = ('    if "\\n## Acknowledgments\\n" in after_refs:\n'
       '        refs = after_refs.split("\\n## Acknowledgments\\n", 1)[0]\n'
       '    else:\n'
       '        refs = after_refs.split("\\n## Statements and Declarations\\n", 1)[0]\n')
if text.count(old) != 1:
    raise RuntimeError(f"reference parser target count={text.count(old)}")
PATH.write_text(text.replace(old, new, 1), encoding="utf-8")
SELF.unlink()
