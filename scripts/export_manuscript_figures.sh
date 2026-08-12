#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INPUT_DIR="$ROOT/manuscript/figures"
OUTPUT_DIR="${1:-$ROOT/artifacts/manuscript_figures}"
PREP_DIR="$(mktemp -d)"
trap 'rm -rf "$PREP_DIR"' EXIT

mkdir -p "$OUTPUT_DIR"

if ! command -v inkscape >/dev/null 2>&1; then
  echo "inkscape is required to export manuscript figures to EPS" >&2
  exit 2
fi

sources=(
  "FIGURE_1_MECHANISTIC_ARCHITECTURE"
  "FIGURE_2_THEORY_REGIME_MAP"
  "FIGURE_3_EMPIRICAL_MECHANISM_ARCHITECTURE"
)
outputs=("Fig1" "Fig2" "Fig3")

for i in "${!sources[@]}"; do
  src="$INPUT_DIR/${sources[$i]}.svg"
  prepared="$PREP_DIR/${outputs[$i]}.svg"
  dst="$OUTPUT_DIR/${outputs[$i]}.eps"

  test -s "$src"

  # The journal asks that an illustration not carry its own title/caption.
  # Canonical SVGs retain standalone-review titles; the deterministic export
  # preprocessor removes only the visible top-level title before EPS export.
  python "$ROOT/scripts/prepare_submission_svg.py" "$src" "$prepared"
  test -s "$prepared"

  # Theoretical Ecology prefers EPS for vector graphics and requests figure
  # filenames of the form Fig1.eps, Fig2.eps, ... . Converting text to paths
  # avoids submission-time font substitution while preserving vector geometry.
  inkscape "$prepared" \
    --export-filename="$dst" \
    --export-type=eps \
    --export-text-to-path

  test -s "$dst"
  grep -aq '^%!PS-Adobe' "$dst"
  grep -aq '%%BoundingBox:' "$dst"
done

cat > "$OUTPUT_DIR/README.txt" <<'EOF'
Theoretical Ecology manuscript figure export artifact

Canonical source of truth: manuscript/figures/*.svg
Submission preprocessing: visible outer figure title removed; panel labels, equations,
annotations, and accessibility metadata retained
Submission filenames: Fig1.eps, Fig2.eps, Fig3.eps
Export format: EPS vector graphics
Exporter: Inkscape CLI
Text handling: converted to paths to avoid font substitution

Interpretation guardrails remain those stated in the manuscript figure captions:
- Fig. 2 percentages are finite-grid occupancies, not prevalence.
- Fig. 3 is an evidence architecture; marginal evidence is not W_AD.
EOF

printf 'Exported submission-ready EPS figures to %s\n' "$OUTPUT_DIR"
