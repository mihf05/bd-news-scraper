# Data

Generated outputs of the catalog. Everything here is produced from
[`src/earlywarn/catalog.py`](../src/earlywarn/catalog.py) — edit that, then
re-run the commands below rather than editing these files by hand.

| Path | Contents |
|------|----------|
| `sources/datasets.csv` | The catalog, one row per dataset |
| `sources/datasets.json` | The same catalog as JSON records |
| `index.html` | Browsable page: filter the catalog, read every field, download the files |
| `reference/bd_road_death_estimates.csv` | WHO estimate vs official Bangladesh road deaths, 2021 |
| `reference/bd_road_death_estimates.json` | The same, as JSON |
| `raw/` | Where `earlywarn fetch` writes downloaded datasets (git-ignored) |

## Regenerating

```bash
earlywarn export    # sources/datasets.csv and sources/datasets.json
earlywarn page      # index.html
earlywarn validate  # check the catalog before regenerating
```

## Catalog columns

| Column | Meaning |
|--------|---------|
| `idea` | Which application the source serves: `dengue`, `flood`, `road_safety`, `air_quality` |
| `dataset_id` | Stable slug, unique across the catalog, used for filenames |
| `dataset_name` | Human readable name |
| `provider` | Organisation publishing the data |
| `url` | Landing page or API root |
| `data_type` | What the rows actually contain |
| `geography` | Geographic coverage |
| `coverage_start` | First year covered, empty when not applicable |
| `coverage_end` | Last year covered, or `ongoing` |
| `update_frequency` | How often new data lands |
| `formats` | File or response formats offered |
| `access` | How the data is obtained, in one phrase |
| `auth_required` | `no`, or `yes (...)` naming the credential |
| `license` | License as published by the provider |
| `fetchable` | `True` when `earlywarn fetch` can download it unattended |
| `download_url` | Direct URL used by the fetcher, empty when there is none |
| `notes` | Anything worth knowing before using it |

`fetchable` marks the sources the fetcher can download on its own. Everything
else needs a manual step first: an approved API key (Google Flood Forecasting), a
free account (GloFAS, CAMS), a login (IEEE DataPort), a resolved article id
(figshare), or an HTML/PDF parser (FFWC, DGHS, DoE CASE). The `access` column
names the step.

## The page

`index.html` is standalone — no server, no network, no build step. It carries
the four application areas with their download ratios, search and access
filters, a card per dataset with every field and a coverage bar on a shared
timeline, a full-table view of all 17 columns, and download buttons for the CSV
and JSON. Light and dark palettes.

The downloadable files are embedded byte-for-byte identical to the files in this
directory, so what the page hands you is exactly what is committed here.

## Provenance

No datasets are committed. Licenses and URLs are recorded as published by each
provider; several are marked "confirm on download" and should be checked on the
landing page the first time you use them.

The reference figures are cited estimates (WHO ~32,000 vs ~11,000 official road
deaths for 2021), flagged `is_approximate` with their source — not measurements
collected here. That gap is why each application area pairs a national source
with an independent or international one.
