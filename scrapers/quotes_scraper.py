from datetime import datetime, timezone
from typing import Iterator, Dict, Any
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .base import BaseScraper

BASE_URL = "https://quotes.toscrape.com/"
START_URL = BASE_URL


class QuotesScraper(BaseScraper):
    """Scrapes all available pages from Quotes to Scrape."""

    def scrape(self) -> Iterator[Dict[str, Any]]:
        url = START_URL
        page_number = 0

        while url:
            page_number += 1
            html = self.fetch(url)
            soup = BeautifulSoup(html, "html.parser")

            for quote in soup.select("div.quote"):
                text_el = quote.select_one("span.text")
                author_el = quote.select_one("small.author")
                tag_els = quote.select("a.tag")

                if not text_el:
                    continue

                yield {
                    "source": "Quotes to Scrape",
                    "source_url": url,
                    "name_or_title": text_el.get_text(" ", strip=True),
                    "category": None,
                    "price": None,
                    "rating": None,
                    "author": author_el.get_text(" ", strip=True) if author_el else None,
                    "tags": [x.get_text(" ", strip=True) for x in tag_els],
                    "description": None,
                    "scraped_at": datetime.now(timezone.utc).isoformat(),
                    "_page": page_number,
                }

            next_link = soup.select_one("li.next a")
            url = urljoin(url, next_link.get("href")) if next_link and next_link.get("href") else None
