import csv
import json
import logging
import sys
import time
from collections import Counter
from pathlib import Path

from scrapers.books_scraper import BooksScraper
from scrapers.quotes_scraper import QuotesScraper
from processing.cleaning import clean_record
from processing.validation import validate_record
from processing.deduplication import deduplicate

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output"
LOG_DIR = ROOT / "logs"

OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "scraper.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("pipeline")

FIELDS = [
    "source", "source_url", "name_or_title", "category", "price",
    "rating", "author", "tags", "description", "scraped_at"
]


def run_source(name, scraper):
    collected = []
    failures = 0
    try:
        for record in scraper.scrape():
            collected.append(record)
    except Exception:
        failures += 1
        logger.exception("%s failed; continuing with the next source", name)
    logger.info("%s: collected=%d failures=%d", name, len(collected), failures)
    return collected, failures


def main():
    started = time.perf_counter()

    source_results = {}
    all_raw = []
    failures = 0

    for name, scraper in [
        ("Books to Scrape", BooksScraper()),
        ("Quotes to Scrape", QuotesScraper()),
    ]:
        records, source_failures = run_source(name, scraper)
        source_results[name] = records
        all_raw.extend(records)
        failures += source_failures

    cleaned = []
    cleaning_rejected = 0
    validation_rejected = 0
    validation_errors = Counter()

    for raw in all_raw:
        try:
            record = clean_record(raw)
        except Exception:
            cleaning_rejected += 1
            logger.exception("Cleaning failed for record: %r", raw)
            continue

        valid, errors = validate_record(record)
        if not valid:
            validation_rejected += 1
            validation_errors.update(errors)
            logger.warning("Rejected record: %s", errors)
            continue

        cleaned.append(record)

    unique, duplicates = deduplicate(cleaned)

    output_csv = OUTPUT_DIR / "final_dataset.csv"
    with output_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(unique)

    per_source = {
        name: len(records)
        for name, records in source_results.items()
    }
    cleaned_per_source = Counter(record["source"] for record in cleaned)
    final_per_source = Counter(record["source"] for record in unique)

    elapsed = round(time.perf_counter() - started, 3)

    summary = {
        "records_collected_per_source": per_source,
        "total_records_collected": len(all_raw),
        "records_after_cleaning_and_validation": len(cleaned),
        "cleaning_rejected": cleaning_rejected,
        "validation_rejected": validation_rejected,
        "validation_errors": dict(validation_errors),
        "duplicates_detected_removed": duplicates,
        "final_record_count": len(unique),
        "final_records_per_source": dict(final_per_source),
        "source_failures": failures,
        "execution_time_seconds": elapsed,
        "output_file": str(output_csv.relative_to(ROOT)),
    }

    with (OUTPUT_DIR / "summary_report.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    logger.info("Pipeline completed in %.3fs. Final records=%d", elapsed, len(unique))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
