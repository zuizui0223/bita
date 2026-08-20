from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"
WF = ROOT / ".github" / "workflows" / "_reference-order-tmp.yml"
SELF = Path(__file__)
text = MAN.read_text(encoding="utf-8")
old = '''Junker RR, Blüthgen N (2010) Floral scents repel facultative flower visitors, but attract obligate ones. *Annals of Botany* 105:777–782. https://doi.org/10.1093/aob/mcq045

Johnson CA, Smith GP, Yule K, Davidowitz G, Bronstein JL, Ferrière R (2021) Coevolutionary transitions from antagonism to mutualism explained by the Co-Opted Antagonist Hypothesis. *Nature Communications* 12:2867. https://doi.org/10.1038/s41467-021-23177-x
'''
new = '''Johnson CA, Smith GP, Yule K, Davidowitz G, Bronstein JL, Ferrière R (2021) Coevolutionary transitions from antagonism to mutualism explained by the Co-Opted Antagonist Hypothesis. *Nature Communications* 12:2867. https://doi.org/10.1038/s41467-021-23177-x

Junker RR, Blüthgen N (2010) Floral scents repel facultative flower visitors, but attract obligate ones. *Annals of Botany* 105:777–782. https://doi.org/10.1093/aob/mcq045
'''
if text.count(old) != 1:
    raise RuntimeError(f"reference-order target count={text.count(old)}")
MAN.write_text(text.replace(old, new, 1), encoding="utf-8")
if WF.exists():
    WF.unlink()
if SELF.exists():
    SELF.unlink()
