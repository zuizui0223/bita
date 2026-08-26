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
  "$ROOT/manuscript/identification_figures/FIGURE_1_IDENTIFICATION_DESIGN.svg"
  "$ROOT/manuscript/identification_figures/FIGURE_2_IDENTIFICATION_DESIGN.svg"
  "$ROOT/manuscript/identification_figures/FIGURE_3_IDENTIFICATION_DESIGN.svg"
  "$ROOT/manuscript/identification_figures/FIGURE_4_IDENTIFICATION_DESIGN.svg"
  "$ROOT/manuscript/identification_figures/FIGURE_5_IDENTIFICATION_DESIGN.svg"
)
outputs=("Fig1" "Fig2" "Fig3" "Fig4" "Fig5")
expected_removed=(1 1 1 1 1)

for i in "${!sources[@]}"; do
  src="${sources[$i]}"
  prepared="$PREP_DIR/${outputs[$i]}.svg"
  dst="$OUTPUT_DIR/${outputs[$i]}.eps"

  test -s "$src"
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

Canonical identification-design Main hierarchy:
- Fig1: total trait interaction versus mechanism allocation
- Fig2: 16-cell crossed intervention design and separability diagnostic
- Fig3: independent joint-cost assay and hidden-channel diagnostic
- Fig4: existing-data stress tests and identification coverage
- Fig5: executable experimental roadmap

Canonical SVG sources are manuscript/identification_figures/FIGURE_1..5_IDENTIFICATION_DESIGN.svg.
Submission preprocessing removes the standalone outer title from each SVG while preserving
panel text, equations, annotations, and accessibility metadata.

Submission filenames: Fig1.eps, Fig2.eps, Fig3.eps, Fig4.eps, Fig5.eps
Export format: EPS vector graphics
Exporter: Inkscape CLI
Text handling: converted to paths to avoid font substitution

Interpretation guardrails:
- a total Delta_AD interaction does not identify mechanism allocation;
- the 16-cell design requires selective consumer interventions;
- a non-zero A×D×G×P contrast rejects the simple separable-channel representation;
- the residual joint channel is not automatically kappa;
- the 16-system coverage matrix is a screened-set audit, not literature prevalence.
EOF

printf 'Exported submission-ready identification-design EPS figures to %s\n' "$OUTPUT_DIR"
