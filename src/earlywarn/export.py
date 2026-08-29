"""Write the catalog out as CSV and JSON."""

import csv
import json
from dataclasses import asdict
from pathlib import Path

from earlywarn import paths
from earlywarn.catalog import CATALOG
from earlywarn.models import COLUMN_NAMES, DataSource


def as_rows(sources: list[DataSource] | None = None) -> list[dict]:
    """Convert sources to plain dictionaries.

    Args:
        sources: Sources to convert, or None for the whole catalog.

    Returns:
        list[dict]: One dictionary per source, keyed by column name.
    """
    return [asdict(source) for source in (sources if sources is not None else CATALOG)]


def write_csv(path: Path, rows: list[dict]) -> Path:
    """Write rows to a CSV file, creating parent directories as needed.

    Args:
        path: Destination file.
        rows: Rows to write.

    Returns:
        Path: The path written.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=COLUMN_NAMES)
        writer.writeheader()
        writer.writerows(rows)
    return path


def write_json(path: Path, rows: list[dict]) -> Path:
    """Write rows to a JSON file, creating parent directories as needed.

    Args:
        path: Destination file.
        rows: Rows to write.

    Returns:
        Path: The path written.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as jsonfile:
        json.dump(rows, jsonfile, indent=2, ensure_ascii=False)
        jsonfile.write("\n")
    return path


def export_catalog(data_dir: Path | str | None = None) -> tuple[Path, Path]:
    """Write the whole catalog to CSV and JSON.

    Args:
        data_dir: Data directory, or None for the default.

    Returns:
        tuple[Path, Path]: Paths of the written CSV and JSON files.
    """
    root = paths.resolve(data_dir)
    rows = as_rows()
    return (
        write_csv(root / paths.CATALOG_CSV, rows),
        write_json(root / paths.CATALOG_JSON, rows),
    )
