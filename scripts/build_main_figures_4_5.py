from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "manuscript" / "figures"

# Frozen manuscript-facing values. This script is presentation-only: no analysis.
N_EVAL = 2592
WINDOW_PRECISION = 77.2
IN_WINDOW_SUBSTITUTABLE = 397
ROUTE_RECORDS = 56
BIOLOGICAL_CLUSTERS = 25
SAME_SYSTEM = 14
SIGN_SWITCH = 17
CONTEXT_ONLY = 7
LEAL = {
    "female": (-0.210, 48),
    "nectar": (-0.483, 28),
    "visitation": (-0.291, 22),
}
FEMALE_NEGATIVE = "35/48"
FEMALE_PI = (-1.13, 0.71)
MODERATOR_R2 = "0–8%"
SASIDHARAN_RD = 0.129
SASIDHARAN_LOCO = "32/32"
DIRECT_AXD_STRICT = 1
KAPPA_STRICT = 0


def _box(ax, x, y, w, h, text, fontsize=11, lw=1.4):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.015,rounding_size=0.018",
        fill=False,
        linewidth=lw,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize, wrap=True)


def _arrow(ax, x1, y1, x2, y2, lw=1.4):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="->", mutation_scale=14, linewidth=lw))


def build_figure_4(path: Path) -> None:
    plt.rcParams["svg.fonttype"] = "none"
    fig = plt.figure(figsize=(14, 8))
    ax = fig.add_axes([0.025, 0.055, 0.95, 0.90])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(
        0.5, 0.97,
        "Mechanism before Pattern: from a complex ecological balance to a falsifiable boundary",
        ha="center", va="top", fontsize=18, fontweight="bold",
    )
    ax.text(
        0.5, 0.925,
        "Theory defines the exclusion and the evidence classes before the cross-system synthesis is assembled.",
        ha="center", fontsize=11,
    )

    _box(ax, 0.025, 0.68, 0.17, 0.16,
         "Ecological problem\n\nAttraction can recruit\nmutualists + antagonists;\ndefence can relieve damage\nbut interfere with pollination.", 10.4)
    _arrow(ax, 0.195, 0.76, 0.245, 0.76)
    _box(ax, 0.245, 0.65, 0.225, 0.22,
         "Declare focal channels\n\n$W_{AD}=\\rho-\\iota-\\kappa$\n\n$\\rho$: antagonist relief\n$\\iota$: pollinator interference\n$\\kappa$: direct joint-cost curvature", 10.8)
    _arrow(ax, 0.47, 0.76, 0.52, 0.76)
    _box(ax, 0.52, 0.64, 0.205, 0.24,
         "One-line exclusion\n\n$\\kappa\\geq0,\\ W_{AD}>0$\n$\\Rightarrow\\ \\rho>\\iota$\n\nNecessary window,\nnot a sufficient sign rule.", 11.2)
    _arrow(ax, 0.725, 0.76, 0.775, 0.76)
    _box(ax, 0.775, 0.66, 0.20, 0.20,
         f"Finite verification\n\n{N_EVAL:,} evaluations\n0 outside-window counterexamples\n\n~23% of in-window points\nremain substitutable", 10.2)

    _box(ax, 0.05, 0.31, 0.21, 0.19,
         "Theory defines evidence classes\n\nA→pollination\nA→antagonism\nD→antagonism\nD→pollination\nsame-system / switching", 10.4)
    _arrow(ax, 0.26, 0.405, 0.325, 0.405)
    _box(ax, 0.325, 0.30, 0.225, 0.21,
         f"Cross-system Pattern\n\n{ROUTE_RECORDS} route records\n{BIOLOGICAL_CLUSTERS} independent clusters\n{SAME_SYSTEM} same-system\n{SIGN_SWITCH} context/sign switches\n{CONTEXT_ONLY} context-only programs", 10.3)
    _arrow(ax, 0.55, 0.405, 0.615, 0.405)
    _box(ax, 0.615, 0.30, 0.17, 0.21,
         "What recurs?\n\nConstituent mechanisms\n+ switching architectures\n\nNot one universal\nsign of $W_{AD}$", 10.2)
    _arrow(ax, 0.785, 0.405, 0.835, 0.405)
    _box(ax, 0.835, 0.30, 0.14, 0.21,
         f"What remains\nunidentified?\n\nDirect total $A\\times D$:\nsparse\n\nStrict $\\kappa$ estimates: {KAPPA_STRICT}", 10.0)

    ax.text(0.18, 0.14, "Mechanism → Pattern\nnot theory → validation", ha="center", va="center", fontsize=14, fontweight="bold")
    _arrow(ax, 0.30, 0.14, 0.50, 0.14)
    _box(ax, 0.52, 0.07, 0.44, 0.14,
         "Experimental triage\n\n2×2 attraction × defence cost assay → test joint-cost sign\nFull A×D factorial → estimate total interaction + channel allocation", 10.5)

    fig.savefig(path, bbox_inches="tight", metadata={"Date": None})
    plt.close(fig)


