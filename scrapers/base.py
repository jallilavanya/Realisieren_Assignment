from abc import ABC, abstractmethod
from typing import Iterator, Dict, Any
import requests


class BaseScraper(ABC):
    """Common HTTP behavior for source-specific scrapers."""

    def __init__(self, timeout: int = 15, retries: int = 2):
        self.timeout = timeout
        self.retries = retries
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "scraping-assignment/1.0 (educational; respectful-rate-limit)"
        })

    def fetch(self, url: str) -> str:
        last_error = None
        for attempt in range(self.retries + 1):
            try:
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                return response.text
            except requests.RequestException as exc:
                last_error = exc
                if attempt < self.retries:
                    continue
        raise last_error

    @abstractmethod
    def scrape(self) -> Iterator[Dict[str, Any]]:
        raise NotImplementedError
