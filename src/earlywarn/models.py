"""Data model for a catalogued source."""

from dataclasses import dataclass, fields


@dataclass(frozen=True)
class DataSource:
    """A single dataset that can feed an early-warning application.

    Attributes:
        idea: Which application the dataset serves (see `earlywarn.catalog.ideas`).
        dataset_id: Stable slug, unique across the catalog, used for filenames.
        dataset_name: Human readable dataset name.
        provider: Organisation publishing the data.
        url: Landing page or API root.
        data_type: What the dataset actually contains.
        geography: Geographic coverage.
        coverage_start: First year covered as a string ("" if not applicable).
        coverage_end: Last year covered, or "ongoing".
        update_frequency: How often new data lands.
        formats: File or response formats offered.
        access: How the data is obtained, in one phrase.
        auth_required: Whether a key, login or approval is needed. Values
            starting with "yes" mark a source as needing credentials.
        license: License as published by the provider.
        fetchable: Whether `earlywarn fetch` can download it unattended.
        download_url: Direct URL used by `earlywarn fetch` ("" if none).
        notes: Anything worth knowing before using it.
    """

    idea: str
    dataset_id: str
    dataset_name: str
    provider: str
    url: str
    data_type: str
    geography: str
    coverage_start: str
    coverage_end: str
    update_frequency: str
    formats: str
    access: str
    auth_required: str
    license: str
    fetchable: bool
    download_url: str = ""
    notes: str = ""

    @property
    def access_class(self) -> str:
        """Classify how much work it takes to obtain this source.

        Returns:
            str: One of "auto" (downloads unattended), "key" (needs
            credentials first) or "manual" (needs a human step first).
        """
        if self.fetchable:
            return "auto"
        if self.auth_required.startswith("yes"):
            return "key"
        return "manual"


COLUMN_NAMES: list[str] = [field.name for field in fields(DataSource)]
