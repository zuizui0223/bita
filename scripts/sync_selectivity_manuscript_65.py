from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"
SECTION = "### 6.5 Environmental variables are joint ecological states that move the window\n\nThe theoretical comparative statics require derivatives of all channel contributions, not verbal assumptions that more antagonists must favour defence or that more pollinators must favour attraction. The larceny synthesis gives this caution direct empirical content. Antagonist exposure reduces female fitness on average, but 27% of female-fitness clusters are non-negative and the prediction interval spans both signs; none of the declared coarse moderators explains more than a small fraction of the heterogeneity. The exposure term that helps locate the selectivity window is therefore itself strongly context dependent.\n\nLarceny exposure also depresses legitimate visitation, so \\(P\\) and \\(H\\) cannot always be implemented as independent realised ecological quantities. In the separable corollary, allowing \\(P\\) to decline with \\(H\\) adds a positive correction to the derivative of \\(W_{AD}\\) with respect to antagonist pressure because the interference channel weakens while the relief channel is loaded. For this specific coupling, the separable form is conservative in direction, but the observation does not calibrate the total derivative or rescue any particular regime classification.\n\nFuture applications should therefore measure ecological exposure and channel responses together. The sign of \\(\\partial W_{AD}/\\partial H\\) or \\(\\partial W_{AD}/\\partial P\\) remains a balance among channel derivatives, and the window's location is a property of the joint ecological state rather than of a single named pressure variable."

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
    next_heading = next(h for h in ['### 6.6 A decisive empirical test', '### 6.6 Two empirical tests now have different jobs'] if h + "\n" in text)
    text = replace_any(text, ['### 6.5 Environmental variables should be treated as joint ecological states', '### 6.5 Environmental variables are joint ecological states that move the window'], next_heading, SECTION)
    MANUSCRIPT.write_text(text, encoding="utf-8")

if __name__ == "__main__":
    main()
