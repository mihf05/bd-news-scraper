"""The generated page must be self-contained and carry the whole catalog."""

import json
import re
from pathlib import Path

import pytest

from earlywarn import paths
from earlywarn.catalog import CATALOG
from earlywarn.page import DATA_MARKER, build_page, count_rows, render


def embedded_payload(html: str) -> dict:
    """Pull the JSON payload back out of a rendered page."""
    raw = re.search(r"var DATA = (\{.*?\});\n", html, re.S).group(1)
    return json.loads(raw.replace("<\\/", "</"))


def test_page_is_a_complete_document(built: Path):
    html = (built / paths.PAGE_HTML).read_text(encoding="utf-8")
    assert html.startswith("<!doctype html>")
    assert html.rstrip().endswith("</html>")
    assert "<title>" in html
    assert DATA_MARKER not in html


def test_page_carries_every_source(built: Path):
    payload = embedded_payload((built / paths.PAGE_HTML).read_text(encoding="utf-8"))
    assert [row["dataset_id"] for row in payload["catalog"]] == [s.dataset_id for s in CATALOG]
    assert payload["columns"]
    assert {idea["id"] for idea in payload["ideas"]} == {s.idea for s in CATALOG}


def test_page_embeds_the_downloadable_files_verbatim(built: Path):
    payload = embedded_payload((built / paths.PAGE_HTML).read_text(encoding="utf-8"))
    names = {entry["name"]: entry for entry in payload["files"]}
    assert "datasets.csv" in names and "datasets.json" in names

    on_disk = (built / paths.CATALOG_CSV).read_bytes().decode("utf-8")
    assert names["datasets.csv"]["content"] == on_disk, "download would differ from the file"
    assert names["datasets.csv"]["rows"] == len(CATALOG)


def test_fragment_has_no_document_skeleton(tmp_path: Path):
    from earlywarn.export import export_catalog

    export_catalog(tmp_path)
    fragment = tmp_path / "fragment.html"
    build_page(tmp_path, fragment_path=fragment)

    text = fragment.read_text(encoding="utf-8")
    assert text.startswith("<title>")
    for tag in ("<!doctype", "<html", "<head>", "<body>"):
        assert tag not in text


def test_render_rejects_a_template_without_markers(monkeypatch, tmp_path: Path):
    monkeypatch.setattr("earlywarn.page.read_template", lambda: "<p>no markers</p>")
    with pytest.raises(ValueError):
        render(tmp_path)


def test_count_rows_ignores_the_csv_header():
    assert count_rows("a,b\r\n1,2\r\n3,4\r\n", is_json=False) == 2
    assert count_rows("[]", is_json=True) == 0
