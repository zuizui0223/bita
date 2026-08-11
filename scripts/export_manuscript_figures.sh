#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INPUT_DIR="$ROOT/manuscript/figures"
OUTPUT_DIR="${1:-$ROOT/artifacts/manuscript_figures}"

mkdir -p "$OUTPUT_DIR"

if ! command -v inkscape >/dev/null 2>&1; then
  echo "inkscape is required to export manuscript figures to EPS" >&2
  exit 2
fi

figures=(
  "FIGURE_1_MECHANISTIC_ARCHITECTURE"
  "FIGURE_2_THEORY_REGIME_MAP"
  "FIGURE_3_EMPIRICAL_MECHANISM_ARCHITECTURE"
)

for stem in "${figures[@]}"; do
  src="$INPUT_DIR/${stem}.svg"
  dst="$OUTPUT_DIR/${stem}.eps"

  test -s "$src"

  # Springer prefers EPS for vector graphics. Converting text to paths avoids
  # submission-time font substitution while preserving vector geometry.
  inkscape "$src" \
    --export-filename="$dst" \
    --export-type=eps \
    --export-text-to-path

  test -s "$dst"
  grep -aq '^%!PS-Adobe' "$dst"
  grep -aq '%%BoundingBox:' "$dst"
done

cat > "$OUTPUT_DIR/README.txt" <<'EOF'
Manuscript figure export artifact

Source of truth: manuscript/figures/*.svg
Export format: EPS vector graphics
Exporter: Inkscape CLI
Text handling: converted to paths to avoid font substitution

Interpretation guardrails remain those stated in the manuscript figure captions:
- Figure 2 percentages are finite-grid occupancies, not prevalence.
- Figure 3 is an evidence architecture; marginal evidence is not W_AD.
EOF

printf 'Exported EPS figures to %s\n' "$OUTPUT_DIR"
