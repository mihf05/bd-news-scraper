"""CSV and JSON exports must agree with the catalog and with each other."""

import csv
import json
from pathlib import Path

from earlywarn import paths
from earlywarn.catalog import CATALOG
from earlywarn.export import export_catalog
from earlywarn.models import COLUMN_NAMES


def test_export_writes_both_files(tmp_path: Path):
    csv_path, json_path = export_catalog(tmp_path)
    assert csv_path.exists() and json_path.exists()


def test_csv_columns_match_the_model(tmp_path: Path):
    csv_path, _ = export_catalog(tmp_path)
    with open(csv_path, newline="", encoding="utf-8") as handle:
        assert next(csv.reader(handle)) == COLUMN_NAMES


def test_both_formats_carry_every_source(tmp_path: Path):
    csv_path, json_path = export_catalog(tmp_path)
    with open(csv_path, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    records = json.loads(json_path.read_text(encoding="utf-8"))

    assert len(rows) == len(records) == len(CATALOG)
    assert [row["dataset_id"] for row in rows] == [s.dataset_id for s in CATALOG]
    assert [record["dataset_id"] for record in records] == [s.dataset_id for s in CATALOG]


def test_committed_exports_are_up_to_date(tmp_path: Path, repo_data: Path):
    """Guards against editing the catalog and forgetting to re-export."""
    fresh_csv, fresh_json = export_catalog(tmp_path)
    for fresh, relative in ((fresh_csv, paths.CATALOG_CSV), (fresh_json, paths.CATALOG_JSON)):
        committed = repo_data / relative
        assert committed.exists(), f"{relative} is missing - run 'earlywarn export'"
        assert fresh.read_bytes() == committed.read_bytes(), (
            f"{relative} is stale - run 'earlywarn export'"
        )
