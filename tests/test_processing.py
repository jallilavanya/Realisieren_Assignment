import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from processing.cleaning import clean_record, parse_price
from processing.validation import validate_record
from processing.deduplication import deduplicate


def test_parse_price():
    assert parse_price("£51.77") == 51.77
    assert parse_price("€12.50") == 12.50
    assert parse_price(None) is None


def test_clean_record():
    record = clean_record({
        "source": " Books to Scrape ",
        "source_url": "https://books.toscrape.com/catalogue/a_1/index.html",
        "name_or_title": "  Example   Book ",
        "price": "£10.99",
        "rating": "4",
        "author": None,
        "tags": [" one ", "two"],
        "description": " In stock ",
    })
    assert record["source"] == "Books to Scrape"
    assert record["name_or_title"] == "Example Book"
    assert record["price"] == 10.99
    assert record["tags"] == "one, two"


def test_validation():
    valid = {
        "source": "Quotes to Scrape",
        "source_url": "https://quotes.toscrape.com/",
        "name_or_title": "A quote",
        "rating": None,
    }
    assert validate_record(valid)[0] is True

    invalid = dict(valid, source_url="not-a-url")
    assert validate_record(invalid)[0] is False


def test_deduplication():
    records = [
        {"source": "Books to Scrape", "name_or_title": " Example Book ", "author": None},
        {"source": "Books to Scrape", "name_or_title": "EXAMPLE BOOK", "author": None},
        {"source": "Quotes to Scrape", "name_or_title": "Example Book", "author": None},
    ]
    unique, duplicates = deduplicate(records)
    assert len(unique) == 2
    assert duplicates == 1
