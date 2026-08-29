"""Shared fixtures."""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def repo_data() -> Path:
    """The data directory committed to the repository."""
    return REPO_ROOT / "data"


@pytest.fixture
def built(tmp_path: Path) -> Path:
    """A freshly generated data directory in a temporary location."""
    from earlywarn.export import export_catalog
    from earlywarn.page import build_page

    export_catalog(tmp_path)
    build_page(tmp_path)
    return tmp_path