def build_figure_5(path: Path) -> None:
    plt.rcParams["svg.fonttype"] = "none"
    fig = plt.figure(figsize=(14, 8))
    ax = fig.add_axes([0.03, 0.07, 0.94, 0.86])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(
        0.5, 0.975,
        "Quantitative evidence narrows the problem but does not identify the total interaction",
        ha="center", va="top", fontsize=18, fontweight="bold",
    )
    ax.text(0.24, 0.89, "Floral larceny: pooled directions", ha="center", fontsize=13, fontweight="bold")

    x0, x1 = 0.12, 0.45
    emin, emax = -1.2, 0.8
    ex = lambda v: x0 + (v - emin) / (emax - emin) * (x1 - x0)
    zero = ex(0)
    ax.plot([zero, zero], [0.57, 0.84], linewidth=1)
    items = [
        ("Female fitness", *LEAL["female"], 0.80),
        ("Nectar standing crop", *LEAL["nectar"], 0.73),
        ("Legitimate visitation", *LEAL["visitation"], 0.66),
    ]
    for label, value, n, y in items:
        ax.text(0.035, y, label, va="center", fontsize=10.5)
        ax.plot([zero, ex(value)], [y, y], linewidth=2)
        ax.plot(ex(value), y, "o", markersize=8)
        ax.text(ex(value) - 0.006, y + 0.025, f"{value:+.3f}  (n={n})", ha="right", fontsize=9.8)

    y = 0.585
    ax.text(0.035, y, "Female 95% prediction interval", va="center", fontsize=10.5)
    ax.plot([ex(FEMALE_PI[0]), ex(FEMALE_PI[1])], [y, y], linewidth=2)
    ax.plot([ex(FEMALE_PI[0]), ex(FEMALE_PI[1])], [y, y], "|", markersize=14)
    ax.text((ex(FEMALE_PI[0]) + ex(FEMALE_PI[1])) / 2, y - 0.04,
            f"{FEMALE_PI[0]:+.2f} to {FEMALE_PI[1]:+.2f}", ha="center", fontsize=9.8)
    ax.text(0.035, 0.515,
            f"{FEMALE_NEGATIVE} female-fitness effects negative; declared moderators explain only {MODERATOR_R2} of heterogeneity.",
            fontsize=10.4)

    _box(ax, 0.54, 0.58, 0.40, 0.27,
         f"Floral volatile responses\n\nAssembled florivore − pollinator risk difference = +{SASIDHARAN_RD:.3f}\n\n{SASIDHARAN_LOCO} leave-one-component-out refits remain positive\n\nBut only 3 study components contain both roles;\nall 3 paired differences = 0", 10.7)

    _box(ax, 0.04, 0.16, 0.28, 0.25,
         "What the synthesis establishes\n\n• antagonist exposure matters on average\n• constituent routes recur\n• realized effects switch with context\n\nIt does NOT estimate\n$\\rho$, $\\iota$, $\\kappa$, or total $W_{AD}$", 10.2)
    _box(ax, 0.375, 0.16, 0.25, 0.25,
         f"Identification gap\n\nDirect total $A\\times D$:\n{DIRECT_AXD_STRICT} strict sign-unresolved cluster\n\nDirect joint-cost $\\kappa$:\n{KAPPA_STRICT} strict estimates\n\nUnknown ≠ zero", 10.6)
    _box(ax, 0.70, 0.16, 0.25, 0.25,
         "Next tests\n\n1. 2×2 cost assay → sign of $\\kappa$\n\n2. Full $A\\times D$ factorial\n→ total $W_{AD}$ + channel allocation", 10.6)
    _arrow(ax, 0.625, 0.285, 0.69, 0.285)

    ax.text(
        0.5, 0.065,
        "Empirical synthesis supports recurrent mechanisms + context-dependent balance,\nwhile compressing the remaining uncertainty to directly testable coordinates.",
        ha="center", fontsize=12, fontweight="bold",
    )

    fig.savefig(path, bbox_inches="tight", metadata={"Date": None})
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    build_figure_4(OUT / "FIGURE_4_MECHANISM_PATTERN_OVERVIEW.svg")
    build_figure_5(OUT / "FIGURE_5_QUANTITATIVE_IDENTIFICATION_BOUNDARY.svg")


if __name__ == "__main__":
    main()
