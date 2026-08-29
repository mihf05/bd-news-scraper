"""Early-warning data catalog.

A curated, machine-readable catalog of open data sources for building
early-warning applications in Bangladesh - dengue outbreaks, river flooding,
road accident black spots and air quality.

The catalog is defined once in :mod:`earlywarn.catalog` and rendered to CSV,
JSON and a standalone HTML page, so the three can never disagree.
"""

from earlywarn.models import COLUMN_NAMES, DataSource

__version__ = "1.0.0"
__all__ = ["COLUMN_NAMES", "DataSource", "__version__"]
