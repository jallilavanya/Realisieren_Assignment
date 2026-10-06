from typing import Dict, Any, List, Tuple
from urllib.parse import urlparse

REQUIRED_FIELDS = ("source", "source_url", "name_or_title")


def validate_record(record: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors = []

    for field in REQUIRED_FIELDS:
        if not record.get(field):
            errors.append(f"missing:{field}")

    if record.get("price") is not None and not isinstance(record["price"], (int, float)):
        errors.append("invalid:price")

    if record.get("rating") is not None:
        if not isinstance(record["rating"], (int, float)) or not 0 <= record["rating"] <= 5:
            errors.append("invalid:rating")

    if record.get("source_url"):
        parsed = urlparse(record["source_url"])
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            errors.append("invalid:source_url")

    return not errors, errors
