from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "manuscript" / "figures"
SUPP_FIG = ROOT / "manuscript" / "supplementary" / "figures"

# Frozen manuscript-facing values. This script is presentation-only: no analysis.
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
        boxstyle="round,pad=0.012,rounding_size=0.015",
        fill=False,
        linewidth=lw,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize, wrap=True)


def _arrow(ax, x1, y1, x2, y2, lw=1.4):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="->", mutation_scale=14, linewidth=lw))


def _svg_defaults() -> None:
    plt.rcParams["svg.fonttype"] = "none"
    plt.rcParams["svg.hashsalt"] = "bita-main-results-figures-4-5-v1"


def build_quantitative_figure(path: Path) -> None:
    """Quantitative evidence and direct-identification boundary, frozen results only."""
    _svg_defaults()
    fig = plt.figure(figsize=(9, 10))
    ax = fig.add_axes([0.03, 0.04, 0.94, 0.93])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(
        0.5, 0.98,
        "Quantitative evidence narrows the problem\nwithout identifying the total interaction",
        ha="center", va="top", fontsize=16, fontweight="bold",
    )
    ax.text(
        0.5, 0.89,
        "Floral larceny: pooled log response ratios",
        ha="center", fontsize=12.5, fontweight="bold",
    )

    x0, x1 = 0.32, 0.67
    emin, emax = -1.2, 0.8

    def ex(value: float) -> float:
        return x0 + (value - emin) / (emax - emin) * (x1 - x0)

    zero = ex(0)
    ax.plot([zero, zero], [0.61, 0.82], linewidth=1)
    items = [
        ("Female fitness", *LEAL["female"], 0.78),
        ("Nectar standing crop", *LEAL["nectar"], 0.71),
        ("Legitimate visitation", *LEAL["visitation"], 0.64),
    ]
    for label, value, n, y in items:
        ax.text(0.12, y, label, va="center", fontsize=10.3)
        ax.plot([zero, ex(value)], [y, y], linewidth=2)
        ax.plot(ex(value), y, "o", markersize=8)
        ax.text(ex(value) - 0.005, y + 0.022, f"{value:+.3f} (n={n})", ha="right", fontsize=9.5)

    y = 0.575
    ax.text(0.12, y, "Female 95% prediction interval", va="center", fontsize=10.2)
    ax.plot([ex(FEMALE_PI[0]), ex(FEMALE_PI[1])], [y, y], linewidth=2)
    ax.plot([ex(FEMALE_PI[0]), ex(FEMALE_PI[1])], [y, y], "|", markersize=14)
    ax.text(
        (ex(FEMALE_PI[0]) + ex(FEMALE_PI[1])) / 2,
        y - 0.035,
        "−1.13 to +0.71",
        ha="center",
        fontsize=9.5,
    )
    ax.text(
        0.5, 0.515,
        f"{FEMALE_NEGATIVE} female-fitness effects negative; declared moderators explain only {MODERATOR_R2} of heterogeneity.",
        ha="center", fontsize=10.0,
    )

    _box(
        ax, 0.12, 0.39, 0.76, 0.105,
        "Floral volatile responses\n\n"
        f"Assembled florivore − pollinator risk difference = +{SASIDHARAN_RD:.3f}\n"
        f"{SASIDHARAN_LOCO} leave-one-component-out refits remain positive\n"
        "Only 3 study components contain both roles; all 3 paired differences = 0.",
        10.1,
    )

    _box(
        ax, 0.07, 0.20, 0.38, 0.13,
        "What the synthesis establishes\n\n"
        "• antagonist exposure matters on average\n"
        "• constituent routes recur\n"
        "• realized effects switch with context\n\n"
        "It does NOT estimate $\\rho$, $\\iota$, $\\kappa$, or $W_{AD}$.",
        9.9,
    )
    _box(
        ax, 0.55, 0.20, 0.38, 0.13,
        "Identification gap\n\n"
        "Direct total $A\\times D$:\n"
        f"{DIRECT_AXD_STRICT} strict sign-unresolved cluster\n\n"
        "Direct joint-cost $\\kappa$:\n"
        f"{KAPPA_STRICT} strict estimates (unknown ≠ zero)",
        10.0,
    )

    _box(
        ax, 0.21, 0.055, 0.58, 0.095,
        "Ordered next tests\n\n"
        "1. 2×2 cost assay → identify the sign of $\\kappa$\n"
        "2. Full $A\\times D$ factorial → estimate total $W_{AD}$ and allocate channels",
        10.2,
    )
    _arrow(ax, 0.74, 0.20, 0.74, 0.15)

    ax.text(
        0.5, 0.012,
        "Recurrent mechanisms + context-dependent balance; uncertainty compressed to testable coordinates.",
        ha="center", fontsize=11.2, fontweight="bold",
    )

    fig.savefig(path, bbox_inches="tight", metadata={"Date": None})
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    # Kept at the existing source path to avoid duplicating a frozen SVG solely for renumbering.
    # In the Ecology Main Document this source is Figure 4.
    build_quantitative_figure(OUT / "FIGURE_5_QUANTITATIVE_IDENTIFICATION_BOUNDARY.svg")

    # Main Figure 5 reuses the already frozen same-system matrix source directly.
    # The submission builder points to this file; it is no longer packaged as a Supplement figure.
    same_system = SUPP_FIG / "FIGURE_S3_SAME_SYSTEM_ROUTE_MATRIX.svg"
    if not same_system.exists():
        raise FileNotFoundError(f"missing canonical same-system matrix: {same_system}")


if __name__ == "__main__":
    main()
