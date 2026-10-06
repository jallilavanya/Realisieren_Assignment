# Multi-Source Web Scraping & Data Consolidation

A medium-level Python take-home implementation for scraping:

- Books to Scrape
- Quotes to Scrape

The pipeline follows:

**Scraping → Cleaning → Validation → Deduplication → Consolidation → CSV + JSON summary**

## Python version

Python 3.11+ recommended.

## Setup

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

From the `scraping_assignment` directory:

```bash
python main.py
```

The program writes:

```text
output/final_dataset.csv
output/summary_report.json
logs/scraper.log
```

## Source handling

Each source has its own scraper module so selectors and pagination remain isolated.

### Books to Scrape

The scraper starts at the public catalog and follows the `next` link until no next page exists. It extracts title, product URL, price, rating, availability text, source and timestamp.

### Quotes to Scrape

The scraper starts at the public quote listing and follows the `next` link until the final page. It extracts quote text, author, tags, source and timestamp.

No page count is hard-coded.

## Data model

The consolidated record contains:

| Field | Purpose |
|---|---|
| source | Original source |
| source_url | Original page/product URL |
| name_or_title | Book title or quote text |
| category | Source-specific category when available |
| price | Numeric price when available |
| rating | Numeric rating when available |
| author | Author when available |
| tags | Comma-separated tags when available |
| description | Additional source information |
| scraped_at | UTC scrape timestamp |

Missing source-specific fields remain `null`/empty rather than being invented.

## Cleaning

Cleaning is kept separate from scraping.

- Collapses repeated whitespace.
- Trims text.
- Converts list tags to a consistent string.
- Converts currency strings to numeric values.
- Converts ratings to numeric values.
- Validates HTTP/HTTPS URLs.
- Normalizes missing values to `None`.

## Validation

Records require:

- source
- source_url
- name_or_title

When present, price must be numeric, rating must be between 0 and 5, and the URL must look like an HTTP(S) URL.

Invalid records are rejected and counted instead of crashing the entire pipeline.

## Deduplication

The duplicate key is:

```text
normalized source + normalized name_or_title + normalized author
```

Normalization uses Unicode normalization, whitespace collapsing and case folding.

The source is included deliberately. This prevents a quote and a book with identical text from being incorrectly treated as the same cross-source record.

Duplicates are removed from the final dataset and counted in `summary_report.json`.

## Error handling

HTTP failures are retried a limited number of times. A source-level exception is logged and the pipeline continues to the other source.

Missing selectors are handled defensively where practical. The scraper does not bypass authentication, CAPTCHAs, robots restrictions or access controls.

## Testing

Run:

```bash
pytest -q
```

Tests cover price parsing, cleaning, validation and duplicate detection.

## Assumptions

1. The two provided websites remain available and retain their general practice-site structure.
2. A source's own URL/text identity is a safer duplicate boundary than cross-source fuzzy matching.
3. The assignment does not require crawling every individual quote author page or every individual book detail page.
4. Missing source-specific fields are legitimate and are not fabricated.

## Known limitations

- The implementation uses synchronous HTTP requests.
- It does not persist checkpoints between runs.
- It does not use a database.
- Fuzzy duplicate detection is intentionally not enabled because false positives would be more damaging than missing an ambiguous duplicate.
- Site structure changes may require selector updates.

## Production improvements

For a production scraper, I would add configurable rate limiting, exponential backoff, checkpoint/resume, structured JSON logging, metrics, a persistent storage layer, schema versioning, alerting, and source-specific contract tests.

## AI usage

See `AI_USAGE.md`.
