from __future__ import annotations

import io
import zipfile

from scripts.analyze_sakhalkar2023_network import analyze_workbook


def _sheet_xml(headers, rows):
    all_rows = [headers] + rows
    width = len(headers)
    end_col = chr(ord("A") + width - 1)
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">',
        f'<dimension ref="A1:{end_col}{len(all_rows)}"/>',
        '<sheetData>',
    ]
    for r_idx, row in enumerate(all_rows, start=1):
        parts.append(f'<row r="{r_idx}">')
        for c_idx, value in enumerate(row, start=1):
            col = chr(ord("A") + c_idx - 1)
            ref = f"{col}{r_idx}"
            if isinstance(value, (int, float)):
                parts.append(f'<c r="{ref}"><v>{value}</v></c>')
            else:
                parts.append(
                    f'<c r="{ref}" t="inlineStr"><is><t>{value}</t></is></c>'
                )
        parts.append('</row>')
    parts.extend(['</sheetData>', '</worksheet>'])
    return "".join(parts)


def _fake_workbook() -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as book:
        book.writestr(
            "xl/workbook.xml",
            """<?xml version="1.0" encoding="UTF-8"?>
            <workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
              xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
              <sheets>
                <sheet name="cheater_data" sheetId="1" r:id="rId1"/>
                <sheet name="plant_traits" sheetId="2" r:id="rId2"/>
              </sheets>
            </workbook>""",
        )
        book.writestr(
            "xl/_rels/workbook.xml.rels",
            """<?xml version="1.0" encoding="UTF-8"?>
            <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
              <Relationship Id="rId1" Type="worksheet" Target="worksheets/sheet1.xml"/>
              <Relationship Id="rId2" Type="worksheet" Target="worksheets/sheet2.xml"/>
            </Relationships>""",
        )
        book.writestr(
            "xl/worksheets/sheet1.xml",
            _sheet_xml(
                ["spcode", "behavior", "freq_fm_per_species"],
                [
                    ["A", "robbing", 1.0],
                    ["A", "pollinating", 3.0],
                    ["B", "thieving", 2.0],
                    ["B", "pollinating", 2.0],
                    ["B", "visiting", 9.0],
                ],
            ),
        )
        book.writestr(
            "xl/worksheets/sheet2.xml",
            _sheet_xml(
                ["spcode", "shape", "tube_length", "tube_width"],
                [
                    ["A", "tube", 4.0, 1.0],
                    ["B", "open", 1.0, 2.0],
                ],
            ),
        )
    return buffer.getvalue()


def test_network_analysis_reproduces_behavior_and_trait_grain() -> None:
    result = analyze_workbook(_fake_workbook(), permutations=99)
    assert result["raw_cheater_rows"] == 5
    assert result["analysis_visit_rows"] == 4
    assert result["behavior_counts"] == {"pollinating": 2, "robbing": 1, "thieving": 1}
    assert result["visited_species"] == 2
    assert result["trait_matched_species"] == 2
    assert result["species_with_robbing"] == 1
    assert result["species_with_thieving"] == 1


def test_tube_length_predicts_cheating_mode_balance_in_synthetic_case() -> None:
    result = analyze_workbook(_fake_workbook(), permutations=99)
    balance = result["tube_length_cheating_mode_balance"]
    assert balance["n_species"] == 2
    assert balance["spearman_rho"] == 1.0
    assert result["median_tube_length_robber_only"] == 4.0
    assert result["median_tube_length_thief_only"] == 1.0


def test_analysis_output_contains_no_species_level_raw_rows() -> None:
    result = analyze_workbook(_fake_workbook(), permutations=99)
    assert "species_rows" not in result
    assert "A" not in str(result)
    assert "B" not in str(result)
