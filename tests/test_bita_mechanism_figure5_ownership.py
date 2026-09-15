from scripts import build_mechanism_identification_figures_svg as figures


def test_figure5_keeps_bita_orthogonal_and_ladder_in_bounds() -> None:
    svg = figures.fig5()

    assert "orthogonal mechanism-identification track" in svg
    assert "exports identified L" in svg
    assert "BITA: observed interaction → mechanism allocation" in svg

    # The old publication-facing figure incorrectly drew SLK -> BITA as a
    # downstream transport arrow. The revised figure uses a dashed separator.
    assert '<line x1="910" y1="82" x2="910" y2="445" class="dash"/>' in svg
    assert '<line x1="920" y1="260" x2="995" y2="260" class="line"/>' not in svg

    # Final BITA ladder box ends at x=1210 inside the 1300-wide SVG canvas.
    assert '<rect x="1090" y="555" width="120" height="78"' in svg
