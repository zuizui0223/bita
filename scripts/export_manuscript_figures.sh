#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="${1:-$ROOT/artifacts/manuscript_figures}"
PREP_DIR="$(mktemp -d)"
trap 'rm -rf "$PREP_DIR"' EXIT

mkdir -p "$OUTPUT_DIR"

if ! command -v inkscape >/dev/null 2>&1; then
  echo "inkscape is required to export manuscript figures to EPS" >&2
  exit 2
fi

sources=(
  "$ROOT/manuscript/figures/FIGURE_1_MECHANISTIC_ARCHITECTURE.svg"
  "$ROOT/manuscript/figures/FIGURE_2_THEORY_REGIME_MAP.svg"
  "$ROOT/manuscript/figures/FIGURE_3_EMPIRICAL_MECHANISM_ARCHITECTURE.svg"
  "$ROOT/manuscript/figures/FIGURE_5_QUANTITATIVE_IDENTIFICATION_BOUNDARY.svg"
  "$ROOT/manuscript/supplementary/figures/FIGURE_S3_SAME_SYSTEM_ROUTE_MATRIX.svg"
)
outputs=("Fig1" "Fig2" "Fig3" "Fig4" "Fig5")
expected_removed=(1 1 1 2 0)

for i in "${!sources[@]}"; do
  src="${sources[$i]}"
  prepared="$PREP_DIR/${outputs[$i]}.svg"
  dst="$OUTPUT_DIR/${outputs[$i]}.eps"

  test -s "$src"

  # Canonical sources differ in whether they carry a standalone-review title:
  # Figs 1–3 have one title element, Fig4 has a two-line Matplotlib title,
  # and Fig5 begins directly with route-column headers. Remove exactly those
  # declared outer-title elements and nothing else.
  python "$ROOT/scripts/prepare_submission_svg.py" \
    "$src" "$prepared" \
    --expected-removed "${expected_removed[$i]}"
  test -s "$prepared"

  inkscape "$prepared" \
    --export-filename="$dst" \
    --export-type=eps \
    --export-text-to-path

  test -s "$dst"
  grep -aq '^%!PS-Adobe' "$dst"
  grep -aq '%%BoundingBox:' "$dst"
done

cat > "$OUTPUT_DIR/README.txt" <<'EOF'
Ecology Concepts & Synthesis manuscript figure export artifact

Canonical result-first Main hierarchy:
- Fig1: mechanistic architecture and inference boundary
- Fig2: finite theory regime / selectivity-window result
- Fig3: cross-system Pattern architecture
- Fig4: quantitative evidence and identification boundary
- Fig5: same-system route architecture

Source files remain at their reproducibility locations; Fig4 reuses the frozen quantitative SVG
originally introduced under the Figure-5 filename, and Fig5 reuses the frozen same-system matrix
source originally stored under supplementary/figures. They are not duplicated solely for numbering.

Submission preprocessing: declared visible outer figure title elements removed; panel labels,
equations, annotations, route headers, and accessibility metadata retained
Submission filenames: Fig1.eps, Fig2.eps, Fig3.eps, Fig4.eps, Fig5.eps
Export format: EPS vector graphics
Exporter: Inkscape CLI
Text handling: converted to paths to avoid font substitution

Interpretation guardrails remain those stated in the manuscript figure captions:
- Fig. 2 percentages are finite-grid occupancies, not prevalence.
- Fig. 3 is an evidence architecture; marginal evidence is not W_AD.
- Fig. 4 quantitative modules retain incompatible metrics and do not estimate W_AD.
- Fig. 5 linked marginal routes are not direct A x D evidence.
EOF

printf 'Exported submission-ready EPS figures to %s\n' "$OUTPUT_DIR"
