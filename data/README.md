# Data

Source catalog and reference figures for the four app ideas in
[docs/app-ideas.md](../docs/app-ideas.md).

## What is here

| Path | Contents |
|------|----------|
| `sources/datasets.csv` | Catalog of 18 candidate data sources, one row per dataset |
| `sources/datasets.json` | Same catalog as JSON records |
| `reference/bd_road_death_estimates.csv` | WHO estimate vs official Bangladesh road deaths (2021) |
| `reference/bd_road_death_estimates.json` | Same, as JSON |
| `raw/` | Where `fetch` writes downloaded datasets (git-ignored) |

The catalog lives in `scripts/data_sources.py` as the single source of truth;
both files are generated from it, so edit the script and re-export rather than
editing the CSV or JSON by hand.

## Catalog columns

`idea`, `dataset_id`, `dataset_name`, `provider`, `url`, `data_type`,
`geography`, `coverage_start`, `coverage_end`, `update_frequency`, `formats`,
`access`, `auth_required`, `license`, `fetchable`, `download_url`, `notes`.

`fetchable` marks the sources `fetch` can download unattended. Everything else
needs a manual step first: an approved API key (Google Flood Forecasting), a
free account (GloFAS, CAMS), a login (IEEE DataPort), a resolved article ID
(figshare), or an HTML/PDF parser (FFWC, DGHS, DoE CASE).

Licenses and URLs are recorded as published by each provider. Confirm them on
the landing page the first time you download - several are marked
"confirm on download" for that reason.

## Usage

```bash
# Regenerate the catalog files after editing scripts/data_sources.py
python scripts/data_sources.py export

# See what would be downloaded
python scripts/data_sources.py fetch --dry-run

# Download the open sources (optionally one idea at a time)
export OPENAQ_API_KEY=...   # free key from the OpenAQ Explorer
export WAQI_TOKEN=...       # free token from aqicn.org/data-platform/token
python scripts/data_sources.py fetch --idea air_quality
```

JSON responses are saved as `.json` and flattened to `.csv` when the payload is
a list of records; other responses are saved verbatim. Failures are reported per
source and do not stop the run.

## Note on the committed data

The catalog and the reference figures are committed; the actual datasets are
not. They were not downloaded in the environment these files were written in -
outbound access to `opendengue.org`, `api.openaq.org`, `api.figshare.com` and
`api.waqi.info` was refused by that environment's egress policy, so no case
counts, AQI readings or accident records were retrieved. Run the fetcher on an
unrestricted network to populate `data/raw/`.

## Why multiple sources per idea

For 2021 WHO estimated roughly 32,000 road deaths in Bangladesh against roughly
11,000 in official figures - close to a 3x gap (`reference/bd_road_death_estimates.csv`).
Every idea in the catalog therefore pairs an official national source with at
least one independent or international one, so the model can be calibrated
against the discrepancy instead of inheriting it.
