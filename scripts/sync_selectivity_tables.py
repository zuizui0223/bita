from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "manuscript" / "TABLES_THEORETICAL_ECOLOGY.md"

ROW = '| Selectivity window | \\(\\rho>\\iota\\) before direct joint cost | Declared oriented channel definitions | Necessary region for complementarity under non-negative joint cost; not sufficient |'
ROWS = '| Total mixed-partial evaluations | 2,592 |\n| Complementary evaluations outside the selectivity window | 0 |\n| In-window but substitutable evaluations | 397 |\n| Selectivity-window precision | 77.2% |\n| Zero-joint-cost window/sign agreement | 100% |'
OLD_KAPPA = '| Direct joint cost \\(\\kappa\\) | 0 strict estimates after targeted exhaustion | Marginal costs, covariance, and ecological interference exist, but no channel-specific simultaneous A+D intrinsic-cost curvature was found | \\(\\kappa\\) is unidentified, not zero |'
NEW_KAPPA = '| Direct joint cost \\(\\kappa\\) | 0 strict estimates after targeted exhaustion | Marginal costs, covariance, and ecological interference exist, but no channel-specific simultaneous A+D intrinsic-cost curvature was found | \\(\\kappa\\) is unidentified, not zero; a sufficiently negative value is the only failure route for the one-sided selectivity bound in the declared family |'
OLD_LEAL = '| **Reproduced meta-analysis 1 — Leal et al. 2025 floral larceny** | Secondary reanalysis of deposited study-level group data; one aggregate effect per independent cluster and outcome stratum; log response ratio | Female reproductive success: \\(-0.210\\), 48 clusters; nectar standing crop: \\(-0.483\\), 28; legitimate visitation: \\(-0.291\\), 22 | Direction stable to declared within-cluster correlation, quarantined-row sensitivity, and leave-one-cluster-out; very high heterogeneity | Establishes recurrent realised antagonist costs across fitness, reward, and visitation |'
NEW_LEAL = '| **Reproduced meta-analysis 1 — Leal et al. 2025 floral larceny** | Secondary reanalysis of deposited study-level group data; one aggregate effect per independent cluster and outcome stratum; log response ratio | Female reproductive success: \\(-0.210\\), 48 clusters; nectar standing crop: \\(-0.483\\), 28; legitimate visitation: \\(-0.291\\), 22 | Female: 35/48 negative but prediction interval \\(-1.13,+0.71\\); direction survives declared sensitivities and leave-one-out; moderators explain 0-8%; within-study reward-visitation association \\(r=-0.17\\) | Opens the antagonist-pressure gate on average while demonstrating strong system dependence; does not establish an end-to-end reward-mediated mechanism |'

def sync(text):
    if "| Selectivity window |" not in text:
        anchor = "| \\(\\kappa\\) | Direct joint-cost curvature | Direct cost-channel definition | Total energetic or construction cost |"
        if anchor not in text:
            raise RuntimeError("Table 1 kappa anchor not found")
        text = text.replace(anchor, anchor + "\n" + ROW, 1)
    if "| Selectivity-window precision |" not in text:
        anchor = "| Total mixed-partial evaluations | 2,592 |"
        if anchor not in text:
            raise RuntimeError("Table 2 evaluation anchor not found")
        text = text.replace(anchor, ROWS, 1)
    if OLD_KAPPA in text:
        text = text.replace(OLD_KAPPA, NEW_KAPPA, 1)
    if OLD_LEAL in text:
        text = text.replace(OLD_LEAL, NEW_LEAL, 1)
    return text

def main():
    text = TABLES.read_text(encoding="utf-8")
    TABLES.write_text(sync(text), encoding="utf-8")
    print("synchronized tables selectivity story")

if __name__ == "__main__":
    main()
