"""Download the sources that can be fetched unattended.

Only sources marked ``fetchable`` are downloaded. Everything else needs a human
step first - an approved API key, a free account, a login, a resolved article
id, or a parser for an HTML or PDF page - and is reported as skipped with that
step named.

Two sources read credentials from the environment:

``OPENAQ_API_KEY``
    Free key from the OpenAQ Explorer, sent as the ``X-API-Key`` header.
``WAQI_TOKEN``
    Free token from aqicn.org/data-platform/token, sent as a query parameter.
"""

import csv
import json
import os
from dataclasses import dataclass
from pathlib import Path

from earlywarn import paths
from earlywarn.catalog import by_idea
from earlywarn.models import DataSource

REQUEST_TIMEOUT = 60
USER_AGENT = "earlywarn-data-catalog/1.0"


@dataclass
class FetchOutcome:
    """What happened to one source during a fetch run.

    Attributes:
        source: The source in question.
        status: One of "fetched", "failed", "skipped" or "planned".
        detail: Saved path, error message, or the manual step needed.
    """

    source: DataSource
    status: str
    detail: str


def build_headers(source: DataSource) -> dict[str, str]:
    """Build request headers, injecting any API key from the environment.

    Args:
        source: Source about to be requested.

    Returns:
        dict[str, str]: Headers for the request.
    """
    headers = {"User-Agent": USER_AGENT}
    if source.dataset_id == "openaq":
        key = os.environ.get("OPENAQ_API_KEY")
        if key:
            headers["X-API-Key"] = key
    return headers


def build_url(source: DataSource) -> str:
    """Return the download URL with any required token appended.

    Args:
        source: Source about to be requested.

    Returns:
        str: URL to request.
    """
    if source.dataset_id == "waqi":
        return f"{source.download_url}?token={os.environ.get('WAQI_TOKEN', '')}"
    return source.download_url


def flatten_to_csv(path: Path, records: list[dict]) -> None:
    """Write a list of JSON records as a CSV table.

    Nested values are re-encoded as JSON so a cell never breaks the row.

    Args:
        path: Destination CSV file.
        records: Records to write; the first one defines the columns.
    """
    keys = list(records[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        for record in records:
            writer.writerow({
                key: json.dumps(value) if isinstance(value, (dict, list)) else value
                for key, value in record.items()
            })


def fetch_source(source: DataSource, raw_dir: Path) -> Path:
    """Download one source and save it.

    JSON responses are saved as ``.json`` and also flattened to ``.csv`` when
    the payload is a list of records. Anything else is saved verbatim.

    Args:
        source: Source to download.
        raw_dir: Directory raw downloads are written to.

    Returns:
        Path: Path of the primary saved file.

    Raises:
        requests.HTTPError: If the server returns an error status.
        requests.RequestException: If the request cannot be completed.
    """
    import requests

    raw_dir.mkdir(parents=True, exist_ok=True)
    response = requests.get(
        build_url(source),
        headers=build_headers(source),
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()

    if "json" not in response.headers.get("Content-Type", ""):
        raw_path = raw_dir / f"{source.dataset_id}.csv"
        raw_path.write_bytes(response.content)
        return raw_path

    payload = response.json()
    json_path = raw_dir / f"{source.dataset_id}.json"
    with open(json_path, "w", encoding="utf-8") as jsonfile:
        json.dump(payload, jsonfile, indent=2, ensure_ascii=False)
        jsonfile.write("\n")

    records = payload.get("results") if isinstance(payload, dict) else payload
    if isinstance(records, list) and records and isinstance(records[0], dict):
        flatten_to_csv(raw_dir / f"{source.dataset_id}.csv", records)
    return json_path


def fetch_catalog(
    idea: str | None = None,
    dry_run: bool = False,
    data_dir: Path | str | None = None,
) -> list[FetchOutcome]:
    """Fetch every downloadable source, optionally filtered by idea.

    One source failing never stops the run - each outcome is recorded and the
    next source is attempted.

    Args:
        idea: Only handle sources for this idea, or None for all.
        dry_run: Report what would be fetched without downloading.
        data_dir: Data directory, or None for the default.

    Returns:
        list[FetchOutcome]: One outcome per source considered.
    """
    raw_dir = paths.resolve(data_dir) / paths.RAW_SUBDIR
    outcomes: list[FetchOutcome] = []

    for source in by_idea(idea):
        if not source.fetchable:
            outcomes.append(FetchOutcome(source, "skipped", source.access))
            continue
        if dry_run:
            outcomes.append(FetchOutcome(source, "planned", build_url(source)))
            continue
        try:
            path = fetch_source(source, raw_dir)
            outcomes.append(FetchOutcome(source, "fetched", str(path)))
        except Exception as error:  # noqa: BLE001 - record and continue
            outcomes.append(FetchOutcome(source, "failed", str(error)))

    return outcomes
