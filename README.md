# Early-Warning Data Catalog

A curated, machine-readable catalog of **18 open data sources** for building
early-warning applications in Bangladesh: dengue outbreaks, river flooding, road
accident black spots and air quality.

Finding the data is most of the work. For each source the catalog records what it
covers, how far back, what format it comes in, what it costs you to get it (open
download, free key, application, login, or a parser you have to write) and how
its license is published. One command downloads the sources that can be
downloaded; the rest are listed with the manual step named.

The catalog is defined once in Python and rendered to CSV, JSON and a standalone
HTML page, so the three can never disagree.

## Install

Python 3.10 or newer.

```bash
git clone https://github.com/mihf05/bd-news-scraper.git
cd bd-news-scraper
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -e .
```

That puts the `earlywarn` command on your path. Without installing, every
command also works as `python -m earlywarn ...` with `src/` on `PYTHONPATH`.

## Use it

### Browse the catalog in your terminal

```bash
earlywarn list                      # all 18 sources
earlywarn list --idea flood         # one application area
earlywarn list --access auto        # only what downloads unattended
```

```
opendengue  auto    1990-ongoing    OpenDengue global dengue database
openaq      auto    2013-ongoing    OpenAQ measurements API
waqi        auto    ?-ongoing       World Air Quality Index (aqicn) feed

3 of 18 sources (3 auto)
```

### Browse it in a browser

```bash
earlywarn page
python -m webbrowser data/index.html
```

`data/index.html` is standalone — no server, no network, no build step. Search
and filter the sources, switch between cards and a full table of all 17 columns,
and download the CSV or JSON straight from the page. It follows your system's
light or dark theme.

### Download the datasets

```bash
earlywarn fetch --dry-run           # what would be downloaded, without downloading

export OPENAQ_API_KEY=your_key      # free: OpenAQ Explorer
export WAQI_TOKEN=your_token        # free: aqicn.org/data-platform/token

earlywarn fetch                     # everything that can be fetched
earlywarn fetch --idea air_quality  # one application area
```

Downloads land in `data/raw/`, which is git-ignored. JSON responses are saved as
`.json` and flattened to `.csv` when the payload is a list of records; anything
else is saved verbatim. One source failing never stops the run.

Sources that need a manual step first are reported as skipped with the step
named:

```
skipped  google_flood_forecasting_api  manual step: Free, but pilot access is applied for and approved by email
```

### Regenerate the exports

```bash
earlywarn export                    # data/sources/datasets.{csv,json}
earlywarn validate                  # check the catalog is well formed
```

## What's in the catalog

| Application | Sources | Download unattended | Notable |
|-------------|---------|---------------------|---------|
| Dengue | 3 | 1 | OpenDengue (case counts since 1990, 102 countries), HealthMap, DGHS daily press releases |
| Flood | 6 | 0 | Google Flood Hub + Flood Forecasting API, Inundation History, GRRR, FFWC gauges, GloFAS |
| Road safety | 4 | 0 | figshare 2025 multi-agency dataset (2007–2024), IEEE DataPort, WHO estimates |
| Air quality | 5 | 2 | OpenAQ, WAQI/aqicn, IQAir, CAMS, DoE CASE |

Each column of the catalog is documented in [data/README.md](data/README.md).

**Why two sources per application.** Official national figures undercount. For
2021 the WHO estimated roughly 32,000 road deaths in Bangladesh against roughly
11,000 in official figures — close to a 3× gap, recorded in
`data/reference/bd_road_death_estimates.csv`. Every application area therefore
pairs a national source with an independent or international one, so a model can
be calibrated against the discrepancy instead of inheriting it.

## Project structure

```
early-warning-data-catalog/
├── src/earlywarn/
│   ├── catalog.py            # THE CATALOG — the single source of truth
│   ├── models.py             # DataSource dataclass
│   ├── export.py             # CSV and JSON output
│   ├── page.py               # HTML page renderer
│   ├── fetch.py              # downloader for the open sources
│   ├── cli.py                # the earlywarn command
│   ├── paths.py              # where generated files live
│   └── templates/page.html   # markup and styling for the page
├── data/
│   ├── index.html            # generated page
│   ├── sources/              # generated datasets.csv and datasets.json
│   ├── reference/            # reference figures used for calibration
│   └── raw/                  # downloads (git-ignored)
├── docs/
│   ├── app-ideas.md          # the applications the catalog was assembled for
│   └── adding-a-source.md    # how to extend the catalog
├── tests/                    # pytest suite, no network required
└── pyproject.toml
```

## Contributing

Adding a source is a single dataclass entry — see
[docs/adding-a-source.md](docs/adding-a-source.md).

```bash
pip install -e ".[dev]"
pytest -q
```

The suite runs offline and covers the catalog's integrity, both exports, the
rendered page and every CLI command. One test re-exports the catalog and compares
it byte for byte with the files in `data/`, so a change that forgets to
regenerate them fails CI.

## Notes on the data

No datasets are committed to this repository — only the catalog describing them
and the reference figures. Run `earlywarn fetch` to populate `data/raw/`.

Licenses and URLs are recorded as each provider publishes them, and several are
marked "confirm on download". Confirm them on the landing page the first time you
use a source, and respect each provider's terms.

The two reference figures are cited estimates, flagged `is_approximate` with
their source — they are not measurements collected here.

## License

MIT — see [LICENSE](LICENSE).
