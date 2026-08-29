# Adding a data source

Every output — the CSV, the JSON and the HTML page — is generated from one list
in [`src/earlywarn/catalog.py`](../src/earlywarn/catalog.py). Add a source
there and the rest follows.

## 1. Add the entry

Append a `DataSource(...)` to `CATALOG`, in the block for its idea:

```python
DataSource(
    idea="flood",                      # a key from IDEAS
    dataset_id="my_source",            # unique slug, used for filenames
    dataset_name="Readable dataset name",
    provider="Who publishes it",
    url="https://example.org/dataset", # landing page or API root
    data_type="What the rows actually contain",
    geography="What it covers",
    coverage_start="2015",             # "" when not applicable
    coverage_end="ongoing",            # or a year
    update_frequency="Daily",
    formats="CSV, JSON",
    access="How you get it, in one phrase",
    auth_required="no",                # "yes (...)" if credentials are needed
    license="As published by the provider",
    fetchable=False,                   # True only if `fetch` can download it
    download_url="",                   # required when fetchable is True
    notes="Anything worth knowing before using it.",
),
```

Record the license and URL **as the provider publishes them**. If you have not
confirmed the license, say so in the field (`"CC BY 4.0 (confirm on download)"`)
rather than guessing.

## 2. Decide whether it is fetchable

`fetchable=True` means `earlywarn fetch` can download it unattended, with no
human step. Set it only when a direct `download_url` returns the data.

Anything that needs an approved key, a free account, a login, a resolved article
id, or a parser for an HTML or PDF page stays `fetchable=False`. Those are
reported as skipped, with the `access` phrase shown as the step needed — so
write `access` as the instruction someone would follow.

If the source needs a credential, read it from the environment in
[`fetch.py`](../src/earlywarn/fetch.py) (`build_headers` for a header,
`build_url` for a query parameter) and document the variable in the module
docstring and the README. Never commit a key.

## 3. Adding a new idea

Add the key and label to `IDEAS` and a one-line summary to `IDEA_SUMMARIES`.
The page picks it up automatically; it will use the accent colour unless you
also add a hue for it in the `HUES` map in
[`templates/page.html`](../src/earlywarn/templates/page.html).

## 4. Regenerate and check

```bash
earlywarn validate      # duplicate ids, empty fields, fetchable without a URL
earlywarn export        # rewrites data/sources/
earlywarn page          # rewrites data/index.html
pytest -q
```

Commit the regenerated files in `data/` along with your change — CI fails if
they are stale.
