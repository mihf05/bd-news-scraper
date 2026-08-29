"""Catalog of open data sources for the Bangladesh life-saving app ideas.

The catalog below is the single source of truth. It can be exported to CSV and
JSON (``export``) and the openly downloadable entries can be fetched to disk
(``fetch``).

Usage:
    python scripts/data_sources.py export
    python scripts/data_sources.py fetch [--idea dengue] [--dry-run]
"""

import argparse
import csv
import json
import sys
from dataclasses import asdict, dataclass, field, fields
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SOURCES_DIR = DATA_DIR / "sources"
RAW_DIR = DATA_DIR / "raw"

REQUEST_TIMEOUT = 60
USER_AGENT = "bd-news-scraper-datasources/1.0"


@dataclass
class DataSource:
    """A single dataset that can feed one of the app ideas.

    Attributes:
        idea: Which app idea the dataset serves.
        dataset_id: Stable slug used for filenames.
        dataset_name: Human readable dataset name.
        provider: Organisation publishing the data.
        url: Landing page or API root.
        data_type: What the dataset actually contains.
        geography: Geographic coverage.
        coverage_start: First year covered ("" if not applicable).
        coverage_end: Last year covered, or "ongoing".
        update_frequency: How often new data lands.
        formats: File/response formats offered.
        access: How the data is obtained.
        auth_required: Whether a key, login or approval is needed.
        license: License as published (confirm on first download).
        fetchable: Whether ``fetch`` can download it unattended.
        download_url: Direct URL used by ``fetch`` ("" if none).
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


CATALOG: list[DataSource] = [
    # ------------------------------------------------------------------ dengue
    DataSource(
        idea="dengue",
        dataset_id="opendengue",
        dataset_name="OpenDengue global dengue database",
        provider="OpenDengue (LSHTM-led collaboration)",
        url="https://opendengue.org/",
        data_type="Aggregated dengue case counts by admin unit and time period",
        geography="102 dengue-affected countries incl. Bangladesh",
        coverage_start="1990",
        coverage_end="ongoing",
        update_frequency="Versioned releases (v1.2 = 56M+ cases)",
        formats="CSV",
        access="Open download from opendengue.org and the OpenDengue GitHub org",
        auth_required="no",
        license="CC BY 4.0 (confirm on download)",
        fetchable=True,
        download_url="https://opendengue.org/data/OpenDengue_extract_V1_2.csv",
        notes="Compiled from ministry of health sites, peer-reviewed papers and "
              "disease databases. Filter to Bangladesh on the country column.",
    ),
    DataSource(
        idea="dengue",
        dataset_id="healthmap",
        dataset_name="HealthMap outbreak alerts",
        provider="HealthMap (Boston Children's Hospital)",
        url="https://www.healthmap.org/",
        data_type="Near-real-time outbreak signals from ProMED, news and eyewitness reports",
        geography="Global",
        coverage_start="2006",
        coverage_end="ongoing",
        update_frequency="Continuous",
        formats="HTML, JSON (undocumented endpoints)",
        access="Site scrape or partner access; feeds WHO outbreak intelligence",
        auth_required="partner agreement for bulk access",
        license="Terms of use apply",
        fetchable=False,
        notes="Use for leading signal ahead of official counts, not as ground truth.",
    ),
    DataSource(
        idea="dengue",
        dataset_id="dghs_dengue_press_release",
        dataset_name="DGHS daily dengue press release",
        provider="Directorate General of Health Services, Bangladesh",
        url="https://dghs.gov.bd/",
        data_type="Daily hospital admissions and deaths by division and hospital",
        geography="Bangladesh",
        coverage_start="2019",
        coverage_end="ongoing",
        update_frequency="Daily during season",
        formats="PDF, HTML",
        access="Published as daily PDFs; needs a parser",
        auth_required="no",
        license="Government publication",
        fetchable=False,
        notes="Official ground truth to calibrate against. Lags real infection curve.",
    ),

    # ------------------------------------------------------------------- flood
    DataSource(
        idea="flood",
        dataset_id="google_flood_hub",
        dataset_name="Google Flood Hub forecasts",
        provider="Google Research",
        url="https://sites.research.google/floods/",
        data_type="Riverine flood forecasts up to 7 days ahead",
        geography="80+ countries; launched in India and Bangladesh",
        coverage_start="2018",
        coverage_end="ongoing",
        update_frequency="Continuous",
        formats="Web UI, API",
        access="Free for governments, aid organisations and individuals",
        auth_required="no (viewer)",
        license="Google terms",
        fetchable=False,
        notes="Bangladesh-proven: used in anticipatory cash-relief pilots with IRC.",
    ),
    DataSource(
        idea="flood",
        dataset_id="google_flood_forecasting_api",
        dataset_name="Google Flood Forecasting API",
        provider="Google Research",
        url="https://developers.google.com/flood-forecasting",
        data_type="Programmatic gauge-level flood forecasts and thresholds",
        geography="Flood Hub coverage area",
        coverage_start="2023",
        coverage_end="ongoing",
        update_frequency="Continuous",
        formats="JSON",
        access="Free, but pilot access is applied for and approved by email",
        auth_required="yes (approved API key)",
        license="Google API terms",
        fetchable=False,
        notes="The alert layer would consume this directly - no model to train.",
    ),
    DataSource(
        idea="flood",
        dataset_id="google_inundation_history",
        dataset_name="Inundation History dataset",
        provider="Google Research",
        url="https://sites.research.google/floods/",
        data_type="Historical satellite-derived inundation extents",
        geography="Global flood-prone basins",
        coverage_start="1999",
        coverage_end="2020",
        update_frequency="Static release",
        formats="Raster / tabular",
        access="Public research dataset",
        auth_required="no",
        license="Confirm on download",
        fetchable=False,
        notes="Training data if you model inundation yourself instead of consuming forecasts.",
    ),
    DataSource(
        idea="flood",
        dataset_id="google_grrr",
        dataset_name="Google Runoff Reanalysis & Reforecast (GRRR)",
        provider="Google Research",
        url="https://sites.research.google/floods/",
        data_type="Modelled historical and reforecast river runoff",
        geography="Global",
        coverage_start="1980",
        coverage_end="2023",
        update_frequency="Static release",
        formats="NetCDF / tabular",
        access="Public research dataset",
        auth_required="no",
        license="Confirm on download",
        fetchable=False,
        notes="Long training record for a custom risk model.",
    ),
    DataSource(
        idea="flood",
        dataset_id="ffwc",
        dataset_name="FFWC river water level bulletins",
        provider="Flood Forecasting and Warning Centre, BWDB",
        url="http://www.ffwc.gov.bd/",
        data_type="Observed river gauge levels vs danger levels, daily bulletins",
        geography="Bangladesh river gauge network",
        coverage_start="",
        coverage_end="ongoing",
        update_frequency="Daily (more often in monsoon)",
        formats="HTML, PDF",
        access="Public website; needs a parser",
        auth_required="no",
        license="Government publication",
        fetchable=False,
        notes="Official national ground truth; pair with Flood Hub forecasts.",
    ),
    DataSource(
        idea="flood",
        dataset_id="glofas",
        dataset_name="GloFAS global flood awareness system",
        provider="Copernicus Emergency Management Service",
        url="https://global-flood.emergency.copernicus.eu/",
        data_type="Global river discharge forecasts and reanalysis",
        geography="Global",
        coverage_start="1979",
        coverage_end="ongoing",
        update_frequency="Daily",
        formats="NetCDF, GRIB via CDS API",
        access="Free Copernicus/CDS account",
        auth_required="yes (free account)",
        license="Copernicus open licence",
        fetchable=False,
        notes="Independent cross-check against Flood Hub.",
    ),

    # ------------------------------------------------------------ road safety
    DataSource(
        idea="road_safety",
        dataset_id="figshare_bd_road_accidents_2025",
        dataset_name="Integrated Bangladesh road accident dataset (2007-2024)",
        provider="figshare (multi-agency compilation)",
        url="https://figshare.com/",
        data_type="Accident records with location, severity and vehicle details",
        geography="Bangladesh",
        coverage_start="2007",
        coverage_end="2024",
        update_frequency="Static release (2025)",
        formats="CSV / XLSX",
        access="Open download via figshare article and API",
        auth_required="no",
        license="Usually CC BY on figshare - confirm on the article page",
        fetchable=False,
        notes="Integrates ARI (BUET), BRTA, Dhaka Metropolitan Police and Military "
              "Police records plus primary field collection - the multi-source "
              "cross-check the black-spot model needs. Resolve the article ID first.",
    ),
    DataSource(
        idea="road_safety",
        dataset_id="ieee_dataport_bd_accidents",
        dataset_name="Bangladesh road accident dataset from newspaper reports",
        provider="IEEE DataPort",
        url="https://ieee-dataport.org/",
        data_type="Accident records extracted from newspaper reporting",
        geography="Bangladesh",
        coverage_start="2016",
        coverage_end="2019",
        update_frequency="Static release",
        formats="CSV",
        access="IEEE DataPort account required",
        auth_required="yes (login)",
        license="IEEE DataPort terms",
        fetchable=False,
        notes="Media-sourced angle to compare against official figures.",
    ),
    DataSource(
        idea="road_safety",
        dataset_id="who_road_safety",
        dataset_name="WHO Global Status Report on Road Safety",
        provider="World Health Organization",
        url="https://www.who.int/teams/social-determinants-of-health/safety-and-mobility/global-status-report-on-road-safety-2023",
        data_type="Modelled national road traffic death estimates",
        geography="Global, per country",
        coverage_start="2000",
        coverage_end="2021",
        update_frequency="Every ~3 years",
        formats="PDF, XLSX",
        access="Open download",
        auth_required="no",
        license="CC BY-NC-SA 3.0 IGO",
        fetchable=False,
        notes="Source of the ~3x gap vs official Bangladesh reporting - see "
              "data/reference/bd_road_death_estimates.csv.",
    ),
    DataSource(
        idea="road_safety",
        dataset_id="prothom_alo_scrape",
        dataset_name="Prothom Alo accident reporting (this repository)",
        provider="Self-collected via src/scraper.py",
        url="https://github.com/mihf05/bd-news-scraper",
        data_type="News articles with headline, content, tags, sections and timestamps",
        geography="Bangladesh",
        coverage_start="2010",
        coverage_end="ongoing",
        update_frequency="Incremental, on each run",
        formats="CSV (yearly files)",
        access="Run the scraper in this repo",
        auth_required="no",
        license="Educational/research use - see repository disclaimer",
        fetchable=False,
        notes="Continuous media-sourced stream. Filter on accident keywords to "
              "extend the newspaper-derived datasets past 2019.",
    ),

    # ------------------------------------------------------------- air quality
    DataSource(
        idea="air_quality",
        dataset_id="openaq",
        dataset_name="OpenAQ measurements API",
        provider="OpenAQ",
        url="https://docs.openaq.org/",
        data_type="Station-level pollutant measurements (PM2.5, PM10, NO2, ...)",
        geography="Global incl. Dhaka",
        coverage_start="2013",
        coverage_end="ongoing",
        update_frequency="Continuous",
        formats="JSON (REST API v3), CSV exports",
        access="REST API; free API key from the OpenAQ Explorer",
        auth_required="yes (free API key, X-API-Key header)",
        license="CC BY 4.0",
        fetchable=True,
        download_url="https://api.openaq.org/v3/locations?iso=BD&limit=1000",
        notes="Fastest of the four to get running. Set OPENAQ_API_KEY before fetching.",
    ),
    DataSource(
        idea="air_quality",
        dataset_id="waqi",
        dataset_name="World Air Quality Index (aqicn) feed",
        provider="WAQI / aqicn.org",
        url="https://aqicn.org/data-platform/token/",
        data_type="Real-time AQI per station with per-pollutant breakdown",
        geography="Global; several Dhaka stations",
        coverage_start="",
        coverage_end="ongoing",
        update_frequency="Hourly",
        formats="JSON",
        access="Free token from aqicn.org/data-platform/token",
        auth_required="yes (free token)",
        license="WAQI terms, attribution required",
        fetchable=True,
        download_url="https://api.waqi.info/feed/dhaka/",
        notes="Set WAQI_TOKEN before fetching.",
    ),
    DataSource(
        idea="air_quality",
        dataset_id="iqair",
        dataset_name="IQAir AirVisual API",
        provider="IQAir",
        url="https://www.iqair.com/air-pollution-data-api",
        data_type="Current AQI plus pollution forecasts",
        geography="Global",
        coverage_start="",
        coverage_end="ongoing",
        update_frequency="Hourly",
        formats="JSON",
        access="Paid tiers (limited free community tier)",
        auth_required="yes (paid key for forecasts)",
        license="Commercial terms",
        fetchable=False,
        notes="Only needed if you want vendor forecasts rather than modelling spikes yourself.",
    ),
    DataSource(
        idea="air_quality",
        dataset_id="cams",
        dataset_name="CAMS global atmospheric composition forecasts",
        provider="Copernicus Atmosphere Monitoring Service",
        url="https://atmosphere.copernicus.eu/",
        data_type="Modelled and satellite-derived pollutant fields",
        geography="Global",
        coverage_start="2003",
        coverage_end="ongoing",
        update_frequency="Daily",
        formats="NetCDF, GRIB via ADS API",
        access="Free Copernicus account",
        auth_required="yes (free account)",
        license="Copernicus open licence",
        fetchable=False,
        notes="Fills gaps where Dhaka ground stations are sparse or offline.",
    ),
    DataSource(
        idea="air_quality",
        dataset_id="doe_case",
        dataset_name="DoE CASE air quality monitoring",
        provider="Department of Environment, Bangladesh",
        url="http://case.doe.gov.bd/",
        data_type="Official CAMS station readings and national AQI",
        geography="Bangladesh (Dhaka and divisional cities)",
        coverage_start="2013",
        coverage_end="ongoing",
        update_frequency="Hourly/daily",
        formats="HTML",
        access="Public website; needs a parser",
        auth_required="no",
        license="Government publication",
        fetchable=False,
        notes="Official national reference to cross-check OpenAQ and WAQI.",
    ),
]

COLUMN_NAMES: list[str] = [f.name for f in fields(DataSource)]


def export_catalog(output_dir: Path = SOURCES_DIR) -> tuple[Path, Path]:
    """Write the catalog to CSV and JSON.

    Args:
        output_dir: Directory the two files are written to.

    Returns:
        tuple[Path, Path]: Paths of the written CSV and JSON files.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "datasets.csv"
    json_path = output_dir / "datasets.json"

    rows = [asdict(source) for source in CATALOG]

    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=COLUMN_NAMES)
        writer.writeheader()
        writer.writerows(rows)

    with open(json_path, "w", encoding="utf-8") as jsonfile:
        json.dump(rows, jsonfile, indent=2, ensure_ascii=False)
        jsonfile.write("\n")

    return csv_path, json_path


