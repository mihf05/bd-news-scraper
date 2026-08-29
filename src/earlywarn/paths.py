"""Where the generated files live.

Every path is derived from one data directory, which defaults to ``./data``
relative to the working directory. Pass ``--data-dir`` to the CLI, or a
``data_dir`` argument to the functions, to put the outputs somewhere else.
"""

from pathlib import Path

DEFAULT_DATA_DIR = Path("data")

CATALOG_CSV = "sources/datasets.csv"
CATALOG_JSON = "sources/datasets.json"
REFERENCE_JSON = "reference/bd_road_death_estimates.json"
REFERENCE_CSV = "reference/bd_road_death_estimates.csv"
PAGE_HTML = "index.html"
RAW_SUBDIR = "raw"


def resolve(data_dir: Path | str | None = None) -> Path:
    """Resolve the data directory to use.

    Args:
        data_dir: Directory to use, or None for the default.

    Returns:
        Path: The data directory (not created).
    """
    return Path(data_dir) if data_dir is not None else DEFAULT_DATA_DIR
