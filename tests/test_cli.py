"""Every command must run end to end without touching the network."""

from pathlib import Path

import pytest

from earlywarn import paths
from earlywarn.catalog import CATALOG
from earlywarn.cli import main


def test_validate_succeeds():
    assert main(["validate"]) == 0


def test_list_prints_every_source(capsys):
    assert main(["list"]) == 0
    out = capsys.readouterr().out
    for source in CATALOG:
        assert source.dataset_id in out


def test_list_filters_by_idea_and_access(capsys):
    assert main(["list", "--idea", "flood"]) == 0
    out = capsys.readouterr().out
    assert "google_flood_hub" in out
    assert "opendengue" not in out

    assert main(["list", "--access", "auto"]) == 0
    out = capsys.readouterr().out
    assert "opendengue" in out
    assert "healthmap" not in out


def test_export_writes_into_the_given_data_dir(tmp_path: Path):
    assert main(["--data-dir", str(tmp_path), "export"]) == 0
    assert (tmp_path / paths.CATALOG_CSV).exists()
    assert (tmp_path / paths.CATALOG_JSON).exists()


def test_page_writes_into_the_given_data_dir(tmp_path: Path):
    assert main(["--data-dir", str(tmp_path), "export"]) == 0
    assert main(["--data-dir", str(tmp_path), "page"]) == 0
    assert (tmp_path / paths.PAGE_HTML).exists()


def test_page_works_before_export_has_ever_run(tmp_path: Path):
    """A first-time user running 'page' straight away still gets a page."""
    assert main(["--data-dir", str(tmp_path), "page"]) == 0
    assert (tmp_path / paths.PAGE_HTML).exists()


def test_fetch_dry_run_touches_nothing(tmp_path: Path, capsys):
    assert main(["--data-dir", str(tmp_path), "fetch", "--dry-run"]) == 0
    assert not (tmp_path / paths.RAW_SUBDIR).exists()
    assert "would fetch" in capsys.readouterr().out


def test_unknown_idea_is_rejected():
    with pytest.raises(SystemExit):
        main(["list", "--idea", "not_an_idea"])