def build_headers(source: DataSource) -> dict[str, str]:
    """Build request headers, injecting API keys from the environment.

    Args:
        source: Data source about to be requested.

    Returns:
        dict[str, str]: Headers for the request.
    """
    import os

    headers = {"User-Agent": USER_AGENT}
    if source.dataset_id == "openaq":
        key = os.environ.get("OPENAQ_API_KEY")
        if key:
            headers["X-API-Key"] = key
    return headers


def build_url(source: DataSource) -> str:
    """Return the download URL with any required token appended.

    Args:
        source: Data source about to be requested.

    Returns:
        str: URL to request.
    """
    import os

    if source.dataset_id == "waqi":
        token = os.environ.get("WAQI_TOKEN", "")
        return f"{source.download_url}?token={token}"
    return source.download_url


def fetch_source(source: DataSource, output_dir: Path = RAW_DIR) -> Path:
    """Download one source and save it to disk.

    JSON responses are saved as ``.json`` and also flattened to ``.csv`` when
    the payload is a list of records. Anything else is saved verbatim.

    Args:
        source: Data source to download.
        output_dir: Directory raw downloads are written to.

    Returns:
        Path: Path of the primary saved file.

    Raises:
        requests.HTTPError: If the request fails.
    """
    import requests

    output_dir.mkdir(parents=True, exist_ok=True)
    response = requests.get(
        build_url(source),
        headers=build_headers(source),
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")
    if "json" in content_type:
        payload = response.json()
        json_path = output_dir / f"{source.dataset_id}.json"
        with open(json_path, "w", encoding="utf-8") as jsonfile:
            json.dump(payload, jsonfile, indent=2, ensure_ascii=False)
            jsonfile.write("\n")

        records = payload.get("results") if isinstance(payload, dict) else payload
        if isinstance(records, list) and records and isinstance(records[0], dict):
            csv_path = output_dir / f"{source.dataset_id}.csv"
            keys = list(records[0].keys())
            with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=keys, extrasaction="ignore")
                writer.writeheader()
                for record in records:
                    writer.writerow({k: json.dumps(v) if isinstance(v, (dict, list)) else v
                                     for k, v in record.items()})
        return json_path

    raw_path = output_dir / f"{source.dataset_id}.csv"
    raw_path.write_bytes(response.content)
    return raw_path


