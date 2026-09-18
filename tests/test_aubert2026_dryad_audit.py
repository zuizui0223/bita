from __future__ import annotations

import io
import json
import zipfile

from scripts.audit_aubert2026_dryad import summarize_archive


def _fake_archive() -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr(
            "Interactions_data_Ecuador.txt",
            "waypoint\tsite\tinteraction\tnectar_robbing\tbird_species\n"
            "w1\ts1\tyes\tno\tBird a\n"
            "w1\ts1\tyes\tyes\tBird b\n"
            "w2\ts2\tyes\tmaybe\tBird c\n",
        )
        archive.writestr(
            "Cameras_data_Ecuador.txt",
            "waypoint\tsite\tplant_species\n"
            "w1\ts1\tPlant a\n"
            "w2\ts2\tPlant b\n",
        )
        archive.writestr(
            "Plant_traits.txt",
            "plant_species\ttube_length\n"
            "Plant a\t2.0\n"
            "Plant b\t3.0\n",
        )
        archive.writestr("script.R", "x <- 1\nprint(x)\n")
    return buffer.getvalue()


def test_archive_audit_reports_required_files_and_safe_aggregates() -> None:
    report = summarize_archive(_fake_archive())

    assert report["required_files_present"] is True
    assert report["interaction_rows"] == 3
    assert report["camera_rows"] == 2
    assert report["plant_trait_rows"] == 2
    assert report["interaction_sites"] == 2
    assert report["nectar_robbing_counts"] == {"maybe": 1, "no": 1, "yes": 1}
    assert report["script_present"] is True
    assert report["script_line_count"] == 2


def test_archive_audit_does_not_emit_raw_interaction_rows() -> None:
    report = summarize_archive(_fake_archive())
    encoded = json.dumps(report)
    assert "Bird a" not in encoded
    assert "Plant a" not in encoded
    assert "raw_rows" not in report
