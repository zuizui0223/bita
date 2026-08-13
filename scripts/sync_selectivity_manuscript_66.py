from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"
SECTION = "### 6.6 Two empirical tests now have different jobs\n\nThe one-sided theorem changes the order of the empirical programme. The cheapest first test is not a full field estimate of \\(W_{AD}\\), but a test of the theorem's biological applicability. A 2 × 2 allocation design — neither focal trait, attraction only, defence only, and both — can ask whether simultaneous expression costs more or less than additivity predicts. Scoring construction, resource, or other appropriately defined direct costs identifies the **sign of joint-cost curvature**. No pollinators, antagonists, or total-fitness assay are required for this first gate. A sufficiently negative cross-cost would falsify the one-sided selectivity bound for that focal trait pair.\n\nA second, harder experiment has a different purpose: estimating the total interaction and its mechanism. That design must manipulate one attraction trait and one distinct flower-specific antagonist-reducing defence/access trait factorially in the same biological units, with compatible mutualist contribution, antagonist loss, direct cost, and total-fitness outcomes. It would estimate the total \\(A\\times D\\) interaction and test whether the observed curvature is allocated to antagonist relief, pollinator interference, or joint cost.\n\nThe literature-access problem therefore no longer defines the main theoretical bottleneck. The strongest boundary is controlled by a quantity for which strict direct measurements are largely absent, but whose sign is experimentally much cheaper to obtain than the full mixed partial. The full factorial remains essential for calibration; the 2 × 2 cost design is the faster falsification gate."

def replace_any(text, heads, next_heading, replacement):
    for head in heads:
        token = head + "\n"
        if token in text:
            start = text.index(token)
            end = text.index(next_heading + "\n", start)
            return text[:start] + replacement.rstrip() + "\n\n" + text[end:]
    raise RuntimeError("section anchor missing")

def main():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    text = replace_any(text, ['### 6.6 A decisive empirical test', '### 6.6 Two empirical tests now have different jobs'], "## 7. Conclusions", SECTION)
    MANUSCRIPT.write_text(text, encoding="utf-8")

if __name__ == "__main__":
    main()
