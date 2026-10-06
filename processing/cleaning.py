import re
from typing import Any, Dict, Optional
from urllib.parse import urlparse

from decimal import Decimal, InvalidOperation


def clean_text(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, list):
        value = ", ".join(str(x) for x in value)
    text = re.sub(r"\s+", " ", str(value)).strip()
    return text or None


def normalize_title(value: Any) -> Optional[str]:
    text = clean_text(value)
    if not text:
        return None
    return re.sub(r"\s+", " ", text).casefold()


def parse_price(value: Any) -> Optional[float]:
    text = clean_text(value)
    if not text:
        return None
    cleaned = re.sub(r"[^0-9.\-]", "", text)
    if not cleaned:
        return None
    try:
        return float(Decimal(cleaned))
    except InvalidOperation:
        return None


def normalize_rating(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    try:
        rating = float(value)
    except (TypeError, ValueError):
        return None
    return rating


def normalize_url(value: Any) -> Optional[str]:
    text = clean_text(value)
    if not text:
        return None
    parsed = urlparse(text)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return None
    return text


def clean_record(record: Dict[str, Any]) -> Dict[str, Any]:
    tags = record.get("tags")
    if isinstance(tags, list):
        tags = ", ".join(clean_text(x) or "" for x in tags)

    return {
        "source": clean_text(record.get("source")),
        "source_url": normalize_url(record.get("source_url")),
        "name_or_title": clean_text(record.get("name_or_title")),
        "category": clean_text(record.get("category")),
        "price": parse_price(record.get("price")),
        "rating": normalize_rating(record.get("rating")),
        "author": clean_text(record.get("author")),
        "tags": clean_text(tags),
        "description": clean_text(record.get("description")),
        "scraped_at": clean_text(record.get("scraped_at")),
    }
