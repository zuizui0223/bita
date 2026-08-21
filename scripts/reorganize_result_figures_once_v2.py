from pathlib import Path

p = Path(__file__).with_name("reorganize_result_figures_once.py")
s = p.read_text(encoding="utf-8")
replacements = {
    "caption_pattern.subn(replacement, text, count=1)": "caption_pattern.subn(lambda _m: replacement, text, count=1)",
    "pattern.subn(replacement, text, count=1)": "pattern.subn(lambda _m: replacement, text, count=1)",
    "fig_block.subn(new_fig_block, text, count=1)": "fig_block.subn(lambda _m: new_fig_block, text, count=1)",
    "old_test.subn(new_test, text, count=1)": "old_test.subn(lambda _m: new_test, text, count=1)",
}
for old, new in replacements.items():
    if old not in s:
        raise RuntimeError(f"missing patch target: {old}")
    s = s.replace(old, new)
p.write_text(s, encoding="utf-8")
exec(compile(s, str(p), "exec"), {"__name__": "__main__", "__file__": str(p)})
