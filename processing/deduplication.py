import re
import unicodedata
from typing import Dict, Any, List, Tuple


def canonical_text(value: Any) -> str:
    text = "" if value is None else str(value)
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"\s+", " ", text).strip().casefold()
    return text


def duplicate_key(record: Dict[str, Any]) -> Tuple[str, str, str]:
    """
    Primary identity:
      - source: prevents unrelated records from different sources colliding
      - normalized title/text
      - normalized author, when available

    This is deterministic and intentionally conservative. A cross-source
    record is not treated as a duplicate solely because its text matches.
    """
    return (
        canonical_text(record.get("source")),
        canonical_text(record.get("name_or_title")),
        canonical_text(record.get("author")),
    )


def deduplicate(records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int]:
    seen = set()
    unique = []
    duplicates = 0

    for record in records:
        key = duplicate_key(record)
        if key in seen:
            duplicates += 1
            continue
        seen.add(key)
        unique.append(record)

    return unique, duplicates
