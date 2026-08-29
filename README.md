# BD news Scraper

A Python-based web scraper. This tool efficiently downloads, processes, and stores news articles in CSV format with comprehensive metadata.

## ✨ Features

- 🔄 Incremental scraping with automatic progress tracking
- 📊 Exports data to yearly CSV files with 20+ metadata fields
- 🔍 Smart filtering and data validation
- 📝 Comprehensive logging system
- ⚙️ Configurable date ranges and request parameters
- 🛡️ Robust error handling and retry mechanisms
- 💾 Efficient memory usage with modern Python dataclasses
- 🗂️ Companion data source catalog with CSV, JSON and a browsable HTML page

## 📋 Requirements

- **Python 3.10+** (uses modern type hints and language features)
- See [requirements.txt](requirements.txt) for package dependencies

## 🚀 Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/mihf05/bd-news-scraper.git
   cd prothom-alo-scraper
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configure settings**
   
   Edit `config.json` to customize scraping parameters:
   - `start_date`: Starting date for scraping (DD-MM-YYYY)
   - `output_directory`: Where to save CSV files
   - `log_directory`: Where to save log files
   - `threshold`: Number of days to scrape per batch
   - `limit`: Articles per API request
   - `max_attempts`: Maximum retry attempts for failed requests

## 📖 Usage

Run the scraper:
```bash
python src/scraper.py
```

The scraper will:
1. Load configuration from `config.json`
2. Resume from the last scraped date
3. Fetch articles in batches
4. Process and validate data
5. Save to yearly CSV files (e.g., `2024.csv`)
6. Update progress in `config.json`
7. Generate detailed logs

## 🗂️ Data Source Catalog

Alongside the scraper, `scripts/data_sources.py` maintains a catalog of 18 open
data sources for early-warning apps in Bangladesh — dengue, flood, road safety
and air quality. The catalog is defined once in that script and exported to CSV,
JSON and a browsable HTML page, so the three can't drift apart.

### View the catalog

```bash
python scripts/data_sources.py page
```

Then open `data/index.html` in a browser. It is standalone — no server, no
network, no build step. Search and filter the sources, switch between card and
full-table views, and download the CSV or JSON straight from the page.

### Regenerate the CSV and JSON

```bash
python scripts/data_sources.py export
```

Writes `data/sources/datasets.csv` and `data/sources/datasets.json`. Run this
after editing the `CATALOG` list in `scripts/data_sources.py`, then re-run
`page` so the HTML picks up the change.

### Download the datasets themselves

```bash
# See what would be downloaded, without fetching
python scripts/data_sources.py fetch --dry-run

# Free keys: OpenAQ Explorer, and aqicn.org/data-platform/token
export OPENAQ_API_KEY=your_key
export WAQI_TOKEN=your_token

# Fetch everything, or one idea at a time
python scripts/data_sources.py fetch
python scripts/data_sources.py fetch --idea air_quality
```

Downloads land in `data/raw/`, which is git-ignored. JSON responses are saved as
`.json` and flattened to `.csv` when the payload is a list of records; anything
else is saved verbatim. Failures are reported per source and don't stop the run.

Sources needing a manual step first — an approved API key, a free account, a
login, or an HTML/PDF parser — are listed as skipped with the step named. See
[data/README.md](data/README.md) for the full column reference.

## 📁 Project Structure

```
bd-news-scraper/
├── src/
│   ├── config.py               # Configuration management
│   ├── models.py               # Data models (ItemModel, ItemsModel)
│   ├── processor.py            # Data processing and cleaning
│   ├── requester.py            # API requests with retry logic
│   ├── saver.py                # CSV file operations
│   ├── scraper.py              # Main scraper orchestration
│   └── utils.py                # Utility functions
├── scripts/
│   ├── data_sources.py         # Data source catalog: export, page, fetch
│   └── page_template.html      # Markup and styling for the catalog page
├── data/
│   ├── index.html              # Browsable catalog page (generated)
│   ├── sources/                # datasets.csv and datasets.json (generated)
│   ├── reference/              # Reference figures used for calibration
│   └── raw/                    # Downloaded datasets (git-ignored)
├── docs/
│   └── app-ideas.md            # App ideas the catalog was assembled for
├── config.json                 # Configuration file
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 📊 Output Format

Articles are saved with the following fields:

| Field | Description |
|-------|-------------|
| `text_id` | Unique article identifier |
| `text_headline` | Article headline |
| `text_subheadline` | Article subheadline |
| `text_summary` | Article summary |
| `text_content` | Full article content (cleaned) |
| `text_main_author` | Primary author name |
| `text_authors` | All authors (comma-separated) |
| `text_url` | Article URL |
| `int_read_time` | Estimated read time (minutes) |
| `text_seo_description` | SEO meta description |
| `text_seo_tags` | SEO keywords |
| `text_tags` | Article tags |
| `text_sections` | Article sections/categories |
| `int_word_count` | Word count |
| `date_published` | Publication timestamp |
| `date_first_published_at` | First publication timestamp |
| `date_last_published_at` | Last publication timestamp |
| `date_created_at` | Creation timestamp |
| `date_updated_at` | Last update timestamp |
| `date_content_updated_at` | Content update timestamp |


## 🔧 Advanced Configuration

### Example `config.json`:
```json
{
  "start_date": {
    "description": "Starting date for scraping",
    "value": "01-01-2020"
  },
  "last_scraped_date": {
    "description": "Last successfully scraped date",
    "value": null
  },
  "threshold": {
    "description": "Days per batch",
    "value": 1
  },
  "limit": {
    "description": "Articles per request",
    "value": 20
  },
  "max_attempts": {
    "description": "Maximum retry attempts",
    "value": 3
  }
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⚠️ Disclaimer

This scraper is for educational and research purposes only. Please respect Prothom Alo's terms of service and robots.txt when using this tool.