def fetch_catalog(idea: str | None = None, dry_run: bool = False) -> int:
    """Fetch every openly downloadable source, optionally filtered by idea.

    Args:
        idea: Only fetch sources for this idea, or None for all.
        dry_run: List what would be fetched without downloading.

    Returns:
        int: Number of sources successfully downloaded.
    """
    selected = [s for s in CATALOG if s.fetchable and (idea is None or s.idea == idea)]
    skipped = [s for s in CATALOG if not s.fetchable and (idea is None or s.idea == idea)]

    downloaded = 0
    for source in selected:
        if dry_run:
            print(f"would fetch {source.dataset_id:<32} {build_url(source)}")
            continue
        try:
            path = fetch_source(source)
            print(f"fetched  {source.dataset_id:<32} -> {path}")
            downloaded += 1
        except Exception as error:  # noqa: BLE001 - report and continue
            print(f"FAILED   {source.dataset_id:<32} {error}", file=sys.stderr)

    for source in skipped:
        print(f"skipped  {source.dataset_id:<32} manual step: {source.access}")

    return downloaded


def main() -> None:
    """Command line entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("export", help="Write the catalog to CSV and JSON")

    fetch_parser = subparsers.add_parser("fetch", help="Download the open sources")
    fetch_parser.add_argument("--idea", choices=sorted({s.idea for s in CATALOG}))
    fetch_parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    if args.command == "export":
        csv_path, json_path = export_catalog()
        print(f"wrote {csv_path}")
        print(f"wrote {json_path}")
    else:
        fetch_catalog(idea=args.idea, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
