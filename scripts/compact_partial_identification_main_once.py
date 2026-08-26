# One-shot trigger: compact Main after partial-identification integration.
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "manuscript" / "MANUSCRIPT_IDENTIFICATION_DESIGN.md"


def replace_section(text: str, start: str, end: str, replacement: str) -> str:
    if text.count(start) != 1 or text.count(end) != 1:
        raise RuntimeError(f"non-unique section marker: {start!r} / {end!r}")
    a = text.index(start)
    b = text.index(end, a)
    return text[:a] + replacement.rstrip() + "\n\n" + text[b:]


text = MAN.read_text(encoding="utf-8")

sec46 = r'''### 4.6 Other informative near misses

Two additional systems isolate different design requirements. Kessler et al. (2015) crossed floral scent and nectar production, but nectar is a reward axis rather than an independently justified antagonist-reducing defence trait; this biological orientation problem is more fundamental than the absence of a recovered machine-readable outcome table. In *Pedicularis rex*, Sun and Huang (2015) manipulated a water-holding bract barrier that strongly affected seed predation without a detected effect on legitimate pollinator or nectar-robber visitation. This provides a practical model for selective access, but no independent attraction manipulation was present.

Across the 16 screened systems, failure modes therefore differ—missing trait interactions, missing consumer factorials, invalid floral coordinates, or missing attraction manipulation—but no system includes an independent attraction-by-defence joint-cost assay.'''
text = replace_section(text, "### 4.6 Other informative near misses", "## 5. Designing an identifiable experiment", sec46)

sec51 = r'''### 5.1 Choose the biological system before choosing the exclusion device

The main design difficulty is intervention selectivity, not the number of cells. Generic bags or broad pesticides can alter pollinators, antagonists and plant physiology simultaneously, destroying the channel interpretation. Candidate systems should instead exploit natural asymmetries such as body size, access route, diel activity or phenology. *Pedicularis rex* illustrates the useful logic: a consumer-specific access mechanism can first supply a selective defence manipulation, then an independent attraction manipulation and selective consumer toggles can be crossed onto that backbone.'''
text = replace_section(text, "### 5.1 Choose the biological system before choosing the exclusion device", "### 5.2 Analysis sequence", sec51)

sec52 = r'''### 5.2 Analysis sequence

Analysis follows the causal contrasts. Estimate \(\Delta_{AD}W\) within consumer states, form antagonist-exclusion and pollinator-increment contrasts with propagated uncertainty, estimate or justify \(m_{0,\Delta}\), and then test the single \(A\times D\times E_G\times E_P\) four-way separability contrast. Only after these gates should the remaining joint channel be compared with the independent cost assay. The sampling model can be generalized, permutation-based or randomization-based; the required invariant is the contrast structure and its biological interpretation.'''
text = replace_section(text, "### 5.2 Analysis sequence", "### 5.3 What counts as a successful outcome", sec52)

sec53 = r'''### 5.3 What counts as a successful outcome

The experiment is informative regardless of the sign of \(\Delta_{AD}W\). Near-zero four-way coupling plus residual–assay agreement supports the proposed decomposition. Non-zero four-way coupling rejects separability. Residual–assay disagreement exposes a missing channel, intervention failure or scale mismatch. Finally, complementarity with \(\rho_\Delta\le\iota_\Delta\) forces a negative remaining joint channel on the chosen scale. Each outcome therefore resolves a different part of the identification problem rather than being labelled a failed experiment.'''
text = replace_section(text, "### 5.3 What counts as a successful outcome", "### 5.4 Computational and AI-assisted workflow transparency", sec53)

MAN.write_text(text, encoding="utf-8")
