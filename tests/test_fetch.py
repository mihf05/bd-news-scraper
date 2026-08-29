"""Fetching must be predictable offline: no source is downloaded by surprise."""

import csv
from pathlib import Path

from earlywarn.catalog import CATALOG, by_idea, get
from earlywarn.fetch import build_headers, build_url, fetch_catalog, flatten_to_csv


def test_dry_run_downloads_nothing(tmp_path: Path):
    outcomes = fetch_catalog(dry_run=True, data_dir=tmp_path)
    assert not (tmp_path / "raw").exists()
    assert {o.status for o in outcomes} <= {"planned", "skipped"}


def test_only_fetchable_sources_are_planned(tmp_path: Path):
    outcomes = fetch_catalog(dry_run=True, data_dir=tmp_path)
    planned = {o.source.dataset_id for o in outcomes if o.status == "planned"}
    assert planned == {s.dataset_id for s in CATALOG if s.fetchable}


def test_skipped_outcomes_name_the_manual_step(tmp_path: Path):
    for outcome in fetch_catalog(dry_run=True, data_dir=tmp_path):
        if outcome.status == "skipped":
            assert outcome.detail == outcome.source.access
            assert outcome.detail.strip()


def test_idea_filter_limits_the_run(tmp_path: Path):
    outcomes = fetch_catalog(idea="flood", dry_run=True, data_dir=tmp_path)
    assert {o.source.dataset_id for o in outcomes} == {s.dataset_id for s in by_idea("flood")}


def test_a_failing_source_is_recorded_not_raised(tmp_path: Path, monkeypatch):
    def explode(source, raw_dir):
        raise RuntimeError("network is down")

    monkeypatch.setattr("earlywarn.fetch.fetch_source", explode)
    outcomes = fetch_catalog(idea="air_quality", data_dir=tmp_path)
    failed = [o for o in outcomes if o.status == "failed"]
    assert failed and all("network is down" in o.detail for o in failed)


def test_credentials_come_from_the_environment(monkeypatch):
    monkeypatch.setenv("OPENAQ_API_KEY", "test-key")
    monkeypatch.setenv("WAQI_TOKEN", "test-token")
    assert build_headers(get("openaq"))["X-API-Key"] == "test-key"
    assert build_url(get("waqi")).endswith("token=test-token")


def test_missing_credentials_do_not_crash(monkeypatch):
    monkeypatch.delenv("OPENAQ_API_KEY", raising=False)
    monkeypatch.delenv("WAQI_TOKEN", raising=False)
    assert "X-API-Key" not in build_headers(get("openaq"))
    assert build_url(get("waqi")).endswith("token=")


def test_flatten_to_csv_encodes_nested_values(tmp_path: Path):
    path = tmp_path / "out.csv"
    flatten_to_csv(path, [{"id": 1, "coords": {"lat": 23.8}}, {"id": 2, "coords": None}])
    with open(path, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert rows[0]["coords"] == '{"lat": 23.8}'
    assert rows[1]["id"] == "2"
